# SE4095 Assignment 01 - Part C

This script uses the betweenness ranking selected in Part B. It never reads `value` until after label-free Louvain detection, when evaluation metrics are calculated.

## Controlled experiment

Remove the top **15 (1%)** directed-betweenness brokers, then compare with 15 randomly removed nodes using seed `20260912`. Each graph uses the same Louvain modularity-maximization settings on the unweighted undirected link-presence projection: resolution 1.0, threshold `1e-7`, seed `4095`.

| Graph | Nodes | Edges | Weak components | Communities | Modularity | Accuracy | F1 label 1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original | 1490 | 19022 | 268 | 278 | 0.4270 | 0.9624 | 0.9619 |
| Betweenness-targeted | 1475 | 15219 | 301 | 311 | 0.4311 | 0.9546 | 0.9540 |
| Random control | 1475 | 18706 | 266 | 275 | 0.4258 | 0.9620 | 0.9617 |

Targeted removal deletes 3,803 links and raises weak components from 268 to 301; random removal deletes 316 links and leaves 266 components. Targeted removal lowers F1 from 0.9619 to 0.9540, while random removal is 0.9617. The modest modularity increase after targeting should not be read as improvement: fragmentation can remove between-community ties.
