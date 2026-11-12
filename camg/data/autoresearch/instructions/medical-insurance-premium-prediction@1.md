# OpenMLE-fast task

Task ID: `medical-insurance-premium-prediction@1`

Native metric: `MedicalInsurancePremiumMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3007 bytes)
- `data/sample_submission.csv` (2590 bytes); columns: ["Id", "PremiumPrice"]
- `data/test.csv` (6294 bytes); columns: ["Id", "Age", "Diabetes", "BloodPressureProblems", "AnyTransplants", "AnyChronicDiseases", "Height", "Weight", "KnownAllergies", "HistoryOfCancerInFamily", "NumberOfMajorSurgeries"]
- `data/train.csv` (29356 bytes); columns: ["Id", "Age", "Diabetes", "BloodPressureProblems", "AnyTransplants", "AnyChronicDiseases", "Height", "Weight", "KnownAllergies", "HistoryOfCancerInFamily", "NumberOfMajorSurgeries", "PremiumPrice"]

## Public description

Premium INR Prediction (Tabular Regression)

Overview
An insurer wants to price yearly medical coverage (in ₹) for new customers based on basic demographic and health risk factors captured at signup. Your task is to build a model that predicts the yearly premium for unseen customers as accurately as possible.

Files
- train.csv — Labeled training set. Includes an Id column, the target PremiumPrice, and all input features.
- test.csv — Unlabeled test set. Includes an Id column and all input features. Participants must predict PremiumPrice for these rows.
- sample_submission.csv — A sample submission file with the required columns and a randomly generated placeholder prediction for each test Id.

Target and features (all numeric)
- Target: PremiumPrice — annual premium in rupees (₹), integer-valued in the dataset.
- Inputs:
  - Age (years)
  - Diabetes (0/1)
  - BloodPressureProblems (0/1)
  - AnyTransplants (0/1)
  - AnyChronicDiseases (0/1)
  - Height (cm)
  - Weight (kg)
  - KnownAllergies (0/1)
  - HistoryOfCancerInFamily (0/1)
  - NumberOfMajorSurgeries (count)

Evaluation
- Metric: Mean Absolute Error (MAE) on PremiumPrice. The official scorer joins your submission with the hidden answers by Id and computes the average absolute difference.
- Submission format: A CSV with columns [Id, PremiumPrice].
  - Id must exactly match the values in test.csv (order does not matter).
  - PremiumPrice must be numeric and finite (float or int). No NaNs/±Inf. No other columns.
  - The metric uses raw numeric values; you may output any real numbers. Rounding to the nearest ₹1000 is optional (not required) and may or may not help.

What makes this challenging
- The sample size is modest, and some risk factors are rare (e.g., AnyTransplants). Balancing bias/variance and capturing interactions is key.
- Premiums exhibit monotonic yet nonlinear trends with certain variables (e.g., age, major surgeries), and values are discretized at coarse steps. Robust modeling and calibration help.

Recommendations (optional)
- Feature engineering: Body Mass Index (BMI = Weight / (Height/100)^2), interactions such as Age × AnyChronicDiseases, or NumberOfMajorSurgeries × AnyTransplants.
- Modeling: Regularized linear models, gradient boosting, random forests, or monotonic-constraint tree models can perform well. Calibrated regression or post-processing to discrete price steps may improve accuracy.
- Validation: Use K-fold or stratified-by-target-bin cross-validation on train.csv to obtain stable estimates.

Rules and checks
- Use only train.csv to train/validate your models. Do not use external data that could reveal the answers.
- Predictions must be provided for every Id in test.csv, with the exact column names [Id, PremiumPrice].
- The scoring script is order-agnostic and merges by Id. Ensure no duplicate Ids and no missing predictions.

Goal
Minimize MAE on the held-out test set by building a robust tabular regression model using the provided health risk features.
