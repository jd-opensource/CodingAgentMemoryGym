# OpenMLE-fast task

Task ID: `retail-sales-data@1`

Native metric: `RetailSalesMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3151 bytes)
- `data/sample_submission.csv` (1122822 bytes); columns: ["Transaction_ID", "Sales_Amount"]
- `data/test.csv` (2588906 bytes); columns: ["Transaction_ID", "Product_Category", "Discount", "Sales_Region", "Date_of_Sale", "Customer_Age", "Customer_Gender", "Sales_Representative"]
- `data/train.csv` (6968873 bytes); columns: ["Transaction_ID", "Product_Category", "Discount", "Sales_Region", "Date_of_Sale", "Customer_Age", "Customer_Gender", "Sales_Representative", "Sales_Amount"]

## Public description

Retail Sales Amount Prediction Challenge

Problem statement
- Build a machine learning model that predicts the monetary Sales_Amount for a retail transaction given its context (category, discount, timing, region, demographics, and sales representative).
- The goal is to minimize prediction error on out-of-time data, reflecting real-world generalization.

Data description
- You will receive two CSVs:
  - train.csv: transactions with features and Sales_Amount labels.
  - test.csv: transactions with features only (labels withheld).
- Each row represents one transaction. Columns
  - Transaction_ID: unique identifier for a transaction (for row alignment in submissions; do not use as a predictive feature).
  - Product_Category: categorical product segment.
  - Discount: numeric discount applied to the transaction.
  - Sales_Region: categorical region string (high cardinality).
  - Date_of_Sale: transaction date as YYYY-MM-DD (2024).
  - Customer_Age: numeric customer age.
  - Customer_Gender: categorical gender value (including possible "Other" or missing).
  - Sales_Representative: categorical salesperson string (high cardinality).
  - Sales_Amount (train.csv only): numeric target to predict.

Train/test split
- Time-based split for realistic generalization:
  - train.csv contains labeled transactions dated January–June 2024.
  - test.csv contains unlabeled transactions dated July–September 2024.
- This split creates temporal shift and exposure to new patterns while keeping feature spaces consistent.

Submission format
- Submit a CSV named as you prefer with exactly two columns in this exact order:
  - Transaction_ID
  - Sales_Amount
- Include one row per transaction in test.csv. Transaction_ID values must match those in test.csv and appear exactly once.

Evaluation metric
- Root Mean Squared Error (RMSE) on Sales_Amount.
- RMSE is defined as sqrt(mean((y_true - y_pred)^2)). It penalizes larger errors more, aligns with monetary risk, and is stable for the value ranges in this dataset.

Modeling guidance
- Recommended preprocessing and feature engineering:
  - Parse Date_of_Sale into month, day-of-week, and week-of-year; consider cyclical encodings.
  - Handle high-cardinality categoricals (Sales_Region and Sales_Representative) via target/frequency encoding, hashing, or learned embeddings. Include an explicit Unknown bucket for rare/missing tokens.
  - One-hot or target/frequency encode Product_Category.
  - Treat Customer_Gender as categorical with an Unknown category for missing values.
  - Normalize or scale Discount; explore interaction features (e.g., category × discount, seasonality × category).
- Effective models include gradient-boosted trees, tabular neural networks with embeddings, and regularized linear models with rich feature engineering.

Files provided
- train.csv: features + Sales_Amount labels.
- test.csv: features only.
- sample_submission.csv: valid example submission file with random but plausible predictions.

Notes
- Do not leak label information; test.csv does not include Sales_Amount.
- Transaction_ID is for row alignment only and should not be used to memorize labels.
