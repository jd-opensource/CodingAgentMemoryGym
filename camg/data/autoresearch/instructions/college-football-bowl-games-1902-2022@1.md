# OpenMLE-fast task

Task ID: `college-football-bowl-games-1902-2022@1`

Native metric: `CollegeFootballBowlGameMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2836 bytes)
- `data/sample_submission.csv` (4999 bytes); columns: ["id", "total_points"]
- `data/test.csv` (17648 bytes); columns: ["id", "year", "date", "day", "team1", "team2", "rank1", "rank2", "sponsor", "bowl_name"]
- `data/train.csv` (103528 bytes); columns: ["id", "year", "date", "day", "team1", "team2", "rank1", "rank2", "sponsor", "bowl_name", "total_points"]

## Public description

Title: Bowl Game Total Points Challenge (1902–2021)

Problem statement
- Predict the total combined points scored in a college football bowl game using only pregame context.
- You are given historical bowl matchups with metadata: year/date/day, the two teams (unordered pair), their pregame ranks (unordered), sponsor, and bowl name. Your task is to predict total_points = winner_points + loser_points.
- This is a tabular regression problem with strong distribution shift across eras, high-cardinality categoricals (teams, bowls, sponsors), and missing ranks for many games.

Files
- train.csv: Training data with features and the label column total_points.
- test.csv: Test data with the same features as train.csv (without total_points).
- sample_submission.csv: A valid example submission with random predictions.

Columns
Each row represents a single bowl game.
- id: Unique game identifier.
- year: Year of the game.
- date: Calendar date string (e.g., 12/29/2016 or 1/2/2016).
- day: Day of the week (e.g., Mon, Tue, ...).
- team1, team2: The two teams in alphabetical order (unordered pair to avoid leakage).
- rank1, rank2: The teams’ pregame ranks aligned with team1 and team2, respectively (NaN if unranked/unknown). Lower is better.
- sponsor: Sponsor of the game (string; may be Unknown).
- bowl_name: Name of the bowl game.
- total_points (train only): Target label, equal to winner_points + loser_points.

Evaluation
- Submissions are evaluated using Mean Absolute Error (MAE) between your predictions and the ground truth total_points on the test set.
- Lower MAE is better.

Submission format
- A single CSV with exactly two columns in this order: id, total_points.
- id must exactly match test.csv ids in the same order.
- total_points must be finite real numbers.

Suggested approach and notes
- Time-aware modeling: The split uses past data to predict more recent seasons (2016–2021). Expect concept drift from rule changes and evolving play styles.
- Feature engineering ideas: month/day from date; decade bins from year; rank features such as best_rank, worst_rank, rank_spread; any_ranked flag; team/bowl/sponsor interactions; historical aggregates computed using only training data.
- Categorical encoding: Consider target encoding with proper CV, regularized embeddings, or high-cardinality-friendly models (e.g., tree ensembles with careful preprocessing).
- Missing data: Handle NaNs in ranks and rare/unknown sponsors robustly.
- Caution: The teams and ranks are provided as unordered pairs to prevent leakage from “winner/loser” ordering.

Important
- Do not attempt to recover labels from filenames or column names; test labels are hidden.
- Keep inference strictly pregame: attendance, MVP, and postgame signals are not provided.

Good luck, and have fun building robust, time-aware regressors!
