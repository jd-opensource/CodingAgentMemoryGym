# OpenMLE-fast task

Task ID: `cjs-dataset@1`

Native metric: `InternodeProfileClassificationMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1074 bytes)
- `data/sample_submission.csv` (70190 bytes); columns: ["sprout_id", "control", "methanol_control", "PP_333_20gL", "PP_333_4gL", "EL_500_20gL", "EL_500_4gL"]
- `data/test.csv` (27819 bytes); columns: ["sprout_id", "INTERNODE_1", "INTERNODE_2", "INTERNODE_3", "INTERNODE_4", "INTERNODE_5", "INTERNODE_6", "INTERNODE_7", "INTERNODE_8", "INTERNODE_9", "INTERNODE_10", "INTERNODE_11", "INTERNODE_12", "INTERNODE_13", "INTERNODE_14", "INTERNODE_15", "INTERNODE_16", "INTERNODE_17", "INTERNODE_18", "INTERNODE_19", "INTERNODE_20", "INTERNODE_21", "INTERNODE_22", "INTERNODE_23", "INTERNODE_24", "INTERNODE_25", "INTERNODE_26", "INTERNODE_27", "INTERNODE_28", "INTERNODE_29"]
- `data/train.csv` (131954 bytes); columns: ["sprout_id", "INTERNODE_1", "INTERNODE_2", "INTERNODE_3", "INTERNODE_4", "INTERNODE_5", "INTERNODE_6", "INTERNODE_7", "INTERNODE_8", "INTERNODE_9", "INTERNODE_10", "INTERNODE_11", "INTERNODE_12", "INTERNODE_13", "INTERNODE_14", "INTERNODE_15", "INTERNODE_16", "INTERNODE_17", "INTERNODE_18", "INTERNODE_19", "INTERNODE_20", "INTERNODE_21", "INTERNODE_22", "INTERNODE_23", "INTERNODE_24", "INTERNODE_25", "INTERNODE_26", "INTERNODE_27", "INTERNODE_28", "INTERNODE_29", "treatment"]

## Public description

Title: Internode Profiles Challenge: Infer Growth Regulator Treatment from Sprout Morphology

Problem statement
Utilities routinely trim trees near power lines. Two growth regulators (Paclobutrazol, PP 333, and Flurprimidol, EL-500) can suppress regrowth. You are given detailed measurements of internode lengths along individual terminal sprouts collected 20 months after treatment. Your task is to predict which treatment and dosage each sprout was subjected to, using only the per-internode length sequence. This is a 6-class classification problem.

Files provided
- train.csv: columns = [sprout_id] + INTERNODE_1..INTERNODE_29 + [treatment]
- test.csv: columns = [sprout_id] + INTERNODE_1..INTERNODE_29
- sample_submission.csv: columns = [sprout_id] + probability columns for each class

Evaluation metric
- Submissions must provide probabilities for all classes for each sprout in test.csv.
- The leaderboard metric is macro-averaged multiclass log loss (base e).

Submission format
- A valid submission is a CSV with columns: sprout_id, <one column per class label>.
