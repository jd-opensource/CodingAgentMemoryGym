# OpenMLE-fast task

Task ID: `drug-pharma-new-dataset@1`

Native metric: `DrugPharmaClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2641 bytes)
- `data/sample_submission.csv` (304285 bytes); columns: ["id", "Type", "Dosages Description"]
- `data/test.csv` (1541340 bytes); columns: ["id", "Name of the Manufacturer", "Brand Name", "Generic Name and Strength", "text"]
- `data/train.csv` (6988522 bytes); columns: ["id", "Name of the Manufacturer", "Brand Name", "Generic Name and Strength", "text", "Type", "Dosages Description"]

## Public description

```
description.txt (48 lines)
sample_submission.csv (10717 lines)
test.csv (10717 lines)
train.csv (42863 lines)```

-> sample_submission.csv has 10716 rows and 3 columns.
Here is some information about the columns:
Dosages Description (object) has 171 unique values. Some example values: ['Needle for Syringe', 'Vaginal Suppository', 'Dust', 'Rectal Ointment']
Type (object) has 5 unique values: ['Ayurvedic', 'Homeopathic', 'Unani', 'Allopathic', 'Herbal']
id (int64) has range: 4.00 - 53574.00, 0 nan values

-> test.csv has 10716 rows and 5 columns.
Here is some information about the columns:
Brand Name (object) has 9022 unique values. Some example values: ['Ashokarista', 'Sharbat Jinsin', 'Aswagandharista', 'Water For Injection']
Generic Name and Strength (object) has 2834 unique values. Some example values: ['Sharbat Jinsin', 'Ashokarista', 'Aswagandharista', 'Sharbat Musaffi']
Name of the Manufacturer (object) has 679 unique values. Some example values: ['Incepta Pharmaceuticals Ltd.', 'Opsonin Pharma Limited', 'Square Pharmaceuticals PLC, Pabna', 'The ACME Laboratories Ltd.']
id (int64) has range: 4.00 - 53574.00, 0 nan values
text (object) has 10624 unique values. Some example values: ['Drug International Ltd. | Azimex 500 | Azithromycin500 mg', 'Synovia Pharma PLC. | Fimoxyl 250 | Amoxicillin250 mg', 'S. B. Laboratories (Ayurvedic) | Leciplus | Soya Lecithin Vitamineral Mix', 'Opsonin Pharma Limited | Moxin 250 | Amoxicillin250 mg']

-> train.csv has 42862 rows and 7 columns.
Here is some information about the columns:
Brand Name (object) has 36232 unique values. Some example values: ['Water for Injection', 'Sharbat Faulad', 'Chandanasav', 'Ginseng']
Dosages Description (object) has 171 unique values. Some example values: ['Tablet', 'Capsule', 'Liquid', 'Injection']
Generic Name and Strength (object) has 4835 unique values. Some example values: ['Esomeprazole20 mg', 'Sharbat Faulad', 'Sharbat Deenar', 'Sharbat Buzuri']
Name of the Manufacturer (object) has 723 unique values. Some example values: ['Incepta Pharmaceuticals Ltd.', 'Opsonin Pharma Limited', 'Square Pharmaceuticals PLC, Pabna', 'Advanced Chemical Industries Limited']
Type (object) has 5 unique values: ['Allopathic', 'Ayurvedic', 'Herbal', 'Homeopathic', 'Unani']
id (int64) has range: 1.00 - 53578.00, 0 nan values
text (object) has 42494 unique values. Some example values: ['Incepta Pharmaceuticals Ltd. | Esonix 20 | Esomeprazole20 mg', 'Opsonin Pharma Limited | Moxin 500 | Amoxicillin500 mg', 'Neptune Laboratories Ltd. | Gastocon | Sufoof Humuzin', 'Square Pharmaceuticals PLC, Pabna | Nacromin 2% | Sodium Cromoglycate20 mg/ml']
