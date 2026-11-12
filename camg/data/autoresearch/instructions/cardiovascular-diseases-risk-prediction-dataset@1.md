# OpenMLE-fast task

Task ID: `cardiovascular-diseases-risk-prediction-dataset@1`

Native metric: `CardiovascularDiseaseRiskMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3173 bytes)
- `data/sample_submission.csv` (1603207 bytes); columns: ["row_id", "Heart_Disease"]
- `data/test.csv` (6174655 bytes); columns: ["Checkup", "Exercise", "Skin_Cancer", "Other_Cancer", "Depression", "Diabetes", "Arthritis", "Sex", "Age_Category", "Height_(cm)", "Weight_(kg)", "BMI", "Smoking_History", "Alcohol_Consumption", "Fruit_Consumption", "Green_Vegetables_Consumption", "FriedPotato_Consumption", "row_id"]
- `data/train.csv` (25455024 bytes); columns: ["Checkup", "Exercise", "Skin_Cancer", "Other_Cancer", "Depression", "Diabetes", "Arthritis", "Sex", "Age_Category", "Height_(cm)", "Weight_(kg)", "BMI", "Smoking_History", "Alcohol_Consumption", "Fruit_Consumption", "Green_Vegetables_Consumption", "FriedPotato_Consumption", "row_id", "Heart_Disease"]

## Public description

```
description.txt (46 lines)
sample_submission.csv (61772 lines)
test.csv (61772 lines)
train.csv (247084 lines)```

-> sample_submission.csv has 61771 rows and 2 columns.
Here is some information about the columns:
Heart_Disease (float64) has range: 0.00 - 1.00, 0 nan values
row_id (int64) has range: 8.00 - 308849.00, 0 nan values

-> test.csv has 61771 rows and 18 columns.
Here is some information about the columns:
Age_Category (object) has 13 unique values. Some example values: ['65-69', '60-64', '70-74', '55-59']
Alcohol_Consumption (float64) has range: 0.00 - 30.00, 0 nan values
Arthritis (object) has 2 unique values: ['No', 'Yes']
BMI (float64) has range: 12.12 - 99.33, 0 nan values
Checkup (object) has 5 unique values: ['Within the past year', 'Within the past 2 years', 'Within the past 5 years', '5 or more years ago', 'Never']
Depression (object) has 2 unique values: ['No', 'Yes']
Diabetes (object) has 4 unique values: ['No', 'Yes', 'Yes, but female told only during pregnancy', 'No, pre-diabetes or borderline diabetes']
Exercise (object) has 2 unique values: ['Yes', 'No']
FriedPotato_Consumption (float64) has range: 0.00 - 120.00, 0 nan values
Fruit_Consumption (float64) has range: 0.00 - 120.00, 0 nan values
Green_Vegetables_Consumption (float64) has range: 0.00 - 124.00, 0 nan values
Height_(cm) (float64) has range: 91.00 - 229.00, 0 nan values
Other_Cancer (object) has 2 unique values: ['No', 'Yes']
Sex (object) has 2 unique values: ['Female', 'Male']
Skin_Cancer (object) has 2 unique values: ['No', 'Yes']
Smoking_History (object) has 2 unique values: ['Yes', 'No']
Weight_(kg) (float64) has range: 27.22 - 273.52, 0 nan values
row_id (int64) has range: 8.00 - 308849.00, 0 nan values

-> train.csv has 247083 rows and 19 columns.
Here is some information about the columns:
Age_Category (object) has 13 unique values. Some example values: ['65-69', '60-64', '70-74', '55-59']
Alcohol_Consumption (float64) has range: 0.00 - 30.00, 0 nan values
Arthritis (object) has 2 unique values: ['Yes', 'No']
BMI (float64) has range: 12.02 - 99.17, 0 nan values
Checkup (object) has 5 unique values: ['Within the past year', 'Within the past 5 years', 'Within the past 2 years', '5 or more years ago', 'Never']
Depression (object) has 2 unique values: ['No', 'Yes']
Diabetes (object) has 4 unique values: ['No', 'No, pre-diabetes or borderline diabetes', 'Yes', 'Yes, but female told only during pregnancy']
Exercise (object) has 2 unique values: ['No', 'Yes']
FriedPotato_Consumption (float64) has range: 0.00 - 128.00, 0 nan values
Fruit_Consumption (float64) has range: 0.00 - 120.00, 0 nan values
Green_Vegetables_Consumption (float64) has range: 0.00 - 128.00, 0 nan values
Heart_Disease (object) has 2 unique values: ['No', 'Yes']
Height_(cm) (float64) has range: 91.00 - 241.00, 0 nan values
Other_Cancer (object) has 2 unique values: ['No', 'Yes']
Sex (object) has 2 unique values: ['Female', 'Male']
Skin_Cancer (object) has 2 unique values: ['No', 'Yes']
Smoking_History (object) has 2 unique values: ['No', 'Yes']
Weight_(kg) (float64) has range: 24.95 - 293.02, 0 nan values
row_id (int64) has range: 0.00 - 308853.00, 0 nan values
