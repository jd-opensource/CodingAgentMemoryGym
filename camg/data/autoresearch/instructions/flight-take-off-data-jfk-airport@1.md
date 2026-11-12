# OpenMLE-fast task

Task ID: `flight-take-off-data-jfk-airport@1`

Native metric: `TaxiOutTimeMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3804 bytes)
- `data/sample_submission.csv` (452278 bytes); columns: ["row_id", "TAXI_OUT"]
- `data/test.csv` (1517700 bytes); columns: ["row_id", "MONTH", "DAY_OF_MONTH", "DAY_OF_WEEK", "OP_UNIQUE_CARRIER", "TAIL_NUM", "DEST", "CRS_ELAPSED_TIME", "DISTANCE", "CRS_DEP_M", "Temperature", "Dew Point", "Humidity", "Wind", "Wind Speed", "Wind Gust", "Pressure", "Condition", "sch_dep", "sch_arr"]
- `data/train.csv` (760061 bytes); columns: ["MONTH", "DAY_OF_MONTH", "DAY_OF_WEEK", "OP_UNIQUE_CARRIER", "TAIL_NUM", "DEST", "CRS_ELAPSED_TIME", "DISTANCE", "CRS_DEP_M", "Temperature", "Dew Point", "Humidity", "Wind", "Wind Speed", "Wind Gust", "Pressure", "Condition", "sch_dep", "sch_arr", "TAXI_OUT"]

## Public description

JFK Taxi-Out Time Prediction Challenge

Problem statement
Accurately estimating taxi-out time (minutes from gate pushback to wheels-off) at a congested hub like JFK enables better runway sequencing, fuel planning, and on-time performance. Your task is to build a model that predicts the taxi-out time for each departing flight using only information available before wheels-off, including schedule, identifiers, routing, and concurrent local weather.

Files provided
- train.csv: Training data with features and the target column TAXI_OUT.
- test.csv: Test data with the same features as train.csv and a row_id column. The target is withheld.
- sample_submission.csv: Example submission file with columns [row_id, TAXI_OUT]. Your submission must follow this format.

Target
- TAXI_OUT: Integer minutes from pushback to wheels-off, to be predicted for each row in test.csv.

Features
The following columns are included in train.csv and test.csv as model inputs. They reflect information known pre-departure and avoid post-event leakage:
- MONTH: Numeric month (1–12)
- DAY_OF_MONTH: Day of month (1–31)
- DAY_OF_WEEK: Day of week (1=Monday … 7=Sunday)
- OP_UNIQUE_CARRIER: Marketing carrier code
- TAIL_NUM: Aircraft tail number
- DEST: Destination airport code
- CRS_ELAPSED_TIME: Scheduled gate-to-gate time (minutes)
- DISTANCE: Great-circle distance (miles)
- CRS_DEP_M: Scheduled departure minute-of-day (0–1439)
- Temperature: Local temperature at JFK at scheduled departure
- Dew Point: Local dew point
- Humidity: Local relative humidity
- Wind: Cardinal/ordinal wind direction (categorical)
- Wind Speed: Wind speed
- Wind Gust: Wind gust speed (may be missing)
- Pressure: Sea-level pressure
- Condition: Textual weather condition category at JFK
- sch_dep: Scheduled departure hour (local, integer)
- sch_arr: Scheduled arrival hour (local, integer)

The following columns present in the raw source were excluded to avoid leakage or ambiguity and are NOT provided in the final files: DEP_DELAY, DEP_TIME_M, CRS_ARR_M.

Evaluation
- Metric: Mean Absolute Error (MAE) between your predictions and the true TAXI_OUT on the test set.
- Definition: MAE = mean(|y_pred − y_true|) computed over all rows in test.csv matched by row_id.
- Rationale: MAE measures expected deviation in minutes, is robust and interpretable for operations, and aligns with how schedule and fuel penalties scale with time.

Submission format
- CSV with two columns and header: row_id,TAXI_OUT
- row_id must match exactly the identifiers provided in test.csv.
- TAXI_OUT must be numeric (float or integer). Predictions outside a plausible range are allowed but will hurt your score.

Recommended modeling notes
- Temporal generalization: The test set is held out by calendar months, so expect seasonal and congestion differences. Avoid using any post-departure or realized-outcome information.
- Feature engineering ideas:
  - Encode high-cardinality categoricals (TAIL_NUM, DEST) with target/catboost or regularized encodings.
  - Cyclical time-of-day transforms for CRS_DEP_M and sch_dep/sch_arr.
  - Wind components: derive u/v from Wind and Wind Speed.
  - Interactions: time-of-day × carrier × weather.
- Handle missing values in Wind Gust and any sparse weather fields robustly.

Data split policy
- Train/test are split by calendar months to reduce leakage and emulate deployment. Train contains months 1–10; Test contains months 11–12. All rows are used; no downsampling.

Rules
- Use only the provided features. External data is optional but must be publicly available and equally accessible to all participants.
- Do not attempt to infer or reconstruct excluded leakage fields.

Good luck building a model that can robustly predict taxi-out time under varying traffic and weather conditions at JFK!
