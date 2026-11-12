# OpenMLE-fast task

Task ID: `predicting-manufacturing-defects-dataset@2`

Native metric: `ManufacturingDefectRateMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3022 bytes)
- `data/prepare_manifest.json` (520 bytes)
- `data/sample_submission.csv` (14996 bytes); columns: ["Id", "DefectRate"]
- `data/test.csv` (140641 bytes); columns: ["Id", "ProductionVolume", "ProductionCost", "SupplierQuality", "DeliveryDelay", "QualityScore", "MaintenanceHours", "DowntimePercentage", "InventoryTurnover", "StockoutRate", "WorkerProductivity", "SafetyIncidents", "EnergyConsumption", "EnergyEfficiency", "AdditiveProcessTime", "AdditiveMaterialCost"]
- `data/train.csv` (607365 bytes); columns: ["Id", "ProductionVolume", "ProductionCost", "SupplierQuality", "DeliveryDelay", "QualityScore", "MaintenanceHours", "DowntimePercentage", "InventoryTurnover", "StockoutRate", "WorkerProductivity", "SafetyIncidents", "EnergyConsumption", "EnergyEfficiency", "AdditiveProcessTime", "AdditiveMaterialCost", "DefectRate"]

## Public description

Predicting Daily Defect Rate in Manufacturing (Regression)

Problem
Quality and manufacturing engineers need precise daily forecasts of expected defects per thousand units to plan inspections, allocate maintenance, and prioritize supplier and process improvements. Your task is to build a regression model that predicts the continuous DefectRate for each production day from operational, quality, maintenance, inventory, workforce, energy, and additive manufacturing metrics.

Files you will use
- train.csv — Tabular training data with Id, all features, and the target column DefectRate.
- test.csv — Same features and Id as train.csv but without DefectRate.
- sample_submission.csv — Example of the required submission format.

Target
- DefectRate (float): expected defects per thousand units produced (approximately in the range 0.5–5.0).

Inputs (features)
All features are numeric and cleanly bounded:
- ProductionVolume (int)
- ProductionCost (float)
- SupplierQuality (float, %)
- DeliveryDelay (int, days)
- QualityScore (float, %)
- MaintenanceHours (int, hours/week)
- DowntimePercentage (float, %)
- InventoryTurnover (float)
- StockoutRate (float, %)
- WorkerProductivity (float, %)
- SafetyIncidents (int, per month)
- EnergyConsumption (float, kWh)
- EnergyEfficiency (float)
- AdditiveProcessTime (float, hours)
- AdditiveMaterialCost (float, $)

Notes
- Id is a unique row identifier provided for joining and submission only; do not treat Id as a predictive feature.
- The original dataset may also include a binary DefectStatus field. It is excluded to avoid leakage and keep the task focused on precise regression of DefectRate.

Submission format
- A single CSV with two columns and a header: Id,DefectRate
- Id must match exactly the Id values provided in test.csv (unique, same set and count).
- DefectRate must be numeric and finite for every row. Predictions will not be clipped; use your best estimate.

Evaluation
- Metric: Root Mean Squared Error (RMSE)
  RMSE = sqrt(mean((y_pred - y_true)^2))
- Rationale: RMSE is on the same scale as DefectRate and penalizes large errors, encouraging accuracy across both low- and high-defect regimes.

Split policy
- A single deterministic split between train.csv and test.csv is provided. There is no temporal component; the split is stratified by target quantiles to ensure coverage across the DefectRate range.

Modeling tips
- Strong tabular baselines include gradient-boosted trees, random forests, linear models with interactions, and tabular neural networks.
- Consider feature engineering: interactions (e.g., ProductionVolume × DowntimePercentage), ratios (e.g., EnergyConsumption per unit), non-linear transforms, and monotonic constraints where appropriate.
- Expect mild heteroscedasticity across production scales; regularization and robust validation will help.

Deliverable
- Submit a file named, for example, submission.csv with columns: Id,DefectRate.
- The leaderboard is computed with RMSE on the hidden ground truth for test.csv.
