# OpenMLE-fast task

Task ID: `crop-production-statistics-india@1`

Native metric: `CropProductionRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (676 bytes)
- `data/sample_submission.csv` (772160 bytes); columns: ["row_id", "Production"]
- `data/test.csv` (3101575 bytes); columns: ["row_id", "State", "District", "Crop", "Crop_Year", "Season", "Area"]
- `data/train.csv` (17896973 bytes); columns: ["row_id", "State", "District", "Crop", "Crop_Year", "Season", "Area", "Production"]

## Public description

Competition: India District–Crop–Season Production Prediction (1997–2020)

Files in this directory
- train.csv: Training data with features and the target Production.
- test.csv: Test data with the same features as train.csv but without Production.
- sample_submission.csv: Example submission with the required columns (row_id, Production).

Columns
- row_id: Unique identifier for each row.
- State, District, Crop, Season: Categorical descriptors.
- Crop_Year: Year of the observation.
- Area: Sown area for that row.
- Production: Target variable (present in train.csv only).

Evaluation
- Submissions are evaluated using RMSLE between predicted and true Production.
