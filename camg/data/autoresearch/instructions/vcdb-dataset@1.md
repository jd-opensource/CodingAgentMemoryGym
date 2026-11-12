# OpenMLE-fast task

Task ID: `vcdb-dataset@1`

Native metric: `CyberIncidentActionVarietyMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2610 bytes)
- `data/sample_submission.csv` (81477 bytes); columns: ["incident_id", "action_variety"]
- `data/test.csv` (209562 bytes); columns: ["incident_id", "action_notes", "motive", "actor", "actor_variety", "asset.total_amount", "asset_cloud", "asset_hosting", "asset_management", "asset_ownership", "asset_role", "asset_variety", "external_actor_country", "asset_country", "victim_country", "day", "month", "year"]
- `data/train.csv` (921700 bytes); columns: ["incident_id", "action_notes", "motive", "actor", "actor_variety", "asset.total_amount", "asset_cloud", "asset_hosting", "asset_management", "asset_ownership", "asset_role", "asset_variety", "external_actor_country", "asset_country", "victim_country", "day", "month", "year", "action_variety"]

## Public description

Title: Fine-grained Cyber Incident Action Variety Classification (72-class)

Problem statement
Predict the fine-grained action_variety for each cybersecurity incident from mixed tabular and sparse text features. Incidents span diverse scenarios and geographies and are highly imbalanced across 72 classes, making robust preprocessing, feature engineering, and modeling essential.

Files provided
- train.csv: Training data with features and the target column action_variety.
- test.csv: Test data with the same feature columns as train.csv, without action_variety.
- sample_submission.csv: Example submission file with the required format.

Target and features
- Target: action_variety (72 fine-grained classes; only labeled, non-Unknown rows are included).
- Identifier: incident_id (unique per incident; use as the Id in submissions).
- Features (tabular + text):
  - action_notes (free text; may be empty)
  - motive
  - actor, actor_variety
  - asset.total_amount (numeric where present)
  - asset_cloud, asset_hosting, asset_management, asset_ownership, asset_role, asset_variety
  - external_actor_country, asset_country, victim_country
  - day, month, year (calendar fields; may be missing)

Important notes
- The parent label action is excluded from train/test to avoid label leakage.
- String-like missing values are kept as-is; participants should handle them during preprocessing.

Submission format
- CSV with header and two columns in this order: incident_id,action_variety
- Exactly one row per incident_id in test.csv
- action_variety must be a single class string per row (case-sensitive, exact match).

Evaluation
- Metric: Macro F1 over the classes present in the test set, computed between your predicted action_variety and the held-out ground truth.
- Rationale: Macro F1 equally weights all classes, counteracting class imbalance and rewarding performance on rare classes.

Guidance (non-exhaustive)
- Categorical encoding: one-hot, target, or hashing for high-cardinality fields (countries, asset_variety, actor_variety).
- Text: TF-IDF or bag-of-words over action_notes; combine with tabular encodings.
- Date features: derive month-of-year, year, and missingness indicators.
- Imbalance handling: class weights, sampling, calibrated decision thresholds.
- Baselines: linear models on concatenated TF-IDF + categorical encodings; tree-based models with robust encoders; simple neural models for text+tabular.

Final competition files
- train.csv
- test.csv
- sample_submission.csv

Scoring
- Submissions are scored with Macro F1, ranging from 0.0 (worst) to 1.0 (best). Higher is better.
