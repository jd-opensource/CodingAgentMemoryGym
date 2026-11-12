# OpenMLE-fast task

Task ID: `heart-attack-risk-dataset-of-china@1`

Native metric: `HeartAttackRiskChinaMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4377 bytes)
- `data/sample_submission.csv` (622125 bytes); columns: ["Sample_ID", "Heart_Attack"]
- `data/test.csv` (6748588 bytes); columns: ["Sample_ID", "Age", "Gender", "Smoking_Status", "Hypertension", "Diabetes", "Obesity", "Cholesterol_Level", "Air_Pollution_Exposure", "Physical_Activity", "Diet_Score", "Stress_Level", "Alcohol_Consumption", "Family_History_CVD", "Healthcare_Access", "Rural_or_Urban", "Region", "Province", "Hospital_Availability", "TCM_Use", "Employment_Status", "Education_Level", "Income_Level", "Blood_Pressure", "Chronic_Kidney_Disease", "Previous_Heart_Attack"]
- `data/train.csv` (27597066 bytes); columns: ["Sample_ID", "Age", "Gender", "Smoking_Status", "Hypertension", "Diabetes", "Obesity", "Cholesterol_Level", "Air_Pollution_Exposure", "Physical_Activity", "Diet_Score", "Stress_Level", "Alcohol_Consumption", "Family_History_CVD", "Healthcare_Access", "Rural_or_Urban", "Region", "Province", "Hospital_Availability", "TCM_Use", "Employment_Status", "Education_Level", "Income_Level", "Blood_Pressure", "Chronic_Kidney_Disease", "Previous_Heart_Attack", "Heart_Attack"]

## Public description

```
description.txt (41 lines)
sample_submission.csv (47855 lines)
test.csv (47855 lines)
train.csv (191413 lines)```

-> sample_submission.csv has 47854 rows and 2 columns.
Here is some information about the columns:
Heart_Attack (float64) has 1 unique values: [0.5]
Sample_ID (object) has 47854 unique values. Some example values: ['S0167568', 'S0232246', 'S0022431', 'S0189002']

-> test.csv has 47854 rows and 26 columns.
Here is some information about the columns:
Age (int64) has range: 30.00 - 89.00, 0 nan values
Air_Pollution_Exposure (object) has 3 unique values: ['Medium', 'Low', 'High']
Alcohol_Consumption (object) has 2 unique values: ['No', 'Yes']
Blood_Pressure (int64) has range: 90.00 - 179.00, 0 nan values
Cholesterol_Level (object) has 3 unique values: ['Normal', 'Low', 'High']
Chronic_Kidney_Disease (object) has 2 unique values: ['No', 'Yes']
Diabetes (object) has 2 unique values: ['No', 'Yes']
Diet_Score (object) has 3 unique values: ['Moderate', 'Healthy', 'Poor']
Education_Level (object) has 3 unique values: ['Secondary', 'Primary', 'Higher', nan]
Employment_Status (object) has 3 unique values: ['Employed', 'Retired', 'Unemployed']
Family_History_CVD (object) has 2 unique values: ['No', 'Yes']
Gender (object) has 2 unique values: ['Male', 'Female']
Healthcare_Access (object) has 3 unique values: ['Moderate', 'Good', 'Poor']
Hospital_Availability (object) has 3 unique values: ['Low', 'High', 'Medium']
Hypertension (object) has 2 unique values: ['No', 'Yes']
Income_Level (object) has 3 unique values: ['Low', 'High', 'Middle']
Obesity (object) has 2 unique values: ['Yes', 'No']
Physical_Activity (object) has 3 unique values: ['Medium', 'Low', 'High']
Previous_Heart_Attack (object) has 2 unique values: ['No', 'Yes']
Province (object) has 8 unique values: ['Shanghai', 'Gansu', 'Shandong', 'Guangdong', 'Qinghai', 'Henan', 'Beijing', 'Sichuan']
Region (object) has 5 unique values: ['Eastern', 'Northern', 'Western', 'Southern', 'Central']
Rural_or_Urban (object) has 2 unique values: ['Rural', 'Urban']
Sample_ID (object) has 47854 unique values. Some example values: ['S0167568', 'S0232246', 'S0022431', 'S0189002']
Smoking_Status (object) has 2 unique values: ['Smoker', 'Non-Smoker']
Stress_Level (object) has 3 unique values: ['Low', 'High', 'Medium']
TCM_Use (object) has 2 unique values: ['Yes', 'No']

-> train.csv has 191412 rows and 27 columns.
Here is some information about the columns:
Age (int64) has range: 30.00 - 89.00, 0 nan values
Air_Pollution_Exposure (object) has 3 unique values: ['Medium', 'Low', 'High']
Alcohol_Consumption (object) has 2 unique values: ['Yes', 'No']
Blood_Pressure (int64) has range: 90.00 - 179.00, 0 nan values
Cholesterol_Level (object) has 3 unique values: ['High', 'Low', 'Normal']
Chronic_Kidney_Disease (object) has 2 unique values: ['No', 'Yes']
Diabetes (object) has 2 unique values: ['No', 'Yes']
Diet_Score (object) has 3 unique values: ['Healthy', 'Poor', 'Moderate']
Education_Level (object) has 3 unique values: ['Secondary', 'Primary', nan, 'Higher']
Employment_Status (object) has 3 unique values: ['Retired', 'Unemployed', 'Employed']
Family_History_CVD (object) has 2 unique values: ['No', 'Yes']
Gender (object) has 2 unique values: ['Female', 'Male']
Healthcare_Access (object) has 3 unique values: ['Good', 'Poor', 'Moderate']
Heart_Attack (object) has 2 unique values: ['No', 'Yes']
Hospital_Availability (object) has 3 unique values: ['High', 'Medium', 'Low']
Hypertension (object) has 2 unique values: ['Yes', 'No']
Income_Level (object) has 3 unique values: ['Low', 'Middle', 'High']
Obesity (object) has 2 unique values: ['No', 'Yes']
Physical_Activity (object) has 3 unique values: ['High', 'Low', 'Medium']
Previous_Heart_Attack (object) has 2 unique values: ['No', 'Yes']
Province (object) has 8 unique values: ['Beijing', 'Gansu', 'Henan', 'Sichuan', 'Shanghai', 'Qinghai', 'Shandong', 'Guangdong']
Region (object) has 5 unique values: ['Northern', 'Southern', 'Eastern', 'Western', 'Central']
Rural_or_Urban (object) has 2 unique values: ['Rural', 'Urban']
Sample_ID (object) has 191412 unique values. Some example values: ['S0100276', 'S0066126', 'S0211839', 'S0131406']
Smoking_Status (object) has 2 unique values: ['Smoker', 'Non-Smoker']
Stress_Level (object) has 3 unique values: ['Medium', 'High', 'Low']
TCM_Use (object) has 2 unique values: ['Yes', 'No']
