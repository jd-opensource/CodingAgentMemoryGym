# OpenMLE-fast task

Task ID: `financial-sentiment-analysis@2`

Native metric: `FinancialSentimentClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2135 bytes)
- `data/sample_submission.csv` (21405 bytes); columns: ["id", "Sentiment"]
- `data/test.csv` (190041 bytes); columns: ["id", "Sentence", "domain"]
- `data/train.csv` (606233 bytes); columns: ["id", "Sentence", "domain", "Sentiment"]

## Public description

Financial Domain-Robust Sentiment Classification

Overview
Build a 3-class sentiment classifier for financial text that is robust across two language styles: formal news-like sentences and microtext-style posts (ticker/URL-heavy). Models should generalize well across both domains.

Data
You are given fully labeled training data and unlabeled test data. Each row is a single sentence.

Files provided
- train.csv: columns [id, Sentence, domain, Sentiment]
  - domain: "micro" if the sentence contains a $TICKER (e.g., $AAPL) or a URL; otherwise "news"
  - Sentiment: one of {negative, neutral, positive}
- test.csv: columns [id, Sentence, domain]
- sample_submission.csv: columns [id, Sentiment]

Task
Predict the Sentiment for every id in test.csv. You may use the domain column as an auxiliary feature, but the task is standard text classification.

Important notes
- The split prevents exact duplicate sentences from crossing train/test to reduce leakage.
- All three sentiment labels appear in both training and test sets.
- Finance-relevant tokens and symbols are kept as-is (e.g., $TICKER, %, +, -). URLs may appear in text.

Evaluation
- Metric: Macro-averaged F1 across the three sentiment classes {negative, neutral, positive}.
- Submission format: CSV with header id,Sentiment
  - id must match those in test.csv (one row per id)
  - Sentiment values must be one of {negative, neutral, positive}
- Leaderboard is sorted by Macro F1 (higher is better).

Recommendations (non-exhaustive)
- Preprocessing: consider lowercasing; normalize unicode quotes/spaces; preserve finance markers like $TICKER and numerals; optionally replace full URLs with a [URL] token while keeping the signal.
- Modeling: linear models on n-grams, neural encoders, or transformers. Consider domain-aware strategies (sample reweighting, adversarial training) to improve robustness across "micro" and "news".
- Class imbalance: use class weights, focal loss, or resampling.

Sanity checks
- Ensure your submission has exactly the test ids and valid labels.
- Validate Macro F1 locally using metric.py (with your own validation) to avoid format errors.
