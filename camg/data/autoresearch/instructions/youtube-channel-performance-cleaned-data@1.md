# OpenMLE-fast task

Task ID: `youtube-channel-performance-cleaned-data@1`

Native metric: `YouTubeViewsRegressionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3283 bytes)
- `data/sample_submission.csv` (17913 bytes); columns: ["video_id", "views"]
- `data/test.csv` (1004293 bytes); columns: ["video_id", "title", "channel_title", "category_id", "category_name", "publish_time", "tags", "publish_date", "publish_hour", "day_of_week", "Title_Length", "description"]
- `data/train.csv` (8308208 bytes); columns: ["video_id", "title", "channel_title", "category_id", "category_name", "publish_time", "tags", "publish_date", "publish_hour", "day_of_week", "Title_Length", "description", "views"]

## Public description

Title: Predicting YouTube Trending Views from Pre-Publish Metadata

Problem statement:
Build a model to predict the number of views at the first trending snapshot for US YouTube videos using only information available at or before publish time. The task is a regression problem on a heavy-tailed target, requiring strong feature engineering across text, category, channel, and timing signals while avoiding leakage from contemporaneous engagement metrics.

Data description:
You are provided with two files for modeling:
- train.csv: Each row is a video with its metadata (features) and the target label.
- test.csv: Same schema as train.csv but without the target.

Target:
- views: The number of views recorded at the first trending snapshot.

Features included (pre-publish, leakage-safe):
- video_id: Unique identifier for the video (use as key; may be used as a feature with caution).
- title: Video title (text).
- channel_title: Channel name (categorical/text).
- category_id, category_name: Category identifiers and names.
- publish_time: Original ISO timestamp string when the video was published.
- publish_date: Date string (YYYY-MM-DD) extracted from publish_time.
- publish_hour: Hour of day (0–23) extracted from publish_time.
- day_of_week: Day name (e.g., Monday) extracted from publish_time.
- Title_Length: Length of title string in characters.
- tags: Pipe-separated tags.
- description: Full text description.

Intentionally excluded to prevent leakage:
- likes, dislikes, comment_count, like_ratio, comment_ratio, trending_date, comments_disabled, ratings_disabled, video_error_or_removed, thumbnail_link.
These are contemporaneous with views or post-publish signals and would make the task trivial or unfair.

Recommended approach:
- Data processing: Deduplicate by video_id + trending snapshot, robustly parse timestamps.
- Feature engineering: Text normalization, tokenization for title/tags/description; TF-IDF or embeddings; counts and keyword flags; categorical encodings for category_name and channel_title; temporal features from publish_time.
- Modeling: Train regression models that handle long-tailed targets (e.g., tree-based models, regularized linear models, or neural encoders). Consider log-transforming the target during training.
- Evaluation: Validate generalization under temporal distribution shift.

Evaluation metric:
- Root Mean Squared Error (RMSE) computed on log1p scale.
  RMSE(log1p(y_true), log1p(y_pred)) ensures fairness with heavy-tailed counts and penalizes large errors proportionally.

Submission format:
- A CSV file with exactly two columns, in this order:
  video_id, views
- video_id: Must match the IDs in test.csv exactly.
- views: Your predicted view counts (non-negative numeric). Predictions are evaluated on the log1p scale.

Data split:
- The split is temporal: train contains earlier trending dates; test contains later ones. This mimics realistic forecasting and reduces leakage.

Final files provided:
- train.csv
- test.csv
- sample_submission.csv

Notes:
- Keep your pipeline deterministic for reproducibility.
- Do not merge in aggregated statistics computed across the entire dataset, as they may cause leakage across the temporal split.
- Use the full provided data; runtime constraints are not enforced.
