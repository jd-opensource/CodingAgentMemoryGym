# OpenMLE-fast task

Task ID: `oral-cancer-prediction-dataset@1`

Native metric: `OralCancerRiskPredictionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2817 bytes)
- `data/sample_submission.csv` (167613 bytes); columns: ["ID", "Oral Cancer (Diagnosis)"]
- `data/test.csv` (1152549 bytes); columns: ["ID", "Country", "Age", "Gender", "Tobacco Use", "Alcohol Consumption", "HPV Infection", "Betel Quid Use", "Chronic Sun Exposure", "Poor Oral Hygiene", "Diet (Fruits & Vegetables Intake)", "Family History of Cancer", "Compromised Immune System", "Oral Lesions", "Unexplained Bleeding", "Difficulty Swallowing", "White or Red Patches in Mouth"]
- `data/train.csv` (4848712 bytes); columns: ["ID", "Country", "Age", "Gender", "Tobacco Use", "Alcohol Consumption", "HPV Infection", "Betel Quid Use", "Chronic Sun Exposure", "Poor Oral Hygiene", "Diet (Fruits & Vegetables Intake)", "Family History of Cancer", "Compromised Immune System", "Oral Lesions", "Unexplained Bleeding", "Difficulty Swallowing", "White or Red Patches in Mouth", "Oral Cancer (Diagnosis)"]

## Public description

```
description.txt (51 lines)
sample_submission.csv (16986 lines)
test.csv (16986 lines)
train.csv (67938 lines)```

-> sample_submission.csv has 16985 rows and 2 columns.
Here is some information about the columns:
ID (int64) has range: 2.00 - 84919.00, 0 nan values
Oral Cancer (Diagnosis) (float64) has 1 unique values: [0.5]

-> test.csv has 16985 rows and 17 columns.
Here is some information about the columns:
Age (int64) has range: 17.00 - 98.00, 0 nan values
Alcohol Consumption (object) has 2 unique values: ['No', 'Yes']
Betel Quid Use (object) has 2 unique values: ['Yes', 'No']
Chronic Sun Exposure (object) has 2 unique values: ['No', 'Yes']
Compromised Immune System (object) has 2 unique values: ['No', 'Yes']
Country (object) has 17 unique values. Some example values: ['Taiwan', 'Pakistan', 'Sri Lanka', 'India']
Diet (Fruits & Vegetables Intake) (object) has 3 unique values: ['High', 'Moderate', 'Low']
Difficulty Swallowing (object) has 2 unique values: ['No', 'Yes']
Family History of Cancer (object) has 2 unique values: ['No', 'Yes']
Gender (object) has 2 unique values: ['Male', 'Female']
HPV Infection (object) has 2 unique values: ['Yes', 'No']
ID (int64) has range: 2.00 - 84919.00, 0 nan values
Oral Lesions (object) has 2 unique values: ['No', 'Yes']
Poor Oral Hygiene (object) has 2 unique values: ['No', 'Yes']
Tobacco Use (object) has 2 unique values: ['No', 'Yes']
Unexplained Bleeding (object) has 2 unique values: ['No', 'Yes']
White or Red Patches in Mouth (object) has 2 unique values: ['Yes', 'No']

-> train.csv has 67937 rows and 18 columns.
Here is some information about the columns:
Age (int64) has range: 15.00 - 101.00, 0 nan values
Alcohol Consumption (object) has 2 unique values: ['Yes', 'No']
Betel Quid Use (object) has 2 unique values: ['No', 'Yes']
Chronic Sun Exposure (object) has 2 unique values: ['Yes', 'No']
Compromised Immune System (object) has 2 unique values: ['No', 'Yes']
Country (object) has 17 unique values. Some example values: ['India', 'Sri Lanka', 'Pakistan', 'Taiwan']
Diet (Fruits & Vegetables Intake) (object) has 3 unique values: ['Moderate', 'High', 'Low']
Difficulty Swallowing (object) has 2 unique values: ['Yes', 'No']
Family History of Cancer (object) has 2 unique values: ['No', 'Yes']
Gender (object) has 2 unique values: ['Male', 'Female']
HPV Infection (object) has 2 unique values: ['No', 'Yes']
ID (int64) has range: 1.00 - 84922.00, 0 nan values
Oral Cancer (Diagnosis) (object) has 2 unique values: ['No', 'Yes']
Oral Lesions (object) has 2 unique values: ['No', 'Yes']
Poor Oral Hygiene (object) has 2 unique values: ['Yes', 'No']
Tobacco Use (object) has 2 unique values: ['No', 'Yes']
Unexplained Bleeding (object) has 2 unique values: ['No', 'Yes']
White or Red Patches in Mouth (object) has 2 unique values: ['Yes', 'No']
