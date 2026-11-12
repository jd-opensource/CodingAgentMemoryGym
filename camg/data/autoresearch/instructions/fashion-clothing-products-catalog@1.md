# OpenMLE-fast task

Task ID: `fashion-clothing-products-catalog@1`

Native metric: `FashionPricePredictionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3296 bytes)
- `data/sample_submission.csv` (66226 bytes); columns: ["ProductID", "Price (INR)"]
- `data/test.csv` (589673 bytes); columns: ["ProductID", "ProductName", "ProductBrand", "Gender", "NumImages", "Description"]
- `data/train.csv` (2482944 bytes); columns: ["ProductID", "ProductName", "ProductBrand", "Gender", "NumImages", "Description", "Price (INR)"]

## Public description

Fashion Price Prediction from Catalog Text + Metadata

Problem statement
Predict the listed product price (INR) for fashion e-commerce items using their catalog metadata and text. Each row represents a product with its name, description, brand, gender segment, and other attributes. Your task is to learn a model that generalizes across brands and diverse product types by leveraging both textual descriptions and tabular signals.

Why it’s interesting
Price estimation from catalog data is an important merchandising and auditing task. It requires modeling nuanced brand effects, product families (e.g., apparel, luggage, fragrances, home decor), and rich domain-specific vocabulary present in the text.

Files provided
- train.csv: Training data with features and the target price.
- test.csv: Test data with features only.
- sample_submission.csv: A sample file showing the required submission format.

Columns
- ProductID: Unique product identifier (string). Use it only as an identifier in submissions and joins.
- ProductName: Product title/name (text). Rich source of category, style, and material cues.
- ProductBrand: Brand name (categorical).
- Gender: Intended segment (categorical) such as Men, Women, Unisex.
- NumImages: Number of product images on the listing (numeric).
- Description: Detailed free-text description (text). Often contains garment type, material, fit, volume/size (e.g., 125 ml), and other attributes.
- Price (INR): Target variable in train.csv only (numeric, strictly positive).

Task and expectations
- Build a regression model to predict Price (INR) for the test set.
- Make good use of text and tabular features. Strong solutions typically:
  - Normalize and tokenize text from ProductName and Description; extract informative n-grams and key phrases (e.g., fabric, fit, product type, volumes like ml/liters, warranty mentions).
  - Encode ProductBrand and Gender effectively (e.g., one-hot, target/impact encoding, embeddings).
  - Consider transformations such as training on log(Price) while evaluating on the INR scale.
  - Handle heavy-tailed price distribution and heterogeneity across product families.

Submission format
- Submit a CSV file with exactly these two columns and header:
  - ProductID
  - Price (INR)
- Include every ProductID from test.csv exactly once. Do not include extra rows. Order does not matter, but IDs must match exactly.

Evaluation
- Metric: Mean Absolute Error (MAE) on Price (INR).
  - MAE = average of absolute differences between your predictions and the ground truth prices, measured in INR.
  - This metric is robust to outliers and directly interpretable as the average rupee error.

Rules and notes
- Use train.csv for model development; test.csv contains the held-out instances used for final scoring.
- ProductID is an identifier only and must be preserved in your submission.
- No external data is required. You may employ common NLP and tabular ML techniques (e.g., TF-IDF + linear models, gradient boosting, or transformer embeddings combined with tree-based or neural models).
- Runtime constraints are not enforced here; focus on solution quality and rigorous validation.

Deliverables
- One CSV submission with predictions for all products in test.csv, following the exact submission format described above.
