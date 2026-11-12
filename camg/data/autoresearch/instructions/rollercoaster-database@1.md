# OpenMLE-fast task

Task ID: `rollercoaster-database@1`

Native metric: `RollerCoasterSpeedMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3620 bytes)
- `data/sample_submission.csv` (4178 bytes); columns: ["row_id", "speed_mph"]
- `data/test.csv` (32016 bytes); columns: ["row_id", "coaster_name", "Location", "Status", "Type_Main", "Manufacturer", "Model", "Designer", "Track layout", "Lift/launch system", "Restraints", "Restraint Style", "Park section", "height_ft", "drop_ft", "max_vertical_angle_deg", "Inversions_clean", "latitude", "longitude", "year_introduced", "height_restriction_in", "duration_seconds", "capacity_riders_per_hour"]
- `data/train.csv` (129889 bytes); columns: ["row_id", "coaster_name", "Location", "Status", "Type_Main", "Manufacturer", "Model", "Designer", "Track layout", "Lift/launch system", "Restraints", "Restraint Style", "Park section", "height_ft", "drop_ft", "max_vertical_angle_deg", "Inversions_clean", "latitude", "longitude", "year_introduced", "height_restriction_in", "duration_seconds", "capacity_riders_per_hour", "speed_mph"]
- `data/train_media/media_0000.jpg` (907076 bytes)

## Public description

Roller Coaster Speed Prediction Challenge

Problem statement
Estimate the maximum speed (in miles per hour) of roller coasters from their design, engineering system, context, and era. The dataset spans many decades and manufacturers, covering wooden and steel coasters, different lift/launch systems, layouts, and geographies. Your goal is to build a tabular ML model that generalizes across eras and designs to accurately predict speed_mph for a held-out test set.

Files provided
- train.csv: Feature columns plus the target column speed_mph, and a unique row_id per coaster.
- test.csv: Same feature columns and row_id, without speed_mph.
- sample_submission.csv: Example submission file with the required format (row_id, speed_mph) containing random but valid values.

Target
- speed_mph (numeric): Maximum speed of the roller coaster, standardized to miles per hour.

Features
The dataset combines geometry/design, system, context, and era features. Representative columns include:
- Geometry: height_ft, drop_ft (parsed from Drop), max_vertical_angle_deg (parsed from Max vertical angle), Inversions_clean.
- System/engineering: Lift/launch system, Type_Main (Wood/Steel/Other), Track layout, Restraints, Restraint Style.
- Maker/context: Manufacturer, Model, Designer, Status (Operating/Closed/Removed), Park section.
- Temporal: year_introduced (numeric; decade effects are common), optionally derived from opening_date_clean.
- Geographic: latitude, longitude.
- Operational constraints: height_restriction_in (parsed from Height restriction).
Additional helper numeric fields may be present (e.g., duration_seconds, capacity_riders_per_hour) when reliably parsed.

To ensure a fair and leakage-free task, speed-related raw fields and post-operational measurements are removed from the feature set (e.g., Speed, speed1, speed2, speed1_value, speed1_unit, G-force/Gforce_clean). The only speed information available to you is the target speed_mph in train.csv.

Evaluation
- Metric: Mean Absolute Error (MAE) on speed_mph.
- Your submission must be a CSV with two columns: row_id and speed_mph. The MAE is computed between your predicted speed_mph and the ground truth for matching row_id values in the test set.
- MAE is robust to outliers and directly interpretable (average mph error) across eras and build styles.

Data split
- A deterministic single split (approximately 80/20) is used for train/test. The split maintains diversity across material types and introduction decades to fairly evaluate generalization.

Expectations for participants
- Data processing: Handle messy text fields and units (angles in degrees, drops/heights in feet, restrictions in inches). Impute missing values appropriately.
- Feature engineering: Capture physics intuition (e.g., interactions among height, drop, angle, inversions) and categorical heterogeneity (manufacturer, layout, restraints). Consider temporal and geospatial context.
- Modeling: Train regression models (e.g., regularized linear models, tree ensembles, gradient boosting, tabular neural nets) with proper preprocessing. Carefully evaluate generalization.
- Leakage avoidance: Do not use speed-related raw fields or post-operational measurements as features.

Submission format
- CSV with columns: row_id, speed_mph.
- row_id must match the identifiers in test.csv; speed_mph must be numeric and finite.

Notes
- The feature set balances cleaned numeric fields and rich categorical/contextual information to create a challenging yet solvable task.
- External data is unnecessary; strong performance can be achieved via careful preprocessing and modeling.
