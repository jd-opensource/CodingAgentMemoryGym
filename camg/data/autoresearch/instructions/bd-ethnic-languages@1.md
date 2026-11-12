# OpenMLE-fast task

Task ID: `bd-ethnic-languages@1`

Native metric: `BangladeshEthnicLanguageMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2576 bytes)
- `data/sample_submission.csv` (11328 bytes); columns: ["id", "language"]
- `data/test.csv` (65229 bytes); columns: ["id", "text"]
- `data/train.csv` (294162 bytes); columns: ["id", "text", "language"]

## Public description

Bangladesh Ethnic Language Identification (6-class)

Overview
You are given short to medium text snippets in several ethnic languages of Bangladesh. Your task is to build a model that predicts which language each snippet belongs to. The languages share visually similar scripts in many cases, and snippets can be very short—making the task challenging and rewarding robust Unicode-aware modeling.

Labels (exactly these 6):
- Chakma
- Marma
- Rakhine
- Santali
- Garo
- Tripura

Files provided
- train.csv: training set with columns [id, text, language]
- test.csv: test set with columns [id, text]
- sample_submission.csv: example submission with columns [id, language]

Task
Train a text classification model on train.csv and predict the language for each row in test.csv. Submit a CSV with columns [id, language] and a header row. The language value must be one of the six labels above.

Data details
- All rows of the source have been used; nothing is discarded.
- Text and labels are Unicode-normalized (NFC) and stripped of surrounding whitespace.
- Some exact texts appear multiple times in the dataset. The split ensures such duplicates are not split across train and test (grouped by exact text).
- The dataset is imbalanced; Tripura is comparatively low-resource.

Train/test split
- Deterministic 80/20 split
- Grouped by exact text so duplicates remain entirely in either train or test
- Stratified by language and further co-stratified by text-length buckets to reflect both class imbalance and the short/long text mix

Submission format
- CSV with exactly these two columns and a header: id, language
- Each id must appear exactly once
- language must be one of: Chakma, Marma, Rakhine, Santali, Garo, Tripura

Evaluation
- Metric: macro-averaged F1 across the six classes
- Definition: compute per-class F1 = 2 × (precision × recall) / (precision + recall), treating each class as positive vs. the rest; average the six per-class F1 scores
- Why macro-F1: it treats all classes equally and is robust to class imbalance and prevalence shifts

Modeling guidance (optional, non-exhaustive)
- Character/byte-level neural models (CNN/RNN/Transformers)
- Subword tokenization (e.g., SentencePiece/BPE) for compact vocabularies
- Unicode-aware features (e.g., script/block proportions, punctuation/diacritic patterns)
- Handle invisible characters safely; do not collapse characters that distinguish scripts (e.g., different sentence terminators)

Good luck, and have fun building robust multilingual text classifiers that help represent under-resourced languages!
