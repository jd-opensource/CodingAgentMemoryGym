# OpenMLE-fast task

Task ID: `covid-19-clinical-trials-data@2`

Native metric: `CovidClinicalTrialsStatusMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (699 bytes)
- `data/sample_submission.csv` (33219 bytes); columns: ["NCT Number", "Status"]
- `data/test.csv` (1361441 bytes); columns: ["NCT Number", "Titl", "Acrony", "Study Result", "Condition", "Intervention", "Outcome Measure", "Sponsor/Collaborator", "Gende", "Ag", "Phase", "Enrollmen", "Funded By", "Study Typ", "Study Design", "Start Dat", "First Poste", "Last Update Poste", "Location", "Other IDs"]
- `data/train.csv` (5407792 bytes); columns: ["NCT Number", "Status", "Titl", "Acrony", "Study Result", "Condition", "Intervention", "Outcome Measure", "Sponsor/Collaborator", "Gende", "Ag", "Phase", "Enrollmen", "Funded By", "Study Typ", "Study Design", "Start Dat", "First Poste", "Last Update Poste", "Location", "Other IDs"]

## Public description

```
description.txt (45 lines)
sample_submission.csv (1154 lines)
test.csv (1154 lines)
train.csv (4631 lines)```

-> sample_submission.csv has 1153 rows and 2 columns.
The columns are: NCT Number, Status

-> test.csv has 1153 rows and 20 columns.
The columns are: NCT Number, Titl, Acrony, Study Result, Condition, Intervention, Outcome Measure, Sponsor/Collaborator, Gende, Ag, Phase, Enrollmen, Funded By, Study Typ, Study Design... and 5 more columns

-> train.csv has 4630 rows and 21 columns.
The columns are: NCT Number, Status, Titl, Acrony, Study Result, Condition, Intervention, Outcome Measure, Sponsor/Collaborator, Gende, Ag, Phase, Enrollmen, Funded By, Study Typ... and 6 more columns
