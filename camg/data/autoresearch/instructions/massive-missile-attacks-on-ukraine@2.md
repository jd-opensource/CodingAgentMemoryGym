# OpenMLE-fast task

Task ID: `massive-missile-attacks-on-ukraine@2`

Native metric: `RaidDurationMAEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3242 bytes)
- `data/sample_submission.csv` (3842 bytes); columns: ["id", "duration_hours"]
- `data/test.csv` (29584 bytes); columns: ["id", "time_start", "model", "launch_place", "target", "target_main", "carrier", "reg_category", "reg_national_origin", "reg_type", "reg_launch_platform", "reg_name", "reg_name_NATO", "reg_in_sevice", "reg_designer", "reg_manufacturer", "reg_guidance_system", "reg_unit_cost"]
- `data/train.csv` (191991 bytes); columns: ["id", "time_start", "model", "launch_place", "target", "target_main", "carrier", "reg_category", "reg_national_origin", "reg_type", "reg_launch_platform", "reg_name", "reg_name_NATO", "reg_in_sevice", "reg_designer", "reg_manufacturer", "reg_guidance_system", "reg_unit_cost", "duration_hours"]

## Public description

Attack Duration Nowcasting: Predict Hours from Start to End of Raid

Problem statement
You are given event-level records of massive missile/UAV raids against Ukraine. Using only information plausibly available at or near the event start (e.g., start timestamp, model name, reported launch origins, target descriptors, carrier), predict the raid duration in hours. The target is continuous.

Files
- train.csv: One row per event with features and the target duration_hours.
- test.csv: Same columns as train.csv except duration_hours.
- sample_submission.csv: Example submission with random valid predictions.

Target definition
- duration_hours = (time_end − time_start) measured in hours, computed from precise timestamps.
- Only events with precise time-of-day in both time_start and time_end are included. Date-only rows are excluded.

Columns present in train/test
- id: Unique event identifier.
- time_start: Start timestamp string (local, as reported). Intended for deriving temporal features (hour-of-day, weekday/weekend, month/season, holidays, etc.).
- model: Missile or UAV model string (lightly normalized).
- launch_place: Reported launch origin(s). May contain multiple locations separated by " and ". Toponyms may include commas (e.g., "Chauda, Crimea").
- target: Target region/city/direction text as initially reported.
- target_main: Main target if specified (may be empty).
- carrier: Launch platform (e.g., "Navi" for sea-based; may be empty).
- reg_category, reg_national_origin, reg_type, reg_launch_platform, reg_name, reg_name_NATO, reg_in_sevice, reg_designer, reg_manufacturer, reg_guidance_system, reg_unit_cost: Technical registry fields joined by model when available. These may be missing.
- duration_hours: Target column (train only).

What is intentionally excluded to avoid leakage
- Any post-outcome or evolving counts/fields (e.g., destroyed, launched, not_reach_goal, still_attacking, affected region, *_details) are not included.

Evaluation
- Metric: Mean Absolute Error (MAE) between your predictions and the ground truth duration_hours on the test set.
- Submission format: A CSV with exactly two columns [id, duration_hours]. Predictions must be finite real numbers.

Split protocol
- Chronological split to respect causality: train contains earlier events; test contains the most recent events (~10–15%).

Guidance and expectations
- Strong baselines use temporal covariates from time_start (hour-of-day, weekday, season) and simple encodings from model, carrier, and geography (launch_place/target). Consider cyclic encodings, counts of distinct launch origins, and flags for maritime vs. terrestrial launches.
- Enrich with registry fields (category, national origin, guidance system, in-service year) and engineer interactions.
- Anticipate heavy-tailed durations (brief strikes vs. prolonged overnight swarms). MAE is chosen for robustness and interpretability in hours.

Deliverables
- Submit predictions for every id in test.csv as a CSV with columns [id, duration_hours].

Files provided
- train.csv
- test.csv
- sample_submission.csv

Your objective
Build a model that minimizes MAE on the test set by applying careful data processing, feature engineering, and robust regression modeling.
