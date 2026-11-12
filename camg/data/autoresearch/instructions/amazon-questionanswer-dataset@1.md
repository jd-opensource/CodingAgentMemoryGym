# OpenMLE-fast task

Task ID: `amazon-questionanswer-dataset@1`

Native metric: `AmazonQATimeToFirstAnswerMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2399 bytes)
- `data/sample_submission.csv` (270344 bytes); columns: ["question_id", "time_to_first_answer_hours"]
- `data/test.csv` (1873183 bytes); columns: ["question_id", "question_type", "category", "asker_id", "question_time", "question_text"]
- `data/train.csv` (7711504 bytes); columns: ["question_id", "question_type", "category", "asker_id", "question_time", "question_text", "time_to_first_answer_hours"]

## Public description

Amazon Product Q&A: Time-to-First-Answer Prediction

Problem statement
Build a model that predicts how long it takes (in hours) for a newly asked product question to receive its first answer. You must make predictions using only the information available at question time (question text and metadata). The label is deterministically derived from the earliest observed answer timestamp per question.

Files
- train.csv: Training set with features and the target column time_to_first_answer_hours.
- test.csv: Test set with the same feature columns as train.csv but without the target.
- sample_submission.csv: A valid example submission file with random, valid predictions.

Columns
- question_id: Unique identifier for a question.
- question_type: The type of question (e.g., yes/no, open-ended).
- category: Product category.
- asker_id: Pseudonymous identifier for the asker.
- question_time: The date the question was asked (ISO date string). You may derive temporal features such as hour-of-day, day-of-week, seasonality, etc.
- question_text: The free-text content of the question.
- time_to_first_answer_hours (train only): Target label, computed as the elapsed hours between question_time and the earliest answer time for that question.

Evaluation
- Metric: Root Mean Squared Logarithmic Error (RMSLE) on time_to_first_answer_hours.
- Definition: RMSLE = sqrt( mean( (log1p(y_pred) - log1p(y_true))^2 ) ).
- Requirements: Predictions must be non-negative real numbers. The submission must contain exactly the rows and IDs in test.csv.

Submission format
- A CSV with the following columns in this order:
  - question_id
  - time_to_first_answer_hours
- The file must include exactly one row per question_id present in test.csv.

Notes and tips
- This is a heavy-tailed regression problem (minutes to weeks). RMSLE emphasizes multiplicative calibration and reduces sensitivity to extreme outliers.
- Strong baselines often combine text features (n-grams, embeddings) with metadata (category, question_type, temporal signals) derived from question_time.
- You may train language models or embeddings on any text available in train.csv and other public resources subject to typical competition rules; be careful to avoid any information from answers at prediction time.
- No answer-side information (e.g., answer text or timestamps) is present in train/test and must not be used for inference.
