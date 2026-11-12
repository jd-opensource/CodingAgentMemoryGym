# OpenMLE-fast task

Task ID: `bigpicture-company-dataset@2`

Native metric: `CompanyTypeClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3697 bytes)
- `data/sample_submission.csv` (89134 bytes); columns: ["id", "type"]
- `data/test.csv` (294966 bytes); columns: ["id", "name", "website", "industry", "size", "founded", "city", "state", "country_code"]
- `data/train.csv` (1303371 bytes); columns: ["id", "name", "website", "industry", "size", "founded", "city", "state", "country_code", "type"]

## Public description

Competition: Company Type Inference from Firmographics and Web Signals

Problem statement
Participants must predict a company’s organizational type (e.g., Privately Held, Public Company, Nonprofit, Government Agency, Educational, Partnership, Self-Owned, etc.) from firmographic and textual signals. The challenge spans multiple languages and countries with missing and noisy data.

Data description
You are provided with large-scale tabular data derived from public company profiles. Each row represents a company. The final files include:
- train.csv: Training examples with input features and a target column.
- test.csv: Test examples with the same features but without the target.
- sample_submission.csv: A template submission with randomized valid labels.

Columns
- id: An opaque, deterministic identifier for the row. Use this to align predictions with test rows.
- name: Company name (string; multilingual, may be noisy).
- website: Company website (string; may be missing, may include domains and TLDs).
- industry: Industry category (string; high cardinality; may be missing).
- size: Company size bucket (string; examples: 1-10, 11-50, 51-200, 201-500, 1K-5K, etc.).
- founded: Year founded (integer-like string; may be missing).
- city, state, country_code: Geographic fields (strings; may be missing).
- type (train.csv only): Organizational type (target label; string).

Target
- type is a multi-class categorical label with a long-tail distribution across many categories. All categories present in test also appear at least once in train.

Expected approaches
- Data processing: Normalize and tokenize text; derive domain/TLD from website; robustly handle Unicode and punctuation.
- Feature engineering: Legal-entity cues (e.g., inc, ltd, llc, gmbh, s.a., s.r.l., bv, oy, as, sas, gk, kk, a.s., plc, nv, ab, sp. z o.o., sdn bhd, foundation); age from founded; encodings for high-cardinality categoricals (industry, geography, TLD).
- Modeling: Strong baselines include gradient-boosted trees (CatBoost/LightGBM/XGBoost) on engineered features, as well as character/word models or multilingual embeddings for name and domain text.

Evaluation
- Submissions must be a CSV with columns: id,type
- Metric: Macro-averaged F1 score across all distinct labels present in the hidden ground truth.
  - For each label c: F1_c = 2 * (precision_c * recall_c) / (precision_c + recall_c), with safe handling when denominators are zero.
  - Macro F1 = mean over labels.
  - Comparisons are case-insensitive after trimming whitespace. Invalid or unseen labels are treated as mismatches.

File specifications
- train.csv: id,name,website,industry,size,founded,city,state,country_code,type
- test.csv: id,name,website,industry,size,founded,city,state,country_code
- sample_submission.csv: id,type

Notes and constraints
- Deterministic split: An 80/20 split is created using a stable hash of each company’s identifier to avoid data leakage and ensure reproducibility.
- Missing values: Appear as empty strings. Handle them appropriately.
- High-cardinality fields: Expect many unique industries, names, and geographies. Efficient encoders or text models are recommended.
- Scale: The training and test files are large. Efficient, streaming data pipelines are encouraged. Runtime is not restricted.

Submission
- Upload a CSV named submission.csv (or any name) with columns id,type covering all rows in test.csv. No extra columns. The id values must match test.csv exactly.

Scoring details
- Submissions failing format validation (missing ids, duplicates, extra/missing columns) will not score.
- F1 is computed in a single pass with careful handling of numerical edge cases (NaN/inf guarded).
