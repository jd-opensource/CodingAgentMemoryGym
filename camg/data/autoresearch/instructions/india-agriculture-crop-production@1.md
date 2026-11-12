# OpenMLE-fast task

Task ID: `india-agriculture-crop-production@1`

Native metric: `IndiaCropProductionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2234 bytes)
- `data/sample_submission.csv` (216304 bytes); columns: ["row_id", "Production"]
- `data/test.csv` (977699 bytes); columns: ["row_id", "State", "District", "Crop", "Season", "YearStart", "Area"]
- `data/train.csv` (16868199 bytes); columns: ["State", "District", "Crop", "Season", "YearStart", "Area", "Production"]

## Public description

Title: India District–Crop Production Forecasting

Problem statement
Accurately forecast agricultural output by predicting Production (tonnes) for district–crop–season combinations across India using historical tabular records. Each row corresponds to a specific State, District, Crop, Season, YearStart (parsed from Year), and sown Area (hectares). The task is to generalize across regions, crops, seasons, and time to produce reliable forecasts for the held-out year.

Files provided (all under public/)
- train.csv: Training features and target for years up to 2018.
- test.csv: Test features for year 2019 (target withheld). Includes a row_id column that uniquely identifies each test row.
- sample_submission.csv: Example submission file in the correct format.
- description.txt: This description file.

Columns
- State: State/Union Territory name
- District: District name
- Crop: Crop name
- Season: Season name (e.g., Kharif, Rabi, Whole Year, Summer, Winter, Autumn)
- YearStart: Numeric start year parsed from the Year field (e.g., "2014-15" → 2014)
- Area: Sown area in hectares (non-negative numeric)
- Production: Target variable (tonnes). Present only in train.csv and required in submissions.

Data notes and preprocessing
- Units are consistent: Production is in Tonnes and Area is in Hectares.
- The original Yield column is excluded to prevent label leakage (it is derived from Area and Production).
- Rows with missing essential fields were removed. Rows with Production = 0 are retained to reflect real-world failures.

Train/Test split
- Train: YearStart ≤ 2018
- Test: YearStart = 2019
The time-based split mirrors real forecasting, requiring extrapolation to the next season while leveraging historical context.

Submission format
- Create a CSV with exactly two columns: row_id and Production
- row_id must exactly match the IDs in test.csv (order does not matter)
- Production must be a non-negative numeric value for every row_id

Evaluation metric
- Root Mean Squared Logarithmic Error (RMSLE) on Production (tonnes)
- Definition: sqrt(mean((log1p(y_true) − log1p(y_pred))^2))
RMSLE emphasizes relative accuracy across a wide target range, is robust to heavy tails, and handles zeros via log1p.
