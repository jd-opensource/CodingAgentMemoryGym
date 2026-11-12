# OpenMLE-fast task

Task ID: `dry-eye-disease@1`

Native metric: `DryEyeDiseaseMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3096 bytes)
- `data/sample_submission.csv` (37794 bytes); columns: ["Id", "DED_Probability"]
- `data/test.csv` (273333 bytes); columns: ["Id", "Gender", "Age", "Sleep duration", "Sleep quality", "Stress level", "Blood pressure", "Heart rate", "Daily steps", "Physical activity", "Height", "Weight", "Sleep disorder", "Wake up during night", "Feel sleepy during day", "Caffeine consumption", "Alcohol consumption", "Smoking", "Medical issue", "Ongoing medication", "Smart device before bed", "Average screen time", "Blue-light filter"]
- `data/train.csv` (1124354 bytes); columns: ["Id", "Gender", "Age", "Sleep duration", "Sleep quality", "Stress level", "Blood pressure", "Heart rate", "Daily steps", "Physical activity", "Height", "Weight", "Sleep disorder", "Wake up during night", "Feel sleepy during day", "Caffeine consumption", "Alcohol consumption", "Smoking", "Medical issue", "Ongoing medication", "Smart device before bed", "Average screen time", "Blue-light filter", "Dry Eye Disease"]

## Public description

Dry Eye Disease Risk Prediction (Tabular, Binary Classification)

Problem statement
Build a model that predicts the probability that an individual has Dry Eye Disease (DED) based on demographics, sleep and lifestyle habits, vitals, activity, and screen/device usage. Your model should output well-calibrated probabilities P(DED=Y) for a held-out test set.

Data
- train.csv: Tabular training data. Each row is a subject. Includes an Id column and the target column Dry Eye Disease with values Y/N.
- test.csv: Same columns as train.csv except Dry Eye Disease is withheld. Includes an Id column matching the submission Ids.
- sample_submission.csv: Example submission file with the correct format and randomized probability values.

Input features (columns in train/test besides Id and target):
- Gender, Age, Sleep duration, Sleep quality, Stress level, Blood pressure, Heart rate, Daily steps, Physical activity, Height, Weight, Sleep disorder, Wake up during night, Feel sleepy during day, Caffeine consumption, Alcohol consumption, Smoking, Medical issue, Ongoing medication, Smart device before bed, Average screen time, Blue-light filter

Notes
- Three near-definitional ocular symptom fields are intentionally excluded to prevent label leakage and preserve a clinically meaningful task.
- The Blood pressure column is a string in the format "systolic/diastolic" and can be parsed into numeric components during feature engineering.

Task and expectations
- Use the training data to build a probabilistic binary classifier that outputs P(DED=Y) for each row in the test set.
- You are encouraged to perform comprehensive preprocessing and feature engineering (e.g., parsing blood pressure into systolic/diastolic, scaling or encoding features, handling correlations), model training, and calibration.
- The full dataset is provided; do not subsample for your final submission.

Evaluation metric
- Submissions are evaluated using ROC AUC computed on the predicted probability for the positive class (DED=Y).
- ROC AUC is threshold-free and robust to the moderate class imbalance observed in this dataset.

Submission format
- A CSV with the following columns and no extra columns:
  - Id: integer identifiers exactly matching the Ids in test.csv
  - DED_Probability: a floating-point probability in [0, 1] representing P(DED=Y)
- The submission must contain every Id present in test.csv exactly once. Order does not matter, but duplicates are not allowed.

Rules and guidance
- Use only the columns provided in train/test. The target column is only present in train.csv.
- External data is allowed if it is publicly available to all participants at no cost and cited in your discussion; however, strong baselines can be achieved with the provided data alone.
- Keep deterministic settings for reproducibility in your own validation.

Files provided
- train.csv: training set with features and Dry Eye Disease target
- test.csv: test set with features only
- sample_submission.csv: sample submission file

Good luck, and build models that generalize well and output well-ranked probabilities!
