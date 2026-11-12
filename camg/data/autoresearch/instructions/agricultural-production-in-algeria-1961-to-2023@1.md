# OpenMLE-fast task

Task ID: `agricultural-production-in-algeria-1961-to-2023@1`

Native metric: `AlgeriaAgriPanelMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (90 bytes)
- `data/sample_submission.csv` (41192 bytes); columns: ["series_id", "year", "value"]
- `data/series_map.csv` (23099 bytes); columns: ["series_id", "original_name", "unit", "category", "is_target"]
- `data/target_series.csv` (976 bytes); columns: ["series_id"]
- `data/test.csv` (16275 bytes); columns: ["series_id", "year"]
- `data/train.csv` (340962 bytes); columns: ["series_id", "year", "value"]

## Public description

Files:
- train.csv
- test.csv
- sample_submission.csv
- series_map.csv
- target_series.csv
