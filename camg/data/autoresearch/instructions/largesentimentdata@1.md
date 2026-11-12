# OpenMLE-fast task

Task ID: `largesentimentdata@1`

Native metric: `BanglaSentimentMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1217 bytes)
- `data/sample_submission.csv` (74776 bytes); columns: ["Label"]
- `data/test.csv` (1436303 bytes); columns: ["Platform", "Comment"]
- `data/train.csv` (3764280 bytes); columns: ["Platform", "Comment", "Label"]

## Public description

Bangla Emotion & Toxicity Multiclass Classification

Problem statement:
You are given short Bangla (Bengali) comments collected from social platforms. Your task is to predict the comment’s sentiment category among five classes:
0 = Toxic, 1 = Neutral, 2 = Sad, 3 = Funny, 4 = Happy.

Public data (relative to the public/ directory):
- train.csv: Labeled training data with columns Platform, Comment, Label.
- test.csv: Unlabeled test data with columns Platform, Comment.
- sample_submission.csv: A sample submission file with the correct format.

Notes:
- The primary feature is Comment (Bangla text). Platform is an optional categorical feature that may provide context.
- The split prevents exact-text leakage: identical Comment strings never appear in both train and test.

Evaluation:
- Metric: Macro F1 across the five classes {0,1,2,3,4}.

Submission format:
- Submit a single-column CSV with header Label and one integer per row in {0,1,2,3,4}, corresponding to each row in test.csv in the same order.

Recommendations:
- Ensure UTF-8 handling for Bangla script.
- Consider Bangla-aware tokenization or multilingual transformers (e.g., mBERT, XLM-R, bn-BERT).
- You may optionally use Platform as a feature.
