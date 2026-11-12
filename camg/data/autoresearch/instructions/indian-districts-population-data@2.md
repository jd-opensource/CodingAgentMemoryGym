# OpenMLE-fast task

Task ID: `indian-districts-population-data@2`

Native metric: `IndianDistrictSexRatioMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2986 bytes)
- `data/sample_submission.csv` (1913 bytes); columns: ["ID", "Sex-Ratio"]
- `data/test.csv` (3535 bytes); columns: ["ID", "State", "Population", "Growth", "Literacy"]
- `data/train.csv` (27707 bytes); columns: ["ID", "State", "Population", "Growth", "Literacy", "Sex-Ratio"]

## Public description

Title: District Sex Ratio Prediction with State Holdout

Problem statement
Predict the district-level Sex-Ratio (females per 1000 males) using other census attributes. The split is by state: all districts from a subset of states are entirely held out for testing. Your model must generalize to unseen states.

Data description
You are provided with cleaned, reconciled tabular data at the district level.
- Target: Sex-Ratio (continuous; integer-valued in data)
- Features in both train.csv and test.csv:
  - ID: An anonymized row identifier (string)
  - State: State/UT name (categorical)
  - Population: Total population (numeric)
  - Growth: Decadal population growth percentage (numeric), e.g., 36.01 for 36.01%
  - Literacy: Overall literacy rate percentage (numeric)
- District names and any rank/order proxies are excluded to avoid leakage via near-unique identifiers.

Files
- train.csv: Columns [ID, State, Population, Growth, Literacy, Sex-Ratio]
- test.csv: Columns [ID, State, Population, Growth, Literacy]
- sample_submission.csv: Columns [ID, Sex-Ratio]

Split protocol
- State-wise holdout: approximately 20% of states/UTs are selected as the test set; all their districts appear only in test.csv. Remaining states form train.csv.
- The split is deterministic to ensure reproducibility.

Task
- Train a regression model using train.csv to predict Sex-Ratio for the rows in test.csv.
- You may perform preprocessing and feature engineering. Ensure any statistics used for transformations (e.g., target encodings, scalers) are computed using training data only.

Evaluation
- Metric: Mean Absolute Error (MAE) between your predictions and the ground-truth Sex-Ratio on the test set.
  - MAE = mean over test rows of |prediction − ground truth|.
  - All test rows are equally weighted.

Submission format
- A CSV file with exactly two columns in this order: [ID, Sex-Ratio].
- Requirements:
  - IDs must match those in test.csv exactly (one prediction per ID; no duplicates, no missing, no extras).
  - Sex-Ratio must be numeric and finite. Predictions may be any real values; integer rounding is not required but acceptable.
  - File should not contain any additional columns or metadata.

Modeling notes and suggestions
- The State feature will contain unseen categories in test. Consider robust handling of high-cardinality categoricals (e.g., regularized encodings, models tolerant to unseen categories, or state-agnostic representations).
- Potential features (computed using training data only): log(Population), interactions (e.g., Growth × Literacy), non-linear transforms, and distributional statistics learned from the training set.
- Baselines: A national-mean predictor provides a simple reference; tree ensembles or regularized linear models with careful encoding should outperform it.

Goal
- Achieve low MAE on the held-out states by learning portable relationships between demographics and sex ratio, rather than memorizing state-specific idiosyncrasies.
