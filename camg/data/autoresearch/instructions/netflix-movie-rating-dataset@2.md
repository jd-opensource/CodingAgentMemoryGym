# OpenMLE-fast task

Task ID: `netflix-movie-rating-dataset@2`

Native metric: `NetflixRatingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1185 bytes)
- `data/sample_submission.csv` (1733282 bytes); columns: ["User_ID", "Movie_ID", "Rating"]
- `data/test.csv` (3404975 bytes); columns: ["User_ID", "Movie_ID", "Year", "Name"]
- `data/test_movies.csv` (109 bytes); columns: ["Movie_ID", "Year", "Name"]
- `data/train.csv` (3514826 bytes); columns: ["User_ID", "Movie_ID", "Rating"]
- `data/train_movies.csv` (1072 bytes); columns: ["Movie_ID", "Year", "Name"]

## Public description

Title: Netflix Cold-Start Rating Prediction

Background
This challenge focuses on predicting user ratings for completely unseen movies (strict item cold-start).

Files Provided (under public/)
- train.csv: training interactions [User_ID, Movie_ID, Rating].
- train_movies.csv: metadata for training movies [Movie_ID, Year, Name].
- test.csv: test interactions (targets hidden) [User_ID, Movie_ID, Year, Name].
- test_movies.csv: metadata for test movies [Movie_ID, Year, Name].
- sample_submission.csv: example submission [User_ID, Movie_ID, Rating].

Split Strategy
- Approximately 10% of movies are held out as test movies with a fixed seed for determinism.
- Train set contains all interactions for the remaining movies.
- Test set contains all interactions for the held-out movies, filtered so users appear in train.

Evaluation Metric
- Root Mean Squared Error (RMSE) over all test rows; lower is better.

Submission Rules
- Submit a CSV with columns [User_ID, Movie_ID, Rating].
- Every (User_ID, Movie_ID) pair in test.csv must appear exactly once; no extras or duplicates.
- Rating must be a finite numeric value. Predictions outside [1, 5] are allowed and evaluated directly.
