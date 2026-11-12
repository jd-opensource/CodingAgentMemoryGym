# OpenMLE-fast task

Task ID: `hospital-ratings@1`

Native metric: `HospitalRatingsMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3339 bytes)
- `data/sample_submission.csv` (6345 bytes); columns: ["Provider ID", "Hospital overall rating"]
- `data/test.csv` (218019 bytes); columns: ["Provider ID", "Hospital Name", "City", "State", "ZIP Code", "County Name", "Hospital Type", "Hospital Ownership", "Emergency Services", "Meets criteria for meaningful use of EHRs", "Mortality national comparison", "Safety of care national comparison", "Readmission national comparison", "Patient experience national comparison", "Effectiveness of care national comparison", "Timeliness of care national comparison", "Efficient use of medical imaging national comparison"]
- `data/train.csv` (875542 bytes); columns: ["Provider ID", "Hospital Name", "City", "State", "ZIP Code", "County Name", "Hospital Type", "Hospital Ownership", "Emergency Services", "Meets criteria for meaningful use of EHRs", "Mortality national comparison", "Safety of care national comparison", "Readmission national comparison", "Patient experience national comparison", "Effectiveness of care national comparison", "Timeliness of care national comparison", "Efficient use of medical imaging national comparison", "Hospital overall rating"]

## Public description

Title: Predict Medicare Hospital Overall Star Rating (1–5)

Overview
Participants are challenged to predict the Medicare Hospital “overall star rating” (an ordinal score from 1 to 5) for U.S. hospitals using hospital characteristics and quality domain national-comparison indicators. This task requires robust handling of mixed-type tabular data, missing values encoded as “Not Available,” and class imbalance (few 1-star and 5-star hospitals).

Problem Statement
Given hospital-level attributes and national-comparison indicators across multiple care domains, build a model that predicts the hospital overall star rating (1–5) for the held-out test hospitals.

Files
- train.csv: Labeled rows with features and the target column Hospital overall rating.
- test.csv: Unlabeled rows with the same features as train.csv (without Hospital overall rating). You must predict this target for each hospital.
- sample_submission.csv: A sample file showing the required submission format.

Target
- Hospital overall rating: Integer in {1, 2, 3, 4, 5}.

Features
All columns below appear in both train.csv and test.csv (the target is present only in train.csv):
- Provider ID (unique hospital identifier)
- Hospital Name
- City
- State
- ZIP Code (string; preserves leading zeros)
- County Name
- Hospital Type
- Hospital Ownership
- Emergency Services (Yes/No)
- Meets criteria for meaningful use of EHRs (e.g., Y/N/Not Available)
- Mortality national comparison (Above/Same/Below/Not Available)
- Safety of care national comparison (Above/Same/Below/Not Available)
- Readmission national comparison (Above/Same/Below/Not Available)
- Patient experience national comparison (Above/Same/Below/Not Available)
- Effectiveness of care national comparison (Above/Same/Below/Not Available)
- Timeliness of care national comparison (Above/Same/Below/Not Available)
- Efficient use of medical imaging national comparison (Above/Same/Below/Not Available)

Notes
- Only rows with a valid numeric Hospital overall rating are included in train/test. Rows with missing ratings are excluded.
- Several descriptive or footnote columns from the source table were removed to avoid unstructured notes and potential leakage. The remaining columns are standardized categorical or structured fields suitable for ML.
- Treat “Not Available” as a distinct category.

Submission Format
- CSV with columns: Provider ID, Hospital overall rating
- Provider ID must match the identifiers in test.csv.
- Hospital overall rating must be an integer in {1, 2, 3, 4, 5}.
- The order of rows does not matter, but all test hospitals must be present exactly once.

Evaluation
- Metric: Quadratic Weighted Kappa (QWK) computed between your predictions and the ground truth Hospital overall rating on the test set.
- Why QWK? The star rating is ordinal. QWK penalizes larger errors more than near-misses, and accounts for class imbalance better than accuracy or unweighted F1.

Modeling Tips
- Encode categorical features (including “Not Available”) carefully (e.g., one-hot or target encoding). Consider preserving ZIP Code as a string or using its prefix to reduce sparsity.
- Handle mixed data types and class imbalance. Ordinal-aware losses, calibrated probabilities, and ensembling can help.
- Cross-validation with stratification on the target is recommended.
