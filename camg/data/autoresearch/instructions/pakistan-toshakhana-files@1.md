# OpenMLE-fast task

Task ID: `pakistan-toshakhana-files@1`

Native metric: `ToshakhanaValueMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2688 bytes)
- `data/sample_submission.csv` (11861 bytes); columns: ["id", "Assessed Value"]
- `data/test.csv` (67225 bytes); columns: ["id", "Detail of Gifts", "Item Category", "Name of Recipient", "Affiliation", "Date", "Retained", "Retention Cost"]
- `data/train.csv` (275066 bytes); columns: ["id", "Detail of Gifts", "Item Category", "Name of Recipient", "Affiliation", "Date", "Retained", "Retention Cost", "Assessed Value"]

## Public description

Title: Toshakhana Gift Value Estimation Challenge

Problem statement:
Predict the officially assessed monetary value of a gift recorded in the Pakistan Toshakhana archives. Each record includes a detailed description of the gift, item category, recipient, affiliation, date, retention status, and retention cost. Your task is to build a model that estimates the Assessed Value for unseen records.

Why it’s interesting and challenging:
- Real-world, messy, multilingual textual descriptions interspersed with structured fields.
- Highly skewed target distribution spanning small items to luxury assets.
- Requires careful data processing, feature engineering, and robust modeling under noise and irregular formatting.

Data description:
- train.csv: Feature columns plus the target.
  - id: Integer identifier.
  - Detail of Gifts: Text description of the gift.
  - Item Category: Gift category (e.g., Decoration Pieces, Carpet, etc.).
  - Name of Recipient: Recipient name and role.
  - Affiliation: Affiliation/era (e.g., Gen. Musharraf, etc.).
  - Date: Gift date as text (parse as needed).
  - Retained: Whether the gift was retained/auctioned/etc.
  - Retention Cost: Numeric cost associated with retention.
  - Assessed Value: Target variable (numeric, non-negative).
- test.csv: Same feature columns as train.csv except without Assessed Value.
- sample_submission.csv: A valid-format sample submission with random plausible predictions for all test ids.

Target:
- Assessed Value (numeric, non-negative). Consider predicting in log space and transforming back for stability.

Evaluation metric:
- Symmetric Mean Absolute Percentage Error (SMAPE) on Assessed Value.
  - SMAPE = 200 * mean(|pred - true| / (|pred| + |true|)).
  - Lower is better. Robust to scale and bounded in [0, 200].

Submission format:
- CSV with exactly two columns and header: id, Assessed Value.
- id must match those in test.csv.
- Assessed Value must be numeric, finite, and non-negative.

Notes and recommendations:
- Text cleaning matters: normalize whitespace, handle line breaks, punctuation, and multilingual tokens.
- Feature engineering ideas: parse size/count from descriptions; extract currency hints; item-level taxonomy; recipient/affiliation embeddings; temporal features from date; retention status and cost interactions.
- Modeling ideas: gradient boosting on engineered features; text encoders (TF-IDF, word/subword embeddings); hybrid models combining text and structure.
- Evaluation tips: predict in log1p space, calibrate outputs, and consider quantile losses to handle skew.
- Ensure reproducibility and avoid data leakage; use only train.csv for training and test.csv for inference.
