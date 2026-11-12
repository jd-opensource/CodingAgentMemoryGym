# OpenMLE-fast task

Task ID: `mcdonalds-reviews@1`

Native metric: `McDonaldsReviewMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2321 bytes)
- `data/sample_submission.csv` (3638 bytes); columns: ["row_id", "Like"]
- `data/test.csv` (20938 bytes); columns: ["row_id", "yummy", "convenient", "spicy", "fattening", "greasy", "fast", "cheap", "tasty", "expensive", "healthy", "disgusting", "Age", "VisitFrequency", "Gender"]
- `data/train.csv` (86220 bytes); columns: ["row_id", "yummy", "convenient", "spicy", "fattening", "greasy", "fast", "cheap", "tasty", "expensive", "healthy", "disgusting", "Age", "VisitFrequency", "Gender", "Like"]

## Public description

Competition: Predict McDonald’s Overall Liking (−5 to +5)

Problem statement
Participants are given anonymized survey responses from 1,453 Australian adults describing their perceptions of McDonald’s across 11 attributes (Yes/No), along with Age, Gender, and VisitFrequency. The task is to predict each respondent’s overall liking score on an integer scale from −5 (strong dislike) to +5 (strong like).

Why this is challenging
- The target is ordinal and discrete (11 levels), which rewards models that capture ordered structure rather than simple classification.
- The 11 binary perceptions are correlated (e.g., fattening/healthy/greasy/tasty trade-offs), and demographic/behavioral signals interact with perceptions.
- Small-sample regime (N≈1.5k) requires careful regularization and validation.

Files provided
- train.csv: Rows with features and the ground-truth target column Like.
- test.csv: Rows with features only; the Like column is withheld.
- sample_submission.csv: Correct file format with randomly generated placeholder predictions.

Target and features
- Target: Like (integer in [−5, +5]).
- Features:
  - Perception attributes (11 columns): yummy, convenient, spicy, fattening, greasy, fast, cheap, tasty, expensive, healthy, disgusting (values: Yes/No)
  - Demographics/behavior: Age (numeric), Gender (categorical), VisitFrequency (categorical)
- An ID column row_id uniquely identifies each row in test.csv and must be used in submissions.

Submission format
- A single CSV file with two columns and a header:
  - row_id: must exactly match the row_id values in test.csv
  - Like: your predicted overall liking; numeric values are allowed (integers or real numbers). Predictions outside [−5, +5] will be rejected.
- Do not include any additional columns.

Evaluation
- Metric: Mean Absolute Error (MAE) between your predictions and ground-truth Like values on the test set.
- Lower is better. MAE reflects the ordered nature of the target and is robust to outliers.

Notes
- All classes present in test are represented in train; no label leakage exists (the Like column is not present in test.csv).
- You may use any modeling approach that respects the format. Typical baselines include regularized linear/ordinal regression, tree-based gradient boosting, or calibrated classifiers.
