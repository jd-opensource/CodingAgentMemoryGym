# OpenMLE-fast task

Task ID: `bangalore-rapido-ride-services-dataset@2`

Native metric: `RideFareRegressionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2503 bytes)
- `data/sample_submission.csv` (190157 bytes); columns: ["id", "total_fare"]
- `data/test.csv` (722052 bytes); columns: ["id", "services", "date", "time", "source", "destination", "duration", "distance", "payment_method"]
- `data/train.csv` (4001266 bytes); columns: ["id", "services", "date", "time", "source", "destination", "duration", "distance", "payment_method", "total_fare"]

## Public description

```
description.txt (56 lines)
sample_submission.csv (7361 lines)
test.csv (7361 lines)
train.csv (37605 lines)```

-> sample_submission.csv has 7360 rows and 2 columns.
Here is some information about the columns:
id (object) has 7360 unique values. Some example values: ['R044637', 'R044661', 'R044667', 'R044669']
total_fare (float64) has range: 25.86 - 1496.75, 0 nan values

-> test.csv has 7360 rows and 9 columns.
Here is some information about the columns:
date (object) has 10 unique values. Some example values: ['2024-08-10', '2024-08-14', '2024-08-13', '2024-08-11']
destination (object) has 5585 unique values. Some example values: ['Hulimavu Park', 'Kothanur Landing', 'Hulimavu Esplanade', 'Banaswadi 6th Block']
distance (float64) has range: 1.00 - 50.00, 0 nan values
duration (int64) has range: 10.00 - 119.00, 0 nan values
id (object) has 7360 unique values. Some example values: ['R044637', 'R044661', 'R044667', 'R044669']
payment_method (object) has 4 unique values: ['Amazon Pay', 'Paytm', 'GPay', 'QR scan']
services (object) has 5 unique values: ['parcel', 'cab economy', 'auto', 'bike', 'bike lite']
source (object) has 5576 unique values. Some example values: ['Banaswadi Meadows', 'Arekere Yard', 'Seshadripuram Pier', 'Sanjay Nagar Close']
time (object) has 7357 unique values. Some example values: ['11:50:10.788614', '01:42:02.771041', '10:02:38.689686', '10:17:26.735376']

-> train.csv has 37604 rows and 10 columns.
Here is some information about the columns:
date (object) has 51 unique values. Some example values: ['2024-08-03', '2024-07-29', '2024-07-14', '2024-06-24']
destination (object) has 12441 unique values. Some example values: ['Gottigere Landing', 'HRBR Layout Drive', 'Gottigere Square', 'Hulimavu Drive']
distance (float64) has range: 1.00 - 50.00, 0 nan values
duration (int64) has range: 10.00 - 119.00, 0 nan values
id (object) has 37604 unique values. Some example values: ['R044963', 'R000001', 'R000002', 'R000003']
payment_method (object) has 4 unique values: ['Amazon Pay', 'Paytm', 'QR scan', 'GPay']
services (object) has 5 unique values: ['cab economy', 'auto', 'parcel', 'bike lite', 'bike']
source (object) has 12469 unique values. Some example values: ['Kothanur Landing', 'Banaswadi Landing', 'HRBR Layout Landing', 'Kalyan Nagar Landing']
time (object) has 37247 unique values. Some example values: ['19:55:36.542646', '03:38:25.754771', '21:57:50.611537', '15:30:12.771041']
total_fare (float64) has range: 51.71 - 1048.80, 0 nan values
