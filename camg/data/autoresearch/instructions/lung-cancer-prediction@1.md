# OpenMLE-fast task

Task ID: `lung-cancer-prediction@1`

Native metric: `LungCancerStageMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2538 bytes)
- `data/sample_submission.csv` (108788 bytes); columns: ["Id", "Stage"]
- `data/test.csv` (1886599 bytes); columns: ["Id", "Age", "Gender", "Smoking_History", "Tumor_Size_mm", "Tumor_Location", "Ethnicity", "Insurance_Type", "Family_History", "Comorbidity_Diabetes", "Comorbidity_Hypertension", "Comorbidity_Heart_Disease", "Comorbidity_Chronic_Lung_Disease", "Comorbidity_Kidney_Disease", "Comorbidity_Autoimmune_Disease", "Comorbidity_Other", "Performance_Status", "Blood_Pressure_Systolic", "Blood_Pressure_Diastolic", "Blood_Pressure_Pulse", "Hemoglobin_Level", "White_Blood_Cell_Count", "Platelet_Count", "Albumin_Level", "Alkaline_Phosphatase_Level", "Alanine_Aminotransferase_Level", "Aspartate_Aminotransferase_Level", "Creatinine_Level", "LDH_Level", "Calcium_Level", "Phosphorus_Level", "Glucose_Level", "Potassium_Level", "Sodium_Level", "Smoking_Pack_Years"]
- `data/train.csv` (7451616 bytes); columns: ["Age", "Gender", "Smoking_History", "Tumor_Size_mm", "Tumor_Location", "Stage", "Ethnicity", "Insurance_Type", "Family_History", "Comorbidity_Diabetes", "Comorbidity_Hypertension", "Comorbidity_Heart_Disease", "Comorbidity_Chronic_Lung_Disease", "Comorbidity_Kidney_Disease", "Comorbidity_Autoimmune_Disease", "Comorbidity_Other", "Performance_Status", "Blood_Pressure_Systolic", "Blood_Pressure_Diastolic", "Blood_Pressure_Pulse", "Hemoglobin_Level", "White_Blood_Cell_Count", "Platelet_Count", "Albumin_Level", "Alkaline_Phosphatase_Level", "Alanine_Aminotransferase_Level", "Aspartate_Aminotransferase_Level", "Creatinine_Level", "LDH_Level", "Calcium_Level", "Phosphorus_Level", "Glucose_Level", "Potassium_Level", "Sodium_Level", "Smoking_Pack_Years"]

## Public description

Title: Lung Cancer Stage Prediction (I–IV)

Problem Statement:
Predict the clinical stage of lung cancer (Stage I, Stage II, Stage III, Stage IV) at diagnosis using tabular patient data. The dataset contains demographics, lifestyle, comorbidities, performance status, vitals, and laboratory measurements. The task is a four-class classification problem.

Data Description:
- Train file: train.csv — rows with features and the target column "Stage".
- Test file: test.csv — rows with features only plus an "Id" column for identification.
- Sample submission: sample_submission.csv — example of the required submission format.

Feature categories include (non-exhaustive):
- Demographics: Age, Gender, Ethnicity, Insurance_Type, Family_History
- Smoking: Smoking_History, Smoking_Pack_Years
- Tumor characteristics: Tumor_Size_mm, Tumor_Location
- Functional status: Performance_Status
- Vitals: Blood_Pressure_Systolic, Blood_Pressure_Diastolic, Blood_Pressure_Pulse
- Labs: Hemoglobin_Level, White_Blood_Cell_Count, Platelet_Count, Albumin_Level, Alkaline_Phosphatase_Level, Alanine_Aminotransferase_Level, Aspartate_Aminotransferase_Level, Creatinine_Level, LDH_Level, Calcium_Level, Phosphorus_Level, Glucose_Level, Potassium_Level, Sodium_Level
- Comorbidities (Yes/No flags): Diabetes, Hypertension, Heart_Disease, Chronic_Lung_Disease, Kidney_Disease, Autoimmune_Disease, Other

Participants may perform feature engineering (e.g., categorical encoding, normalization), train models (e.g., gradient boosting, neural nets, ensembles), and evaluate using the metric described below.

Evaluation Metric:
- Macro F1 score across the four stage classes. This metric assigns equal weight to each class and balances precision and recall, making it robust under mild class imbalance.
- Submission format: CSV with columns [Id, Stage]. Stage must be one of {"Stage I", "Stage II", "Stage III", "Stage IV"}.

Notes:
- The test set contains all four classes and each class appears in the training set.
- No filesystem paths should be included in any CSV values.
- Do not attempt to infer labels from leaked identifiers or treatment/outcome variables; they are not present in the provided competition files.

Getting Started:
- Load train.csv, perform preprocessing (e.g., impute if needed, encode categorical variables, scale continuous features), and fit a multi-class classifier.
- Use test.csv to generate predictions, create a CSV with columns [Id, Stage], and submit.

Files Provided:
- train.csv
- test.csv
- sample_submission.csv
