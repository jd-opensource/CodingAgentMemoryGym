# OpenMLE-fast task

Task ID: `customer-satisfaction-10k@2`

Native metric: `CustomerSatisfactionSpeedMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (351 bytes)
- `data/sample_submission.csv` (18595 bytes); columns: ["id", "speed"]
- `data/test.csv` (34586 bytes); columns: ["id", "overall", "food", "accurate"]
- `data/train.csv` (171329 bytes); columns: ["id", "overall", "food", "accurate", "speed"]

## Public description

Competition: Predict Delivery Speed Satisfaction (1–5)

Data description:
- train.csv: id, overall, food, accurate, speed (target).
- test.csv: id, overall, food, accurate.
- sample_submission.csv: id, speed.

Evaluation:
- Metric: Mean Absolute Error (MAE) on speed. Lower is better.
- Submit a CSV with columns id and speed matching test.csv ids.
