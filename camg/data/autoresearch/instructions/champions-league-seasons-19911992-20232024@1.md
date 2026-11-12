# OpenMLE-fast task

Task ID: `champions-league-seasons-19911992-20232024@1`

Native metric: `ChampionsLeagueProgressionMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/assets/diagram.png` (30165 bytes)
- `data/description.txt` (2421 bytes)
- `data/sample_submission.csv` (1317 bytes); columns: ["row_id", "label"]
- `data/test.csv` (46358 bytes); columns: ["row_id", "season_id", "team_id", "group_name", "season_year", "season_mid_year", "country_code", "latitude", "longitude", "secound_group_stage_name", "minutes_total", "top5_share", "cnt_over_900", "mean_age", "median_age", "age_std", "nat_entropy", "domestic_min_share", "min_gk", "min_df", "min_mf", "min_fw", "min_share_gk", "min_share_df", "min_share_mf", "min_share_fw", "group_place", "group_place_first", "group_place_second", "group_place_drop_out", "group_place_advance_to_final", "has_second_group", "sec_group_place_first", "sec_group_place_second", "sec_group_place_drop_out", "era_second_group_stage"]
- `data/train.csv` (219467 bytes); columns: ["row_id", "season_id", "team_id", "group_name", "season_year", "season_mid_year", "country_code", "latitude", "longitude", "secound_group_stage_name", "minutes_total", "top5_share", "cnt_over_900", "mean_age", "median_age", "age_std", "nat_entropy", "domestic_min_share", "min_gk", "min_df", "min_mf", "min_fw", "min_share_gk", "min_share_df", "min_share_mf", "min_share_fw", "group_place", "group_place_first", "group_place_second", "group_place_drop_out", "group_place_advance_to_final", "has_second_group", "sec_group_place_first", "sec_group_place_second", "sec_group_place_drop_out", "era_second_group_stage", "label"]

## Public description

Title: Champions League Progression Forecast (1991/1992–2023/2024)

Problem statement
Forecast the highest UEFA Champions League stage reached by each team-season using information available by or at the end of the group stage, plus squad and team metadata. The target label is ordinal and encodes progression depth.

Target classes (ordinal 0–6)
- 0: group_stage_exit
- 1: second_group_stage_exit (only applicable in seasons with a second group stage)
- 2: round_of_16
- 3: quarter_final
- 4: semi_final
- 5: final_loser
- 6: final_winner

Provided files
- train.csv: tabular features for each team-season and the ground-truth "label" (0–6)
- test.csv: same columns as train.csv except without the "label" column
- sample_submission.csv: a valid example submission for test.csv

Schema notes
- Each row represents a unique team-season and includes a "row_id" key for submission alignment.
- Features capture group-stage context, second group stage context (where relevant), squad composition and minutes distribution, age and nationality diversity, and team metadata such as coordinates and era indicators. No knockout-stage information is included among the features.

Train/test split
- Train: seasons 1991/1992 through 2018/2019
- Test: seasons 2019/2020 through 2023/2024
This chronological split simulates real forecasting and prevents temporal leakage.

Evaluation
Submissions are evaluated with Quadratic Weighted Kappa (QWK) over the ordinal labels 0–6.
- Submission format: a single CSV with two columns—"row_id" and integer "label" (0–6)—covering all rows in test.csv.
- QWK penalizes larger ordinal errors more heavily, reflecting the ordered nature of progression stages.

Guidance
- Model using features that would be known by the end of the group stage plus squad and team metadata. Do not derive features from knockout outcomes.
- Expect class imbalance (few finalists/winners). Ordinal-aware objectives, class weights, and robust validation will help.
- Strong solutions will combine careful data processing, feature engineering (e.g., positional minutes shares, minutes concentration, age profiles, nationality entropy, domestic minutes share, group placement indicators), and well-tuned models.

Final competition files
- train.csv
- test.csv
- sample_submission.csv

Build robust tabular ML models that generalize across eras while respecting the ordinal nature of the target. Good luck!
