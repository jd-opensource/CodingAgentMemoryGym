# OpenMLE-fast task

Task ID: `telechurn@2`

Native metric: `TelecomChurnMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3140 bytes)
- `data/sample_submission.csv` (31036 bytes); columns: ["id", "churn"]
- `data/test.csv` (67509 bytes); columns: ["id", "state", "account_length", "area_code", "international_plan", "voice_mail_plan", "number_vmail_messages", "total_day_minutes", "total_day_calls", "total_eve_minutes", "total_eve_calls", "total_night_minutes", "total_night_calls", "total_intl_minutes", "total_intl_calls", "customer_service_calls"]
- `data/train.csv` (161599 bytes); columns: ["id", "state", "account_length", "area_code", "international_plan", "voice_mail_plan", "number_vmail_messages", "total_day_minutes", "total_day_calls", "total_eve_minutes", "total_eve_calls", "total_night_minutes", "total_night_calls", "total_intl_minutes", "total_intl_calls", "customer_service_calls", "churn"]

## Public description

Calibrated Churn Risk Forecasting

Background
Telecom operators lose revenue when customers churn. Beyond ranking, real-world retention planning needs well-calibrated probabilities to size offers and budgets. Your task is to estimate the probability that a customer will churn, given their usage and service interaction signals.

Problem statement
Given customer-level telecom usage features, predict the probability that each customer will churn. Submissions are evaluated on a class-balanced log loss that rewards both discrimination and calibration under class imbalance.

Data description
The dataset consists of tabular, per-customer aggregates with no missing values. Column names are normalized to snake_case. We remove four redundant charge columns because they are deterministic linear functions of minutes.

Files
- train.csv: training rows with features and the target column.
- test.csv: test rows with features only.
- sample_submission.csv: a sample with the correct submission format.

Columns
- id: unique identifier for each row.
- Features:
  - state (categorical, 2-letter code)
  - account_length (int)
  - area_code (int)
  - international_plan (categorical: Yes/No)
  - voice_mail_plan (categorical: Yes/No)
  - number_vmail_messages (int)
  - total_day_minutes (float)
  - total_day_calls (int)
  - total_eve_minutes (float)
  - total_eve_calls (int)
  - total_night_minutes (float)
  - total_night_calls (int)
  - total_intl_minutes (float)
  - total_intl_calls (int)
  - customer_service_calls (int)
- Target:
  - churn (binary: 0 = no churn, 1 = churn)

Split
Rows are split into train/test with a fixed random seed using stratified sampling on churn to preserve the minority class prevalence. All labels present in the test set also occur in the training set.

Submission format
- A CSV file with the following columns:
  - id: the id from test.csv
  - churn: the predicted probability of churn for that id (a real number in [0,1])
- The order of rows does not matter, but ids must match exactly those in test.csv and be unique. Submissions containing NaN/Inf or probabilities outside [0,1] will be rejected.

Evaluation metric
Primary metric: Class-balanced Log Loss.
We compute the standard binary log loss separately on the positive and negative classes and average the two:
- loss_pos = mean(-log(p) over samples with churn = 1)
- loss_neg = mean(-log(1 - p) over samples with churn = 0)
- score = 0.5 * (loss_pos + loss_neg)
This is equivalent to inverse-frequency weighting by class, ensuring that the majority class does not dominate the score. Lower is better.

Notes and tips
- The task emphasizes probability calibration under class imbalance. Proper scoring rules like log loss favor well-calibrated models.
- Consider regularized linear models, tree ensembles, and post-hoc calibration (e.g., Platt scaling or isotonic regression) validated via cross-validation.
- Categorical handling (e.g., one-hot or target encoding) and careful feature scaling may improve calibration.
- The charge columns are deliberately excluded because they are deterministic multiples of minutes and add no new information.
