# OpenMLE-fast task

Task ID: `tmbd-movie-dataset@2`

Native metric: `TmdbRatingRegressionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3689 bytes)
- `data/sample_submission.csv` (1795 bytes); columns: ["id", "vote_average"]
- `data/test.csv` (105866 bytes); columns: ["id", "original_title", "tagline", "keywords", "overview", "genres", "cast", "director", "production_companies", "homepage", "runtime", "budget", "budget_adj", "release_date", "release_year"]
- `data/train.csv` (773401 bytes); columns: ["id", "original_title", "tagline", "keywords", "overview", "genres", "cast", "director", "production_companies", "homepage", "runtime", "budget", "budget_adj", "release_date", "release_year", "vote_average"]

## Public description

TMDb Cold-Start Audience Rating Prediction

Problem statement
Studios often need to estimate a film’s likely audience reception before release to guide positioning and marketing. Your task is to predict a movie’s TMDb vote_average (a continuous score in [0, 10]) using only information that would plausibly be available pre-release (e.g., title, synopsis, cast, crew, genres, budget, etc.). The challenge is designed as a temporal cold-start setting: models trained on past releases must generalize to later years.

Data
You are provided with two CSV files containing movie-level records:
- train.csv: Each row is a movie with pre-release descriptors and the target column vote_average.
- test.csv: The same pre-release descriptors for a held-out set of later releases. The target vote_average is hidden.
A sample_submission.csv illustrates the expected submission format.

Feature columns (appear in both train.csv and test.csv)
- id: Unique movie identifier (string/integer). Required in submissions.
- original_title: Original movie title (text)
- tagline: Tagline or slogan (text; may be empty)
- keywords: Pipe-delimited keywords (text/list-like)
- overview: Plot summary (text)
- genres: Pipe-delimited list of genres (categorical, multi-label)
- cast: Pipe-delimited main cast (categorical, high-cardinality)
- director: Director(s) (categorical)
- production_companies: Pipe-delimited list of companies (categorical, high-cardinality)
- homepage: Official site URL (text; you may extract domain or ignore)
- runtime: Runtime in minutes (numeric)
- budget: Production budget (numeric)
- budget_adj: Budget adjusted to 2010 dollars (numeric)
- release_date: Calendar date string YYYY-MM-DD (date-like)
- release_year: Year number (numeric)

Target column (train.csv only)
- vote_average: Audience rating in [0, 10] (float)

Important notes
- The split is chronological to mimic a real cold-start scenario: training data consists of earlier releases, while test data contains later releases only.
- Post-release outcome fields such as revenue, revenue_adj, popularity, vote_count, profit, and any derivative of these are excluded from the feature set to avoid leakage.
- Some fields are long text and high-cardinality categorical attributes. Strong solutions typically combine text modeling (e.g., TF-IDF) with robust encodings for entities (e.g., hashing/frequency) and careful regularization.

Submission format
- A CSV file with exactly two columns and a header: id, vote_average
- One row per movie in test.csv. The id values must match test.csv exactly and be unique.
- Predicted vote_average should be numeric (float). Values outside [0, 10] will be clipped during evaluation.

Evaluation
Submissions are evaluated using a reliability-weighted Root Mean Squared Error (Weighted RMSE) on the 0–10 scale:
- Each test movie i receives a weight w_i = log(1 + min(vote_count_i, 5000)).
- The score is sqrt( sum_i w_i * (y_i - yhat_i)^2 / sum_i w_i ).
- The weighting emphasizes titles with more votes (more reliable labels) while capping and log-scaling prevent domination by a few mega-hits.

Files provided
- train.csv
- test.csv
- sample_submission.csv

Tips
- Engineer time features from release_date (year/month/quarter/weekday, season).
- Use text features from overview, tagline, keywords, and title (e.g., word/character n-grams).
- Encode high-cardinality entities (cast, director, companies) with hashing or frequency, and consider leakage-safe historical statistics computed on training data only.
- Consider log transforms for skewed numerics (e.g., budget, budget_adj).
- Expect temporal drift between train and test; regularization and ensembling help robustness.
