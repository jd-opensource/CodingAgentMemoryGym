# OpenMLE-fast task

Task ID: `spam-mails-dataset@1`

Native metric: `SpamDetectionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2704 bytes)
- `data/sample_submission.csv` (28608 bytes); columns: ["id", "spam_probability"]
- `data/test.csv` (1139187 bytes); columns: ["id", "text"]
- `data/train.csv` (4327030 bytes); columns: ["text", "label"]

## Public description

Competition: Enron-1 Email Spam Detection (Leakage-Safe Split)

Background
Corporate email systems receive a mix of legitimate messages (ham) and unwanted messages (spam). Effective spam filtering requires robust text modeling, strong generalization beyond duplicated content, and good probability calibration.

Problem Statement
Given the full raw email text, predict whether the email is spam. Your model should output a calibrated probability for the “spam” class.

Data Description
You will receive a binary text classification dataset derived from the Enron-1 corpus.
- Training data: train.csv
  - Columns: text, label
  - text: Full email content including subject line and body
  - label: "ham" or "spam"
- Test data: test.csv
  - Columns: id, text
  - text: Full email content including subject line and body
  - id: An anonymized identifier for each test email
- Submission format: sample_submission.csv
  - Columns: id, spam_probability
  - spam_probability: A floating-point number in [0, 1] indicating the predicted probability that the email is spam

Important characteristics:
- Class imbalance is present (approximately 71% ham, 29% spam).
- The split is group-aware by exact-text hash: any exact duplicate emails are placed entirely in either train or test to prevent leakage.
- Non-informative columns (e.g., export indices or numeric encodings of the label) are removed from the released features.

Evaluation Metric
- Primary metric: Log Loss (binary cross-entropy) on the spam class probability.
  - This proper scoring rule rewards calibrated probabilities and penalizes overconfident errors.
  - Predictions must be valid probabilities in [0, 1].

What makes this challenging and meaningful
- Long, noisy texts with obfuscation tactics (e.g., misspellings, random tokens) require robust NLP modeling.
- Imbalance and the need for probability calibration favor principled approaches.
- Deduplicated, leakage-safe split emphasizes generalization rather than memorization of repeated content.

Guidance for participants (optional)
- Consider modern NLP approaches: TF-IDF + regularized linear models or fine-tuned compact transformers.
- Feature engineering ideas: token/character n-grams, URL/currency/obfuscation patterns, header cues like "Subject:".
- Use stratified cross-validation and calibration (e.g., Platt scaling or isotonic regression) to improve probability estimates.

Files provided
- train.csv: labeled training emails
- test.csv: unlabeled test emails with ids
- sample_submission.csv: example submission format

Your task
- Train a model on train.csv.
- Predict spam_probability for each id in test.csv.
- Submit a CSV with two columns: id and spam_probability.
