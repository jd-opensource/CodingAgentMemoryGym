# OpenMLE-fast task

Task ID: `student-study-performance@1`

Native metric: `StudentStudyPerformanceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (813 bytes)
- `data/sample_submission.csv` (13168 bytes); columns: ["row_id", "math_score", "reading_score", "writing_score"]
- `data/test.csv` (11686 bytes); columns: ["row_id", "gender", "race_ethnicity", "parental_level_of_education", "lunch", "test_preparation_course"]
- `data/train.csv` (53623 bytes); columns: ["row_id", "gender", "race_ethnicity", "parental_level_of_education", "lunch", "test_preparation_course", "math_score", "reading_score", "writing_score"]

## Public description

Competition: Multi-Target Student Achievement Prediction

Problem statement:
Predict each student’s performance in three subjects—math_score, reading_score, and writing_score—using only pre-exam attributes: gender, race_ethnicity, parental_level_of_education, lunch, and test_preparation_course.

Public files (paths relative to the public/ directory):
- train.csv
- test.csv
- sample_submission.csv

Train.csv columns:
row_id, gender, race_ethnicity, parental_level_of_education, lunch, test_preparation_course, math_score, reading_score, writing_score

Test.csv columns:
row_id, gender, race_ethnicity, parental_level_of_education, lunch, test_preparation_course

Sample submission format:
row_id, math_score, reading_score, writing_score

Evaluation metric:
Macro RMSE across subjects (lower is better).
