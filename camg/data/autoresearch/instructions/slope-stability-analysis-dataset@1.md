# OpenMLE-fast task

Task ID: `slope-stability-analysis-dataset@1`

Native metric: `SlopeStabilityCMAEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2905 bytes)
- `data/sample_submission.csv` (51108 bytes); columns: ["Id", "FS"]
- `data/test.csv` (260765 bytes); columns: ["Id", "unit_weight", "cohesion", "friction_angle_deg", "slope_angle_deg", "slope_height_m", "pwp_ratio", "reinforcement_type"]
- `data/train.csv` (1123689 bytes); columns: ["Id", "unit_weight", "cohesion", "friction_angle_deg", "slope_angle_deg", "slope_height_m", "pwp_ratio", "reinforcement_type", "FS"]

## Public description

Censor-Aware Slope Stability Prediction (FS)

Overview
Predict the Factor of Safety (FS) for slopes from geotechnical parameters and reinforcement type. Many ground-truth labels are capped at 3.0, meaning they are right-censored: when FS = 3.0, the true value is at least 3.0 but not exactly known. Your task is to build models that handle this censoring properly while providing accurate predictions.

Files provided
- train.csv: Training data with features and the target column FS.
- test.csv: Test data with the same features and an Id column; FS is withheld.
- sample_submission.csv: Example submission file with the required format (Id, FS).

Data description
Each row corresponds to one slope design scenario. Columns in train.csv and test.csv:
- Id: Unique identifier for each row.
- unit_weight: Unit Weight of soil/rock (kN/m^3).
- cohesion: Cohesion (kPa).
- friction_angle_deg: Internal Friction Angle (degrees).
- slope_angle_deg: Slope Angle (degrees).
- slope_height_m: Slope Height (meters).
- pwp_ratio: Pore Water Pressure Ratio (dimensionless).
- reinforcement_type: Type of slope reinforcement (categorical string; values include Drainage, Geosynthetics, Retaining Wall, Soil Nailing).
- FS: Target variable (only in train.csv). FS < 1 implies unstable; FS >= 1 implies stable. Many values are exactly 3.0, which indicates censoring (true FS >= 3.0).

Notes
- The Reinforcement Numeric column from the source data is intentionally omitted to avoid redundant encodings of reinforcement type.
- No missing values are expected; units are preserved.

Evaluation metric
Censored Mean Absolute Error (C-MAE)
- For uncensored points (FS < 3.0): loss = |prediction − FS|.
- For censored points (FS = 3.0): loss = max(0, 3.0 − prediction). Predictions ≥ 3.0 incur zero loss on censored rows, but may incur loss on uncensored rows.
The final score is the mean loss over all test rows. Lower is better.

Why this metric?
- It respects the partial information in capped labels: where FS is known precisely, standard MAE applies; where FS is right-censored at 3.0, predictions are only penalized for underestimating the lower bound.

Modeling tips
- This is a tabular regression task with right-censoring. Gradient-boosted trees, random forests, and neural networks can work well.
- Handle the categorical reinforcement_type appropriately (e.g., one-hot encoding). Feature scaling may benefit linear/NN models but is optional for trees.
- Consider censor-aware techniques (e.g., custom loss approximating the metric, Tobit-style modeling, or post-processing to avoid underpredicting clearly censored cases). Calibrate carefully: overpredicting on uncensored rows increases loss.

Submission format
- A CSV with two columns and a header:
  - Id
  - FS
- Id values must match those in test.csv exactly (one prediction per row). FS must be numeric and finite. No additional columns are allowed.
