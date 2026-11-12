# OpenMLE-fast task

Task ID: `cloud-vulnerabilities-dataset@2`

Native metric: `CloudVulnerabilityClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (541 bytes)
- `data/sample_submission.csv` (5848 bytes); columns: ["id", "predicted_category"]
- `data/test.csv` (50008 bytes); columns: ["id", "text"]
- `data/train.csv` (218792 bytes); columns: ["id", "text", "category"]

## Public description

Competition: Cross-Provider Robust Vulnerability Category Prediction (Provider-Neutral Inputs)

Files provided
- train.csv: columns [id, text, category]
- test.csv: columns [id, text]
- sample_submission.csv: columns [id, predicted_category]
- description.txt: competition description and file listing

Task
Predict the vulnerability category given provider-neutralized text. Evaluation is macro-averaged F1 across categories.

Notes
- Deterministic stratified split; no overlap between train and test ids.
- All test labels appear in train.
