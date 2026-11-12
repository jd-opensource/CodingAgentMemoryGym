# OpenMLE-fast task

Task ID: `physics-teacher-jobs-linkedin@2`

Native metric: `PhysicsTeacherJobsMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (760 bytes)
- `data/sample_submission.csv` (2127 bytes); columns: ["id", "employment_type"]
- `data/test.csv` (652607 bytes); columns: ["id", "title", "location", "publishedAt", "companyName", "description", "applicationsCount", "experienceLevel", "workType", "sector", "salary"]
- `data/train.csv` (2566826 bytes); columns: ["id", "title", "location", "publishedAt", "companyName", "description", "applicationsCount", "experienceLevel", "workType", "sector", "salary", "employment_type"]

## Public description

Title: Physics Teacher Employment Type Classification

Background
School districts and job seekers care whether roles are full-time, part-time, or alternative arrangements. Employment type is often implicit in job titles and descriptions.

Problem Statement
Predict the employment type for each posting among three classes: Full-time, Part-time, Other.

Files
- train.csv: Features and the employment_type label
- test.csv: Features only (no labels)
- sample_submission.csv: Example submission file with columns [id, employment_type]

Submission Format
Upload a CSV with two columns: id, employment_type (values in {Full-time, Part-time, Other}).
The id values must match those in test.csv.

Evaluation Metric
Macro-averaged F1 score across the three classes.
