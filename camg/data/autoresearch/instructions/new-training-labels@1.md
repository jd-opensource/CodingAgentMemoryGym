# OpenMLE-fast task

Task ID: `new-training-labels@1`

Native metric: `DataCitationMCCMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1403 bytes)
- `data/sample_submission.csv` (7428 bytes); columns: ["row_id", "type"]
- `data/test.csv` (23237 bytes); columns: ["row_id", "article_id", "dataset_id"]
- `data/train.csv` (82044 bytes); columns: ["row_id", "article_id", "dataset_id", "type"]

## Public description

```
description.txt (32 lines)
sample_submission.csv (506 lines)
test.csv (506 lines)
train.csv (1451 lines)```

-> sample_submission.csv has 505 rows and 2 columns.
Here is some information about the columns:
row_id (int64) has range: 1.00 - 1941.00, 0 nan values
type (object) has 2 unique values: ['Secondary', 'Primary']

-> test.csv has 505 rows and 3 columns.
Here is some information about the columns:
article_id (object) has 66 unique values. Some example values: ['10.3897_zookeys.500.9360', '10.7554_eLife.63194', '10.7717_peerj.10452', '10.1186_s12881-019-0773-3']
dataset_id (object) has 505 unique values. Some example values: ['https://doi.org/10.6084/m9.figshare.12763997.v1', 'https://doi.org/10.17882/49388', 'https://doi.org/10.17882/47142', 'https://doi.org/10.5061/dryad.6fp82p0']
row_id (int64) has range: 1.00 - 1941.00, 0 nan values

-> train.csv has 1450 rows and 4 columns.
Here is some information about the columns:
article_id (object) has 212 unique values. Some example values: ['10.1128_spectrum.00422-24', '10.1371_journal.pone.0170126', '10.1111_bph.14747', '10.7554_elife.29944']
dataset_id (object) has 1447 unique values. Some example values: ['https://doi.org/10.24381/cds.adbb2d47', 'GCA_000007825.1', 'https://doi.org/10.5066/f7930r7p', 'PXD032899']
row_id (int64) has range: 3.00 - 1955.00, 0 nan values
type (object) has 2 unique values: ['Primary', 'Secondary']
