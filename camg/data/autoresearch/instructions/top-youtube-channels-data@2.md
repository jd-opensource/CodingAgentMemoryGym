# OpenMLE-fast task

Task ID: `top-youtube-channels-data@2`

Native metric: `YouTubeViewsRegressionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4007 bytes)
- `data/sample_submission.csv` (4474 bytes); columns: ["row_id", "video_views"]
- `data/test.csv` (9786 bytes); columns: ["row_id", "youtuber", "subscribers", "video_count", "category", "started"]
- `data/train.csv` (47846 bytes); columns: ["row_id", "youtuber", "subscribers", "video_count", "category", "started", "video_views"]

## Public description

Most-Viewed Channel Regression Challenge (RMSLE)

Problem statement
Participants must predict the total lifetime video views of YouTube channels from tabular metadata. The target exhibits an extreme long-tail distribution with zeros and very large counts. Robust preprocessing, careful feature engineering, and non-linear models can significantly improve accuracy.

Files
- train.csv: Training data with features and the target.
- test.csv: Test data with the same features but without the target.
- sample_submission.csv: Example submission file showing the required format.

Input features and target
- Features (columns in train.csv and test.csv):
  - row_id: Unique identifier for each record (use this to align predictions; do not model it).
  - youtuber: Channel name (free text; can be used for text features such as length, character n-grams, keyword flags, etc.).
  - subscribers: Total subscribers (non-negative integer).
  - video_count: Number of uploaded videos (non-negative integer).
  - category: Declared channel category. Missing categories are labeled as "Unknown".
  - started: Channel start year (integer).
- Target (only in train.csv):
  - video_views: Total lifetime video views (non-negative integer). This is what you must predict for test.csv rows.

Task details and constraints
- Use all rows of the provided data. No subset is necessary.
- The following are intentionally excluded from the final feature set to prevent leakage of ordering information: any rank-like columns are not present in the competition files.
- Participants may perform feature engineering, including but not limited to:
  - Log-transform numeric features, interaction terms (e.g., subscribers × video_count), and calendar features (e.g., years since start).
  - Robust encoding for category (target-agnostic encodings such as one-hot or frequency).
  - Text processing of youtuber names (length, character/word n-grams, presence of substrings like "VEVO", etc.).
- External data is allowed provided it does not reveal the target for test entries and adheres to Kaggle rules.

Evaluation
- Metric: Root Mean Squared Log Error (RMSLE) between predictions and ground truth on video_views.
- Definition: RMSLE(y_true, y_pred) = sqrt(mean((log1p(y_pred) - log1p(y_true))^2)).
- Properties: Handles zeros gracefully, reduces the impact of extreme outliers, and evaluates multiplicative accuracy.

Submission format
- Your submission must be a CSV with the following columns in any order:
  - row_id: must match exactly the values in test.csv.
  - video_views: your non-negative predictions (floats are allowed).
- No extra columns. No missing or non-finite values. Values will be clipped to [0, +inf) before scoring.

Train/test split
- A single 80/20 train/test split is provided. The split is stratified on quantiles of log1p(video_views) to ensure a representative distribution across the heavy-tailed target. The identifiers in test.csv match the sample_submission.csv and the hidden ground truth used for evaluation.

Tips for a strong baseline
- Start by modeling log1p(video_views).
- Include interactions such as subscribers × video_count and years_since_start = current_year - started.
- Try regularized linear models on engineered features or gradient boosting trees (e.g., XGBoost, LightGBM, CatBoost).
- Consider simple text features from youtuber (e.g., length, digits ratio, presence of common tokens, character n-grams).

File schema
- train.csv columns: row_id, youtuber, subscribers, video_count, category, started, video_views
- test.csv columns: row_id, youtuber, subscribers, video_count, category, started
- sample_submission.csv columns: row_id, video_views

Important notes
- Do not attempt to infer targets from any auxiliary files or metadata: only train.csv includes the target.
- The order of rows in submissions does not matter as long as row_id values match the test set exactly.
- Numerical stability is enforced during scoring; negative or NaN predictions will be treated as 0.
