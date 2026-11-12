# OpenMLE-fast task

Task ID: `fifa-24-player-stats-dataset@1`

Native metric: `FifaPlayerValueMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (144 bytes)
- `data/sample_submission.csv` (16745 bytes); columns: ["id", "value"]
- `data/test.csv` (154080 bytes); columns: ["id", "country", "club", "height", "weight", "age", "ball_control", "dribbling", "slide_tackle", "stand_tackle", "aggression", "reactions", "att_position", "interceptions", "vision", "composure", "crossing", "short_pass", "long_pass", "acceleration", "stamina", "strength", "balance", "sprint_speed", "agility", "jumping", "heading", "shot_power", "finishing", "long_shots", "curve", "fk_acc", "penalties", "volleys", "gk_positioning", "gk_diving", "gk_handling", "gk_kicking", "gk_reflexes"]
- `data/train.csv` (616950 bytes); columns: ["country", "club", "height", "weight", "age", "ball_control", "dribbling", "slide_tackle", "stand_tackle", "aggression", "reactions", "att_position", "interceptions", "vision", "composure", "crossing", "short_pass", "long_pass", "acceleration", "stamina", "strength", "balance", "sprint_speed", "agility", "jumping", "heading", "shot_power", "finishing", "long_shots", "curve", "fk_acc", "penalties", "volleys", "gk_positioning", "gk_diving", "gk_handling", "gk_kicking", "gk_reflexes", "value"]

## Public description

FIFA 24 Player Valuation Challenge

Files in this directory:
- train.csv
- test.csv
- sample_submission.csv

Submit a CSV with columns: id,value
