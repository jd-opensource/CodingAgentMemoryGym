# OpenMLE-fast task

Task ID: `arxivorg-ai-research-papers-dataset@2`

Native metric: `ArxivAIPaperClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3292 bytes)
- `data/sample_submission.csv` (60092 bytes); columns: ["paper_id", "label"]
- `data/test.csv` (2528632 bytes); columns: ["paper_id", "title", "summary", "comment", "authors", "primary_category", "categories", "published_year"]
- `data/train.csv` (10172333 bytes); columns: ["paper_id", "title", "summary", "comment", "authors", "primary_category", "categories", "published_year", "label"]

## Public description

Title: Predicting Journal Publication from arXiv Metadata

Problem statement:
Given an AI paper’s information available at submission time on arXiv (title, abstract, authors, categories, comment, and published year), predict the probability that the paper will eventually have a non-empty journal reference (journal_ref). This is a binary classification task; the target is 1 if a journal reference exists, 0 otherwise.

Why this matters:
Many arXiv preprints later appear in peer-reviewed journals. Anticipating which papers are likely to get published can help researchers, institutions, and recommendation systems prioritize attention and resources. The problem is challenging due to temporal drift across decades, class imbalance, and the need to combine free text with metadata.

Files provided:
- train.csv — Training set with features and the target column.
- test.csv — Test set with the same features as train.csv, without the target.
- sample_submission.csv — A format example for predictions.

Data description (columns in train/test):
- paper_id: Unique identifier of each paper for the competition.
- title: Paper title.
- summary: Paper abstract.
- comment: Free-text comments provided by the authors at submission (may be empty).
- authors: Raw author string (you may also derive features such as author count).
- primary_category: The arXiv primary category (e.g., cs.AI).
- categories: All categories/tags associated with the paper (string list).
- published_year: The year the paper was published on arXiv.
- label (train.csv only): Binary target indicating whether journal_ref is present (1) or not (0).

Important notes:
- All features are available at submission time; no post-submission fields are included in train/test.
- Identifiers and links that do not carry semantic content are excluded from the features.
- You are encouraged to leverage both text (title, abstract, comment) and metadata (authors, categories, year) to build your model.

Evaluation metric:
- Primary: ROC-AUC computed on the probability predictions for the positive class (label = 1). Ties are handled properly; probabilities must be within [0, 1].
- Secondary (informational only for local validation): Average Precision (PR-AUC). Only ROC-AUC is used for leaderboard scoring.

Submission format:
- CSV with the following columns and order:
  - paper_id: Must match the IDs in test.csv exactly (no missing/extra/duplicate IDs).
  - label: A probability between 0 and 1 representing the predicted likelihood of having a journal reference.

Data split details:
- A single deterministic train/test split preserves the year distribution and class ratio via decade-based bins, mitigating temporal drift. No validation split is provided; consider time-aware validation locally.

Recommended modeling directions:
- Text modeling on title + summary + comment (bag-of-words, TF-IDF, n-grams, or transformer encoders).
- Metadata features such as author count, presence of certain keywords in comments (e.g., "to appear"), category encodings, and temporal features.
- Handle class imbalance via class weights, resampling, or calibrated thresholds.
- Carefully validate under temporal drift; consider time-aware validation splits.

Final data files:
- train.csv
- test.csv
- sample_submission.csv
