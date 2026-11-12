# OpenMLE-fast task

Task ID: `book-recommendation-dataset@1`

Native metric: `BookRatingPredictionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1976 bytes)
- `data/sample_submission.csv` (697808 bytes); columns: ["User-ID", "ISBN", "Book-Rating"]
- `data/test.csv` (343278 bytes); columns: ["User-ID", "ISBN"]
- `data/test_books.csv` (884358 bytes); columns: ["ISBN", "Book-Title", "Book-Author", "Year-Of-Publication", "Publisher"]
- `data/test_users.csv` (337426 bytes); columns: ["User-ID", "Location", "Age"]
- `data/train.csv` (3567044 bytes); columns: ["User-ID", "ISBN", "Book-Rating"]
- `data/train_books.csv` (7495410 bytes); columns: ["ISBN", "Book-Title", "Book-Author", "Year-Of-Publication", "Publisher"]
- `data/train_users.csv` (1931434 bytes); columns: ["User-ID", "Location", "Age"]

## Public description

Title: Explicit Book Rating Prediction with Side Information

Problem statement:
Predict the explicit rating (1–10) that a user will assign to a book, given historical user–book interactions and optional side information from user demographics and book metadata. This is a regression task designed to encourage hybrid recommender systems that combine collaborative signals with content-based features.

Data provided to participants:
- train.csv: Training interactions with columns [User-ID, ISBN, Book-Rating]. Only explicit ratings (1–10) are included.
- test.csv: Test interactions with columns [User-ID, ISBN]. Ratings for these pairs are held out for evaluation.
- train_users.csv: Demographics for users appearing in train.csv with columns [User-ID, Location, Age].
- test_users.csv: Demographics for users appearing in test.csv with columns [User-ID, Location, Age].
- train_books.csv: Metadata for books appearing in train.csv with columns [ISBN, Book-Title, Book-Author, Year-Of-Publication, Publisher].
- test_books.csv: Metadata for books appearing in test.csv with columns [ISBN, Book-Title, Book-Author, Year-Of-Publication, Publisher].
- sample_submission.csv: Example submission file with columns [User-ID, ISBN, Book-Rating] containing random but valid predictions.

Important notes:
- Only explicit ratings (1–10) are used as labels. Implicit feedback (0) is excluded from both train and test.
- Every user and every book appearing in test also appears at least once in train to avoid cold-start impossibility while keeping the task challenging.

Submission format:
- A single CSV with columns [User-ID, ISBN, Book-Rating], containing one row per pair in test.csv.
- Book-Rating may be non-integer numeric values; it will be evaluated as continuous predictions.

Evaluation metric:
- Root Mean Squared Error (RMSE) between submitted predictions and held-out ground truth ratings on the test set. RMSE is computed over all test pairs; lower is better.
