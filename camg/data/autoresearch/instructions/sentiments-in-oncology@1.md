# OpenMLE-fast task

Task ID: `sentiments-in-oncology@1`

Native metric: `OncologySentimentMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2860 bytes)
- `data/sample_submission.csv` (7919 bytes); columns: ["id", "label"]
- `data/test.csv` (889890 bytes); columns: ["id", "comment", "tokens", "stopword_tokens", "lemma_tokens"]
- `data/train.csv` (3199146 bytes); columns: ["id", "comment", "tokens", "stopword_tokens", "lemma_tokens", "label"]

## Public description

Title: Multilingual Oncology Treatment-Family Classification (Redacted Drug Names)

Problem statement
- Task: Given a real-world, multilingual patient comment with explicit drug names redacted, classify which oncology treatment family it describes.
- Classes: FOLFOX (incl. FOLFOXIRI), AROMASIN_EXEMESTANE, AFINITOR_EVEROLIMUS.
- Goal: Build robust NLP models that rely on clinical context, side-effects, dosing/regimen patterns, and co-therapy cues — not simple keyword spotting.

Data description
- Train file: train.csv
  - Columns:
    - id: unique integer identifier for each row.
    - comment: patient comment text with drug-family names replaced by the placeholder [DRUG].
    - tokens: tokenized representation as a stringified list; drug tokens redacted to [DRUG].
    - stopword_tokens: stopword-removed token list (stringified); redaction applied.
    - lemma_tokens: lemmatized token list (stringified); redaction applied.
    - label: target class in {FOLFOX, AROMASIN_EXEMESTANE, AFINITOR_EVEROLIMUS}.
- Test file: test.csv (same columns as train.csv except label is withheld).
- Provided sample: sample_submission.csv (contains random valid labels; replace with your predictions).

Scope and preprocessing
- Source comments span English, French, and German, containing domain jargon, abbreviations (e.g., folfoxiri), misspellings (e.g., affinitor), and code-switching.
- Redaction: All explicit mentions of the target drug families and common variants are replaced by [DRUG] across comment, tokens, stopword_tokens, and lemma_tokens.
- Split: Single stratified train/test split is provided; competitors should manage their own validation strategy.

Evaluation
- Metric: Macro F1 across the three classes.
  - Rationale: Macro F1 treats classes equally and is robust to class imbalance by averaging per-class F1 scores.
- Submission format: CSV with two columns: id, label.
  - id must exactly match the integer ids in test.csv.
  - label must be one of {FOLFOX, AROMASIN_EXEMESTANE, AFINITOR_EVEROLIMUS}.

Suggested approach
- Data processing: Normalize Unicode/casing as needed; consider de-noising punctuation and leveraging multilingual text processing.
- Feature engineering: Combine character/word n-grams, multilingual embeddings, and domain lexicons capturing side-effects, regimen schedules, and co-therapies. The provided tokens and lemmas can serve as auxiliary inputs.
- Modeling: Strong baselines include linear models with TF-IDF and multilingual transformers (e.g., XLM-R). Address class imbalance with class weights or loss adjustments.
- Evaluation: Align internal validation to macro F1 for consistency with the leaderboard.

Files for participants
- train.csv
- test.csv
- sample_submission.csv

Build context-aware, multilingual models that can distinguish treatment families without relying on explicit drug-name mentions.
