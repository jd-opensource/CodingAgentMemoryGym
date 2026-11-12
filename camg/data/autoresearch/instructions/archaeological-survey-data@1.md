# OpenMLE-fast task

Task ID: `archaeological-survey-data@1`

Native metric: `ArchaeologicalFeatureTriageMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (848 bytes)
- `data/sample_submission.csv` (12633 bytes); columns: ["id", "type"]
- `data/test.csv` (352765 bytes); columns: ["id", "wc2.1_30s_bio_1", "wc2.1_30s_bio_10", "wc2.1_30s_bio_11", "wc2.1_30s_bio_12", "wc2.1_30s_bio_13", "wc2.1_30s_bio_14", "wc2.1_30s_bio_15", "wc2.1_30s_bio_16", "wc2.1_30s_bio_17", "wc2.1_30s_bio_18", "wc2.1_30s_bio_19", "wc2.1_30s_bio_2", "wc2.1_30s_bio_3", "wc2.1_30s_bio_4", "wc2.1_30s_bio_5", "wc2.1_30s_bio_6", "wc2.1_30s_bio_7", "wc2.1_30s_bio_8", "wc2.1_30s_bio_9", "wc2.1_30s_elev", "pest", "distriver1", "distriver2", "distriver3", "rivtype", "distlake", "distshore", "agpot", "distblack", "distclear", "distwhite", "npp", "T_SILT", "phsoil", "T_GRAVEL", "S_CEC_CLAY", "T_PH_H2O", "S_SAND", "S_GRAVEL", "mgs", "nure", "nuav", "rug", "nitrogen", "bdod", "cec", "cfvo", "clay", "phh2o", "sand", "silt", "soc", "phos", "smn30cm", "smc30cm", "T_C", "S_C", "T_OC", "S_OC", "AWT_S_OC", "AWT_T_OC", "AWC", "T_CEC_CLAY", "T_BULK_DEN", "S_BULK_DEN"]
- `data/train.csv` (678015 bytes); columns: ["id", "type", "wc2.1_30s_bio_1", "wc2.1_30s_bio_10", "wc2.1_30s_bio_11", "wc2.1_30s_bio_12", "wc2.1_30s_bio_13", "wc2.1_30s_bio_14", "wc2.1_30s_bio_15", "wc2.1_30s_bio_16", "wc2.1_30s_bio_17", "wc2.1_30s_bio_18", "wc2.1_30s_bio_19", "wc2.1_30s_bio_2", "wc2.1_30s_bio_3", "wc2.1_30s_bio_4", "wc2.1_30s_bio_5", "wc2.1_30s_bio_6", "wc2.1_30s_bio_7", "wc2.1_30s_bio_8", "wc2.1_30s_bio_9", "wc2.1_30s_elev", "pest", "distriver1", "distriver2", "distriver3", "rivtype", "distlake", "distshore", "agpot", "distblack", "distclear", "distwhite", "npp", "T_SILT", "phsoil", "T_GRAVEL", "S_CEC_CLAY", "T_PH_H2O", "S_SAND", "S_GRAVEL", "mgs", "nure", "nuav", "rug", "nitrogen", "bdod", "cec", "cfvo", "clay", "phh2o", "sand", "silt", "soc", "phos", "smn30cm", "smc30cm", "T_C", "S_C", "T_OC", "S_OC", "AWT_S_OC", "AWT_T_OC", "AWC", "T_CEC_CLAY", "T_BULK_DEN", "S_BULK_DEN"]

## Public description

```
description.txt (44 lines)
sample_submission.csv (718 lines)
test.csv (718 lines)
train.csv (1365 lines)```

-> sample_submission.csv has 717 rows and 2 columns.
The columns are: id, type

-> test.csv has 717 rows and 66 columns.
The columns are: id, wc2.1_30s_bio_1, wc2.1_30s_bio_10, wc2.1_30s_bio_11, wc2.1_30s_bio_12, wc2.1_30s_bio_13, wc2.1_30s_bio_14, wc2.1_30s_bio_15, wc2.1_30s_bio_16, wc2.1_30s_bio_17, wc2.1_30s_bio_18, wc2.1_30s_bio_19, wc2.1_30s_bio_2, wc2.1_30s_bio_3, wc2.1_30s_bio_4... and 51 more columns

-> train.csv has 1364 rows and 67 columns.
The columns are: id, type, wc2.1_30s_bio_1, wc2.1_30s_bio_10, wc2.1_30s_bio_11, wc2.1_30s_bio_12, wc2.1_30s_bio_13, wc2.1_30s_bio_14, wc2.1_30s_bio_15, wc2.1_30s_bio_16, wc2.1_30s_bio_17, wc2.1_30s_bio_18, wc2.1_30s_bio_19, wc2.1_30s_bio_2, wc2.1_30s_bio_3... and 52 more columns
