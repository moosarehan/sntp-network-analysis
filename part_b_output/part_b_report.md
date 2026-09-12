# SE4095 Assignment 01 - Part B

Only PageRank and betweenness centrality are computed; both are on the allowed course list. The `value` ground-truth attribute is not read in this script.

## PageRank

Question: which blogs are the strongest authorities when incoming hyperlinks confer attention and outgoing links divide it? PageRank is used because it is designed for a directed link graph. It uses incoming endorsements, `alpha=0.85`, uniform handling of dangling nodes, tolerance `1e-10`, and at most `1000` power iterations. Scores sum to 1, so raw and normalized scores are identical.

| rank | node_id | label | raw_score | normalized_score |
|---|---|---|---|---|
| 1 | 155 | dailykos.com | 0.0179383450 | 0.0179383450 |
| 2 | 55 | atrios.blogspot.com | 0.0152240321 | 0.0152240321 |
| 3 | 1051 | instapundit.com | 0.0126202348 | 0.0126202348 |
| 4 | 855 | blogsforbush.com | 0.0124868013 | 0.0124868013 |
| 5 | 641 | talkingpointsmemo.com | 0.0124303744 | 0.0124303744 |
| 6 | 1153 | michellemalkin.com | 0.0109059733 | 0.0109059733 |
| 7 | 963 | drudgereport.com | 0.0107076377 | 0.0107076377 |
| 8 | 729 | washingtonmonthly.com | 0.0105423064 | 0.0105423064 |
| 9 | 1245 | powerlineblog.com | 0.0089316119 | 0.0089316119 |
| 10 | 798 | andrewsullivan.com | 0.0086105622 | 0.0086105622 |


## Betweenness centrality

Question: which blogs broker the greatest share of shortest directed reference paths? Exact directed Brandes betweenness is used; all links have length 1, endpoints are excluded, unreachable ordered pairs contribute zero, and normalized scores divide raw scores by `(n-1)(n-2)`.

| rank | node_id | label | raw_score | normalized_score |
|---|---|---|---|---|
| 1 | 855 | blogsforbush.com | 218464.0483049624 | 0.0986012336 |
| 2 | 55 | atrios.blogspot.com | 90985.8358274916 | 0.0410654097 |
| 3 | 1051 | instapundit.com | 76270.0252590192 | 0.0344235980 |
| 4 | 155 | dailykos.com | 54982.0162423476 | 0.0248155002 |
| 5 | 454 | newleftblogs.blogspot.com | 45895.5152820013 | 0.0207144125 |
| 6 | 387 | madkane.com/notable.html | 45021.6161451870 | 0.0203199882 |
| 7 | 1479 | wizbangblog.com | 40602.7276696979 | 0.0183255738 |
| 8 | 1101 | lashawnbarber.com | 36135.5525231639 | 0.0163093657 |
| 9 | 1041 | hughhewitt.com | 34249.6655151948 | 0.0154581923 |
| 10 | 729 | washingtonmonthly.com | 32659.9266053369 | 0.0147406819 |


## Comparison and interpretation

Spearman rank correlation: **0.8095**. Top-10 overlap: **5/10**. `dailykos.com` is PageRank rank 1 and betweenness rank 4, so it is both structurally authoritative and a frequent intermediary. `blogsforbush.com` is betweenness rank 1 but PageRank rank 4, illustrating brokerage distinct from authority. `talkingpointsmemo.com` is PageRank rank 5 but outside the betweenness top 10, illustrating that an authority need not be a shortest-path broker. These are network-structural results, not evidence of real-world political influence.
