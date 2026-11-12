# OpenMLE-fast task

Task ID: `ufc-fighters-statistics@1`

Native metric: `UFCWinRatioMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2934 bytes)
- `data/sample_submission.csv` (12119 bytes); columns: ["id", "win_ratio"]
- `data/test.csv` (52233 bytes); columns: ["id", "height_cm", "weight_in_kg", "reach_in_cm", "stance", "date_of_birth", "significant_strikes_landed_per_minute", "significant_striking_accuracy", "significant_strikes_absorbed_per_minute", "significant_strike_defence", "average_takedowns_landed_per_15_minutes", "takedown_accuracy", "takedown_defense", "average_submissions_attempted_per_15_minutes"]
- `data/train.csv` (239334 bytes); columns: ["id", "height_cm", "weight_in_kg", "reach_in_cm", "stance", "date_of_birth", "significant_strikes_landed_per_minute", "significant_striking_accuracy", "significant_strikes_absorbed_per_minute", "significant_strike_defence", "average_takedowns_landed_per_15_minutes", "takedown_accuracy", "takedown_defense", "average_submissions_attempted_per_15_minutes", "win_ratio"]

## Public description

UFC Win Ratio Prediction Challenge

Problem statement
- Build a machine learning model to predict a UFC fighter’s career win ratio from tabular attributes and aggregated performance statistics.
- Target to predict: win_ratio ∈ [0, 1], defined as wins / (wins + losses). Draws are excluded from the denominator to avoid ambiguity. You should not use wins, losses, draws directly as features.

Files provided
- train.csv: Training set with features, an id column, and the target column win_ratio.
- test.csv: Test set with the same features and id but without the target.
- sample_submission.csv: Example submission file with the required columns.

Data description
Each row represents a fighter. Columns include:
- id: Integer identifier for row alignment across files.
- height_cm, weight_in_kg, reach_in_cm: Physical attributes.
- stance: Categorical fighting stance (e.g., Orthodox, Southpaw, Switch, Sideways, empty for missing/unknown).
- date_of_birth: ISO-8601 string (YYYY-MM-DD) when available; can be empty.
- significant_strikes_landed_per_minute
- significant_striking_accuracy (percent)
- significant_strikes_absorbed_per_minute
- significant_strike_defence (percent)
- average_takedowns_landed_per_15_minutes
- takedown_accuracy (percent)
- takedown_defense (percent)
- average_submissions_attempted_per_15_minutes
- win_ratio (train only): The target to predict.

Notes and recommendations
- Treat blank strings as missing values. Many numeric fields may be empty.
- Consider feature engineering such as:
  - Age derived from date_of_birth using a fixed reference date.
  - BMI from height_cm and weight_in_kg.
  - Reach-to-height ratio.
  - One-hot encoding of stance, including an Unknown category.
- Handle missing values with suitable imputation strategies (median/most-frequent) and consider adding missingness indicators.
- Clip outliers to realistic ranges (e.g., accuracies to [0, 100]).
- Avoid label leakage: do not use wins, losses, or draws to infer the target in the test set.

Evaluation
- Submissions are evaluated with Weighted Mean Absolute Error (WMAE) on win_ratio.
- The weight for each test row is the number of decisive bouts used in the label denominator: wins + losses. This naturally reduces the impact of noisy estimates from short careers.
- Lower WMAE is better.

Submission format
- CSV with header: id,win_ratio
- id must match the ids in test.csv (order does not matter).
- win_ratio should be a numeric value; predictions outside [0, 1] are clipped during scoring.

Rules and tips
- You may use any ML technique appropriate for tabular regression (e.g., gradient boosting, tree ensembles, linear models with interactions, neural networks).
- You are encouraged to perform careful preprocessing, feature engineering, and hyperparameter tuning.
- Runtime is not a concern for this competition; use the full data and explore thoroughly.

Good luck and have fun modeling UFC performance!
