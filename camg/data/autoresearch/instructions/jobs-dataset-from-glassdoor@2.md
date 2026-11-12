# OpenMLE-fast task

Task ID: `jobs-dataset-from-glassdoor@2`

Native metric: `GlassdoorJobClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (858 bytes)
- `data/sample_submission.csv` (2215 bytes); columns: ["id", "job_simp"]
- `data/test.csv` (444332 bytes); columns: ["id", "Unnamed: 0", "Job Description", "Rating", "Company Name", "Location", "Headquarters", "Size", "Founded", "Type of ownership", "Industry", "Sector", "Revenue", "Competitors", "company_txt", "job_state", "same_state", "age", "python_yn", "R_yn", "spark", "aws", "excel", "seniority", "desc_len", "num_comp"]
- `data/train.csv` (1856425 bytes); columns: ["id", "Unnamed: 0", "Job Description", "Rating", "Company Name", "Location", "Headquarters", "Size", "Founded", "Type of ownership", "Industry", "Sector", "Revenue", "Competitors", "company_txt", "job_state", "same_state", "age", "python_yn", "R_yn", "spark", "aws", "excel", "seniority", "desc_len", "num_comp", "job_simp"]

## Public description

Job Role Classification from Glassdoor Descriptions (Tech Roles)

Problem statement:
Predict the simplified job role (job_simp) for a job posting using its description and company metadata. The target is one of six classes: analyst, data engineer, data scientist, director, manager, mle. The original job title and salary-related fields are not included to avoid label leakage.

Data description:
- train.csv: Each row is a job posting with features and the target label job_simp.
- test.csv: Same columns as train.csv except job_simp is hidden.
- sample_submission.csv: Example submission file with the required columns and valid labels.

Submission format:
- CSV with two columns: id, job_simp
- id values must exactly match those in test.csv; job_simp must be one of the six classes.

Evaluation:
- Metric: Macro-averaged F1 score across the six classes.
