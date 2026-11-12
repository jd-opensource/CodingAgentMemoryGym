# OpenMLE-fast task

Task ID: `tmbd-movie-dataset@1`

Native metric: `TmdbBoxOfficeRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3335 bytes)
- `data/sample_submission.csv` (4140 bytes); columns: ["id", "revenue_adj"]
- `data/test.csv` (107504 bytes); columns: ["id", "imdb_id", "budget", "budget_adj", "original_title", "cast", "homepage", "director", "tagline", "keywords", "overview", "runtime", "genres", "production_companies", "release_date", "release_year"]
- `data/train.csv` (798347 bytes); columns: ["id", "imdb_id", "budget", "budget_adj", "original_title", "cast", "homepage", "director", "tagline", "keywords", "overview", "runtime", "genres", "production_companies", "release_date", "release_year", "revenue_adj"]

## Public description

Title: Pre-release Worldwide Box Office Forecasting (2010-adjusted)

Problem statement
Build a model that predicts a movie’s worldwide box office revenue adjusted to 2010 dollars (revenue_adj) using only information available prior to release. This is a realistic forecasting task with heterogeneous inputs (text, categorical entities, dates, and numerics) and a highly skewed target.

Data description
You are provided with a single train/test split mimicking real pre-release forecasting:
- Train: Movies released up to 2013 (inclusive)
- Test: Movies released in 2014–2015

Files
- train.csv: Pre-release features and the target revenue_adj for training. Includes the identifier id.
- test.csv: The same features as train.csv except revenue_adj is withheld.
- sample_submission.csv: Example submission file with columns id and revenue_adj.

Columns available to model (pre-release signals)
- id: TMDb movie identifier (use as key; do not leak into evaluation merge order)
- imdb_id: IMDB identifier (optional feature)
- budget, budget_adj: Production budget in nominal and 2010-adjusted dollars
- original_title: Title text
- cast: Pipe-delimited list of principal cast
- director: Director(s)
- tagline: Tagline text
- keywords: Pipe-delimited keywords
- overview: Synopsis text
- runtime: Duration in minutes
- genres: Pipe-delimited genres
- production_companies: Pipe-delimited production companies
- homepage: Official site (may be empty)
- release_date: Release date (string). You may engineer year/month/weekday, etc.
- release_year: Release year (integer)

Columns intentionally excluded from train/test (post-release leakage or redundant)
- revenue (non-adjusted), profit, popularity, vote_count, vote_average, popularity_level, unnamed index columns if any

Target
- revenue_adj (continuous, non-negative). Predictions in submissions must be in the original 2010-adjusted scale (not log-transformed).

Evaluation
- Metric: Root Mean Squared Logarithmic Error (RMSLE) between your predictions and the ground truth revenue_adj.
  - For each movie i with true y_i and prediction p_i, RMSLE = sqrt( mean( (log1p(p_i) - log1p(y_i))^2 ) ).
  - Predictions should be non-negative. Any negative or non-finite predictions are clipped/sanitized to zero before scoring.

Submission format
- CSV with two columns and no header changes: id, revenue_adj
- One row per movie in test.csv. Each id must appear exactly once.

Notes and recommendations
- The target is long-tailed; log1p transformations in your model can stabilize training, but submit predictions in the original scale.
- Combine modalities: TF–IDF or modern embeddings for text; frequency/target-agnostic encodings for high-cardinality entities (cast, director, companies); calendar features from dates; and numeric transforms (e.g., log budgets).
- Beware temporal drift: only compute any historical aggregates (like a director’s prior average box office) from training years.
- No validation split is provided; use cross-validation within the training years if desired.

Deliverables
- Submit a CSV named however you like but with the exact columns id and revenue_adj as above.

This challenge is designed to be solvable with classic ML pipelines (linear models + TF–IDF, tree ensembles) while rewarding careful feature engineering and temporal generalization.
