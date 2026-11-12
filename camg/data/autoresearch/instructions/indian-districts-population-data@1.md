# OpenMLE-fast task

Task ID: `indian-districts-population-data@1`

Native metric: `IndianDistrictLiteracyMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2174 bytes)
- `data/sample_submission.csv` (2675 bytes); columns: ["Id", "Literacy"]
- `data/test.csv` (5491 bytes); columns: ["Id", "State", "District", "Population", "Growth", "Sex-Ratio"]
- `data/train.csv` (23066 bytes); columns: ["Id", "State", "District", "Population", "Growth", "Sex-Ratio", "Literacy"]

## Public description

Competition: District Literacy Rate Prediction (India Census 2011)

Problem statement
Participants must predict the Literacy rate (in percentage points) for Indian districts using other demographic attributes from the 2011 census. You will receive a training set with features and target, and a test set with features only. Submit predicted Literacy for each test row.

Data description
- Target: Literacy (float, 0–100). Percentage of literate population in the district.
- Features provided:
  - State (categorical)
  - District (categorical, can be used as text/categorical ID)
  - Population (integer)
  - Growth (float, percentage points)
  - Sex-Ratio (integer, number of females per 1000 males)
- Ignored in this competition build: Ranking (a simple ordering by population; excluded to avoid redundant signaling).

Files
- train.csv: Columns [Id, State, District, Population, Growth, Sex-Ratio, Literacy]
- test.csv: Columns [Id, State, District, Population, Growth, Sex-Ratio]
- sample_submission.csv: Columns [Id, Literacy]

Important notes
- All numeric fields are pre-cleaned: Population has no thousands separators; Growth contains numeric values without the percent sign; Sex-Ratio is integer.
- Id uniquely identifies each row across files.
- The split preserves broad state coverage: states with multiple districts appear in both train and test whenever possible.

Evaluation
- Metric: Mean Absolute Error (MAE) on Literacy, averaged over all test rows.
- Definition: MAE = mean(|y_true − y_pred|). Lower is better.
- Submission format must match sample_submission.csv exactly: a CSV with columns [Id, Literacy], containing one row per test Id, no duplicates, and finite numeric predictions.

Hints for strong baselines
- Encode State as categorical and consider state-level aggregates computed from training data only.
- Try regularized linear models and gradient boosting regressors.
- Feature engineering ideas: log(Population), interactions between Population and Growth, per-state population ranks (computed from training only), and target encoding variants with cross-validation.

Reproducibility
- The data split is deterministic and reproducible.
