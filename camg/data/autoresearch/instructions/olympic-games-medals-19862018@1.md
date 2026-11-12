# OpenMLE-fast task

Task ID: `olympic-games-medals-19862018@1`

Native metric: `OlympicMedalClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (530 bytes)
- `data/sample_submission.csv` (161241 bytes); columns: ["row_id", "medal"]
- `data/test.csv` (2538460 bytes); columns: ["row_id", "discipline_title", "event_title", "participant_type", "country_name", "country_code", "country_3_letter_code", "slug_game", "game_season", "game_year", "game_location", "event_gender", "is_host_country", "team_size", "age_mean", "age_min", "age_max", "games_participations_mean", "games_participations_sum", "experience_years_mean", "prior_medal_rate_overall", "prior_rate_cd", "prior_medal_count", "prior_entry_count"]
- `data/train.csv` (27067941 bytes); columns: ["row_id", "discipline_title", "event_title", "participant_type", "country_name", "country_code", "country_3_letter_code", "slug_game", "game_season", "game_year", "game_location", "event_gender", "is_host_country", "team_size", "age_mean", "age_min", "age_max", "games_participations_mean", "games_participations_sum", "experience_years_mean", "prior_medal_rate_overall", "prior_rate_cd", "prior_medal_count", "prior_entry_count", "medal"]

## Public description

Olympic Finals Medal Prediction

Files provided (in this public directory):
- train.csv: Training features with target column 'medal'.
- test.csv: Test features with the same columns as train.csv except without 'medal'.
- sample_submission.csv: Example submission with columns ['row_id', 'medal'].
- description.txt: This description file.

Submission format:
- CSV file with two columns: row_id, medal
- medal must be one of: Gold, Silver, Bronze, None

Evaluation:
- Macro F1 across the four classes [Gold, Silver, Bronze, None]
