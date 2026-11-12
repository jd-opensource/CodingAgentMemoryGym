# OpenMLE-fast task

Task ID: `amazon-kindle-books-dataset-2023-130k-books@1`

Native metric: `KindleReviewsPredictionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2642 bytes)
- `data/sample_submission.csv` (373160 bytes); columns: ["asin", "reviews"]
- `data/test.csv` (7423477 bytes); columns: ["asin", "title", "author", "soldBy", "imgUrl", "productURL", "stars", "price", "isKindleUnlimited", "category_id", "isBestSeller", "isEditorsPick", "isGoodReadsChoice", "publishedDate", "category_name"]
- `data/train.csv` (30005438 bytes); columns: ["asin", "title", "author", "soldBy", "imgUrl", "productURL", "stars", "reviews", "price", "isKindleUnlimited", "category_id", "isBestSeller", "isEditorsPick", "isGoodReadsChoice", "publishedDate", "category_name"]

## Public description

Title: Kindle Popularity Prediction (RMSLE)

Problem statement:
- Predict the number of Amazon reviews for a Kindle e-book using its metadata. Each row represents one book with rich tabular and textual attributes (title, author, publisher, price, category, badges, star rating, publication date, etc.). The target is heavily skewed, requiring careful modeling and evaluation.

Files provided:
- train.csv: Book-level metadata including the target column reviews.
- test.csv: Same columns as train.csv except reviews is withheld.
- sample_submission.csv: Example of a valid submission format.

Target and features:
- Target: reviews (non-negative integer count at the October 2023 snapshot).
- Features available include: asin (row identifier), title, author, soldBy (publisher), stars, price, isKindleUnlimited, category_id, isBestSeller, isEditorsPick, isGoodReadsChoice, publishedDate, category_name, imgUrl, productURL. You may ignore URL fields; external fetching is not needed.
- Notes:
  - asin is a stable ID to align predictions with test rows; do not treat it as predictive content.
  - Stars can be missing; consider missingness indicators and careful imputation.
  - Publication date may be absent for many entries; deriving age since publication relative to the 2023 snapshot can be helpful.

Evaluation metric:
- Root Mean Squared Logarithmic Error (RMSLE) on reviews.
- For each book i with true count y_i and prediction p_i, both clipped to be non-negative:
  RMSLE = sqrt( mean_i( (log(1 + y_i) − log(1 + p_i))^2 ) ).
- Predictions may be any non-negative real numbers (integers not required). RMSLE is well-suited to heavy-tailed count data and emphasizes relative accuracy.

Expected approaches:
- Data processing: type coercion (booleans, floats, dates), handling missing values, deduplication on asin.
- Feature engineering: text features from title (e.g., TF-IDF or compact embeddings), categorical encodings (author, soldBy, category_name), interaction terms (e.g., price × badges), and publication recency.
- Modeling: regularized linear models, gradient boosting/ensembles, or transformer-based NLP for titles.
- Evaluation: use robust CV on train.csv and final scoring on test.csv with RMSLE.

Submission format:
- A CSV with exactly two columns and this header:
  asin,reviews
- Include each asin from test.csv exactly once. The reviews column should contain non-negative numeric predictions.

Final files:
- train.csv
- test.csv
- sample_submission.csv

Build a model that leverages both tabular and text features, robust preprocessing, and appropriate optimization for skewed targets to achieve the best RMSLE.
