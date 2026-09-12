"""Run only Assignment Part C: python part_c_analysis.py."""
from pathlib import Path
import json, math
import numpy as np
import network_analysis_core as shared

OUT = Path(__file__).resolve().parent / "part_c_output"

def main():
    OUT.mkdir(exist_ok=True)
    graph = shared.load_analysis_graph()
    _, _, bc_norm, _, bc_order = shared.rankings(graph)
    count = math.ceil(shared.REMOVAL_FRACTION * graph.number_of_nodes())
    targeted = bc_order[:count]
    rng = np.random.default_rng(shared.RANDOM_REMOVAL_SEED)
    random_nodes = rng.choice(list(graph), size=count, replace=False).tolist()
    targeted_graph = graph.copy(); targeted_graph.remove_nodes_from(targeted)
    random_graph = graph.copy(); random_graph.remove_nodes_from(random_nodes)
    results = [shared.graph_comparison("Original", graph), shared.graph_comparison("Betweenness-targeted", targeted_graph), shared.graph_comparison("Random control", random_graph)]
    original, intervention, random_control = results
    payload = {"settings":{"removal_fraction":shared.REMOVAL_FRACTION,"random_seed":shared.RANDOM_REMOVAL_SEED,"louvain_seed":shared.LOUVAIN_SEED},"removed_nodes":targeted,"comparisons":results}
    (OUT / "experiment_results.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    report = f"""# SE4095 Assignment 01 - Part C

This script uses the betweenness ranking selected in Part B. It never reads `value` until after label-free Louvain detection, when evaluation metrics are calculated.

## Controlled experiment

Remove the top **{count} ({shared.REMOVAL_FRACTION:.0%})** directed-betweenness brokers, then compare with {count} randomly removed nodes using seed `{shared.RANDOM_REMOVAL_SEED}`. Each graph uses the same Louvain modularity-maximization settings on the unweighted undirected link-presence projection: resolution 1.0, threshold `1e-7`, seed `{shared.LOUVAIN_SEED}`.

| Graph | Nodes | Edges | Weak components | Communities | Modularity | Accuracy | F1 label 1 |
|---|---:|---:|---:|---:|---:|---:|---:|
""" + "\n".join(f"| {x['name']} | {x['nodes']} | {x['edges']} | {x['weak_components']} | {x['community_count']} | {x['modularity']:.4f} | {x['evaluation']['accuracy']:.4f} | {x['evaluation']['f1_label_1']:.4f} |" for x in results) + f"""

Targeted removal deletes {original['edges']-intervention['edges']:,} links and raises weak components from {original['weak_components']} to {intervention['weak_components']}; random removal deletes {original['edges']-random_control['edges']:,} links and leaves {random_control['weak_components']} components. Targeted removal lowers F1 from {original['evaluation']['f1_label_1']:.4f} to {intervention['evaluation']['f1_label_1']:.4f}, while random removal is {random_control['evaluation']['f1_label_1']:.4f}. The modest modularity increase after targeting should not be read as improvement: fragmentation can remove between-community ties.
"""
    (OUT / "part_c_report.md").write_text(report, encoding="utf-8")

if __name__ == "__main__": main()
