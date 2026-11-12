# OpenMLE-fast task

Task ID: `f1-25-canada-austria-uk-gps@1`

Native metric: `F1NextLapTimeMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2509 bytes)
- `data/sample_submission.csv` (17835 bytes); columns: ["row_id", "lap_time_next_sec"]
- `data/test.csv` (86690 bytes); columns: ["row_id", "driver", "lap_number_t", "position_t", "lap_time_t_sec", "sector1_t_sec", "sector2_t_sec", "sector3_t_sec", "cumulative_time_t_sec", "pit_in_flag", "pit_out_flag", "stops_so_far", "q1_time", "q2_time", "q3_time", "qualifying_pos", "grid_position", "race_round", "race_name", "country"]
- `data/train.csv` (291901 bytes); columns: ["row_id", "driver", "lap_number_t", "position_t", "lap_time_t_sec", "sector1_t_sec", "sector2_t_sec", "sector3_t_sec", "cumulative_time_t_sec", "pit_in_flag", "pit_out_flag", "stops_so_far", "q1_time", "q2_time", "q3_time", "qualifying_pos", "grid_position", "race_round", "race_name", "country", "lap_time_next_sec"]

## Public description

F1 Next-Lap Time Forecasting (Canada + Austria → UK)

Problem statement
- Predict a driver’s next lap time in seconds. For each row, you are given lap-level information available at lap t; your task is to forecast the lap time at t+1. This is a time-series regression challenge designed to evaluate cross-circuit generalization.

Data provided
- train.csv: aligned lap-level features from Canada and Austria Grands Prix, with the target column lap_time_next_sec.
- test.csv: aligned lap-level features from the UK Grand Prix without labels, including a unique row_id.
- sample_submission.csv: example of the required submission format.

How the alignment works
- For each driver sequence, the features at lap t are paired with the label (next lap time) at lap t+1.
- The last lap of each driver (no next-lap label) is excluded.

Feature columns (in train.csv and test.csv)
- driver: driver abbreviation.
- lap_number_t: current lap number.
- position_t: current race position.
- lap_time_t_sec: current lap time (seconds).
- sector1_t_sec, sector2_t_sec, sector3_t_sec: current lap sector times (seconds; may be missing on some laps).
- cumulative_time_t_sec: driver’s cumulative race time at the end of lap t (seconds).
- pit_in_flag, pit_out_flag: binary flags indicating a pit-in or pit-out event on lap t.
- stops_so_far: cumulative count of pit-ins up to lap t.
- q1_time, q2_time, q3_time: qualifying session times (seconds; missing if not applicable),
- qualifying_pos: qualifying position (integer; large value if missing),
- grid_position: starting grid position.
- race_round, race_name, country: event metadata.
- lap_time_next_sec: the target (only in train.csv).

Submission format
- A single CSV file with exactly two columns:
  - row_id: matches the row_id in test.csv.
  - lap_time_next_sec: a non-negative, finite float in seconds.

Evaluation metric
- Driver-averaged Mean Absolute Error (MAE), measured in seconds:
  - Compute MAE for each driver across their test rows, then macro-average over drivers.
  - This balances drivers with different numbers of laps while remaining interpretable and robust.

Guidance
- Effective solutions will combine feature engineering (rolling aggregates across recent laps, pace deltas, pit effects) with robust regression models (e.g., gradient boosting, temporal neural nets).
- Handle missing sector splits carefully and ensure predictions are non-negative and finite.
- You may use any ML technique; cross-validation on train.csv is recommended.
