# OpenMLE-fast task

Task ID: `products-datasets@2`

Native metric: `PricePredictionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2863 bytes)
- `data/sample_submission.csv` (18134 bytes); columns: ["Product ID", "SellPrice"]
- `data/test.csv` (155790 bytes); columns: ["Product ID", "BrandName", "Product Name", "Brand Desc", "Product Size", "Currency", "Category"]
- `data/train.csv` (504649 bytes); columns: ["Product ID", "BrandName", "Product Name", "Brand Desc", "Product Size", "Currency", "Category", "SellPrice"]

## Public description

Problem: Predict the final consumer-facing SellPrice for each product using only catalog metadata (brand, title, description, size, and category). The MRP and Discount fields are excluded from the competition data to avoid trivial leakage.

Context: Retail teams frequently estimate likely market prices for new or unlisted items using historical catalog attributes. This competition evaluates models that generalize price estimation across brands and categories with noisy short text and structured attributes.

Files provided to participants
- train.csv: Training data with features and the target SellPrice.
- test.csv: Test data with the same features but without SellPrice.
- sample_submission.csv: Example submission file containing Product ID and a placeholder SellPrice.

Columns
- Product ID: Unique identifier for the product (string).
- BrandName: Brand of the product (string).
- Product Name: Product title (string).
- Brand Desc: Short description (string).
- Product Size: Size information as free text (string).
- Currency: Currency code/text (string; constant in this dataset).
- Category: Product category (string).
- SellPrice (train only): Final consumer-facing price to predict (numeric, INR).

Target
- SellPrice (numeric, INR). You should predict this value for each row in test.csv.

Important notes
- The MRP and Discount fields are intentionally removed from train/test to prevent label leakage. Use only the provided columns above.
- Product ID is the key for submissions and has a one-to-one mapping to products.

Evaluation
- Metric: Root Mean Squared Logarithmic Error (RMSLE) on SellPrice.
  - Definition: RMSLE(y_true, y_pred) = sqrt( mean( (log1p(y_true) - log1p(max(y_pred, 0)))^2 ) ).
  - Rationale: Prices are heavy-tailed; RMSLE emphasizes relative errors and reduces the dominance of outliers. Predictions are clipped at zero before scoring to ensure stability.

Submission format
- A single CSV file with exactly these columns and headers:
  - Product ID
  - SellPrice
- Include one row per Product ID present in test.csv. Extra/missing IDs or duplicate IDs will invalidate the submission.

Split policy (already applied in the provided train/test files)
- The split is a brand-holdout: entire brands are held out into test to assess cross-brand generalization.
- All categories present in test are also represented in train.

Suggested approaches
- Data processing: Clean text, normalize casing, and handle size strings.
- Feature engineering: TF-IDF or embeddings from Product Name/Brand Desc; one-hot or target encodings for BrandName and Category; engineered size features (e.g., count of size options).
- Modeling: Linear models over text features, gradient boosting over tabular + text-derived features, or neural models combining both.

Final files for this competition
- train.csv
- test.csv
- sample_submission.csv
