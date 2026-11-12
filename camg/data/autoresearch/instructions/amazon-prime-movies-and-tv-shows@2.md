# OpenMLE-fast task

Task ID: `amazon-prime-movies-and-tv-shows@2`

Native metric: `AmazonPrimeRatingMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2516 bytes)
- `data/sample_submission.csv` (18054 bytes); columns: ["show_id", "rating"]
- `data/test.csv` (897251 bytes); columns: ["show_id", "type", "title", "director", "cast", "country", "date_added", "release_year", "duration", "listed_in", "description"]
- `data/train.csv` (3067919 bytes); columns: ["show_id", "type", "title", "director", "cast", "country", "date_added", "release_year", "rating", "duration", "listed_in", "description"]

## Public description

Problem title: Predict Content Rating of Amazon Prime Titles

Problem statement
Build a robust multi-class classifier to predict the content rating of Amazon Prime titles. Each row describes one title with text synopsis and rich metadata (type, cast, country, release year, duration, genres, etc.). Your task is to infer the single categorical rating label assigned to the title.

Data description
Provided files:
- train.csv: Labeled data with features and a rating column (target)
- test.csv: Unlabeled data with the same features but without the rating column
- sample_submission.csv: Example submission with columns show_id and rating

Columns
- show_id: Unique identifier per title
- type: Movie or TV Show
- title: Title name
- director: Director(s)
- cast: Cast members
- country: Countries
- date_added: Date added to platform
- release_year: Year of release
- duration: Runtime in minutes (for movies) or number of seasons (for TV shows)
- listed_in: Genres/categories
- description: Short text synopsis
- rating (train only): Target content rating label (e.g., TV-Y, TV-PG, TV-14, TV-MA, G, PG, PG-13, R, NC-17, NR, 7+, 13+, 16+, 18+, ALL, etc.)

Submission format
- A CSV with exactly two columns in this order: show_id, rating
- One row for each show_id present in test.csv, in the same order
- Predicted rating must be one of the valid class labels present in train.csv

Evaluation
- Metric: Macro F1 score across rating classes
- For each class c, F1_c = 2 * precision_c * recall_c / (precision_c + recall_c) when denominators are non-zero, else 0. The final score is the unweighted average of F1_c over all classes that appear in the test set.

Modeling guidance and expectations
- Use both textual fields (description, title, cast, director, listed_in) and structured fields (type, country, release_year, duration, date_added)
- Address data cleaning and normalization: missing values, varying duration units, country list formatting, and textual preprocessing
- Consider feature engineering (n-grams, TF-IDF, transformer embeddings; categorical encoders; interaction features)
- Explore diverse models and ensembles: linear classifiers, gradient boosting trees, neural networks (e.g., combining text embeddings with tabular models)
- The test set labels are guaranteed to be seen in the training set at least once

Notes
- Do not include file paths in any CSV fields or predictions
- Predict a single rating per show_id
- The dataset size supports comprehensive modeling without runtime constraints
