# OpenMLE-fast task

Task ID: `datahackers-subset-2025@1`

Native metric: `JobChangeIntentMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2465 bytes)
- `data/sample_submission.csv` (63993 bytes); columns: ["prediction"]
- `data/test.csv` (278458 bytes); columns: ["f1", "f2", "f3", "f4", "f5", "f6"]
- `data/train.csv` (1391420 bytes); columns: ["f1", "f2", "f3", "f4", "f5", "f6", "label"]

## Public description

Title: Job-Change Intent Prediction (Brazil Data Professionals Survey)

Problem statement
Predict a respondent’s 6‑month job-change intent from their survey answers. The goal is multiclass classification over four intent categories. Participants must build an ML pipeline for text-rich, multi-select survey data in Portuguese.

Data description
Final files provided:
- train.csv: Features plus the target label column.
- test.csv: Features only (no labels).
- sample_submission.csv: A sample file showing the required submission format.

Columns
- f1–f6: Text features derived from survey questions, covering perceptions of career impact, job selection criteria, company layoff status, company priorities around generative AI, types of AI usage within the company, and individual usage of tools like ChatGPT/Copilot.
- label (train only): The target class representing job-change intent in the next 6 months.

Target classes (exact strings)
- Não estou buscando, mas me considero aberto a outras oportunidades
- Não estou buscando e não pretendo mudar de emprego nos próximos 6 meses
- Estou em busca de oportunidades dentro ou fora do Brasil
- Estou em busca de oportunidades, mas apenas fora do Brasil

Submission format
- CSV file with a single header column named "prediction".
- Exactly one prediction per row of test.csv, in the same order.
- Each value must be exactly one of the target class strings listed above.

Evaluation
- Macro-averaged F1 score across the 4 classes.
- Definition: Compute F1 per class from precision and recall for that class, then take the unweighted mean over classes. This equally rewards performance on minority classes and is robust to class imbalance.

Guidance
- Data processing: Keep UTF-8, semicolon source parsing handled for you. Strings may contain commas due to multi-select answers; treat features as raw text or parse multi-select options.
- Feature engineering: Consider bag-of-words/char n-grams, Portuguese tokenization/stopwords, multi-select expansion, binary flags, and missingness indicators.
- Modeling: Linear classifiers with TF-IDF are strong baselines; multilingual transformers (e.g., XLM-R, mBERT) can improve performance.
- Fairness and robustness: Use macro F1, validate edge cases and missing values. Avoid label leakage; test.csv contains no labels.

Notes
- No validation split is provided; participants may use cross-validation within train.csv.
- All target classes appear in train.csv.
