# SE4095 Assignment 01 - Part F: Reproducibility and reflection

## Reproducibility

The complete analysis is runnable from top to bottom with:

```powershell
python run_all_parts.py
```

The equivalent notebook is `SE4095_assignment.ipynb`; run its cells in order.
The raw input is `data/polblogs.gml`. Part A parses and cleans it; the
separate Part B, C, D, and E scripts perform centrality, intervention,
community detection, and post-detection evaluation. `network_analysis_core.py`
contains shared graph functions only, avoiding duplicated transformations.

Fixed settings are recorded in code and reports: PageRank alpha 0.85, tolerance
`1e-10`, maximum 1,000 iterations; random-removal seed 20260912; Louvain seeds
4095, 100, 200, 300, and 400; and visualization seed 4095. All layouts also
use fixed seeds. Each part writes its own report and machine-readable output to
its own output folder.

## Conclusion and limitations

The directed hyperlink structure identifies different structural roles: PageRank
highlights authorities receiving discounted incoming attention, while
betweenness identifies brokers on directed shortest routes. Louvain on the
label-free undirected link-presence projection recovers political orientation
well in pairwise precision (0.9248) but only moderate pairwise recall (0.5667),
showing that same-orientation blogs are not necessarily one structural group.
Removing the top 1% betweenness brokers increases fragmentation and lowers
pairwise F1 from 0.7028 to 0.6589, whereas the seeded random control remains
near 0.7040. This supports the limited conclusion that the identified brokers
help maintain the observed hyperlink-community structure.

The data describe a historical political-blog ecosystem around the 2004 US
election, not current political communication. A hyperlink can be criticism,
quotation, monitoring, navigation, or endorsement; it is not proof of support,
influence, readership, or causal political importance. The GML labels are also
binary and external to the link structure. Louvain requires an undirected
projection, has a resolution limit, and its stochastic variation is reported
but not exhaustively sampled. The targeted-versus-one-random-control comparison
is an experiment on recorded topology, not causal evidence about real people or
political effects.
