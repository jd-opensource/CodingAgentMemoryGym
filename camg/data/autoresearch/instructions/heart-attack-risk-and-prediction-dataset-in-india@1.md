# OpenMLE-fast task

Task ID: `heart-attack-risk-and-prediction-dataset-in-india@1`

Native metric: `HeartAttackRiskIndiaMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3400 bytes)
- `data/sample_submission.csv` (48915 bytes); columns: ["Patient_ID", "Heart_Attack_Risk"]
- `data/test.csv` (162177 bytes); columns: ["Patient_ID", "State_Name", "Age", "Gender", "Diabetes", "Hypertension", "Obesity", "Smoking", "Alcohol_Consumption", "Physical_Activity", "Diet_Score", "Cholesterol_Level", "Triglyceride_Level", "LDL_Level", "HDL_Level", "Systolic_BP", "Diastolic_BP", "Air_Pollution_Exposure", "Family_History", "Stress_Level", "Healthcare_Access", "Emergency_Response_Time", "Annual_Income", "Health_Insurance"]
- `data/train.csv` (664550 bytes); columns: ["Patient_ID", "State_Name", "Age", "Gender", "Diabetes", "Hypertension", "Obesity", "Smoking", "Alcohol_Consumption", "Physical_Activity", "Diet_Score", "Cholesterol_Level", "Triglyceride_Level", "LDL_Level", "HDL_Level", "Systolic_BP", "Diastolic_BP", "Air_Pollution_Exposure", "Family_History", "Stress_Level", "Healthcare_Access", "Emergency_Response_Time", "Annual_Income", "Health_Insurance", "Heart_Attack_Risk"]

## Public description

```
description.txt (38 lines)
sample_submission.csv (2001 lines)
test.csv (2001 lines)
train.csv (8001 lines)```

-> sample_submission.csv has 2000 rows and 2 columns.
Here is some information about the columns:
Heart_Attack_Risk (float64) has range: 0.01 - 0.81, 0 nan values
Patient_ID (int64) has range: 4.00 - 9990.00, 0 nan values

-> test.csv has 2000 rows and 24 columns.
Here is some information about the columns:
Age (int64) has range: 20.00 - 79.00, 0 nan values
Air_Pollution_Exposure (int64) has 2 unique values: [0, 1]
Alcohol_Consumption (int64) has 2 unique values: [0, 1]
Annual_Income (int64) has range: 50353.00 - 1999386.00, 0 nan values
Cholesterol_Level (int64) has range: 150.00 - 299.00, 0 nan values
Diabetes (int64) has 2 unique values: [1, 0]
Diastolic_BP (int64) has range: 60.00 - 119.00, 0 nan values
Diet_Score (int64) has range: 0.00 - 10.00, 0 nan values
Emergency_Response_Time (int64) has range: 10.00 - 399.00, 0 nan values
Family_History (int64) has 2 unique values: [0, 1]
Gender (object) has 2 unique values: ['Male', 'Female']
HDL_Level (int64) has range: 20.00 - 79.00, 0 nan values
Health_Insurance (int64) has 2 unique values: [0, 1]
Healthcare_Access (int64) has 2 unique values: [1, 0]
Hypertension (int64) has 2 unique values: [0, 1]
LDL_Level (int64) has range: 50.00 - 199.00, 0 nan values
Obesity (int64) has 2 unique values: [1, 0]
Patient_ID (int64) has range: 4.00 - 9990.00, 0 nan values
Physical_Activity (int64) has 2 unique values: [1, 0]
Smoking (int64) has 2 unique values: [0, 1]
State_Name (object) has 28 unique values. Some example values: ['Meghalaya', 'Tripura', 'Gujarat', 'Bihar']
Stress_Level (int64) has range: 1.00 - 10.00, 0 nan values
Systolic_BP (int64) has range: 90.00 - 179.00, 0 nan values
Triglyceride_Level (int64) has range: 50.00 - 299.00, 0 nan values

-> train.csv has 8000 rows and 25 columns.
Here is some information about the columns:
Age (int64) has range: 20.00 - 79.00, 0 nan values
Air_Pollution_Exposure (int64) has 2 unique values: [1, 0]
Alcohol_Consumption (int64) has 2 unique values: [0, 1]
Annual_Income (int64) has range: 50366.00 - 1999714.00, 0 nan values
Cholesterol_Level (int64) has range: 150.00 - 299.00, 0 nan values
Diabetes (int64) has 2 unique values: [0, 1]
Diastolic_BP (int64) has range: 60.00 - 119.00, 0 nan values
Diet_Score (int64) has range: 0.00 - 10.00, 0 nan values
Emergency_Response_Time (int64) has range: 10.00 - 399.00, 0 nan values
Family_History (int64) has 2 unique values: [0, 1]
Gender (object) has 2 unique values: ['Female', 'Male']
HDL_Level (int64) has range: 20.00 - 79.00, 0 nan values
Health_Insurance (int64) has 2 unique values: [0, 1]
Healthcare_Access (int64) has 2 unique values: [0, 1]
Heart_Attack_Risk (int64) has 2 unique values: [0, 1]
Hypertension (int64) has 2 unique values: [0, 1]
LDL_Level (int64) has range: 50.00 - 199.00, 0 nan values
Obesity (int64) has 2 unique values: [1, 0]
Patient_ID (int64) has range: 1.00 - 10000.00, 0 nan values
Physical_Activity (int64) has 2 unique values: [0, 1]
Smoking (int64) has 2 unique values: [0, 1]
State_Name (object) has 28 unique values. Some example values: ['Chhattisgarh', 'Kerala', 'Arunachal Pradesh', 'Manipur']
Stress_Level (int64) has range: 1.00 - 10.00, 0 nan values
Systolic_BP (int64) has range: 90.00 - 179.00, 0 nan values
Triglyceride_Level (int64) has range: 50.00 - 299.00, 0 nan values
