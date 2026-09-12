"""SE4095 Assignment 01, Part E. Run: python part_e_analysis.py"""
from pathlib import Path
from collections import Counter
from math import comb, ceil
import json
import numpy as np
import network_analysis_core as core

OUT=Path(__file__).resolve().parent/'part_e_output'

def ratio(n,d):
    return None if d==0 else n/d

def pairwise_evaluation(graph, communities, modularity):
    """Ground truth is accessed here only, after the Louvain partition exists."""
    label={v:graph.nodes[v]['value'] for v in graph}
    # Each Louvain node is in one disjoint community.  Pair counts are obtained
    # combinatorially, without comparing a community number to a label value.
    tp=fp=0
    for group in communities:
        counts=Counter(label[v] for v in group)
        tp+=sum(comb(counts[x],2) for x in (0,1))
        fp+=counts[0]*counts[1]
    total_same_truth=sum(comb(sum(1 for v in graph if label[v]==x),2) for x in (0,1))
    total_pairs=comb(len(graph),2)
    fn=total_same_truth-tp
    tn=total_pairs-tp-fp-fn
    precision=ratio(tp,tp+fp); recall=ratio(tp,tp+fn)
    f1=None if precision is None or recall is None or precision+recall==0 else 2*precision*recall/(precision+recall)
    return {'tp':tp,'tn':tn,'fp':fp,'fn':fn,'accuracy':ratio(tp+tn,total_pairs),'precision':precision,'recall':recall,'f1':f1,'modularity':modularity}

def detect_and_score(name, graph):
    projection, communities, modularity=core.detect_louvain(graph)
    return {'name':name,'nodes':len(graph),'edges':graph.number_of_edges(),'community_count':len(communities),'community_sizes':[len(c) for c in communities], **pairwise_evaluation(graph,communities,modularity)}

def f(x): return 'undefined' if x is None else f'{x:.6f}'

def main():
    OUT.mkdir(exist_ok=True)
    graph=core.load_analysis_graph()
    _,_,bc,_,order=core.rankings(graph)
    n=ceil(core.REMOVAL_FRACTION*len(graph)); targeted=graph.copy(); targeted.remove_nodes_from(order[:n])
    rng=np.random.default_rng(core.RANDOM_REMOVAL_SEED); random_graph=graph.copy(); random_graph.remove_nodes_from(rng.choice(list(graph),size=n,replace=False))
    results=[detect_and_score('Original',graph),detect_and_score('Betweenness-targeted',targeted),detect_and_score('Random control',random_graph)]
    (OUT/'pairwise_evaluation.json').write_text(json.dumps({'louvain_seed':core.LOUVAIN_SEED,'random_removal_seed':core.RANDOM_REMOVAL_SEED,'results':results},indent=2),encoding='utf-8')
    rows='\n'.join(f"| {r['name']} | {r['tp']:,} | {r['tn']:,} | {r['fp']:,} | {r['fn']:,} | {f(r['accuracy'])} | {f(r['precision'])} | {f(r['recall'])} | {f(r['f1'])} | {r['modularity']:.6f} |" for r in results)
    report=f"""# SE4095 Assignment 01 - Part E

## Evaluation design and label-permutation control

The political-orientation `value` attribute is used **only now**, after the three Louvain partitions have been detected. Louvain communities are disjoint, so two nodes are judged to be in the same detected community exactly when they have the same detected membership. Community IDs are arbitrary, therefore they are never compared directly to 0/1 labels. Instead, every unordered pair of remaining nodes is classified by two independent yes/no questions: same detected community and same ground-truth orientation. This makes the result invariant to any permutation or renaming of community IDs. There are no unassigned nodes in Louvain; isolates are singleton communities and therefore remain included.

Louvain uses the same label-free settings for all graphs: unweighted undirected link-presence projection, resolution 1.0, threshold `1e-7`, and seed {core.LOUVAIN_SEED}. The targeted graph removes the top {n} directed-betweenness nodes from Part B; the random control removes {n} nodes using seed {core.RANDOM_REMOVAL_SEED}. Each removal graph is evaluated only on its remaining nodes.

## Pairwise confusion matrices and metrics

For each graph, TP = same detected community and same orientation; TN = different detected communities and different orientations; FP = same detected community but different orientation; FN = different detected communities but same orientation.

| Graph | TP | TN | FP | FN | Accuracy | Precision | Recall | F1 | Modularity |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{rows}

All denominators in this run are non-zero, so no metric is undefined. If `TP+FP` were zero, precision would be reported as undefined; if `TP+FN` were zero, recall would be undefined; and F1 would be undefined whenever precision or recall is undefined (or their sum is zero). Standard modularity is defined because the Louvain partition is disjoint and the reported score is calculated on its undirected projection.

## Interpretation

Pairwise precision asks: among pairs placed together by the detected structure, what proportion truly share political orientation? In this hyperlink network, high precision means within-community linking tends to be politically homogeneous. Pairwise recall asks: among all same-orientation pairs of remaining blogs, what proportion Louvain puts together? Low recall can occur even when precision is high because one political orientation can legitimately split into multiple topical, regional, or stylistic hyperlink communities.

Strong structural communities can still disagree with political orientation because hyperlinks reflect more than ideology: blogs may link around a shared issue, media source, campaign event, audience, or brokerage relationship that crosses orientation. Thus modularity measures internal edge concentration, whereas the pairwise metrics measure alignment with this specific external political label; neither guarantees the other.
"""
    (OUT/'part_e_report.md').write_text(report,encoding='utf-8')

if __name__=='__main__': main()
