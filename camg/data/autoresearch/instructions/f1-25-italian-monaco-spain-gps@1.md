# OpenMLE-fast task

Task ID: `f1-25-italian-monaco-spain-gps@1`

Native metric: `F1NextLapTimeENMAEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2989 bytes)
- `data/sample_submission.csv` (36335 bytes); columns: ["row_id", "next_lap_time"]
- `data/test.csv` (126819 bytes); columns: ["row_id", "event", "driver_abbr", "team", "lap_number", "position", "time_from_start_sec", "lap_time_t_sec", "sector1_t_sec", "sector2_t_sec", "sector3_t_sec", "pitted_on_t", "next_is_outlap", "stint_number", "laps_since_last_stop", "grid_position", "q1_sec", "q2_sec", "q3_sec"]
- `data/train.csv` (297386 bytes); columns: ["row_id", "event", "driver_abbr", "team", "lap_number", "position", "time_from_start_sec", "lap_time_t_sec", "sector1_t_sec", "sector2_t_sec", "sector3_t_sec", "pitted_on_t", "next_is_outlap", "stint_number", "laps_since_last_stop", "grid_position", "q1_sec", "q2_sec", "q3_sec", "next_lap_time"]

## Public description

F1 Next-Lap Time Forecasting across Three European GPs

Overview
Build a model that, given a driver’s race context up to lap t, predicts their lap time at t+1 (in seconds). Data comes from three 2025 Grands Prix. The split is by event to test cross-circuit generalization.

Files in public/
- train.csv: Modeling table with features available up to and including lap t, plus the target next_lap_time.
- test.csv: Same columns as train.csv except next_lap_time is withheld.
- sample_submission.csv: An example submission containing row_id and next_lap_time.

Task
- Problem type: Regression.
- Target: next_lap_time = the driver’s lap time at t+1 (in seconds).
- Each row represents a driver-lap at lap t with only information available up to t.
- Final laps and any t without t+1 are excluded from the modeling tables.

Submission format
- CSV with exactly two columns, in this order:
  • row_id: matches test.csv row_id values and order exactly
  • next_lap_time: predicted lap time in seconds (float, finite, > 0)
- row_id format: "{event}_{driver_abbr}_{lap_number}" (lowercase event, underscores only).

Columns in train.csv and test.csv
- row_id: unique identifier for the driver-lap row at lap t
- event: categorical event identifier (Italy, Monaco, Spain)
- driver_abbr: driver abbreviation (e.g., VER)
- team: team name aligned with the driver at this event
- lap_number: integer lap index t
- position: car’s on-track position at lap t
- time_from_start_sec: race clock at end of lap t (seconds)
- lap_time_t_sec: lap t time in seconds
- sector1_t_sec, sector2_t_sec, sector3_t_sec: sector times for lap t (seconds; may be missing)
- pitted_on_t: 1 if a pit stop is recorded on lap t, else 0
- next_is_outlap: 1 if lap t+1 is an out-lap (derived from pitted_on_t), else 0
- stint_number: integer stint index as of lap t (first stint = 1)
- laps_since_last_stop: laps since the previous pit stop ended, at lap t (0 on an out-lap)
- grid_position: starting grid position
- q1_sec, q2_sec, q3_sec: qualifying times in seconds (may be missing)
- next_lap_time: only in train.csv (the target)

Evaluation
- Metric: Event-Normalized Mean Absolute Error (EN-MAE).
  • Let y_i be the true next_lap_time and ŷ_i your prediction for row i.
  • For an event e, define M_e as the median next-lap time (in seconds) for that event in the evaluation set.
  • Each row’s error is normalized by its event’s median: e_i' = |y_i − ŷ_i| / M_event(i).
  • EN-MAE is the mean of e_i' across all rows (lower is better).

Official split
- Train: Italy + Monaco events.
- Test: Spain event.

Notes
- Features are constructed using data available up to and including lap t. No future information beyond t is used.
- Laps that are in-laps or out-laps are kept; pitted_on_t and next_is_outlap allow models to learn strategy-related pace changes.
- Drivers present in the test set also appear in the training set at least once; the challenge is to generalize to a different circuit.
