# OpenMLE-fast task

Task ID: `az-medicine-dataset-of-india@1`

Native metric: `MedicinePriceRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3360 bytes)
- `data/sample_submission.csv` (1212892 bytes); columns: ["row_id", "price"]
- `data/test.csv` (5607088 bytes); columns: ["row_id", "name", "manufacturer_name", "pack_size_label", "short_composition1", "short_composition2", "is_discontinued"]
- `data/train.csv` (23673057 bytes); columns: ["row_id", "name", "manufacturer_name", "pack_size_label", "short_composition1", "short_composition2", "is_discontinued", "price"]

## Public description

Competition: Medicine Price Prediction (RMSLE)

Background
Indian allopathy medicines vary widely across pack forms (tablet, syrup, injection, topical), ingredient strengths, manufacturers, and pack sizes, leading to a heavy‑tailed price distribution. Estimating price from product descriptors is a realistic and challenging ML task with strong practical relevance for pricing analytics and inventory planning.

Problem statement
Given textual and categorical descriptors of a medicine SKU, predict its retail price (₹). You should build models that generalize across forms and brands and are robust to extreme outliers and heavy‑tailed targets.

Data description
Final competition files:
- train.csv: Training set including features and the target column.
- test.csv: Test set with the same features but no target.
- sample_submission.csv: Example submission format.

Columns in train.csv and test.csv
- row_id: Unique identifier for each row in the provided files. Use this only for submission indexing; it is not a predictive feature.
- name: Product name (text). Contains brand and dosage signals.
- manufacturer_name: Manufacturer (categorical; many levels).
- pack_size_label: Pack/form description (text). Examples: "strip of 10 tablets", "bottle of 100 ml Syrup".
- short_composition1: Primary composition string (text). Contains ingredient names and strengths.
- short_composition2: Secondary composition string (text). Often empty; treat as missing.
- is_discontinued: Availability snapshot as of Nov 2022 (boolean-like string). Optional feature; use with caution.
- price: Target column present only in train.csv. Numeric, non‑negative.

Target
- price: Retail price (₹) of the SKU.

Suggested feature engineering (not exhaustive)
- Text normalization and tokenization of name and composition fields.
- Pack size parsing to extract counts, volumes, and units (tablet/capsule/syrup/injection/topical/etc.).
- Ingredient parsing to derive strengths per unit where possible.
- Categorical encoding for manufacturer_name.

Evaluation metric
- Root Mean Squared Logarithmic Error (RMSLE):
  RMSLE = sqrt(mean((log1p(actual) − log1p(predicted))^2))
- Rationale: RMSLE is robust to heavy‑tailed price distributions, penalizes multiplicative errors, and handles zeros gracefully.
- Predictions must be non‑negative. Any negative values will be treated as zero during evaluation.

Submission format
- A CSV file with exactly two columns and a header:
  row_id,price
- Include every row_id from test.csv exactly once and in any order. Values must be numeric and non‑negative.

Train/test split policy
- Rows are split by product key (name | manufacturer_name | pack_size_label) to prevent identical SKUs appearing in both train and test. Duplicates of the same SKU remain within the same split to avoid leakage.
- Approximate split ratio: 80% train, 20% test.

Final files delivered
- train.csv: Features plus target price.
- test.csv: Features only.
- sample_submission.csv: Random but valid numeric prices aligned to the test row_id.

Notes
- The data is non‑temporal and contains a diverse set of manufacturers and pack forms.
- Handle missing values (especially short_composition2) gracefully in your pipelines.
- Avoid relying on trivial heuristics; robust text processing and feature engineering will materially improve performance.
