# OpenMLE-fast task

Task ID: `game-recommendations-on-steam@1`

Native metric: `SteamRecommendationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2512 bytes)
- `data/sample_submission.csv` (531102 bytes); columns: ["review_id", "is_recommended"]
- `data/test.csv` (1432007 bytes); columns: ["review_id", "app_id", "user_id", "date", "hours", "helpful", "funny"]
- `data/test_games.csv` (20244 bytes); columns: ["app_id", "title", "date_release", "win", "mac", "linux", "rating", "positive_ratio", "user_reviews", "price_final", "price_original", "discount", "steam_deck"]
- `data/test_games_metadata.json` (16901 bytes)
- `data/test_users.csv` (488007 bytes); columns: ["user_id", "products", "reviews"]
- `data/train.csv` (2970505 bytes); columns: ["review_id", "app_id", "user_id", "date", "hours", "helpful", "funny", "is_recommended"]
- `data/train_games.csv` (14922 bytes); columns: ["app_id", "title", "date_release", "win", "mac", "linux", "rating", "positive_ratio", "user_reviews", "price_final", "price_original", "discount", "steam_deck"]
- `data/train_games_metadata.json` (9292 bytes)
- `data/train_users.csv` (985043 bytes); columns: ["user_id", "products", "reviews"]

## Public description

Competition: Steam Review Recommendation — Predict Thumbs-Up at Scale

Problem statement
- Task: Predict the probability that a user will recommend a game (is_recommended) for future Steam reviews. Your model should learn from historical user–game interactions and rich metadata to generalize across users, games, and time.
- Setting: A strict time-based split simulates real deployment. Models should handle temporal drift, cold-start games, and user heterogeneity, leveraging tabular signals, categorical attributes, tags, and text descriptions.

Data provided (under public/)
Join keys:
- app_id: game/add-on identifier
- user_id: anonymized user identifier

Final data files
- train.csv — interaction-level training data with labels. Columns: review_id, app_id, user_id, date, hours, helpful, funny, is_recommended.
- test.csv — interaction-level test data without labels. Columns mirror train.csv but omit is_recommended. Predictions are keyed by review_id.
- sample_submission.csv — example submission with the required format.
- train_games.csv, test_games.csv — item-level attributes for games present in train/test interactions (e.g., price_final, discount, platforms, date_release, rating, user_reviews, positive_ratio).
- train_users.csv, test_users.csv — user-level attributes for users present in train/test interactions (e.g., products, reviews).
- train_games_metadata.json, test_games_metadata.json — content metadata (tags and descriptions) for games present in train/test interactions.

Split protocol
- Train interactions: reviews with date strictly before 2022-01-01.
- Test interactions: reviews with date on/after 2022-01-01.
- The split is deterministic and guarantees no overlap of review_id between train and test.

Evaluation
- Metric: ROC-AUC (Area Under the Receiver Operating Characteristic Curve).
  - Submit a probability in [0, 1] for each review_id in test.csv.
  - AUC is threshold-independent and robust to class imbalance; it measures how well your scores separate recommended vs. not recommended interactions.

Submission format
- CSV with two columns (exact order): review_id,is_recommended
- review_id must match those in test.csv exactly once.
- is_recommended must be numeric predictions in [0, 1].

Notes
- Use metadata files freely; they represent store-side information and do not leak labels.
- Any history-based aggregates must be derived only from train interactions (no peeking into test labels).
- No paths are embedded in any CSVs; join via IDs.
