# OpenMLE-fast task

Task ID: `philippins-employment-agency-status-from-dmws@1`

Native metric: `AgencyLicenseValidityMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3489 bytes)
- `data/sample_submission.csv` (9060 bytes); columns: ["id", "is_valid"]
- `data/test.csv` (142944 bytes); columns: ["id", "name", "classification", "representative", "address", "municipality_province", "city_province", "contact_number", "email"]
- `data/train.csv` (576173 bytes); columns: ["id", "name", "classification", "representative", "address", "municipality_province", "city_province", "contact_number", "email", "is_valid"]

## Public description

```
description.txt (50 lines)
sample_submission.csv (755 lines)
test.csv (755 lines)
train.csv (3017 lines)```

-> sample_submission.csv has 754 rows and 2 columns.
Here is some information about the columns:
id (object) has 754 unique values. Some example values: ['A003653', 'A001733', 'A002582', 'A002308']
is_valid (float64) has 1 unique values: [0.5]

-> test.csv has 754 rows and 9 columns.
Here is some information about the columns:
address (object) has 754 unique values. Some example values: ['2/F, BLOCK 3 LOT 1 SAPPHIRE ST, SOLDIERS HILLS III SUBD, BRGY 180, TALA', '1575 P.CAMPA ST SAMPALOC MANILA', '1069 HONDURAS ST MAKATI M.M.', '2440-B F.B.HARRISON COR PALM COURT PASAY CITY']
city_province (object) has 23 unique values. Some example values: ['MANILA', 'MAKATI', 'QUEZON CITY', 'PASAY CITY']
classification (object) has 6 unique values: ['Manning Agency', 'Private Employment Agency', 'Construction Contractor', 'Service Contractor', 'Philippine Registered Vessel', 'Authority to negotiate']
contact_number (object) has 697 unique values. Some example values: ['FOR INSTALLATION', '+63 8526 7992 / +63 8525 1031', '5272339 / 7641031', '2863842']
email (object) has 360 unique values. Some example values: [' ', 'simscor_philippines@yahoo.com ', 'info@mychesna.com', 'admin@farland.ph']
id (object) has 754 unique values. Some example values: ['A003653', 'A001733', 'A002582', 'A002308']
municipality_province (object) has 62 unique values. Some example values: ['N.S. (Municipality Not Stated)', 'ERMITA', 'MALATE', 'LEGASPI VILLAGE']
name (object) has 754 unique values. Some example values: ['WANDY OVERSEAS PLACEMENT AGENCY, INC.', 'JEDEC SERVICES INC ', 'PALUMAR ENTERPRISES ', 'MORNING SUN SHIPPING SERVICES(FOR. MARI- LAG SHIPPING SVCS)']
representative (object) has 729 unique values. Some example values: ['NONE', 'MR BONIFACIO F GOMEZ', 'JOSEPHINE J FRANCISCO', 'MR NICASIO T TIMTIMAN']

-> train.csv has 3016 rows and 10 columns.
Here is some information about the columns:
address (object) has 3002 unique values. Some example values: ['RCM BLDG 1418 SAN MARCELINO ST', '3794 CUENCA ST PALANAN MAKATI CITY', '685 QUEZON AVE QUEZON CITY', 'RM 202 2F KIMVI BLDG 1191 MA OROSA ST']
city_province (object) has 41 unique values. Some example values: ['MANILA', 'MAKATI', 'QUEZON CITY', 'PASAY CITY']
classification (object) has 8 unique values: ['Manning Agency', 'Construction Contractor', 'Private Employment Agency', 'Service Contractor', 'Philippine Registered Vessel', 'Authority to negotiate', 'Philippine Overseas Construction Board', 'Philippine Overseas Shipping Enterprise']
contact_number (object) has 2705 unique values. Some example values: [' ', 'FOR INSTALLATION', 'NONE', '5211566 / 5211567']
email (object) has 1507 unique values. Some example values: [' ', 'oriman@oriental.com.ph', 'oeg@sos.com.ph', 'NONE']
id (object) has 3016 unique values. Some example values: ['A001254', 'A002344', 'A000113', 'A002720']
is_valid (int64) has 2 unique values: [1, 0]
municipality_province (object) has 128 unique values. Some example values: ['N.S. (Municipality Not Stated)', 'ERMITA', 'MALATE', 'PALANAN']
name (object) has 3013 unique values. Some example values: ['PACIFIC SEAMEN SERVICES INC', 'ASIAN PROSPERITY LINES INC. ', 'CRESTAMONTE SHIPPING CORPORATION ', 'MANASIA INC (FOR MANN (ASIA) RESOURCES DEV CORP)']
representative (object) has 2851 unique values. Some example values: ['NONE', 'PRESIDENT', 'GREGORIO F ORTEGA', 'CAPT ROSENDO C HERRERA']
