# OpenMLE-fast task

Task ID: `data-engineer-salary-in-2024@1`

Native metric: `DataCompensationForecastMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1864 bytes)
- `data/sample_submission.csv` (57171 bytes); columns: ["row_id", "salary_in_usd"]
- `data/test.csv` (159249 bytes); columns: ["row_id", "experience_level", "employment_type", "job_title", "employee_residence", "remote_ratio", "company_location", "company_size"]
- `data/train.csv` (276830 bytes); columns: ["row_id", "experience_level", "employment_type", "job_title", "employee_residence", "remote_ratio", "company_location", "company_size", "salary_in_usd"]

## Public description

```
description.txt (52 lines)
sample_submission.csv (4075 lines)
test.csv (4075 lines)
train.csv (6040 lines)```

-> sample_submission.csv has 4074 rows and 2 columns.
Here is some information about the columns:
row_id (int64) has range: 6040.00 - 10113.00, 0 nan values
salary_in_usd (float64) has 1 unique values: [138350.0]

-> test.csv has 4074 rows and 8 columns.
Here is some information about the columns:
company_location (object) has 38 unique values. Some example values: ['US', 'CA', 'GB', 'DE']
company_size (object) has 3 unique values: ['L', 'M', 'S']
employee_residence (object) has 38 unique values. Some example values: ['US', 'CA', 'GB', 'DE']
employment_type (object) has 4 unique values: ['CT', 'FL', 'FT', 'PT']
experience_level (object) has 4 unique values: ['EN', 'EX', 'MI', 'SE']
job_title (object) has 106 unique values. Some example values: ['Data Scientist', 'Data Engineer', 'Data Analyst', 'Machine Learning Engineer']
remote_ratio (int64) has 3 unique values: [0, 100, 50]
row_id (int64) has range: 6040.00 - 10113.00, 0 nan values

-> train.csv has 6039 rows and 9 columns.
Here is some information about the columns:
company_location (object) has 76 unique values. Some example values: ['US', 'GB', 'CA', 'DE']
company_size (object) has 3 unique values: ['L', 'S', 'M']
employee_residence (object) has 87 unique values. Some example values: ['US', 'GB', 'CA', 'DE']
employment_type (object) has 4 unique values: ['CT', 'FT', 'PT', 'FL']
experience_level (object) has 4 unique values: ['EN', 'EX', 'MI', 'SE']
job_title (object) has 133 unique values. Some example values: ['Data Engineer', 'Data Scientist', 'Data Analyst', 'Machine Learning Engineer']
remote_ratio (int64) has 3 unique values: [100, 50, 0]
row_id (int64) has range: 1.00 - 6039.00, 0 nan values
salary_in_usd (int64) has range: 15000.00 - 750000.00, 0 nan values
