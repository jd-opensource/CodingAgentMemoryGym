# OpenMLE-fast task

Task ID: `tc-smiles@1`

Native metric: `TcSmilesRegressionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (995 bytes)
- `data/sample_submission.csv` (4078 bytes); columns: ["id", "TC_mean"]
- `data/test.csv` (6619 bytes); columns: ["id", "SMILES"]
- `data/train.csv` (32914 bytes); columns: ["id", "SMILES", "TC_mean"]

## Public description

```
description.txt (31 lines)
sample_submission.csv (176 lines)
test.csv (176 lines)
train.csv (700 lines)```

-> sample_submission.csv has 175 rows and 2 columns.
Here is some information about the columns:
TC_mean (float64) has range: 0.05 - 0.49, 0 nan values
id (int64) has range: 699.00 - 873.00, 0 nan values

-> test.csv has 175 rows and 2 columns.
Here is some information about the columns:
SMILES (object) has 173 unique values. Some example values: ['*/C=C/CCCCCCCC*', '*/C=C/*', '*c1sc(*)c(OCCCCCCCCCCCC)c1C', '*C(*)C']
id (int64) has range: 699.00 - 873.00, 0 nan values

-> train.csv has 699 rows and 3 columns.
Here is some information about the columns:
SMILES (object) has 694 unique values. Some example values: ['*CC/C=C(/*)C', '*/C=C/CC*', '*/C=C/CCC*', '*C1=NC2=CC(=CC=C2N1)C1=CC2=C(NC(O2)C2=CC=C(OC3=CC=C(OC4=CC=C(*)C=C4)C4=C3C3C5=C(C=CC=C5)C4C4=C3C=CC=C4)C=C2)C=C1']
TC_mean (float64) has range: 0.05 - 1.59, 0 nan values
id (int64) has range: 0.00 - 698.00, 0 nan values
