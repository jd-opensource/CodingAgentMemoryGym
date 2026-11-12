# OpenMLE-fast task

Task ID: `7k-books-with-metadata@1`

Native metric: `BooksPopularityMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3425 bytes)
- `data/sample_submission.csv` (20332 bytes); columns: ["book_id", "ratings_count"]
- `data/test.csv` (815333 bytes); columns: ["book_id", "isbn13", "isbn10", "title", "subtitle", "authors", "categories", "thumbnail", "description", "published_year", "average_rating", "num_pages"]
- `data/train.csv` (3361312 bytes); columns: ["book_id", "isbn13", "isbn10", "title", "subtitle", "authors", "categories", "thumbnail", "description", "published_year", "average_rating", "num_pages", "ratings_count"]

## Public description

Book Popularity Prediction from Metadata

Problem statement
Publishers, retailers, and libraries must forecast demand for new and backlist titles with little or no sales history. Your task is to predict a book’s popularity, measured by ratings_count, using only the provided metadata (text and tabular fields). You will build models that combine natural-language features from titles and descriptions with structured signals such as author, categories, year, and page count.

Data
You are given a single metadata table derived from public sources. We provide a deterministic train/test split and a submission template.

Files
- train.csv — Training data with features and target.
- test.csv — Test data with features only.
- sample_submission.csv — Example submission with the required columns and valid placeholder predictions.

Columns
Each row represents one book edition. Columns include:
- book_id: Unique identifier used for submission (string or integer). Stable across train/test.
- isbn13, isbn10: Identifiers for the edition. Treat as IDs; not expected to be predictive.
- title, subtitle: Text fields describing the book.
- authors: One or more authors separated by semicolons.
- categories: High-level subject categories as a semicolon- or comma-separated string.
- thumbnail: URL of a cover thumbnail (optional to use; external fetching is not required).
- description: Natural-language description or synopsis.
- published_year: Year of publication (integer).
- average_rating: Mean user rating in [0, 5].
- num_pages: Number of pages (integer).
- ratings_count: Target variable (non-negative integer) present only in train.csv. Do not expect this column in test.csv.

Target
- ratings_count (train only): The number of ratings a title has received.

Submission format
- A CSV file with exactly two columns and the same number of rows as test.csv:
  - book_id: Must match the IDs in test.csv (any order is acceptable; duplicates are not allowed).
  - ratings_count: Your predicted popularity (non-negative real number). Predict on the original scale; the evaluation will apply a log1p transform internally.

Evaluation
- Metric: Root Mean Squared Error (RMSE) on log1p(ratings_count).
  - Let y be the true ratings_count and p be your prediction. We compute:
    RMSE = sqrt(mean((log1p(y) - log1p(p))^2)).
  - Predictions must be finite numbers and >= 0. The metric is scale-robust and appropriately penalizes errors, especially for highly popular books.

Notes and guidance
- The distribution of ratings_count is extremely long-tailed. Modeling log1p(ratings_count) is recommended during training.
- Useful features include TF-IDF or embeddings over description/title, categorical encodings for authors/categories, and numeric signals such as published_year, average_rating, and num_pages.
- Identifiers (isbn13/isbn10) are provided for completeness. They should be treated as IDs rather than semantic features.
- External data is not required. You may ignore thumbnail URLs.

Baseline ideas
- Text-only baseline: TF-IDF over description + linear regression.
- Text + tabular: Gradient boosting over TF-IDF aggregates plus engineered numeric/categorical features.

Reproducibility
- The provided split is stratified over binned log1p(ratings_count) to stabilize the long tail and ensure a representative test set.

Good luck, and have fun blending NLP and tabular modeling to forecast book popularity!
