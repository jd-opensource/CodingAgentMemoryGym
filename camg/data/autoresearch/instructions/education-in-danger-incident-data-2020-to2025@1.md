# OpenMLE-fast task

Task ID: `education-in-danger-incident-data-2020-to2025@1`

Native metric: `EducationSeverityMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (5038 bytes)
- `data/sample_submission.csv` (23305 bytes); columns: ["id", "Severe"]
- `data/test.csv` (172769 bytes); columns: ["id", "Date", "Country", "Country ISO", "Admin 1", "Latitude", "Longitude", "Geo Precision", "Location of event", "Reported Perpetrator", "Reported Perpetrator Name", "Weapon Carried/Used", "Type of education facility", "Attacks on Schools", "Attacks on Universities", "Military Occupation of Education facility", "Arson attack on education facility", "Forced Entry into education facility", "Damage/Destruction To Ed facility Event", "Attacks on Students and Teachers"]
- `data/train.csv` (687812 bytes); columns: ["id", "Date", "Country", "Country ISO", "Admin 1", "Latitude", "Longitude", "Geo Precision", "Location of event", "Reported Perpetrator", "Reported Perpetrator Name", "Weapon Carried/Used", "Type of education facility", "Attacks on Schools", "Attacks on Universities", "Military Occupation of Education facility", "Arson attack on education facility", "Forced Entry into education facility", "Damage/Destruction To Ed facility Event", "Attacks on Students and Teachers", "Severe"]

## Public description

```
description.txt (30 lines)
sample_submission.csv (922 lines)
test.csv (922 lines)
train.csv (3687 lines)```

-> sample_submission.csv has 921 rows and 2 columns.
Here is some information about the columns:
Severe (float64) has range: 0.00 - 0.98, 0 nan values
id (int64) has range: 19026.00 - 100335.00, 0 nan values

-> test.csv has 921 rows and 20 columns.
Here is some information about the columns:
Admin 1 (object) has 251 unique values. Some example values: ['Gaza Strip', 'Sagaing Region', 'Dnipropetrovsk Oblast', 'West Bank']
Arson attack on education facility (int64) has 2 unique values: [0, 1]
Attacks on Schools (int64) has 2 unique values: [0, 1]
Attacks on Students and Teachers (bool) is 23.24% True, 76.76% False
Attacks on Universities (int64) has 2 unique values: [0, 1]
Country (object) has 54 unique values. Some example values: ['Myanmar', 'Ukraine', 'OPT', 'Nigeria']
Country ISO (object) has 53 unique values. Some example values: ['MMR', 'UKR', 'PSE', 'NGA']
Damage/Destruction To Ed facility Event (int64) has 2 unique values: [0, 1]
Date (object) has 670 unique values. Some example values: ['2022-04-03', '2024-07-27', '2024-01-12', '2023-12-29']
Forced Entry into education facility (int64) has 2 unique values: [0, 1]
Geo Precision (object) has 7 unique values: ['(2) 25 km Precision ', '(3) District, Communicipality or Commune ', '(4) Province, State, Governorate ', 'censored', '(6) Country', 'censored by HDX', '(5) Linear Feature e.g. Along Road/River ']
Latitude (float64) has range: -38.00 - 54.80, 133 nan values
Location of event (object) has 8 unique values: ['Unspecified Location', 'Education Building ', 'Private Travel', 'On Way To or From School', 'Other', 'Home', nan, 'Remote Threat', 'Public Building']
Longitude (float64) has range: -120.80 - 140.70, 133 nan values
Military Occupation of Education facility (int64) has 2 unique values: [0, 1]
Reported Perpetrator (object) has 12 unique values. Some example values: ['NSA', 'Other', 'Foreign Forces - Military', 'Host Government: Military']
Reported Perpetrator Name (object) has 128 unique values. Some example values: ['Armed Forces of the Russian Federation', 'Israeli Defence Forces', 'Myanmar Armed Forces', 'Unidentified Armed Actor']
Type of education facility (object) has 9 unique values: ['Not Applicable', 'Secondary School', 'School: No Further Details', 'Pre-School', 'University', 'Primary School', 'Primary School, Secondary School', 'Pre-School, School: No Further Details', 'Pre-School, Secondary School']
Weapon Carried/Used (object) has 34 unique values. Some example values: ['Firearms', 'Aerial Bomb: Plane', 'Aerial Bomb: Drone', 'Arson']
id (int64) has range: 19026.00 - 100335.00, 0 nan values

-> train.csv has 3686 rows and 21 columns.
Here is some information about the columns:
Admin 1 (object) has 521 unique values. Some example values: ['Gaza Strip', 'Sagaing Region', 'Mandalay', 'West Bank']
Arson attack on education facility (int64) has 2 unique values: [0, 1]
Attacks on Schools (int64) has 2 unique values: [1, 0]
Attacks on Students and Teachers (bool) is 22.57% True, 77.43% False
Attacks on Universities (int64) has 2 unique values: [0, 1]
Country (object) has 93 unique values. Some example values: ['Myanmar', 'Ukraine', 'OPT', 'Syria']
Country ISO (object) has 91 unique values. Some example values: ['MMR', 'UKR', 'PSE', 'SYR']
Damage/Destruction To Ed facility Event (int64) has 2 unique values: [0, 1]
Date (object) has 1454 unique values. Some example values: ['2022-04-03', '2021-03-07', '2024-12-25', '2024-05-17']
Forced Entry into education facility (int64) has 2 unique values: [0, 1]
Geo Precision (object) has 7 unique values: ['(4) Province, State, Governorate ', '(3) District, Communicipality or Commune ', '(2) 25 km Precision ', 'censored', '(6) Country', '(5) Linear Feature e.g. Along Road/River ', 'censored by HDX', nan]
Latitude (float64) has range: -38.60 - 56.80, 493 nan values
Location of event (object) has 8 unique values: ['Education Building ', 'Unspecified Location', 'Private Travel', 'Home', 'Other', 'Public Building', nan, 'On Way To or From School', 'Remote Threat']
Longitude (float64) has range: -111.90 - 144.10, 493 nan values
Military Occupation of Education facility (int64) has 2 unique values: [1, 0]
Reported Perpetrator (object) has 15 unique values. Some example values: ['NSA', 'Other', 'Foreign Forces - Military', 'Host Government: Military']
Reported Perpetrator Name (object) has 259 unique values. Some example values: ['Unidentified Armed Actor', 'Armed Forces of the Russian Federation', 'Myanmar Armed Forces', 'Israeli Defence Forces']
Severe (int64) has 2 unique values: [0, 1]
Type of education facility (object) has 14 unique values. Some example values: ['School: No Further Details', 'Not Applicable', 'Secondary School', 'University']
Weapon Carried/Used (object) has 49 unique values. Some example values: ['Firearms', 'Aerial Bomb: Plane', 'Arson', 'Aerial Bomb: Drone']
id (int64) has range: 19018.00 - 100334.00, 0 nan values
