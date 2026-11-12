# OpenMLE-fast task

Task ID: `baseball-kbo-batting-data-1982-2021@1`

Native metric: `KBORunsPerGameMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3633 bytes)
- `data/sample_submission.csv` (1238 bytes); columns: ["row_id", "target_runs_per_game"]
- `data/test.csv` (5983 bytes); columns: ["row_id", "team_canon", "feature_year", "label_year", "average_batter_age", "games", "plate_appearances", "at_bats", "runs", "hits", "doubles", "triples", "homeruns", "RBI", "stolen_bases", "caught_stealing", "bases_on_balls", "strikeouts", "batting_average", "OBP", "SLG", "OPS", "total_bases", "GDP", "HBP", "sacrifice_hits", "sacrifice_flies", "IBB", "runs_per_game"]
- `data/train.csv` (38062 bytes); columns: ["row_id", "team_canon", "feature_year", "label_year", "average_batter_age", "games", "plate_appearances", "at_bats", "runs", "hits", "doubles", "triples", "homeruns", "RBI", "stolen_bases", "caught_stealing", "bases_on_balls", "strikeouts", "batting_average", "OBP", "SLG", "OPS", "total_bases", "GDP", "HBP", "sacrifice_hits", "sacrifice_flies", "IBB", "runs_per_game", "target_runs_per_game"]

## Public description

KBO Team Runs-Per-Game Forecast Challenge

Problem statement
You are given team-season batting profiles from the Korean Baseball Organization (KBO). Using only a team’s season t batting profile, your goal is to predict that team’s runs per game (R/G) in season t+1. The task requires building models that generalize across teams and eras (1982–2021), handling temporal drift, franchise renames, and multicollinearity among batting statistics.

Data description
You will work with pre-built, time-shifted team-season pairs. Each row represents one franchise and a feature season t with the target defined as that franchise’s runs per game in season t+1. Franchise name continuity is standardized (e.g., SK Wyverns → SSG Landers, Woori/Nexen/Kiwoom Heroes → Heroes).

Files provided
- train.csv: Supervised training data with features from season t and the target target_runs_per_game for season t+1.
- test.csv: Feature-only data from season t for which you must predict season t+1 R/G. Contains a unique row_id key.
- sample_submission.csv: A submission template with the required columns and random but plausible values.

Key columns
- row_id: Unique identifier for each row; stable across test.csv and your submission.
- team_canon: Canonical franchise identifier (categorical) after standardizing historical renames.
- feature_year: The season year t that defines the features for the row.
- label_year: The season year t+1 corresponding to the target for that row (present in train.csv only).
- target_runs_per_game: Target variable in train.csv only; runs per game in season t+1 for the corresponding franchise.
- Feature columns from season t: average_batter_age, games, plate_appearances, at_bats, runs, hits, doubles, triples, homeruns, RBI, stolen_bases, caught_stealing, bases_on_balls, strikeouts, batting_average, OBP, SLG, OPS, total_bases, GDP, HBP, sacrifice_hits, sacrifice_flies, IBB, runs_per_game (season t R/G).

Note: test.csv does not include target_runs_per_game. All features come strictly from season t; the target is always season t+1.

Train/test split
- The split is strictly time-based. Training rows use feature_year ≤ 2016. Test rows use feature_year ∈ [2017, 2020], so targets correspond to label_year ∈ [2018, 2021]. This respects temporal causality and simulates realistic forecasting into the most recent seasons.

Evaluation
- Metric: Root Mean Squared Error (RMSE) on runs per game.
- Definition: RMSE = sqrt(mean((y_pred − y_true)^2)) computed over all rows in the test set.
- Rationale: R/G is a continuous quantity; RMSE penalizes large errors and is standard for forecasting tasks with varying offensive environments across eras.

Submission format
- A CSV file with exactly the following two columns (no index column):
  - row_id
  - target_runs_per_game
- The row_id values must match those in test.csv exactly (order agnostic). The target_runs_per_game values must be finite real numbers.

Modeling tips
- Time awareness: Validate with time-based splits to avoid leakage and over-optimistic estimates.
- Feature engineering: Consider per-PA normalizations, interaction terms, or era/year features. Regularization can help with multicollinearity among counts and rate stats.
- Categorical handling: Encode team_canon appropriately (one-hot or target encoding in cross-validation).
- Robustness: Check for changing run environments across years (e.g., ball changes), which may require adding year as a numeric or spline-like feature.

Deliverables
- Submit a CSV with predictions for target_runs_per_game for all rows in test.csv, using the exact submission format above.
