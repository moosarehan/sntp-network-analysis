"""Run only Assignment Part B: python part_b_analysis.py."""
from pathlib import Path
import csv
import network_analysis_core as shared

OUT = Path(__file__).resolve().parent / "part_b_output"

def main():
    OUT.mkdir(exist_ok=True)
    graph = shared.load_analysis_graph()
    pagerank, bc_raw, bc_norm, pr_order, bc_order = shared.rankings(graph)
    top_pr = shared.top_ten_rows(graph, pagerank, bc_raw, bc_norm, pr_order, "pagerank")
    top_bc = shared.top_ten_rows(graph, pagerank, bc_raw, bc_norm, bc_order, "betweenness")
    for name, rows in [("pagerank_top10.csv", top_pr), ("betweenness_top10.csv", top_bc)]:
        with (OUT / name).open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys()); writer.writeheader(); writer.writerows(rows)
    rho = shared.spearman_from_ranks(shared.average_ranks(pagerank), shared.average_ranks(bc_norm))
    overlap = len(set(pr_order[:10]) & set(bc_order[:10]))
    report = f"""# SE4095 Assignment 01 - Part B

Only PageRank and betweenness centrality are computed; both are on the allowed course list. The `value` ground-truth attribute is not read in this script.

## PageRank

Question: which blogs are the strongest authorities when incoming hyperlinks confer attention and outgoing links divide it? PageRank is used because it is designed for a directed link graph. It uses incoming endorsements, `alpha={shared.PAGERANK_ALPHA}`, uniform handling of dangling nodes, tolerance `{shared.PAGERANK_TOL}`, and at most `{shared.PAGERANK_MAX_ITER}` power iterations. Scores sum to 1, so raw and normalized scores are identical.

{shared.markdown_table(top_pr, ['rank','node_id','label','raw_score','normalized_score'])}

## Betweenness centrality

Question: which blogs broker the greatest share of shortest directed reference paths? Exact directed Brandes betweenness is used; all links have length 1, endpoints are excluded, unreachable ordered pairs contribute zero, and normalized scores divide raw scores by `(n-1)(n-2)`.

{shared.markdown_table(top_bc, ['rank','node_id','label','raw_score','normalized_score'])}

## Comparison and interpretation

Spearman rank correlation: **{rho:.4f}**. Top-10 overlap: **{overlap}/10**. `dailykos.com` is PageRank rank 1 and betweenness rank 4, so it is both structurally authoritative and a frequent intermediary. `blogsforbush.com` is betweenness rank 1 but PageRank rank 4, illustrating brokerage distinct from authority. `talkingpointsmemo.com` is PageRank rank 5 but outside the betweenness top 10, illustrating that an authority need not be a shortest-path broker. These are network-structural results, not evidence of real-world political influence.
"""
    (OUT / "part_b_report.md").write_text(report, encoding="utf-8")

if __name__ == "__main__": main()
