# OpenMLE-fast task

Task ID: `google-play-music-app-reviews@1`

Native metric: `GooglePlayReviewQWKMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3687 bytes)
- `data/sample_submission.csv` (89783 bytes); columns: ["review_id", "rating"]
- `data/test.csv` (1819541 bytes); columns: ["review_id", "app", "review", "version", "date"]
- `data/train.csv` (9773024 bytes); columns: ["review_id", "app", "review", "version", "date", "rating"]

## Public description

Title: Ordinal Star Rating Prediction from Google Play Music App Reviews

Problem statement
Build a model that predicts the 1–5 star rating of a Google Play user review for popular music apps. Each example contains noisy, informal review text plus light metadata (app name, app version, review date). Your task is to map these signals to an accurate ordinal rating.

Why this is challenging
- Reviews are informal and multilingual, with slang, emojis, sarcasm, and typos.
- Ratings are ordinal (distance between 1 and 5 matters) and class distribution is imbalanced.
- Evaluation is time-aware: the test set consists of later reviews than the training set within each app, introducing natural distribution shift.

Files provided
- train.csv: Labeled training data with columns [review_id, app, review, version, date, rating].
- test.csv: Unlabeled test data with columns [review_id, app, review, version, date].
- sample_submission.csv: Template submission with columns [review_id, rating]. Replace rating with your predictions.

Task
- Use train.csv to train your model.
- Predict integer ratings in {1, 2, 3, 4, 5} for every row in test.csv.
- Submit a CSV with columns [review_id, rating], including all and only the review_id values from test.csv.

Data description
- app: Categorical app name (e.g., Spotify, Apple Music, SoundCloud, TIDAL, Deezer, Shazam, Google Play Music).
- review: Raw free-text review content (preserve punctuation/emojis; language may vary, primarily English).
- version: App version string (may be missing; formats vary). You may parse into components (major/minor/patch/build) or treat as categorical.
- date: Timestamp string of the review. You may derive time features such as year, month, day-of-week, and time since epoch.
- rating (train only): Ordinal target in {1,2,3,4,5}.

Split and construction details
- Single train/test split, time-aware within each app: train contains earlier reviews; test contains later reviews. A small number of identical review texts may exist in the data; they are assigned so that identical app+review strings do not cross splits.
- All label classes that appear in test also appear at least once in train.
- Deterministic split: your local runs will match the public data split.

Evaluation metric
- Primary metric: Quadratic Weighted Kappa (QWK) on the 1–5 ordinal ratings.
- QWK measures agreement between predictions and ground truth with heavier penalties for larger disagreements and adjusts for expected agreement due to label frequencies.
- Implementation details: Ratings are treated as integers 1–5. The QWK is computed as 1 - (sum_ij w_ij O_ij) / (sum_ij w_ij E_ij), where O is the observed confusion matrix, E is the expected matrix from the product of label histograms, and w_ij = ((i-j)^2) / ((K-1)^2) with K=5.

Starter ideas (optional)
- Text features: character/word n-grams; transformer encodings (e.g., multilingual BERT); sentiment/emoji features; punctuation/length statistics.
- Metadata: app identity; parsed version fields; date-derived features; language ID.
- Models: linear classifiers with ordinal calibration; gradient boosted trees on engineered features; pretrained transformers fine-tuned for ordinal classification.
- Post-processing: ordinal calibration (thresholding over latent regression), class-weighting or focal loss, ensembling.

Submission format
- CSV with columns [review_id, rating].
- review_id must match those in test.csv exactly and be unique.
- rating must be integers in {1,2,3,4,5}. Non-integer or out-of-range values will be rejected.

Good luck! Design a robust model that generalizes across apps and over time while respecting the ordinal nature of ratings.
