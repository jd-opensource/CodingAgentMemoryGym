# OpenMLE-fast task

Task ID: `diabetes-health-dataset-analysis@2`

Native metric: `DiabetesHbA1cRegressionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3022 bytes)
- `data/sample_submission.csv` (10777 bytes); columns: ["Id", "HbA1c"]
- `data/test.csv` (175305 bytes); columns: ["Id", "Age", "Gender", "Ethnicity", "SocioeconomicStatus", "EducationLevel", "BMI", "Smoking", "AlcoholConsumption", "PhysicalActivity", "DietQuality", "SleepQuality", "FamilyHistoryDiabetes", "GestationalDiabetes", "PolycysticOvarySyndrome", "PreviousPreDiabetes", "Hypertension", "SystolicBP", "DiastolicBP", "FastingBloodSugar", "SerumCreatinine", "BUNLevels", "CholesterolTotal", "CholesterolLDL", "CholesterolHDL", "CholesterolTriglycerides", "AntihypertensiveMedications", "Statins", "AntidiabeticMedications", "FrequentUrination", "ExcessiveThirst", "UnexplainedWeightLoss", "FatigueLevels", "BlurredVision", "SlowHealingSores", "TinglingHandsFeet", "QualityOfLifeScore", "HeavyMetalsExposure", "OccupationalExposureChemicals", "WaterQuality", "MedicalCheckupsFrequency", "MedicationAdherence", "HealthLiteracy", "Diagnosis"]
- `data/train.csv` (549430 bytes); columns: ["Id", "Age", "Gender", "Ethnicity", "SocioeconomicStatus", "EducationLevel", "BMI", "Smoking", "AlcoholConsumption", "PhysicalActivity", "DietQuality", "SleepQuality", "FamilyHistoryDiabetes", "GestationalDiabetes", "PolycysticOvarySyndrome", "PreviousPreDiabetes", "Hypertension", "SystolicBP", "DiastolicBP", "FastingBloodSugar", "HbA1c", "SerumCreatinine", "BUNLevels", "CholesterolTotal", "CholesterolLDL", "CholesterolHDL", "CholesterolTriglycerides", "AntihypertensiveMedications", "Statins", "AntidiabeticMedications", "FrequentUrination", "ExcessiveThirst", "UnexplainedWeightLoss", "FatigueLevels", "BlurredVision", "SlowHealingSores", "TinglingHandsFeet", "QualityOfLifeScore", "HeavyMetalsExposure", "OccupationalExposureChemicals", "WaterQuality", "MedicalCheckupsFrequency", "MedicationAdherence", "HealthLiteracy", "Diagnosis"]

## Public description

HbA1c Estimation from Routine Health Data

Problem statement
Predict the glycated hemoglobin (HbA1c, %) of a patient using routine health, lifestyle, medical history, vital signs, laboratory values, medications, symptoms, and health behavior information. HbA1c reflects average blood glucose over ~3 months and is central to diabetes screening and management. Accurate estimation from routinely collected features can help prioritize diagnostic testing.

Files
- train.csv: Labeled training data with one row per patient. Includes an Id column and all predictive features plus the target column HbA1c.
- test.csv: Unlabeled test data with the same feature columns as train.csv (excluding HbA1c) and an Id column.
- sample_submission.csv: Submission template with columns Id and HbA1c.

Target
- HbA1c: continuous percentage value across the full observed range (approximately 4.0–10.0%).

Features
All columns in train.csv except HbA1c are candidate features. These include (non-exhaustive list): Age, Gender, Ethnicity, SocioeconomicStatus, EducationLevel, BMI, Smoking, AlcoholConsumption, PhysicalActivity, DietQuality, SleepQuality, FamilyHistoryDiabetes, GestationalDiabetes, PolycysticOvarySyndrome, PreviousPreDiabetes, Hypertension, SystolicBP, DiastolicBP, FastingBloodSugar, SerumCreatinine, BUNLevels, CholesterolTotal, CholesterolLDL, CholesterolHDL, CholesterolTriglycerides, AntihypertensiveMedications, Statins, AntidiabeticMedications, FrequentUrination, ExcessiveThirst, UnexplainedWeightLoss, FatigueLevels, BlurredVision, SlowHealingSores, TinglingHandsFeet, QualityOfLifeScore, HeavyMetalsExposure, OccupationalExposureChemicals, WaterQuality, MedicalCheckupsFrequency, MedicationAdherence, HealthLiteracy, Diagnosis.
Note: DoctorInCharge is removed and not part of the features.

Evaluation
- Metric: Mean Absolute Error (MAE) between the submitted HbA1c predictions and the ground truth, matched by Id.
- Submission format: A CSV file with exactly two columns and a header: Id, HbA1c. Ids must match test.csv exactly (order does not matter), and HbA1c values must be finite numbers.

Guidance and expectations
- Data processing: The data is fully numeric/categorical-encoded and contains no missing values. Standardization may benefit linear models. Consider variance-stabilizing transforms (e.g., logs) for skewed lab values (e.g., triglycerides) if desired.
- Feature engineering: Optional but encouraged (e.g., pulse pressure = SystolicBP − DiastolicBP, interactions such as BMI×Age, nonlinear transforms). Avoid target leakage.
- Modeling: Any supervised regression method is allowed, including linear models, gradient boosted trees, random forests, neural networks, and ensembles. Cross-validation should be performed using train.csv only.
- Reproducibility: Keep your pipelines deterministic via fixed random seeds when possible.

Goal
Build accurate, robust regressors for HbA1c estimation across the full range observed in the dataset. The leaderboard is ranked by MAE (lower is better).
