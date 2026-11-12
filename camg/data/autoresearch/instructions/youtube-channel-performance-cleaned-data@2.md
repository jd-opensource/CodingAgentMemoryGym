# OpenMLE-fast task

Task ID: `youtube-channel-performance-cleaned-data@2`

Native metric: `YouTubeCategoryMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (417 bytes)
- `data/sample_submission.csv` (23214 bytes); columns: ["video_id", "category_name"]
- `data/test.csv` (1503174 bytes); columns: ["video_id", "title", "tags", "description", "publish_time", "publish_date", "publish_hour", "day_of_week", "Title_Length", "channel_title"]
- `data/train.csv` (7708702 bytes); columns: ["video_id", "title", "tags", "description", "publish_time", "publish_date", "publish_hour", "day_of_week", "Title_Length", "channel_title", "category_name"]

## Public description

Title: YouTube Category Prediction from Publish-Time Metadata

Files in this directory (relative paths):
- train.csv
- test.csv
- sample_submission.csv

Task: Predict category_name for each video in test.csv using metadata available at publish time.


Submission format: CSV with columns [video_id, category_name] covering all rows in test.csv.
