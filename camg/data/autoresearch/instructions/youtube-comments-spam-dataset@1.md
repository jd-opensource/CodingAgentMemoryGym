# OpenMLE-fast task

Task ID: `youtube-comments-spam-dataset@1`

Native metric: `YouTubeCommentSpamMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2916 bytes)
- `data/sample_submission.csv` (8664 bytes); columns: ["id", "probability_of_spam"]
- `data/test.csv` (116953 bytes); columns: ["id", "content", "date", "video_name"]
- `data/train.csv` (206224 bytes); columns: ["id", "content", "date", "video_name", "class"]

## Public description

Title: YouTube Comment Spam Generalization Challenge

Problem statement
Build a model that predicts whether a YouTube comment is spam (1) or not (0). The task emphasizes generalization across videos: the training data contains comments from some videos, while the test data contains comments from different, unseen videos. You must submit calibrated probabilities of spam for each test comment.

Data description
You are provided with preprocessed CSV files derived from a public YouTube comments dataset of 1,956 labeled comments across five highly viewed music videos. The provided columns are:
- id: Unique identifier for each comment (synthetic; no semantic meaning)
- content: The text of the comment
- date: Timestamp string of when the comment was posted. If the original date is missing, a placeholder token "unknown" is used.
- video_name: The title of the YouTube video where the comment was posted
- class (train only): Target label (1 = spam, 0 = not spam)

Files
- train.csv: Labeled training data with columns [id, content, date, video_name, class]
- test.csv: Unlabeled test data with columns [id, content, date, video_name]
- sample_submission.csv: A valid sample submission with columns [id, probability_of_spam]

Important notes
- Train and test are split by video to enforce domain shift. Use video_name and date as context features if helpful, but do not expect authors or raw comment identifiers (they are intentionally excluded to prevent non-generalizable shortcuts).
- The labels are balanced overall, and both classes appear in training and test.
- The dataset size is small enough for classical NLP (e.g., TF-IDF + linear models) and modern text models with appropriate regularization and preprocessing.

Evaluation
- Submissions must be a CSV file with columns: [id, probability_of_spam].
  - id: Must match exactly the ids in test.csv (unique, no duplicates, no extras).
  - probability_of_spam: A probability in [0, 1] for the spam class.
- The competition metric is LogLoss (binary cross-entropy) averaged over all test rows. Probabilities will be clipped to a small epsilon from 0 and 1 for numerical stability.

Suggested modeling approaches
- Text preprocessing: lowercasing, Unicode normalization, collapsing whitespace; optional normalization of URLs/handles/numbers to special tokens.
- Feature engineering: word/character n-grams, URL/handle presence, length features, temporal features (e.g., hour-of-day or an "unknown" date indicator), and a video_name indicator.
- Models: logistic regression, linear SVM with calibrated probabilities, gradient boosting on engineered features, or transformer-based classifiers.

Submission format
- CSV with header: id,probability_of_spam
- Example:
  id,probability_of_spam
  10001,0.42
  10002,0.07
  ...

Good luck, and focus on building models that generalize across unseen videos while maintaining well-calibrated probability estimates.
