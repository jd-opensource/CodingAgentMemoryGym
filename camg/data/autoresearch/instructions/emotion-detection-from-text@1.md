# OpenMLE-fast task

Task ID: `emotion-detection-from-text@1`

Native metric: `EmotionClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2570 bytes)
- `data/sample_submission.csv` (152903 bytes); columns: ["id", "label"]
- `data/test.csv` (689696 bytes); columns: ["id", "text"]
- `data/train.csv` (3020221 bytes); columns: ["id", "text", "label"]

## Public description

Competition: 13-Class Emotion Recognition in Tweets (Macro-F1)

Problem statement
Build a model that predicts the underlying emotion expressed in a short tweet. Each tweet belongs to exactly one of 13 emotion classes: anger, boredom, empty, enthusiasm, fun, happiness, hate, love, neutral, relief, sadness, surprise, worry.

Files provided
- train.csv: Training data with labels.
- test.csv: Test data without labels.
- sample_submission.csv: A sample prediction file with the correct format.

Data format
- train.csv columns:
  - id: Unique identifier for the tweet (string).
  - text: The tweet content (string, raw and unnormalized).
  - label: The emotion class (one of the 13 labels).
- test.csv columns:
  - id: Unique identifier for the tweet (string).
  - text: The tweet content (string, raw and unnormalized).
- sample_submission.csv columns:
  - id: Unique identifier matching those in test.csv.
  - label: The predicted emotion class.

Evaluation
- Primary metric: Macro-averaged F1-score across the 13 classes.
  - For each class c, compute F1(c) from its precision and recall (with 0 used when a denominator is 0). The final score is the unweighted mean over all classes present in the test set.
  - Ties are broken by higher micro-averaged F1 (reported in the hosted metric implementation but not used for ranking).

Notes and recommendations
- Data preprocessing choices (tokenization, normalization of URLs/mentions/hashtags, casing, punctuation handling) are up to participants. Tweets are short and noisy and may contain mentions (@user), URLs, emojis, and colloquialisms.
- Class distribution is highly imbalanced. Strong solutions typically consider class weighting, focal loss, threshold tuning, or augmentation, and ensure robust validation.
- The split is group-aware by identical text content to prevent duplicate tweets from appearing across splits (avoiding leakage by memorization). All classes present in the test set occur at least once in the training set.

Submission format
- A CSV file with header containing two columns: id,label
- One row per id present in test.csv. The set of id values must match test.csv exactly.
- Predictions for label must be one of the 13 classes listed above.

Rules
- External data is allowed only if made publicly available under a compatible license and disclosed as per competition rules. Pretrained language models are allowed.
- No manual labeling of the test set.

Baseline
- Reasonable baselines include TF-IDF + linear classifiers, or pretrained transformer encoders fine-tuned on the training data.
