# OpenMLE-fast task

Task ID: `electric-vehicle-population-analysis@1`

Native metric: `ElectricVehicleRangeMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2801 bytes)
- `data/sample_submission.csv` (180925 bytes); columns: ["Id", "Electric Range"]
- `data/test.csv` (3718535 bytes); columns: ["County", "City", "Postal Code", "Model Year", "Make", "Model", "Electric Vehicle Type", "Clean Alternative Fuel Vehicle (CAFV) Eligibility", "Base MSRP", "Legislative District", "Vehicle Location", "Electric Utility", "2020 Census Tract", "Id"]
- `data/train.csv` (17777160 bytes); columns: ["County", "City", "Postal Code", "Model Year", "Make", "Model", "Electric Vehicle Type", "Clean Alternative Fuel Vehicle (CAFV) Eligibility", "Electric Range", "Base MSRP", "Legislative District", "Vehicle Location", "Electric Utility", "2020 Census Tract"]

## Public description

Title: Washington EV Range Prediction

Overview
Predict the Electric Range (in miles) of registered electric vehicles in Washington State from rich tabular attributes about the vehicle, policy eligibility, utility service area, and local context. This is a supervised regression task designed to reward models that generalize to unseen vehicle profiles and handle high-cardinality categorical features, textual noise, and missingness.

Files
- train.csv — feature columns and the target column Electric Range.
- test.csv — the same feature columns plus an Id column; Electric Range is withheld.
- sample_submission.csv — example submission with columns [Id, Electric Range].

Target
- Electric Range: numeric, strictly positive values (miles).

Features (typical)
- Vehicle: Model Year, Make, Model, Electric Vehicle Type (e.g., BEV, PHEV), Base MSRP
- Policy: Clean Alternative Fuel Vehicle (CAFV) Eligibility (text label)
- Geography and context: County, City, Postal Code, Legislative District, 2020 Census Tract, Electric Utility (may contain multiple utilities delimited by | or ||), Vehicle Location (POINT (lon lat) as text)

Notes on data preparation
- Rows with ambiguous/missing target information were removed to ensure a clean regression target (e.g., Electric Range reported as 0 or eligibility text indicating range is unknown).
- To prevent leakage from exact duplicates, groups defined by [Model Year, Make, Model, Electric Vehicle Type, CAFV Eligibility] are assigned entirely to either train or test (dedup-aware split). This creates a challenging generalization setting where identical profiles do not appear across splits.
- Identifier columns that enable memorization are not included. High-cardinality and multi-valued fields are retained to encourage feature engineering.

Evaluation
- Metric: Mean Absolute Error (MAE) on Electric Range.
  - MAE is robust to outliers and directly interpretable in miles, encouraging consistent accuracy across diverse models and years.

Submission
- Submit a CSV with exactly two columns in this order:
  - Id: the integer identifier provided in test.csv
  - Electric Range: your numeric prediction (miles) for the corresponding Id
- Predictions must be numeric and finite. The leaderboard is computed using MAE.

What makes this challenging
- Generalization to unseen vehicle profiles due to dedup-aware splitting (no identical [year, make, model, type, CAFV] combinations shared between train and test).
- Mixed feature types and scales: free-text model names, multi-valued utility fields, geography, and policy labels.
- Missingness and ambiguity in real-world administrative data (e.g., MSRP=0 as missing, unstandardized strings) require careful preprocessing.

Final competition files
- train.csv
- test.csv
- sample_submission.csv
