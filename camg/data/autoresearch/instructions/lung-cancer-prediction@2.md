# OpenMLE-fast task

Task ID: `lung-cancer-prediction@2`

Native metric: `LungCancerSurvivalMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (452 bytes)
- `data/sample_submission.csv` (188498 bytes); columns: ["Id", "Survive5Y"]
- `data/test.csv` (2412244 bytes); columns: ["Id", "Age", "Gender", "Smoking_History", "Tumor_Size_mm", "Tumor_Location", "Stage", "Ethnicity", "Insurance_Type", "Family_History", "Comorbidity_Diabetes", "Comorbidity_Hypertension", "Comorbidity_Heart_Disease", "Comorbidity_Chronic_Lung_Disease", "Comorbidity_Kidney_Disease", "Comorbidity_Autoimmune_Disease", "Comorbidity_Other", "Performance_Status", "Blood_Pressure_Systolic", "Blood_Pressure_Diastolic", "Blood_Pressure_Pulse", "Hemoglobin_Level", "White_Blood_Cell_Count", "Platelet_Count", "Albumin_Level", "Alkaline_Phosphatase_Level", "Alanine_Aminotransferase_Level", "Aspartate_Aminotransferase_Level", "Creatinine_Level", "LDH_Level", "Calcium_Level", "Phosphorus_Level", "Glucose_Level", "Potassium_Level", "Sodium_Level", "Smoking_Pack_Years"]
- `data/train.csv` (7270213 bytes); columns: ["Id", "Survive5Y", "Age", "Gender", "Smoking_History", "Tumor_Size_mm", "Tumor_Location", "Stage", "Ethnicity", "Insurance_Type", "Family_History", "Comorbidity_Diabetes", "Comorbidity_Hypertension", "Comorbidity_Heart_Disease", "Comorbidity_Chronic_Lung_Disease", "Comorbidity_Kidney_Disease", "Comorbidity_Autoimmune_Disease", "Comorbidity_Other", "Performance_Status", "Blood_Pressure_Systolic", "Blood_Pressure_Diastolic", "Blood_Pressure_Pulse", "Hemoglobin_Level", "White_Blood_Cell_Count", "Platelet_Count", "Albumin_Level", "Alkaline_Phosphatase_Level", "Alanine_Aminotransferase_Level", "Aspartate_Aminotransferase_Level", "Creatinine_Level", "LDH_Level", "Calcium_Level", "Phosphorus_Level", "Glucose_Level", "Potassium_Level", "Sodium_Level", "Smoking_Pack_Years"]

## Public description

Title: Five-Year Survival at Diagnosis: Lung Cancer Risk Prediction

Files:
- train.csv: Training data with columns [Id, Survive5Y, ...features].
- test.csv: Test data with columns [Id, ...features] (no Survive5Y).
- sample_submission.csv: Example submission with columns [Id, Survive5Y] (probabilities).

Notes:
- Target Survive5Y is 1 if Survival_Months >= 60, else 0.
- Evaluate using ROC-AUC between predicted probabilities and ground-truth labels.
