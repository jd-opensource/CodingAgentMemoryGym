# OpenMLE-fast task

Task ID: `kohli-international-score-log@1`

Native metric: `KohliFiftyPlusMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2684 bytes)
- `data/sample_submission.csv` (2898 bytes); columns: ["row_id", "prob_50plus"]
- `data/test.csv` (5511 bytes); columns: ["row_id", "Format", "Opposition", "Ground", "Pos", "Inns", "StartDate"]
- `data/train.csv` (22245 bytes); columns: ["row_id", "Format", "Opposition", "Ground", "Pos", "Inns", "StartDate", "is_50plus"]

## Public description

Title: Kohli 50+ Probability from Pre‑Match Context

Background
Virat Kohli’s international batting spans Tests, ODIs, and T20Is across venues and opponents worldwide. Before an innings begins, some information is already known: match format, opponent, venue, batting position, and the innings number. Can we use this pre‑match context to predict the chance that Kohli scores 50 or more in that innings?

Problem Statement
Binary probabilistic classification. For each international innings, predict the probability that the score is at least 50.

Data Description
You will receive tabular data with one row per international innings.
- Features (pre‑match context only):
  - Format (Test, ODI, T20I)
  - Opposition (opposing team)
  - Ground (venue)
  - Pos (batting position as integer)
  - Inns (innings number in the match)
  - StartDate (date string for the match start, ISO style YYYY‑MM‑DD)
  - row_id (unique identifier for each row)
- Target (train only):
  - is_50plus (1 if Runs_scored ≥ 50, else 0)

Final files provided
- train.csv — rows with features plus is_50plus.
- test.csv — rows with features only (no target).
- sample_submission.csv — example of the required submission format.

Train/Test Split
The split is strictly chronological by StartDate to prevent look‑ahead. The first 80% of innings form the training set; the last 20% form the test set. All classes (0 and 1) occur at least once in the training set.

Modeling Guidance
Participants should apply ML techniques including:
- Data processing and cleansing (e.g., parsing StartDate, trimming text, encoding categorical variables)
- Feature engineering from pre‑match context (e.g., year/month, venue/opponent history, recency features computed only from past innings)
- Model training (e.g., logistic regression, calibrated tree‑based models, or other probabilistic classifiers)
- Model evaluation and calibration
Do not use any post‑innings outcome information in features.

Submission Format
Submit a CSV with the following columns:
- row_id — must match the ids in test.csv
- prob_50plus — predicted probability in [0, 1] that is_50plus = 1
The evaluator will align on row_id and compute the metric.

Evaluation Metric
Log Loss (cross‑entropy) on the test set:
LL = mean over rows of [ −y·log(p) − (1−y)·log(1−p) ], with p clipped to [1e−15, 1−1e−15] to avoid numerical issues.

Notes
- The data has moderate class imbalance; well‑calibrated probabilities are important.
- Time‑aware validation (e.g., rolling or forward validation) is recommended.
- Ensure any aggregate features use only information available before the innings being predicted.
