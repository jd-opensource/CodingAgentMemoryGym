# OpenMLE-fast task

Task ID: `mental-health-dataset@2`

Native metric: `MentalHealthTreatmentMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (623 bytes)
- `data/sample_submission.csv` (1514036 bytes); columns: ["row_id", "treatment"]
- `data/test.csv` (6351505 bytes); columns: ["row_id", "Timestamp", "Gender", "Country", "Occupation", "self_employed", "family_history", "Days_Indoors", "Growing_Stress", "Changes_Habits", "Mental_Health_History", "Mood_Swings", "Coping_Struggles", "Work_Interest", "Social_Weakness", "mental_health_interview", "care_options"]
- `data/train.csv` (25870083 bytes); columns: ["row_id", "Timestamp", "Gender", "Country", "Occupation", "self_employed", "family_history", "Days_Indoors", "Growing_Stress", "Changes_Habits", "Mental_Health_History", "Mood_Swings", "Coping_Struggles", "Work_Interest", "Social_Weakness", "mental_health_interview", "care_options", "treatment"]

## Public description

Screen Time Impact on Mental Health — Treatment Prediction Challenge

Files:
- train.csv: Training data with features and binary target `treatment` (0/1).
- test.csv: Test data with the same features as train, without `treatment`.
- sample_submission.csv: Example of a valid submission with columns [row_id, treatment].

Target
- treatment: 1 if the respondent reports receiving treatment, 0 otherwise.

Evaluation
- Binary Log Loss on the probability for treatment=1. Lower is better.

Submission format
- CSV with columns [row_id, treatment], one row per row_id in test.csv;
  treatment must be a probability in [0,1].
