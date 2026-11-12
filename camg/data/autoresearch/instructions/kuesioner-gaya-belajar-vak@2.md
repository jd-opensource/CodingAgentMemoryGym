# OpenMLE-fast task

Task ID: `kuesioner-gaya-belajar-vak@2`

Native metric: `VAKLearningStyleMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2138 bytes)
- `data/sample_submission.csv` (2250 bytes); columns: ["id", "label"]
- `data/test.csv` (7761 bytes); columns: ["id", "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10", "Q11", "Q12"]
- `data/train.csv` (25863 bytes); columns: ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10", "Q11", "Q12", "label"]

## Public description

VAK Learning Style Classification from Likert Responses

Problem statement
Predict the dominant learning style label (V = Visual, A = Auditory, K = Kinesthetic) from 12 Likert-scale questionnaire items (integer responses 1–4). Each row corresponds to one respondent’s answers.

Data description
- Input features: Q1–Q12 (12 ordered categorical/integer items, each in {1,2,3,4}).
- Target: label ∈ {V, A, K} for training data only.
- Final files provided to participants:
  - train.csv: columns Q1–Q12, label
  - test.csv: columns id, Q1–Q12
  - sample_submission.csv: columns id, label (example format with placeholder predictions)

Notes
- Only use Q1–Q12 for modeling. Any other aggregate columns have been removed to keep the task focused on learning from item-level patterns.
- Labels are mildly imbalanced; robust handling of class imbalance is recommended.

Evaluation
- Metric: Macro F1 over classes {V, A, K}.
  - For each class, compute F1 = 2 × precision × recall / (precision + recall), treating division-by-zero as 0.
  - The final score is the unweighted mean of per-class F1.
- Submission format: CSV with exactly two columns in this order: id, label. The id values must match test.csv exactly and appear once each. The label values must be in {V, A, K}.

Suggested approach (non-exhaustive)
- Data processing: ensure Q1–Q12 are interpreted as ordered categorical or integers; optional normalization to [0,1].
- Feature engineering: ordinal encodings; interaction features between items; response-pattern features.
- Modeling: tree ensembles (e.g., gradient boosting, random forests), regularized linear models, or shallow neural networks. Calibrated probabilities may help.
- Validation: stratified k-fold cross-validation; consider group-aware folds if you detect exact duplicate response vectors.

Rules and constraints
- Runtime is not restricted here; focus on correctness and robustness.
- Do not attempt to infer or use any labels from file names or hidden metadata; only Q1–Q12 and the label in train.csv are relevant.

Good luck and have fun building a robust classifier for VAK learning styles!
