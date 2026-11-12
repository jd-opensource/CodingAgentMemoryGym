# OpenMLE-fast task

Task ID: `s-and-p-500-with-financial-news-headlines-20082024@1`

Native metric: `SP500HeadlinesMAEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2531 bytes)
- `data/sample_submission.csv` (13982 bytes); columns: ["id", "prediction"]
- `data/test.csv` (586602 bytes); columns: ["id", "date", "text"]
- `data/train.csv` (734747 bytes); columns: ["id", "date", "text", "target"]

## Public description

S&P 500 5‑Day Return from Daily Financial Headlines (Regression)

Problem statement
Given all financial news headlines published on each trading day t, predict the 5‑trading‑day forward percentage return of the S&P 500 index: r_t = close[t+5]/close[t] − 1. You are provided text-only inputs aggregated per day. Your task is to learn how news sentiment/semantics relate to near‑term market movement.

Files you will use
- train.csv: Training rows with columns [id, date, text, target]. The target is the 5‑day forward return for that date.
- test.csv: Test rows with columns [id, date, text]. Predict a numeric value for each id.
- sample_submission.csv: Example submission with columns [id, prediction].

Data construction details
- Headlines are grouped by trading date and concatenated into a single document per date using the separator " [SEP] ". Duplicate headlines within the same date are removed, but cross‑date duplicates are kept.
- Labels (targets) are computed as 5‑trading‑day forward returns using the closing prices associated with each date in the original dataset. The last five trading dates have no defined target and are excluded from train/test rows.
- Chronological split ensures realistic evaluation and prevents look‑ahead leakage. Train covers earlier years; test covers the most recent years.

Target definition
For each date t included in train/test rows:
- target = close[t+5]/close[t] − 1 (a real number, typically a few percent in magnitude)
Note: Only text and date are provided in the competition files; no prices are included.

Evaluation
- Metric: Mean Absolute Error (MAE)
- Lower MAE is better. Your submission must contain exactly two columns named id and prediction, one row per test id. Predictions must be finite real numbers.

Suggested approaches (not required)
- Text preprocessing and normalization (e.g., case‑folding, Unicode normalization)
- Feature engineering (bag‑of‑words/TF‑IDF, financial sentiment lexicons, NER/tickers)
- Sequence models (e.g., linear models, gradient boosting on text features, transformer encoders)
- Temporal modeling/regularization to handle regime changes

Important notes
- The split is strictly chronological. Do not use any information from future dates when training features or models.
- Text length per day varies widely (from 1 to dozens of headlines). Methods should be robust to variable document length.
- This is a regression task with small signal‑to‑noise. MAE provides a robust and interpretable objective.
