# OpenMLE-fast task

Task ID: `telechurn@1`

Native metric: `TelecomChurnMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3258 bytes)
- `data/sample_submission.csv` (12036 bytes); columns: ["customer_id", "churn_probability"]
- `data/test.csv` (64822 bytes); columns: ["customer_id", "Unnamed:_0", "State", "Account_length", "Area_code", "International_plan", "Voice_mail_plan", "Number_vmail_messages", "Total_day_minutes", "Total_day_calls", "Total_day_charge", "Total_eve_minutes", "Total_eve_calls", "Total_eve_charge", "Total_night_minutes", "Total_night_calls", "Total_night_charge", "Total_intl_minutes", "Total_intl_calls", "Total_intl_charge", "Customer_service_calls"]
- `data/train.csv` (263579 bytes); columns: ["customer_id", "Unnamed:_0", "State", "Account_length", "Area_code", "International_plan", "Voice_mail_plan", "Number_vmail_messages", "Total_day_minutes", "Total_day_calls", "Total_day_charge", "Total_eve_minutes", "Total_eve_calls", "Total_eve_charge", "Total_night_minutes", "Total_night_calls", "Total_night_charge", "Total_intl_minutes", "Total_intl_calls", "Total_intl_charge", "Customer_service_calls", "Churn"]

## Public description

Title: Telecom Customer Churn Prediction

Background
Customer churn is a critical challenge for telecom operators. Accurately identifying customers at risk of leaving helps target retention efforts and optimize marketing resources. Given rich customer usage and service interaction data, your task is to build a model that predicts churn risk.

Problem Statement
You are provided customer-level tabular data including usage patterns, service plan flags, and customer service interactions. Build a machine learning model that outputs, for each customer in the test set, the probability that they will churn.

Data Description
Each row represents one customer with the following features:
- State: customer’s state (categorical)
- Account length: number of days/months account has been active (numeric)
- Area code: area code (numeric/categorical)
- International plan: whether the customer has an international plan (Yes/No)
- Voice mail plan: whether the customer has a voice mail plan (Yes/No)
- Number vmail messages: number of voice mail messages (numeric)
- Total day minutes, Total day calls, Total day charge (numeric)
- Total eve minutes, Total eve calls, Total eve charge (numeric)
- Total night minutes, Total night calls, Total night charge (numeric)
- Total intl minutes, Total intl calls, Total intl charge (numeric)
- Customer service calls: number of customer service calls made (numeric)
- customer_id: synthetic identifier (do not use as a predictive feature)

Training file
- train.csv: includes all feature columns above plus the target label column:
  - Churn: binary target, 1 if the customer churned, 0 otherwise

Test files
- test.csv: same feature columns as train.csv, without the Churn label; includes customer_id
- sample_submission.csv: template submission file with columns:
  - customer_id
  - churn_probability: your model’s predicted probability of Churn=1 for each test customer

Submission Format Rules
- The submission must contain exactly two columns in this order: customer_id, churn_probability
- Provide one row per test customer_id (no duplicates, no missing, and no unknown IDs)
- churn_probability must be a finite value within [0, 1]

Evaluation Metric
Submissions are evaluated using a composite metric that balances ranking quality and probability calibration:
- ROC AUC: measures how well your predictions rank churners ahead of non-churners
- Normalized Log Loss: standard binary log loss normalized against the constant-baseline that predicts the positive class prior; defined as 1 − (logloss / baseline_logloss), clipped to [0, 1]

Final score = 0.5 × ROC_AUC + 0.5 × Normalized_Log_Loss

Guidelines
- Output well-calibrated probabilities in [0, 1] for churn_probability
- Explore feature engineering (e.g., interactions between minutes and charges, plan flags, usage ratios), robust preprocessing for categorical variables, and model selection/tuning
- Handle class imbalance with appropriate techniques (e.g., class weights, resampling, thresholding)
- Avoid leakage and overfitting; do not use the Churn label for any test set operations

Files provided
- train.csv
- test.csv
- sample_submission.csv

Your goal: build the best predictive model to maximize the final score on the hidden test labels.
