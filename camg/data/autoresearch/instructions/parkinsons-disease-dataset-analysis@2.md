# OpenMLE-fast task

Task ID: `parkinsons-disease-dataset-analysis@2`

Native metric: `ParkinsonsUPDRSMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3682 bytes)
- `data/sample_submission.csv` (6479 bytes); columns: ["PatientID", "UPDRS"]
- `data/test.csv` (105668 bytes); columns: ["PatientID", "Age", "Gender", "Ethnicity", "EducationLevel", "BMI", "Smoking", "AlcoholConsumption", "PhysicalActivity", "DietQuality", "SleepQuality", "FamilyHistoryParkinsons", "TraumaticBrainInjury", "Hypertension", "Diabetes", "Depression", "Stroke", "SystolicBP", "DiastolicBP", "CholesterolTotal", "CholesterolLDL", "CholesterolHDL", "CholesterolTriglycerides", "MoCA", "FunctionalAssessment", "Tremor", "Rigidity", "Bradykinesia", "PosturalInstability", "SpeechProblems", "SleepDisorders", "Constipation"]
- `data/train.csv` (452402 bytes); columns: ["PatientID", "Age", "Gender", "Ethnicity", "EducationLevel", "BMI", "Smoking", "AlcoholConsumption", "PhysicalActivity", "DietQuality", "SleepQuality", "FamilyHistoryParkinsons", "TraumaticBrainInjury", "Hypertension", "Diabetes", "Depression", "Stroke", "SystolicBP", "DiastolicBP", "CholesterolTotal", "CholesterolLDL", "CholesterolHDL", "CholesterolTriglycerides", "UPDRS", "MoCA", "FunctionalAssessment", "Tremor", "Rigidity", "Bradykinesia", "PosturalInstability", "SpeechProblems", "SleepDisorders", "Constipation"]

## Public description

Problem: Predict UPDRS severity (0–199) for people with Parkinson’s disease using comprehensive clinical, cognitive, symptom, lifestyle, and lab features.

Overview
- Task: Given patient-level tabular features, build a regression model that predicts the Unified Parkinson’s Disease Rating Scale (UPDRS) score.
- Why it matters: UPDRS summarizes overall disease severity and is used widely in clinical practice and research. Accurate prediction requires learning across heterogeneous domains (symptoms, cognition, vitals, lipids, lifestyle), handling nonlinearities, and coping with multicollinearity.

Files
- train.csv: Training rows with all input features and the target column UPDRS.
- test.csv: Test rows with the same input features but without UPDRS.
- sample_submission.csv: Submission template with PatientID and a placeholder UPDRS prediction for each test row.

Target
- UPDRS (continuous, range 0–199).

Input features (columns present in both train.csv and test.csv)
- PatientID: Unique identifier (integer). Use only to join predictions; do not train on it directly.
- Demographics: Age, Gender (0/1), Ethnicity (0: Caucasian, 1: African American, 2: Asian, 3: Other), EducationLevel (0: None, 1: High School, 2: Bachelor’s, 3: Higher).
- Lifestyle: BMI, Smoking (0/1), AlcoholConsumption (units/week), PhysicalActivity (hours/week), DietQuality (0–10), SleepQuality (4–10).
- Medical history: FamilyHistoryParkinsons (0/1), TraumaticBrainInjury (0/1), Hypertension (0/1), Diabetes (0/1), Depression (0/1), Stroke (0/1).
- Clinical measurements: SystolicBP (mmHg), DiastolicBP (mmHg), CholesterolTotal (mg/dL), CholesterolLDL (mg/dL), CholesterolHDL (mg/dL), CholesterolTriglycerides (mg/dL).
- Cognitive/functional: MoCA (0–30), FunctionalAssessment (0–10).
- Symptoms (0/1): Tremor, Rigidity, Bradykinesia, PosturalInstability, SpeechProblems, SleepDisorders, Constipation.

Notes on preprocessing
- Two categorical variables (Ethnicity, EducationLevel) are encoded as integers; you may one-hot encode them. All other binary indicators are 0/1.
- Continuous variables span varied scales; normalization/standardization often helps linear models. Tree-based methods can use raw values.
- The data contains no missing values. Verify and implement robust handling in case your pipeline introduces NaNs or infs.

Evaluation
- Metric: Root Mean Squared Error (RMSE) between your predictions and the ground truth UPDRS on the hidden test set.
  RMSE = sqrt(mean((y_pred − y_true)^2))
- Lower is better.

Submission format
- A CSV with two columns and a header: PatientID,UPDRS
- Each PatientID from test.csv must appear exactly once, in the same row order as test.csv.
- UPDRS must be a finite real number for every row.

Split protocol (already prepared for you)
- A single deterministic 80/20 train/test split was produced, approximately stratified across the range of UPDRS using quantile bins to maintain distributional balance.
- Columns that could cause leakage or add no information (Diagnosis, DoctorInCharge) were removed from both train and test.

Modeling guidance (non-exhaustive)
- Feature engineering: one-hot for categorical, interactions (e.g., Age×Hypertension), nonlinear transforms (splines), rank-normalization for heavy-tailed lipids.
- Models: regularized linear (Ridge/Lasso/ElasticNet), tree ensembles (Random Forest, XGBoost/LightGBM/CatBoost), kernel methods, or stacking.
- Validation: use cross-validation or repeated K-fold with stratification on UPDRS quantile bins to stabilize estimates.

Goal
- Achieve the lowest RMSE you can while ensuring predictions are clinically plausible and robust across the full UPDRS range.
