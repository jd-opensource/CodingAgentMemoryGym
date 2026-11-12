# OpenMLE-fast task

Task ID: `nykaa-popular-brands-cosmetics-beauty-products@1`

Native metric: `NykaaPopularityMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2692 bytes)
- `data/sample_submission.csv` (18518 bytes); columns: ["product_id", "y_pred_log"]
- `data/test.csv` (95700 bytes); columns: ["product_id", "brand_name", "product_title", "mrp", "price", "discount_pct", "listing_page_name"]
- `data/train.csv` (392537 bytes); columns: ["product_id", "brand_name", "product_title", "mrp", "price", "discount_pct", "listing_page_name", "rating_count"]

## Public description

Competition: Predict Product Popularity on Nykaa (Rating Count Regression)

Problem statement
- Predict a product’s popularity (the number of ratings) from its metadata on Nykaa. You are given product attributes such as brand, title, and pricing. Your task is to build an ML model that estimates popularity for unseen products in the test set.

Data description
- train.csv: Tabular file with the following columns (one row per product):
  - product_id: string identifier
  - brand_name: categorical
  - product_title: text
  - mrp: numeric (maximum retail price)
  - price: numeric (current selling price)
  - discount_pct: numeric in [0, 1], derived as (mrp - price) / mrp
  - listing_page_name: categorical (brand/category page section)
  - rating_count: target label (integer count of ratings)
- test.csv: Same columns as train.csv except rating_count is withheld. Columns:
  - product_id, brand_name, product_title, mrp, price, discount_pct, listing_page_name
- sample_submission.csv: Example submission showing the required schema.

What is excluded (and why)
- Features that can leak the target or are not self-contained are excluded from train/test: image_url, product_url, listing_url, in_stock, tags, rating, listing_page_no.

Submission format
- Submit a CSV with exactly two columns:
  - product_id
  - y_pred_log: your prediction of log1p(rating_count) for each product in test.csv
- The product_id set must match test.csv exactly (same IDs, any order). Duplicates are not allowed. Predictions must be finite numeric values.

Evaluation metric
- Primary: RMSE on log1p(rating_count). Lower is better.
  score = sqrt(mean((y_pred_log - log1p(y_true))^2))
- Rationale: Rating counts are highly skewed. Evaluating in log space provides a fair, precise comparison across low- and high-popularity products and rewards calibrated, robust models.

Train/test split
- The split is 80/20 with stratification by brand_name where possible. All brands present in the test set also appear in the training set to avoid brand-only leakage.

Modeling guidance
- Consider combining tabular features (price, discount, brand, listing_page_name) with text features from product_title (e.g., n-grams, embeddings). Price vs MRP vs discount interactions and title cues (variant, size, bundle vs single) are often predictive. Modeling log1p(rating_count) as the target during training is recommended, with direct prediction of y_pred_log at inference.

Files provided
- train.csv, test.csv, sample_submission.csv

Notes
- The dataset is self-contained; external fetching (e.g., using image_url/product_url) is not intended.
- Ensure reproducibility and robust handling of skew and numeric edge cases.
