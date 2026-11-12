# OpenMLE-fast task

Task ID: `gestational-diabetes-mellitus-gdm-data-set@1`

Native metric: `GDMPredictionMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2378 bytes)
- `data/sample_submission.csv` (30852 bytes); columns: ["id", "GDM_probability"]
- `data/test.csv` (51057 bytes); columns: ["id", "Age", "No of Pregnancy", "Gestation in previous Pregnancy", "BMI", "HDL", "Family History", "unexplained prenetal loss", "Large Child or Birth Default", "PCOS", "Sys BP", "Dia BP", "Hemoglobin", "Sedentary Lifestyle", "Prediabetes"]
- `data/train.csv` (99268 bytes); columns: ["Age", "No of Pregnancy", "Gestation in previous Pregnancy", "BMI", "HDL", "Family History", "unexplained prenetal loss", "Large Child or Birth Default", "PCOS", "Sys BP", "Dia BP", "Hemoglobin", "Sedentary Lifestyle", "Prediabetes", "target"]

## Public description

Title: GDM Risk Prediction Without OGTT

Problem statement
Build a machine learning model that estimates the probability that a pregnant individual has Gestational Diabetes Mellitus (GDM), using routinely available clinical and history features only. The diagnostic Oral Glucose Tolerance Test (OGTT) is intentionally excluded to avoid label leakage and to simulate early screening when OGTT may not be available.

Files provided
- train.csv: Tabular features and the binary target for model development.
- test.csv: Tabular features with an id column; the target is hidden.
- sample_submission.csv: Template showing the required submission format.

Target and features
- Target column: target (binary), where 1 indicates GDM and 0 indicates Non-GDM.
- Feature columns included in both train.csv and test.csv (exact names):
  - Age
  - No of Pregnancy
  - Gestation in previous Pregnancy
  - BMI
  - HDL
  - Family History
  - unexplained prenetal loss
  - Large Child or Birth Default
  - PCOS
  - Sys BP
  - Dia BP
  - Hemoglobin
  - Sedentary Lifestyle
  - Prediabetes
- Missing values: The provided files preserve original missingness. Handling missingness is part of the challenge.

Task
- Train a model on train.csv to predict the probability of GDM for each row in test.csv.
- You may use any technique appropriate for tabular classification.

Submission format
- A CSV file with exactly the following columns:
  - id: The identifier provided in test.csv (exact match required, unique, and one row per test case).
  - GDM_probability: A numeric probability in [0, 1] representing the predicted risk of GDM for the corresponding id.

Evaluation
- Metric: ROC-AUC computed on the hidden test labels using the submitted probabilities.
- Your submission must include exactly the two columns [id, GDM_probability] and cover all rows in test.csv. Duplicate ids, missing rows, NaN/Inf, or non-numeric values will invalidate the submission.

Data split and preparation notes
- The data are split with stratified sampling to preserve class balance between train and test.
- Exact duplicate records were removed before splitting.
- Direct identifiers and OGTT were excluded from the provided files to prevent diagnostic leakage.

Deliverable
- Submit a CSV file named as you like that matches the sample_submission.csv structure and contains predictions for every row in test.csv.
