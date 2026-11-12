# OpenMLE-fast task

Task ID: `f1-25-australia-bahrain-saudi-arabia-miami-gps@1`

Native metric: `F1NextLapTimeMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3569 bytes)
- `data/sample_submission.csv` (25521 bytes); columns: ["row_id", "next_lap_time_seconds"]
- `data/test.csv` (144039 bytes); columns: ["row_id", "event_name", "driver", "team", "lap_number", "position_t", "session_time_seconds", "sector1_seconds", "sector2_seconds", "sector3_seconds", "lap_time_t_seconds", "prev_lap_time_seconds", "prev2_lap_time_seconds", "rolling_mean_3", "rolling_std_3", "stops_so_far_t", "lap_in_stint_t", "grid_position"]
- `data/train.csv` (505695 bytes); columns: ["row_id", "event_name", "driver", "team", "lap_number", "position_t", "session_time_seconds", "sector1_seconds", "sector2_seconds", "sector3_seconds", "lap_time_t_seconds", "prev_lap_time_seconds", "prev2_lap_time_seconds", "rolling_mean_3", "rolling_std_3", "stops_so_far_t", "lap_in_stint_t", "grid_position", "next_lap_time_seconds"]

## Public description

F1-25 Next-Lap Lap Time Forecasting (Cross-circuit)

Problem statement
You are given per-lap timing data from four 2025 Formula 1 Grands Prix (Australia, Bahrain, Saudi Arabia, USA/Miami). At the end of lap t for a given driver within an event, predict the total lap time for lap t+1 (in seconds). Your model should generalize across circuits, strategies, and race phases.

Data
Each row represents a driver-event-lap “state” at lap t. The target is the next lap’s total time at t+1 for the same driver within the same event.

Provided files
- train.csv: Features at lap t and the target next_lap_time_seconds for multiple events (Australia, Bahrain, Saudi Arabia).
- test.csv: Features at lap t for the held-out event (USA/Miami). The target for these rows is hidden.
- sample_submission.csv: A valid example submission containing row_id and predicted next_lap_time_seconds.

Columns
- row_id: Unique identifier for each sample. This must be used to align your predictions with the test set.
- event_name: Event identifier string.
- driver: Driver abbreviation (e.g., VER, NOR).
- team: Team name string.
- lap_number: Current lap number t (integer).
- position_t: Running position at the end of lap t (integer, may contain missing values for some laps due to timing gaps).
- session_time_seconds: Session clock time for lap t (seconds since session start; float).
- sector1_seconds, sector2_seconds, sector3_seconds: Sector split times for lap t in seconds (floats; may be missing).
- lap_time_t_seconds: Total lap time at lap t in seconds (float; may be missing for a small number of laps).
- prev_lap_time_seconds, prev2_lap_time_seconds: Previous laps’ total times (floats; may be missing early in a stint).
- rolling_mean_3, rolling_std_3: Rolling mean and standard deviation of lap times over the last up to 3 laps, computed per driver within an event and including lap t (floats; may be partially missing early on).
- stops_so_far_t: Number of pit stops completed up to and including lap t (integer).
- lap_in_stint_t: Laps since the most recent pit stop up to lap t (integer; starts at 1 at race start and first lap after a stop).
- grid_position: Qualifying result grid position for the driver (float; may be missing for drivers without a set time).
- target (train only): next_lap_time_seconds, the label your model must predict.

Task
Train a model using train.csv to predict next_lap_time_seconds for rows in test.csv. Your submission must provide one prediction per row_id.

Evaluation
Primary metric: Mean Absolute Error (MAE), computed in seconds between your predictions and the ground truth next_lap_time_seconds for the test set. Lower is better.

Submission format
- CSV with the following columns and header:
  - row_id: exactly matching the row_id values provided in test.csv
  - next_lap_time_seconds: your predicted value (must be a finite number)

Notes
- The split is event-based to emphasize cross-circuit generalization. Test rows come only from the USA/Miami event, while train rows come from Australia, Bahrain, and Saudi Arabia.
- The tabular features reflect only information available up to and including lap t to avoid future leakage with respect to t+1.
- Timing fields are parsed to seconds. Missing sector splits or intermediate fields may occur due to official feed gaps; robust feature engineering or modeling strategies are encouraged.
- You may create additional features, apply time-series models, gradient boosting, or deep learning approaches. There is no runtime constraint; focus on accuracy and sound methodology.
