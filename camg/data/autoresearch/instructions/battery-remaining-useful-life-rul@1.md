# OpenMLE-fast task

Task ID: `battery-remaining-useful-life-rul@1`

Native metric: `BatteryRemainingUsefulLifeMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (583 bytes)
- `data/sample_submission.csv` (70533 bytes); columns: ["row_id", "RUL"]
- `data/test.csv` (214569 bytes); columns: ["row_id", "discharge_time_s", "decrement_3_6_to_3_4_v_s", "max_voltage_discharge_v", "min_voltage_charge_v", "time_at_4_15v_s", "time_constant_current_s", "charging_time_s"]
- `data/train.csv` (905268 bytes); columns: ["row_id", "discharge_time_s", "decrement_3_6_to_3_4_v_s", "max_voltage_discharge_v", "min_voltage_charge_v", "time_at_4_15v_s", "time_constant_current_s", "charging_time_s", "RUL"]

## Public description

Battery Remaining Useful Life (RUL)

Files in this competition (under the public directory):
- train.csv: Training data with columns [row_id] + feature columns + RUL.
- test.csv: Test data with columns [row_id] + feature columns (no RUL).
- sample_submission.csv: Example submission with columns [row_id, RUL].
- description.txt: This file describing the dataset and expected formats.

Submission format
- A CSV file with exactly two columns: row_id and RUL, matching the ordering of test.csv.

Notes
- Do not include any labels or ground truth in your submission; predictions only.
