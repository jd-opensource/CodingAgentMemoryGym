# OpenMLE-fast task

Task ID: `batadal-a-dataset-for-cyber-attack-detection@1`

Native metric: `BatadalAttackDetectionMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2670 bytes)
- `data/sample_submission.csv` (17707 bytes); columns: ["row_id", "ATT_FLAG"]
- `data/test.csv` (472911 bytes); columns: ["row_id", "timestamp", "L_T1", "L_T2", "L_T3", "L_T4", "L_T5", "L_T6", "L_T7", "F_PU1", "S_PU1", "F_PU2", "S_PU2", "F_PU3", "S_PU3", "F_PU4", "S_PU4", "F_PU5", "S_PU5", "F_PU6", "S_PU6", "F_PU7", "S_PU7", "F_PU8", "S_PU8", "F_PU9", "S_PU9", "F_PU10", "S_PU10", "F_PU11", "S_PU11", "F_V2", "S_V2", "P_J280", "P_J269", "P_J300", "P_J256", "P_J289", "P_J415", "P_J302", "P_J306", "P_J307", "P_J317", "P_J14", "P_J422"]
- `data/train.csv` (3808841 bytes); columns: ["timestamp", "L_T1", "L_T2", "L_T3", "L_T4", "L_T5", "L_T6", "L_T7", "F_PU1", "S_PU1", "F_PU2", "S_PU2", "F_PU3", "S_PU3", "F_PU4", "S_PU4", "F_PU5", "S_PU5", "F_PU6", "S_PU6", "F_PU7", "S_PU7", "F_PU8", "S_PU8", "F_PU9", "S_PU9", "F_PU10", "S_PU10", "F_PU11", "S_PU11", "F_V2", "S_V2", "P_J280", "P_J269", "P_J300", "P_J256", "P_J289", "P_J415", "P_J302", "P_J306", "P_J307", "P_J317", "P_J14", "P_J422", "ATT_FLAG"]

## Public description

BATADAL: Cyber Attacks Detection in Water Systems (Timestamp-level PR-AUC)

Problem statement
Participants are given multivariate SCADA telemetry from a benchmark water distribution network (tanks, pumps, a valve, and pressures). The task is to predict, for each hourly timestamp in the hidden test set, the probability that the system is under cyberattack.

You must build a model that outputs a calibrated probability per test row, leveraging temporal structure, sensor-actuator interactions, and imbalanced learning strategies.

Files provided
- train.csv: Labeled historical data. Each row is an hourly timestamp with all sensors/actuators and the target ATT_FLAG ∈ {0,1}.
- test.csv: Unlabeled data with the same columns as train.csv except the target. Includes a row_id column indicating the row order.
- sample_submission.csv: Example submission file with row_id and a probabilistic ATT_FLAG column.

Data schema
- timestamp: Hourly timestamp string.
- Sensors and actuators (continuous): L_T1..L_T7 (tank levels), F_PU1..F_PU11 (pump flows), F_V2 (valve flow), P_J280..P_J422 (pressures).
- Actuator states (binary): S_PU1..S_PU11, S_V2.
- Target (train.csv only): ATT_FLAG ∈ {0,1} indicates whether the system is under attack at that timestamp.

Notes and recommendations
- Parse timestamp as an hourly time feature if needed. Temporal features such as hour-of-day, day-of-week, month/season and derivatives (e.g., rates of change of levels/pressures) are often useful.
- Sensor sanity relationships (e.g., on/off transitions, flow-pressure consistency) can be predictive.
- Handle class imbalance carefully. Consider threshold-independent optimization and calibrated probabilities.

Evaluation
- Submissions must be a CSV with exactly two columns:
  - row_id: integer identifiers 0..N-1 matching the row order in test.csv
  - ATT_FLAG: predicted probability in [0,1]
- The leaderboard metric is Average Precision (AP, area under the Precision–Recall curve) computed at the timestamp level over all test rows. AP is robust for rare positives and rewards ranking quality.
- Numerical stability: non-finite predictions are not allowed; values are clipped to [0,1] before scoring.

Rules for data usage
- Use only the provided train.csv for supervised training. test.csv contains no labels. External data and model ensembling are allowed unless they introduce label leakage.
- Do not rely on future information beyond each timestamp when constructing features for training/inference.

Deliverables
- A single CSV in the format of sample_submission.csv containing one probability per test row.

Final data files
- train.csv
- test.csv
- sample_submission.csv
