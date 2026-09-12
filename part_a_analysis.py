"""SE4095 Assignment 01, Part A: Political Blogs graph construction and profile.

Run from this folder with:  python part_a_analysis.py

The parser is deliberately small because NetworkX's GML reader rejects this
particular file when it encounters its duplicate directed edge records.  The
file is parsed first as a raw edge stream so that duplicates can be reported,
then converted to a simple DiGraph for all stated Part A calculations.
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


ROOT = Path(__file__).resolve().parent
GML_PATH = ROOT / "data" / "polblogs.gml"
OUT = ROOT / "part_a_output"


def field(block: str, name: str, quoted: bool = False):
    """Extract a scalar GML field from one node/edge block."""
    pattern = rf'\b{name}\s+"([^"]*)"' if quoted else rf"\b{name}\s+(-?\d+)"
    match = re.search(pattern, block)
    return match.group(1) if match else None


def parse_polblogs(path: Path):
    """Return node attributes and the raw ordered directed edge records."""
    text = path.read_text(encoding="utf-8")
    node_blocks = re.findall(r"\bnode\s*\[(.*?)\n\s*\]", text, flags=re.S)
    edge_blocks = re.findall(r"\bedge\s*\[(.*?)\n\s*\]", text, flags=re.S)
    nodes = {}
    for block in node_blocks:
        node_id = int(field(block, "id"))
        nodes[node_id] = {
            "label": field(block, "label", quoted=True),
            "value": int(field(block, "value")),
            "source": field(block, "source", quoted=True),
        }
    edges = [(int(field(block, "source")), int(field(block, "target"))) for block in edge_blocks]
    return nodes, edges


def component_sizes(components):
    return sorted((len(c) for c in components), reverse=True)


def write_report(stats: dict) -> None:
    report = f"""# SE4095 Assignment 01 — Part A

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
| Raw nodes parsed | {stats['raw_nodes']:,} |
| Raw directed edge records parsed | {stats['raw_edges']:,} |
| Nodes with missing `label`, `value`, or `source` | {stats['missing_label']}, {stats['missing_value']}, {stats['missing_source']} |
| Self-loop records | {stats['self_loops']} |
| Repeated directed edge records beyond first occurrence | {stats['duplicate_records']:,} |
| Action | Collapse exact repeated `source → target` pairs, then remove self-loops; retain all nodes |
| Nodes removed | 0 |
| Edges removed as duplicates | {stats['duplicate_records']:,} |
| Edges removed as self-loops after deduplication | {stats['unique_self_loops']:,} |
| Analysis graph | {stats['nodes']:,} nodes; {stats['edges']:,} distinct directed edges |

No nodes, isolates, or disconnected components were removed: removing them
would change the observed system. Duplicate records are collapsed because the
network is an unweighted link-presence graph. The three remaining self-loops
are removed because a blog linking to itself provides no relationship between
two blogs and can artificially increase degree-based scores.

## Graph profile of the analysis graph

