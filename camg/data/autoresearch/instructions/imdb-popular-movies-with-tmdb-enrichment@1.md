# OpenMLE-fast task

Task ID: `imdb-popular-movies-with-tmdb-enrichment@1`

Native metric: `ImdbRevenueForecastMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2838 bytes)
- `data/sample_submission.csv` (8992 bytes); columns: ["Id", "Revenue"]
- `data/test.csv` (199483 bytes); columns: ["Id", "Title", "originalTitle", "Year", "Runtime", "Genres", "Director", "Writer", "Actors", "Plot", "Budget", "Tagline", "Country", "Languages"]
- `data/train.csv` (2076101 bytes); columns: ["Id", "Title", "originalTitle", "Year", "Runtime", "Genres", "Director", "Writer", "Actors", "Plot", "Budget", "Tagline", "Country", "Languages", "Revenue"]

## Public description

IMDb Popular Movies Forecast Challenge: Pre-release Box Office Prediction

Problem statement
- Task: Predict a movie’s box office Revenue using only pre-release information.
- Context: Studios, platforms, and investors seek revenue forecasts before release. This dataset provides rich plots, genres, creative team, multilingual production info, and budget to enable content + metadata modeling.

Data files provided
- train.csv: Pre-release features plus target column Revenue.
- test.csv: Pre-release features only, with an Id column for row identification.
- sample_submission.csv: A sample file showing the expected submission format (Id, Revenue).

Columns included (features)
- Id: Synthetic identifier that uniquely maps rows across files.
- Title, originalTitle
- Year (year of release)
- Runtime (minutes)
- Genres (comma-separated)
- Director, Writer, Actors (comma-separated names)
- Plot (full plot summary)
- Budget (USD)
- Tagline
- Country (comma-separated production countries)
- Languages (comma-separated spoken languages)

Target
- Revenue (USD). Present in train.csv only.

Important exclusions (to ensure realism and fairness)
- Popularity, Votes, Rating, pure IDs, and external URLs are excluded to avoid post-release leakage or non-semantic lookup.

Train/test split
- Time-aware split reflecting realistic forecasting: train contains movies released up to 2021; test contains movies released from 2022 onward.
- Only movies with Revenue > 0 are included (nonzero revenue values are considered reliable, filtering out likely “unknown/not reported” entries).

Evaluation metric
- Root Mean Squared Logarithmic Error (RMSLE) on Revenue.
- Definition: rmsle = sqrt(mean((log1p(y_pred) - log1p(y_true))^2)).
- Rationale: RMSLE emphasizes relative errors, is robust to heavy-tailed revenues, and prevents a handful of blockbusters from dominating the score.

Submission format
- CSV with two columns: Id, Revenue.
- Id values must exactly match those in test.csv; Revenue predictions must be numeric and non-negative.

Modeling guidance (non-binding)
- Encourage blending text and tabular signals:
  - Text: TF-IDF or embeddings on Plot (+ optionally Tagline/Titles), with vocabulary capping or dimensionality reduction.
  - Structured: log1p(Budget), standardized Runtime, Year as numeric, multi-hot for Genres/Country/Languages, frequency-capped hashing for high-cardinality names (Director/Writer/Actors), and explicit missing indicators.
- Target transform: Train and evaluate models on log1p(Revenue) to stabilize the distribution; remember to invert for submission.

Notes
- Multilingual plots and multi-country productions are present; some fields have mild missingness. Robust preprocessing and feature engineering are part of the challenge.
- No image/audio files are provided; the task is tabular + text.
