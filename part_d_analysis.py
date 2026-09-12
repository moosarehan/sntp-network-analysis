"""SE4095 Assignment 01, Part D. Run: python part_d_analysis.py"""
from pathlib import Path
from collections import Counter
import csv, json
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import network_analysis_core as shared

OUT = Path(__file__).resolve().parent / "part_d_output"
SEEDS = [4095, 100, 200, 300, 400]
VISUAL_SEED = 4095

def detect(graph, seed):
    """Label-free Louvain on an undirected link-presence projection."""
    projection = nx.Graph(graph)
    communities = nx.community.louvain_communities(projection, weight=None, resolution=1.0, threshold=1e-7, seed=seed)
    communities = sorted((set(c) for c in communities), key=lambda c: (-len(c), min(c)))
    return projection, communities, nx.community.modularity(projection, communities, weight=None, resolution=1.0)

def evaluate(graph, communities):
    """Evaluation-only label read, after community memberships are fixed."""
    labels = {v: graph.nodes[v]['value'] for v in graph}
    pred = {}
    for c in communities:
        counts = Counter(labels[v] for v in c)
        winner = max((counts[x], -x, x) for x in (0, 1))[2]
        pred.update({v: winner for v in c})
    cm = [[0,0],[0,0]]
    for v in graph: cm[labels[v]][pred[v]] += 1
    tn, fp = cm[0]; fn, tp = cm[1]
    precision = tp/(tp+fp) if tp+fp else 0; recall = tp/(tp+fn) if tp+fn else 0
    return {'accuracy':(tn+tp)/len(graph), 'precision_label_1':precision, 'recall_label_1':recall,
            'f1_label_1':2*precision*recall/(precision+recall) if precision+recall else 0, 'cm':cm}

def main():
    OUT.mkdir(exist_ok=True)
    graph = shared.load_analysis_graph()
    pagerank, bc_raw, bc_norm, pr_order, _ = shared.rankings(graph)
    runs=[]; chosen=None
    for seed in SEEDS:
        projection, communities, modularity = detect(graph, seed)
        result={'seed':seed, 'communities':len(communities), 'sizes':[len(c) for c in communities], 'modularity':modularity, **evaluate(graph, communities)}
        runs.append(result)
        if seed == VISUAL_SEED: chosen=(projection, communities, result)
    metrics=['accuracy','precision_label_1','recall_label_1','f1_label_1']
    means={m:float(np.mean([r[m] for r in runs])) for m in metrics}; sds={m:float(np.std([r[m] for r in runs], ddof=1)) for m in metrics}
    projection, communities, selected = chosen
    memberships={v:i+1 for i,c in enumerate(communities) for v in c}
    major=[]
    for i,c in enumerate(communities,1):
        if len(c) < 10: continue
        top_pr=max(c,key=lambda v:pagerank[v]); top_bc=max(c,key=lambda v:bc_norm[v])
        major.append({'community':i,'size':len(c),'share_percent':100*len(c)/len(graph),'mean_pagerank':float(np.mean([pagerank[v] for v in c])), 'mean_betweenness':float(np.mean([bc_norm[v] for v in c])), 'top_pagerank_blog':graph.nodes[top_pr]['label'], 'top_betweenness_blog':graph.nodes[top_bc]['label']})
    with (OUT/'major_community_profiles.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=major[0].keys()); w.writeheader(); w.writerows(major)
    # Readable sample: top 200 selected PageRank nodes, not political labels.
    nodes=pr_order[:200]; visual=projection.subgraph(nodes); pos=nx.spring_layout(visual,seed=VISUAL_SEED,k=.22,iterations=100)
    fig,ax=plt.subplots(figsize=(12,9)); nx.draw_networkx_edges(visual,pos,ax=ax,edge_color='#777777',alpha=.14,width=.3)
    nx.draw_networkx_nodes(visual,pos,ax=ax,node_size=[14+4*np.sqrt(projection.degree(v)) for v in visual],node_color=[memberships[v] for v in visual],cmap='tab20',alpha=.85,linewidths=0)
    ax.set_title('Louvain communities: top 200 PageRank blogs (seed 4095)\nColour = detected community; labels are not used'); ax.set_axis_off()
    fig.savefig(OUT/'community_network.png',dpi=220,bbox_inches='tight'); plt.close(fig)
    payload={'seeds':SEEDS,'visual_seed':VISUAL_SEED,'parameters':{'projection':'unweighted undirected link-presence','resolution':1.0,'threshold':1e-7},'runs':runs,'evaluation_mean':means,'evaluation_sd':sds,'major_communities':major}
    (OUT/'community_results.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
    table='\n'.join(f"| {r['seed']} | {r['communities']} | {r['modularity']:.4f} | {r['accuracy']:.4f} | {r['precision_label_1']:.4f} | {r['recall_label_1']:.4f} | {r['f1_label_1']:.4f} |" for r in runs)
    profiles='\n'.join(f"| {r['community']} | {r['size']} | {r['share_percent']:.2f}% | {r['mean_pagerank']:.6f} | {r['mean_betweenness']:.6f} | {r['top_pagerank_blog']} | {r['top_betweenness_blog']} |" for r in major)
    report=f"""# SE4095 Assignment 01 - Part D

## Method choice

I use **Louvain modularity maximization**, a taught method for finding disjoint, non-overlapping groups whose within-group edge density is high relative to the modularity null model. This fits a political-blog hyperlink network where the goal is a partition rather than overlapping affiliations. Louvain is stochastic and does not require choosing a community count from the political labels. Standard Louvain modularity is undirected, so each cleaned directed hyperlink is transformed into an unweighted undirected link-presence tie; reciprocal hyperlinks become one tie. Direction is retained in Part B centrality, but the transformation is required and stated for this community method. The `value` label is never read until after a partition is detected for evaluation.

Parameters: resolution 1.0, modularity threshold `1e-7`, unweighted undirected projection, seeds {SEEDS}. Declared visualization run: seed {VISUAL_SEED}.

## Five-seed results

| Seed | Communities | Modularity | Accuracy | Precision (label 1) | Recall (label 1) | F1 (label 1) |
|---:|---:|---:|---:|---:|---:|---:|
{table}

Mean (SD) across seeds: accuracy {means['accuracy']:.4f} ({sds['accuracy']:.4f}); precision {means['precision_label_1']:.4f} ({sds['precision_label_1']:.4f}); recall {means['recall_label_1']:.4f} ({sds['recall_label_1']:.4f}); F1 {means['f1_label_1']:.4f} ({sds['f1_label_1']:.4f}).

For the declared seed {VISUAL_SEED}, Louvain detects {selected['communities']} communities. Its size distribution is {selected['sizes']}; most singleton communities correspond to isolates or tiny disconnected pieces retained from Part A. Modularity is {selected['modularity']:.4f}. The confusion matrix (true rows 0/1; post-detection majority-mapped predicted columns 0/1) is {selected['cm']}.

## Major-community profiles

Only communities of size at least 10 are profiled. Mean PageRank and normalized directed betweenness are the two Part B measures; no extra centrality is used.

| Community | Size | Share | Mean PageRank | Mean betweenness | Highest PageRank blog | Highest betweenness blog |
|---:|---:|---:|---:|---:|---|---|
{profiles}

The community-colored figure is `community_network.png`. It samples the 200 highest-PageRank blogs solely for readability; calculations and detection use all 1,490 nodes. Colours encode Louvain membership, never political ground truth.
"""
    (OUT/'part_d_report.md').write_text(report,encoding='utf-8')

if __name__=='__main__': main()
