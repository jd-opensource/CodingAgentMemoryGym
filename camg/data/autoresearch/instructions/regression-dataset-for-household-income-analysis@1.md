# OpenMLE-fast task

Task ID: `regression-dataset-for-household-income-analysis@1`

Native metric: `HouseholdIncomeMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2706 bytes)
- `data/sample_submission.csv` (46513 bytes); columns: ["Id", "Income"]
- `data/test.csv` (187360 bytes); columns: ["Id", "Age", "Education_Level", "Occupation", "Number_of_Dependents", "Location", "Work_Experience", "Marital_Status", "Employment_Status", "Household_Size", "Homeownership_Status", "Type_of_Housing", "Gender", "Primary_Mode_of_Transportation"]
- `data/train.csv` (802932 bytes); columns: ["Id", "Age", "Education_Level", "Occupation", "Number_of_Dependents", "Location", "Work_Experience", "Marital_Status", "Employment_Status", "Household_Size", "Homeownership_Status", "Type_of_Housing", "Gender", "Primary_Mode_of_Transportation", "Income"]

## Public description

```
description.txt (34 lines)
sample_submission.csv (2001 lines)
test.csv (2001 lines)
train.csv (8001 lines)```

-> sample_submission.csv has 2000 rows and 2 columns.
Here is some information about the columns:
Id (int64) has range: 2.00 - 9995.00, 0 nan values
Income (float64) has range: 1241.83 - 60941765.84, 0 nan values

-> test.csv has 2000 rows and 14 columns.
Here is some information about the columns:
Age (int64) has range: 18.00 - 70.00, 0 nan values
Education_Level (object) has 4 unique values: ["Bachelor's", "Master's", 'High School', 'Doctorate']
Employment_Status (object) has 3 unique values: ['Full-time', 'Part-time', 'Self-employed']
Gender (object) has 2 unique values: ['Male', 'Female']
Homeownership_Status (object) has 2 unique values: ['Rent', 'Own']
Household_Size (int64) has 7 unique values: [3, 1, 7, 6, 5, 2, 4]
Id (int64) has range: 2.00 - 9995.00, 0 nan values
Location (object) has 3 unique values: ['Urban', 'Suburban', 'Rural']
Marital_Status (object) has 3 unique values: ['Married', 'Single', 'Divorced']
Number_of_Dependents (int64) has 6 unique values: [1, 3, 4, 0, 2, 5]
Occupation (object) has 5 unique values: ['Others', 'Technology', 'Education', 'Finance', 'Healthcare']
Primary_Mode_of_Transportation (object) has 4 unique values: ['Car', 'Biking', 'Walking', 'Public transit']
Type_of_Housing (object) has 3 unique values: ['Townhouse', 'Single-family home', 'Apartment']
Work_Experience (int64) has range: 0.00 - 50.00, 0 nan values

-> train.csv has 8000 rows and 15 columns.
Here is some information about the columns:
Age (int64) has range: 18.00 - 70.00, 0 nan values
Education_Level (object) has 4 unique values: ["Bachelor's", "Master's", 'High School', 'Doctorate']
Employment_Status (object) has 3 unique values: ['Full-time', 'Part-time', 'Self-employed']
Gender (object) has 2 unique values: ['Male', 'Female']
Homeownership_Status (object) has 2 unique values: ['Rent', 'Own']
Household_Size (int64) has 7 unique values: [4, 3, 6, 2, 1, 7, 5]
Id (int64) has range: 0.00 - 9999.00, 0 nan values
Income (int64) has range: 31044.00 - 9992571.00, 0 nan values
Location (object) has 3 unique values: ['Urban', 'Suburban', 'Rural']
Marital_Status (object) has 3 unique values: ['Single', 'Married', 'Divorced']
Number_of_Dependents (int64) has 6 unique values: [3, 2, 5, 4, 0, 1]
Occupation (object) has 5 unique values: ['Education', 'Healthcare', 'Finance', 'Technology', 'Others']
Primary_Mode_of_Transportation (object) has 4 unique values: ['Car', 'Biking', 'Public transit', 'Walking']
Type_of_Housing (object) has 3 unique values: ['Single-family home', 'Townhouse', 'Apartment']
Work_Experience (int64) has range: 0.00 - 50.00, 0 nan values
