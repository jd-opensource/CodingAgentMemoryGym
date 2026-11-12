# OpenMLE-fast task

Task ID: `cair-cvd-2025-cardiovascular-risk-from-bangladesh@1`

Native metric: `CvdRiskKappaMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2757 bytes)
- `data/sample_submission.csv` (3619 bytes); columns: ["RowId", "CVD Risk Level"]
- `data/test.csv` (34981 bytes); columns: ["RowId", "Sex", "Age", "Weight (kg)", "Height (m)", "BMI", "Abdominal Circumference (cm)", "Blood Pressure (mmHg)", "Total Cholesterol (mg/dL)", "HDL (mg/dL)", "Fasting Blood Sugar (mg/dL)", "Smoking Status", "Diabetes Status", "Physical Activity Level", "Family History of CVD", "Height (cm)", "Waist-to-Height Ratio", "Systolic BP", "Diastolic BP", "Blood Pressure Category", "Estimated LDL (mg/dL)"]
- `data/train.csv` (148892 bytes); columns: ["RowId", "Sex", "Age", "Weight (kg)", "Height (m)", "BMI", "Abdominal Circumference (cm)", "Blood Pressure (mmHg)", "Total Cholesterol (mg/dL)", "HDL (mg/dL)", "Fasting Blood Sugar (mg/dL)", "Smoking Status", "Diabetes Status", "Physical Activity Level", "Family History of CVD", "Height (cm)", "Waist-to-Height Ratio", "Systolic BP", "Diastolic BP", "Blood Pressure Category", "Estimated LDL (mg/dL)", "CVD Risk Level"]

## Public description

CAIR-CVD-2025 Ordinal Risk Prediction Challenge (Bangladesh)

Problem statement
Predict each patient's cardiovascular risk tier (LOW, INTERMEDIARY, HIGH) from routinely collected tabular clinical and lifestyle variables. This is an ordinal classification task: misclassifications farther from the true class are penalized more than near misses.

Data files
- Train data: train.csv
  - Columns: RowId, CVD Risk Level (target), and all predictor columns from the source dataset except CVD Risk Score (removed to prevent label leakage).
- Test data: test.csv
  - Columns: RowId and the same predictor columns as in train.csv (excluding CVD Risk Level and CVD Risk Score). Labels are hidden.
- Sample submission: sample_submission.csv
  - Columns: RowId, CVD Risk Level
  - Valid label values: LOW, INTERMEDIARY, HIGH

Predictor overview
- Demographics and lifestyle: Sex, Age, Smoking Status, Diabetes Status, Physical Activity Level, Family History of CVD.
- Anthropometrics: Weight (kg), Height (m), Height (cm), BMI, Abdominal Circumference (cm), Waist-to-Height Ratio.
- Blood pressure: Blood Pressure (mmHg) textual reading, Systolic BP, Diastolic BP, Blood Pressure Category.
- Lipids and glycemia: Total Cholesterol (mg/dL), HDL (mg/dL), Estimated LDL (mg/dL), Fasting Blood Sugar (mg/dL).
- Excluded: CVD Risk Score (numeric) — intentionally removed to avoid target leakage.

Evaluation metric
- Leaderboard metric: Quadratic Weighted Kappa (QWK) on ordinal-encoded labels with mapping LOW=0, INTERMEDIARY=1, HIGH=2.
  - QWK measures agreement adjusted for chance and applies quadratic weights so that larger ordinal errors are penalized more than smaller ones.
  - Score range: 0 (no agreement beyond chance) to 1 (perfect agreement).

Submission requirements
- Submit a CSV file with exactly two columns in this order: RowId, CVD Risk Level.
- RowId must match the values and order in test.csv exactly, with no duplicates or missing entries.
- CVD Risk Level must be one of: LOW, INTERMEDIARY, HIGH.

Guidance for participants
- Handle real-world tabular challenges: missing values; mixed units (height in meters and centimeters); textual and numeric BP fields; derived measures (BMI, waist-to-height).
- Suggested techniques: robust preprocessing and imputation; feature engineering (e.g., parsing Blood Pressure (mmHg) to reconcile SBP/DBP); consistent categorical encoding; ordinal-aware modeling and calibration.
- Class imbalance is modest (LOW is the minority). Strategies such as class-weighting, focal loss variants for ordinal tasks, or threshold tuning may help.

Deliverable
- A predictions file following the submission requirements above. The leaderboard evaluates your predictions on test.csv using QWK against a hidden ground truth.
