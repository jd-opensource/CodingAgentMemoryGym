# OpenMLE-fast task

Task ID: `cartier-jewelry-catalog@1`

Native metric: `CartierCatalogPriceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2091 bytes)
- `data/sample_submission.csv` (3841 bytes); columns: ["ref", "price"]
- `data/test.csv` (25066 bytes); columns: ["ref", "categorie", "title", "tags", "description"]
- `data/train.csv` (102275 bytes); columns: ["ref", "categorie", "title", "tags", "description", "price"]

## Public description

Title: Cartier Catalog Price Prediction

Objective
Predict the retail price of Cartier jewelry pieces using their catalog descriptors. Each row describes a single product with category, title, tags, and free-text description. The task is a regression problem.

What you are given
- train.csv: Product catalog rows with columns [ref, categorie, title, tags, description, price].
- test.csv: Same columns as train.csv except without price.
- sample_submission.csv: Example submission format with columns [ref, price].

Key modeling signals
- categorie: rings, bracelets, necklaces, earrings.
- title: short product name (often shared among variants).
- tags and description: free text containing metals (white/yellow/pink gold, platinum), karat (e.g., 18K, 950), gemstone types and counts, approximate sizes.
- ref: product reference identifier (string) that may reflect family codes; used as the submission key.

Official split protocol
- All products sharing the same title are placed entirely in either train or test (grouped by title) to prevent leakage across near-duplicate variants.
- The split preserves the category distribution as much as possible.

Evaluation
- Submissions must be a CSV with columns [ref, price].
- The score is RMSLE (root mean squared logarithmic error) between your predictions and the hidden ground truth prices:
  RMSLE = sqrt(mean((log1p(y_pred) - log1p(y_true))^2))
- Predictions should be nonnegative real numbers. Extremely large/small values are evaluated in log space.

Notes
- Prices span several orders of magnitude and are positively skewed; RMSLE evaluates relative error and is robust to outliers.
- You are encouraged to combine text features (e.g., TF-IDF or language model embeddings) with engineered signals (materials, karat, gemstone presence/count, sizes) and tabular modeling.
- All columns provided in train.csv/test.csv may be used; only price is held out in test.csv.

Submission format
- CSV with exactly two columns: [ref, price].
- ref values must match those in test.csv exactly, appear once, and reflect one prediction per product.
