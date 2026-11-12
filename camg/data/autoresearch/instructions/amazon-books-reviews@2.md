# OpenMLE-fast task

Task ID: `amazon-books-reviews@2`

Native metric: `AmazonBooksHelpfulnessMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2884 bytes)
- `data/sample_submission.csv` (23646 bytes); columns: ["review_id", "helpfulness_ratio"]
- `data/test.csv` (4310556 bytes); columns: ["review_id", "book_id", "title", "user_id", "review_time", "review_score", "review_summary", "review_text", "price", "book_description", "authors", "categories", "publisher", "published_year"]
- `data/train.csv` (17256851 bytes); columns: ["review_id", "book_id", "title", "user_id", "review_time", "review_score", "review_summary", "review_text", "price", "book_description", "authors", "categories", "publisher", "published_year", "helpfulness_ratio"]

## Public description

Amazon Books Review Helpfulness Prediction

Problem statement
Participants are asked to predict the helpfulness ratio r in [0, 1] of an Amazon book review using the review text, its metadata, and per-book information. Each review has community feedback votes: X helpful votes out of Y total votes; the target is r = X / Y for reviews with Y > 0.

Files provided
- train.csv: Training data with features and the target helpfulness_ratio for each review.
- test.csv: Test data with the same features but without the target.
- sample_submission.csv: A sample submission file with the required format.

Prediction target
- helpfulness_ratio: The ratio X/Y derived from review/helpfulness for reviews with at least one vote (Y > 0). Present only in train.csv.

Key columns
- review_id: Unique identifier for each review row (use this to align predictions in the submission).
- book_id: Book identifier (original Id field).
- title: Book title.
- user_id: Reviewer identifier.
- review_time: Review time as a Unix timestamp (UTC seconds since epoch).
- review_score: The star rating (float in [0, 5]).
- review_summary: Short summary text of the review.
- review_text: Full review text.
- price: Price of the book if available (float; may be missing).
- book_description: Book description from book metadata.
- authors: Authors list as a string.
- categories: Book categories/genres as a string.
- publisher: Publisher.
- published_year: Year extracted from the book metadata when available.

Train/test split protocol
- Only reviews with at least one total vote (Y > 0) are included.
- The split is chronological to simulate future prediction: approximately the earliest 80% (by review_time) are in train.csv and the later 20% are in test.csv. If a review_time equals the cut-off, it is assigned to test.

Submission format
- A CSV with two columns and a header:
  - review_id: The review identifier from test.csv
  - helpfulness_ratio: Your predicted helpfulness ratio in [0, 1]

Evaluation
- Weighted Mean Absolute Error (WMAE): samples are weighted by their total vote count Y.
- Definition: Score = sum_i w_i * |r_i - rhat_i| / sum_i w_i, where r_i is the true ratio, rhat_i is your prediction clipped to [0, 1], and w_i = Y_i are the total votes for review i.
- Why this metric: Ratios with more votes are more reliable and more important in practice. MAE is bounded and robust in [0,1], and vote-weighting aligns evaluation with label certainty.

Notes
- The train/test files include text and tabular signals. Strong solutions typically combine text encoders (e.g., TF-IDF, pretrained transformers) with tabular features (time, rating, price, metadata) and appropriate sample weighting.
- The test file does not include the original helpfulness votes to prevent leakage. Use review_id to align predictions.
- All files are UTF-8 CSV with headers. No paths are included in the files.
