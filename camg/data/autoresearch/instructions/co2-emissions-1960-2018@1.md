# OpenMLE-fast task

Task ID: `co2-emissions-1960-2018@1`

Native metric: `CO2PerCapitaForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2727 bytes)
- `data/entity_map.csv` (4943 bytes); columns: ["entity_id", "entity_name"]
- `data/sample_submission.csv` (34231 bytes); columns: ["entity_id", "year", "co2_per_capita"]
- `data/test.csv` (11965 bytes); columns: ["entity_id", "year"]
- `data/train.csv` (360049 bytes); columns: ["entity_id", "year", "co2_per_capita"]

## Public description

Title: Global Panel Forecast — CO2 per capita 2014–2018

Problem statement
Predict per‑capita CO2 emissions for the last five years (2014–2018) for every entity (countries and regional aggregates) using only their historical trajectories. You are given long‑horizon annual series from 1960–2018. Train on years up to and including 2013 and forecast 2014–2018.

Why this is interesting and hard
- Heterogeneous dynamics across entities (industrialization, policy shifts, shocks)
- Non‑stationary trends and varying history lengths
- Heavy‑tailed targets (small islands vs hydrocarbon producers)

Files provided after running prepare.py
- train.csv: Panel in long format with columns [entity_id, year, co2_per_capita] for all years ≤ 2013 (may include missing values where the source is missing).
- test.csv: The rows to predict with columns [entity_id, year] for all entity‑years in 2014–2018 where ground truth exists.
- sample_submission.csv: Same shape and ordering as test.csv, with a baseline set of numeric predictions.
- entity_map.csv: Mapping between entity_id and the original entity name for reference.

Task
- Use train.csv (and any features you engineer from it) to predict co2_per_capita for the rows listed in test.csv.
- Submit a CSV with columns [entity_id, year, co2_per_capita] containing one prediction for every row in test.csv, in the same order. Predictions must be finite, non‑negative real numbers.

Evaluation
- Metric: Mean Absolute Error on the log1p scale.
    - For each row: err = |log1p(y_pred) − log1p(y_true)|
    - Score = mean(err) over all rows
- Rationale: log1p stabilizes heavy tails, avoids dominance by large emitters, and is defined at zero.

Data description
- entity_id: Integer identifier for an entity (country or region). Use entity_map.csv if you need the human‑readable name; do not infer labels from names.
- year: Integer year.
- co2_per_capita: Metric tons of CO2 per person. Non‑negative real number. train.csv may contain missing entries reflecting the source data; test.csv only contains rows where ground truth exists (used privately for scoring).

Rules and expectations
- Use only information available in years ≤ 2013 to build features. Do not leak future labels.
- Typical approaches: lag/rolling features, differences and growth rates, cross‑sectional pooling (global models), gradient boosting on panel features, ARIMA/ETS, RNN/TFT.
- Your submission must exactly match the rows and order of test.csv and include columns [entity_id, year, co2_per_capita].

Final data files used in this competition
- train.csv
- test.csv
- sample_submission.csv
- entity_map.csv

Good luck and have fun building robust global forecasting models!
