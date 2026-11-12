# OpenMLE-fast task

Task ID: `mental-health-corpus@1`

Native metric: `MentalHealthRiskClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3251 bytes)
- `data/sample_submission.csv` (158273 bytes); columns: ["id", "risk_probability"]
- `data/test.csv` (2640235 bytes); columns: ["id", "text"]
- `data/train.csv` (10681769 bytes); columns: ["id", "text", "label"]

## Public description

Mental Health Risk Text Classification (Binary)

Problem statement
Given a user-generated post/comment, predict the likelihood that it contains high-risk mental health language (positive class) versus not (negative class). Your model should output a probability for the positive class to enable effective ranking and triage.

Files provided
- train.csv: Labeled training data with columns
  - id: Unique identifier for each row
  - text: The raw post/comment text
  - label: Binary target, 1 indicates high-risk language, 0 indicates non-risk
- test.csv: Unlabeled test data with columns
  - id: Unique identifier for each row
  - text: The raw post/comment text
- sample_submission.csv: A valid example of the required submission format with columns
  - id
  - risk_probability: Your model’s predicted probability of label = 1 for the corresponding id in test.csv

Task
Build a machine learning model that, given text, outputs a probability that the text contains high-risk language. Long and noisy texts, domain slang, and subtle cues make this problem challenging; careful preprocessing and modeling are expected to perform well.

Data description
- Source domain: Community posts related to anxiety, depression, and broader mental health topics.
- Scale: ≈28k rows, variable and often long text lengths (long-tail distribution).
- Labels: Binary (0 = non-risk, 1 = risk). Both labels are present in train and test.
- Splitting: The organizer split groups of identical texts together to avoid leakage. A single deterministic split is provided, stratified by label and text-length buckets to reduce distribution drift.

Evaluation
- Metric: Average Precision (AP) for the positive class, computed from your predicted risk_probability values and the hidden ground truth labels for test rows.
  - AP emphasizes ranking quality under class imbalance and balances precision and recall where it matters most.
  - Predictions should be numeric probabilities in [0, 1]. Values outside this range will be clipped for scoring.
- Submission format: A single CSV with exactly two columns in this order: id, risk_probability. It must include every id from test.csv exactly once.

Recommendations (non-binding)
- Text preprocessing: Lowercasing, whitespace normalization, and removal of simple HTML artifacts can help; preserve emojis/emoticons and slang where useful.
- Long text handling: Consider smart truncation (e.g., head+tail), sliding window inference with pooling, or long-context models to capture key cues.
- Modeling: Strong linear baselines with n-grams and regularization, fine-tuned Transformer encoders, or hybrid approaches often work well. Calibrate probabilities for better ranking.
- Robustness: Guard against spurious correlations and overfitting to annotation artifacts; validate carefully via cross-validation on train data.

Submission
- Create a file with columns: id, risk_probability
- Ensure row coverage equals the number of rows in test.csv and that ids match exactly.
- The leaderboard is ranked by Average Precision (higher is better).

Ethical note
This dataset contains sensitive mental health content, including crisis language. Use responsibly and avoid deploying models without appropriate human-in-the-loop safeguards.
