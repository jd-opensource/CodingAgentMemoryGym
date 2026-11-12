# OpenMLE-fast task

Task ID: `fifa-football-world-cup@1`

Native metric: `WorldCupOutcomeMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3678 bytes)
- `data/sample_submission.csv` (8408 bytes); columns: ["match_id", "home_win", "draw", "away_win"]
- `data/test.csv` (15684 bytes); columns: ["match_id", "home_team", "away_team", "Round", "Date", "Host", "Year", "Venue", "teams_total", "matches_total", "tournament_host", "is_home_host", "is_away_host", "home_rank", "home_points", "away_rank", "away_points"]
- `data/train.csv` (100641 bytes); columns: ["match_id", "home_team", "away_team", "Round", "Date", "Host", "Year", "Venue", "teams_total", "matches_total", "tournament_host", "is_home_host", "is_away_host", "home_rank", "home_points", "away_rank", "away_points", "result"]

## Public description

World Cup Match Outcome Probability Forecasting (1930–2022)

Problem statement
Predict the probability of each outcome (home win, draw, away win) for FIFA World Cup matches using only pre-match information available before kickoff. You must submit calibrated probabilities for three outcomes for each match in the test set.

Files provided
- train.csv: Historical matches with features and the target label result.
- test.csv: Future-era matches with the same features but without the label.
- sample_submission.csv: Example of a valid submission with random probabilities.

Target and classes
- result: The ground-truth match outcome using 90’+ET scores (penalty shootouts ignored for the label), encoded as:
  - H: home_team wins
  - D: draw after regulation/extra time
  - A: away_team wins

Data description
Each row represents a World Cup match. The features have been curated to prevent leakage and reflect information available pre-match only. Columns:
- match_id: Unique identifier for the match, used to join with submissions
- home_team, away_team: National teams as named historically (e.g., West Germany, USSR)
- Round: Tournament stage (e.g., Group stage, Round of 16, Quarter-finals, Semi-finals, Final)
- Date: ISO date string (YYYY-MM-DD)
- Host: Host nation where the match took place
- Year: World Cup year
- Venue: Stadium and city (string)
- teams_total: Number of teams in that year’s World Cup
- matches_total: Number of matches in that year’s World Cup
- tournament_host: Host(s) for that year (may include multiple, comma-separated)
- is_home_host, is_away_host: Indicator if a team is the tournament host
- home_rank, home_points, away_rank, away_points: FIFA ranking and points for 2022 teams only; missing (NaN) otherwise
- result: Target label (only in train.csv), with values in {H, D, A}

Train/test split
- Chronological split to emulate real forecasting and avoid leakage across eras:
  - Train: 1930–2014
  - Test: 2018–2022

Evaluation metric
- Multiclass Log Loss on the three outcomes (H/D/A). For each match i and true class c_i, the loss is -log p_i(c_i). Submissions must provide probabilities that sum to 1 across the three outcomes for every match.

Submission format
- CSV with columns (in order): match_id, home_win, draw, away_win
- match_id must match exactly the IDs in test.csv
- Each row’s probabilities must be non-negative, finite, and sum to 1

Modeling guidance and caveats
- The dataset is order-aware but neutral: home/away indicates listing order, not home advantage. Use order-robust encodings or features invariant to team order.
- You may design time-aware features from training data only (e.g., rolling win/goal rates, Elo-like ratings), taking care to avoid peeking into test matches.
- world_cup context features (teams_total, matches_total) capture tournament formats by year.
- 2022-only FIFA ranking features provide optional signal for that tournament; they are NaN for other years and should be handled accordingly.
- Avoid using any post-match or in-match artifacts beyond what is provided in train.csv; fields not present are intentionally removed to prevent leakage.

Tips for strong baselines
- Regularized linear models and tree ensembles with thoughtful categorical handling (e.g., target encoding within cross-validation) are competitive.
- Team-embedding models or Elo-like rating systems can capture relative strength.
- Calibrate outputs (e.g., Platt/Isotonic on cross-validated predictions) to improve log loss.

Deliverables
- A single CSV submission following the specified format.
- No external data is required, but creative feature engineering from the training set is encouraged.
