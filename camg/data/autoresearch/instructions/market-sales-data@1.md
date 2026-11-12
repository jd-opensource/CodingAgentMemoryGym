# OpenMLE-fast task

Task ID: `market-sales-data@1`

Native metric: `SupermarketProductLineMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2972 bytes)
- `data/sample_submission.csv` (24787 bytes); columns: ["row_id", "Electronic accessories", "Fashion accessories", "Food and beverages", "Health and beauty", "Home and lifestyle", "Sports and travel"]
- `data/test.csv` (7154 bytes); columns: ["row_id", "Gender", "Branch", "City", "Customer type", "Unit price", "Quantity"]
- `data/train.csv` (44172 bytes); columns: ["row_id", "Gender", "Branch", "City", "Customer type", "Unit price", "Quantity", "Product line"]

## Public description

Supermarket Product Line Identification (Multiclass Classification)

Problem statement
Retailers often need to infer what category of goods a transaction belongs to using limited contextual data (store, customer type, pricing, basket size). Your task is to predict the product line (one of 6 categories) for each checkout transaction based on tabular attributes.

Goal
Build a model that outputs well-calibrated probabilities over the 6 product lines for each transaction in the test set.

Data description
You are given transaction-level tabular data. The final files are:
- train.csv — contains features and the target label (Product line) for model training.
- test.csv — contains the same features without the target label.
- sample_submission.csv — shows the required submission format.

Columns in train.csv and test.csv
- row_id: Unique identifier for each row (do not treat as a predictive feature; used only to align submissions).
- Gender: Categorical (Male/Female)
- Branch: Categorical (A/B/C)
- City: Categorical (Yangon/Mandalay/Naypyitaw)
- Customer type: Categorical (Member/Normal)
- Unit price: Numeric (float)
- Quantity: Numeric (integer)
- Product line: Target label (only in train.csv). One of 6 classes:
  - Electronic accessories
  - Fashion accessories
  - Food and beverages
  - Health and beauty
  - Home and lifestyle
  - Sports and travel

Notes
- The following raw columns are intentionally excluded from train/test features:
  - Invoice ID (row identifier; not predictive)
  - Tax 5% (inconsistent magnitude across rows; a near-deterministic function of Unit price×Quantity with noisy scaling)
- Basic cleaning has been applied (whitespace/casing normalization for string fields). No missing values are expected.

Submission format
- File: CSV with the following columns:
  - row_id
  - Electronic accessories, Fashion accessories, Food and beverages, Health and beauty, Home and lifestyle, Sports and travel
- Each row corresponds to one row_id in test.csv.
- The 6 class columns must be probabilities (non-negative, finite) and each row must sum to 1.

Evaluation
- Primary metric: Multiclass log loss (cross-entropy) averaged over all test rows. For each test row i with true class c_i and submitted probability p_i,c_i, the score is:
  LogLoss = -(1/N) * Σ_i log(max(min(p_i,c_i, 1 - 1e-15), 1e-15))
Lower is better. This metric rewards well-calibrated probabilistic predictions and treats all classes symmetrically.

Recommended approach (not required)
- Encode categorical variables (e.g., one-hot or target encoding) for Gender, Branch, City, Customer type.
- Consider interaction features (e.g., Branch×Customer type) and regularization to avoid overfitting on this small dataset.
- Calibrate predicted probabilities if your base model is not well-calibrated.

Files provided
- train.csv
- test.csv
- sample_submission.csv

Good luck and have fun building robust probabilistic classifiers for retail product line prediction!
