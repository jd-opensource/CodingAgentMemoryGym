# OpenMLE-fast task

Task ID: `australia-rain-dataset@1`

Native metric: `AustraliaRainLogLossMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3267 bytes)
- `data/sample_submission.csv` (708138 bytes); columns: ["RowId", "RainTomorrow"]
- `data/test.csv` (3084169 bytes); columns: ["RowId", "Date", "Location", "MinTemp", "MaxTemp", "Rainfall", "Evaporation", "Sunshine", "WindGustDir", "WindGustSpeed", "WindDir9am", "WindDir3pm", "WindSpeed9am", "WindSpeed3pm", "Humidity9am", "Humidity3pm", "Pressure9am", "Pressure3pm", "Cloud9am", "Cloud3pm", "Temp9am", "Temp3pm", "RainToday"]
- `data/train.csv` (12295598 bytes); columns: ["Date", "Location", "MinTemp", "MaxTemp", "Rainfall", "Evaporation", "Sunshine", "WindGustDir", "WindGustSpeed", "WindDir9am", "WindDir3pm", "WindSpeed9am", "WindSpeed3pm", "Humidity9am", "Humidity3pm", "Pressure9am", "Pressure3pm", "Cloud9am", "Cloud3pm", "Temp9am", "Temp3pm", "RainToday", "RainTomorrow"]

## Public description

Australia Next-Day Rain Occurrence Challenge

Background
Daily meteorological observations across 49 Australian locations over multiple years capture rich weather variability in temperature, humidity, wind, pressure, cloud cover, and rainfall. Reliable next-day rain forecasts are crucial for agriculture, logistics, energy, and hazard mitigation.

Problem
Given same-day weather observations at a station, forecast the probability that it will rain tomorrow. Participants must build models that output calibrated probabilities for next-day rain occurrence (Yes/No).

Data
- train.csv: Labeled tabular data with daily observations and the target column RainTomorrow.
- test.csv: Unlabeled tabular data with the same feature set as train.csv (excluding RainTomorrow), plus a RowId column.
- sample_submission.csv: Example file showing the required submission format.

Columns (features)
The tabular records include the following columns (subject to missing values):
Date, Location, MinTemp, MaxTemp, Rainfall, Evaporation, Sunshine, WindGustDir, WindGustSpeed, WindDir9am, WindDir3pm, WindSpeed9am, WindSpeed3pm, Humidity9am, Humidity3pm, Pressure9am, Pressure3pm, Cloud9am, Cloud3pm, Temp9am, Temp3pm, RainToday. The target is RainTomorrow (Yes/No) in train.csv only.

Train/test split
To prevent temporal leakage and preserve local climate characteristics, the split is time-aware per Location: the most recent 20% of dates for each location are assigned to test.csv; the earlier 80% are assigned to train.csv. All rows with missing target labels are excluded before splitting. The split is deterministic.

Submission format
Submit a CSV with the following columns:
- RowId: Unique integer identifier matching the rows in test.csv.
- RainTomorrow: Predicted probability of rain tomorrow, a float in [0, 1].
Each test row must be predicted exactly once; do not reorder or omit RowIds.

Evaluation metric
Submissions are evaluated using binary log loss on predicted probabilities:
logloss = mean( -[ y * log(p) + (1 - y) * log(1 - p) ] ), where y ∈ {0,1} and p ∈ [0,1].
Probabilities are clipped to [1e-15, 1 - 1e-15] for numerical stability. Log loss fairly penalizes overconfident errors, is threshold-independent, and handles class imbalance better than accuracy.

Guidance and expectations
- Data Processing: Parse Date and consider deriving calendar features (e.g., month, day-of-year) to capture seasonality. Handle missing values using training-only statistics.
- Feature Engineering: Encode categorical wind directions (e.g., one-hot or compass angle), create rolling aggregates from strictly prior days (e.g., 3-day mean humidity, 7-day rainfall sum) per location, and consider interaction terms.
- Modeling: Tabular ML methods (e.g., gradient boosting, random forests, regularized logistic regression) and modern tabular deep learning are applicable. Calibration (e.g., Platt scaling, isotonic regression) is recommended.
- Evaluation: Optimize log loss. Avoid target leakage; fit all preprocessing and feature creation using training data only and past information.

Files provided
train.csv, test.csv, sample_submission.csv.

Goal
Build a robust, well-calibrated model that generalizes across locations and seasons to minimize log loss on the test set.
