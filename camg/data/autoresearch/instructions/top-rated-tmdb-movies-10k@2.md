# OpenMLE-fast task

Task ID: `top-rated-tmdb-movies-10k@2`

Native metric: `TmdbRatingRegressionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2690 bytes)
- `data/sample_submission.csv` (48193 bytes); columns: ["id", "vote_average"]
- `data/test.csv` (706878 bytes); columns: ["id", "title", "genre", "original_language", "overview", "popularity", "release_date", "vote_count"]
- `data/train.csv` (2790618 bytes); columns: ["id", "title", "genre", "original_language", "overview", "popularity", "release_date", "vote_average", "vote_count"]

## Public description

TMDB Movie Ratings: Predict vote_average from Plot Overviews and Metadata

Problem statement
Given a movie’s plot overview and basic metadata, predict its TMDB user rating (vote_average) on a 0–10 scale. You are provided a training set with labels and a test set without labels. For each test movie, submit a single numeric prediction of vote_average.

Files
- train.csv: Training data with the target column vote_average.
- test.csv: Test data without the target column. Use this file to generate predictions.
- sample_submission.csv: Example submission file with the required format and plausible placeholder predictions.

Data description
Each row represents a single movie. Columns include:
- id: TMDB movie ID (unique identifier for merging and submission).
- title: Movie title text.
- genre: Comma-separated list of genres.
- original_language: ISO 639-1 original language code.
- overview: Movie plot overview (free text).
- popularity: Popularity signal within TMDB at the time of snapshot (optional feature; may correlate weakly with ratings).
- release_date: Release date (YYYY-MM-DD). You may derive year/decade features.
- vote_count: Number of votes cast by users.
- vote_average: Target variable in train.csv only (0–10 float).

Task guidance (non-binding)
Participants are encouraged to explore NLP feature extraction from overview (e.g., TF–IDF, pretrained transformers), fuse with tabular features (language, genres, release year/decade, log1p(vote_count), etc.), and train a regression model (e.g., regularized linear models, gradient boosting, or neural networks). Robust preprocessing, careful target scaling, and outlier handling can improve performance.

Evaluation
Submissions are evaluated using Root Mean Squared Error (RMSE) between your predictions and the ground-truth vote_average on the test set:
RMSE = sqrt(mean((y_pred - y_true)^2)).
Predictions are clipped to [0, 10] before scoring. Lower is better. Predictions should be numeric and will be matched to ground truth by id.

Submission format
Submit a CSV file with exactly the following two columns:
- id
- vote_average
The file should contain one row per test id. The order of rows does not matter, but ids must be unique and match those in test.csv.

Notes
- This is a text–tabular fusion regression task with rich signal in overview plus informative metadata.
- Consider feature engineering: tokenization/TF–IDF or transformer embeddings, language one-hot, multi-hot genres, release year/decade, and log1p(vote_count). You may also try ensembling.
- Please ensure all preprocessing and modeling steps are reproducible.
- The supplied sample_submission.csv conforms to the expected format.
