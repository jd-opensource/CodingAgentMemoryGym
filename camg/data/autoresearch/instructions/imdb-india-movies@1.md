# OpenMLE-fast task

Task ID: `imdb-india-movies@1`

Native metric: `ImdbIndiaRatingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2889 bytes)
- `data/sample_submission.csv` (47808 bytes); columns: ["Id", "Rating"]
- `data/test.csv` (170032 bytes); columns: ["Id", "Name", "Year", "Duration", "Genre", "Director", "Actor 1", "Actor 2", "Actor 3"]
- `data/train.csv` (705976 bytes); columns: ["Id", "Name", "Year", "Duration", "Genre", "Director", "Actor 1", "Actor 2", "Actor 3", "Rating"]

## Public description

Title: Predict IMDb Ratings of Indian Movies from Metadata

Problem statement
Build a model to predict the IMDb user rating (continuous target typically in [1, 10]) for Indian movies using only metadata available near release: title, year, duration, genre(s), director, and top-billed cast. The task is a tabular regression problem with high-cardinality categorical variables, multi-genre entries, and temporal drift spanning more than a century.

Final competition files
- train.csv: Labeled training data. Columns: Id, Name, Year, Duration, Genre, Director, Actor 1, Actor 2, Actor 3, Rating.
- test.csv: Unlabeled test data. Columns: Id, Name, Year, Duration, Genre, Director, Actor 1, Actor 2, Actor 3.
- sample_submission.csv: Example submission format with random valid predictions. Columns: Id, Rating.

Important notes
- Id is a synthetic anonymized identifier with no semantic relation to the movie; use Id only to align rows across files and in your submission.
- Votes are excluded to avoid label leakage, as popularity co-evolves with rating post-release.
- Fields are messy by design (e.g., Year like "(2019)", Duration like "102 min", Genre as comma-separated lists, names with varied casing). Robust preprocessing and feature engineering are expected.
- Only rows with valid ratings are used for train/test. Rows without ratings are not part of the evaluation.

Submission format
- A single CSV file with two columns: Id and Rating.
- Id values must exactly match and be in the same order as the Ids in test.csv; no duplicates or missing rows.
- Rating must be numeric. Values outside [1, 10] are permitted but will be clipped to [1, 10] for scoring to ensure numerical stability.

Evaluation metric
- Root Mean Squared Error (RMSE) between your predictions and the true ratings for the test set.
- RMSE is fair and precise for bounded continuous labels, penalizing larger errors and encouraging well-calibrated predictions across the rating scale.

Train/test split policy
- A single deterministic split that preserves distribution across decades and rating bins to mitigate temporal drift and label distribution imbalance. Test labels are withheld and correspond exactly to the Ids in test.csv.

Modeling guidance
- Handle multi-genre strings (e.g., multi-hot encoding), missing values (e.g., duration), and high-cardinality director/actor names (e.g., frequency or CV-based target encoders applied on training folds only).
- Consider time signals (year/decade) and interactions with genres and cast.
- Optional lightweight text features from titles (e.g., n-grams or hashing) can add signal.
- Avoid leakage from the target or post-release dynamics (e.g., do not use votes or derive features from ratings).

Goal
Deliver a robust, generalizable predictor that minimizes RMSE and demonstrates strong preprocessing and feature engineering on messy, real-world tabular data.
