# OpenMLE-fast task

Task ID: `phq-9-depression-assessment@1`

Native metric: `MoodForecastingMAEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4105 bytes)
- `data/sample_submission.csv` (21760 bytes); columns: ["row_id", "happiness_next"]
- `data/test.csv` (401516 bytes); columns: ["row_id", "user_id", "phq1", "phq2", "phq3", "phq4", "phq5", "phq6", "phq7", "phq8", "phq9", "age", "sex", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10", "q11", "q12", "q13", "q14", "q16", "q46", "q47", "happiness.score", "time", "period.name", "phq.day"]
- `data/train.csv` (1531606 bytes); columns: ["user_id", "phq1", "phq2", "phq3", "phq4", "phq5", "phq6", "phq7", "phq8", "phq9", "age", "sex", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10", "q11", "q12", "q13", "q14", "q16", "q46", "q47", "happiness.score", "time", "period.name", "phq.day", "happiness_next"]

## Public description

Title: Next-Period Mood Forecasting from Ambulatory Assessments

Problem statement
- Task: Given a participant’s ambulatory assessment (AA) record at time t, predict the next period’s happiness score (an ordinal rating 0–4) at time t+1 for the same participant. Your model should generalize across users and leverage temporal, clinical, and demographic context while strictly avoiding lookahead beyond time t.
- Perspective: This is a short-horizon, within-subject forecasting problem on irregularly sampled time series (typically morning/midday/evening per day) with high missingness in several items and notable class imbalance.

Files provided
- train.csv: Feature rows at time t with the corresponding label happiness_next (the next period’s happiness, 0–4).
- test.csv: Feature rows at time t with an additional row_id column for submission alignment, and without the target.
- sample_submission.csv: Example submission file with the required format and randomly generated valid predictions.

Target and features
- Target: happiness_next (integer in [0, 4]), defined as the next period’s happiness score following each feature row.
- Core features available in both train and test include (not exhaustive):
  - user_id: Participant identifier.
  - time: Timestamp of the AA record (string ISO-like format).
  - period.name: Time-of-day label (morning/midday/evening).
  - phq.day: Relative day index of the AA record.
  - happiness.score: The participant’s happiness at time t (0–4).
  - PHQ-9 items: phq1–phq9 (integer 0–3 where present; missing for some rows).
  - Demographics: age (years; may be missing), sex (categorical; may be missing).
  - Additional AA items: q1–q14, q16, q46, q47 (typically 0–4 where present; many missing values).
- Columns intentionally excluded from both train and test due to redundancy/leakage risk: id, start.time, any unnamed/empty column.

How the data is constructed
- Records are sorted within each user by time. For each record at index j, a supervised example is created using the features at index j and the label equal to the happiness.score at index j+1 (the next-period value). The final row per user is not used as a source record because it has no next-period label.
- The dataset is split within each user chronologically: approximately the earliest 80% source records per user form the training set and the remaining 20% form the test set. A small, deterministic adjustment ensures that every happiness_next class present in the test set also appears at least once in the training set.

Evaluation
- Official metric: Mean Absolute Error (MAE) between your predictions and the true happiness_next values.
  - MAE = mean(|y_pred − y_true|) over all test rows.
  - Predictions may be real-valued and will be clipped to [0, 4] for scoring stability; they are compared directly to the integer ground truth.
  - Lower is better.

Submission format
- A CSV with exactly two columns and a header row:
  - row_id: Unique identifier for each test row (exactly matches the row_id in test.csv).
  - happiness_next: Your prediction for the next period’s happiness (numeric; values outside [0, 4] will be clipped for scoring).
- The submission must contain one row for every row of test.csv, with matching row_id values and no duplicates.

Guidance and constraints
- No lookahead: Use only information available at or before time t to predict time t+1.
- Missing values: Many AA items are sparse. Consider robust imputations, missingness indicators, and user-level statistics computed on training data.
- Temporal modeling: Useful approaches include lag features, rolling aggregates, and sequence models. Time encodings (period-of-day, day-of-week) and PHQ-9 context can be beneficial.
- Ordinal target: MAE is chosen to reflect the ordered nature of the target and to be robust to class imbalance.

Deliverables summary
- train.csv
- test.csv
- sample_submission.csv

Good luck and have fun building robust temporal-ordinal models that respect real-world data constraints while extracting signal from rich clinical and temporal context!
