# OpenMLE-fast task

Task ID: `pakistan-hopitals-dataset@1`

Native metric: `PakistanHospitalDoctorCountMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/aux_area_counts.csv` (56519 bytes); columns: ["CITY", "AREA", "TOTAL HOSPITALS"]
- `data/aux_city_counts.csv` (1491 bytes); columns: ["CITY", "TOTAL HOSPITALS"]
- `data/description.txt` (3161 bytes)
- `data/sample_submission.csv` (9981 bytes); columns: ["row_id", "DOCTORS"]
- `data/test.csv` (188303 bytes); columns: ["row_id", "HOSPITAL NAME", "CITY", "AREA", "ADDRESS", "CONTACT"]
- `data/train.csv` (765497 bytes); columns: ["row_id", "HOSPITAL NAME", "CITY", "AREA", "ADDRESS", "CONTACT", "DOCTORS"]

## Public description

```
aux_area_counts.csv (2191 lines)
aux_city_counts.csv (128 lines)
description.txt (37 lines)
sample_submission.csv (1228 lines)
test.csv (1228 lines)
train.csv (4921 lines)```

-> aux_area_counts.csv has 2190 rows and 3 columns.
Here is some information about the columns:
AREA (object) has 1665 unique values. Some example values: ['Punjab', 'Civil Lines', 'Model Town', 'Opposite Police Station Defence A On Ghazi Road']
CITY (object) has 127 unique values. Some example values: ['Lahore', 'Rawalpindi', 'Faisalabad', 'Multan']
TOTAL HOSPITALS (int64) has range: 1.00 - 1403.00, 0 nan values

-> aux_city_counts.csv has 127 rows and 2 columns.
Here is some information about the columns:
CITY (object) has 127 unique values. Some example values: ['Abbottabad', 'Alipur', 'Attock', 'Baden']
TOTAL HOSPITALS (int64) has range: 1.00 - 2315.00, 0 nan values

-> sample_submission.csv has 1227 rows and 2 columns.
Here is some information about the columns:
DOCTORS (int64) has range: 1.00 - 155.00, 0 nan values
row_id (int64) has range: 12.00 - 6144.00, 0 nan values

-> test.csv has 1227 rows and 6 columns.
Here is some information about the columns:
ADDRESS (object) has 1227 unique values. Some example values: ['Makkah Medical Store Hospital, Opposite Dhq, Link Road, Near Dhq Laboratory, Abbottabad', 'Ramzi Brain And Spine Center, Nishtar Rd, Al Rahim Colony, Multan', 'Zaha Aesthetics Hospital, Dost Plaza, Nishtar Rd, Al Rahim Colony, Multan', 'Physiofitness Hospital, Shah Rukne Alam Colony-299, B Block, Multan']
AREA (object) has 472 unique values. Some example values: ['0', 'Johar Town', 'Model Town', 'Bahria Town']
CITY (object) has 82 unique values. Some example values: ['Lahore', 'Karachi', 'Islamabad', 'Rawalpindi']
CONTACT (object) has 1086 unique values. Some example values: ['3111222398', '042-32591432', '042-32591427', '4232591427']
HOSPITAL NAME (object) has 1226 unique values. Some example values: ['Shifa Hospital', 'Unicare Medical Centre', 'Karimia Medical Centre', 'Dental Avenue Hospital']
row_id (int64) has range: 12.00 - 6144.00, 0 nan values

-> train.csv has 4920 rows and 7 columns.
Here is some information about the columns:
ADDRESS (object) has 4920 unique values. Some example values: ['Similia Homoeo Clinix Hospital, 18.China Center, The Mall, The Mall, Abbottabad', 'Al Rehman Medicure Clinic, Hasnabad Gate No 1, 0, Multan', 'The Physio Clinic, Khan Centre, Abdali Rd, Adali Colony, Multan', 'National Diagnostic Center, Suraj Miani Road, Ahsan Colony, Multan']
AREA (object) has 1162 unique values. Some example values: ['0', 'Johar Town', 'Model Town', 'Punjab']
CITY (object) has 120 unique values. Some example values: ['Lahore', 'Karachi', 'Islamabad', 'Rawalpindi']
CONTACT (object) has 4180 unique values. Some example values: ['3111222398', '042-32591432', '042-32591427', '4232591427']
DOCTORS (int64) has range: 1.00 - 155.00, 0 nan values
HOSPITAL NAME (object) has 4910 unique values. Some example values: ['Ali Medical Complex Hospital', 'Surgicare Complex Hospital', 'Dar Ul Shifa Hospital', 'Alkareem Medical And Surgical Complex Hospital']
row_id (int64) has range: 0.00 - 6146.00, 0 nan values
