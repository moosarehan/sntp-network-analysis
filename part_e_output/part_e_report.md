# SE4095 Assignment 01 - Part E

## Evaluation design and label-permutation control

The political-orientation `value` attribute is used **only now**, after the three Louvain partitions have been detected. Louvain communities are disjoint, so two nodes are judged to be in the same detected community exactly when they have the same detected membership. Community IDs are arbitrary, therefore they are never compared directly to 0/1 labels. Instead, every unordered pair of remaining nodes is classified by two independent yes/no questions: same detected community and same ground-truth orientation. This makes the result invariant to any permutation or renaming of community IDs. There are no unassigned nodes in Louvain; isolates are singleton communities and therefore remain included.

Louvain uses the same label-free settings for all graphs: unweighted undirected link-presence projection, resolution 1.0, threshold `1e-7`, and seed 4095. The targeted graph removes the top 15 directed-betweenness nodes from Part B; the random control removes 15 nodes using seed 20260912. Each removal graph is evaluated only on its remaining nodes.

## Pairwise confusion matrices and metrics

For each graph, TP = same detected community and same orientation; TN = different detected communities and different orientations; FP = same detected community but different orientation; FN = different detected communities but same orientation.

| Graph | TP | TN | FP | FN | Accuracy | Precision | Recall | F1 | Modularity |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Original | 314,225 | 529,299 | 25,557 | 240,224 | 0.760408 | 0.924784 | 0.566734 | 0.702783 | 0.427028 |
| Betweenness-targeted | 281,045 | 514,995 | 28,729 | 262,306 | 0.732277 | 0.907258 | 0.517244 | 0.658860 | 0.431097 |
| Random control | 310,564 | 515,312 | 28,412 | 232,787 | 0.759723 | 0.916183 | 0.571572 | 0.703966 | 0.425799 |

All denominators in this run are non-zero, so no metric is undefined. If `TP+FP` were zero, precision would be reported as undefined; if `TP+FN` were zero, recall would be undefined; and F1 would be undefined whenever precision or recall is undefined (or their sum is zero). Standard modularity is defined because the Louvain partition is disjoint and the reported score is calculated on its undirected projection.

## Interpretation

Pairwise precision asks: among pairs placed together by the detected structure, what proportion truly share political orientation? In this hyperlink network, high precision means within-community linking tends to be politically homogeneous. Pairwise recall asks: among all same-orientation pairs of remaining blogs, what proportion Louvain puts together? Low recall can occur even when precision is high because one political orientation can legitimately split into multiple topical, regional, or stylistic hyperlink communities.

Strong structural communities can still disagree with political orientation because hyperlinks reflect more than ideology: blogs may link around a shared issue, media source, campaign event, audience, or brokerage relationship that crosses orientation. Thus modularity measures internal edge concentration, whereas the pairwise metrics measure alignment with this specific external political label; neither guarantees the other.
