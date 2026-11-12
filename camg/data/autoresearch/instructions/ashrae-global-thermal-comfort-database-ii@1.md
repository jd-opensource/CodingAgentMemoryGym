# OpenMLE-fast task

Task ID: `ashrae-global-thermal-comfort-database-ii@1`

Native metric: `ThermalComfortMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3454 bytes)
- `data/sample_submission.csv` (288792 bytes); columns: ["row_id", "Thermal sensation"]
- `data/test.csv` (3412583 bytes); columns: ["Year", "Season", "Koppen climate classification", "Climate", "City", "Country", "Building type", "Cooling startegy_building level", "Cooling startegy_operation mode for MM buildings", "Heating strategy_building level", "Age", "Sex", "PMV", "PPD", "SET", "Clo", "Met", "activity_10", "activity_20", "activity_30", "activity_60", "Air temperature (C)", "Ta_h (C)", "Ta_m (C)", "Ta_l (C)", "Operative temperature (C)", "Radiant temperature (C)", "Globe temperature (C)", "Tg_h (C)", "Tg_m (C)", "Tg_l (C)", "Relative humidity (%)", "Air velocity (m/s)", "Velocity_h (m/s)", "Velocity_m (m/s)", "Velocity_l (m/s)", "Subject«s height (cm)", "Subject«s weight (kg)", "Blind (curtain)", "Fan", "Window", "Door", "Heater", "Outdoor monthly air temperature (C)", "row_id"]
- `data/train.csv` (16668639 bytes); columns: ["Year", "Season", "Koppen climate classification", "Climate", "City", "Country", "Building type", "Cooling startegy_building level", "Cooling startegy_operation mode for MM buildings", "Heating strategy_building level", "Age", "Sex", "PMV", "PPD", "SET", "Clo", "Met", "activity_10", "activity_20", "activity_30", "activity_60", "Air temperature (C)", "Ta_h (C)", "Ta_m (C)", "Ta_l (C)", "Operative temperature (C)", "Radiant temperature (C)", "Globe temperature (C)", "Tg_h (C)", "Tg_m (C)", "Tg_l (C)", "Relative humidity (%)", "Air velocity (m/s)", "Velocity_h (m/s)", "Velocity_m (m/s)", "Velocity_l (m/s)", "Subject«s height (cm)", "Subject«s weight (kg)", "Blind (curtain)", "Fan", "Window", "Door", "Heater", "Outdoor monthly air temperature (C)", "row_id", "Thermal sensation"]

## Public description

Title: Predicting Occupant Thermal Sensation from Real Buildings Worldwide

Overview
Build a model that predicts an occupant’s reported thermal sensation given instrumented indoor conditions, contextual metadata, clothing/activity, and relevant outdoor signals. The target is the ASHRAE thermal sensation vote treated as a numeric value. Models should generalize across studies, cities, and climates.

Data
Each row represents a paired observation: an occupant’s survey response collected simultaneously with indoor environmental measurements and context. Feature columns include, when available:
- Indoor thermal/comfort indices: PMV, PPD, SET
- Clothing and activity: Clo, Met, activity durations
- Temperatures: Air temperature (C), Ta_h/m/l (C), Operative temperature (C), Radiant temperature (C), Globe temperature (C), Tg_h/m/l (C)
- Moisture and airflow: Relative humidity (%), Air velocity (m/s), Velocity_h/m/l (m/s)
- Outdoor context: Outdoor monthly air temperature (C)
- Building/context metadata: Season, Koppen climate classification, Climate, City, Country, Building type, cooling/heating strategies
- Occupant controls and actions: Blind (curtain), Fan, Window, Door, Heater
- Anthropometrics when available: subject height (cm), subject weight (kg)

Notes
- Features may contain missing values; do not assume completeness. SI units are used (Celsius, m/s, %). Redundant Fahrenheit and fpm columns have been removed.
- Subjective survey outcomes other than the target are excluded to prevent label leakage and reflect realistic prediction scenarios.

Files
- train.csv: Features plus the numeric target column Thermal sensation and a row_id column.
- test.csv: Features only plus a row_id column.
- sample_submission.csv: A template with row_id and Thermal sensation filled with random but valid values. Replace Thermal sensation with your predictions for the rows in test.csv.

Target
- Thermal sensation (numeric), typically in the range [-3, 3]. Use the numeric values directly; do not discretize.

Evaluation
- Metric: Mean Absolute Error (MAE).
- Computation: MAE between submitted Thermal sensation predictions and the hidden ground truth for the rows in test.csv. Lower is better.
- Submission requirements:
  - Provide a CSV containing exactly two columns: row_id and Thermal sensation.
  - Include one prediction per row_id present in test.csv. The set and order of row_id must match test.csv; duplicates or missing/extra row_ids are invalid.
  - Predictions must be numeric and finite. No clipping is required; MAE is computed directly.

Train/test split
The test set consists of entire held-out studies to enforce distribution shift and realistic generalization. Train contains the target; test does not. The row_id provides a stable alignment for test.csv and submissions.

Guidance
- Robustly handle missing values; do not drop rows solely due to missing features when the target is present in train.
- Encode categorical features (e.g., Season, climate classes, City, Country, Building type, cooling/heating strategies) appropriately.
- Consider physics-informed features and aggregates (e.g., combining multiple sensor heights) during feature engineering.
- Use ML techniques suited for tabular data and mixed types (e.g., gradient boosting, regularized linear models, deep tabular models). Ensure numerical stability throughout to avoid NaN/Inf.

Final competition files
- train.csv
- test.csv
- sample_submission.csv
