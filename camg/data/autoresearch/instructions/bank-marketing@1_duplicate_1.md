# OpenMLE-fast task

Task ID: `bank-marketing@1_duplicate_1`

Native metric: `BankMarketingMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1169 bytes)
- `data/sample_submission.csv` (88236 bytes); columns: ["id", "y"]
- `data/test.csv` (731147 bytes); columns: ["id", "age", "job", "marital", "education", "default", "balance", "housing", "loan", "contact", "day", "month", "campaign", "pdays", "previous", "poutcome"]
- `data/train.csv` (2995783 bytes); columns: ["id", "age", "job", "marital", "education", "default", "balance", "housing", "loan", "contact", "day", "month", "campaign", "pdays", "previous", "poutcome", "y"]

## Public description

Title: Bank Telemarketing Conversion Prediction (Leakage-free)

Problem statement
Predict the probability that a contacted client will subscribe to a term deposit in an upcoming telemarketing campaign.

Final data files
- train.csv: Training set with features and target.
- test.csv: Test set with features only.
- sample_submission.csv: Example submission showing the expected format.

Data schema
All files are standard comma-separated CSV with UTF-8 encoding.
- Common columns (present in both train.csv and test.csv):
  id, age, job, marital, education, default, balance, housing, loan, contact, day, month, campaign, pdays, previous, poutcome
- Target column (only in train.csv):
  y (binary label; 1 = subscribed, 0 = not subscribed)
Notes:
- The original leaky field "duration" (last call duration in seconds) is intentionally excluded from train/test files.

Evaluation
- Metric: ROC AUC computed on the positive class (y = 1).
- Submission format: A single CSV with two columns: id, y. The y column must contain predicted probabilities for y=1 (values in [0,1]).

Split details
- Deterministic stratified split with 80/20 ratio to maintain class distribution.
