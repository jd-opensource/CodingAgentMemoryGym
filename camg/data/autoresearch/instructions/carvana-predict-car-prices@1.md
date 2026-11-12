# OpenMLE-fast task

Task ID: `carvana-predict-car-prices@1`

Native metric: `CarvanaPricePredictionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2981 bytes)
- `data/sample_submission.csv` (60124 bytes); columns: ["id", "Price"]
- `data/test.csv` (142548 bytes); columns: ["id", "Name", "Year", "Miles"]
- `data/train.csv` (695678 bytes); columns: ["id", "Name", "Year", "Miles", "Price"]

## Public description

Carvana Used Car Price Prediction

Problem statement
Build a model that predicts the resale price (USD) of a used car listing using its textual make/model name, model year, and mileage. Listings include messy name strings and occasional digit contamination in the year field (e.g., “20173” implying the model “X3”), making robust preprocessing and feature engineering essential.

Data description
- train.csv: Training data with columns
  - id: unique identifier for each row (no predictive signal)
  - Name: make/model string, cleaned to preserve informative punctuation and digits
  - Year: 4-digit model year (1990–2023)
  - Miles: non-negative integer mileage
  - Price: target label in USD (positive number)
- test.csv: Test data with columns id, Name, Year, Miles (no Price). The id column aligns with sample_submission.csv.
- sample_submission.csv: Template for submissions with id and Price for each test id.

Evaluation
- Metric: RMSLE (root mean squared logarithmic error) on Price + 1
  - For each test id, let y be the true price and p be the submitted prediction. We score on log(y + 1) vs log(max(0, p) + 1) and report the root mean squared error over all ids.
  - Motivation: Price spans a broad range. RMSLE emphasizes proportional error and is robust to right-skewed targets while remaining smooth and stable.

What you should build
- Data processing: Normalize whitespace in Name, preserve informative punctuation (e.g., hyphens) and digits, and ensure Year/Miles are valid numerics. Handling of year-digit contamination is often beneficial (e.g., recovering “X3” from “20173” cases).
- Feature engineering:
  - Text: character and word n-grams over Name, keeping digit and hyphen information; subword tokenization can help with variants like “CX-5”, “QX50”, “A3”, etc.
  - Structured: Year, Miles, interactions such as Year × log(Miles + 1), polynomial terms, and monotonic transforms to capture diminishing returns.
- Modeling: Any regression approach is allowed (e.g., gradient boosting, regularized linear models with text features, neural models over character n-grams). Use cross-validation on train.csv to select and tune models.
- Validation tips: Duplicated or near-duplicated rows can exist. Consider group-aware CV by identical (Name, Year, Miles) triplets within train to reduce optimistic leakage across folds.

Submission format
- A CSV file with exactly two columns in any row order: id, Price
- id must match the set of ids in test.csv with no duplicates or missing rows
- Price must be numeric; negative values are clipped to 0 during scoring

Files provided
- train.csv
- test.csv
- sample_submission.csv

Practical guidance
- Do not use id as a feature; it is a random identifier.
- Consider modeling in log-space and exponentiating at inference; the official scoring is on the original scale using RMSLE.
- Be mindful of rare models and trims; robust text representations and regularization help generalization.
