# OpenMLE-fast task

Task ID: `best-selling-steam-games-of-all-time@1`

Native metric: `SteamReviewForecastMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3447 bytes)
- `data/sample_submission.csv` (15576 bytes); columns: ["id", "all_reviews_number"]
- `data/test.csv` (137342 bytes); columns: ["id", "release_date", "developer", "user_defined_tags", "supported_os", "supported_languages", "price", "other_features"]
- `data/train.csv` (587188 bytes); columns: ["id", "release_date", "developer", "user_defined_tags", "supported_os", "supported_languages", "price", "other_features", "all_reviews_number"]

## Public description

Competition: Forecast Steam Review Volume from Pre-release Metadata

Problem statement
Given only metadata that is available at or before release for a Steam game, predict its eventual total number of user reviews on Steam. This simulates an early-stage market reach forecast based on genre/tags, platform/language support, developer identity, features, price, and release timing.

Data description
- train.csv: Each row is a game. Columns include a unique id, metadata features, and the target label all_reviews_number (exact integer review counts).
- test.csv: Same feature columns and id as train.csv but without the target label.
- sample_submission.csv: A template showing the required submission format; participants will replace the all_reviews_number values with their predictions for the rows in test.csv.

Included feature columns
- id: Unique identifier for each row. Use this to align predictions to the test set.
- release_date: Steam release date as text (e.g., "21 Aug, 2012"). Participants may parse to engineer time features.
- developer: Primary developer/studio name.
- user_defined_tags: Comma-separated standardized tags (subset of 42 genres/tags).
- supported_os: Comma-separated list of officially supported operating systems (win, mac, linux).
- supported_languages: Comma-separated list of supported interface/audio/subtitle languages.
- price: Price in regional USD (MENA). A value of 0 indicates Free to Play.
- other_features: Comma-separated set of Steam player support features (e.g., Single-player, Online Co-op, Steam Achievements, etc.).

Target label
- all_reviews_number: The total number of user reviews the game has received on Steam.

Excluded columns
The following original dataset columns are excluded from train.csv and test.csv to avoid target leakage or mixed-provenance noise: reviews_like_rate, estimated_downloads, age_restriction, rating, difficulty, length, game_name.

Evaluation metric
- Primary metric: Root Mean Squared Error (RMSE) computed on log1p of the counts.
- Concretely: For each game i in the test set, compute e_i = log1p(y_pred_i) - log1p(y_true_i). The score is sqrt(mean(e_i^2)). This metric stabilizes heavy-tailed counts and rewards relative accuracy across both indie and blockbuster scales.

Submission format
- CSV with two columns: id and all_reviews_number.
- id must match exactly the ids provided in test.csv.
- all_reviews_number must be non-negative numeric values (floats or integers). The metric operates on log1p; negative or non-finite values will be rejected.

Modeling guidance (optional)
- Suggested feature engineering: Parse release_date to derive year, month, quarter, day-of-week, and age at snapshot; multi-hot encode user_defined_tags, supported_os, supported_languages, and other_features; compute log1p(price) and a free_to_play indicator.
- Handle high-cardinality developer with frequency capping, hashing, or target encoding on train only.
- Consider temporal generalization: trends change, and the split is chronological.

Final competition files
- train.csv
- test.csv
- sample_submission.csv

Notes
- The split is a chronological 80/20 by release_date: train contains the earlier 80% of games; test contains the most recent 20%. This enforces forecasting realism.
- No validation set is provided; participants may create their own cross-validation on train.
- The dataset size is the full set of 2,380 games to maximize modeling depth and challenge.
