# OpenMLE-fast task

Task ID: `medium-post-titles@1`

Native metric: `MediumPostTitleMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2511 bytes)
- `data/sample_submission.csv` (508730 bytes); columns: ["id", "label"]
- `data/test.csv` (3844601 bytes); columns: ["id", "text"]
- `data/train.csv` (16390454 bytes); columns: ["id", "text", "label"]

## Public description

Medium Post Titles: 93‑Class Topic Classification

Problem statement
Predict the topical category of a Medium post from short text. Each example is a post’s title optionally followed by its subtitle. Your task is to build a model that maps the text to one of 93 categories.

Files you will use
- train.csv — Training data with columns:
  - id: unique identifier for each post
  - text: the input text (title if no subtitle; otherwise title + " [SEP] " + subtitle)
  - label: the ground‑truth category (string)
- test_data.csv — Test data with columns:
  - id: unique identifier
  - text: the input text
- sample_submission.csv — Example submission with columns:
  - id
  - label: a valid category (string)

Task details
- Input: Short texts (title and, when present, subtitle), already concatenated into the text column using the separator token [SEP].
- Output: A single category label per test id.
- Number of classes: 93. Classes are imbalanced and include semantically close topics; robust modeling and thoughtful handling of class imbalance are important.

Data split and leakage control
- The data are split once into train/test (~80/20) using group‑aware splitting on identical post titles so that any repeated titles are entirely in either train or test (never both). This reduces leakage from duplicated titles with different subtitles.
- Each category present in test also appears in the training set at least once.

Evaluation
- Primary metric: Macro‑averaged F1 score across all categories present in the test set. Each class contributes equally regardless of frequency. Higher is better.
- Tie‑breaker: Micro‑averaged F1 score.

Submission format
- File must have two columns with headers: id,label
- Include exactly one row for every id in test_data.csv and no extra/missing ids.
- Labels must be strings (case‑sensitive) corresponding to valid categories.

Recommendations (non‑binding)
- Feature engineering: character/word n‑grams, subword features, or pretrained language models.
- Handling imbalance: class‑weighted losses, focal loss, calibration, threshold tuning.
- Preprocessing: whitespace normalization, casing choices, punctuation retention (often informative), optional language‑specific tokenization.
- Validation: You may perform your own internal cross‑validation on train.csv; the official score uses the provided test split.

Reproducibility
- The provided split is deterministic. Do not rely on any information outside text and id when training.
