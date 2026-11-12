# OpenMLE-fast task

Task ID: `amazon-books-reviews@1`

Native metric: `AmazonBookRatingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/books_metadata.csv` (916666 bytes); columns: ["book_title", "title_norm", "description", "authors", "publisher", "publishedDate", "categories", "ratingsCount"]
- `data/description.txt` (3203 bytes)
- `data/sample_submission.csv` (20839 bytes); columns: ["review_id", "rating"]
- `data/test.csv` (1108622 bytes); columns: ["review_id", "book_title", "user_id", "review_time", "review_summary", "review_text", "helpful_votes", "helpful_total", "price"]
- `data/train.csv` (18125145 bytes); columns: ["review_id", "book_title", "user_id", "review_time", "review_summary", "review_text", "helpful_votes", "helpful_total", "price", "rating"]

## Public description

Title: Amazon Book Review Rating Prediction

Problem statement:
Predict the star rating (continuous 1.0–5.0) that a user assigns to a book review using the review text and available metadata. You are provided with millions of Amazon book reviews and a companion file with book-level information. Your task is to build a model that accurately estimates review ratings for unseen reviews.

Files provided:
- train.csv: Labeled training set with features and the target rating.
- test.csv: Unlabeled test set with the same features as train.csv (without the target).
- sample_submission.csv: Example submission file with the correct format.
- books_metadata.csv: Book-level metadata to optionally join to train/test by book_title or normalized title (title_norm).

Columns:
- Common feature columns in train.csv and test.csv:
  - review_id: Unique identifier for each review row.
  - book_title: Title of the book reviewed.
  - user_id: Anonymized reviewer identifier.
  - review_time: Unix epoch timestamp (seconds) when the review was posted.
  - review_summary: Short summary/title of the review.
  - review_text: Full text of the review.
  - helpful_votes: Number of “helpful” votes for the review.
  - helpful_total: Total “helpful” votes cast on the review (denominator).
  - price: The price field as provided in the source (may be empty or non-numeric).
- Target column in train.csv only:
  - rating: The star rating assigned to the review, a real value in [1.0, 5.0].

books_metadata.csv columns:
- book_title, title_norm, description, authors, publisher, publishedDate, categories, ratingsCount
This file can be joined to train/test on book_title (or title_norm for a more robust match). No external scraping is required.

Evaluation:
- Metric: Root Mean Squared Error (RMSE) between your predictions and the true ratings on the hidden test labels.
- Submission format: A CSV with exactly two columns and a header: review_id,rating
  - review_id must match the IDs in test.csv.
  - rating should be a numeric prediction; values outside [1.0, 5.0] will be clipped to that range for scoring.

Train/Test split details:
- A single chronological split is used: earlier reviews form the training set and later reviews form the test set. This simulates predicting future reviews from past data and discourages leakage.

Modeling notes and recommendations:
- Text modeling of review_summary and review_text is expected to be the most informative signal; consider TF-IDF + linear models, modern transformers, and/or sentiment-oriented features.
- Leverage review_time to model temporal drift and user/book effects.
- Join book-level context from books_metadata.csv (e.g., description, authors, categories, publisher, publishedDate) to improve predictions.
- Handle missing and noisy fields robustly (e.g., price, helpfulness).
- Ensure careful evaluation, regularization, and numerical stability.

Submission example:
- sample_submission.csv shows the required format and data types.

Rules of the game:
- Do not attempt to infer or reconstruct test labels.
- Keep the submission schema exact: review_id,rating.

Good luck and have fun building robust text+tabular models for rating prediction!
