# SE4095 Assignment 01 - Part D

## Method choice

I use **Louvain modularity maximization**, a taught method for finding disjoint, non-overlapping groups whose within-group edge density is high relative to the modularity null model. This fits a political-blog hyperlink network where the goal is a partition rather than overlapping affiliations. Louvain is stochastic and does not require choosing a community count from the political labels. Standard Louvain modularity is undirected, so each cleaned directed hyperlink is transformed into an unweighted undirected link-presence tie; reciprocal hyperlinks become one tie. Direction is retained in Part B centrality, but the transformation is required and stated for this community method. The `value` label is never read until after a partition is detected for evaluation.

Parameters: resolution 1.0, modularity threshold `1e-7`, unweighted undirected projection, seeds [4095, 100, 200, 300, 400]. Declared visualization run: seed 4095.

## Five-seed results

| Seed | Communities | Modularity | Accuracy | Precision (label 1) | Recall (label 1) | F1 (label 1) |
|---:|---:|---:|---:|---:|---:|---:|
| 4095 | 278 | 0.4270 | 0.9624 | 0.9580 | 0.9658 | 0.9619 |
| 100 | 277 | 0.4253 | 0.9570 | 0.9430 | 0.9713 | 0.9569 |
| 200 | 278 | 0.4270 | 0.9604 | 0.9578 | 0.9617 | 0.9598 |
| 300 | 277 | 0.4264 | 0.9597 | 0.9565 | 0.9617 | 0.9591 |
| 400 | 278 | 0.4271 | 0.9604 | 0.9591 | 0.9604 | 0.9597 |

Mean (SD) across seeds: accuracy 0.9600 (0.0019); precision 0.9549 (0.0067); recall 0.9642 (0.0045); F1 0.9595 (0.0018).

For the declared seed 4095, Louvain detects 278 communities. Its size distribution is [632, 529, 38, 5, 4, 3, 3, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]; most singleton communities correspond to isolates or tiny disconnected pieces retained from Part A. Modularity is 0.4270. The confusion matrix (true rows 0/1; post-detection majority-mapped predicted columns 0/1) is [[727, 31], [25, 707]].

## Major-community profiles

Only communities of size at least 10 are profiled. Mean PageRank and normalized directed betweenness are the two Part B measures; no extra centrality is used.

| Community | Size | Share | Mean PageRank | Mean betweenness | Highest PageRank blog | Highest betweenness blog |
|---:|---:|---:|---:|---:|---|---|
| 1 | 632 | 42.42% | 0.000786 | 0.000839 | instapundit.com | blogsforbush.com |
| 2 | 529 | 35.50% | 0.000821 | 0.000975 | dailykos.com | atrios.blogspot.com |
| 3 | 38 | 2.55% | 0.000308 | 0.000169 | etalkinghead.com | theblueview.blogspot.com |

The community-colored figure is `community_network.png`. It samples the 200 highest-PageRank blogs solely for readability; calculations and detection use all 1,490 nodes. Colours encode Louvain membership, never political ground truth.
