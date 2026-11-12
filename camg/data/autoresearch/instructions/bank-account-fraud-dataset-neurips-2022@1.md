# OpenMLE-fast task

Task ID: `bank-account-fraud-dataset-neurips-2022@1`

Native metric: `BankAccountFraudMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (168 bytes)
- `data/sample_submission.csv` (450022 bytes); columns: ["sample_id", "prediction"]
- `data/test.csv` (6969846 bytes); columns: ["sample_id", "domain", "income", "name_email_similarity", "prev_address_months_count", "current_address_months_count", "customer_age", "days_since_request", "intended_balcon_amount", "payment_type", "zip_count_4w", "velocity_6h", "velocity_24h", "velocity_4w", "bank_branch_count_8w", "date_of_birth_distinct_emails_4w", "employment_status", "credit_risk_score", "email_is_free", "housing_status", "phone_home_valid", "phone_mobile_valid", "bank_months_count", "has_other_cards", "proposed_credit_limit", "foreign_request", "source", "session_length_in_minutes", "device_os", "keep_alive_session", "device_distinct_emails_8w", "device_fraud_count", "month"]
- `data/train.csv` (7029534 bytes); columns: ["sample_id", "domain", "income", "name_email_similarity", "prev_address_months_count", "current_address_months_count", "customer_age", "days_since_request", "intended_balcon_amount", "payment_type", "zip_count_4w", "velocity_6h", "velocity_24h", "velocity_4w", "bank_branch_count_8w", "date_of_birth_distinct_emails_4w", "employment_status", "credit_risk_score", "email_is_free", "housing_status", "phone_home_valid", "phone_mobile_valid", "bank_months_count", "has_other_cards", "proposed_credit_limit", "foreign_request", "source", "session_length_in_minutes", "device_os", "keep_alive_session", "device_distinct_emails_8w", "device_fraud_count", "month", "fraud_bool"]

## Public description

Files in this directory:
- train.csv: Training data with labels.
- test.csv: Test data without labels.
- sample_submission.csv: Sample submission with required columns.
