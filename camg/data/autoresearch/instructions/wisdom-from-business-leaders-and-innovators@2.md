# OpenMLE-fast task

Task ID: `wisdom-from-business-leaders-and-innovators@2`

Native metric: `QuoteAuthorIdentificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2472 bytes)
- `data/sample_submission.csv` (29221 bytes); columns: ["id", "author"]
- `data/test.csv` (352218 bytes); columns: ["id", "quote"]
- `data/train.csv` (1511933 bytes); columns: ["id", "quote", "author"]

## Public description

Competition: Closed-set Author Identification from Quote Text

Problem statement:
Given the text of a quote, predict the author who wrote it from a fixed set of authors. This is a multiclass text classification task that requires learning stylistic, thematic, and lexical cues tied to each author.

Data description:
The dataset contains curated quotes attributed to well-known leaders, entrepreneurs, and innovators. The competition focuses on a cleaned subset with authors having at least three quotes. Input features consist solely of the quote text; metadata (such as themes, sources, regions, decades, or genders) are excluded to avoid leakage. Text is minimally normalized (Unicode normalization, standardized apostrophes/quotes, and removal of outer quotation marks when they wrap the entire quote).

Files provided:
- train.csv: columns [id, quote, author]
- test.csv: columns [id, quote]
- sample_submission.csv: columns [id, author]

Participants may use any modeling approach; typical pipelines include text preprocessing, feature engineering (e.g., tokenization, embeddings), model training (e.g., linear classifiers, tree-based models over handcrafted features, transformer encoders), and evaluation.

Evaluation metric:
Macro-averaged F1 over the authors present in the test set. The F1 score for each author class is computed from true positives, false positives, and false negatives; the final score is an unweighted mean across classes. This metric is robust to class imbalance and rewards models that perform well across both frequent and rare authors.

Train/test split:
A deterministic stratified 80/20 split is used, ensuring every author has at least one example in both train and test. IDs are random-looking integers that carry no semantic meaning. The test set labels are hidden and should be predicted in submissions.

Submission format:
Submit a CSV file with exactly two columns [id, author] in that order. The id values must match those in test.csv, and the author labels must match one of the author names present in train.csv (case-sensitive exact match). Any deviation from the format will be rejected.

Notes:
- Keep quotes as text input only; do not use any metadata for modeling.
- You may apply your own preprocessing and modeling strategies, including transformer-based encoders.
- External data is allowed if it does not leak author identity (e.g., generic language models), but predictions must be based on the provided quote texts.
