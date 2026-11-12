# OpenMLE-fast task

Task ID: `english-premier-league-results@1`

Native metric: `EPLMatchOutcomeMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3338 bytes)
- `data/sample_submission.csv` (23987 bytes); columns: ["match_id", "p_H", "p_D", "p_A"]
- `data/test.csv` (23520 bytes); columns: ["match_id", "Season", "DateTime", "HomeTeam", "AwayTeam", "Referee"]
- `data/train.csv` (822970 bytes); columns: ["match_id", "Season", "DateTime", "HomeTeam", "AwayTeam", "Referee", "FTR"]

## Public description

EPL Pre-Match Outcome Probability Forecasting

Problem statement
Forecast calibrated pre-match probabilities for the full-time result of English Premier League matches. For each match in the test set, submit three probabilities: P(Home win), P(Draw), P(Away win). Lower log loss wins.

What you are given
- train.csv: Historical matches with features available prior to kickoff and the target label.
- test.csv: Future-season matches with the same features but without the target label.
- sample_submission.csv: Example submission file with the required format.

Columns
Each row represents one match.
- match_id: Unique identifier for a match; the only key used in submissions.
- Season: Match season (e.g., 2018-19).
- DateTime: Kickoff time in ISO-8601 UTC (e.g., 2016-08-13T14:00:00Z).
- HomeTeam: Home team name (string category).
- AwayTeam: Away team name (string category).
- Referee: Referee name (string, may be missing).
- FTR: Only in train.csv. Full-time result with values in {H, D, A} for Home win, Draw, Away win.

Task and constraints
- Predict a probability distribution over {H, D, A} for every match in test.csv, keyed by match_id.
- Use only pre-match information. No post-match or in-play statistics are present.
- External data is not allowed; model performance should come from feature engineering on the provided training history only.

Train/test split
- Strict temporal split to reflect real-world deployment and prevent leakage.
- Train: seasons 1993-94 through 2020-21.
- Test: season 2021-22.

Submission format
- CSV with exactly these columns and header: match_id, p_H, p_D, p_A
- One row per match_id in test.csv. The set of match_id must match exactly (order does not matter; the evaluator will align by match_id).
- p_H, p_D, p_A must be non-negative and should sum to 1 per row (the evaluator will normalize and clip tiny values for numerical stability).

Evaluation
- Primary metric: Multiclass log loss over {H, D, A}.
  logloss = - (1/N) * sum over matches of log(p_true)
  where p_true is the submitted probability assigned to the actual outcome. Probabilities are clipped to a small positive epsilon and row-normalized before evaluation to ensure numerical stability. Lower is better.

Modeling guidance (non-binding)
- Engineer leakage-safe features using only information available prior to each match, for example:
  - Rolling team strengths (e.g., Elo/Dixon–Coles), recent form, head-to-head summaries.
  - Temporal context: month, weekday, hour, and season trends, including potential home-advantage drift.
  - Referee tendencies derived from historical data.
- Viable approaches include regularized multinomial logistic regression, gradient-boosted trees, tree ensembles, and neural models with team/referee embeddings. Consider calibration (e.g., isotonic/Platt) if needed.

Files provided
- train.csv: match_id, Season, DateTime, HomeTeam, AwayTeam, Referee, FTR
- test.csv: match_id, Season, DateTime, HomeTeam, AwayTeam, Referee
- sample_submission.csv: match_id, p_H, p_D, p_A

Notes
- Names for teams and referees can vary over time; treat as categorical features or map consistently in your pipeline.
- Missing values may occur in Referee; handle accordingly.
- The problem is intentionally non-stationary across seasons; validate using time-based folds within the training window.
