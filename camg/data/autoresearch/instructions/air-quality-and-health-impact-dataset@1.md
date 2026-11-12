# OpenMLE-fast task

Task ID: `air-quality-and-health-impact-dataset@1`

Native metric: `AirQualityOrdinalHealthImpactMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3029 bytes)
- `data/sample_submission.csv` (7906 bytes); columns: ["Id", "HealthImpactClass"]
- `data/test.csv` (197355 bytes); columns: ["Id", "AQI", "PM10", "PM2_5", "NO2", "SO2", "O3", "Temperature", "Humidity", "WindSpeed"]
- `data/train.csv` (798163 bytes); columns: ["Id", "AQI", "PM10", "PM2_5", "NO2", "SO2", "O3", "Temperature", "Humidity", "WindSpeed", "HealthImpactClass"]

## Public description

Air Quality Ordinal Health Impact Classification

Problem statement
Given environmental measurements of air quality and weather, predict the ordinal health impact severity class for each observation. The target has five ordered categories: 0=Very High, 1=High, 2=Moderate, 3=Low, 4=Very Low. Your goal is to build a model that maps pollutant concentrations and weather conditions to the correct severity class while respecting the ordinal structure of the labels.

Files
- train.csv: Training data containing feature columns and the target HealthImpactClass. Includes an Id column.
- test.csv: Test data containing the same feature columns as train.csv (without the target). Includes an Id column matching sample_submission.csv.
- sample_submission.csv: A sample submission file with the required format (Id, HealthImpactClass).

Target
- HealthImpactClass (integer in {0,1,2,3,4})
  - 0: Very High
  - 1: High
  - 2: Moderate
  - 3: Low
  - 4: Very Low

Features
Use only the environmental drivers provided below. These are the sole inputs in train.csv and test.csv:
- AQI: Air Quality Index
- PM10: PM10 concentration (μg/m³)
- PM2_5: PM2.5 concentration (μg/m³)
- NO2: Nitrogen dioxide (ppb)
- SO2: Sulfur dioxide (ppb)
- O3: Ozone (ppb)
- Temperature: Degrees Celsius (°C)
- Humidity: Relative humidity (%)
- WindSpeed: Wind speed (m/s)

Do not expect outcome variables (e.g., medical counts) or any score that directly defines the label in the training/test files. The task focuses on learning from environmental signals.

Evaluation
Submissions are evaluated using Quadratic Weighted Kappa (QWK) between your predicted HealthImpactClass and the ground truth on the test set. QWK measures agreement between two ordinal ratings, penalizing distant misclassifications more than near misses and mitigating effects of class imbalance.
- Range: [-1, 1]
  - 1 indicates perfect agreement.
  - 0 indicates chance-level agreement.
  - Negative indicates worse than chance.

Submission format
- A CSV file with two columns and a header: Id, HealthImpactClass
- Each Id from test.csv must appear exactly once.
- HealthImpactClass must be an integer in {0,1,2,3,4} for every row.

Notes and modeling guidance
- The label is ordinal. Approaches that exploit the ordering (e.g., ordinal regression, cumulative link models, tailored loss functions, or calibrated thresholds) can improve performance.
- Class imbalance is present. Consider class-weighted losses, resampling, or calibrated decision rules.
- Tabular ML methods such as gradient-boosted trees, random forests, linear/GLM with interactions, and neural networks with appropriate regularization are all applicable.
- Sensible preprocessing may include standardization, robust scaling, log transforms for skewed pollutants, and engineered interactions (e.g., PM2_5/PM10) as you see fit.

Data integrity
- All rows in train.csv and test.csv have complete feature values.
- Id is a neutral identifier; it should be used only to merge predictions, not as a predictive feature.
