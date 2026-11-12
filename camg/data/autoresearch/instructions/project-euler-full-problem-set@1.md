# OpenMLE-fast task

Task ID: `project-euler-full-problem-set@1`

Native metric: `ProjectEulerDifficultyMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2839 bytes)
- `data/sample_submission.csv` (1659 bytes); columns: ["id", "difficulty"]
- `data/test.csv` (294478 bytes); columns: ["id", "title", "subtitle", "content", "html_content", "release_date"]
- `data/train.csv` (1238814 bytes); columns: ["id", "title", "subtitle", "content", "html_content", "release_date", "difficulty"]

## Public description

Competition: Predict Project Euler Problem Difficulty from Text

Problem statement:
Given the natural-language and mathematical description of a Project Euler problem, predict its official difficulty score. Each problem’s difficulty is on a 5-point grid between 5 and 100. Your goal is to build a model that maps the problem text (and optional context) to a numeric difficulty.

Data description:
- train.csv: id, title, subtitle, content, html_content, release_date, difficulty
  - difficulty is the numeric target (5–100 on a 5-point grid).
- test.csv: id, title, subtitle, content, html_content, release_date
  - No target column.
- sample_submission.csv: id, difficulty
  - Provide one numeric prediction per test id. Continuous values are allowed; they will be clipped to the valid range during evaluation.

Notes on the fields:
- title, subtitle, content: plain text describing the problem.
- html_content: HTML with embedded math (e.g., LaTeX). You may choose to use content, html_content, or both.
- release_date: ISO timestamp; you may derive features like year, month, or decade.
- id is a unique key and should be used only to align rows, not as a predictive feature.

What is expected:
- Data processing: Clean text while preserving mathematical tokens and numeric magnitudes. Normalize whitespace and Unicode; unescape HTML entities if helpful.
- Feature engineering: Consider character/word n-grams, TF-IDF, pretrained language-model embeddings, math-aware tokenization, and simple counts (e.g., equation markers, presence of sums/products, numeric ranges).
- Model training: Fit a regression or ordinal-regression model that outputs a numeric difficulty.
- Model evaluation: Validate carefully and avoid leakage. Do not use engagement-derived signals (e.g., solved-by counts); rely on the problem text and optional release_date.

Evaluation metric:
- Mean Absolute Error (MAE) on the numeric difficulty values.
- Before scoring, predictions are clipped to [5, 100]. MAE is then computed as the mean absolute difference between predictions and ground truth.

Submission format:
- CSV with columns: id,difficulty
- Include exactly one row per id in the test set.
- Predictions must be numeric and finite; order does not matter.

Split details:
- A single train/test split is provided. The test set covers a broad range of difficulties, and every difficulty value present in the test set appears at least once in the training set.

Tips for success:
- Preserve important math tokens and numerals; avoid overly aggressive stop-word removal.
- Combine content and html_content judiciously; stripping HTML while retaining LaTeX can work, or embeddings from raw html_content can be effective.
- Consider regularization and robust baselines (e.g., TF-IDF + linear) alongside pretrained transformers with adapters or finetuning.
