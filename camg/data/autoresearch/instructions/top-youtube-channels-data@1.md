# OpenMLE-fast task

Task ID: `top-youtube-channels-data@1`

Native metric: `YouTubeSubscribersRankingMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2597 bytes)
- `data/sample_submission.csv` (3815 bytes); columns: ["id", "subscribers"]
- `data/test.csv` (12211 bytes); columns: ["id", "youtuber", "video_views", "video_count", "category", "started"]
- `data/train.csv` (56936 bytes); columns: ["id", "youtuber", "video_views", "video_count", "category", "started", "subscribers"]

## Public description

Top YouTube Channels: Predict Subscriber Ranking

Problem statement
Participants must predict the relative popularity of top YouTube channels. Given metadata for each channel (name, video views, video count, category, and start year), produce a numeric prediction per channel that ranks channels by their subscriber counts. Higher predictions should correspond to higher true subscriber counts. The task focuses on learning ordering, not exact calibration, and the label distribution is extremely skewed.

Files provided
- train.csv: Training data with features and the target.
- test.csv: Test data with features only.
- sample_submission.csv: Template showing the required submission format.

Columns
- id: An anonymized unique identifier per channel.
- youtuber: Channel name as provided.
- video_views: Total channel video views (integer; may be zero).
- video_count: Number of uploaded videos (integer; may be zero).
- category: Channel category (string; may be "Unknown").
- started: Channel start year (integer).
- subscribers: Target column (integer; present only in train.csv).

Task details and guidance
- You must predict a numeric value for each row in test.csv and submit a CSV with columns [id, subscribers]. Any real-valued score is accepted; only the ordering matters for the primary metric.
- Useful derived features may include: years_since_start, views_per_video = video_views / max(video_count, 1), and simple text features from the youtuber field (e.g., character or word n-grams). Handle missing category by assigning a dedicated value (e.g., "Unknown").
- The distribution is heavy-tailed with outliers and special cases (e.g., zero views/count). Robust preprocessing and modeling are recommended.

Evaluation
- Primary metric: Spearman rank correlation between your predictions and the true subscriber counts on the test set. This metric evaluates how well your scores preserve the ordering of channels by subscribers and is invariant to monotonic transformations.
- Requirements: Your submission must include predictions for all ids in test.csv and only for those ids. Predictions must be finite numeric values.

Submission format
- File: CSV with header: id,subscribers
- Each row: id from test.csv and a numeric prediction.

Important notes
- The rank column from the original data is not part of the competition data to prevent leakage.
- Do not attempt to infer labels from filenames or ordering; ids are anonymized and randomized.
- External data is not required. Traditional tabular ML models, optionally augmented with basic text features from youtuber, work well.
