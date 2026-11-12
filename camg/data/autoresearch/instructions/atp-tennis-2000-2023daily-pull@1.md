# OpenMLE-fast task

Task ID: `atp-tennis-2000-2023daily-pull@1`

Native metric: `ATPTennisWinProbabilityMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/sample_submission.csv` (364241 bytes); columns: ["match_id", "p1_win"]
- `data/test.csv` (1545158 bytes); columns: ["match_id", "Tournament", "Date", "Series", "Court", "Surface", "Round", "Best of", "Player_1", "Player_2", "Rank_1", "Rank_2", "Pts_1", "Pts_2"]
- `data/train.csv` (6277629 bytes); columns: ["match_id", "Tournament", "Date", "Series", "Court", "Surface", "Round", "Best of", "Player_1", "Player_2", "Rank_1", "Rank_2", "Pts_1", "Pts_2", "target"]

## Public description

No additional public description was provided.
