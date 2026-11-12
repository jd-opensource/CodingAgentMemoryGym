# OpenMLE-fast task

Task ID: `marvel-comic-books@2`

Native metric: `MarvelFreeIssueMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2950 bytes)
- `data/sample_submission.csv` (254336 bytes); columns: ["id", "is_free"]
- `data/test.csv` (3070750 bytes); columns: ["id", "comic_name", "active_years", "issue_title", "publish_date", "issue_description", "penciler", "writer", "cover_artist", "Imprint", "Format", "Rating"]
- `data/train.csv` (9803237 bytes); columns: ["id", "comic_name", "active_years", "issue_title", "publish_date", "issue_description", "penciler", "writer", "cover_artist", "Imprint", "Format", "Rating", "is_free"]

## Public description

Marvel Free vs Paid Issue Classification

Problem statement
Predict whether a Marvel comic issue is offered for free or paid using its metadata and textual fields. Your task is to output P(Free) for each issue.

Data description
Each row corresponds to an individual comic issue with the following columns:
- id: Unique identifier for the issue (string)
- comic_name: Name of the comic series
- active_years: Years during which the series was active
- issue_title: Title of the individual issue
- publish_date: Date when the issue was published
- issue_description: Textual description of the issue
- penciler: Penciler(s) of the issue
- writer: Writer(s) of the issue
- cover_artist: Cover artist(s)
- Imprint: Publishing imprint
- Format: Publishing format (e.g., Comic, Infinite Comic)
- Rating: Age rating
- is_free (train only): Binary ground-truth label, where 1 = Free and 0 = Paid

The label was derived from the original catalog price information and is not present in the competition files. “Price” is intentionally excluded from the provided train/test files to avoid label leakage.

Files provided
- train.csv: Training data with features and the target column is_free
- test.csv: Test data with features only (no target)
- sample_submission.csv: Example submission file with the correct format

Train/test split
- The split is chronological based on publish_date among labeled rows: the earliest 80% of dated issues are assigned to the training set and the latest 20% to the test set. Rows lacking a valid publish_date are assigned to the training set to keep evaluation temporal and prevent leakage.
- The split is deterministic.

Task
- Build a model that predicts P(Free) for issues in test.csv using the provided metadata and text. You may combine tabular, NLP, and time-aware features. Avoid using external data that would reveal the ground truth labels.

Submission format
- A single CSV file with the following columns and no index column:
  - id: Must match exactly the ids in test.csv
  - is_free: A probability in [0, 1] representing P(Free)

Evaluation metric
- The leaderboard is based on binary log loss (cross-entropy):
  logloss = -mean(y*log(p) + (1-y)*log(1-p))
  where p is the submitted probability for the Free class and y is the true label (1 for Free, 0 for Paid). Predictions are clipped to a small epsilon away from 0 and 1 for numerical stability.

Notes and recommendations
- Consider feature engineering from text (issue_title, issue_description) using TF-IDF, n-grams, or pretrained embeddings.
- Extract temporal features from publish_date (year, month, decade) and series-level features from active_years (start/end/age).
- Normalize categorical text (e.g., creator fields split by commas, casing normalization) and count features (e.g., number of creators listed).
- Expect distribution and format shifts over time (e.g., digital freebies vs print prices), making calibration and robustness important.
