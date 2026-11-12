# OpenMLE-fast task

Task ID: `predict-movie-success-rate@1`

Native metric: `MovieRevenueRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3208 bytes)
- `data/sample_submission.csv` (2036 bytes); columns: ["Id", "Revenue_Millions"]
- `data/test.csv` (55292 bytes); columns: ["Id", "Title", "Description", "Genre", "Director", "Actors", "Year", "Runtime_Minutes", "Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Musical", "Mystery", "Romance", "Sci_Fi", "Sport", "Thriller", "War", "Western"]
- `data/train.csv` (229853 bytes); columns: ["Id", "Title", "Description", "Genre", "Director", "Actors", "Year", "Runtime_Minutes", "Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Musical", "Mystery", "Romance", "Sci_Fi", "Sport", "Thriller", "War", "Western", "Revenue_Millions"]

## Public description

Competition: Box Office Revenue Forecast (2006–2016)

Problem statement
Build a model that predicts domestic box office revenue (Millions USD) for a movie using only information available before release. You are given a training set with the target and a test set without the target.

Target
- Revenue_Millions: Domestic revenue in millions of USD (continuous, non-negative).

What you can use
The provided tabular data combines text, categorical, and numeric signals extracted from public movie metadata. All columns reflect information plausibly available pre-release.
- Id: Unique identifier for each movie row.
- Title: Movie title (text).
- Description: Short plot description (text).
- Genre: Comma-separated list of genres (string).
- Director: Director name(s) (string).
- Actors: Top billed cast, comma-separated (string).
- Year: Release year (integer).
- Runtime_Minutes: Runtime in minutes (integer).
- Binary genre flags (0/1): Action, Adventure, Animation, Biography, Comedy, Crime, Drama, Family, Fantasy, History, Horror, Music, Musical, Mystery, Romance, Sci_Fi, Sport, Thriller, War, Western.
  Notes:
  - A historical header typo in the source (Aniimation) has been corrected to Animation.
  - Sci_Fi is a safe-column-name version of Sci-Fi.

What is not included (to prevent label leakage)
Post-release outcome signals are excluded from the modeling files: Rank, Rating, Votes, Metascore, Success.

Files
- train.csv: Training rows with all features above plus Revenue_Millions.
- test.csv: Test rows with the same features but without Revenue_Millions.
- sample_submission.csv: Example submission with two columns: Id and Revenue_Millions.

Suggested approach (non-exhaustive)
- Text: Build TF–IDF features on Title and Description (consider word and/or character n-grams with regularization).
- Categorical: One-hot or hash features for Director and Actors (top-k with rare-category binning). Parse Genre string to multi-hot and consider interactions with binary genre flags.
- Numeric: Scale Year and Runtime_Minutes; optionally craft interactions (e.g., decade bins, genre × runtime).
- Missing values: Fill text with empty string and numeric with sensible defaults; be robust to occasional missing entries.
- Models: Regularized linear models, tree ensembles (GBM/Random Forest), or shallow neural networks can perform well when blended.

Evaluation
Submissions are evaluated using Root Mean Squared Logarithmic Error (RMSLE) on Revenue_Millions:
- For each row i: e_i = log1p(y_pred_i) − log1p(y_true_i)
- RMSLE = sqrt(mean(e_i^2))
- Predictions must be non-negative; any negative values will be clipped to 0 for scoring.

Rationale: Revenue is heavy-tailed; RMSLE rewards multiplicative accuracy while reducing the dominance of outliers.

Submission format
- A CSV file with exactly two columns and header: Id,Revenue_Millions
- Include a row for every Id in test.csv, any order.

Data split
- A deterministic random split (fixed seed) partitions the original dataset into train and test; duplicates across Title+Year are de-duplicated prior to splitting. Only information available pre-release is retained in both splits.

Good luck and have fun forecasting the box office!
