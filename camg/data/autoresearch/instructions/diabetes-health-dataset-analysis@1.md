# OpenMLE-fast task

Task ID: `diabetes-health-dataset-analysis@1`

Native metric: `DiabetesRiskAUCMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2871 bytes)
- `data/sample_submission.csv` (12920 bytes); columns: ["Id", "DiabetesProbability"]
- `data/test.csv` (131104 bytes); columns: ["Id", "Age", "Gender", "Ethnicity", "SocioeconomicStatus", "EducationLevel", "BMI", "Smoking", "AlcoholConsumption", "PhysicalActivity", "DietQuality", "SleepQuality", "FamilyHistoryDiabetes", "GestationalDiabetes", "PolycysticOvarySyndrome", "PreviousPreDiabetes", "Hypertension", "SystolicBP", "DiastolicBP", "SerumCreatinine", "BUNLevels", "CholesterolTotal", "CholesterolLDL", "CholesterolHDL", "CholesterolTriglycerides", "AntihypertensiveMedications", "Statins", "FatigueLevels", "QualityOfLifeScore", "HeavyMetalsExposure", "OccupationalExposureChemicals", "WaterQuality", "MedicalCheckupsFrequency", "MedicationAdherence", "HealthLiteracy"]
- `data/train.csv` (525153 bytes); columns: ["Id", "Age", "Gender", "Ethnicity", "SocioeconomicStatus", "EducationLevel", "BMI", "Smoking", "AlcoholConsumption", "PhysicalActivity", "DietQuality", "SleepQuality", "FamilyHistoryDiabetes", "GestationalDiabetes", "PolycysticOvarySyndrome", "PreviousPreDiabetes", "Hypertension", "SystolicBP", "DiastolicBP", "SerumCreatinine", "BUNLevels", "CholesterolTotal", "CholesterolLDL", "CholesterolHDL", "CholesterolTriglycerides", "AntihypertensiveMedications", "Statins", "FatigueLevels", "QualityOfLifeScore", "HeavyMetalsExposure", "OccupationalExposureChemicals", "WaterQuality", "MedicalCheckupsFrequency", "MedicationAdherence", "HealthLiteracy", "Diagnosis"]

## Public description

Diabetes Risk Screening Challenge (Leakage-Aware)

Problem statement
Predict the probability that a patient has a diabetes diagnosis using routinely available, non-diagnostic health information. The provided train/test files exclude direct glycemic markers (e.g., fasting glucose, HbA1c) and overt symptom flags to prevent trivial label leakage. Your goal is to build a robust, well-calibrated model that generalizes across demographics, lifestyle, comorbidities, clinical measurements, medications, and environmental exposures.

Data description
Each row represents one patient. The features are numerically encoded and include (non-exhaustive):
- Demographics and socioeconomic: Age, Gender, Ethnicity, SocioeconomicStatus, EducationLevel
- Lifestyle and behaviors: BMI, Smoking, AlcoholConsumption, PhysicalActivity, DietQuality, SleepQuality, MedicalCheckupsFrequency, MedicationAdherence, HealthLiteracy
- Family and history: FamilyHistoryDiabetes, GestationalDiabetes, PolycysticOvarySyndrome, PreviousPreDiabetes, Hypertension
- Vitals and labs (non-glycemic): SystolicBP, DiastolicBP, SerumCreatinine, BUNLevels, CholesterolTotal, CholesterolLDL, CholesterolHDL, CholesterolTriglycerides
- Medications (non-antidiabetic): AntihypertensiveMedications, Statins
- Symptoms and quality of life (non-overt): QualityOfLifeScore
- Environmental exposures: HeavyMetalsExposure, OccupationalExposureChemicals, WaterQuality

Target
- Diagnosis: 0/1 indicating absence/presence of a diabetes diagnosis.

Provided files
- train.csv: Id, features, and Diagnosis
- test.csv: Id and features (Diagnosis withheld)
- sample_submission.csv: Id and DiabetesProbability (example format)

Submission format
- A CSV with two columns: Id, DiabetesProbability
- DiabetesProbability should be a well-calibrated probability in [0, 1] for Diagnosis = 1.

Evaluation
- Primary metric: ROC-AUC computed on DiabetesProbability versus the hidden Diagnosis labels for the test set. ROC-AUC is threshold-free and robust to moderate class imbalance.
- Ties and constant predictions are handled safely. Submissions with invalid/missing Ids, duplicate Ids, or non-finite predictions will be rejected.

Recommended approach
- Data processing: Standardize or robust-scale continuous variables as needed; handle outliers (e.g., triglycerides) via winsorization or transformations.
- Feature engineering (optional): Interaction terms (e.g., BMI × Age), BP ratios, log transforms for heavy-tailed features.
- Modeling: Try gradient-boosted trees, regularized linear models, and calibrated ensembles. Use cross-validation and stratified folds within train.

Notes
- The feature set is curated to remove direct diagnostic markers and overt hyperglycemia symptoms; the task focuses on screening from non-diagnostic information.
- External data is allowed only if it does not contain patient-level leakage.
