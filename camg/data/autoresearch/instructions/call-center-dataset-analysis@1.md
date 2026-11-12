# OpenMLE-fast task

Task ID: `call-center-dataset-analysis@1`

Native metric: `CallCenterCSATMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3035 bytes)
- `data/sample_submission.csv` (59377 bytes); columns: ["id", "csat_score"]
- `data/test.csv` (267491 bytes); columns: ["id", "customer_name", "sentiment", "call_timestamp", "reason", "city", "state", "channel", "response_time", "call duration in minutes", "call_center"]
- `data/train.csv` (1379822 bytes); columns: ["id", "customer_name", "sentiment", "csat_score", "call_timestamp", "reason", "city", "state", "channel", "response_time", "call duration in minutes", "call_center"]

## Public description

```
description.txt (46 lines)
sample_submission.csv (2048 lines)
test.csv (2048 lines)
train.csv (10225 lines)```

-> sample_submission.csv has 2047 rows and 2 columns.
Here is some information about the columns:
csat_score (float64) has 1 unique values: [5.0]
id (object) has 2047 unique values. Some example values: ['FTZ-87704815-T-824288-iC', 'DKK-57076809-w-055481-fU', 'JVI-79728660-U-224285-4a', 'OKT-23554135-U-885557-tw']

-> test.csv has 2047 rows and 11 columns.
Here is some information about the columns:
call duration in minutes (int64) has range: 5.00 - 45.00, 0 nan values
call_center (object) has 4 unique values: ['Los Angeles/CA', 'Baltimore/MD', 'Chicago/IL', 'Denver/CO']
call_timestamp (object) has 5 unique values: ['10/29/2020', '10/28/2020', '10/27/2020', '10/30/2020', '10/26/2020']
channel (object) has 4 unique values: ['Call-Center', 'Web', 'Chatbot', 'Email']
city (object) has 388 unique values. Some example values: ['Washington', 'Houston', 'El Paso', 'Dallas']
customer_name (object) has 2047 unique values. Some example values: ['Odey Seed', 'Analise Gairdner', 'Kaylyn Emlen', 'Callida Le Franc']
id (object) has 2047 unique values. Some example values: ['FTZ-87704815-T-824288-iC', 'DKK-57076809-w-055481-fU', 'JVI-79728660-U-224285-4a', 'OKT-23554135-U-885557-tw']
reason (object) has 3 unique values: ['Billing Question', 'Payments', 'Service Outage']
response_time (object) has 3 unique values: ['Within SLA', 'Below SLA', 'Above SLA']
sentiment (object) has 5 unique values: ['Neutral', 'Negative', 'Positive', 'Very Negative', 'Very Positive']
state (object) has 49 unique values. Some example values: ['Texas', 'California', 'Florida', 'New York']

-> train.csv has 10224 rows and 12 columns.
Here is some information about the columns:
call duration in minutes (int64) has range: 5.00 - 45.00, 0 nan values
call_center (object) has 4 unique values: ['Los Angeles/CA', 'Baltimore/MD', 'Denver/CO', 'Chicago/IL']
call_timestamp (object) has 25 unique values. Some example values: ['10/23/2020', '10/21/2020', '10/20/2020', '10/10/2020']
channel (object) has 4 unique values: ['Chatbot', 'Email', 'Call-Center', 'Web']
city (object) has 461 unique values. Some example values: ['Washington', 'Houston', 'New York City', 'El Paso']
csat_score (float64) has range: 1.00 - 10.00, 0 nan values
customer_name (object) has 10224 unique values. Some example values: ['Pearle Scolli', 'Noreen Lafflina', 'Phillipe Bowring', 'Melesa Ricardot']
id (object) has 10224 unique values. Some example values: ['ZHQ-56186331-y-086221-rs', 'ZJI-96807559-i-620008-m7', 'AZI-95054097-e-185542-PT', 'DPT-56483482-P-371409-CQ']
reason (object) has 3 unique values: ['Billing Question', 'Payments', 'Service Outage']
response_time (object) has 3 unique values: ['Within SLA', 'Above SLA', 'Below SLA']
sentiment (object) has 5 unique values: ['Very Negative', 'Neutral', 'Positive', 'Negative', 'Very Positive']
state (object) has 51 unique values. Some example values: ['Texas', 'California', 'Florida', 'New York']
