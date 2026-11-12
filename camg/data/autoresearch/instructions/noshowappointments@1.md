# OpenMLE-fast task

Task ID: `noshowappointments@1`

Native metric: `NoShowAppointmentMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2323 bytes)
- `data/sample_submission.csv` (206285 bytes); columns: ["RowId", "No-show"]
- `data/test.csv` (1055039 bytes); columns: ["RowId", "ScheduledDay", "AppointmentDay", "Gender", "Age", "Neighbourhood", "Scholarship", "Hipertension", "Diabetes", "Alcoholism", "Handcap", "SMS_received"]
- `data/train.csv` (7896218 bytes); columns: ["RowId", "ScheduledDay", "AppointmentDay", "Gender", "Age", "Neighbourhood", "Scholarship", "Hipertension", "Diabetes", "Alcoholism", "Handcap", "SMS_received", "No-show"]

## Public description

```
description.txt (62 lines)
sample_submission.csv (13587 lines)
test.csv (13587 lines)
train.csv (96941 lines)```

-> sample_submission.csv has 13586 rows and 2 columns.
Here is some information about the columns:
No-show (float64) has range: 0.00 - 1.00, 0 nan values
RowId (int64) has range: 1.00 - 13586.00, 0 nan values

-> test.csv has 13586 rows and 12 columns.
Here is some information about the columns:
Age (int64) has range: 0.00 - 99.00, 0 nan values
Alcoholism (int64) has 2 unique values: [0, 1]
AppointmentDay (object) has 3 unique values: ['2016-06-06T00:00:00Z', '2016-06-07T00:00:00Z', '2016-06-08T00:00:00Z']
Diabetes (int64) has 2 unique values: [0, 1]
Gender (object) has 2 unique values: ['F', 'M']
Handcap (int64) has 4 unique values: [0, 1, 2, 4]
Hipertension (int64) has 2 unique values: [0, 1]
Neighbourhood (object) has 78 unique values. Some example values: ['JARDIM CAMBURI', 'MARIA ORTIZ', 'RESISTÊNCIA', 'JARDIM DA PENHA']
RowId (int64) has range: 1.00 - 13586.00, 0 nan values
SMS_received (int64) has 2 unique values: [0, 1]
ScheduledDay (object) has 13069 unique values. Some example values: ['2016-04-25T17:19:03Z', '2016-06-07T16:15:14Z', '2016-04-18T15:43:23Z', '2016-06-07T07:46:52Z']
Scholarship (int64) has 2 unique values: [0, 1]

-> train.csv has 96940 rows and 13 columns.
Here is some information about the columns:
Age (int64) has range: 0.00 - 115.00, 0 nan values
Alcoholism (int64) has 2 unique values: [0, 1]
AppointmentDay (object) has 24 unique values. Some example values: ['2016-05-16T00:00:00Z', '2016-05-09T00:00:00Z', '2016-05-30T00:00:00Z', '2016-05-11T00:00:00Z']
Diabetes (int64) has 2 unique values: [0, 1]
Gender (object) has 2 unique values: ['F', 'M']
Handcap (int64) has 5 unique values: [0, 1, 2, 3, 4]
Hipertension (int64) has 2 unique values: [1, 0]
Neighbourhood (object) has 81 unique values. Some example values: ['JARDIM CAMBURI', 'MARIA ORTIZ', 'RESISTÊNCIA', 'JARDIM DA PENHA']
No-show (object) has 2 unique values: ['No', 'Yes']
RowId (int64) has range: 1.00 - 96940.00, 0 nan values
SMS_received (int64) has 2 unique values: [0, 1]
ScheduledDay (object) has 91053 unique values. Some example values: ['2016-05-06T07:09:54Z', '2016-05-06T07:09:53Z', '2016-04-25T17:17:46Z', '2016-04-25T17:18:27Z']
Scholarship (int64) has 2 unique values: [0, 1]
