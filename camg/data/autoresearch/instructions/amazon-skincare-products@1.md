# OpenMLE-fast task

Task ID: `amazon-skincare-products@1`

Native metric: `SkincarePriceRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3259 bytes)
- `data/sample_submission.csv` (8164 bytes); columns: ["item_id", "Price"]
- `data/test.csv` (59622 bytes); columns: ["item_id", "Title", "Product", "Brand", "Skin_Type", "Number of items", "Sold By"]
- `data/train.csv` (187015 bytes); columns: ["item_id", "Title", "Product", "Brand", "Skin_Type", "Number of items", "Sold By", "Price"]

## Public description

Title: Predict Amazon Skincare Product Prices from Listing Text

Problem statement:
Given listing metadata for skincare and cosmetics products (including title text and categorical attributes), predict the product’s listed price. Listings vary widely by brand, pack size, formulation, skin-type claims, and seller, while titles are noisy and heterogeneous. Your goal is to build models that accurately predict prices using only the provided training data.

Files provided:
- train.csv: Training data with features and the target column Price.
- test.csv: Test data with the same features as train.csv but without the target.
- sample_submission.csv: A sample submission file with the required format.

Columns:
Each row represents a single product listing with a unique identifier.
- item_id: Unique identifier for the listing.
- Title: Free-text listing title (may contain noisy punctuation, spacing, and mixed casing).
- Product: Product type/category (e.g., Moisturizer, Primer, Facial sprays, Hand cream, Nail paint).
- Brand: Brand name (inconsistent casing may occur).
- Skin_Type: Declared suitable skin types. May be a single value (e.g., "Dry") or comma-separated values (e.g., "All, Combination, Sensitive").
- Number of items: Count of items in a pack (integer-like string or number).
- Sold By: Seller name (categorical, sometimes missing).
- Price: Target variable in train.csv only (positive numeric price).

Evaluation metric:
Submissions are evaluated using RMSLE (Root Mean Squared Logarithmic Error) on the Price target:
RMSLE = sqrt(mean((log1p(y_pred) - log1p(y_true))^2)).
- Predictions must be non-negative real numbers. During scoring, values are clipped at 0 to avoid invalid logs.
- RMSLE is robust to right-skewed price distributions and balances relative error across low- and high-price items.

Submission format:
- A CSV file with exactly two columns and a header: item_id,Price
- Include one row per row in test.csv.
- The order of rows does not matter; rows are matched by item_id.

Guidance and baseline ideas:
- Text processing: Clean and normalize Title text (whitespace, unicode, lowercasing), and extract numeric cues such as pack sizes (ml, g, kg, l), counts (pack of N, 2x/3x), SPF, and percentage actives (e.g., 2%, 10%). Consider ingredient keywords (e.g., vitamin C/E, niacinamide, hyaluronic, ceramide, aloe) and form factors (gel, cream, lotion, spray, polish).
- Categorical features: Normalize Brand casing (e.g., LAKMÉ/Lakme), and encode Brand and Sold By with frequency/target encodings. For Skin_Type, map to a canonical set {All, Normal, Dry, Combination, Sensitive, Oily, Acne Prone} and handle multi-valued entries using multi-hot flags.
- Modeling: Combine TF-IDF (or embeddings) from Title with gradient-boosted trees or regularized linear models on engineered features. Address skew by training on log1p(Price).

Important notes:
- Use only the provided data; external scraping or auxiliary sources are not permitted.
- The Link field and constant-Category information are not included in the final files and should not be used.
- The train/test split preserves the distribution of Product types and covers all provided rows.

Best of luck, and have fun building robust text+tabular regression models!
