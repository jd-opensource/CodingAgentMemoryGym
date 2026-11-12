# OpenMLE-fast task

Task ID: `banjir-jabodetabek@1`

Native metric: `FloodPredictionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2835 bytes)
- `data/sample_submission.csv` (143459 bytes); columns: ["id", "banjir"]
- `data/test.csv` (479700 bytes); columns: ["id", "NAME_2", "NAME_3", "avg_rainfall", "max_rainfall", "avg_temperature", "elevation", "landcover_class", "ndvi", "slope", "soil_moisture", "year", "month", "lat", "long"]
- `data/train.csv` (1931840 bytes); columns: ["id", "NAME_2", "NAME_3", "avg_rainfall", "max_rainfall", "avg_temperature", "elevation", "landcover_class", "ndvi", "slope", "soil_moisture", "year", "month", "lat", "long", "banjir"]

## Public description

Title: National Flood Occurrence Prediction (Tabular-only)

Problem statement
You are given monthly environmental and physiographic indicators for Indonesian districts. For each district–month, predict the probability that a flood occurs (banjir=1). This is a binary probabilistic classification task; your model should output well-calibrated probabilities rather than hard labels.

Data description
Final files provided:
- train.csv: Tabular training data with features and the target column banjir.
- test.csv: Tabular test data with the same features as train.csv, plus an id column; the target is withheld.
- sample_submission.csv: Example submission with the required columns id and banjir (predicted probability for banjir=1).

Each row corresponds to a district (NAME_2, NAME_3) in a specific year and month. Columns include:
- id: Unique identifier for the row.
- NAME_2, NAME_3: Province and district names (normalized lowercase strings).
- avg_rainfall, max_rainfall: Aggregated rainfall indicators.
- avg_temperature: Average air temperature.
- elevation: Terrain elevation.
- landcover_class: Dominant land cover category (normalized to a small set of tokens such as tree_cover, built_up, cropland, water, wetlands, shrubland, grassland, bare, unknown).
- ndvi: Vegetation index.
- slope: Terrain slope in degrees.
- soil_moisture: Surface soil moisture proxy.
- year, month: Time indices.
- lat, long: Representative coordinates of the district.
- banjir: Only in train.csv. Binary target indicating whether a flood was recorded that month (1) or not (0).

The data spans multiple years, with the held-out test period covering a future year to evaluate temporal generalization. Note: No image data is required in this track; the provided satellite imagery is not used by the official evaluation.

Submission format
- A CSV file with two columns: id and banjir.
- id must match the ids in test.csv (order does not matter).
- banjir must be a probability in [0, 1] for the class banjir=1.

Evaluation metric
- Log Loss (binary cross-entropy) computed over the test set.
- Your predictions are clipped to [1e-15, 1-1e-15] before scoring to ensure numerical stability.

Guidance
- Use feature engineering on climate, terrain, land cover, seasonality (month), and spatiotemporal effects (interactions, encodings of district and province).
- Proper preprocessing (handling missing values, outlier clipping, categorical encoding) and calibration can improve performance.
- Models such as gradient-boosted trees, random forests, and tabular neural networks are suitable baselines. Temporal validation (e.g., training on past years and validating on later months) is recommended.

Files to submit
- A single CSV file with columns id and banjir.

Good luck reducing disaster risk with timely, accurate flood probability forecasts!
