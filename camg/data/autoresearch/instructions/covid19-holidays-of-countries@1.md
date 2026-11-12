# OpenMLE-fast task

Task ID: `covid19-holidays-of-countries@1`

Native metric: `CountryHolidayClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2975 bytes)
- `data/sample_submission.csv` (8758 bytes); columns: ["id", "code"]
- `data/test.csv` (45837 bytes); columns: ["id", "holiday", "ds_holidays", "ds"]
- `data/train.csv` (98739 bytes); columns: ["id", "holiday", "ds_holidays", "ds", "code"]

## Public description

Title: Holiday-to-Country Multilingual Classification (COVID-19 calendar)

Problem statement
- You are given public holiday records consisting of a multilingual holiday name and its calendar date (ds_holidays) plus a systematically shifted date (ds) used in COVID-19 impact modeling. Each record belongs to one of 70 countries (target label is the ISO alpha‑2 code).
- Task: Predict the country code for each holiday record in the test set.
- Goal: Build models that jointly leverage text and calendar signals to correctly identify the country of origin, and generalize from 2020–2021 to 2022.

Files
- train.csv: id, holiday, ds_holidays, ds, code
- test.csv: id, holiday, ds_holidays, ds
- sample_submission.csv: id, code

Data description
- holiday: holiday name string in native languages (may include multiple languages and diacritics).
- ds_holidays: original holiday date (YYYY-MM-DD).
- ds: a 7-day shifted date aligned to COVID-19 symptom reporting windows. It is provided as an additional temporal cue; it is redundant to ds_holidays but may be helpful for feature design.
- code: ISO alpha-2 country code (label). There are 70 classes.

Split protocol
- Records are deduplicated across multiple source versions by (code, holiday, ds_holidays) to retain unique holiday instances.
- Train set: all records with ds_holidays in 2020–2021.
- Test set: all records with ds_holidays in 2022.
- Each row has a unique integer id. Test ids align 1:1 with sample_submission.csv.

Evaluation
- Primary metric: Macro F1 across all country codes.
  - Rationale: Class sizes vary and several holiday names are shared across countries/languages. Macro F1 balances performance across all classes and penalizes models that focus on only frequent countries.
- Submission format: CSV with columns [id, code] in this exact order. All test ids must be present exactly once.

Suggestions for modeling
- Text features: character/word n‑grams; multilingual tokenizers; subword or transformer-based embeddings. Preserve accents—orthography carries strong signals.
- Time features from ds_holidays (and optionally ds): month, day, day‑of‑week, week number, day‑of‑year, is_weekend, month‑week index. Combining text and temporal features is often essential (e.g., Independence/Republic/Constitution days on country‑specific dates).
- Baselines: linear models on n‑grams + calendar features; tree‑based models on engineered features; multilingual transformers fine‑tuned on holiday text plus calendar encodings.

Rules and notes
- The training data includes labels; the test data does not. No external data is required, but you may use generic pretrained NLP models per typical Kaggle rules if desired.
- The dataset contains only tabular files for this competition. There are no image/audio assets to split.
- No file paths are included in the CSVs. Ids are synthetic and deterministic.

Good luck and have fun building multilingual, calendar‑aware classifiers!
