# OpenMLE-fast task

Task ID: `nuclear-energy-datasets@2`

Native metric: `GlobalPlantGenerationMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3148 bytes)
- `data/sample_submission.csv` (48731 bytes); columns: ["plant_id", "generation_gwh_2019"]
- `data/test.csv` (237103 bytes); columns: ["plant_id", "country", "country_long", "capacity_mw", "latitude", "longitude", "primary_fuel", "other_fuel1", "other_fuel2", "other_fuel3", "commissioning_year", "year_of_capacity_data", "generation_gwh_2013", "generation_gwh_2014", "generation_gwh_2015", "generation_gwh_2016", "generation_gwh_2017", "generation_gwh_2018"]
- `data/train.csv` (1002043 bytes); columns: ["plant_id", "country", "country_long", "capacity_mw", "latitude", "longitude", "primary_fuel", "other_fuel1", "other_fuel2", "other_fuel3", "commissioning_year", "year_of_capacity_data", "generation_gwh_2013", "generation_gwh_2014", "generation_gwh_2015", "generation_gwh_2016", "generation_gwh_2017", "generation_gwh_2018", "generation_gwh_2019"]

## Public description

Global Plant-Level Annual Generation Prediction (2019)

Problem statement
Build a model that predicts the 2019 annual electricity generation (in GWh) of grid-scale power plants worldwide. You are given plant metadata (fuel, capacity, location, commissioning year, etc.) and historical reported generation (2013–2018) where available. Your task is to generalize across fuels, sizes, geographies, and plant ages to estimate 2019 generation.

Why it’s challenging
- Targets span orders of magnitude and are long-tailed (from zero to many thousands of GWh).
- Heterogeneous plants across fuels, regions, and vintages with sparse/missing history.
- Strong interactions (fuel × age × geography) and zero-inflation for some plants.

Files provided (after running prepare.py)
- train.csv: Training data containing plant features and the target column generation_gwh_2019.
- test.csv: Test data containing the same feature columns as train.csv, excluding the target.
- sample_submission.csv: Valid example submission file with random plausible predictions.

Target
- generation_gwh_2019 (regression; non-negative real values, unit: GWh).

Core columns you can expect
- plant_id: Unique identifier for each plant (stable across files).
- country, country_long
- capacity_mw
- latitude, longitude
- primary_fuel, other_fuel1, other_fuel2, other_fuel3
- commissioning_year, year_of_capacity_data
- generation_gwh_2013 … generation_gwh_2018 (historical reported values; may be missing)
- generation_gwh_2019 (target; only present in train.csv)

Note: Columns that are model-generated or risk label leakage (e.g., estimated_generation_* and various descriptive free-text fields) are excluded.

Evaluation
- Primary metric: sMAPE (Symmetric Mean Absolute Percentage Error), expressed in percent. Lower is better.
  sMAPE = mean over i of 200 * |yi - pi| / (|yi| + |pi|), with the term defined as 0 when yi = pi = 0.
- For reference (not used for ranking), MAE (mean absolute error, in GWh) may also be reported locally.

Submission format
- CSV with the following columns and header:
  - plant_id
  - generation_gwh_2019
- The file must include exactly one row per plant_id found in test.csv, with no duplicates or missing IDs.

Recommended approaches
- Data processing: Handle missing historical values, validate numeric ranges, and consider removing or encoding rare categories.
- Feature engineering: Capacity-factor proxies (generation/capacity/8.76), age features (2019 − commissioning_year), historical statistics (mean, trend, volatility), geography features (country/region), and fuel interactions.
- Modeling: Try gradient-boosted trees, random forests, or tabular neural networks with careful regularization; consider stratified CV by primary fuel.
- Calibration: Enforce non-negativity, and consider modeling in log-space or applying target transforms.

Reproducibility and fairness
- The split is deterministic and stratified by primary_fuel where possible.
- Only reported generation values are used as labels. Columns with estimated_generation_* are excluded.

Enjoy building robust, generalizable models for global power plant generation!
