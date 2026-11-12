# OpenMLE-fast task

Task ID: `air-quality-dataset@2`

Native metric: `AirQualityForecastMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (869 bytes)
- `data/sample_submission.csv` (9228 bytes); columns: ["row_id", "NO2_GT"]
- `data/test.csv` (558939 bytes); columns: ["row_id", "PT08_S1_CO_lag1", "PT08_S1_CO_lag2", "PT08_S1_CO_lag3", "PT08_S1_CO_lag4", "PT08_S1_CO_lag5", "PT08_S1_CO_lag6", "PT08_S1_CO_lag7", "PT08_S1_CO_lag8", "PT08_S1_CO_lag9", "PT08_S1_CO_lag10", "PT08_S1_CO_lag11", "PT08_S1_CO_lag12", "PT08_S2_NMHC_lag1", "PT08_S2_NMHC_lag2", "PT08_S2_NMHC_lag3", "PT08_S2_NMHC_lag4", "PT08_S2_NMHC_lag5", "PT08_S2_NMHC_lag6", "PT08_S2_NMHC_lag7", "PT08_S2_NMHC_lag8", "PT08_S2_NMHC_lag9", "PT08_S2_NMHC_lag10", "PT08_S2_NMHC_lag11", "PT08_S2_NMHC_lag12", "PT08_S3_NOx_lag1", "PT08_S3_NOx_lag2", "PT08_S3_NOx_lag3", "PT08_S3_NOx_lag4", "PT08_S3_NOx_lag5", "PT08_S3_NOx_lag6", "PT08_S3_NOx_lag7", "PT08_S3_NOx_lag8", "PT08_S3_NOx_lag9", "PT08_S3_NOx_lag10", "PT08_S3_NOx_lag11", "PT08_S3_NOx_lag12", "PT08_S4_NO2_lag1", "PT08_S4_NO2_lag2", "PT08_S4_NO2_lag3", "PT08_S4_NO2_lag4", "PT08_S4_NO2_lag5", "PT08_S4_NO2_lag6", "PT08_S4_NO2_lag7", "PT08_S4_NO2_lag8", "PT08_S4_NO2_lag9", "PT08_S4_NO2_lag10", "PT08_S4_NO2_lag11", "PT08_S4_NO2_lag12", "PT08_S5_O3_lag1", "PT08_S5_O3_lag2", "PT08_S5_O3_lag3", "PT08_S5_O3_lag4", "PT08_S5_O3_lag5", "PT08_S5_O3_lag6", "PT08_S5_O3_lag7", "PT08_S5_O3_lag8", "PT08_S5_O3_lag9", "PT08_S5_O3_lag10", "PT08_S5_O3_lag11", "PT08_S5_O3_lag12", "T_lag1", "T_lag2", "T_lag3", "T_lag4", "T_lag5", "T_lag6", "T_lag7", "T_lag8", "T_lag9", "T_lag10", "T_lag11", "T_lag12", "RH_lag1", "RH_lag2", "RH_lag3", "RH_lag4", "RH_lag5", "RH_lag6", "RH_lag7", "RH_lag8", "RH_lag9", "RH_lag10", "RH_lag11", "RH_lag12", "AH_lag1", "AH_lag2", "AH_lag3", "AH_lag4", "AH_lag5", "AH_lag6", "AH_lag7", "AH_lag8", "AH_lag9", "AH_lag10", "AH_lag11", "AH_lag12", "hour_sin", "hour_cos", "dow_sin", "dow_cos", "month_sin", "month_cos"]
- `data/train.csv` (4560953 bytes); columns: ["row_id", "PT08_S1_CO_lag1", "PT08_S1_CO_lag2", "PT08_S1_CO_lag3", "PT08_S1_CO_lag4", "PT08_S1_CO_lag5", "PT08_S1_CO_lag6", "PT08_S1_CO_lag7", "PT08_S1_CO_lag8", "PT08_S1_CO_lag9", "PT08_S1_CO_lag10", "PT08_S1_CO_lag11", "PT08_S1_CO_lag12", "PT08_S2_NMHC_lag1", "PT08_S2_NMHC_lag2", "PT08_S2_NMHC_lag3", "PT08_S2_NMHC_lag4", "PT08_S2_NMHC_lag5", "PT08_S2_NMHC_lag6", "PT08_S2_NMHC_lag7", "PT08_S2_NMHC_lag8", "PT08_S2_NMHC_lag9", "PT08_S2_NMHC_lag10", "PT08_S2_NMHC_lag11", "PT08_S2_NMHC_lag12", "PT08_S3_NOx_lag1", "PT08_S3_NOx_lag2", "PT08_S3_NOx_lag3", "PT08_S3_NOx_lag4", "PT08_S3_NOx_lag5", "PT08_S3_NOx_lag6", "PT08_S3_NOx_lag7", "PT08_S3_NOx_lag8", "PT08_S3_NOx_lag9", "PT08_S3_NOx_lag10", "PT08_S3_NOx_lag11", "PT08_S3_NOx_lag12", "PT08_S4_NO2_lag1", "PT08_S4_NO2_lag2", "PT08_S4_NO2_lag3", "PT08_S4_NO2_lag4", "PT08_S4_NO2_lag5", "PT08_S4_NO2_lag6", "PT08_S4_NO2_lag7", "PT08_S4_NO2_lag8", "PT08_S4_NO2_lag9", "PT08_S4_NO2_lag10", "PT08_S4_NO2_lag11", "PT08_S4_NO2_lag12", "PT08_S5_O3_lag1", "PT08_S5_O3_lag2", "PT08_S5_O3_lag3", "PT08_S5_O3_lag4", "PT08_S5_O3_lag5", "PT08_S5_O3_lag6", "PT08_S5_O3_lag7", "PT08_S5_O3_lag8", "PT08_S5_O3_lag9", "PT08_S5_O3_lag10", "PT08_S5_O3_lag11", "PT08_S5_O3_lag12", "T_lag1", "T_lag2", "T_lag3", "T_lag4", "T_lag5", "T_lag6", "T_lag7", "T_lag8", "T_lag9", "T_lag10", "T_lag11", "T_lag12", "RH_lag1", "RH_lag2", "RH_lag3", "RH_lag4", "RH_lag5", "RH_lag6", "RH_lag7", "RH_lag8", "RH_lag9", "RH_lag10", "RH_lag11", "RH_lag12", "AH_lag1", "AH_lag2", "AH_lag3", "AH_lag4", "AH_lag5", "AH_lag6", "AH_lag7", "AH_lag8", "AH_lag9", "AH_lag10", "AH_lag11", "AH_lag12", "hour_sin", "hour_cos", "dow_sin", "dow_cos", "month_sin", "month_cos", "NO2_GT"]

## Public description

```
description.txt (43 lines)
sample_submission.csv (809 lines)
test.csv (809 lines)
train.csv (6434 lines)```

-> sample_submission.csv has 808 rows and 2 columns.
The columns are: row_id, NO2_GT

-> test.csv has 808 rows and 103 columns.
The columns are: row_id, PT08_S1_CO_lag1, PT08_S1_CO_lag2, PT08_S1_CO_lag3, PT08_S1_CO_lag4, PT08_S1_CO_lag5, PT08_S1_CO_lag6, PT08_S1_CO_lag7, PT08_S1_CO_lag8, PT08_S1_CO_lag9, PT08_S1_CO_lag10, PT08_S1_CO_lag11, PT08_S1_CO_lag12, PT08_S2_NMHC_lag1, PT08_S2_NMHC_lag2... and 88 more columns

-> train.csv has 6433 rows and 104 columns.
The columns are: row_id, PT08_S1_CO_lag1, PT08_S1_CO_lag2, PT08_S1_CO_lag3, PT08_S1_CO_lag4, PT08_S1_CO_lag5, PT08_S1_CO_lag6, PT08_S1_CO_lag7, PT08_S1_CO_lag8, PT08_S1_CO_lag9, PT08_S1_CO_lag10, PT08_S1_CO_lag11, PT08_S1_CO_lag12, PT08_S2_NMHC_lag1, PT08_S2_NMHC_lag2... and 89 more columns
