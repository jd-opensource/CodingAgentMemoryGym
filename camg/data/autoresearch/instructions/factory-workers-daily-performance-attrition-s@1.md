# OpenMLE-fast task

Task ID: `factory-workers-daily-performance-attrition-s@1`

Native metric: `EfficacyRmseMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (714 bytes)
- `data/history.csv` (171840859 bytes); columns: ["sub_ID", "sub_fname", "sub_lname", "sub_age", "sub_sex", "sub_shift", "sub_team", "sub_role", "sub_coll_IDs", "sub_colls_same_sex_prtn", "sub_health_h", "sub_commitment_h", "sub_perceptiveness_h", "sub_dexterity_h", "sub_sociality_h", "sub_goodness_h", "sub_strength_h", "sub_openmindedness_h", "sub_workstyle_h", "sup_ID", "sup_fname", "sup_lname", "sup_age", "sup_sub_age_diff", "sup_sex", "sup_role", "sup_commitment_h", "sup_perceptiveness_h", "sup_goodness_h", "event_date", "event_week_in_series", "event_day_in_series", "event_weekday_num", "event_weekday_name", "behav_comptype_h", "behav_cause_h", "actual_efficacy_h", "record_comptype", "record_cause", "recorded_efficacy", "recorded_note_from_sup"]
- `data/sample_submission.csv` (310159 bytes); columns: ["row_id", "actual_efficacy_h"]
- `data/test.csv` (4863112 bytes); columns: ["row_id", "sub_ID", "sub_fname", "sub_lname", "sub_age", "sub_sex", "sub_shift", "sub_team", "sub_role", "sub_coll_IDs", "sub_colls_same_sex_prtn", "sub_health_h", "sub_commitment_h", "sub_perceptiveness_h", "sub_dexterity_h", "sub_sociality_h", "sub_goodness_h", "sub_strength_h", "sub_openmindedness_h", "sub_workstyle_h", "sup_ID", "sup_fname", "sup_lname", "sup_age", "sup_sub_age_diff", "sup_sex", "sup_role", "sup_commitment_h", "sup_perceptiveness_h", "sup_goodness_h", "event_date", "event_week_in_series", "event_day_in_series", "event_weekday_num", "event_weekday_name", "behav_comptype_h", "behav_cause_h", "record_comptype", "record_cause", "recorded_efficacy", "recorded_note_from_sup"]
- `data/train.csv` (78931177 bytes); columns: ["sub_ID", "sub_fname", "sub_lname", "sub_age", "sub_sex", "sub_shift", "sub_team", "sub_role", "sub_coll_IDs", "sub_colls_same_sex_prtn", "sub_health_h", "sub_commitment_h", "sub_perceptiveness_h", "sub_dexterity_h", "sub_sociality_h", "sub_goodness_h", "sub_strength_h", "sub_openmindedness_h", "sub_workstyle_h", "sup_ID", "sup_fname", "sup_lname", "sup_age", "sup_sub_age_diff", "sup_sex", "sup_role", "sup_commitment_h", "sup_perceptiveness_h", "sup_goodness_h", "event_date", "event_week_in_series", "event_day_in_series", "event_weekday_num", "event_weekday_name", "behav_comptype_h", "behav_cause_h", "actual_efficacy_h", "record_comptype", "record_cause", "recorded_efficacy", "recorded_note_from_sup"]

## Public description

Title: De-noising Manager Ratings — Estimating True Daily Efficacy

Files provided (relative to this repository root):
- public/train.csv — Efficacy rows in the training period, includes actual_efficacy_h.
- public/test.csv — Efficacy rows in a later period, target removed, includes row_id.
- public/history.csv — All events strictly before the test period for feature engineering.
- public/sample_submission.csv — Correct submission format example.

Target and submission
- Target column: actual_efficacy_h (continuous).
- Submit a CSV with columns: row_id, actual_efficacy_h; one row per test row in the same order.

Evaluation
- Root Mean Squared Error (RMSE) on actual_efficacy_h (lower is better).
