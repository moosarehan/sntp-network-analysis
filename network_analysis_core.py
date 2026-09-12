"""Shared graph utilities; this is not an assignment-part submission script."""
from collections import Counter
import re
import networkx as nx
import numpy as np
from part_a_analysis import GML_PATH, parse_polblogs

PAGERANK_ALPHA=.85; PAGERANK_TOL=1e-10; PAGERANK_MAX_ITER=1000
LOUVAIN_SEED=4095; RANDOM_REMOVAL_SEED=20260912; REMOVAL_FRACTION=.01

def load_analysis_graph():
    nodes, raw=parse_polblogs(GML_PATH); edges=list(dict.fromkeys(raw))
    g=nx.DiGraph(); g.add_nodes_from(nodes.items()); g.add_edges_from((u,v) for u,v in edges if u!=v); return g

def rankings(g):
    pr=nx.pagerank(g,alpha=PAGERANK_ALPHA,tol=PAGERANK_TOL,max_iter=PAGERANK_MAX_ITER,dangling=None)
    raw=nx.betweenness_centrality(g,normalized=False,endpoints=False,weight=None)
    norm=nx.betweenness_centrality(g,normalized=True,endpoints=False,weight=None)
    return pr,raw,norm,sorted(g,key=lambda v:(-pr[v],v)),sorted(g,key=lambda v:(-norm[v],v))

def average_ranks(scores):
    order=sorted(scores,key=lambda v:(-scores[v],v)); result={}; start=0
    while start<len(order):
        end=start+1
        while end<len(order) and scores[order[end]]==scores[order[start]]: end+=1
        rank=(start+1+end)/2
        for v in order[start:end]: result[v]=rank
        start=end
    return result

def spearman_from_ranks(a,b):
    return float(np.corrcoef([a[v] for v in a],[b[v] for v in a])[0,1])

def top_ten_rows(g,pr,raw,norm,order,measure):
    return [{'rank':i,'node_id':v,'label':g.nodes[v]['label'],'raw_score':pr[v] if measure=='pagerank' else raw[v],'normalized_score':pr[v] if measure=='pagerank' else norm[v]} for i,v in enumerate(order[:10],1)]

def markdown_table(rows,fields):
    text='| '+' | '.join(fields)+' |\n|'+'|'.join(['---']*len(fields))+'|\n'
    for r in rows: text+='| '+' | '.join(f"{r[x]:.10f}" if isinstance(r[x],float) else str(r[x]) for x in fields)+' |\n'
    return text

def detect_louvain(g):
    p=nx.Graph(g); c=nx.community.louvain_communities(p,weight=None,resolution=1.0,threshold=1e-7,seed=LOUVAIN_SEED); c=sorted((set(x) for x in c),key=lambda x:(-len(x),min(x))); return p,c,nx.community.modularity(p,c,weight=None,resolution=1.0)

def evaluate_after_detection(g,c):
    labels={v:g.nodes[v]['value'] for v in g}; pred={}
    for group in c:
        counts=Counter(labels[v] for v in group); winner=max((counts[x],-x,x) for x in (0,1))[2]; pred.update({v:winner for v in group})
    cm=[[0,0],[0,0]]
    for v in g: cm[labels[v]][pred[v]]+=1
    tn,fp=cm[0]; fn,tp=cm[1]; precision=tp/(tp+fp) if tp+fp else 0; recall=tp/(tp+fn) if tp+fn else 0
    return {'confusion_matrix':cm,'accuracy':(tn+tp)/len(g),'precision_label_1':precision,'recall_label_1':recall,'f1_label_1':2*precision*recall/(precision+recall) if precision+recall else 0}

def graph_comparison(name,g):
    _,c,q=detect_louvain(g); ev=evaluate_after_detection(g,c); w=sorted((len(x) for x in nx.weakly_connected_components(g)),reverse=True); s=sorted((len(x) for x in nx.strongly_connected_components(g)),reverse=True)
    return {'name':name,'nodes':len(g),'edges':g.number_of_edges(),'weak_components':len(w),'largest_weak':w[0],'strong_components':len(s),'largest_strong':s[0],'community_count':len(c),'community_sizes':[len(x) for x in c],'largest_community':len(c[0]),'modularity':q,'evaluation':ev}
