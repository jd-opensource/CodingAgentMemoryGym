# OpenMLE-fast task

Task ID: `house-price-prediction-seattle@2`

Native metric: `SeattleMillionLogLossMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2151 bytes)
- `data/sample_submission.csv` (11643 bytes); columns: ["id", "is_million"]
- `data/test.csv` (19138 bytes); columns: ["id", "beds", "baths", "size", "size_units", "lot_size", "lot_size_units", "zip_code"]
- `data/train.csv` (88333 bytes); columns: ["id", "beds", "baths", "size", "size_units", "lot_size", "lot_size_units", "zip_code", "is_million"]

## Public description

Seattle Million‑Dollar Home Classification

Problem statement
Participants must predict the probability that a Seattle home sold for more than $1,000,000 based on tabular property attributes and a location proxy (ZIP code). Your model should output well‑calibrated probabilities, not hard labels.

Data description
Final files provided:
- train.csv: Training features and target.
  - Columns: id, beds, baths, size, size_units, lot_size, lot_size_units, zip_code, is_million
  - is_million is the binary target: 1 if sale price > 1,000,000; else 0.
  - price is not included to prevent leakage.
- test.csv: Test features (no target).
  - Columns: id, beds, baths, size, size_units, lot_size, lot_size_units, zip_code
- sample_submission.csv: Example submission with random but valid probabilities.
  - Columns: id, is_million

Notes:
- size_units is typically “sqft”. lot_size may be in sqft or acres; 1 acre = 43,560 sqft.
- Some lot_size values are missing; handle missingness robustly.
- ZIP codes are categorical; careful encoding can improve generalization.

Submission format
- A single CSV file with two columns: id, is_million
- id must match exactly the ids in test.csv (same set and count, unique).
- is_million must be a probability in [0, 1].

Evaluation
- Metric: Binary Log Loss (cross‑entropy) computed over all test rows.
- Definition: For each test row i with ground truth yi ∈ {0,1} and submitted probability pi ∈ [0,1], the score is
  LogLoss = −(1/N) * Σ [ yi * log(pi) + (1 − yi) * log(1 − pi) ]
- Submissions are validated for format (columns, ids, finiteness) and probabilities are numerically clipped to a small epsilon away from 0 and 1 when scoring to avoid numerical issues.

Modeling guidance (optional)
- Useful features often include: size, baths, interactions (beds×baths), log transforms of size and lot size, and ZIP encodings.
- Convert lot sizes expressed in acres to square feet and consider missingness flags.
- Calibrated classifiers (e.g., gradient boosting with probability calibration, logistic regression, or tree‑based models that natively output probabilities) tend to perform well.
