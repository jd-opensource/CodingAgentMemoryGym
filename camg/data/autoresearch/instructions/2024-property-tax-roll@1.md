# OpenMLE-fast task

Task ID: `2024-property-tax-roll@1`

Native metric: `PropertyAssessmentMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4035 bytes)
- `data/sample_submission.csv` (213126 bytes); columns: ["P_ID", "TOTAL_ASSMT"]
- `data/test.csv` (1479683 bytes); columns: ["P_ID", "TAX_MAP", "plat", "lot", "unit", "CLASS", "SHORT_DESC", "LEVY_CODE_1", "SHORT_DESC 1", "CIVIC", "STREET", "SUFFIX", "FORMATED_ADDRESS", "CITY", "ZIP_POSTAL", "Property_Location", "lon", "lat"]
- `data/train.csv` (6188727 bytes); columns: ["P_ID", "TAX_MAP", "plat", "lot", "unit", "CLASS", "SHORT_DESC", "LEVY_CODE_1", "SHORT_DESC 1", "CIVIC", "STREET", "SUFFIX", "FORMATED_ADDRESS", "CITY", "ZIP_POSTAL", "Property_Location", "lon", "lat", "TOTAL_ASSMT"]

## Public description

```
description.txt (46 lines)
sample_submission.csv (8836 lines)
test.csv (8836 lines)
train.csv (35199 lines)```

-> sample_submission.csv has 8835 rows and 2 columns.
Here is some information about the columns:
P_ID (int64) has range: 4.00 - 79000.00, 0 nan values
TOTAL_ASSMT (float64) has range: 2132.95 - 25112842.61, 0 nan values

-> test.csv has 8835 rows and 18 columns.
Here is some information about the columns:
CITY (object) has 3 unique values: ['Providence', 'Providence, RI', nan, 'Provience']
CIVIC (float64) has range: 0.00 - 1496.00, 22 nan values
CLASS (int64) has range: 1.00 - 84.00, 0 nan values
FORMATED_ADDRESS (object) has 8097 unique values. Some example values: ['1000 Providence Pl', '1 Randall Sq', '178 Bowen St', '160 Waterman St']
LEVY_CODE_1 (object) has 7 unique values: ['C01', 'OO01', 'E01', 'NO01', '8LAW', 'PRA', 'TSA']
P_ID (int64) has range: 4.00 - 79000.00, 0 nan values
Property_Location (object) has 7725 unique values. Some example values: ['POINT (-71.421716004 41.827929994)', 'POINT (-71.410529013 41.83695898)', 'POINT (-71.420743033 41.81829399)', 'POINT (-71.415202008 41.837433019)']
SHORT_DESC (object) has 25 unique values. Some example values: ['Single Family', '2 -5 Family', 'Residential Condo', 'Residential Vacant Land']
SHORT_DESC 1 (object) has 7 unique values: ['C01', 'OO01', 'Non Residential Exempt', 'NO01', '8LAW', 'PRA', 'TSA']
STREET (object) has 468 unique values. Some example values: ['Providence', 'Douglas', 'Washington', 'Indiana']
SUFFIX (object) has 12 unique values. Some example values: ['St', 'Ave', 'Pl', 'Dr']
TAX_MAP (object) has 8835 unique values. Some example values: ['068-0843-0000', '000-0001-0022', '005-0514-0000', '024-0675-0000']
ZIP_POSTAL (object) has 24 unique values. Some example values: ['02908', '02905', '02906', '02909']
lat (float64) has range: 41.77 - 41.97, 0 nan values
lon (float64) has range: -71.55 - -71.38, 0 nan values
lot (int64) has range: 1.00 - 1127.00, 0 nan values
plat (int64) has range: 0.00 - 123.00, 0 nan values
unit (object) has 683 unique values. Some example values: ['0000', '8LAW', '0002', '0001']

-> train.csv has 35198 rows and 19 columns.
Here is some information about the columns:
CITY (object) has 5 unique values: ['Providence', nan, 'Providence, RI', 'PROVIDENCE', 'Providence, Ri', 'Providence,RI']
CIVIC (float64) has range: 0.00 - 1955.00, 73 nan values
CLASS (int64) has range: 1.00 - 84.00, 0 nan values
FORMATED_ADDRESS (object) has 33655 unique values. Some example values: ['130 Westminster St', '555 South Water St', '30 Bridge St', '28 Bassett St']
LEVY_CODE_1 (object) has 8 unique values: ['OO01', 'E01', 'C01', 'NO01', '8LAW', 'TSA', 'PRA', 'R01']
P_ID (int64) has range: 16.00 - 79006.00, 0 nan values
Property_Location (object) has 31889 unique values. Some example values: ['POINT (-71.401528023 41.817893)', 'POINT (-71.412771005 41.82738802)', 'POINT (-71.41086668 41.824112268)', 'POINT (-71.388764983 41.825365006)']
SHORT_DESC (object) has 27 unique values. Some example values: ['Single Family', '2 -5 Family', 'Residential Condo', 'Residential Vacant Land']
SHORT_DESC 1 (object) has 8 unique values: ['OO01', 'Non Residential Exempt', 'C01', 'NO01', '8LAW', 'TSA', 'PRA', 'RE Tax']
STREET (object) has 1443 unique values. Some example values: ['Westminster', 'Hope', 'Manton', 'Atwells']
SUFFIX (object) has 16 unique values. Some example values: ['St', 'Ave', 'Rd', 'Dr']
TAX_MAP (object) has 35198 unique values. Some example values: ['025-0155-R304', '077-0893-0000', '008-0350-0000', '016-0560-0000']
TOTAL_ASSMT (float64) has range: 0.00 - 708726600.00, 0 nan values
ZIP_POSTAL (object) has 68 unique values. Some example values: ['02909', '02906', '02905', '02907']
lat (float64) has range: 41.73 - 42.00, 0 nan values
lon (float64) has range: -71.62 - -71.34, 0 nan values
lot (int64) has range: 0.00 - 1197.00, 0 nan values
plat (int64) has range: 1.00 - 129.00, 0 nan values
unit (object) has 1008 unique values. Some example values: ['0000', '8LAW', '0001', '0002']
