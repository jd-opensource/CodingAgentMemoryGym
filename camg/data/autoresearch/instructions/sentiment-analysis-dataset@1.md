# OpenMLE-fast task

Task ID: `sentiment-analysis-dataset@1`

Native metric: `SmartphoneTweetSentimentMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1881 bytes)
- `data/sample_submission.csv` (38224 bytes); columns: ["id", "prob_negative"]
- `data/test.csv` (217475 bytes); columns: ["id", "tweet"]
- `data/train.csv` (871674 bytes); columns: ["id", "tweet", "label"]

## Public description

Smartphone Tweet Sentiment: Binary Classification Challenge

Problem statement
- Task: Given the text of a tweet, predict the probability that its sentiment is negative.
- Target definition: label==1 indicates negative sentiment; label==0 indicates non-negative (positive/neutral).
- Input: Short, noisy tweets with hashtags, mentions, URLs, emojis, and slang centered around smartphones and related brands.

Provided files
- train.csv: columns [id, tweet, label]
- test.csv: columns [id, tweet]
- sample_submission.csv: columns [id, prob_negative]

Important notes about the split
- Deterministic 80/20 train/test split with a fixed random seed.
- Stratification preserves class proportions.
- Grouping by identical tweet text prevents exact text duplicates from being split across train and test, avoiding leakage.

Evaluation
- Your submission must be a CSV with the following columns:
  - id: the sample identifier matching test.csv
  - prob_negative: your predicted probability P(label==1) as a real number in [0, 1]
- Metric: ROC AUC computed on prob_negative for the negative class (label==1).
  - Why ROC AUC? It is threshold-independent, handles class imbalance robustly, and evaluates the ranking quality of predicted probabilities.

Data details and guidelines
- Text is provided as-is (including hashtags, mentions, URLs). Competitors are free to choose any preprocessing/tokenization approach.
- No additional metadata is provided; id serves only as a row identifier.
- You may use any modeling approach (e.g., linear models with n-grams, gradient-boosted trees on engineered features, CNN/RNN, or pretrained transformers). Calibration of probabilities is recommended.

Rules and validation
- Submission IDs must exactly match the IDs in test.csv with no duplicates or missing rows.
- prob_negative must be numeric and bounded in [0, 1].

Good luck and happy modeling!
