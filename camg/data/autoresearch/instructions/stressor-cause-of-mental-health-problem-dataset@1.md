# OpenMLE-fast task

Task ID: `stressor-cause-of-mental-health-problem-dataset@1`

Native metric: `StressorSpanExtractionMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (513 bytes)
- `data/sample_submission.csv` (4276 bytes); columns: ["id", "spans"]
- `data/test.csv` (86075 bytes); columns: ["id", "text"]
- `data/train.csv` (598316 bytes); columns: ["id", "text", "spans"]

## Public description

Stressor Span Extraction from Social Media Posts

Data Files
- train.csv: Columns [id, text, spans] where spans is a JSON-encoded list of stressor surface strings.
- test.csv: Columns [id, text] without labels.
- sample_submission.csv: Template with columns [id, spans].

Submission
- Submit a CSV with columns [id, spans], where spans is a JSON-encoded list of strings.
- ids must match those in test.csv (any order is fine).

Evaluation
- Micro-averaged F1 over normalized span strings using multiset matching.
