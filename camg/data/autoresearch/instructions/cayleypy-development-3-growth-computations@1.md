# OpenMLE-fast task

Task ID: `cayleypy-development-3-growth-computations@1`

Native metric: `CayleyWordDistanceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2067 bytes)
- `data/sample_submission.csv` (31177 bytes); columns: ["id", "distance"]
- `data/test.csv` (205759 bytes); columns: ["id", "puzzle", "perm"]
- `data/train.csv` (1551084 bytes); columns: ["id", "puzzle", "perm", "distance"]

## Public description

```
description.txt (43 lines)
sample_submission.csv (1114 lines)
test.csv (1114 lines)
train.csv (15828 lines)```

-> sample_submission.csv has 1113 rows and 2 columns.
Here is some information about the columns:
distance (int64) has 7 unique values: [1, 4, 5, 2, 0, 6, 3]
id (object) has 1113 unique values. Some example values: ['s_3x3x3_d9664a5baba41c35', 's_3x3x3_b8e24ef1302a857a', 's_3x3x3_812228e8eb2eb342', 's_3x3x3_2d9cb88fc2f4d0a7']

-> test.csv has 1113 rows and 3 columns.
Here is some information about the columns:
id (object) has 1113 unique values. Some example values: ['s_3x3x3_d9664a5baba41c35', 's_3x3x3_b8e24ef1302a857a', 's_3x3x3_812228e8eb2eb342', 's_3x3x3_2d9cb88fc2f4d0a7']
perm (object) has 1113 unique values. Some example values: ['3 1 2 20 21 19 4 5 6 7 8 9 24 22 23 11 12 10 13 14 15 16 17 18 31 32 42 41 27 28 29 30 44 43 39 40 33 34 35 36 38 37 26 25 45 46 47 48', '17 18 16 6 4 5 9 7 8 12 10 11 2 3 1 13 14 15 21 19 20 24 22 23 43 44 25 26 45 46 29 30 35 36 41 42 47 48 33 34 27 28 39 40 37 38 31 32', '3 1 2 22 23 24 18 16 17 7 8 9 4 5 6 11 12 10 19 20 21 14 15 13 31 32 42 41 35 36 29 30 44 43 27 28 37 38 39 40 45 46 26 25 34 33 47 48', '3 1 2 6 4 5 9 7 8 12 10 11 18 16 17 21 19 20 14 15 13 24 22 23 28 27 45 46 32 31 26 25 44 43 41 42 36 35 47 48 34 33 39 40 30 29 38 37']
puzzle (object) has 2 unique values: ['3x3x3', '4x4x4']

-> train.csv has 15827 rows and 4 columns.
Here is some information about the columns:
distance (int64) has 7 unique values: [5, 6, 4, 3, 2, 1, 0]
id (object) has 15827 unique values. Some example values: ['s_2x2x2_c0e60b7eed6fb31a', 's_2x2x2_d32096f653032105', 's_2x2x2_bf9382919f2dc94b', 's_2x2x2_94d6473111c15104']
perm (object) has 15827 unique values. Some example values: ['17 18 16 3 1 2 21 19 20 24 22 23 11 12 10 9 7 8 4 5 6 15 13 14', '9 7 8 12 10 11 20 21 19 1 2 3 5 6 4 16 17 18 14 15 13 24 22 23', '18 16 17 14 15 13 9 7 8 22 23 24 12 10 11 3 1 2 21 19 20 5 6 4', '24 22 23 4 5 6 7 8 9 16 17 18 3 1 2 20 21 19 11 12 10 13 14 15']
puzzle (object) has 2 unique values: ['2x2x2', '3x3x3']
