# OpenMLE-fast task

Task ID: `parkinsons-disease-dataset-analysis@1`

Native metric: `ParkinsonsDiseaseAUCMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2542 bytes)
- `data/sample_submission.csv` (3809 bytes); columns: ["PatientID", "Diagnosis"]
- `data/test.csv` (118531 bytes); columns: ["PatientID", "Age", "Gender", "Ethnicity", "EducationLevel", "BMI", "Smoking", "AlcoholConsumption", "PhysicalActivity", "DietQuality", "SleepQuality", "FamilyHistoryParkinsons", "TraumaticBrainInjury", "Hypertension", "Diabetes", "Depression", "Stroke", "SystolicBP", "DiastolicBP", "CholesterolTotal", "CholesterolLDL", "CholesterolHDL", "CholesterolTriglycerides", "UPDRS", "MoCA", "FunctionalAssessment", "Tremor", "Rigidity", "Bradykinesia", "PosturalInstability", "SpeechProblems", "SleepDisorders", "Constipation", "DoctorInCharge"]
- `data/train.csv` (475960 bytes); columns: ["PatientID", "Age", "Gender", "Ethnicity", "EducationLevel", "BMI", "Smoking", "AlcoholConsumption", "PhysicalActivity", "DietQuality", "SleepQuality", "FamilyHistoryParkinsons", "TraumaticBrainInjury", "Hypertension", "Diabetes", "Depression", "Stroke", "SystolicBP", "DiastolicBP", "CholesterolTotal", "CholesterolLDL", "CholesterolHDL", "CholesterolTriglycerides", "UPDRS", "MoCA", "FunctionalAssessment", "Tremor", "Rigidity", "Bradykinesia", "PosturalInstability", "SpeechProblems", "SleepDisorders", "Constipation", "Diagnosis", "DoctorInCharge"]

## Public description

Title: Parkinson’s Diagnosis Prediction from Multi-domain Clinical Data

Problem statement
- Build a model that predicts the probability that a patient has Parkinson’s Disease (PD) using a comprehensive clinical snapshot spanning demographics, lifestyle, medical history, vitals, laboratory lipids, cognitive/functional scores, and symptom flags.
- Submit one probability per patient indicating the likelihood of PD (class 1). Higher values mean higher risk.

Files
- train.csv: Tabular training data with features and the target column Diagnosis.
- test.csv: Tabular test data with the same features as train.csv except Diagnosis is withheld.
- sample_submission.csv: Example submission file with two columns: PatientID and Diagnosis (a probability in [0,1]).

Target
- Diagnosis: binary label where 1 indicates PD and 0 indicates no PD.

Features
- Inputs cover multiple domains: Age, Gender, Ethnicity, EducationLevel, BMI, Smoking, AlcoholConsumption, PhysicalActivity, DietQuality, SleepQuality, FamilyHistoryParkinsons, TraumaticBrainInjury, Hypertension, Diabetes, Depression, Stroke, SystolicBP, DiastolicBP, CholesterolTotal, CholesterolLDL, CholesterolHDL, CholesterolTriglycerides, UPDRS, MoCA, FunctionalAssessment, Tremor, Rigidity, Bradykinesia, PosturalInstability, SpeechProblems, SleepDisorders, Constipation. PatientID is provided as a stable identifier to join predictions and must not be used as a predictive feature.

Evaluation
- Metric: ROC AUC on predicted probabilities for class 1.
- Rationale: AUC is threshold-free, robust to moderate class imbalance, and appropriately evaluates ranking quality for clinical risk triage.
- Submission format: CSV with columns [PatientID, Diagnosis] where Diagnosis is a probability in [0,1]. The PatientID values must exactly match those in test.csv.

Rules and guidance
- Use any ML approach suitable for tabular data (e.g., regularized linear models, gradient boosting, calibrated ensembles). Feature engineering, careful preprocessing, and probability calibration are encouraged.
- Treat binary columns as binary features; consider one-hot encoding for encoded categorical variables (e.g., Ethnicity, EducationLevel) if your model assumes ordinality.
- Handle numerical stability in inference (no NaN/Inf outputs). Clip or bound predictions to [0, 1].
- Do not engineer features directly from PatientID; it is an identifier only.

Goal
- Achieve the highest ROC AUC by accurately ranking patients by PD risk, making good use of the rich, multi-domain clinical information.
