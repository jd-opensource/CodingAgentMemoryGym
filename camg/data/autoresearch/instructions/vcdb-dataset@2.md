# OpenMLE-fast task

Task ID: `vcdb-dataset@2`

Native metric: `ImpactedAssetTypeMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (659 bytes)
- `data/sample_submission.csv` (92299 bytes); columns: ["incident_id", "asset_variety"]
- `data/test.csv` (323731 bytes); columns: ["incident_id", "action_notes", "action", "action_variety", "motive", "actor", "actor_variety", "asset.total_amount", "asset_cloud", "asset_hosting", "asset_management", "asset_ownership", "asset_role", "external_actor_country", "asset_country", "victim_country", "day", "month", "year"]
- `data/train.csv` (1401712 bytes); columns: ["incident_id", "action_notes", "action", "action_variety", "motive", "actor", "actor_variety", "asset.total_amount", "asset_cloud", "asset_hosting", "asset_management", "asset_ownership", "asset_role", "asset_variety", "external_actor_country", "asset_country", "victim_country", "day", "month", "year"]

## Public description

Competition: Impacted Asset Type Classification (VCDB)

Files provided (under this public directory):
- train.csv: Labeled training data including the target column asset_variety.
- test.csv: Unlabeled test data with the same feature columns as train.csv except asset_variety is omitted.
- sample_submission.csv: Example submission with the required columns [incident_id, asset_variety].

Target
- asset_variety (categorical).

Evaluation
- Macro F1 computed between your predictions and the hidden test labels.

Submission format
- CSV with two columns (header required): incident_id, asset_variety.
- Must include each incident_id in test.csv exactly once.
