# OpenMLE-fast task

Task ID: `call-center-dataset-analysis@2`

Native metric: `CallCenterSLAMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2270 bytes)
- `data/sample_submission.csv` (237221 bytes); columns: ["id", "response_time"]
- `data/test.csv` (607646 bytes); columns: ["id", "call_timestamp", "reason", "city", "state", "channel", "call_center"]
- `data/train.csv` (2710527 bytes); columns: ["id", "call_timestamp", "reason", "city", "state", "channel", "call_center", "response_time"]

## Public description

```
description.txt (44 lines)
sample_submission.csv (6590 lines)
test.csv (6590 lines)
train.csv (26353 lines)```

-> sample_submission.csv has 6589 rows and 2 columns.
Here is some information about the columns:
id (object) has 6589 unique values. Some example values: ['ZKL-36741649-t-725923-42', 'FMY-91007802-K-610011-Mw', 'MEK-48259500-K-277505-Oi', 'ILX-48224690-9-351405-hL']
response_time (object) has 1 unique values: ['Within SLA']

-> test.csv has 6589 rows and 7 columns.
Here is some information about the columns:
call_center (object) has 4 unique values: ['Los Angeles/CA', 'Chicago/IL', 'Baltimore/MD', 'Denver/CO']
call_timestamp (object) has 31 unique values. Some example values: ['10/21/2020', '10/17/2020', '10/20/2020', '10/13/2020']
channel (object) has 4 unique values: ['Call-Center', 'Web', 'Email', 'Chatbot']
city (object) has 457 unique values. Some example values: ['Washington', 'Houston', 'El Paso', 'New York City']
id (object) has 6589 unique values. Some example values: ['ZKL-36741649-t-725923-42', 'FMY-91007802-K-610011-Mw', 'MEK-48259500-K-277505-Oi', 'ILX-48224690-9-351405-hL']
reason (object) has 3 unique values: ['Billing Question', 'Service Outage', 'Payments']
state (object) has 51 unique values. Some example values: ['California', 'Texas', 'Florida', 'New York']

-> train.csv has 26352 rows and 8 columns.
Here is some information about the columns:
call_center (object) has 4 unique values: ['Baltimore/MD', 'Los Angeles/CA', 'Denver/CO', 'Chicago/IL']
call_timestamp (object) has 30 unique values. Some example values: ['10/22/2020', '10/06/2020', '10/28/2020', '10/30/2020']
channel (object) has 4 unique values: ['Chatbot', 'Call-Center', 'Web', 'Email']
city (object) has 461 unique values. Some example values: ['Washington', 'Houston', 'New York City', 'El Paso']
id (object) has 26352 unique values. Some example values: ['EMO-73405811-q-733228-Pf', 'HUZ-48902400-k-369806-Bm', 'NPZ-59117542-S-661400-Z1', 'VHW-70170149-i-362174-FD']
reason (object) has 3 unique values: ['Billing Question', 'Service Outage', 'Payments']
response_time (object) has 3 unique values: ['Within SLA', 'Below SLA', 'Above SLA']
state (object) has 51 unique values. Some example values: ['California', 'Texas', 'Florida', 'New York']
