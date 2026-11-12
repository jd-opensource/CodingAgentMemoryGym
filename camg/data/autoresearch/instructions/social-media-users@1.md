# OpenMLE-fast task

Task ID: `social-media-users@1`

Native metric: `SocialMediaUsersAgeMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2314 bytes)
- `data/sample_submission.csv` (565081 bytes); columns: ["id", "age"]
- `data/test.csv` (1624473 bytes); columns: ["id", "gender", "interests", "city", "country"]
- `data/train.csv` (7970714 bytes); columns: ["id", "gender", "interests", "city", "country", "age"]

## Public description

Global Social Media Age Estimation Challenge

Problem statement
Predict each user’s age in years from non-identifying social signals. You are given Interests (a comma-separated list of interest categories), City, Country, and Gender. Your task is to build a model that accurately estimates continuous age from these features across a globally diverse population.

Data description
- train.csv: Feature columns plus the training label.
  - id: anonymized user identifier
  - gender: categorical (e.g., Male, Female)
  - interests: text list of interest categories (comma-separated)
  - city: city name (string, high cardinality)
  - country: country name (string)
  - age: label to predict; age in years as of 2025-07-01
- test.csv: Feature columns only (same schema as train.csv minus the label).
  - id, gender, interests, city, country
- sample_submission.csv: Example submission file with the required format.
  - id, age

Label definition
Age is computed from the provided date of birth (DOB) as of a fixed reference date, 2025-07-01. The label reflects continuous age in years using the conversion: age_years = (reference_date − DOB) / 365.2425.

What you can use
- Features available at inference: interests, city, country, gender.
- Do not rely on name or raw DOB; those are not included in the released train/test files to prevent leakage.

Recommended modeling considerations
- Interests often contain duplicates and varied capitalization. Consider rigorous text parsing and canonicalization, de-duplication, and multi-hot or embedding-based encodings.
- City is high-cardinality; hashing, frequency/target encoding, or learned embeddings can help.
- Country and gender can be encoded categorically.
- Robust regularization and non-linear models (e.g., gradient boosting or tabular neural nets) generally perform well.

Evaluation
- Metric: Mean Absolute Error (MAE) on age in years.
- Submission format: A CSV with two columns: id and age. The id set must match the test.csv ids exactly; ages must be finite numeric values.

Goal
Minimize MAE by building a strong feature processing and modeling pipeline that generalizes across countries and interest profiles. The task emphasizes careful data cleaning, high-cardinality categorical handling, and fair evaluation across a globally diverse user base.
