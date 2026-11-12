# OpenMLE-fast task

Task ID: `el-ateneo-marketplace-books@1`

Native metric: `ElAteneoBookPriceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2957 bytes)
- `data/sample_submission.csv` (38107 bytes); columns: ["id", "precio"]
- `data/test.csv` (448777 bytes); columns: ["titulo", "autor", "editorial", "idioma", "nro_paginas", "fecha_publicacion", "encuadernacion", "categoria", "genero", "subgenero", "id"]
- `data/train.csv` (1878074 bytes); columns: ["titulo", "autor", "editorial", "idioma", "nro_paginas", "fecha_publicacion", "encuadernacion", "categoria", "genero", "subgenero", "id", "precio"]

## Public description

El Ateneo Book Price Prediction (ARS)

Problem statement:
Predict the list price (in Argentine pesos, ARS) of books sold by El Ateneo’s online marketplace using product-page metadata. Build models that generalize price formation across publishers, categories, bindings, and publication dates using tabular and textual features.

Files provided:
- train.csv: Training data with feature columns and the target column precio. Includes a synthetic id column to identify rows.
- test.csv: Test data with the same feature columns as train.csv (excluding precio) and the id column.
- sample_submission.csv: A submission template with id and precio columns.

Target and features:
- Target: precio (integer ARS). Prices are strictly positive and heavy‑tailed.
- Core features: titulo, autor, editorial, idioma, nro_paginas, fecha_publicacion (MM/YYYY), encuadernacion, categoria, genero, subgenero, and id.
  - Note: id is a synthetic identifier for submission alignment and carries no price information.
  - Identifiers such as product URL and ISBN are intentionally excluded to prevent shortcut learning.

Train/test split:
- A single organizer split is provided, approximately 80/20, stratified by (categoria, encuadernacion) to preserve distribution across segments. Each product appears in exactly one split; IDs are contiguous and unique across train+test.

Recommended data processing (non‑exhaustive):
- Parse fecha_publicacion to derive numeric signals (year, month, age in months at scrape date, decade bucket).
- Normalize text features (e.g., titulo, autor, editorial): lowercase, strip accents, trim whitespace, collapse repeated spaces; consider light TF‑IDF or character n‑grams on titulo.
- Handle high‑cardinality categoricals (autor, editorial, possibly titulo) via models that natively support them (e.g., CatBoost) or encodings (e.g., target/likelihood encoding with regularization, learned embeddings).
- Impute missing values (e.g., nro_paginas has some missing), and consider missing indicators.
- Consider training on a log‑transformed target while producing predictions in ARS for evaluation.

Evaluation metric:
- Root Mean Squared Logarithmic Error (RMSLE) computed on precio using log(1 + x):
  - RMSLE = sqrt(mean((log1p(y_pred) − log1p(y_true))^2)).
  - Predictions must be non‑negative; any negative or non‑finite predictions will be clipped to zero for scoring.
  - RMSLE treats multiplicative errors more uniformly across the price range and is robust to heavy tails.

Submission format:
- CSV with columns: id, precio.
- Each id from test.csv must appear exactly once; no extra or missing rows are allowed.
- precio should be numeric (float or integer) and finite.

Notes:
- Use the full scale of the data; strong solutions will combine robust tabular ML with thoughtful feature engineering on categorical and textual signals.
- The dataset consists of unique products; there are no exact duplicates to exploit.
