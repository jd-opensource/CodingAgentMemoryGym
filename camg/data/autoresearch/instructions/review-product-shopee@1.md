# OpenMLE-fast task

Task ID: `review-product-shopee@1`

Native metric: `ShopeeReviewQWKMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (786 bytes)
- `data/komentar shopee.csv` (62801 bytes); columns: ["No.", "komentar"]
- `data/sample_submission.csv` (4798 bytes); columns: ["id", "rating"]
- `data/test.csv` (55246 bytes); columns: ["id", "comment"]
- `data/train.csv` (224410 bytes); columns: ["id", "comment", "rating"]

## Public description

Shopee Speaker Reviews – Ordinal Star Rating Prediction (ID)

Files in this directory (public/):
- train.csv: Labeled training set with columns [id, comment, rating] where rating ∈ {1,2,3,4,5}.
- test.csv: Unlabeled test set with columns [id, comment].
- sample_submission.csv: Example submission file with columns [id, rating].
- komentar shopee.csv (optional): Additional unlabeled Indonesian reviews for unsupervised use.

Submission format:
- Submit a CSV with columns: id, rating.
- The set of ids must match test.csv exactly (order does not matter).
- rating values may be real numbers; they are clipped to [1,5] and rounded for evaluation.

Evaluation metric:
- Primary: Quadratic Weighted Kappa (QWK) between rounded predictions and ground-truth ratings (higher is better).
