# OpenMLE-fast task

Task ID: `arabic-company-reviews@1`

Native metric: `ArabicCompanyReviewSentimentMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2397 bytes)
- `data/sample_submission.csv` (61738 bytes); columns: ["id", "rating"]
- `data/test.csv` (863987 bytes); columns: ["id", "review_description", "company"]
- `data/train.csv` (3464717 bytes); columns: ["id", "review_description", "company", "rating"]

## Public description

Arabic Company Review Sentiment Classification

Problem statement
You are given short user reviews in Arabic about various companies. Your task is to predict the sentiment of each review into one of three classes: -1 (negative), 0 (neutral), or 1 (positive). Reviews are noisy, dialectal, and highly imbalanced across companies and classes, making robust modeling essential.

Data
- train.csv: Labeled training data with columns [id, review_description, company, rating].
- test.csv: Unlabeled test data with columns [id, review_description, company].
- sample_submission.csv: Example submission format with columns [id, rating]. Use this to ensure your output shape and value types match the expected format.

Notes
- Text is in Arabic, includes punctuation, emojis, and occasional code-switching. No heavy preprocessing is applied in the provided files; you should build your own normalization/tokenization pipeline.
- Companies are highly imbalanced (one major company dominates the data, with a long tail of smaller ones). You may optionally use the company name as a categorical feature to help handle domain shifts.

Evaluation
- Official metric: Macro-averaged F1 over the three sentiment classes {-1, 0, 1} on the full test set.
  - Macro-F1 equally weights classes, which makes performance on the rare neutral class as important as performance on the majority classes.
  - Predictions must be integers from the set {-1, 0, 1}. Submissions with invalid labels or missing ids will be rejected.

Rules and recommendations
- Use the entire dataset. Efficient data processing and robust modeling are encouraged; runtime is not restricted.
- Consider Arabic-specific preprocessing: unify Alef forms, remove diacritics and tatweel, normalize digits, and handle elongated character repeats. Preserve punctuation/emojis if your tokenizer supports them.
- Feature engineering and modeling: try TF–IDF n-grams with linear models, or Arabic pretrained transformers (e.g., AraBERT/MARBERT). Incorporating the company feature may improve generalization across domains.

Submission format
- A CSV file named submission.csv with columns [id, rating].
- id must match exactly those in test.csv; rating must be one of {-1, 0, 1}.

Files provided
- train.csv
- test.csv
- sample_submission.csv

Good luck, and build a model that generalizes across companies and handles the rare neutral class effectively!
