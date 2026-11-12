# OpenMLE-fast task

Task ID: `trkiye-il-ile-listesi@1`

Native metric: `TurkeyProvinceDistrictLogLossMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1051 bytes)
- `data/sample_submission.csv` (13623 bytes); columns: ["id", "target"]
- `data/test.csv` (21921 bytes); columns: ["id", "il", "ilce"]
- `data/train.csv` (97706 bytes); columns: ["id", "il", "ilce", "target"]

## Public description

```
description.txt (38 lines)
sample_submission.csv (981 lines)
test.csv (981 lines)
train.csv (3886 lines)```

-> sample_submission.csv has 980 rows and 2 columns.
Here is some information about the columns:
id (int64) has range: 1.00 - 980.00, 0 nan values
target (float64) has range: 0.00 - 1.00, 0 nan values

-> test.csv has 980 rows and 3 columns.
Here is some information about the columns:
id (int64) has range: 1.00 - 980.00, 0 nan values
il (object) has 81 unique values. Some example values: ['İstanbul', 'Konya', 'İzmir', 'Ankara']
ilce (object) has 637 unique values. Some example values: ['Marmaraereğlisi', 'Palandöken', 'Göynücek', 'Çiftlik']

-> train.csv has 3885 rows and 4 columns.
Here is some information about the columns:
id (int64) has range: 1.00 - 3885.00, 0 nan values
il (object) has 81 unique values. Some example values: ['İstanbul', 'Konya', 'İzmir', 'Ankara']
ilce (object) has 945 unique values. Some example values: ['Akhisar', 'Sarıçam', 'Beşiri', 'Kozaklı']
target (int64) has 2 unique values: [0, 1]
