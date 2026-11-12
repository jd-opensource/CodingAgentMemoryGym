# OpenMLE-fast task

Task ID: `european-electricity-price-and-generation-2024-25@1`

Native metric: `ElectricityPriceRMSEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3729 bytes)
- `data/sample_submission.csv` (1226325 bytes); columns: ["row_id", "price"]
- `data/test.csv` (6145570 bytes); columns: ["row_id", "datetime", "country", "nuclear", "fossil_gas", "solar", "waste", "wind_offshore", "wind_onshore", "_biomass_actual_aggregated_", "_fossil_brown_coal_lignite_actual_aggregated_", "_fossil_coal_derived_gas_actual_aggregated_", "_fossil_gas_actual_aggregated_", "_fossil_hard_coal_actual_aggregated_", "_fossil_oil_actual_aggregated_", "_hydro_pumped_storage_actual_aggregated_", "_hydro_pumped_storage_actual_consumption_", "_hydro_run_of_river_and_poundage_actual_aggregated_", "_hydro_water_reservoir_actual_aggregated_", "_other_actual_aggregated_", "_other_renewable_actual_aggregated_", "_solar_actual_aggregated_", "_wind_onshore_actual_aggregated_", "biomass", "energy_storage", "fossil_brown_coal_lignite", "fossil_coal_derived_gas", "fossil_hard_coal", "fossil_oil", "fossil_oil_shale", "fossil_peat", "geothermal", "hydro_pumped_storage", "hydro_run_of_river_and_poundage", "hydro_total", "hydro_water_reservoir", "marine", "other", "other_renewable"]
- `data/train.csv` (32941938 bytes); columns: ["row_id", "datetime", "country", "price", "nuclear", "fossil_gas", "solar", "waste", "wind_offshore", "wind_onshore", "_biomass_actual_aggregated_", "_fossil_brown_coal_lignite_actual_aggregated_", "_fossil_coal_derived_gas_actual_aggregated_", "_fossil_gas_actual_aggregated_", "_fossil_hard_coal_actual_aggregated_", "_fossil_oil_actual_aggregated_", "_hydro_pumped_storage_actual_aggregated_", "_hydro_pumped_storage_actual_consumption_", "_hydro_run_of_river_and_poundage_actual_aggregated_", "_hydro_water_reservoir_actual_aggregated_", "_other_actual_aggregated_", "_other_renewable_actual_aggregated_", "_solar_actual_aggregated_", "_wind_onshore_actual_aggregated_", "biomass", "energy_storage", "fossil_brown_coal_lignite", "fossil_coal_derived_gas", "fossil_hard_coal", "fossil_oil", "fossil_oil_shale", "fossil_peat", "geothermal", "hydro_pumped_storage", "hydro_run_of_river_and_poundage", "hydro_total", "hydro_water_reservoir", "marine", "other", "other_renewable"]

## Public description

European Electricity Price & Generation Forecasting Challenge

Problem statement
Forecast the hourly day-ahead market clearing price (€/MWh) for 20 European bidding areas. Build models that use only information available up to the prediction time, leveraging historical prices and generation mix across countries. Expect strong seasonality, negative price episodes, spikes, and cross-country dependencies.

Files
- train.csv: Hourly observations for the training period.
  - Columns include:
    - row_id: unique identifier.
    - datetime: hour timestamp in UTC, ISO 8601 (e.g., 2025-04-01T00:00:00Z).
    - country: bidding area code.
    - price: day-ahead market clearing price (€/MWh) [target].
    - Generation mix columns by fuel type (as available): nuclear, fossil_gas, solar, waste, wind_offshore, wind_onshore, biomass, energy_storage, fossil_brown_coal_lignite, fossil_coal_derived_gas, fossil_hard_coal, fossil_oil, fossil_oil_shale, fossil_peat, geothermal, hydro_pumped_storage, hydro_run_of_river_and_poundage, hydro_water_reservoir, hydro_total, marine, other, other_renewable.
    - Aggregated variants for some fuels and countries may appear (e.g., _biomass_actual_aggregated_, _fossil_gas_actual_aggregated_, _hydro_*_actual_aggregated_, _solar_actual_aggregated_, _wind_onshore_actual_aggregated_).
- test.csv: Same columns as train.csv except price is omitted.
- sample_submission.csv: Example file demonstrating the expected submission format.

Train/test split
- Train period: 2024-01-01 00:00:00 UTC to 2025-03-31 23:00:00 UTC (all countries).
- Test period: 2025-04-01 00:00:00 UTC to 2025-06-30 23:00:00 UTC (all countries).

Modeling guidance and constraints
- Time-causality: Use only information available up to (but not including) the prediction timestamp. In particular, do not use contemporaneous (same-hour) actual generation values for the target timestamp; engineer features from historical signals (lags/rolling statistics) instead.
- Generation columns: When both canonical and aggregated variants exist for the same fuel, avoid double-counting. Prefer canonical values; treat aggregated variants as fallbacks for missingness.
- Time handling: All datetimes are normalized to UTC. Derive calendar features (hour-of-day, day-of-week, month, weekend/weekday flags) and handle DST quirks via UTC.
- Missingness and sparsity: Some fuels may be unreported/absent for certain countries. Handle NaNs robustly and consider explicit missingness indicators and "fuel_available" flags.
- Cross-country signals: You may exploit historical interdependencies by constructing lagged features from other countries’ prices and generation.

Submission format
- A CSV with two columns in this exact order: [row_id, price].
- row_id must match the identifiers in test.csv.
- price must be finite numeric values (€/MWh) for every test row.

Evaluation
- Metric: Root Mean Squared Error (RMSE) over all test rows.
  - RMSE = sqrt(mean((y_true - y_pred)^2))
  - Computed across all country-hours in the test period with equal per-row weighting.
  - RMSE preserves the native scale, penalizes large errors, and handles negative prices appropriately.

Why this is challenging and meaningful
- Multi-country, hourly forecasting with heterogeneous generation portfolios.
- Pronounced diurnal/weekly/seasonal patterns, negative price episodes, and spikes.
- Structural missingness in some fuels and aggregated-vs-canonical reporting differences.
- Cross-country interdependencies that reward robust feature engineering and modeling.

Deliverables
- Train a model on train.csv, predict for test.csv, and submit a CSV matching sample_submission.csv. The leaderboard score is computed via RMSE on the test period.
