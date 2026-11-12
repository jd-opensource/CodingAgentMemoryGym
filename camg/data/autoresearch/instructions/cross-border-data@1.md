# OpenMLE-fast task

Task ID: `cross-border-data@1`

Native metric: `CrossBorderLinkPredictionMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2820 bytes)
- `data/sample_submission.csv` (1554162 bytes); columns: ["row_id", "link_probability"]
- `data/test.csv` (5355942 bytes); columns: ["year", "impid", "expid", "ln_service_export", "ln", "ln_importer_service_exports", "ln_importer_s_goods_export", "lngdp", "ln_importer_gdp", "foreign_direct_investment", "ln_importer_s_foreign_direct_investment", "dum", "ippsub", "ippsum_method", "ippsum", "institutional_distance", "row_id"]
- `data/train.csv` (24401328 bytes); columns: ["year", "impid", "expid", "ln_service_export", "ln", "ln_importer_service_exports", "ln_importer_s_goods_export", "lngdp", "ln_importer_gdp", "foreign_direct_investment", "ln_importer_s_foreign_direct_investment", "dum", "ippsub", "ippsum_method", "ippsum", "institutional_distance", "link"]

## Public description

Cross-Border IP Trade Link Prediction

Problem statement
Anticipate whether a cross‑border intellectual property (IP) trade link will occur between an exporter and an importer in a given year. For each (year, exporter, importer) triplet in test.csv, predict the probability that a positive IP trade flow exists.

Provided files
- train.csv: Training set with identifiers and features plus the target column link ∈ {0,1}.
- test.csv: Test set with the same feature columns as train.csv except link, plus a unique row_id for each row.
- sample_submission.csv: Example submission with columns [row_id, link_probability].

Target
- link: Binary label. 1 indicates a positive cross‑border IP trade link for that dyad-year, 0 otherwise.

Data description
- Identifiers: year (int), impid (int, importer ID), expid (int, exporter ID).
- Covariates: Numeric macro/trade/institutional variables describing the exporter, importer, and dyad (e.g., service exports, goods exports, GDP, FDI, policy indices, institutional distance). Column names are standardized to safe snake‑case (spaces removed, special characters normalized) and numeric values use dot decimals with appropriate casting.
- All remaining columns in train.csv, apart from link, are features and also appear in test.csv.

Split
- Temporal generalization is required. Training rows come from earlier years; test rows come from later years. This creates a realistic distribution shift across time and evaluates forward‑looking performance. The split is deterministic and uses the full dataset; no downsampling or subsampling is applied.

Submission format
- Submit a single CSV file with exactly two columns (in this order):
  1) row_id: Provided in test.csv and unique per row.
  2) link_probability: Your predicted probability in [0,1] that link = 1.
- Every row_id in test.csv must appear exactly once in your submission.

Evaluation
- Primary metric: Average Precision (AP), computed as the area under the precision–recall curve obtained by ranking samples by link_probability (descending). AP is robust for imbalanced classification and directly rewards accurate ranking of the rare positive links. Higher is better.
- Numerical safety: link_probability values must be finite and within [0,1]. Invalid formats will be rejected.

Guidance and considerations
- Expect severe class imbalance (many zeros). Consider class weights, calibrated probabilities, focal loss, or threshold tuning.
- Time‑aware validation is recommended (e.g., train on earlier years, validate on a later year) to mirror the leaderboard split.
- Potential features include dyadic interactions, exporter/importer fixed effects, and transformations capturing pair‑specific heterogeneity.
- Do not rely on external information that directly reveals outcomes in the test period.
