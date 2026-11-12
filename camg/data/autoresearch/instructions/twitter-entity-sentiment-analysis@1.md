# OpenMLE-fast task

Task ID: `twitter-entity-sentiment-analysis@1`

Native metric: `TwitterEntitySentimentMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3349 bytes)
- `data/sample_submission.csv` (12907 bytes); columns: ["id", "sentiment"]
- `data/test.csv` (154073 bytes); columns: ["id", "entity", "text"]
- `data/train.csv` (10068819 bytes); columns: ["id", "entity", "sentiment", "text"]

## Public description

Twitter Entity Sentiment Analysis Challenge

Problem statement:
Given a tweet and a specified target entity (e.g., Microsoft, FIFA, Borderlands), predict the sentiment expressed toward that entity. The task is entity-targeted sentiment classification with four classes: Positive, Negative, Neutral, Irrelevant.

Data description:
- Train file: train.csv
  - Columns (with header): id, entity, sentiment, text
  - id: a unique row identifier (integer). Do not use it as a predictive feature.
  - entity: the target entity name mentioned or discussed in the tweet (string).
  - sentiment: the ground-truth label among {Positive, Negative, Neutral, Irrelevant}.
  - text: the tweet text (string), multilingual and noisy, may contain URLs, mentions, hashtags, emojis, and punctuation.
- Test file: test.csv
  - Columns (with header): id, entity, text
  - Same schema as train.csv but without the sentiment label.
- Submission format:
  - sample_submission.csv is provided with header and two columns: id, sentiment.
  - Your submission must be a CSV with a header exactly: id,sentiment.
  - It must contain every id from test.csv exactly once, with a predicted sentiment from {Positive, Negative, Neutral, Irrelevant}.

Recommendations for data processing:
- Robust CSV reading with UTF-8; tweets may contain quotes and commas.
- Light normalization is helpful but optional: normalize URLs (e.g., <URL>), user mentions (e.g., <USER>), and whitespace; retain hashtags and emojis to preserve signal.
- Treat the entity string as an input feature (e.g., prepend "[ENTITY] <name>" to the tweet) or as a categorical feature.
- Remove only exact duplicate rows during your own processing if desired; near-duplicates are intentionally kept to preserve task difficulty.

Evaluation metric:
- Macro-averaged F1 across the four classes: Positive, Negative, Neutral, Irrelevant.
- Definition: For each class c, F1_c = 2 * TP_c / (2 * TP_c + FP_c + FN_c). Macro-F1 is the arithmetic mean of F1_c over all classes.
- Numerical stability: If the denominator (2*TP + FP + FN) is 0 for a class, its F1 is defined as 0 to avoid undefined values.
- Rationale: The distribution of classes is imbalanced. Macro-F1 equally weights all classes, rewarding balanced performance across Positive, Negative, Neutral, and Irrelevant.

Final files provided for the competition:
- train.csv (training data with labels)
- test.csv (test data without labels)
- sample_submission.csv (format example with valid labels)

What makes this task challenging and meaningful:
- Tweets are multilingual and noisy, including sarcasm, slang, code-switching, and varied punctuation.
- Sentiment is entity-specific: the same tweet may be positive about one entity and negative about another.
- The distinction between Neutral and Irrelevant requires careful modeling.

Expected participant workflow:
- Data processing: clean and normalize text minimally; handle multilingual content.
- Feature engineering: entity-aware representations, hashtag/emoji handling, URL and mention normalization.
- Model training: fine-tune multilingual transformer models or build strong classical baselines; use class weighting or focal loss to address imbalance.
- Model evaluation: use cross-validation on the training set; optimize Macro-F1; ensure predictions cover all test ids and follow the submission format.
