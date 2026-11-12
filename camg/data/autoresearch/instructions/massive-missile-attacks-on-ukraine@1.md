# OpenMLE-fast task

Task ID: `massive-missile-attacks-on-ukraine@1`

Native metric: `MissileInterceptionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3903 bytes)
- `data/missiles_and_uavs.csv` (4488 bytes); columns: ["model", "category", "national_origin", "type", "launch_platform", "name", "name_NATO", "in_sevice", "designer", "manufacturer", "guidance_system", "unit_cost"]
- `data/sample_submission.csv` (15808 bytes); columns: ["row_id", "destroyed_rate"]
- `data/test.csv` (193497 bytes); columns: ["time_start", "time_end", "model", "launch_place", "target", "target_main", "launched", "not_reach_goal", "still_attacking", "border_crossing", "is_shahed", "num_hit_location", "num_fall_fragment_location", "carrier", "turbojet", "turbojet_destroyed", "affected region", "destroyed_details", "launched_details", "launch_place_details", "source", "row_id"]
- `data/train.csv` (506642 bytes); columns: ["destroyed_rate", "time_start", "time_end", "model", "launch_place", "target", "target_main", "launched", "not_reach_goal", "still_attacking", "border_crossing", "is_shahed", "num_hit_location", "num_fall_fragment_location", "carrier", "turbojet", "turbojet_destroyed", "affected region", "destroyed_details", "launched_details", "launch_place_details", "source", "row_id"]

## Public description

Massive Missile Attacks on Ukraine: Interception Rate Nowcasting

Problem
Given attack-level reports of Russian missiles and UAVs launched against Ukraine, predict the fraction intercepted during each attack event. The target is destroyed_rate = destroyed / launched ∈ [0, 1]. Each row represents one attack (or sub-wave) with metadata including time, model, launch places, target, platform, and other fields available at report time. An auxiliary table of missile/UAV technical characteristics is provided for feature enrichment.

Data files provided
- train.csv — training rows with features and the target destroyed_rate.
- test.csv — test rows with the same features as train.csv (except the target, which is held out).
- missiles_and_uavs.csv — technical characteristics by model for optional feature enrichment.
- sample_submission.csv — a valid example submission file with random predictions.

Columns
All columns in train.csv and test.csv (except the target in test) are drawn from the original attack reports after filtering out rows without definitive labels. The schema intentionally retains heterogeneous/semi-structured text fields to enable advanced feature engineering.
Key columns include (non-exhaustive):
- row_id — unique identifier for each attack row.
- time_start, time_end — attack start and end timestamps (strings; parse to datetime).
- model — missile/UAV model string (can contain multiple models joined by “and”).
- launch_place — origin locations string (can contain multiple locations).
- target, target_main — target area information.
- launched — number of missiles/UAVs launched (nonnegative numeric).
- not_reach_goal, still_attacking — additional counts where available.
- border_crossing, affected region, destroyed_details, launched_details, launch_place_details — semi-structured text fields; sparse but potentially useful.
- is_shahed, num_hit_location, num_fall_fragment_location, carrier, turbojet, turbojet_destroyed, source — other metadata fields (may be missing for many rows).
- destroyed_rate (train only) — the target to predict, destroyed / launched, clipped to [0, 1].

Task
Build a model that maps the provided features to destroyed_rate for the test set. You may engineer features (for example, parsing timestamps, normalizing location lists, joining missiles_and_uavs.csv by model, and deriving seasonal and platform indicators). Any supervised ML approach is allowed.

Evaluation
Submissions are evaluated with Weighted Mean Absolute Error (WMAE) on destroyed_rate, with per-row weights equal to launched for that row:
WMAE = sum_i w_i * |y_hat_i - y_i| / sum_i w_i, where w_i = launched_i.

Notes
- This weighting emphasizes accuracy on higher-volume attacks and reflects the operational significance and measurement reliability of those events.
- Predictions should be real numbers; values outside [0, 1] will be clipped during evaluation.
- The split is strictly chronological: test rows occur after train rows in time to avoid leakage.

Submission format
- A CSV with exactly two columns and header: row_id, destroyed_rate
- row_id must match the values in test.csv exactly and be unique.
- destroyed_rate can be any real number; it will be clipped to [0, 1] and evaluated with the metric above.

Recommended baseline ideas
- Time features: hour-of-day, day-of-week, month/season, attack duration.
- Model and platform features: model category, national origin, type, launch platform from missiles_and_uavs.csv.
- Geography features: counts and indicators from launch_place/target strings; flags for Black Sea, Crimea, etc.
- Scale-aware modeling: consider logit transform for rates and tree-based regressors (GBDT) with monotone constraints or calibration.

Final files in this competition
- train.csv, test.csv, missiles_and_uavs.csv, sample_submission.csv
Do not reference any hidden files during modeling.
