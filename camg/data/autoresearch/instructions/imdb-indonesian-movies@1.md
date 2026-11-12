# OpenMLE-fast task

Task ID: `imdb-indonesian-movies@1`

Native metric: `IndonesianMoviesRatingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2912 bytes)
- `data/sample_submission.csv` (7041 bytes); columns: ["id", "users_rating"]
- `data/test.csv` (122925 bytes); columns: ["id", "title", "year", "description", "genre", "rating", "votes", "languages", "directors", "actors", "runtime"]
- `data/train.csv` (373315 bytes); columns: ["id", "title", "year", "description", "genre", "rating", "users_rating", "votes", "languages", "directors", "actors", "runtime"]

## Public description

IMDb Indonesian Movies: User Rating Prediction

Problem statement
Participants are challenged to build machine learning models that predict the IMDb user rating (users_rating) of Indonesian films based on their available metadata. The goal is to estimate perceived movie quality across decades, genres, and varying metadata completeness.

Files provided
- train.csv: Movie-level metadata with the ground-truth users_rating for training.
- test.csv: Movie-level metadata without users_rating; participants must predict this.
- sample_submission.csv: A template showing the required submission format and example predictions.

Target
- users_rating: Continuous numeric score reflecting IMDb user ratings.

Input features
Each row corresponds to one movie. All columns in train.csv except users_rating may be used as features. Columns include a mix of text and structured metadata such as:
- id: Unique identifier for each movie (stable across files).
- title: Movie title.
- year: Release year.
- description: Short synopsis (may be missing for some entries).
- genre: Primary genre label (single token, e.g., Horror, Drama, Comedy, etc.).
- rating: Age classification (may be missing).
- votes: Number of votes used to compute the user rating (skewed distribution).
- languages: Primary language(s) of the movie.
- directors: List-like string of director names.
- actors: List-like string of main cast names (may include null/nan artifacts).
- runtime: Runtime string (e.g., "100 min"; may be missing or irregular).

Evaluation
- Metric: Root Mean Squared Error (RMSE)
- Lower is better. RMSE is computed between the ground-truth users_rating and your predictions for the corresponding ids in test.csv.

Submission format
- A single CSV file with columns:
  - id: Movie identifier as provided in test.csv.
  - users_rating: Your predicted numeric rating for that id.
- The submission must contain exactly one row per id present in test.csv, with no extra or missing ids.

Notes and recommendations
- Data processing and feature engineering are key. Consider:
  - Cleaning Indonesian/English mixed text for description and title.
  - Parsing list-like directors/actors into usable categorical or frequency features, handling literal "nan" strings.
  - Converting runtime strings to numeric minutes.
  - Handling missing values robustly.
  - Using log transforms for heavily skewed counts like votes.
  - Accounting for temporal drift (e.g., via decade bins) in modeling.
- You may use any modeling approach (e.g., linear models, gradient boosting, or text models). Ensure predictions are valid numeric values.

Data split
- The train/test split is stratified by release decade to preserve temporal diversity. The id column links rows across files and defines the submission key.

Ethical and licensing
- The dataset is provided under a CC0 public domain dedication. Use responsibly and attribute when appropriate.
