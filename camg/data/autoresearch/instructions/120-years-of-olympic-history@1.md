# OpenMLE-fast task

Task ID: `120-years-of-olympic-history@1`

Native metric: `OlympicMedalistMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3669 bytes)
- `data/sample_submission.csv` (536917 bytes); columns: ["row_id", "Medalist"]
- `data/test.csv` (6124766 bytes); columns: ["Sex", "Age", "Height", "Weight", "Team", "NOC", "region", "Games", "Year", "Season", "City", "Sport", "Event", "row_id"]
- `data/train.csv` (26958583 bytes); columns: ["Sex", "Age", "Height", "Weight", "Team", "NOC", "region", "Games", "Year", "Season", "City", "Sport", "Event", "Medalist", "row_id"]

## Public description

```
description.txt (46 lines)
sample_submission.csv (50689 lines)
submission_oracle.csv (50689 lines)
submission_random.csv (50689 lines)
submission_zero.csv (50689 lines)
test.csv (50689 lines)
train.csv (220429 lines)```

-> sample_submission.csv has 50688 rows and 2 columns.
Here is some information about the columns:
Medalist (float64) has 1 unique values: [0.5]
row_id (int64) has range: 1.00 - 271113.00, 0 nan values

-> submission_oracle.csv has 50688 rows and 2 columns.
Here is some information about the columns:
Medalist (int64) has 2 unique values: [0, 1]
row_id (int64) has range: 1.00 - 271113.00, 0 nan values

-> submission_random.csv has 50688 rows and 2 columns.
Here is some information about the columns:
Medalist (float64) has range: 0.00 - 1.00, 0 nan values
row_id (int64) has range: 1.00 - 271113.00, 0 nan values

-> submission_zero.csv has 50688 rows and 2 columns.
Here is some information about the columns:
Medalist (float64) has 1 unique values: [0.0]
row_id (int64) has range: 1.00 - 271113.00, 0 nan values

-> test.csv has 50688 rows and 14 columns.
Here is some information about the columns:
Age (float64) has range: 11.00 - 77.00, 1668 nan values
City (object) has 42 unique values. Some example values: ['London', 'Athina', 'Beijing', 'Los Angeles']
Event (object) has 474 unique values. Some example values: ["Football Men's Football", "Gymnastics Men's Horizontal Bar", "Gymnastics Men's Parallel Bars", "Water Polo Men's Water Polo"]
Games (object) has 51 unique values. Some example values: ['2008 Summer', '2012 Summer', '2000 Summer', '2004 Summer']
Height (float64) has range: 127.00 - 223.00, 11047 nan values
NOC (object) has 220 unique values. Some example values: ['USA', 'FRA', 'GBR', 'ITA']
Season (object) has 2 unique values: ['Summer', 'Winter']
Sex (object) has 2 unique values: ['M', 'F']
Sport (object) has 56 unique values. Some example values: ['Athletics', 'Gymnastics', 'Swimming', 'Cycling']
Team (object) has 504 unique values. Some example values: ['United States', 'France', 'Great Britain', 'Italy']
Weight (float64) has range: 28.00 - 214.00, 11506 nan values
Year (int64) has range: 1896.00 - 2016.00, 0 nan values
region (object) has 202 unique values. Some example values: ['USA', 'Germany', 'France', 'UK']
row_id (int64) has range: 1.00 - 271113.00, 0 nan values

-> train.csv has 220428 rows and 15 columns.
Here is some information about the columns:
Age (float64) has range: 10.00 - 97.00, 7806 nan values
City (object) has 42 unique values. Some example values: ['London', 'Athina', 'Rio de Janeiro', 'Atlanta']
Event (object) has 715 unique values. Some example values: ["Football Men's Football", "Ice Hockey Men's Ice Hockey", "Hockey Men's Hockey", "Basketball Men's Basketball"]
Games (object) has 51 unique values. Some example values: ['2016 Summer', '1996 Summer', '2000 Summer', '2004 Summer']
Height (float64) has range: 127.00 - 226.00, 49124 nan values
Medalist (int64) has 2 unique values: [0, 1]
NOC (object) has 229 unique values. Some example values: ['USA', 'FRA', 'GBR', 'ITA']
Season (object) has 2 unique values: ['Summer', 'Winter']
Sex (object) has 2 unique values: ['M', 'F']
Sport (object) has 64 unique values. Some example values: ['Athletics', 'Gymnastics', 'Swimming', 'Shooting']
Team (object) has 1012 unique values. Some example values: ['United States', 'France', 'Great Britain', 'Italy']
Weight (float64) has range: 25.00 - 214.00, 51369 nan values
Year (int64) has range: 1896.00 - 2016.00, 0 nan values
region (object) has 209 unique values. Some example values: ['USA', 'Germany', 'France', 'UK']
row_id (int64) has range: 0.00 - 271115.00, 0 nan values
