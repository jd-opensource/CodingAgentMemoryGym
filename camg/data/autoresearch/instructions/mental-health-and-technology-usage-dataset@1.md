# OpenMLE-fast task

Task ID: `mental-health-and-technology-usage-dataset@1`

Native metric: `MentalHealthStatusMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2383 bytes)
- `data/sample_submission.csv` (34447 bytes); columns: ["Id", "Mental_Health_Status"]
- `data/test.csv` (131275 bytes); columns: ["Id", "Age", "Gender", "Technology_Usage_Hours", "Social_Media_Usage_Hours", "Gaming_Hours", "Screen_Time_Hours", "Sleep_Hours", "Physical_Activity_Hours", "Support_Systems_Access", "Work_Environment_Impact", "Online_Support_Usage"]
- `data/train.csv` (575320 bytes); columns: ["Id", "Age", "Gender", "Technology_Usage_Hours", "Social_Media_Usage_Hours", "Gaming_Hours", "Screen_Time_Hours", "Sleep_Hours", "Physical_Activity_Hours", "Support_Systems_Access", "Work_Environment_Impact", "Online_Support_Usage", "Mental_Health_Status"]

## Public description

```
description.txt (46 lines)
sample_submission.csv (1999 lines)
test.csv (1999 lines)
train.csv (8003 lines)```

-> sample_submission.csv has 1998 rows and 2 columns.
Here is some information about the columns:
Id (object) has 1998 unique values. Some example values: ['USER-09996', 'USER-00006', 'USER-00007', 'USER-00013']
Mental_Health_Status (object) has 4 unique values: ['Good', 'Fair', 'Excellent', 'Poor']

-> test.csv has 1998 rows and 12 columns.
Here is some information about the columns:
Age (int64) has range: 18.00 - 65.00, 0 nan values
Gaming_Hours (float64) has range: 0.00 - 5.00, 0 nan values
Gender (object) has 3 unique values: ['Male', 'Female', 'Other']
Id (object) has 1998 unique values. Some example values: ['USER-09996', 'USER-00006', 'USER-00007', 'USER-00013']
Online_Support_Usage (object) has 2 unique values: ['Yes', 'No']
Physical_Activity_Hours (float64) has range: 0.00 - 10.00, 0 nan values
Screen_Time_Hours (float64) has range: 1.01 - 15.00, 0 nan values
Sleep_Hours (float64) has range: 4.00 - 9.00, 0 nan values
Social_Media_Usage_Hours (float64) has range: 0.00 - 8.00, 0 nan values
Support_Systems_Access (object) has 2 unique values: ['Yes', 'No']
Technology_Usage_Hours (float64) has range: 1.00 - 12.00, 0 nan values
Work_Environment_Impact (object) has 3 unique values: ['Neutral', 'Negative', 'Positive']

-> train.csv has 8002 rows and 13 columns.
Here is some information about the columns:
Age (int64) has range: 18.00 - 65.00, 0 nan values
Gaming_Hours (float64) has range: 0.00 - 5.00, 0 nan values
Gender (object) has 3 unique values: ['Female', 'Male', 'Other']
Id (object) has 8002 unique values. Some example values: ['USER-10000', 'USER-00001', 'USER-09952', 'USER-09953']
Mental_Health_Status (object) has 4 unique values: ['Good', 'Poor', 'Fair', 'Excellent']
Online_Support_Usage (object) has 2 unique values: ['Yes', 'No']
Physical_Activity_Hours (float64) has range: 0.00 - 10.00, 0 nan values
Screen_Time_Hours (float64) has range: 1.00 - 15.00, 0 nan values
Sleep_Hours (float64) has range: 4.00 - 9.00, 0 nan values
Social_Media_Usage_Hours (float64) has range: 0.00 - 8.00, 0 nan values
Support_Systems_Access (object) has 2 unique values: ['No', 'Yes']
Technology_Usage_Hours (float64) has range: 1.00 - 12.00, 0 nan values
Work_Environment_Impact (object) has 3 unique values: ['Negative', 'Positive', 'Neutral']
