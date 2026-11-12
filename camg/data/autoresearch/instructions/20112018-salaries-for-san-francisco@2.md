# OpenMLE-fast task

Task ID: `20112018-salaries-for-san-francisco@2`

Native metric: `OvertimeAUCClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (387 bytes)
- `data/sample_submission.csv` (2108372 bytes); columns: ["row_id", "overtime_probability"]
- `data/test.csv` (4573024 bytes); columns: ["row_id", "JobTitle", "BasePay", "OtherPay", "Benefits", "Year"]
- `data/train.csv` (11346382 bytes); columns: ["JobTitle", "BasePay", "OtherPay", "Benefits", "Year", "HasOvertime"]

## Public description

Title: Will an employee accrue any overtime? (San Francisco, 2011–2018)

Files:
- train.csv
- test.csv
- sample_submission.csv

Columns:
- JobTitle, BasePay, OtherPay, Benefits, Year, HasOvertime (train only)
- test.csv also includes row_id (no label)

Submission:
- CSV with columns: row_id, overtime_probability (values in [0,1])

Evaluation:
- ROC AUC computed by matching on row_id
