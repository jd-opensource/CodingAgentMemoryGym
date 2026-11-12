# OpenMLE-fast task

Task ID: `updated-electric-vehicles-spec-2025@1`

Native metric: `ElectricVehiclesAccelerationMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3201 bytes)
- `data/sample_submission.csv` (2841 bytes); columns: ["id", "acceleration_0_100_s"]
- `data/test.csv` (12960 bytes); columns: ["id", "brand", "top_speed_kmh", "battery_capacity_kWh", "number_of_cells", "torque_nm", "efficiency_wh_per_km", "range_km", "fast_charging_power_kw_dc", "fast_charge_port", "towing_capacity_kg", "cargo_volume_l", "seats", "drivetrain", "segment", "length_mm", "width_mm", "height_mm", "car_body_type"]
- `data/train.csv` (49999 bytes); columns: ["id", "brand", "top_speed_kmh", "battery_capacity_kWh", "number_of_cells", "torque_nm", "efficiency_wh_per_km", "range_km", "acceleration_0_100_s", "fast_charging_power_kw_dc", "fast_charge_port", "towing_capacity_kg", "cargo_volume_l", "seats", "drivetrain", "segment", "length_mm", "width_mm", "height_mm", "car_body_type"]

## Public description

Updated Electric Vehicles Acceleration Prediction Challenge

Background
0–100 km/h acceleration is a concise, widely used measure of EV performance. Spec sheets report powertrain, battery, efficiency, and dimensional attributes, but their relationship to straight-line acceleration is nonlinear. Predicting acceleration from these specifications helps benchmark EVs and illuminates engineering trade-offs.

Problem statement
Build a regression model that, given the specifications of an EV, predicts its 0–100 km/h acceleration time (seconds).

Files
- train.csv: Training data with target.
- test.csv: Test data without target.
- sample_submission.csv: A valid example submission file.

Target
- acceleration_0_100_s: Time in seconds to accelerate from 0 to 100 km/h.

Columns provided
- Numerical: top_speed_kmh, battery_capacity_kWh, number_of_cells, torque_nm, efficiency_wh_per_km, range_km, fast_charging_power_kw_dc, towing_capacity_kg, seats, length_mm, width_mm, height_mm.
- Categorical: brand, drivetrain, segment, car_body_type, fast_charge_port.
- id: A synthetic identifier for each row with no semantic meaning.
- Note on cargo_volume_l: This column contains numeric liters for many rows and non-numeric strings for some (e.g., "10 Banana Boxes"). You may parse numeric values and design a strategy for non-numeric entries (e.g., treat as missing, add a flag, or encode categorically).

Included and excluded information
- Excluded identifiers (e.g., model, source_url) are not present, preventing trivial lookups and label leakage.
- All data are tabular; there are no images or audio assets.

Recommended workflow (non-binding)
- Data processing: Cast numeric columns; clean/encode cargo_volume_l; ensure consistent handling of categorical features.
- Feature engineering: Encode categorical variables (e.g., one-hot or target-agnostic frequency encoding); consider interactions and optionally scale numerical features.
- Modeling: Train robust regressors for tabular data (e.g., gradient boosting, random forests, regularized linear models, or well-regularized neural networks).
- Validation: Use cross-validation on train.csv to tune hyperparameters; generate predictions for test.csv for final submission.

Evaluation
- Metric: Root Mean Squared Error (RMSE) on acceleration_0_100_s.
- Definition: RMSE = sqrt(mean((y_pred − y_true)^2)). Lower is better. Submissions with non-finite predictions are invalid.

Submission format
- CSV with header: id,acceleration_0_100_s
- Each id must appear exactly once and correspond to a row in test.csv. The order of rows in the submission does not matter; scoring aligns by id.
- Predictions must be finite numbers (floats).

Data split
- Deterministic 80/20 train/test split using stratification on binned acceleration values to preserve target distribution.
- The id column is synthetic and randomized; it conveys no semantics.

Deliverables recap
- train.csv: id, all features, and acceleration_0_100_s.
- test.csv: id and all features (no target).
- sample_submission.csv: id with plausible numeric acceleration_0_100_s values for all test rows.

Good luck building insightful, high-performing models for EV acceleration prediction!
