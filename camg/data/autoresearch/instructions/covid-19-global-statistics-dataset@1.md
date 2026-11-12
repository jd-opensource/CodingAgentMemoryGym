# OpenMLE-fast task

Task ID: `covid-19-global-statistics-dataset@1`

Native metric: `CovidMortalityRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2044 bytes)
- `data/sample_submission.csv` (1263 bytes); columns: ["Country", "Deaths/1M pop"]
- `data/test.csv` (2889 bytes); columns: ["Country", "Tot Cases/1M pop", "Total Cases", "New Cases", "Total Recovered", "New Recovered", "Active Cases", "Serious, Critical", "Total Tests", "Tests/1M pop"]
- `data/train.csv` (12299 bytes); columns: ["Country", "Tot Cases/1M pop", "Total Cases", "New Cases", "Total Recovered", "New Recovered", "Active Cases", "Serious, Critical", "Total Tests", "Tests/1M pop", "Deaths/1M pop"]

## Public description

```
description.txt (54 lines)
sample_submission.csv (45 lines)
test.csv (45 lines)
train.csv (181 lines)```

-> sample_submission.csv has 44 rows and 2 columns.
Here is some information about the columns:
Country (object) has 44 unique values. Some example values: ['Germany', 'Japan', 'Italy', 'UK']
Deaths/1M pop (float64) has range: 18.25 - 19941.24, 0 nan values

-> test.csv has 44 rows and 10 columns.
Here is some information about the columns:
Active Cases (float64) has range: 0.00 - 396245.00, 8 nan values
Country (object) has 44 unique values. Some example values: ['Germany', 'Japan', 'Italy', 'UK']
New Cases (float64) has 2 unique values: [574.0, nan, 21.0]
New Recovered (float64) has 1 unique values: [nan, 8.0]
Serious, Critical (float64) has range: 2.00 - 131.00, 30 nan values
Tests/1M pop (float64) has range: 16205.00 - 23302116.00, 2 nan values
Tot Cases/1M pop (float64) has range: 347.00 - 703959.00, 0 nan values
Total Cases (float64) has range: 1403.00 - 38819284.00, 0 nan values
Total Recovered (float64) has range: 438.00 - 38240600.00, 8 nan values
Total Tests (float64) has range: 17762.00 - 522526476.00, 2 nan values

-> train.csv has 180 rows and 11 columns.
Here is some information about the columns:
Active Cases (float64) has range: -1.00 - 1448401.00, 40 nan values
Country (object) has 180 unique values. Some example values: ['USA', 'India', 'France', 'Brazil']
Deaths/1M pop (float64) has range: 2.00 - 5042.00, 0 nan values
New Cases (float64) has 6 unique values: [nan, 161.0, 1345.0, 210.0, 46.0, 77.0, 12.0]
New Recovered (float64) has range: 2.00 - 2116.00, 167 nan values
Serious, Critical (float64) has range: 1.00 - 1771.00, 142 nan values
Tests/1M pop (float64) has range: 5093.00 - 22165247.00, 10 nan values
Tot Cases/1M pop (float64) has range: 16.00 - 769596.00, 0 nan values
Total Cases (float64) has range: 10.00 - 111367209.00, 0 nan values
Total Recovered (float64) has range: 9.00 - 109053249.00, 40 nan values
Total Tests (float64) has range: 7850.00 - 1186742917.00, 10 nan values
