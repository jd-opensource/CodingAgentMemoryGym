# OpenMLE-fast task

Task ID: `top-10000-companies-india@1`

Native metric: `CompanyRatingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (898 bytes)
- `data/sample_submission.csv` (46650 bytes); columns: ["Id", "Rating"]
- `data/test.csv` (159283 bytes); columns: ["Id", "Name", "totalReviews", "Salaries", "Location", "theirService", "Jobs"]
- `data/train.csv` (670809 bytes); columns: ["Id", "Name", "totalReviews", "Salaries", "Location", "theirService", "Jobs", "Rating"]

## Public description

Title: Employee Rating Prediction for Top 10k Indian Companies (AmbitionBox 2025)

Overview:
Predict the continuous employee rating (approx. 1.0–5.0) for unseen Indian companies using metadata such as company name text, review counts, salaries, locations, industry/service type, and job openings.

Files (relative to public/):
- train.csv: Training data with target column 'Rating'. Columns: ['Id','Name','totalReviews','Salaries','Location','theirService','Jobs','Rating']
- test.csv: Test data without target column. Columns: ['Id','Name','totalReviews','Salaries','Location','theirService','Jobs']
- sample_submission.csv: Example submission with columns ['Id','Rating'] aligned to test.csv Ids

Submission Format:
- CSV with columns exactly ['Id','Rating']
- 'Id' must match and be aligned with public/test.csv
- 'Rating' should be a numeric prediction in the range ~[1.0, 5.0] (not enforced)
