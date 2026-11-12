# OpenMLE-fast task

Task ID: `weather-forcasting@1`

Native metric: `WeatherNowcastingMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2604 bytes)
- `data/sample_submission.csv` (6447 bytes); columns: ["row_id", "rain_probability"]
- `data/test.csv` (48155 bytes); columns: ["row_id", "Temperature", "Humidity", "Wind_Speed", "Cloud_Cover", "Pressure"]
- `data/train.csv` (115464 bytes); columns: ["row_id", "Temperature", "Humidity", "Wind_Speed", "Cloud_Cover", "Pressure", "Rain"]

## Public description

Weather Nowcasting: Rain Probability from Surface Measurements

Problem statement
Given single-timepoint measurements from a weather station, your task is to predict the probability that rain is occurring at that moment. You are provided with meteorological features (Temperature, Humidity, Wind_Speed, Cloud_Cover, Pressure). Build a model to output a calibrated probability of rain for each test row.

Why this matters
Detecting rain from surface observations is critical to aviation, agriculture, and urban drainage. The dataset is moderately small and imbalanced, demanding careful preprocessing, modeling, and probability calibration.

Files you will use
- train.csv: Labeled training data with all features and the target.
- test.csv: Unlabeled test data with the same features.
- sample_submission.csv: A valid example submission with the required format.

Data description
Each row is an independent station-level observation.
Columns in train.csv:
- row_id: Unique integer identifier for the row.
- Temperature: Continuous, degrees Celsius.
- Humidity: Continuous, percent (0–100+ possible due to measurement noise).
- Wind_Speed: Continuous, meters per second.
- Cloud_Cover: Continuous, percent (0–100+ possible due to measurement noise).
- Pressure: Continuous, hPa.
- Rain: Binary target; 1 = rain, 0 = no rain.

Columns in test.csv:
- row_id: Unique integer identifier for the row (to be used in your submission).
- Temperature, Humidity, Wind_Speed, Cloud_Cover, Pressure: Same definitions as train.

Submission format
Submit a CSV file with exactly these columns and no extra columns:
- row_id: Integer identifier matching those in test.csv.
- rain_probability: A float in [0, 1] representing P(Rain = 1).

Evaluation
Submissions are evaluated using Average Precision (area under the precision–recall curve) for the positive class Rain = 1. AP emphasizes ranking quality for the minority (rain) class under class imbalance. Your predicted probabilities will be clipped to [0, 1] before scoring to ensure numerical stability.

Important notes
- The task is imbalanced. Consider class-aware modeling strategies (e.g., class weights, focal losses), robust cross-validation (e.g., Stratified K-fold), and probability calibration.
- Feature engineering is allowed and encouraged (e.g., interactions, nonlinear transforms). External data is not necessary.
- Use the provided sample_submission.csv to verify your pipeline’s output format.

Reproducibility
The provided prepare.py script creates deterministic train/test splits. You can reproduce the split and sample submission locally.
