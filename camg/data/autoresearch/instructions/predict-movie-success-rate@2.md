# OpenMLE-fast task

Task ID: `predict-movie-success-rate@2`

Native metric: `MovieSuccessMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2985 bytes)
- `data/sample_submission.csv` (1859 bytes); columns: ["id", "Success"]
- `data/test.csv` (63605 bytes); columns: ["id", "Title", "Description", "Genre", "Director", "Actors", "Year", "Runtime_Minutes", "Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Musical", "Mystery", "Romance", "Sci_Fi", "Sport", "Thriller", "War", "Western"]
- `data/train.csv` (252349 bytes); columns: ["id", "Title", "Description", "Genre", "Director", "Actors", "Year", "Runtime_Minutes", "Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Musical", "Mystery", "Romance", "Sci_Fi", "Sport", "Thriller", "War", "Western", "Success"]

## Public description

Pre-release Movie Success Classification

Problem statement
Studios and investors need to decide which projects to back before release. Build a model that predicts the probability a movie will be commercially successful using only pre-release metadata and synopses.

Files provided
- train.csv: Training rows with features and the target column Success.
- test.csv: Test rows with the same features but without Success.
- sample_submission.csv: Example submission with the required columns.

Target
- Success: Binary label where 1 indicates a successful movie and 0 indicates otherwise. Submit probabilities, not hard labels.

Features
No post-release or leakage-prone signals are included. The tabular schema mixes free text, categorical names, and numeric attributes:
- id: Unique row identifier. Use this to align predictions with test rows.
- Title: Movie title (free text).
- Description: Short synopsis (free text).
- Genre: Comma-separated list of genres (string).
- Director: Director name(s).
- Actors: Comma-separated list of main cast.
- Year: Release year (integer).
- Runtime_Minutes: Runtime in minutes (integer).
- Binary genre indicators (0/1): Action, Adventure, Animation, Biography, Comedy, Crime, Drama, Family, Fantasy, History, Horror, Music, Musical, Mystery, Romance, Sci_Fi, Sport, Thriller, War, Western.
  Note: A misspelled Aniimation flag in the original source is standardized here as Animation.

Evaluation
- Metric: Average Precision (AP) on Success=1. AP measures area under the precision–recall curve based on the ranking induced by your submitted probabilities. Higher is better and the metric is robust to class imbalance.
- Submission format: A CSV with exactly two columns and header:
  id,Success
  Success must be a probability in [0,1]. The id values must exactly match those in test.csv, with no extras or omissions.

Data split
- Deterministic 80/20 stratified split into train/test is used. All classes present in test occur in train. The test labels are hidden and used only for scoring.

Guidance (non-binding)
- Text: Build TF–IDF features from Title and Description (word/char n-grams). Limit dimensionality and consider stopwording.
- Names: Encode Director/Actors via hashing trick, frequency, or top-K one-hot. Avoid target encoding that could leak.
- Genres: Use both the string Genre and binary flags; reconcile inconsistencies if helpful.
- Numeric: Use Year and Runtime_Minutes; interactions with genres can help.
- Class imbalance: Use class weights or calibrated decision functions. Cross-validation is encouraged for model selection.

Rules and notes
- Leakage-prone columns (e.g., ratings, votes, metascores, revenues) are not provided. External data may be used only if it does not include post-release information for the listed titles.
- Efficiency is not graded; you may use the full scale of the data.

Deliverable
- Submit a file with columns: id,Success. Your leaderboard score is the AP on the hidden test labels.
