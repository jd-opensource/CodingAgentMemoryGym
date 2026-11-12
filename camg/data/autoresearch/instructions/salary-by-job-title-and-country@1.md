# OpenMLE-fast task

Task ID: `salary-by-job-title-and-country@1`

Native metric: `SalaryPredictionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (690 bytes)
- `data/sample_submission.csv` (18772 bytes); columns: ["id", "predicted_salary"]
- `data/test.csv` (33694 bytes); columns: ["id", "age", "education_level", "job_title", "years_experience", "country"]
- `data/train.csv` (160937 bytes); columns: ["id", "age", "education_level", "job_title", "years_experience", "country", "salary"]

## Public description

Global Salary Prediction by Job Title and Country

Files
- train.csv — features plus target salary
- test.csv — features only
- sample_submission.csv — required submission format

Schema
- id — unique integer identifier
- age — numeric (years)
- education_level — integer in {0,1,2,3}
- job_title — string (lowercased, trimmed)
- years_experience — numeric (years)
- country — string (lowercased, trimmed)
- salary — numeric (USD, strictly positive). Present only in train.csv

Task and evaluation
- Task: Predict salary in USD for every row in test.csv.
- Submission format: CSV with exactly two columns: id and predicted_salary.
- Metric: RMSLE on salary predictions.
