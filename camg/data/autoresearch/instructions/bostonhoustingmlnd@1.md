# OpenMLE-fast task

Task ID: `bostonhoustingmlnd@1`

Native metric: `BostonHousingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2875 bytes)
- `data/sample_submission.csv` (2171 bytes); columns: ["Id", "MEDV"]
- `data/test.csv` (2000 bytes); columns: ["RM", "LSTAT", "PTRATIO", "Id"]
- `data/train.csv` (11422 bytes); columns: ["RM", "LSTAT", "PTRATIO", "MEDV", "Id"]

## Public description

Title: Boston Suburb Prices — Predicting Median Home Value from Socio-Economic Signals

Background
Boston-area neighborhood prices are influenced by socio-economic factors and housing characteristics. This competition focuses on learning from three interpretable predictors to estimate median home value. The dataset contains 489 neighborhood-level records with no missing values.

Problem Statement
Given neighborhood features — average rooms per dwelling (RM), percentage of lower status population (LSTAT), and pupil–teacher ratio by town (PTRATIO) — predict the median home value (MEDV) in USD for unseen neighborhoods.

Files Provided
- train.csv: Training data with features and target (RM, LSTAT, PTRATIO, MEDV) plus an Id column.
- test.csv: Test data with features only (RM, LSTAT, PTRATIO) plus an Id column.
- sample_submission.csv: A valid sample submissions file containing Id and MEDV columns.

Target
- MEDV (median home value, USD). Strictly positive real-valued target.

Data Description
- RM: Average number of rooms per dwelling.
- LSTAT: Percentage of lower status of the population.
- PTRATIO: Pupil–teacher ratio by town.
- Id: Row identifier corresponding across test.csv and submissions.

Task Characteristics
- Small, feature-sparse tabular regression task with non-linear relationships and a skewed target distribution.
- All features are continuous; no categorical variables.
- Outliers exist across both features and target.

Evaluation Metric
- Official score: Root Mean Squared Error on the natural-log target (RMSE of ln(MEDV)).
  - For each test row i, compute yi_true = ln(MEDV_true_i) and yi_pred = ln(max(MEDV_pred_i, ε)) where ε > 0 is a small constant to avoid invalid logs.
  - The final score is sqrt(mean((yi_pred − yi_true)^2)). Lower is better.
  - This metric treats multiplicative errors uniformly across price ranges, improving fairness compared to RMSE on raw prices.

Rules and Guidance
- Use any ML approach suitable for tabular regression: feature scaling/normalization, target transformations (e.g., log), robust losses, tree-based models, linear models with interactions, or generalized additive models.
- External data is not permitted for leaderboard evaluation; rely only on the provided features.
- Do not assume time-series or grouped structure; rows are independent neighborhoods.
- Predictions must be strictly positive real numbers to be valid under the evaluation metric.

Train/Test Split
- The organizers use a single deterministic 80/20 stratified split based on MEDV quantiles to preserve price-range distribution.
- Ids correspond exactly between test.csv and submissions; the provided sample_submission.csv aligns with test.csv.

Submission Format
- CSV with two columns: Id, MEDV.
- Id must match the Ids in test.csv exactly and appear once.
- MEDV must be positive floating-point values (USD).
