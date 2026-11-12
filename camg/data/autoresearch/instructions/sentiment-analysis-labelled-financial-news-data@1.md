# OpenMLE-fast task

Task ID: `sentiment-analysis-labelled-financial-news-data@1`

Native metric: `FinancialSentimentMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3463 bytes)
- `data/sample_submission.csv` (1344 bytes); columns: ["id", "label"]
- `data/test.csv` (224162 bytes); columns: ["id", "Headline", "Synopsis", "Full_text", "Date_published"]
- `data/train.csv` (766400 bytes); columns: ["id", "Headline", "Synopsis", "Full_text", "Date_published", "Final Status"]

## Public description

Financial News Document Sentiment Challenge

Problem statement
You are given financial news articles from the Economic Times (India). Each record contains a Headline, a Synopsis, and the Full_text of the article, along with the publication date. Your task is to predict the overall sentiment of each article as Positive or Negative.

Participants are encouraged to build models that can handle both very short text (headlines) and long, noisy, real-world documents (full articles), and to design features or architectures that generalize over time.

Files provided
- train.csv: Training data with the following columns
  - id: Unique row identifier
  - Headline: Article headline
  - Synopsis: Short summary (may be empty for a few rows)
  - Full_text: Full article text (can be long; preserve numbers and currency symbols)
  - Date_published: Publication date (ISO format)
  - Final Status: Target label, one of {Positive, Negative}
- test.csv: Test data with the same columns as train.csv except that Final Status is not included.
- sample_submission.csv: A sample submission file with two columns: id and label.

Data split and leakage control
- The host split is chronological: training rows come from earlier dates and test rows from later dates.
- To prevent leakage from duplicate or near-identical headlines, exact-duplicate headlines are grouped and kept entirely on one side of the split. The assignment of each headline group is determined by the group’s latest publication date; groups whose latest date falls in the earlier portion go to the training set, and the rest go to the test set.
- The split ensures that every label appearing in the test set also appears at least once in the training set.

Evaluation
- Primary metric: Macro F1 over the two classes {Positive, Negative}.
  - For each class c in {Positive, Negative}, compute precision and recall treating c as the positive class, then F1_c = 2 * precision_c * recall_c / (precision_c + recall_c) with 0 if the denominator is 0. Macro F1 is the simple average (F1_Positive + F1_Negative) / 2.
- Tie-breaker: Accuracy (only used to break exact ties in Macro F1).

Submission format
- Submit a CSV file with exactly two columns in this order:
  - id: The id from test.csv
  - label: Your predicted sentiment for the corresponding id, one of Positive or Negative (case-sensitive)
- The submission must contain exactly one row per id in test.csv, no duplicates, and no extra ids.

Modeling guidance (non-binding)
- Use all three text fields. A strong baseline is to concatenate them as Headline\n\nSynopsis\n\nFull_text, then encode with an NLP model (e.g., transformer). Long-context strategies (hierarchical encoders, chunking with pooling, or LLMs with extended context) are helpful because Full_text can be long.
- Normalize Unicode and punctuation consistently (e.g., currency symbol variants), but avoid removing numbers and entities as they can carry sentiment in finance.
- You may derive temporal features from Date_published if desired, but the primary challenge is to generalize forward in time on textual content.

Goal and difficulty
- Goal: Build robust document-level sentiment models that generalize to later periods.
- Difficulty: Medium–High due to long-document handling, finance-specific language, slight class imbalance, and a time-based split that limits shortcut learning.

Final artifacts
- train.csv
- test.csv
- sample_submission.csv

Good luck and happy modeling!
