# OpenMLE-fast task

Task ID: `trke-haberler-ve-kategori-veri-seti@1`

Native metric: `TurkishNewsCategoryMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (594 bytes)
- `data/sample_submission.csv` (142129 bytes); columns: ["id", "kategori"]
- `data/test.csv` (586133 bytes); columns: ["id", "text"]
- `data/train.csv` (2576255 bytes); columns: ["id", "text", "kategori"]

## Public description

Title: Turkish News Headline Category Classification

Problem statement
Build a model that predicts the editorial category of a Turkish news headline.

Data description
- train.csv: Contains three columns: id, text, kategori.
- test.csv: Contains two columns: id, text.
- sample_submission.csv: A template file with the expected submission format.

Submission format
- Submit a CSV with two columns: id and kategori.
- Each id from test.csv must appear exactly once, with a single predicted kategori.

Evaluation
- Macro F1 score computed across the full label set present in the test answers.
