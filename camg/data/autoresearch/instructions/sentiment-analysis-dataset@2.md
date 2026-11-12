# OpenMLE-fast task

Task ID: `sentiment-analysis-dataset@2`

Native metric: `HashtagRobustnessSentimentMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1718 bytes)
- `data/sample_submission.csv` (15632 bytes); columns: ["id", "prob_negative"]
- `data/test.csv` (204186 bytes); columns: ["id", "tweet"]
- `data/train.csv` (892885 bytes); columns: ["id", "tweet", "label"]

## Public description

Hashtag Robustness Sentiment Challenge

Problem
Build a model that predicts the probability that a tweet expresses negative sentiment. The twist: the test set is constructed to be out-of-domain with respect to the most frequent hashtags in the training data. Models that overly rely on specific hashtags or URL patterns should underperform, while models that capture generalizable semantics will do better.

Data
- train.csv: id, tweet, label
  - label is 1 for negative sentiment and 0 otherwise.
- test.csv: id, tweet (labels hidden)
- sample_submission.csv: id, prob_negative (example predictions format)

Notes
- Tweets are short, noisy, and often contain hashtags, mentions, emojis, and URLs.
- The split is deterministic, grouped by exact tweet text to avoid near-duplicate leakage.
- The test distribution under-represents many of the highest-frequency hashtags seen in training.

Evaluation
- Submissions must contain two columns: id, prob_negative
- prob_negative is the predicted probability that label == 1 for each id in test.csv.
- The leaderboard metric is ROC AUC computed on the hidden test labels.

What makes it challenging and meaningful
- Distribution shift on hashtags encourages robust modeling beyond memorizing token shortcuts.
- Strong baselines include regularized n-gram models and pretrained transformers with careful preprocessing (e.g., hashtag and URL normalization).
- Feature engineering ideas: hashtag segmentation/normalization, URL/mention masking, character- and subword-level representations, adversarial dropout, and reweighting.

File expectations
- Do not assume any label information in test.csv.
- No paths are embedded in the CSVs.
- Ids are unique and stable across files.
