# OpenMLE-fast task

Task ID: `data-scientist-salary-us-glassdoor@1`

Native metric: `GlassdoorIndustryClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (657 bytes)
- `data/sample_submission.csv` (4630 bytes); columns: ["Id", "Industry"]
- `data/test.csv` (644591 bytes); columns: ["index", "Job Title", "Salary Estimate", "Job Description", "Rating", "Company Name", "Location", "Headquarters", "Size", "Founded", "Type of ownership", "Revenue", "Competitors", "Hourly", "Employer provided", "Lower Salary", "Upper Salary", "Avg Salary(K)", "company_txt", "Job Location", "Age", "Id"]
- `data/train.csv` (2426453 bytes); columns: ["index", "Job Title", "Salary Estimate", "Job Description", "Rating", "Company Name", "Location", "Headquarters", "Size", "Founded", "Type of ownership", "Revenue", "Competitors", "Hourly", "Employer provided", "Lower Salary", "Upper Salary", "Avg Salary(K)", "company_txt", "Job Location", "Age", "Id", "Industry"]

## Public description

Competition: Glassdoor Industry Classification from US Data Scientist Job Postings

Data files in public/:
- train.csv: Id + input features + Industry (target).
- test.csv: Id + input features (no Industry).
- sample_submission.csv: Id + Industry (predictions for each test Id).

Notes:
- Id is a stable identifier and should not be used as a predictive feature.
- Several engineered/leakage-prone columns are excluded from features (e.g., Sector, Python, spark, aws, excel, sql, sas, keras, pytorch, scikit, tensor, hadoop, tableau, bi, flink, mongo, google_an, job_title_sim, seniority_by_title, Degree).
- Evaluation uses Macro-F1 over Industry classes.
