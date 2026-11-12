# OpenMLE-fast task

Task ID: `global-space-exploration-dataset-2000-2025@1`

Native metric: `GlobalSpaceExplorationMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3553 bytes)
- `data/sample_submission.csv` (15456 bytes); columns: ["row_id", "Success Rate (%)"]
- `data/test.csv` (47379 bytes); columns: ["row_id", "Country", "Year", "Mission Type", "Satellite Type", "Budget (in Billion $)", "Technology Used", "Collaborating Countries"]
- `data/train.csv` (171666 bytes); columns: ["row_id", "Country", "Year", "Mission Type", "Satellite Type", "Budget (in Billion $)", "Technology Used", "Collaborating Countries", "Success Rate (%)"]

## Public description

Title: Mission Success Rate Forecasting (2000–2025)

Background
Space agencies and private companies plan missions years in advance. Pre-launch decisions—such as technology choice, mission type, international collaboration, and budget—strongly influence the likelihood of success. Accurate success-rate forecasts help prioritize investments and manage risk.

Problem Statement
Given pre-launch mission attributes, predict the mission Success Rate (%) for missions in 2020–2025. You are provided with historical missions from 2000–2019 for training. This is a tabular regression task with a time-aware generalization challenge.

Data Description
You will work with pre-launch mission characteristics. The data has been time-split to avoid leakage from the future into the past. The following files are provided:
- train.csv: Training set containing features and the target.
- test.csv: Test set containing features only.
- sample_submission.csv: A sample submission file in the required format (random but valid values).

Each row describes a mission via the following columns:
- row_id: Unique identifier for each row.
- Country: Country/agency leading the mission.
- Year: Mission year (used for time-aware forecasting; note that the evaluation is on 2020–2025).
- Mission Type: Manned or Unmanned.
- Satellite Type: Category such as Communication, Weather, Research, Spy, Navigation.
- Budget (in Billion $): Pre-launch budget.
- Technology Used: Pre-launch technology class (e.g., Traditional Rocket, Reusable Rocket, Solar Propulsion, Nuclear Propulsion, AI Navigation).
- Collaborating Countries: Comma-separated partner countries (string). Participants may parse and engineer features from this field as desired.
- Success Rate (%): Target variable (present only in train.csv). A continuous value typically in [50, 100].

Columns deliberately excluded from train/test features to prevent leakage or overfitting shortcuts:
- Mission Name, Launch Site (near-identifiers with very high cardinality).
- Environmental Impact, Duration (in Days) (typically post-outcome or not reliably available pre-launch).

Evaluation
Submissions are evaluated on Root Mean Squared Error (RMSE) between the predicted Success Rate (%) and the ground-truth values for the test set. RMSE penalizes larger errors more strongly and is appropriate for a bounded, quasi-continuous target.

Submission Format
Submit a CSV file with exactly these columns:
- row_id
- Success Rate (%)
Rows must correspond 1:1 with test.csv (matching row_id). The order does not matter, but row_id values must match exactly and be unique.

Recommended Approaches (non-exhaustive)
- Data processing: robust type parsing, trimming, handling special characters, and correct time-aware validation.
- Feature engineering: categorical encodings (e.g., one-hot/target/frequency), engineered collaboration features (counts, top-partner indicators), log/scale transformations for Budget, temporal trend features from Year.
- Modeling: tree ensembles (GBDT/Random Forest), linear models with regularization, tabular deep models.
- Evaluation: perform offline validation using a train/validation time split (e.g., 2000–2016 vs 2017–2019) to mimic test conditions.

File List
- train.csv
- test.csv
- sample_submission.csv

Notes
- Do not use information that would not be known pre-launch (e.g., post-mission attributes) in feature engineering.
- The dataset is balanced and sufficiently large to support competitive modeling. The time-aware split introduces realistic distribution shift.
