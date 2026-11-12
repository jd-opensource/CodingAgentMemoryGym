# OpenMLE-fast task

Task ID: `arms-imports-per-country@2`

Native metric: `ArmsImportsSpikeMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3849 bytes)
- `data/panel_history_1950_2015.csv` (329213 bytes); columns: ["entity", "year", "value"]
- `data/sample_submission.csv` (14404 bytes); columns: ["id", "spike"]
- `data/test.csv` (59821 bytes); columns: ["id", "entity", "year", "lag1", "lag2", "lag3", "mean_prev3", "std_prev3", "min_prev3", "max_prev3", "delta1", "delta2", "rel_lag1", "volatility3"]
- `data/train.csv` (682191 bytes); columns: ["id", "entity", "year", "spike", "lag1", "lag2", "lag3", "mean_prev3", "std_prev3", "min_prev3", "max_prev3", "delta1", "delta2", "rel_lag1", "volatility3"]

## Public description

Arms-Imports Spike Detection (Event-onset Prediction)

Problem statement
You are given a multi-entity annual time series panel of arms imports (1950–2020). For each entity-year t, predict whether year t is a spike in imports relative to the recent baseline, using only information available strictly before t. This is a binary classification task evaluated by ranking quality (Average Precision / PR AUC).

Target definition (fixed and public)
For an entity-year t:
- Compute the mean of the previous 3 years: mean_prev3 = mean(value[t-3], value[t-2], value[t-1]). All three years must be present and non-null.
- If value[t] is missing or any of the three previous values is missing, that (entity, t) is not used.
- Label spike[t] = 1 if value[t] >= max(2 * mean_prev3, mean_prev3 + 200); else spike[t] = 0.

Split
- Training examples: all valid (entity, t) with t ≤ 2015.
- Test examples: all valid (entity, t) with 2016 ≤ t ≤ 2020.
This forward-chaining split prevents time leakage.

Files provided
- train.csv: Supervised learning table with one row per training example. Columns:
  - id: unique identifier of an (entity, year) example in the format "entity|year"
  - entity: entity name (country/region/group)
  - year: year t (the target year)
  - spike: binary target (0/1)
  - lag1, lag2, lag3: values at t-1, t-2, t-3 (if any is missing, the example is excluded)
  - mean_prev3, std_prev3, min_prev3, max_prev3: rolling statistics over t-3..t-1
  - delta1, delta2: first differences lag1-lag2 and lag2-lag3
  - rel_lag1: lag1 / (mean_prev3 + 1e-9)
  - volatility3: std_prev3 / (mean_prev3 + 1e-9)
- test.csv: Same columns as train.csv except without the spike column. Contains only the valid test examples (2016–2020). The id order in test.csv is the canonical order.
- sample_submission.csv: Two columns: id, spike. The spike values are example probabilities in [0,1]. The ids must exactly match test.csv in both content and order.

Important notes
- Only information from years prior to t is provided as features; the current-year value value[t] is never included in either train or test features.
- An additional raw-history resource (panel_history_1950_2015.csv) is provided with the original panel values for 1950–2015 to support exploratory analysis and custom feature engineering that does not rely on future information. Do not attempt to reconstruct labels for the test set from this file; it does not contain any current-year values for test years.
- All entities (countries/regions/groups) are included where the target can be computed. Any entity/year without a complete 3-year history is excluded automatically because the target is undefined.

Evaluation
- Metric: Average Precision (area under the precision–recall curve, PR AUC) computed on test examples, where higher is better.
- Submission format: A single CSV with exactly two columns [id, spike], where spike is a predicted probability (or real-valued score) for spike=1. The ids must match test.csv exactly and in the same order. All scores must be finite real numbers (they will be clipped to [0,1] before scoring).

Modeling guidance
Participants are expected to build ML models using the provided features and may engineer additional features from them. Typical helpful features include additional rolling statistics, ratio and difference transforms, growth rates, momentum indicators, and non-linear interactions. Any model family is allowed (e.g., gradient-boosted trees, linear/logistic models, neural nets) as long as only information available before t is used. Given the class imbalance (positives are relatively rare), consider class-weighting, focal loss, or threshold-calibration techniques.

Final data files for the competition
- train.csv
- test.csv
- sample_submission.csv
- panel_history_1950_2015.csv (auxiliary history for exploration)
