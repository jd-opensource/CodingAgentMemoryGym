# OpenMLE-fast task

Task ID: `smart-farming-data-2024-sf24@1`

Native metric: `CropRecommendationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (566 bytes)
- `data/sample_submission.csv` (11507 bytes); columns: ["id", "label"]
- `data/test.csv` (125532 bytes); columns: ["id", "N", "P", "K", "temperature", "humidity", "ph", "rainfall", "soil_moisture", "soil_type", "sunlight_exposure", "wind_speed", "co2_concentration", "organic_matter", "irrigation_frequency", "crop_density", "pest_pressure", "fertilizer_usage", "growth_stage", "urban_area_proximity", "water_source_type", "frost_risk", "water_usage_efficiency"]
- `data/train.csv` (485742 bytes); columns: ["N", "P", "K", "temperature", "humidity", "ph", "rainfall", "label", "soil_moisture", "soil_type", "sunlight_exposure", "wind_speed", "co2_concentration", "organic_matter", "irrigation_frequency", "crop_density", "pest_pressure", "fertilizer_usage", "growth_stage", "urban_area_proximity", "water_source_type", "frost_risk", "water_usage_efficiency"]

## Public description

Title: SF24 Multi-Crop Recommendation Challenge

Files (under public/):
- train.csv: Tabular training data with features and the target column 'label'.
- test.csv: Test data with 'id' and all feature columns (no labels).
- sample_submission.csv: Example submission with columns ['id', 'label'].

Task
- Train a multi-class classifier to predict the 'label' for each row in test.csv.

Evaluation
- Macro F1 score over class labels. Higher is better.

Submission format
- CSV with two columns: id,label. IDs must match those in test.csv exactly and in the same order.
