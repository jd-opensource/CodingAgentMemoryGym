# OpenMLE-fast task

Task ID: `employee-salaries-analysis@1`

Native metric: `OvertimePayRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (934 bytes)
- `data/sample_submission.csv` (13050 bytes); columns: ["row_id", "Overtime_Pay"]
- `data/test.csv` (115527 bytes); columns: ["row_id", "Department", "Department_Name", "Division", "Gender", "Base_Salary", "Longevity_Pay", "Grade"]
- `data/train.csv` (847781 bytes); columns: ["Department", "Department_Name", "Division", "Gender", "Base_Salary", "Longevity_Pay", "Grade", "Overtime_Pay"]

## Public description

Title: Predict Overtime Pay for County Employees

Files in public/
- train.csv: Training data with features and target Overtime_Pay.
- test.csv: Test data with row_id and features only (no target).
- sample_submission.csv: Template predictions with columns [row_id, Overtime_Pay].
- description.txt: This description file.

Target
- Overtime_Pay (continuous, non-negative)

Input features
- Department (categorical)
- Department_Name (categorical)
- Division (categorical)
- Gender (categorical)
- Base_Salary (numeric)
- Longevity_Pay (numeric)
- Grade (categorical)

Evaluation metric
- Root Mean Squared Logarithmic Error (RMSLE) computed between predicted and actual Overtime_Pay.
- Definition: RMSLE = sqrt(mean((log1p(y_pred_clipped) - log1p(y_true_clipped))^2)), with non-negative clipping.

Submission format
- CSV with two columns: row_id, Overtime_Pay.
- Every row_id in test.csv must appear exactly once in the submission.
