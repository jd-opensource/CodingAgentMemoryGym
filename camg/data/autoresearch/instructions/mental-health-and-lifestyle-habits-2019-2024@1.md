# OpenMLE-fast task

Task ID: `mental-health-and-lifestyle-habits-2019-2024@1`

Native metric: `HappinessPredictionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3337 bytes)
- `data/sample_submission.csv` (13211 bytes); columns: ["row_id", "Happiness Score"]
- `data/test.csv` (37240 bytes); columns: ["row_id", "Country", "Age", "Gender", "Exercise Level", "Diet Type", "Sleep Hours", "Stress Level", "Mental Health Condition", "Work Hours per Week", "Screen Time per Day (Hours)", "Social Interaction Score"]
- `data/train.csv` (148024 bytes); columns: ["Country", "Age", "Gender", "Exercise Level", "Diet Type", "Sleep Hours", "Stress Level", "Mental Health Condition", "Work Hours per Week", "Screen Time per Day (Hours)", "Social Interaction Score", "Happiness Score"]

## Public description

Competition: Predict Happiness from Lifestyle

Background
Mental well-being is influenced by sleep, stress, social interaction, exercise, diet, and work-life balance. This tabular dataset (2019–2024) includes demographics and lifestyle habits for 3,000 individuals across multiple countries. Your task is to build a robust regression model that predicts an individual’s self-reported happiness from these inputs.

Problem statement
Given lifestyle and demographic variables, predict the Happiness Score (a bounded 1–10 scale) for unseen individuals.

Files provided
- train.csv: Training data with features and the target column (Happiness Score).
- test.csv: Test data with the same feature columns and an additional identifier column (row_id). The target is not included.
- sample_submission.csv: A template showing the required submission format (row_id, Happiness Score).

Columns
Feature columns include:
- Country
- Age
- Gender
- Exercise Level
- Diet Type
- Sleep Hours
- Stress Level
- Mental Health Condition
- Work Hours per Week
- Screen Time per Day (Hours)
- Social Interaction Score
Target column:
- Happiness Score
Identifier column (in test and sample_submission only):
- row_id

Task expectations
Participants are expected to perform end-to-end ML:
- Data processing and validation (type handling, missing values, bounds, outliers)
- Feature engineering (e.g., categorical encoding, interaction terms, transformations)
- Model training (e.g., linear models, tree ensembles, gradient boosting, stacking)
- Model evaluation and calibration
- Clear, reproducible pipeline with deterministic inference

Important data notes
- The target (Happiness Score) has no missing values. Some feature columns may contain missing values (e.g., Mental Health Condition); handle them appropriately.
- Numeric ranges are sensible and bounded; predictions will be evaluated on the same 1–10 scale.
- All categorical levels present in the test set also occur in the training set by construction.

Evaluation metric
- Root Mean Squared Error (RMSE) on the Happiness Score.
- During evaluation, predictions are clipped to the valid range [1, 10] to ensure robustness and prevent pathological out-of-range scores from skewing results.

Submission format
- A CSV with exactly two columns in order: row_id and Happiness Score.
- Each row_id must match one in test.csv. Do not add extra columns.
- The number of rows must equal the number of rows in test.csv.

Train/test split
- Deterministic 80/20 split.
- The split preserves the target distribution via stratified binning on Happiness Score.
- Train size is approximately 2,400 rows; test size is approximately 600 rows.

Guidance for a strong solution
- Encode categorical features (e.g., one-hot target-aware encoding without leakage).
- Consider non-linear interactions (e.g., sleep × stress, work hours × screen time × social interaction).
- Standardize or normalize continuous variables where appropriate; clip extreme values defensibly.
- Use robust regressors (e.g., regularized linear, tree ensembles, gradient boosting, or stacking) and calibrate predictions.
- Validate your pipeline deterministically and avoid data leakage.

Goal
Build models that minimize RMSE, yielding accurate and well-calibrated happiness predictions grounded in lifestyle and demographic inputs.
