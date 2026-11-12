# OpenMLE-fast task

Task ID: `nba-aba-baa-stats@1`

Native metric: `NBAAllStarSelectionMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3036 bytes)
- `data/sample_submission.csv` (95022 bytes); columns: ["row_id", "is_all_star"]
- `data/test.csv` (1646077 bytes); columns: ["row_id", "season", "player_id", "primary_team_abbr", "pg_age", "pg_g", "pg_gs", "pg_mp_per_game", "pg_fg_per_game", "pg_fga_per_game", "pg_fg_percent", "pg_x3p_per_game", "pg_x3pa_per_game", "pg_x3p_percent", "pg_x2p_per_game", "pg_x2pa_per_game", "pg_x2p_percent", "pg_e_fg_percent", "pg_ft_per_game", "pg_fta_per_game", "pg_ft_percent", "pg_orb_per_game", "pg_drb_per_game", "pg_trb_per_game", "pg_ast_per_game", "pg_stl_per_game", "pg_blk_per_game", "pg_tov_per_game", "pg_pf_per_game", "pg_pts_per_game", "pg_season_minutes", "adv_age", "adv_g", "adv_gs", "adv_mp", "adv_per", "adv_ts_percent", "adv_x3p_ar", "adv_f_tr", "adv_orb_percent", "adv_drb_percent", "adv_trb_percent", "adv_ast_percent", "adv_stl_percent", "adv_blk_percent", "adv_tov_percent", "adv_usg_percent", "adv_ows", "adv_dws", "adv_ws", "adv_ws_48", "adv_obpm", "adv_dbpm", "adv_bpm", "adv_vorp", "pbp_age", "pbp_g", "pbp_gs", "pbp_mp", "pbp_pg_percent", "pbp_sg_percent", "pbp_sf_percent", "pbp_pf_percent", "pbp_c_percent", "pbp_on_court_plus_minus_per_100_poss", "pbp_net_plus_minus_per_100_poss", "pbp_bad_pass_turnover", "pbp_lost_ball_turnover", "pbp_shooting_foul_committed", "pbp_offensive_foul_committed", "pbp_shooting_foul_drawn", "pbp_offensive_foul_drawn", "pbp_points_generated_by_assists", "pbp_and1", "pbp_fga_blocked", "sh_age", "sh_g", "sh_gs", "sh_mp", "sh_fg_percent", "sh_avg_dist_fga", "sh_percent_fga_from_x2p_range", "sh_percent_fga_from_x0_3_range", "sh_percent_fga_from_x3_10_range", "sh_percent_fga_from_x10_16_range", "sh_percent_fga_from_x16_3p_range", "sh_percent_fga_from_x3p_range", "sh_fg_percent_from_x2p_range", "sh_fg_percent_from_x0_3_range", "sh_fg_percent_from_x3_10_range", "sh_fg_percent_from_x10_16_range", "sh_fg_percent_from_x16_3p_range", "sh_fg_percent_from_x3p_range", "sh_percent_assisted_x2p_fg", "sh_percent_assisted_x3p_fg", "sh_percent_dunks_of_fga", "sh_num_of_dunks", "sh_percent_corner_3s_of_3pa", "sh_corner_3_point_percent", "sh_num_heaves_attempted", "sh_num_heaves_made", "team_playoffs", "team_age", "team_w", "team_l", "team_pw", "team_pl", "team_mov", "team_sos", "team_srs", "team_o_rtg", "team_d_rtg", "team_n_rtg", "team_pace", "team_f_tr", "team_x3p_ar", "team_ts_percent", "team_e_fg_percent", "team_tov_percent", "team_orb_percent", "team_ft_fga", "team_opp_e_fg_percent", "team_opp_tov_percent", "team_drb_percent", "team_opp_ft_fga", "team_attend", "team_attend_g"]
- `data/train.csv` (6314830 bytes); columns: ["row_id", "season", "player_id", "primary_team_abbr", "pg_age", "pg_g", "pg_gs", "pg_mp_per_game", "pg_fg_per_game", "pg_fga_per_game", "pg_fg_percent", "pg_x3p_per_game", "pg_x3pa_per_game", "pg_x3p_percent", "pg_x2p_per_game", "pg_x2pa_per_game", "pg_x2p_percent", "pg_e_fg_percent", "pg_ft_per_game", "pg_fta_per_game", "pg_ft_percent", "pg_orb_per_game", "pg_drb_per_game", "pg_trb_per_game", "pg_ast_per_game", "pg_stl_per_game", "pg_blk_per_game", "pg_tov_per_game", "pg_pf_per_game", "pg_pts_per_game", "pg_season_minutes", "adv_age", "adv_g", "adv_gs", "adv_mp", "adv_per", "adv_ts_percent", "adv_x3p_ar", "adv_f_tr", "adv_orb_percent", "adv_drb_percent", "adv_trb_percent", "adv_ast_percent", "adv_stl_percent", "adv_blk_percent", "adv_tov_percent", "adv_usg_percent", "adv_ows", "adv_dws", "adv_ws", "adv_ws_48", "adv_obpm", "adv_dbpm", "adv_bpm", "adv_vorp", "pbp_age", "pbp_g", "pbp_gs", "pbp_mp", "pbp_pg_percent", "pbp_sg_percent", "pbp_sf_percent", "pbp_pf_percent", "pbp_c_percent", "pbp_on_court_plus_minus_per_100_poss", "pbp_net_plus_minus_per_100_poss", "pbp_bad_pass_turnover", "pbp_lost_ball_turnover", "pbp_shooting_foul_committed", "pbp_offensive_foul_committed", "pbp_shooting_foul_drawn", "pbp_offensive_foul_drawn", "pbp_points_generated_by_assists", "pbp_and1", "pbp_fga_blocked", "sh_age", "sh_g", "sh_gs", "sh_mp", "sh_fg_percent", "sh_avg_dist_fga", "sh_percent_fga_from_x2p_range", "sh_percent_fga_from_x0_3_range", "sh_percent_fga_from_x3_10_range", "sh_percent_fga_from_x10_16_range", "sh_percent_fga_from_x16_3p_range", "sh_percent_fga_from_x3p_range", "sh_fg_percent_from_x2p_range", "sh_fg_percent_from_x0_3_range", "sh_fg_percent_from_x3_10_range", "sh_fg_percent_from_x10_16_range", "sh_fg_percent_from_x16_3p_range", "sh_fg_percent_from_x3p_range", "sh_percent_assisted_x2p_fg", "sh_percent_assisted_x3p_fg", "sh_percent_dunks_of_fga", "sh_num_of_dunks", "sh_percent_corner_3s_of_3pa", "sh_corner_3_point_percent", "sh_num_heaves_attempted", "sh_num_heaves_made", "team_playoffs", "team_age", "team_w", "team_l", "team_pw", "team_pl", "team_mov", "team_sos", "team_srs", "team_o_rtg", "team_d_rtg", "team_n_rtg", "team_pace", "team_f_tr", "team_x3p_ar", "team_ts_percent", "team_e_fg_percent", "team_tov_percent", "team_orb_percent", "team_ft_fga", "team_opp_e_fg_percent", "team_opp_tov_percent", "team_drb_percent", "team_opp_ft_fga", "team_attend", "team_attend_g", "is_all_star"]

## Public description

Competition: Predict NBA All-Star Selections (1997–2024)

Problem statement
Build a machine learning model that predicts the probability a player is selected to the NBA All-Star Game in a given regular season. The task is binary classification at the player-season level with severe class imbalance. A single out-of-time split is provided to evaluate generalization and avoid temporal leakage.

Data description
- Each row represents one player-season (NBA only) from 1997–2024.
- The dataset aggregates player statistics across stints and adds team context; features are purely numeric or categorical identifiers.
- Columns
  - row_id: unique identifier (season_player_id)
  - season: integer season year
  - player_id: canonical player identifier
  - primary_team_abbr: player’s primary team abbreviation that season (metadata)
  - Feature columns: engineered numeric features capturing box-score rates, advanced metrics, play-by-play profile, shooting profile, and team context. Feature names are prefixed by source for clarity: pg_*, adv_*, pbp_*, sh_*, team_*.
  - is_all_star (train only): binary target (1 if selected to All-Star, 0 otherwise)
- Train/test split
  - train.csv: seasons 1997–2019, includes is_all_star
  - test.csv: seasons 2020–2024, same schema as train.csv but without is_all_star
  - sample_submission.csv: expected submission format for the test set

Target and ID
- Target column: is_all_star (binary; 1 if selected, 0 otherwise). All selections, including replacements, are treated as positives.
- Identifier column: row_id, which must be used to align predictions with test.csv rows.

Evaluation metric
- Primary metric: Average Precision (micro PR-AUC) across all rows in the test set.
  - Why: The task is highly imbalanced; AP evaluates ranking quality for positives without requiring a threshold.
  - During scoring, predictions are coerced to float, NaNs are replaced by 0.0, infinities are handled, and values are clipped to [0,1].
- Informational tie-breaker: Log Loss on the same test set (lower is better).

Submission format
- CSV with columns exactly: row_id,is_all_star
- is_all_star must be a probability in [0,1] for each row in test.csv.
- row_id must exactly match the identifiers in test.csv (no extras, no missing).

Guidance
- The feature space is rich and heterogeneous; participants should consider:
  - Data processing and robust handling of missing values and era-specific features.
  - Feature engineering (scaling, interactions, monotonic constraints where sensible).
  - Modeling approaches suitable for imbalanced tabular classification (e.g., calibrated gradient boosting, logistic regression, or modern tree-based ensembles).
  - Model evaluation using custom validation within the training split (e.g., time-based folds) to maintain temporal integrity.
- Multi-team seasons are consolidated; team context reflects the player’s primary team. Some features may be unavailable for earlier years within the range—indicator features and careful imputation can help.
