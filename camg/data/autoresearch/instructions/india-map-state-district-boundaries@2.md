# OpenMLE-fast task

Task ID: `india-map-state-district-boundaries@2`

Native metric: `IndiaToponymResolutionMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (148 bytes)
- `data/sample_submission.csv` (15267 bytes); columns: ["id", "label"]
- `data/test.csv` (12926 bytes); columns: ["id", "state_name", "surface_form", "target_level"]
- `data/train.csv` (202143 bytes); columns: ["id", "state_name", "surface_form", "target_level", "label"]

## Public description

Title: Fuzzy Toponym Resolution for Indian Administrative Units (Districts & Tehsils)

Files provided
- train.csv
- test.csv
- sample_submission.csv
