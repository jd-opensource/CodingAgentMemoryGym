# OpenMLE-fast task

Task ID: `medical-insurance-price-prediction@1`

Native metric: `MedicalInsurancePricePredictionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2400 bytes)
- `data/sample_submission.csv` (8373 bytes); columns: ["row_id", "charges"]
- `data/submission_mean.csv` (13097 bytes); columns: ["row_id", "charges"]
- `data/test.csv` (19286 bytes); columns: ["row_id", "age", "sex", "bmi", "children", "smoker", "region"]
- `data/train.csv` (100202 bytes); columns: ["row_id", "age", "sex", "bmi", "children", "smoker", "region", "charges"]

## Public description

Title: Premium Price Prediction

Problem statement
Health insurers must forecast members’ annual medical expenses to price policies and manage risk. Your task is to predict individualized annual medical charges from demographic and lifestyle attributes. Costs are strictly positive and heavily skewed; relative accuracy across the cost spectrum matters.

Data
You are provided a clean tabular dataset describing individuals and their annual medical charges.
- Features: age, sex, bmi, children, smoker, region
- Target: charges (annual medical expense)

Files
- train.csv: Training data with features and the target.
- test_data.csv: Test data with the same features but without the target.
- sample_submission.csv: A properly formatted sample submission file.

All rows in the test set include a unique row_id. Use it to align your predictions. The train file also includes row_id for convenience.

Important notes
- The organizers pre-split the data with careful handling of duplicate records: all identical rows were grouped so that duplicates never span across train and test. This prevents leakage through exact duplicates.
- No other external data is required.

Submission format
Submit a CSV file with the following columns and no index or additional columns:
- row_id: integer, must exactly match the IDs in test_data.csv
- charges: your predicted annual medical charges for the corresponding row_id

Evaluation
Submissions are evaluated using Root Mean Squared Logarithmic Error (RMSLE) between your predictions and the ground truth charges:
RMSLE(y, y_hat) = sqrt( mean( (log1p(y_hat) - log1p(y))^2 ) )

- y and y_hat must be non-negative. Use log1p to ensure stability around zero.
- This metric emphasizes relative error, making it robust to the heavy right-tail of costs and fairly balancing low- and high-cost members.

Baseline modeling tips
- Encode categorical features (sex, smoker, region) and consider interaction terms (e.g., smoker × age, smoker × BMI).
- Model the log-transformed target or directly optimize RMSLE with tree-based models.
- Regularization and robust validation are important given the small sample size and strong interactions.

Deliverables recap
- Use train.csv to train your model.
- Generate predictions for every row in test_data.csv.
- Create a submission.csv with columns [row_id, charges] following the format above.

Good luck, and happy modeling!
