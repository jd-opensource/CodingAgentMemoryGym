# OpenMLE-fast task

Task ID: `myanimelist-dataset@1`

Native metric: `AnimeRatingPredictionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/anime_features.csv` (5953102 bytes); columns: ["anime_id", "Name", "English name", "Other name", "Score", "Genres", "Type", "Episodes", "Premiered", "Status", "Producers", "Licensors", "Studios", "Source", "Duration", "Rating", "Rank", "Popularity", "Favorites", "Scored By", "Members"]
- `data/description.txt` (3324 bytes)
- `data/sample_submission.csv` (206058 bytes); columns: ["row_id", "rating"]
- `data/submission.csv` (585405 bytes); columns: ["row_id", "rating"]
- `data/test.csv` (372453 bytes); columns: ["row_id", "user_id", "anime_id"]
- `data/train.csv` (1735125 bytes); columns: ["row_id", "user_id", "anime_id", "rating"]
- `data/user_features.csv` (5375149 bytes); columns: ["user_id", "Username", "Gender", "Birthday", "Location", "Joined", "Days Watched", "Mean Score", "Watching", "Completed", "On Hold", "Dropped", "Plan to Watch", "Total Entries", "Rewatched", "Episodes Watched"]

## Public description

Title: MAL Explicit Rating Prediction (1–10)

Background
MyAnimeList (MAL) users assign explicit integer ratings from 1 to 10 for anime they have watched. Accurate prediction of a user’s explicit rating for a given anime is a core building block for personalization and recommendation. This competition challenges you to build models that generalize across users and titles while leveraging rich side information about anime and users.

Problem Statement
Given a user and an anime, predict the user’s explicit rating on a 1–10 scale. You are provided historical user–anime ratings for training, plus optional side information files. Your task is to predict ratings for a held-out set of user–anime pairs in the test set.

Files
The following files will be available after running the provided data preparation script:
- train.csv: Historical interactions with the ground-truth rating. Columns: row_id, user_id, anime_id, rating.
- test.csv: The evaluation set without ratings. Columns: row_id, user_id, anime_id.
- sample_submission.csv: A submission template with random but valid ratings. Columns: row_id, rating.
- anime_features.csv: Side information for anime titles (e.g., genres, type, ranks, counts, etc.). Key: anime_id.
- user_features.csv: Side information for users (e.g., activity stats and demographics, when available). Key: user_id.

Target
- rating: an integer in [1, 10]. Models may output real-valued predictions, which will be evaluated against the integer ground truth.

Evaluation
- Metric: Root Mean Squared Error (RMSE) between your predictions and the ground truth ratings in the test set.
- Formal definition: RMSE = sqrt(mean((y_pred_clipped − y_true)^2)). Predictions are clipped to [1, 10] prior to scoring to avoid undue penalty from out-of-range outputs.
- Submission format: A CSV with two columns named exactly: row_id, rating. The row_id values must exactly match those in test.csv; order does not matter.

Rules and Notes
- Train/test split is at the individual rating level. Many users and anime will appear in both train and test; the exact pairs held out for test are excluded from train.
- Ratings with value 0 (no score) are excluded from training and evaluation.
- The side information files are provided to encourage feature engineering (e.g., genre encoding, popularity signals, activity statistics). Use of these files is optional but likely beneficial.
- All files are self-contained; no file paths are embedded in CSV content.

Baseline Ideas (non-exhaustive)
- Global/Anime/User means and deviations
- Matrix factorization and variants (ALS, BPR for ordinal targets with mapping to [1,10])
- Gradient boosted trees or neural networks on engineered features from anime_features and user_features
- Hybrid models that combine collaborative signals with side information

Deliverables
- Submit a CSV named submission.csv with columns: row_id, rating.
- Your model should be trained on train.csv; test.csv must not be used for training. You may optionally join anime_features.csv and user_features.csv using anime_id and user_id, respectively.

Reproducibility
- The split is deterministic and reproducible. The row_id uniquely identifies each (user_id, anime_id) pair in train/test.

Good luck, and have fun building a recommender that understands anime preferences!
