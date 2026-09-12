# SE4095 Assignment 01 — Part A

## Dataset and representation

**Dataset:** Political Blogs Network (`data/polblogs.gml`), downloaded from Mark
Newman's Network Data collection on 12 September 2026. The network describes
hyperlinks among US political blogs. A directed edge `u → v` means blog `u`
contains a hyperlink to blog `v`; direction therefore distinguishes outbound
referencing from inbound attention. Edge records contain no weight, so each
distinct directed pair is assigned weight 1.

| Item | Meaning / decision |
|---|---|
| Node identifier | GML `id` (integer; retained as the NetworkX node key) |
| Blog identifier | GML `label` (blog domain/name; unique in this file) |
| Ground truth | GML `value` (binary political orientation; retained but **not used** in cleaning, plots, or any later community-detection choice) |
| Other node attribute | `source`: directory/directories from which the blog was obtained |
| Edge | A directed hyperlink from `source` to `target` |
| Raw GML declaration | `directed 1` |
| Analysis representation | Unweighted, simple `networkx.DiGraph` |

The raw data are directed because a link from A to B does not imply a link from
B to A. They are unweighted because the edge blocks have no weight field and a
distinct pair only records link presence. The raw edge *stream* has repeated
pairs, so it cannot be treated as a simple graph until those repeats are
collapsed.

## Preprocessing log

| Check/action | Result |
|---|---:|
| Raw nodes parsed | 1,490 |
| Raw directed edge records parsed | 19,090 |
| Nodes with missing `label`, `value`, or `source` | 0, 0, 0 |
| Self-loop records | 3 |
| Repeated directed edge records beyond first occurrence | 65 |
| Action | Collapse exact repeated `source → target` pairs, then remove self-loops; retain all nodes |
| Nodes removed | 0 |
| Edges removed as duplicates | 65 |
| Edges removed as self-loops after deduplication | 3 |
| Analysis graph | 1,490 nodes; 19,022 distinct directed edges |

No nodes, isolates, or disconnected components were removed: removing them
would change the observed system. Duplicate records are collapsed because the
network is an unweighted link-presence graph. The three remaining self-loops
are removed because a blog linking to itself provides no relationship between
two blogs and can artificially increase degree-based scores.

## Graph profile of the analysis graph

| Property | Value |
|---|---:|
| Nodes | 1,490 |
| Directed edges | 19,022 |
| Directed density `m / [n(n−1)]` | 0.008574 |
| Isolates (in-degree = out-degree = 0) | 266 |
| Weakly connected components | 268 |
| Largest weak component | 1,222 nodes (82.01%) |
| Strongly connected components | 688 |
| Largest strongly connected component | 793 nodes (53.22%) |
| Mean in-degree | 12.766 |
| Mean out-degree | 12.766 |
| Median in-degree | 2.0 |
| Median out-degree | 4.0 |
| Maximum in-degree | 337 |
| Maximum out-degree | 256 |

The degree distribution is plotted in `degree_distribution.png`; zero degrees
are included in the linear histogram and excluded only from the logarithmic
view because `log(0)` is undefined. `network_overview.png` is a readable
induced visualization of the 200 highest-total-degree blogs, not a calculation
subset. It encodes total degree through node size and the out-degree minus
in-degree balance through colour, **not** the political label. Arrowheads are omitted
only in the visualization to keep the dense graph readable; all calculations
remain directed.

## Interpretation

The graph is sparse: only a very small fraction of all possible ordered blog
pairs have a hyperlink. Compare its weak and strong component counts: weak
connectivity asks whether direction can be ignored for reachability, whereas
strong connectivity requires mutually directed paths. A much smaller largest
strong component would indicate that links create broad reference pathways
without universal two-way navigability. The in/out-degree plot shows whether a
small number of blogs receive disproportionate attention (high in-degree) and
whether outbound linking is concentrated among relatively few blogs. Such
asymmetry is consistent with a hyperlink ecosystem containing hubs, brokers,
and many peripheral blogs. Political homophily will be tested later through
community detection and evaluation only; it is not assumed here from `value`.

## Distance convention for later stages

No distance-based statistic is calculated in Part A. For any directed distance
measure in later stages, use the largest strongly connected component and the
edge direction `u → v` as the route from a linking blog to the linked blog.
This avoids undefined directed distances between unreachable nodes and retains
the information-flow/reference direction represented by a hyperlink. State
explicitly if a later method instead uses the undirected projection, and why.

## Reproducibility

Run `python part_a_analysis.py` from the assignment folder. It regenerates this
report, `graph_profile.json`, `degree_distribution.png`, `network_overview.png`,
and `degree_summary.csv` from `data/polblogs.gml`.
