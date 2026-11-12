# OpenMLE-fast task

Task ID: `coffee-dataset@1`

Native metric: `CoffeeExportRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3386 bytes)
- `data/sample_submission.csv` (3537 bytes); columns: ["row_id", "Export"]
- `data/test.csv` (35858 bytes); columns: ["row_id", "Country", "Year", "Export_prev1", "Export_prev2", "Export_prev3", "Production_prev1", "Production_prev2", "Production_prev3", "DomesticConsumption_prev1", "DomesticConsumption_prev2", "Import_prev1", "Import_prev2", "ReExport_prev1", "ReExport_prev2", "Inventory_prev1", "Inventory_prev2", "ImportersConsumption_prev1", "ImportersConsumption_prev2", "CoffeeType", "export_yoy_prev1", "production_yoy_prev1", "export_roll3_mean_prev", "production_roll3_mean_prev", "import_minus_reexport_prev1", "production_minus_domestic_prev1", "export_to_production_prev1", "export_over_net_import_prev1", "inventory_over_domestic_prev1", "Export_prev1_missing", "Production_prev1_missing", "DomesticConsumption_prev1_missing", "Import_prev1_missing", "ReExport_prev1_missing", "Inventory_prev1_missing", "ImportersConsumption_prev1_missing"]
- `data/train.csv` (318614 bytes); columns: ["row_id", "Country", "Year", "Export_prev1", "Export_prev2", "Export_prev3", "Production_prev1", "Production_prev2", "Production_prev3", "DomesticConsumption_prev1", "DomesticConsumption_prev2", "Import_prev1", "Import_prev2", "ReExport_prev1", "ReExport_prev2", "Inventory_prev1", "Inventory_prev2", "ImportersConsumption_prev1", "ImportersConsumption_prev2", "CoffeeType", "export_yoy_prev1", "production_yoy_prev1", "export_roll3_mean_prev", "production_roll3_mean_prev", "import_minus_reexport_prev1", "production_minus_domestic_prev1", "export_to_production_prev1", "export_over_net_import_prev1", "inventory_over_domestic_prev1", "Export_prev1_missing", "Production_prev1_missing", "DomesticConsumption_prev1_missing", "Import_prev1_missing", "ReExport_prev1_missing", "Inventory_prev1_missing", "ImportersConsumption_prev1_missing", "Export"]

## Public description

Global Coffee Exports Forecast Challenge

Problem statement
Predict each country’s annual coffee export volume (in kilo units) for the next calendar year using historical, country-level panel data covering production, imports, re-exports, inventories, and consumption. Participants must build time-aware models that leverage multi-table features while strictly avoiding leakage from future information.

Provided files
- train.csv: Feature matrix with labels for calendar years up to and including 2016. Each row represents a (Country, Year) pair with engineered features that use only past data (up to Year−1) and the label Export for Year.
- test.csv: Feature matrix without labels for calendar years 2017–2019. Each row represents a (Country, Year) pair with engineered features using only past data (up to Year−1). Includes a deterministic row_id and the identification columns Country and Year.
- sample_submission.csv: A valid submission example containing columns [row_id, Export] for the test.csv rows.

What you are predicting
- Target: Export, the total calendar-year export volume for each country.
- Units: kilo (1000 grams).

Data description and feature notes
- Multi-source panel features are created from the following domains: production (with a categorical CoffeeType per country), domestic consumption, imports, re-exports, importers’ consumption, and green-coffee inventories.
- Time alignment: Coffee-year columns (e.g., 1990/91) are mapped to the calendar end-year (e.g., 1991) for consistency. Calendar-year tables remain unchanged.
- Ignored columns: All period totals such as Total_export, Total_import, Total_re_export, Total_domestic_consumption, Total_import_consumption, Total_inventorie, Total_production are excluded from features to prevent leakage.
- Cleaning: Country names are trimmed and harmonized; sentinel values (e.g., -2147483648) are treated as missing.
- Engineered signals (non-leaky): Lags (t−1, t−2, t−3), rolling means, year-over-year growth rates, ratios (e.g., export/production, inventories/consumption), trade balance signals like imports minus re-exports, and production minus domestic consumption. Missingness indicators are included for sparse series.

Evaluation
- Metric: Root Mean Squared Logarithmic Error (RMSLE) between submitted predictions and ground truth exports across all test rows. We compute RMSLE as sqrt(mean((log1p(y_pred) − log1p(y_true))^2))). Predictions are clamped to non-negative before scoring to ensure numerical stability.
- Rationale: Export volumes vary by orders of magnitude across countries; RMSLE emphasizes relative accuracy and handles zeros gracefully.

Submission format
- CSV with columns: row_id, Export
- row_id must exactly match the ids provided in test.csv.

Train/test split
- Train: All aligned calendar years up to and including 2016.
- Test: 2017–2019.
- No validation split is provided; participants are encouraged to use time-based cross-validation over the training period.

Important notes
- The provided engineered features are deterministic and strictly based on historical information up to Year−1 for each row.
- Participants may add or transform features from train/test files, but must maintain the submission format and respect temporal causality.
