# OpenMLE-fast task

Task ID: `e-commerce-sales-analysis@1`

Native metric: `ECommerceCategoryMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2689 bytes)
- `data/sample_submission.csv` (2526 bytes); columns: ["product_id", "category"]
- `data/test.csv` (13249 bytes); columns: ["product_id", "price", "review_score", "review_count", "sales_month_1", "sales_month_2", "sales_month_3", "sales_month_4", "sales_month_5", "sales_month_6", "sales_month_7", "sales_month_8", "sales_month_9", "sales_month_10", "sales_month_11", "sales_month_12"]
- `data/train.csv` (59231 bytes); columns: ["product_id", "price", "review_score", "review_count", "sales_month_1", "sales_month_2", "sales_month_3", "sales_month_4", "sales_month_5", "sales_month_6", "sales_month_7", "sales_month_8", "sales_month_9", "sales_month_10", "sales_month_11", "sales_month_12", "category"]

## Public description

Competition: Product Category Prediction from 12-Month Sales Fingerprints

Overview
E-commerce platforms rely on robust product taxonomy to power search, recommendations, and analytics. Many listings are miscategorized or lack reliable categories. However, historical sales patterns and basic listing metadata often reflect latent product traits and seasonality. Your task is to predict the product category from a 12‑month sales fingerprint and metadata.

Problem statement
Given each product’s 12 monthly sales values and listing metadata (price, review score, review count), predict its category among seven classes. This is a multi-class classification problem.

Files
- train.csv: Training data containing product_id, price, review_score, review_count, sales_month_1 … sales_month_12, and the target column category.
- test.csv: Test data with the same schema as train.csv but without the category column.
- sample_submission.csv: Submission template with columns product_id and category.

Target and classes
- Target column: category
- Possible values (7 classes): Books, Clothing, Electronics, Health, Home & Kitchen, Sports, Toys

Notes about features
- The monthly sales columns represent the number of units sold in each of the past 12 months (sales_month_1 … sales_month_12).
- price is the product price, review_score is the average review score (1 to 5), and review_count is the total number of reviews.
- The product_name field present in the source data has been removed from the competition files because it is synthetic and non-informative.
- product_id is a stable identifier only and must not be used to infer labels.

Evaluation
- Metric: Macro F1 score (unweighted mean of per-class F1 scores) computed over the seven classes listed above.
- Submissions must include predictions for every product in test.csv and use one of the allowed class names exactly as shown.

Submission format
- A valid submission is a CSV file with the following columns:
  - product_id: Integer identifier that matches test.csv
  - category: One of {Books, Clothing, Electronics, Health, Home & Kitchen, Sports, Toys}
- Row order does not matter; evaluation will align by product_id.

Recommendations
- Strong solutions typically combine careful feature engineering on the 12-month sales fingerprint (e.g., seasonal shares, peak month, quarterly sums, coefficient of variation, simple trend) with non-linear models (e.g., tree ensembles). Interactions of sales-shape features with price/review features can be helpful.
- Avoid leakage: Do not derive features from the target or use any label-dependent heuristics.

Good luck and have fun building high-performing, robust classifiers!
