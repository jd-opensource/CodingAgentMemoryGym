# OpenMLE-fast task

Task ID: `predict-liver-disease-1700-records-dataset@1`

Native metric: `LiverDiseaseScreeningMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2595 bytes)
- `data/sample_submission.csv` (8029 bytes); columns: ["Id", "Diagnosis"]
- `data/test.csv` (24639 bytes); columns: ["Id", "Age", "Gender", "BMI", "AlcoholConsumption", "Smoking", "GeneticRisk", "PhysicalActivity", "Diabetes", "Hypertension"]
- `data/train.csv` (101024 bytes); columns: ["Id", "Age", "Gender", "BMI", "AlcoholConsumption", "Smoking", "GeneticRisk", "PhysicalActivity", "Diabetes", "Hypertension", "Diagnosis"]

## Public description

Title: Early Screening of Liver Disease from Non‑invasive Risk Factors

Problem statement
- Task: Predict the probability of liver disease (Diagnosis = 1) from non‑invasive demographic, lifestyle, and comorbidity features.
- Constraint: Do not use laboratory results. The LiverFunctionTest column is excluded from the provided train/test files to avoid label leakage and reflect realistic screening.

Data description
- Files provided to participants:
  - train.csv: Tabular training data with columns [Id, Age, Gender, BMI, AlcoholConsumption, Smoking, GeneticRisk, PhysicalActivity, Diabetes, Hypertension, Diagnosis]. Diagnosis is the binary target (0/1). LiverFunctionTest is not included.
  - test.csv: Same columns as train.csv except without Diagnosis. Columns: [Id, Age, Gender, BMI, AlcoholConsumption, Smoking, GeneticRisk, PhysicalActivity, Diabetes, Hypertension].
  - sample_submission.csv: Example submission with columns [Id, Diagnosis], where Diagnosis contains example probabilities for class 1.
- Feature semantics:
  - Age: years (approx. 20–80)
  - Gender: 0 = Male, 1 = Female
  - BMI: Body Mass Index (approx. 15–40)
  - AlcoholConsumption: units/week (approx. 0–20)
  - Smoking: 0 = No, 1 = Yes
  - GeneticRisk: 0 = Low, 1 = Medium, 2 = High
  - PhysicalActivity: hours/week (approx. 0–10)
  - Diabetes: 0 = No, 1 = Yes
  - Hypertension: 0 = No, 1 = Yes

Submission format
- Create a CSV file with exactly two columns:
  - Id: integer identifier that matches the Id values in test.csv
  - Diagnosis: predicted probability that Diagnosis = 1 for each Id; values should be in [0, 1]
- Order of rows does not matter; Ids must match test.csv exactly and be unique.

Evaluation
- Metric: ROC-AUC (area under the Receiver Operating Characteristic curve) computed on the submitted probabilities versus ground truth labels for the hidden test set.
- Rationale: ROC-AUC is threshold‑independent, robust to class imbalance, and measures the quality of ranking by predicted risk.

Recommended modeling notes
- Treat Gender, Smoking, Diabetes, Hypertension as binary; GeneticRisk as ordinal (0/1/2).
- Consider scaling continuous features (Age, BMI, AlcoholConsumption, PhysicalActivity) if using linear models; tree ensembles generally do not require scaling.
- Use stratified cross‑validation for internal validation and fit preprocessing (e.g., scalers/imputers) only on training folds to prevent leakage.

Ethical use
- The dataset is synthetic and for educational purposes. Predictions should not be used for clinical decision‑making without proper validation.
