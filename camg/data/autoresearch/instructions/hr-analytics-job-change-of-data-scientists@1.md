# OpenMLE-fast task

Task ID: `hr-analytics-job-change-of-data-scientists@1`

Native metric: `HRAnalyticsJobChangeMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1305 bytes)
- `data/sample_submission.csv` (37069 bytes); columns: ["enrollee_id", "target"]
- `data/test.csv` (370568 bytes); columns: ["enrollee_id", "city", "city_development_index", "gender", "relevent_experience", "enrolled_university", "education_level", "major_discipline", "experience", "company_size", "company_type", "last_new_job", "training_hours"]
- `data/train.csv` (1515289 bytes); columns: ["enrollee_id", "city", "city_development_index", "gender", "relevent_experience", "enrolled_university", "education_level", "major_discipline", "experience", "company_size", "company_type", "last_new_job", "training_hours", "target"]

## Public description

HR Analytics — Predicting Data Scientists’ Job-Change Intent

Problem statement
A data science training provider wants to anticipate which enrollees are actively seeking a new job. Given candidate demographics, education, employment history, and training behavior, predict the probability that a candidate is looking for a job change.

Public files and structure
- train.csv
  - Labeled training data. Contains the following columns:
    - enrollee_id (unique identifier)
    - city, city_development_index, gender, relevent_experience,
      enrolled_university, education_level, major_discipline, experience,
      company_size, company_type, last_new_job, training_hours
    - target (binary label: 0 or 1)

- test.csv
  - Unlabeled test data with the same feature columns as train.csv except it does not include target:
    - enrollee_id, city, city_development_index, gender, relevent_experience,
      enrolled_university, education_level, major_discipline, experience,
      company_size, company_type, last_new_job, training_hours

- sample_submission.csv
  - Example submission format. Must contain exactly two columns:
    - enrollee_id
    - target (predicted probability in [0, 1])
  - Your final submission should follow this exact format and include predictions for all IDs in test.csv.
