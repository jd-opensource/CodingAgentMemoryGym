# OpenMLE-fast task

Task ID: `movie-dataset-10k@2`

Native metric: `MovieYearPredictionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2538 bytes)
- `data/sample_submission.csv` (20636 bytes); columns: ["id", "Year"]
- `data/test.csv` (632074 bytes); columns: ["id", "Genres", "Description"]
- `data/train.csv` (2589219 bytes); columns: ["id", "Genres", "Description", "Year"]

## Public description

Movie Release Year Prediction from Synopsis + Genres

Problem statement
Predict the release year of a movie using only its synopsis (Description) and multi-label Genres. The official training data includes the target Year; the test data withholds the Year and participants must submit predicted years for each test id.

Why this is interesting
Inferring production era from content signals supports archive organization, search, and cold-start recommendation. Titles often leak the year (e.g., explicit numbers), so they are excluded to preserve the challenge.

Files provided
- train.csv: id, Genres, Description, Year
- test.csv: id, Genres, Description
- sample_submission.csv: id, Year (example predictions)

Target
- Year: Integer release year. The data spans roughly the 1890s to the 2020s.

Inputs
- Genres: Comma-separated list of genres (multiple labels per movie). There are a few dozen distinct tags.
- Description: Short editorial-style overview of the movie. Missing descriptions are represented by empty strings.

Important constraints
- Title is intentionally excluded from the files to avoid leakage. Do not attempt to reconstruct or use it.
- External data is not required. Strong baselines can be built with TF-IDF features from Description combined with one-hot encoded Genres.
- Expect some movies with empty Description; robust handling is part of the challenge.

Evaluation
- Metric: Mean Absolute Error (MAE) on Year.
  - MAE = mean(|y_true − y_pred|), expressed in years.
  - Predictions may be integer or real-valued; absolute error is computed directly.

Official split protocol
- A single official split is provided.
- The split is stratified by decade buckets to stabilize the temporal distribution across train and test.
- Extremely rare decades (with fewer than two samples) are kept in train only to ensure valid stratification and to avoid degenerate test bins. All decades appearing in test also appear in train.

Modeling tips (informal)
- Text features: TF-IDF over word- and/or character n-grams; optional normalization and dimensionality reduction.
- Genre features: One-hot or embeddings; consider interactions with text signals.
- Models: Regularized linear regression, tree-based regressors, or lightweight neural models. Handle outliers and long-tail years carefully.

Submission format
- CSV with columns in order: id, Year
- id must exactly match those in test.csv (no missing/extra rows, no duplicates).
- Year values must be numeric and finite.

Goal
Minimize MAE on the hidden test labels.
