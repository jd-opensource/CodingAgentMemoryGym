# OpenMLE-fast task

Task ID: `pipeline-accidents@1`

Native metric: `PipelineAccidentCostMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3432 bytes)
- `data/sample_submission.csv` (11432 bytes); columns: ["id", "All Costs"]
- `data/test.csv` (89713 bytes); columns: ["id", "Accident Year", "Accident Date/Time", "Operator ID", "Operator Name", "Pipeline/Facility Name", "Pipeline Location", "Pipeline Type", "Liquid Type", "Liquid Subtype", "Liquid Name", "Accident City", "Accident County", "Accident State", "Accident Latitude", "Accident Longitude", "Unintentional Release (Barrels)", "Intentional Release (Barrels)", "Liquid Recovery (Barrels)", "Net Loss (Barrels)", "Liquid Ignition", "Liquid Explosion", "Pipeline Shutdown"]
- `data/train.csv` (520887 bytes); columns: ["id", "Accident Year", "Accident Date/Time", "Operator ID", "Operator Name", "Pipeline/Facility Name", "Pipeline Location", "Pipeline Type", "Liquid Type", "Liquid Subtype", "Liquid Name", "Accident City", "Accident County", "Accident State", "Accident Latitude", "Accident Longitude", "Unintentional Release (Barrels)", "Intentional Release (Barrels)", "Liquid Recovery (Barrels)", "Net Loss (Barrels)", "Liquid Ignition", "Liquid Explosion", "Pipeline Shutdown", "All Costs"]

## Public description

Competition title: Rapid Cost Estimation for Hazardous Liquid Pipeline Incidents

Problem statement:
Build a model that estimates the total financial impact (All Costs, USD) of hazardous liquid pipeline incidents using attributes observable at or shortly after the event. Your predictions should reflect realistic early-triage conditions, before line-item accounting or post-incident investigations are complete.

Data files:
- train.csv: Training data with features and the target column All Costs.
- test.csv: Test data with the same feature columns as train.csv, without All Costs.
- sample_submission.csv: Example submission file showing the required format.

Target:
- All Costs (numeric, USD). The distribution is heavy-tailed with rare, high-cost events.

Features (columns in train/test):
- id: Unique incident identifier (derived from the Report Number; treat as an identifier only).
- Accident Year
- Accident Date/Time (timestamp string; parse as needed)
- Operator ID
- Operator Name
- Pipeline/Facility Name
- Pipeline Location
- Pipeline Type
- Liquid Type
- Liquid Subtype
- Liquid Name
- Accident City
- Accident County
- Accident State
- Accident Latitude
- Accident Longitude
- Unintentional Release (Barrels)
- Intentional Release (Barrels)
- Liquid Recovery (Barrels)
- Net Loss (Barrels)
- Liquid Ignition (YES/NO)
- Liquid Explosion (YES/NO)
- Pipeline Shutdown (YES/NO)

Leakage prevention (important):
- Columns that directly compose the target (e.g., Property Damage Costs, Lost Commodity Costs, Emergency Response Costs, Environmental Remediation Costs, Other Costs) are excluded.
- Post-investigation labels (Cause Category/Subcategory), evacuations, injuries/fatalities, and shutdown/restart timestamps are excluded.
- This ensures the problem reflects early-knowledge prediction and avoids information that would not be known at triage time.

Train/test split:
- Chronological split to emulate future deployment: incidents up to and including 2015 form the training set; incidents from 2016 onward form the test set.

Submission format:
- A CSV with exactly two columns in this order:
  - id
  - All Costs
- The id values must match those in test.csv exactly (same order and content). Predictions must be numeric, non-negative, and finite.

Evaluation metric:
- Root Mean Squared Logarithmic Error (RMSLE) on All Costs:
  - RMSLE = sqrt(mean((log1p(y_pred) - log1p(y_true))^2))
- Rationale: RMSLE emphasizes proportional accuracy and provides a fair comparison across small and very large costs. It is robust to heavy tails and zero values.

Modeling guidance:
- Effective approaches include gradient boosting trees (e.g., XGBoost/LightGBM/CatBoost), regularized linear models on log-transformed targets, and tabular neural networks.
- Suggested feature engineering:
  - Parse Accident Date/Time into year, month, day-of-week, hour, and season.
  - Normalize categorical text (trim, consistent case) and encode via one-hot, target/frequency encoding, or hashing for high-cardinality fields (operator, facility, product names).
  - Log1p-transform skewed volume fields; standardize/scale numeric features as needed.
  - Add coarse geospatial buckets from latitude/longitude and include state effects.

Tips:
- Expect missing values and noisy text fields; robust preprocessing helps.
- The target is long-tailed; training on log1p(All Costs) is often beneficial, with inverse transform at inference time.
