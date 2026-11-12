# OpenMLE-fast task

Task ID: `emotion-detection-from-text@2`

Native metric: `EmotionPolarityMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2758 bytes)
- `data/sample_submission.csv` (124872 bytes); columns: ["id", "label"]
- `data/test.csv` (654659 bytes); columns: ["id", "text"]
- `data/train.csv` (2892156 bytes); columns: ["id", "text", "label"]

## Public description

Competition: Tweet Polarity from Noisy Emotions

Problem statement
Given a short tweet, predict its sentiment polarity as one of three classes: negative, neutral, positive. Tweets are informal, noisy, and short; the target labels are derived deterministically from fine-grained emotion annotations. Your goal is to build a robust text classifier that performs well across all three polarities, not just the majority ones.

Data description
- Training data (train.csv):
  - id: unique integer identifier
  - text: the tweet content (string)
  - label: target polarity in {negative, neutral, positive}
- Test data (test.csv):
  - id: unique integer identifier
  - text: the tweet content (string)
- Sample submission (sample_submission.csv):
  - id, label columns. Replace label with your predictions from {negative, neutral, positive}.

Notes
- Tweets may include mentions, hashtags, URLs, emojis, and common social-media artifacts. Handling these robustly (e.g., normalization to placeholders) is up to you.
- The split is group-aware at the text level to avoid identical-tweet leakage; identical texts will not appear in both train and test.
- Labels are class-imbalanced, especially for the neutral class. Methods like class weighting, calibration, and thresholding may help.

Evaluation
- Primary metric: Macro-averaged F1 over the three classes {negative, neutral, positive}.
  - For each class k, F1_k = 2 * precision_k * recall_k / (precision_k + recall_k). If precision or recall are undefined for a class (e.g., zero predictions and/or zero true cases), its F1 is treated as 0 for that class.
  - Macro-F1 = (F1_negative + F1_neutral + F1_positive) / 3.
- The submission must contain exactly these columns and cover all test ids:
  - id: integer
  - label: one of {negative, neutral, positive}
- Any invalid/missing ids or labels, duplicate ids, or extra/missing rows will result in an invalid submission.

What makes this challenging
- Tweets are short and noisy, with slang and domain-specific cues.
- Neutral is the smallest and hardest class; Macro-F1 ensures fair evaluation across classes.
- Simple lexicon heuristics tend to overfit; robust preprocessing, feature engineering (e.g., character/word n-grams or subword tokenization), and modern language models can improve performance.

Getting started
- A strong baseline can be built using TF–IDF + linear models with class weighting, or a small pretrained transformer fine-tuned on the training data.
- Pay attention to preprocessing: lowercasing, user/URL/hashtag placeholders, and careful handling of emojis/punctuation often help.

Files you will use
- train.csv: training set with labels
- test.csv: test set without labels
- sample_submission.csv: shows the required submission format
