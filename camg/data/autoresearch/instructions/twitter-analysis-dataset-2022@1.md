# OpenMLE-fast task

Task ID: `twitter-analysis-dataset-2022@1`

Native metric: `TweetPolarityMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2812 bytes)
- `data/sample_submission.csv` (98088 bytes); columns: ["id", "probability"]
- `data/test.csv` (600933 bytes); columns: ["id", "tweet"]
- `data/train.csv` (2521673 bytes); columns: ["id", "label", "tweet"]

## Public description

Title: Tweet Polarity Detection (Negative vs Non-negative)

Background
Twitter posts are short, noisy, and often include emojis, mentions, hashtags, and URLs. Detecting negative sentiment reliably in such texts is a practical NLP task with clear applications in moderation and customer support.

Problem Statement
Given a tweet, predict whether it expresses negative polarity (label=1) or not (label=0). Your model should output the probability that each tweet is negative.

Data Description
- Each row is a tweet with three fields:
  - id: unique identifier for submission mapping
  - tweet: raw text content (UTF-8, may include emojis, URLs, hashtags, mentions)
  - label: binary target, 1 for negative sentiment and 0 otherwise (only present in the training set)
- Final competition files:
  - train.csv: columns [id, label, tweet]
  - test.csv: columns [id, tweet]
  - sample_submission.csv: columns [id, probability]

Important Notes
- The id column is for submission indexing only; it should not be used as a predictive feature.
- The split is designed to prevent leakage from duplicate tweets: no identical normalized tweet text appears in both train and test.
- Tweets with conflicting labels under normalization are excluded from the test set to ensure clean evaluation.

Recommended Data Processing
- Preserve raw text as the primary feature while applying careful preprocessing:
  - Lowercasing and Unicode normalization
  - Replace URLs with a placeholder
  - Replace @mentions with a placeholder and keep hashtags as tokens
  - Ensure robust UTF-8 handling for emojis and special characters
- Handle duplicates and near-duplicates thoughtfully; the split already avoids exact duplicate text across train/test under normalization.

Evaluation Metric
- Primary metric: Average Precision (AP) for the positive class (label=1) based on submitted probabilities.
- Rationale: AP focuses on ranking quality for the minority positive class, is threshold-free, and is robust to class imbalance. Predicting all negatives yields very low AP, making the task fairly evaluated.

Submission Format
- Submit a CSV with columns:
  - id: matching the ids in test.csv
  - probability: your predicted probability that the tweet is negative (label=1)
- The leaderboard score is computed using Average Precision on the held-out test set.

What Makes This Challenging
- Class imbalance (negative tweets are the minority)
- Noisy social-media text (emojis, hashtags, code-switching, URLs, mentions)
- Topic diversity and informal language reduce the effectiveness of simple keyword rules

Expectations
- Successful solutions will combine robust preprocessing, feature engineering (e.g., TF-IDF, subword/character features), and model training (e.g., linear classifiers or transformers) to achieve competitive performance.
