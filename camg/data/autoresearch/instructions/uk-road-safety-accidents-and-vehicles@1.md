# OpenMLE-fast task

Task ID: `uk-road-safety-accidents-and-vehicles@1`

Native metric: `UKRoadSafetySeverityMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (466 bytes)
- `data/sample_submission.csv` (122921 bytes); columns: ["row_id", "Slight", "Serious", "Fatal"]
- `data/test.csv` (357813 bytes); columns: ["Year", "Speed_limit", "Day_of_Week", "Road_Type", "Light_Conditions", "Weather_Conditions", "Road_Surface_Conditions", "Urban_or_Rural_Area", "Junction_Control", "Junction_Detail", "1st_Road_Class", "2nd_Road_Class", "Latitude", "Longitude", "hour", "month", "is_weekend", "row_id"]
- `data/train.csv` (1958776 bytes); columns: ["Year", "Speed_limit", "Day_of_Week", "Road_Type", "Light_Conditions", "Weather_Conditions", "Road_Surface_Conditions", "Urban_or_Rural_Area", "Junction_Control", "Junction_Detail", "1st_Road_Class", "2nd_Road_Class", "Latitude", "Longitude", "hour", "month", "is_weekend", "target", "row_id"]

## Public description

Title: UK Collision Severity Prediction (2005–2016)

Files in this directory:
- train.csv: training features and target (column 'target' in {Slight, Serious, Fatal})
- test.csv: test features with identifier 'row_id' (no target column)
- sample_submission.csv: example submission with columns [row_id, Slight, Serious, Fatal]

Submission format:
CSV with columns [row_id, Slight, Serious, Fatal]; probabilities must be numeric, non-negative, and sum to 1 per row.
