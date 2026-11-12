# OpenMLE-fast task

Task ID: `avg-cost-of-undergrad-college-by-state@1`

Native metric: `CollegeCostForecastMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2302 bytes)
- `data/sample_submission.csv` (7764 bytes); columns: ["row_id", "Value"]
- `data/test.csv` (18252 bytes); columns: ["Year", "State", "Type", "Length", "Expense", "row_id"]
- `data/train.csv` (175605 bytes); columns: ["Year", "State", "Type", "Length", "Expense", "Value"]

## Public description

Forecast 2021 Average Undergraduate College Costs by State, Institution Type, Length, and Expense

Problem statement
Build a model that predicts the 2021 average undergraduate cost (USD) for every combination of State × Institution Type × Length × Expense category. Historical records from 2013–2020 are provided for training.

Data
- Train file: public/train.csv. Columns: Year, State, Type, Length, Expense, Value. Each row is an aggregate cost observation.
- Test file: public/test.csv. Columns: Year, State, Type, Length, Expense, row_id. The target Value is withheld.
- Sample submission: public/sample_submission.csv. Columns: row_id, Value.

Target
- Value (USD), the average cost associated with a given row.

Split
- Train: all rows with Year ∈ {2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020}.
- Test: all rows with Year = 2021. Each test row has a unique row_id used for submissions.

Modeling expectations
- Process the tabular data and engineer features to capture state-level heterogeneity and temporal trends.
- Useful approaches include encoding categorical variables (State, Type, Length, Expense), modeling interactions, and leveraging year-based trend features.
- External data is not permitted; build models using the provided historical data only.

Evaluation metric
- Mean Absolute Error (MAE) on the test set.
- Definition: MAE = average over test rows of |Prediction − GroundTruth|.
- Rationale: MAE is interpretable in dollars, treats over/under-estimation symmetrically, and is robust to outliers compared to squared-error metrics.

Submission format
- A CSV with columns: row_id, Value.
- The row_id must exactly match the IDs found in public/test.csv (order is not enforced; IDs must be present and unique).
- Value must be numeric, finite (no NaN/Inf), and expressed in USD.

Files provided
- public/train.csv: training features and targets.
- public/test.csv: test features plus row_id.
- public/sample_submission.csv: example submission with valid structure.

Notes
- All 2021 category combinations in the test set have corresponding historical entries in the training set.
- The challenge is designed to be meaningful and rigorous: successful models must handle multi-level categorical structure and temporal dynamics while avoiding leakage from the test year.
