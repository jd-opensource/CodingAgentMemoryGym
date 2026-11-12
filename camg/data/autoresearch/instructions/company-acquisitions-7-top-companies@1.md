# OpenMLE-fast task

Task ID: `company-acquisitions-7-top-companies@1`

Native metric: `TechAcquisitionsF1Metrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3507 bytes)
- `data/sample_submission.csv` (3063 bytes); columns: ["row_id", "Parent Company"]
- `data/test.csv` (15518 bytes); columns: ["row_id", "Acquisition Year", "Acquisition Month", "Acquired Company", "Business", "Country", "Acquisition Price"]
- `data/train.csv` (72143 bytes); columns: ["row_id", "Acquisition Year", "Acquisition Month", "Acquired Company", "Business", "Country", "Acquisition Price", "Parent Company"]

## Public description

Who’s the Buyer? Predict the Acquiring Tech Company

Problem statement
You are given historical M&A events in the technology sector. For each acquisition event, use the event’s attributes (date, acquired company name, a short business description, country, and price where available) to predict which of the 14 major tech companies made the acquisition.

Your task
- Train a model on past acquisition events and predict the acquiring company for unseen events.
- You will receive a training file with features and the target label, and a test file with only features. Submit predicted labels for the test rows.

Files provided
- train.csv: Training data with features and the target column.
- test.csv: Test data with the same features as train.csv, without the target column.
- sample_submission.csv: A sample submission file demonstrating the required format.

Columns
Each row represents a single acquisition event. The files contain the following columns:
- row_id: Unique identifier for the row (use this to align your predictions in submissions).
- Acquisition Year: Year of the acquisition (integer).
- Acquisition Month: Month of the acquisition (e.g., Jan, Feb, …, or missing/unknown).
- Acquired Company: Name of the acquired company (free text).
- Business: Short description of the acquired company’s business (free text).
- Country: Country of the acquired company (may be missing/unknown).
- Acquisition Price: Acquisition value when known (numeric where available; missing when undisclosed or unavailable).
- Parent Company: Only in train.csv. The acquiring company (one of 14 tech companies). This is the target to predict.

Notes on data
- The data spans 1957–2021 and includes substantial missingness in Country and Acquisition Price. Treat unknowns carefully.
- Text fields (Acquired Company, Business) are noisy free text and can be powerful signals when modeled well.
- Some auxiliary fields present in the original source (such as Category, Derived Products, and raw IDs) are not included to prevent label leakage and keep the task focused.

Target labels
- Parent Company has 14 classes (e.g., Microsoft, Google, IBM, HP, Apple, Amazon, Facebook, Twitter, eBay, Adobe, Citrix, Red Hat, BlackBerry, Disney).

Submission format
- A CSV with exactly the following columns and header:
  - row_id
  - Parent Company
- Include one row per row_id that appears in test.csv, no more and no fewer.
- The Parent Company values must be one of the valid class names present in train.csv.

Evaluation
- Metric: Macro F1 score computed over the 14 acquiring-company classes present in the test set.
- Rationale: Macro F1 gives each company equal weight and penalizes models that ignore minority classes, which is important given class imbalance.

Practical tips
- You are encouraged to combine text and tabular features. Common baselines include TF–IDF + linear models, tree ensembles on engineered features, and lightweight text encoders combined with tabular inputs.
- Handle missing months, countries, and prices explicitly (e.g., unknown categories, missing-value indicators).
- Beware temporal drift across decades; consider using temporal features judiciously.

File integrity and constraints
- The test file does not contain the Parent Company label. Your submission must predict it.
- row_id values in your submission must match those in test.csv exactly; duplicates or missing/extra ids are not allowed.
- Predictions must be valid class names.

Good luck and have fun modeling!
