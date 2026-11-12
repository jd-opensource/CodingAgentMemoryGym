# OpenMLE-fast task

Task ID: `agricultural-production-in-algeria-1961-to-2023@2`

Native metric: `AlgeriaAgriSmapeMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (127 bytes)
- `data/sample_submission.csv` (175987 bytes); columns: ["row_id", "value"]
- `data/series_meta.csv` (31147 bytes); columns: ["series_id", "original_name", "group_id", "measure"]
- `data/test.csv` (131076 bytes); columns: ["row_id", "year", "series_id"]
- `data/train.csv` (412052 bytes); columns: ["row_id", "year", "series_id", "value"]

## Public description

Algeria Agri-Matrix Completion

Files in public/: train.csv, test.csv, sample_submission.csv, series_meta.csv, description.txt
