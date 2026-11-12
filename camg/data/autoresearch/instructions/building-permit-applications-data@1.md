# OpenMLE-fast task

Task ID: `building-permit-applications-data@1`

Native metric: `BuildingPermitCompletionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3416 bytes)
- `data/sample_submission.csv` (154612 bytes); columns: ["row_id", "days_to_completion"]
- `data/test.csv` (4537660 bytes); columns: ["row_id", "Permit Type", "Permit Type Definition", "Block", "Lot", "Street Number", "Street Number Suffix", "Street Name", "Street Suffix", "Unit", "Unit Suffix", "Description", "Filed Date", "Structural Notification", "Number of Existing Stories", "Number of Proposed Stories", "Voluntary Soft-Story Retrofit", "Fire Only Permit", "Estimated Cost", "Existing Use", "Existing Units", "Proposed Use", "Proposed Units", "Plansets", "TIDF Compliance", "Existing Construction Type", "Existing Construction Type Description", "Proposed Construction Type", "Proposed Construction Type Description", "Site Permit", "Supervisor District", "Neighborhoods - Analysis Boundaries", "Zipcode", "Location"]
- `data/train.csv` (28604960 bytes); columns: ["Permit Type", "Permit Type Definition", "Block", "Lot", "Street Number", "Street Number Suffix", "Street Name", "Street Suffix", "Unit", "Unit Suffix", "Description", "Filed Date", "Structural Notification", "Number of Existing Stories", "Number of Proposed Stories", "Voluntary Soft-Story Retrofit", "Fire Only Permit", "Estimated Cost", "Existing Use", "Existing Units", "Proposed Use", "Proposed Units", "Plansets", "TIDF Compliance", "Existing Construction Type", "Existing Construction Type Description", "Proposed Construction Type", "Proposed Construction Type Description", "Site Permit", "Supervisor District", "Neighborhoods - Analysis Boundaries", "Zipcode", "Location", "days_to_completion"]

## Public description

San Francisco Building Permits: Time-to-Completion Prediction

Problem statement
- Goal: Predict the number of calendar days from a permit’s Filed Date to its Completed Date using only information available at filing time.
- Target: days_to_completion = (Completed Date − Filed Date) in calendar days.
- This is a challenging tabular regression task with mixed data types (categorical, numeric, text, geospatial) and a heavy-tailed target.

Data provided
- train.csv: Filing-time features and the training target column days_to_completion.
- test.csv: Filing-time features for the test set plus a unique identifier column row_id.
- sample_submission.csv: A sample submission file with required submission format.

Key columns and feature scope
- Included signals (examples):
  - Permit and scope: Permit Type, Permit Type Definition, Description, Plansets, Site Permit.
  - Location and building characteristics: Block, Lot, Street Number/Suffix, Street Name/Suffix, Unit/Suffix, Zipcode, Neighborhoods, Supervisor District, Location (lat/long), Existing/Proposed Stories, Uses, Units, Construction Types (+ Descriptions).
  - Regulatory flags: Structural Notification, Voluntary Soft-Story Retrofit, Fire Only Permit, TIDF Compliance.
  - Timing context: Filed Date.
  - Costs: Estimated Cost.
- Explicitly excluded (post-filing or leakage-prone): Current Status, Current Status Date, Issued Date, Completed Date, First Construction Document Date, Permit Expiration Date, Revised Cost, Permit Creation Date, Record ID, and the Permit Number identifier (not intended as a model feature).

Train/test split
- Time-based split simulating real deployment:
  - Train: filings from 2013-01-01 to 2016-12-31 (with valid Completed Date and non-negative days_to_completion).
  - Test: filings from 2017-01-01 to 2018-02-25 (with valid Completed Date; labels withheld).
- The test rows have a stable row_id for evaluation; labels are held out in test.csv and used only for scoring.

Evaluation
- Metric: Mean Absolute Error (MAE) on days_to_completion.
- Submission format: A CSV with exactly two columns: row_id and days_to_completion.
  - row_id must match the IDs provided in test.csv.
  - days_to_completion must be numeric (non-negative recommended), representing predicted calendar days.
- MAE rationale: Robust to outliers, interpretable in days, symmetric for over/under prediction, and suitable for heavy-tailed durations.

Guidance for participants
- Use only filing-time signals. Avoid any post-filing fields or derived information from the future.
- Typical approaches: gradient boosting trees on engineered tabular features, linear models with regularization, stacking; enrich with text features from Description (e.g., TF-IDF) and geospatial encodings from Location.
- Handle missing values carefully: add explicit "unknown" categories for categoricals, median-impute numerics, and consider missingness indicators.
- Recommended feature engineering: date parts from Filed Date (weekday, month, year), changes between existing and proposed stories/units, cost log transforms, neighborhood and zip encodings, simple distance features from lat/long.

Files delivered
- train.csv
- test.csv
- sample_submission.csv

Build models on train.csv, generate predictions for the row_id values in test.csv, and submit a CSV with columns row_id and days_to_completion. The leaderboard is ranked by MAE (lower is better).
