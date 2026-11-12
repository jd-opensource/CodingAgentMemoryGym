# OpenMLE-fast task

Task ID: `fitness-exercises-dataset@1`

Native metric: `ExerciseTaxonomyMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (442 bytes)
- `data/sample_submission.csv` (12846 bytes); columns: ["id", "bodyPart", "equipment", "target", "secondary_muscles"]
- `data/test.csv` (135645 bytes); columns: ["id", "text"]
- `data/train.csv` (570307 bytes); columns: ["id", "text", "bodyPart", "equipment", "target", "secondary_muscles"]

## Public description

Title: Text-to-Exercise Taxonomy (Multi-task, Multi-label)

Data files (relative to public/):
- train.csv: id, text, bodyPart, equipment, target, secondary_muscles
- test.csv: id, text
- sample_submission.csv: id, bodyPart, equipment, target, secondary_muscles (semicolon-separated)

Evaluation metric
Leaderboard score = mean of four F1 components:
- bodyPart: macro-F1
- equipment: macro-F1
- target: macro-F1
- secondary_muscles: micro-F1
