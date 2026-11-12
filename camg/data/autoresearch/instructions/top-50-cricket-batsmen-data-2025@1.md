# OpenMLE-fast task

Task ID: `top-50-cricket-batsmen-data-2025@1`

Native metric: `CricketPairwiseRankingMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (794 bytes)
- `data/players.csv` (9088 bytes); columns: ["player_id", "start_year", "end_year", "career_length", "matches", "innings", "total_runs", "hr", "t100", "t50", "runs_per_inning", "matches_per_year", "centuries_per_inning", "fifties_per_inning", "highscore_ratio", "modern_era", "debut_decade", "end_decade", "aff_icc", "aff_asia", "aff_world", "aff_afr", "aff_ind", "aff_sl", "aff_pak", "aff_wi", "aff_eng", "aff_sa", "aff_nz", "aff_aus", "aff_ban", "country_code"]
- `data/sample_submission.csv` (4896 bytes); columns: ["pair_id", "y_pred"]
- `data/test.csv` (5178 bytes); columns: ["pair_id", "player_id_A", "player_id_B"]
- `data/train.csv` (22575 bytes); columns: ["pair_id", "player_id_A", "player_id_B", "y"]

## Public description

Competition: Pairwise Batting-Average Ranking from Career Summaries

Files:
- players.csv: An anonymized table of player-level features engineered from career summaries. It excludes the batting average to prevent leakage.
- train.csv: Labeled training comparisons. Columns: pair_id, player_id_A, player_id_B, y.
- test.csv: Unlabeled test comparisons. Columns: pair_id, player_id_A, player_id_B.
- sample_submission.csv: Template with columns [pair_id, y_pred]. Replace y_pred with probabilities in [0,1].

Task:
- Predict the probability that player_id_A has a higher batting average than player_id_B for each pair in test.csv.

Evaluation:
- Primary: Spearman’s rho on the induced player ranking using your pairwise predictions.
- Secondary: ROC-AUC on held-out pair labels (not provided).
