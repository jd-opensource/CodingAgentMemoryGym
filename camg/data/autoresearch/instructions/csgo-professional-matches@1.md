# OpenMLE-fast task

Task ID: `csgo-professional-matches@1`

Native metric: `CSGOMatchWinLogLossMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4495 bytes)
- `data/economy_starts_test.csv` (325 bytes); columns: ["date", "match_id", "event_id", "team_1", "team_2", "best_of", "_map", "t1_start", "t2_start"]
- `data/economy_starts_train.csv` (1348793 bytes); columns: ["date", "match_id", "event_id", "team_1", "team_2", "best_of", "_map", "t1_start", "t2_start"]
- `data/matches_test.csv` (15852 bytes); columns: ["match_id", "event_id", "date", "team_1", "team_2"]
- `data/matches_train.csv` (670479 bytes); columns: ["match_id", "event_id", "date", "team_1", "team_2", "label"]
- `data/picks_test.csv` (41698 bytes); columns: ["date", "team_1", "team_2", "inverted_teams", "match_id", "event_id", "best_of", "system", "t1_removed_1", "t1_removed_2", "t1_removed_3", "t2_removed_1", "t2_removed_2", "t2_removed_3", "t1_picked_1", "t2_picked_1", "left_over"]
- `data/picks_train.csv` (1723086 bytes); columns: ["date", "team_1", "team_2", "inverted_teams", "match_id", "event_id", "best_of", "system", "t1_removed_1", "t1_removed_2", "t1_removed_3", "t2_removed_1", "t2_removed_2", "t2_removed_3", "t1_picked_1", "t2_picked_1", "left_over"]
- `data/players_roster_test.csv` (67 bytes); columns: ["date", "player_name", "team", "opponent", "country", "player_id", "match_id", "event_id"]
- `data/players_roster_train.csv` (9544897 bytes); columns: ["date", "player_name", "team", "opponent", "country", "player_id", "match_id", "event_id"]
- `data/results_meta_test.csv` (18438 bytes); columns: ["date", "team_1", "team_2", "event_id", "match_id", "rank_1", "rank_2"]
- `data/results_meta_train.csv` (738990 bytes); columns: ["date", "team_1", "team_2", "event_id", "match_id", "rank_1", "rank_2"]
- `data/sample_submission.csv` (12200 bytes); columns: ["match_id", "event_id", "p_team1_win"]
- `data/test.csv` (15852 bytes); columns: ["match_id", "event_id", "date", "team_1", "team_2"]
- `data/train.csv` (670479 bytes); columns: ["match_id", "event_id", "date", "team_1", "team_2", "label"]

## Public description

Competition: Predicting CS:GO Match Winners from Veto and Rosters

Problem statement
- Task: Before the first round is played, predict the probability that team_1 wins a professional CS:GO match.
- Input: Pre-match information only — the veto sequence (picks/removals), best-of format and system, team ranks, and rosters; plus starting sides (CT/T) for each map as part of the pre-game setup. No in-game performance, round-by-round outcomes, or per-map results are included in test data.
- Output: For every match in the test set, submit a calibrated probability p_team1_win in [0, 1].

Unit of prediction
- One prediction per match (identified by match_id and event_id).

Files provided
- matches_train.csv — one row per match with keys and binary label (label = 1 if team_1 wins, else 0) plus basic identifiers.
- matches_test.csv — one row per match with keys and basic identifiers; no label.
- picks_train.csv / picks_test.csv — pre-match veto context (best_of, system, inverted_teams, t1_removed_*, t2_removed_*, t1_picked_1, t2_picked_1, left_over, date, team_1, team_2, match_id, event_id).
- results_meta_train.csv / results_meta_test.csv — pre-match metadata only from results (date, team_1, team_2, match_id, event_id, rank_1, rank_2). All outcome-related columns are removed.
- economy_starts_train.csv / economy_starts_test.csv — pre-match starting sides per map (date, team_1, team_2, best_of, _map, t1_start, t2_start, match_id, event_id). All per‑round equipment and winners are removed.
- players_roster_train.csv / players_roster_test.csv — roster snapshots (date, player_name, team, opponent, country, player_id, match_id, event_id). All performance statistics are removed.
- sample_submission.csv — example submission with randomized but valid probabilities for all test matches.

Submission format
- CSV with the following columns:
  - match_id (integer)
  - event_id (integer)
  - p_team1_win (float probability in [0, 1])
- Each (match_id, event_id) must appear exactly once.

Evaluation
- Metric: Binary Log Loss on p_team1_win.
  - For each test match, let y = 1 if team_1 wins, else 0. The score is the mean of −[y*log(p) + (1−y)*log(1−p)], with p clipped to [1e-7, 1−1e-7] for numerical stability. Lower is better.

Train/test split
- Chronological single split to emulate forecasting: training covers older matches; testing covers newer matches. This avoids leakage and encourages time‑aware modeling. The split is deterministic and respects match_id/event_id as the prediction unit.

Important notes and guidance
- Canonical orientation: The label uses the results orientation of team_1/team_2 in matches_train/test. In picks files, team fields may be inverted; use the inverted_teams flag to align veto-based features with the label orientation.
- Data leakage: Test files contain pre-match information only. Outcome-related signals (map results, round winners, per‑round economy, player performance) are excluded from test and from the meta files. Use only the provided files for modeling.
- Multi-table learning: You are encouraged to merge the tables on (match_id, event_id) and engineer features across veto sequences, roster composition, ranks, best-of formats, systems, and starting sides. Handling differing granularities (match-level, map-level, player-level) is part of the challenge.
- Calibration matters: The leaderboard metric is log loss, rewarding well-calibrated probabilities, not just classification accuracy.
- Scale: All data within the split is included; no downsampling or subsets are used.

Suggested feature directions (not exhaustive)
- Veto structure: Which maps each team removed/picked, decider (left_over), inverted_teams flag, best_of format, system.
- Ranks: rank_1/rank_2, differences/ratios, rank-based prior of strength.
- Starting sides: Map-wise t1_start/t2_start and aggregates (e.g., share of CT starts for team_1 across maps in the match).
- Rosters: Player counts, country composition, roster stability within team and head-to-heads (from training period only).

What is not provided/used for modeling
- Per-map results, map_wins, per-round winners, per-round equipment values, and all player performance stats are intentionally excluded from the provided meta/test files to prevent trivial leakage.

Goal
- Build a robust, well-calibrated pre-match win probability model that generalizes to future matches by leveraging multi-table joins, careful feature engineering, and time-aware validation.
