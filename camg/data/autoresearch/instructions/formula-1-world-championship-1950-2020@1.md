# OpenMLE-fast task

Task ID: `formula-1-world-championship-1950-2020@1`

Native metric: `FormulaOneRankingMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4903 bytes)
- `data/sample_submission.csv` (72265 bytes); columns: ["raceId", "driverId", "prediction"]
- `data/test.csv` (22371 bytes); columns: ["raceId", "driverId"]
- `data/test/circuits.csv` (10104 bytes); columns: ["circuitId", "circuitRef", "name", "location", "country", "lat", "lng", "alt", "url"]
- `data/test/constructors.csv` (17478 bytes); columns: ["constructorId", "constructorRef", "name", "nationality", "url"]
- `data/test/drivers.csv` (94367 bytes); columns: ["driverId", "driverRef", "number", "code", "forename", "surname", "dob", "nationality", "url"]
- `data/test/entries_test.csv` (43635 bytes); columns: ["raceId", "driverId", "constructorId", "number", "grid"]
- `data/test/qualifying_test.csv` (113872 bytes); columns: ["qualifyId", "raceId", "driverId", "constructorId", "number", "position", "q1", "q2", "q3"]
- `data/test/races_test.csv` (22620 bytes); columns: ["raceId", "year", "round", "circuitId", "name", "date", "time", "url", "fp1_date", "fp1_time", "fp2_date", "fp2_time", "fp3_date", "fp3_time", "quali_date", "quali_time", "sprint_date", "sprint_time"]
- `data/test/seasons.csv` (4594 bytes); columns: ["year", "url"]
- `data/test/sprint_results_test.csv` (22630 bytes); columns: ["resultId", "raceId", "driverId", "constructorId", "number", "grid", "position", "positionText", "positionOrder", "points", "laps", "time", "milliseconds", "fastestLap", "fastestLapTime", "statusId"]
- `data/train.csv` (244941 bytes); columns: ["raceId", "driverId", "positionOrder"]
- `data/train/circuits.csv` (10104 bytes); columns: ["circuitId", "circuitRef", "name", "location", "country", "lat", "lng", "alt", "url"]
- `data/train/constructor_results_train.csv` (217155 bytes); columns: ["constructorResultsId", "raceId", "constructorId", "points", "status"]
- `data/train/constructor_standings_train.csv` (284492 bytes); columns: ["constructorStandingsId", "raceId", "constructorId", "points", "position", "positionText", "wins"]
- `data/train/constructors.csv` (17478 bytes); columns: ["constructorId", "constructorRef", "name", "nationality", "url"]
- `data/train/driver_standings_train.csv` (811726 bytes); columns: ["driverStandingsId", "raceId", "driverId", "points", "position", "positionText", "wins"]
- `data/train/drivers.csv` (94367 bytes); columns: ["driverId", "driverRef", "number", "code", "forename", "surname", "dob", "nationality", "url"]
- `data/train/entries_train.csv` (377222 bytes); columns: ["raceId", "driverId", "constructorId", "number", "grid"]
- `data/train/lap_times_train.csv` (12331446 bytes); columns: ["raceId", "driverId", "lap", "position", "time", "milliseconds"]
- `data/train/pit_stops_train.csv` (233399 bytes); columns: ["raceId", "driverId", "stop", "lap", "time", "duration", "milliseconds"]
- `data/train/qualifying_train.csv` (311660 bytes); columns: ["qualifyId", "raceId", "driverId", "constructorId", "number", "position", "q1", "q2", "q3"]
- `data/train/races_train.csv` (133069 bytes); columns: ["raceId", "year", "round", "circuitId", "name", "date", "time", "url", "fp1_date", "fp1_time", "fp2_date", "fp2_time", "fp3_date", "fp3_time", "quali_date", "quali_time", "sprint_date", "sprint_time"]
- `data/train/results_train.csv` (1483310 bytes); columns: ["resultId", "raceId", "driverId", "constructorId", "number", "grid", "position", "positionText", "positionOrder", "points", "laps", "time", "milliseconds", "fastestLap", "rank", "fastestLapTime", "fastestLapSpeed", "statusId"]
- `data/train/seasons.csv` (4594 bytes); columns: ["year", "url"]
- `data/train/sprint_results_train.csv` (152 bytes); columns: ["resultId", "raceId", "driverId", "constructorId", "number", "grid", "position", "positionText", "positionOrder", "points", "laps", "time", "milliseconds", "fastestLap", "fastestLapTime", "statusId"]
- `data/train/status.csv` (2136 bytes); columns: ["statusId", "status"]

## Public description

F1 Pre‑Race Finish Order Prediction (1950–2024)

Problem statement
Predict the final finishing order of drivers in each Formula 1 Grand Prix using only information that would be available before the race start, together with historical data from past races. Your model must output a per‑race ranking for all drivers on the grid in the test set.

What you’re predicting
- For each (raceId, driverId) in the test set, predict a numeric score where a higher value means a better expected finishing position (closer to P1). The evaluation converts your scores into ranks within each race and compares them to the true finishing order.

Data files
The competition provides pre‑race and historical data split into train and test, as well as a submission template:
- train/
  - races_train.csv: Race metadata for training races (season, round, date, circuitId, etc.).
  - results_train.csv: Official race results for training races (includes labels such as positionOrder).
  - qualifying_train.csv, sprint_results_train.csv: Pre‑race session data for training races.
  - lap_times_train.csv, pit_stops_train.csv: Lap‑level and pit‑stop data for training races (for historical feature engineering).
  - driver_standings_train.csv, constructor_standings_train.csv, constructor_results_train.csv: Historical season form for training races.
  - entries_train.csv: Convenience file listing the starting grid and entry details for training races (raceId, driverId, constructorId, number, grid).
  - circuits.csv, drivers.csv, constructors.csv, seasons.csv, status.csv: Entity/reference tables.
- test/
  - races_test.csv: Race metadata for test races.
  - entries_test.csv: Starting grid and entry details for test races (raceId, driverId, constructorId, number, grid). This is the roster you must rank.
  - qualifying_test.csv, sprint_results_test.csv: Pre‑race session data for test races (available before the race).
  - circuits.csv, drivers.csv, constructors.csv, seasons.csv: Entity/reference tables (duplicates of train for convenience).
- sample_submission.csv: Submission template containing all (raceId, driverId) pairs from the test set with random example scores.

Notes on data scope and leakage
- The test split contains only pre‑race information. Lap‑times, pit‑stops, and standings for test races are intentionally not provided to avoid label leakage. Use training history for feature construction.
- Qualifying and sprint sessions occur before the race and are allowed as pre‑race inputs in both train and test.

Target definition
- The ground‑truth finishing order is taken from positionOrder in the official race results. For training, use results_train.csv or the simplified labels available there. For testing (scoring), the hidden labels are the true positionOrder for each (raceId, driverId) in entries_test.csv.

Evaluation
- Primary metric: Mean Spearman rank correlation (per race, macro‑averaged).
  - For each raceId in the test set, we compute Spearman’s ρ between your submitted scores and the true finishing order (where higher score should correspond to a better finish). We then average ρ across all test races.
  - Why this metric: It evaluates the full ranking within each race, is invariant to monotone transformations of your scores, and macro‑averaging ensures races with larger grids don’t dominate the leaderboard.

Submission format
- CSV with the following columns (no header changes and no extra columns):
  - raceId: integer
  - driverId: integer
  - prediction: real number (higher = better expected finish)
- Every (raceId, driverId) in entries_test.csv must appear exactly once in your submission. No duplicates or missing pairs are allowed.

Recommended approach (not mandatory)
- Join entries with races, drivers, constructors, circuits, qualifying and sprint data.
- Engineer historical features from the training split such as:
  - Grid/qualifying pace: best quali lap, delta to pole, grid vs quali deltas.
  - Driver/team form: rolling points, average finishing positions, DNF rates (from status via training results), constructor momentum.
  - Circuit effects: track identity, location, season/round, month.
- Train a ranking model (e.g., gradient boosting with group‑wise ranking loss) that produces per‑race scores. Ensure your features use only information available before each target race in test.

Train/test split
- Train: seasons up to and including 2018.
- Test: seasons 2019 to 2024.

Important rules
- Do not use any post‑race information from the test split (e.g., lap times, pit stops, standings). These are not provided for test.
- Your submission must include one score per (raceId, driverId) in entries_test.csv.

Deliverables
- Submit a single CSV following the required format. The leaderboard is based on the mean per‑race Spearman rank correlation between your scores and the true finishing order.
