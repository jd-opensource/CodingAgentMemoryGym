# OpenMLE-fast task

Task ID: `obdii-ds3@1`

Native metric: `OBDIISpeedPredictionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2715 bytes)
- `data/sample_submission.csv` (292074 bytes); columns: ["id", "speed"]
- `data/test.csv` (820924 bytes); columns: ["id", "source", "vehicle_id", "barometric_pressure", "engine_coolant_temp", "fuel_level", "engine_load", "ambient_air_temp", "engine_rpm", "intake_manifold_pressure", "maf", "long_term_fuel_trim_bank2", "short_term_fuel_trim_bank2", "short_term_fuel_trim_bank1", "air_intake_temp", "fuel_pressure", "throttle_pos", "timing_advance", "equiv_ratio", "current_speed"]
- `data/train.csv` (3364940 bytes); columns: ["id", "source", "vehicle_id", "barometric_pressure", "engine_coolant_temp", "fuel_level", "engine_load", "ambient_air_temp", "engine_rpm", "intake_manifold_pressure", "maf", "long_term_fuel_trim_bank2", "short_term_fuel_trim_bank2", "short_term_fuel_trim_bank1", "air_intake_temp", "fuel_pressure", "throttle_pos", "timing_advance", "equiv_ratio", "current_speed", "speed"]

## Public description

Title: OBD-II Telemetry Next-Step Speed Prediction

Problem statement:
- Given a single-step sequence of OBD-II telemetry readings at time t, predict the vehicle speed at time t+1 (the very next record). Your model should generalize across heterogeneous drivers, vehicles and routes.

Data description:
- Tabular, time-ordered OBD-II telemetry collected from multiple experiments with varied drivers and conditions.
- Predictors include typical engine and intake signals (e.g., RPM, throttle position, manifold pressure, air and coolant temperatures, fuel trims, barometric pressure, mass air flow, equivalent ratio) and the current speed at time t.
- Each row belongs to one of three sources (source ∈ {exp1, exp2, exp3}). The final train and test files aggregate rows from all sources. A deterministic time-based split is used, ensuring each source contributes to both train and test.
- Target is the next-step speed (km/h) at time t+1. Features are taken from time t.

Files provided to participants:
- train.csv: Feature rows at time t with the target column "speed" representing speed at time t+1.
- test.csv: Feature rows at time t (no target column).
- sample_submission.csv: Example submission with the required format and plausible numeric values.

Columns:
- id: Unique identifier for each row.
- source: Categorical identifier for the originating source (exp1, exp2, exp3).
- current_speed and other numeric features: Engine and intake signals parsed into consistent numeric types across sources.
- speed (train.csv only): The next-step speed label.

Important details:
- Features are unified across sources by normalizing column names and converting units and European decimal formats into consistent numeric values.
- Rows are sorted by the best available ordering column per source before constructing next-step labels.
- The split is chronological within each source (first 80% train, last 20% test), preventing leakage.

Evaluation metric:
- Root Mean Squared Error (RMSE), computed separately for each source and macro-averaged across sources:
  - For each source ∈ {exp1, exp2, exp3}: RMSE_source = sqrt(mean((y_pred − y_true)^2)).
  - Final score = (RMSE_exp1 + RMSE_exp2 + RMSE_exp3) / 3.
- This macro-average avoids domination by any single source and yields a fair, precise assessment across distinct operating conditions.

Notes for participants:
- You are encouraged to perform robust data cleaning and feature engineering (e.g., lag features, deltas, per-source normalization), and to handle missing values appropriately.
- Sequence models (RNN/GRU/LSTM/Transformers) or tree-based methods with engineered lags are sensible approaches. Ensure no leakage by respecting temporal order.