| Property | Value |
|---|---:|
| Nodes | {stats['nodes']:,} |
| Directed edges | {stats['edges']:,} |
| Directed density `m / [n(n−1)]` | {stats['density']:.6f} |
| Isolates (in-degree = out-degree = 0) | {stats['isolates']:,} |
| Weakly connected components | {stats['weak_components']:,} |
| Largest weak component | {stats['largest_weak']:,} nodes ({stats['largest_weak_pct']:.2f}%) |
| Strongly connected components | {stats['strong_components']:,} |
| Largest strongly connected component | {stats['largest_strong']:,} nodes ({stats['largest_strong_pct']:.2f}%) |
| Mean in-degree | {stats['mean_in']:.3f} |
| Mean out-degree | {stats['mean_out']:.3f} |
| Median in-degree | {stats['median_in']:.1f} |
| Median out-degree | {stats['median_out']:.1f} |
| Maximum in-degree | {stats['max_in']:,} |
| Maximum out-degree | {stats['max_out']:,} |

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
"""
    (OUT / "part_a_report.md").write_text(report, encoding="utf-8")


def main():
    OUT.mkdir(exist_ok=True)
    nodes, raw_edges = parse_polblogs(GML_PATH)
    unique_edges = list(dict.fromkeys(raw_edges))
    cleaned_edges = [(u, v) for u, v in unique_edges if u != v]
    graph = nx.DiGraph()
    graph.add_nodes_from(nodes.items())
    graph.add_edges_from(cleaned_edges)

    in_degrees = np.array([degree for _, degree in graph.in_degree()])
    out_degrees = np.array([degree for _, degree in graph.out_degree()])
    weak_sizes = component_sizes(nx.weakly_connected_components(graph))
    strong_sizes = component_sizes(nx.strongly_connected_components(graph))
    stats = {
        "raw_nodes": len(nodes), "raw_edges": len(raw_edges),
        "missing_label": sum(a["label"] is None for a in nodes.values()),
        "missing_value": sum(a["value"] is None for a in nodes.values()),
        "missing_source": sum(a["source"] is None for a in nodes.values()),
        "self_loops": sum(u == v for u, v in raw_edges),
        "unique_self_loops": sum(u == v for u, v in unique_edges),
        "duplicate_records": len(raw_edges) - len(set(raw_edges)),
        "nodes": graph.number_of_nodes(), "edges": graph.number_of_edges(),
        "density": nx.density(graph), "isolates": len(list(nx.isolates(graph))),
        "weak_components": len(weak_sizes), "strong_components": len(strong_sizes),
        "largest_weak": weak_sizes[0], "largest_strong": strong_sizes[0],
        "largest_weak_pct": 100 * weak_sizes[0] / graph.number_of_nodes(),
        "largest_strong_pct": 100 * strong_sizes[0] / graph.number_of_nodes(),
        "mean_in": float(in_degrees.mean()), "mean_out": float(out_degrees.mean()),
        "median_in": float(np.median(in_degrees)), "median_out": float(np.median(out_degrees)),
        "max_in": int(in_degrees.max()), "max_out": int(out_degrees.max()),
        "weak_component_sizes": weak_sizes, "strong_component_sizes": strong_sizes,
    }
    (OUT / "graph_profile.json").write_text(json.dumps(stats, indent=2), encoding="utf-8")

    with (OUT / "degree_summary.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["node_id", "blog", "in_degree", "out_degree", "total_degree"])
        for node in graph.nodes:
            writer.writerow([node, graph.nodes[node]["label"], graph.in_degree(node), graph.out_degree(node), graph.degree(node)])

    # Degree figure: inclusive linear histogram plus positive-degree log-log CCDF.
    fig, axes = plt.subplots(1, 2, figsize=(13, 5), constrained_layout=True)
    max_degree = int(max(in_degrees.max(), out_degrees.max()))
    bins = np.arange(max_degree + 2) - 0.5
    axes[0].hist(in_degrees, bins=bins, alpha=0.65, label="in-degree", color="#2878b5")
    axes[0].hist(out_degrees, bins=bins, alpha=0.60, label="out-degree", color="#e07b39")
    axes[0].set_xlim(-0.5, min(max_degree + 0.5, 100))
    axes[0].set_xlabel("Degree (display capped at 100)")
    axes[0].set_ylabel("Number of blogs")
    axes[0].set_title("In- and out-degree distributions")
    axes[0].legend()
    for data, label, colour in [(in_degrees, "in-degree", "#2878b5"), (out_degrees, "out-degree", "#e07b39")]:
        positive = np.sort(data[data > 0])
        ccdf = 1 - np.arange(len(positive)) / len(positive)
        axes[1].step(positive, ccdf, where="post", label=label, color=colour)
    axes[1].set_xscale("log")
    axes[1].set_yscale("log")
    axes[1].set_xlabel("Degree (positive values)")
    axes[1].set_ylabel("P(Degree ≥ k)")
    axes[1].set_title("Degree CCDF (log–log)")
    axes[1].legend()
    fig.savefig(OUT / "degree_distribution.png", dpi=220)
    plt.close(fig)

    # A high-degree induced sample is used only for a readable, fast plot.
    # Colour is component membership only, never political orientation.
    shown_nodes = [node for node, _ in sorted(graph.degree(), key=lambda item: item[1], reverse=True)[:200]]
    visual = graph.subgraph(shown_nodes).copy()
    layout = nx.spring_layout(visual.to_undirected(), seed=4095, k=0.22, iterations=100)
    node_colours = [graph.out_degree(node) - graph.in_degree(node) for node in visual.nodes]
    node_sizes = [12 + 4.3 * np.sqrt(graph.degree(node)) for node in visual.nodes]
    fig, ax = plt.subplots(figsize=(11, 9), facecolor="white")
    nx.draw_networkx_edges(visual, layout, ax=ax, edge_color="#8c8c8c", alpha=0.18, width=0.35, arrows=False)
    drawn_nodes = nx.draw_networkx_nodes(visual, layout, ax=ax, node_size=node_sizes, node_color=node_colours, cmap="coolwarm", alpha=0.78, linewidths=0)
    colourbar = fig.colorbar(drawn_nodes, ax=ax, shrink=0.72)
    colourbar.set_label("Out-degree − in-degree")
    ax.set_title("Political Blogs: induced visualization of 200 highest-degree blogs\n(directed calculations; arrowheads suppressed for legibility)")
    ax.set_axis_off()
    fig.savefig(OUT / "network_overview.png", dpi=240, bbox_inches="tight")
    plt.close(fig)
    write_report(stats)
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
