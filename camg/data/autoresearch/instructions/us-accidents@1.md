# OpenMLE-fast task

Task ID: `us-accidents@1`

Native metric: `UsAccidentsSeverityMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3601 bytes)
- `data/sample_submission.csv` (96012 bytes); columns: ["ID", "Severity"]
- `data/test.csv` (3015539 bytes); columns: ["ID", "Source", "Start_Time", "Start_Lat", "Start_Lng", "Description", "Street", "City", "County", "State", "Zipcode", "Country", "Timezone", "Airport_Code", "Weather_Timestamp", "Temperature(F)", "Wind_Chill(F)", "Humidity(%)", "Pressure(in)", "Visibility(mi)", "Wind_Direction", "Wind_Speed(mph)", "Precipitation(in)", "Weather_Condition", "Amenity", "Bump", "Crossing", "Give_Way", "Junction", "No_Exit", "Railway", "Roundabout", "Station", "Stop", "Traffic_Calming", "Traffic_Signal", "Turning_Loop", "Sunrise_Sunset", "Civil_Twilight", "Nautical_Twilight", "Astronomical_Twilight"]
- `data/train.csv` (6868479 bytes); columns: ["ID", "Source", "Severity", "Start_Time", "Start_Lat", "Start_Lng", "Description", "Street", "City", "County", "State", "Zipcode", "Country", "Timezone", "Airport_Code", "Weather_Timestamp", "Temperature(F)", "Wind_Chill(F)", "Humidity(%)", "Pressure(in)", "Visibility(mi)", "Wind_Direction", "Wind_Speed(mph)", "Precipitation(in)", "Weather_Condition", "Amenity", "Bump", "Crossing", "Give_Way", "Junction", "No_Exit", "Railway", "Roundabout", "Station", "Stop", "Traffic_Calming", "Traffic_Signal", "Turning_Loop", "Sunrise_Sunset", "Civil_Twilight", "Nautical_Twilight", "Astronomical_Twilight"]

## Public description

Title: Ordinal Accident Severity at Detection Time

Problem statement
You are given a large-scale, heterogeneous tabular/text dataset of US traffic incidents. For each incident, only information available at detection time is provided (time, location, weather, road attributes, and free-text description). Your task is to predict the ordinal accident severity level in {1,2,3,4}, where higher values indicate more severe impact.

Files provided
- train.csv: Training rows with features and the target column Severity.
- test.csv: Test rows with features only (no labels).
- sample_submission.csv: Example submission file with the correct format.

Target
- Severity (integer in {1,2,3,4})

Features (columns in train/test)
- ID, Source, Start_Time, Start_Lat, Start_Lng, Description, Street, City, County, State, Zipcode, Country, Timezone, Airport_Code, Weather_Timestamp, Temperature(F), Wind_Chill(F), Humidity(%), Pressure(in), Visibility(mi), Wind_Direction, Wind_Speed(mph), Precipitation(in), Weather_Condition, Amenity, Bump, Crossing, Give_Way, Junction, No_Exit, Railway, Roundabout, Station, Stop, Traffic_Calming, Traffic_Signal, Turning_Loop, Sunrise_Sunset, Civil_Twilight, Nautical_Twilight, Astronomical_Twilight

Important notes
- Only detection-time information is included by design. Post-outcome fields (e.g., End_Time, End_Lat, End_Lng, Distance(mi)) are excluded to prevent label leakage.
- Text (Description) is free-form and can be used (e.g., TF-IDF or embeddings).
- Categorical columns are high-cardinality (e.g., City, Airport_Code, Weather_Condition). Consider robust encodings.
- Weather and environmental fields contain missing values; explicit missing indicators can help.
- Temporal/geospatial effects are important (e.g., seasonality, time of day, regional patterns).

Train/test split
- Deterministic chronological split by Start_Time to emulate "predicting the future": train contains incidents strictly before 2022-10-01 00:00:00; test contains incidents on or after that timestamp.
- The split preserves original row order.

Evaluation
- Submissions must be a CSV with columns: ID, Severity
  - ID must match the IDs in test.csv and be unique, one row per test record.
  - Severity must be integer labels in {1,2,3,4}.
- Metric: Quadratic Weighted Kappa (QWK) computed between your predictions and the hidden ground truth. QWK accounts for the ordinal nature of the labels and penalizes larger mis-rankings more strongly than smaller ones.

Baseline and modeling guidance (non-exhaustive)
- Time: extract hour-of-day, day-of-week, month, is-weekend, and interactions with latitude/longitude for seasonality.
- Geography: use Start_Lat/Start_Lng directly and/or grid encodings (e.g., geohashes) and spatiotemporal interactions.
- Categorical: high-cardinality encoders (target encoding with care, hashing, learned embeddings).
- Weather: numeric transformations and missingness indicators; map wind direction to circular features.
- Text: mine salient tokens and phrases (e.g., road names like I-95; incident descriptors like "multi-vehicle" or "jackknifed").
- Models: gradient boosting on engineered features; linear models with strong regularization; neural models that combine tabular and text signals.

Submission format example
- See sample_submission.csv for the exact column names and types.

Rules and cautions
- Do not infer or reconstruct excluded post-outcome information; focus on detection-time features only.
- Ensure predictions are valid integers in {1,2,3,4}.
- The leaderboard uses QWK; ties are broken by higher QWK and then by submission time.
