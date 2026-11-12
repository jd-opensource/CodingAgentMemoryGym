# OpenMLE-fast task

Task ID: `nba-betting-data-october-2007-to-june-2024@1`

Native metric: `NBABettingSecondHalfMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2636 bytes)
- `data/sample_submission.csv` (318562 bytes); columns: ["row_id", "prob_under", "prob_over", "prob_push"]
- `data/test.csv` (450625 bytes); columns: ["season", "date", "regular", "playoffs", "away", "home", "whos_favored", "spread", "total", "moneyline_away", "moneyline_home", "q1_away", "q2_away", "q1_home", "q2_home", "h2_total", "h2_spread", "row_id"]
- `data/train.csv` (1305368 bytes); columns: ["season", "date", "regular", "playoffs", "away", "home", "whos_favored", "spread", "total", "moneyline_away", "moneyline_home", "q1_away", "q2_away", "q1_home", "q2_home", "h2_total", "h2_spread", "row_id", "h2_outcome"]

## Public description

Competition: NBA Halftime Over/Under Probability (2008–2022)

Problem statement
Given an NBA game at halftime, predict the probability that the second‑half total points (Q3+Q4+OT) will go under, over, or exactly push relative to the posted halftime over/under line (h2_total). Submit calibrated probabilities for three outcomes: under (0), over (1), push (2).

Data description
This competition provides tabular game‑level data with market information known by tipoff/halftime and first‑half scoring. The target label is constructed from post‑halftime scoring and the halftime total line.

Provided files (under public/)
- train.csv: Feature columns plus the target label for training.
- test.csv: Feature columns for the held‑out set (no labels).
- sample_submission.csv: A sample prediction file showing the required submission format.

Features available in both train.csv and test.csv (no label leakage)
- season, date, regular, playoffs
- away, home
- whos_favored, spread, total
- moneyline_away, moneyline_home
- q1_away, q2_away, q1_home, q2_home
- h2_total, h2_spread
- row_id (unique integer identifier for each row)

Target label in train.csv
- h2_outcome: Encoded as 0 (under), 1 (over), 2 (push). Computed as the sign of (Q3+Q4+OT total points) − (h2_total).

Train/test split
- Train: seasons 2008–2018
- Test: seasons 2019–2022
- Only games with a known h2_total are included. Both regular season and playoffs are used.

Submission format
- A CSV with the following columns and rows exactly matching test.csv by row_id:
  - row_id
  - prob_under, prob_over, prob_push
- Probabilities must be non‑negative and should sum to 1 for each row. The evaluation will safely renormalize small numerical deviations, clip invalid values, and reject mismatched row_id sets.

Evaluation metric
- Multiclass log loss on the three outcomes under/over/push, averaged across all test rows. For each row, the loss is −log(p_true), where p_true is the submitted probability assigned to the true class.
- This is a proper scoring rule: it rewards well‑calibrated probabilities, naturally handles class imbalance (pushes are rare but important), and penalizes overconfident errors.

Modeling guidance (optional)
- Do not use post‑halftime scoring or final scores as features; those determine the label.
- Useful signals include first‑half totals/differentials, market context (spread/total/moneylines, favorite side), and how the halftime total compares to pregame expectations.
- Time‑aware features (season, playoffs flag, month/day‑of‑week) and rolling team statistics based only on prior games can help.
