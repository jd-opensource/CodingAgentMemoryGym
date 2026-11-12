# OpenMLE-fast task

Task ID: `f1-25-italian-monaco-spain-gps@2`

Native metric: `PitStopLogLossMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2919 bytes)
- `data/raw_test/drivers_round_9.csv` (1110 bytes); columns: ["Number", "Driver ID", "Abbreviation", "First Name", "Last Name", "Full Name", "Team"]
- `data/raw_test/lap_times_round_9.csv` (153931 bytes); columns: ["Driver", "Lap Number", "Lap Time", "Position", "Time", "Sector 1", "Sector 2", "Sector 3"]
- `data/raw_test/qualifying_round_9.csv` (1962 bytes); columns: ["Abbreviation", "Driver ID", "Full Name", "Team", "Q1 Time", "Q2 Time", "Q3 Time", "Position"]
- `data/raw_test/race_results_round_9.csv` (5366 bytes); columns: ["DriverNumber", "BroadcastName", "Abbreviation", "DriverId", "TeamName", "TeamColor", "TeamId", "FirstName", "LastName", "FullName", "HeadshotUrl", "CountryCode", "Position", "ClassifiedPosition", "GridPosition", "Q1", "Q2", "Q3", "Time", "Status", "Points"]
- `data/raw_test/race_status_round_9.csv` (553 bytes); columns: ["Abbreviation", "Full Name", "Status"]
- `data/raw_test/races_data_2025_roundref_9.csv` (3592 bytes); columns: ["Round", "Event Name", "Official Event Name", "Location", "Country", "First Session", "Last Session"]
- `data/raw_test/season_data_2025_roundref_9.csv` (2375 bytes); columns: ["Round", "Event Name", "Location", "Country", "First Session", "Last Session"]
- `data/raw_train/drivers_round_7.csv` (1163 bytes); columns: ["Number", "Driver ID", "Abbreviation", "First Name", "Last Name", "Full Name", "Team"]
- `data/raw_train/drivers_round_8.csv` (1163 bytes); columns: ["Number", "Driver ID", "Abbreviation", "First Name", "Last Name", "Full Name", "Team"]
- `data/raw_train/lap_times_round_7.csv` (154372 bytes); columns: ["Driver", "Lap Number", "Lap Time", "Position", "Time", "Sector 1", "Sector 2", "Sector 3"]
- `data/raw_train/lap_times_round_8.csv` (182413 bytes); columns: ["Driver", "Lap Number", "Lap Time", "Position", "Time", "Sector 1", "Sector 2", "Sector 3"]
- `data/raw_train/qualifying_round_7.csv` (1918 bytes); columns: ["Abbreviation", "Driver ID", "Full Name", "Team", "Q1 Time", "Q2 Time", "Q3 Time", "Position"]
- `data/raw_train/qualifying_round_8.csv` (1918 bytes); columns: ["Abbreviation", "Driver ID", "Full Name", "Team", "Q1 Time", "Q2 Time", "Q3 Time", "Position"]
- `data/raw_train/race_results_round_7.csv` (5650 bytes); columns: ["DriverNumber", "BroadcastName", "Abbreviation", "DriverId", "TeamName", "TeamColor", "TeamId", "FirstName", "LastName", "FullName", "HeadshotUrl", "CountryCode", "Position", "ClassifiedPosition", "GridPosition", "Q1", "Q2", "Q3", "Time", "Status", "Points"]
- `data/raw_train/race_results_round_8.csv` (5624 bytes); columns: ["DriverNumber", "BroadcastName", "Abbreviation", "DriverId", "TeamName", "TeamColor", "TeamId", "FirstName", "LastName", "FullName", "HeadshotUrl", "CountryCode", "Position", "ClassifiedPosition", "GridPosition", "Q1", "Q2", "Q3", "Time", "Status", "Points"]
- `data/raw_train/race_status_round_7.csv` (579 bytes); columns: ["Abbreviation", "Full Name", "Status"]
- `data/raw_train/race_status_round_8.csv` (553 bytes); columns: ["Abbreviation", "Full Name", "Status"]
- `data/raw_train/races_data_2025_roundref_7.csv` (3592 bytes); columns: ["Round", "Event Name", "Official Event Name", "Location", "Country", "First Session", "Last Session"]
- `data/raw_train/races_data_2025_roundref_8.csv` (3592 bytes); columns: ["Round", "Event Name", "Official Event Name", "Location", "Country", "First Session", "Last Session"]
- `data/raw_train/season_data_2025_roundref_7.csv` (2375 bytes); columns: ["Round", "Event Name", "Location", "Country", "First Session", "Last Session"]
- `data/raw_train/season_data_2025_roundref_8.csv` (2375 bytes); columns: ["Round", "Event Name", "Location", "Country", "First Session", "Last Session"]
- `data/raw_train/strategy_events_round_7.csv` (1295 bytes); columns: ["Driver", "Lap Number", "Pit Out Time", "Pit In Time"]
- `data/raw_train/strategy_events_round_8.csv` (1352 bytes); columns: ["Driver", "Lap Number", "Pit Out Time", "Pit In Time"]
- `data/sample_submission.csv` (38052 bytes); columns: ["id", "pit_next_lap"]
- `data/test.csv` (116634 bytes); columns: ["id", "event", "driver", "lap", "position", "lap_time", "s1", "s2", "s3", "race_time", "team", "quali_pos", "Q1 Time", "Q2 Time", "Q3 Time"]
- `data/train.csv` (259021 bytes); columns: ["id", "event", "driver", "lap", "position", "lap_time", "s1", "s2", "s3", "race_time", "team", "quali_pos", "Q1 Time", "Q2 Time", "Q3 Time", "pit_next_lap"]

## Public description

Competition: F1 Next-Lap Pit Stop Probability

Overview
Predict, for each driver and lap during an F1 race, the probability that the driver will pit on the next lap. You are given per-lap timing, sectors, race position, grid information, and driver/team identities across three events. The task emphasizes time-aware feature engineering and probability calibration under class imbalance.

Data
- Train data: two events (Italy GP 2025, Monaco GP 2025) combined into a single table of per-lap observations with the target.
- Test data: one event (Spain GP 2025) as a single table of per-lap observations without the target.
- Each row represents one state (Event, Driver, Lap). The target pit_next_lap indicates whether the driver will pit on the next lap (1) or not (0).
- Files provided:
  - train.csv: features plus the target pit_next_lap
  - test.csv: features only
  - sample_submission.csv: a properly formatted example submission
  - raw_train/: optional raw files for training events (lap times, qualifying, drivers, race results, race status, and renamed strategy_events_*.csv containing pit stop records)
  - raw_test/: optional raw files for the test event (same as above except strategy/pit files are omitted)

Important details
- Time strings are converted to seconds where applicable.
- Target definition: for a given row (event, driver, lap = t), pit_next_lap = 1 if that driver made a pit stop at lap t+1; otherwise 0. Rows for which t+1 does not exist (final lap or retirement) are excluded.
- Event identity and driver/team categories are present; you may enrich features using raw_train/ and raw_test/ without leaking test labels.
- Any filenames that could reveal answers in the test set (pit stop tables) have been removed from raw_test.

Submission format
- Submit a CSV with exactly two columns, in this order:
  - id: unique identifier for a row in test.csv
  - pit_next_lap: predicted probability (float in [0, 1]) that a pit stop occurs on the next lap
- The set of ids must exactly match those in test.csv; no duplicates are allowed.

Evaluation
- Metric: Log Loss over all test rows.
  - For each row with ground truth y ∈ {0,1} and prediction p ∈ [0,1], the contribution is −(y log p + (1−y) log(1−p)). The final score is the mean across rows.
  - Lower is better. Well-calibrated probabilities are rewarded; overconfident wrong predictions are penalized.

Guidance
- This is a time-aware binary classification problem. Suggested features include rolling pace statistics (lap/sector means, deltas), stint dynamics (laps since last stop), position trends, and grid context from qualifying.
- The split is event-based: training on Italy+Monaco and testing on Spain, which evaluates generalization across circuits. All test drivers also appear in training.

Files
- Final competition files: train.csv, test.csv, sample_submission.csv
- Auxiliary optional files: raw_train/, raw_test/
