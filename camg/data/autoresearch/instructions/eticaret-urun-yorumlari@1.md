# OpenMLE-fast task

Task ID: `eticaret-urun-yorumlari@1`

Native metric: `TurkishEcommerceReviewsMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2100 bytes)
- `data/sample_submission.csv` (27315 bytes); columns: ["id", "label"]
- `data/test.csv` (292341 bytes); columns: ["id", "review_text"]
- `data/train.csv` (1196991 bytes); columns: ["id", "review_text", "label"]

## Public description

Turkish E-commerce Review Sentiment (3-class)

Problem statement
Given a Turkish product review, predict its sentiment among {0=negative, 1=positive, 2=neutral}. Build robust NLP models that handle colloquial Turkish, typos, emojis, and the minority neutral class.

Data provided
- train.csv
  - id: unique identifier
  - review_text: Turkish review text
  - label: sentiment class (0, 1, or 2)
- test.csv
  - id: unique identifier
  - review_text: Turkish review text
- sample_submission.csv
  - id: copied from test.csv
  - label: example predictions (0, 1, or 2)

Splitting and integrity
- Stratified split by label with a deterministic seed preserves overall class proportions.
- Exact duplicate review_text strings are grouped so no identical text appears across train and test (to prevent leakage). Duplicates may exist within train or within test.
- All sentiment classes present in the test set also occur at least once in the training set.
- IDs are unique and non-overlapping between train and test.

Submission format
- A valid submission must be a CSV with exactly two columns: id, label.
- Include every id appearing in test.csv exactly once; no extra or missing ids.
- label values must belong to {0, 1, 2} and be integers.

Evaluation metric
- Macro-averaged F1 across the three classes {0, 1, 2}.
  - Each class contributes equally, addressing moderate imbalance and penalizing models that ignore the neutral class.
  - The score is computed from the confusion matrix with standard precision/recall definitions per class.

Modeling guidance
- Preserve Turkish characters (ç, ğ, ı, İ, ö, ş, ü) and consider case/diacritic normalization if helpful.
- Expect noisy and informal text (slang, spelling variants, emojis). Robust tokenization and preprocessing can help.
- Strong baselines include TF–IDF + linear classifiers with class weighting; transformer models like BERTurk or mBERT may further improve performance.

Goal
Design end-to-end systems that perform high-quality multiclass sentiment classification on Turkish e-commerce reviews with fair, leakage-safe evaluation.
