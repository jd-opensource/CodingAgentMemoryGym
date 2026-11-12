# OpenMLE-fast task

Task ID: `amazon-echo-dot-2-reviews-dataset@1`

Native metric: `EchoDotReviewRatingMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/sample_submission.csv` (9385 bytes); columns: ["review_id", "rating"]
- `data/test.csv` (230072 bytes); columns: ["review_id", "review_text", "review_color", "user_verified", "review_month", "configuration_text"]
- `data/train.csv` (939490 bytes); columns: ["review_id", "review_text", "review_color", "user_verified", "review_month", "configuration_text", "rating"]

## Public description

No additional public description was provided.
