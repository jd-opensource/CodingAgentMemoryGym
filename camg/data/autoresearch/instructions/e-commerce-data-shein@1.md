# OpenMLE-fast task

Task ID: `e-commerce-data-shein@1`

Native metric: `ECommercePricePredictionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3438 bytes)
- `data/sample_submission.csv` (435385 bytes); columns: ["id", "price_usd"]
- `data/test.csv` (1149862 bytes); columns: ["id", "title", "category", "subcategory", "discount_percent", "color_count", "selling_recent"]
- `data/train.csv` (3573605 bytes); columns: ["id", "title", "category", "subcategory", "discount_percent", "color_count", "selling_recent", "price_usd"]

## Public description

Title: Cross-Category E‑Commerce Price Prediction

Background
You are given a large, noisy, real‑world e‑commerce dataset covering 80,000+ products across 20+ categories. Each row contains a product title plus various metadata fields such as discount, optional color counts, subcategory context, and “sold recently” signals. Prices vary widely and follow a heavy‑tailed distribution.

Problem Statement
Build a machine learning model that predicts the product’s final listed price from text and tabular metadata across all categories. Your solution should robustly handle heterogeneous features, missing values, inconsistent formatting, and duplicates while generalizing across categories.

Data Description
The competition dataset is provided as two CSV files plus a sample submission. Rows represent individual products and the schema is standardized across categories. Columns include:
- id: Unique identifier for each product row.
- title: Product title text (noisy and non‑uniform).
- category: High‑level category (e.g., Electronics, Home & Kitchen, Sports & Outdoors).
- subcategory: Optional subcategory context extracted from rank‑related text (e.g., “in Cable Storage”). May be empty.
- discount_percent: Numeric percent discount when available (e.g., 13.0 for “-13%”). Empty when unavailable.
- color_count: Integer count of available color variants when present. Empty when unavailable.
- selling_recent: Lower‑bound count derived from “X+ sold recently” signals (e.g., 600 or 1500 for “1.5k+”). Empty when unavailable.
- price_usd: The numeric target (final listed USD price). Present only in train.csv.

Files
- train.csv: Features plus the target column price_usd.
- test.csv: Features only (no price_usd).
- sample_submission.csv: Example of the expected submission format.

Notes
- Fields are noisy and may be missing or inconsistently formatted; you are expected to perform data cleaning and feature engineering.
- Missing values in feature columns are represented by empty strings.
- URL‑like columns and other identity‑leaking fields have been removed from the standardized dataset.
- Duplicates and near‑duplicates may exist; robust models should avoid memorization.

Submission Format
Submit a CSV file with the following columns (exact header order required):
- id: Must match the ids in test.csv.
- price_usd: Your predicted prices as non‑negative finite numbers.

Evaluation Metric
Root Mean Squared Logarithmic Error (RMSLE) between your predictions and the hidden ground truth:
- Computed as sqrt(mean((log(1 + y_pred) − log(1 + y_true))^2))).
- Predictions are clipped at 0 to avoid negative values.
- RMSLE fairly penalizes multiplicative errors and reduces the impact of extreme outliers common in price data.

Expectations and Hints
- Strong baselines can be built with TF‑IDF over title text plus tabular features (discount_percent, color_count, selling_recent, category/subcategory).
- Improved solutions may use pretrained text embeddings, gradient boosting over engineered features, or multimodal tabular‑text models.
- Consider careful normalization, robust parsing of numeric signals, and duplicate/near‑duplicate handling when constructing features.
- Ensure reproducibility and avoid leakage across train/test when constructing features.

Good luck and build robust, generalizable models that price products accurately across diverse categories!
