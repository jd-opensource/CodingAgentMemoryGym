# OpenMLE-fast task

Task ID: `letterboxd-movie-ratings-data@2`

Native metric: `LetterboxdMovieRatingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3198 bytes)
- `data/sample_submission.csv` (29136 bytes); columns: ["movie_id", "rating"]
- `data/test.csv` (574182 bytes); columns: ["movie_id", "movie_title", "original_language", "overview", "genres", "production_countries", "spoken_languages", "release_date", "year_released", "runtime", "popularity"]
- `data/train.csv` (2400582 bytes); columns: ["movie_id", "movie_title", "original_language", "overview", "genres", "production_countries", "spoken_languages", "release_date", "year_released", "runtime", "popularity", "rating"]

## Public description

Letterboxd Cold-Start Movie Quality Prediction

Problem statement
You are given rich metadata and plot overviews for a large catalog of films. Your task is to predict each film’s average Letterboxd user rating (on a 1–10 scale) for movies that have no observed interactions at test time. This simulates a common cold-start scenario in recommender systems where only item content is available for new titles.

Files you will work with
- train.csv: Movie-level features and the target column rating.
- test.csv: Same features as train.csv but without the rating column. This file defines the prediction set.
- sample_submission.csv: A valid example submission file with the correct format and columns.

Target
- rating: The arithmetic mean of user ratings for each movie, computed from explicit star ratings (1–10, half-star increments).

Features
Each row corresponds to one movie. Columns include, but are not limited to:
- movie_id: Stable identifier that links rows across files. Use it to merge with predictions only; do not treat it as a feature.
- movie_title: Title of the movie (text).
- original_language: Primary spoken language code (e.g., en, ja, fr).
- overview: Plot synopsis (free text; multilingual, noisy, and informative).
- genres, production_countries, spoken_languages: List-like string columns you can parse and encode.
- release_date, year_released, runtime, popularity: Numeric/date and categorical signals.
Columns that directly leak external crowd judgements (e.g., vote_average, vote_count) and external links/IDs have been removed from the provided train/test files.

Evaluation
- Metric: Mean Absolute Error (MAE) between your predictions and the ground-truth average ratings for the test set.
- Range handling: Predictions will be interpreted as real numbers and clipped to [1, 10] before scoring to ensure numerical robustness.
- Submission format: A CSV with two columns and a header: movie_id,rating. It must contain exactly one row per movie_id in test.csv.

Why this is challenging and meaningful
- Cold-start focus: Test movies have no interactions available; you must generalize from content. This mirrors production constraints for new releases.
- Heterogeneous data: Strong text signal (overview) combines with multilingual and tabular metadata (genres, language, era, runtime, popularity) to enable sophisticated feature engineering.
- Long-tail and drift: Wide coverage across decades, languages, and genres requires careful modeling and regularization.

Recommendations for participants
- Text: Clean and tokenize overview; try TF-IDF, character/word n-grams, or pretrained embeddings. Consider language detection or per-language models.
- Tabular: Engineer decade from year_released, language buckets, genre counts, log/popularity transforms, and runtime missingness indicators.
- Models: Strong baselines include linear models or gradient boosting on concatenated text+tabular features. Neural encoders over text plus tabular MLPs can further improve.

Submission
- Create a file with columns: movie_id,rating
- Ensure every movie_id in test.csv appears exactly once.
- Ratings can be any real number; they will be clipped to [1,10] before scoring.
