# OpenMLE-fast task

Task ID: `goibibo-flight-data@2`

Native metric: `GoibiboCheapestFlightMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3494 bytes)
- `data/sample_submission.csv` (1914849 bytes); columns: ["id", "is_cheapest"]
- `data/test.csv` (5770252 bytes); columns: ["id", "airline", "flight_num", "travel_class", "origin", "destination", "dep_time", "arr_time", "duration_mins", "stops_count", "dep_hour", "dep_minute", "arr_hour", "arr_minute", "flight_date"]
- `data/train.csv` (22113292 bytes); columns: ["id", "airline", "flight_num", "travel_class", "origin", "destination", "dep_time", "arr_time", "duration_mins", "stops_count", "dep_hour", "dep_minute", "arr_hour", "arr_minute", "flight_date", "is_cheapest"]

## Public description

Goibibo Cheapest Flight Classification (Route-Date-Class)

Problem statement
Travelers face multiple flight options for the same route, date, and travel class. Your task is to predict, for each individual flight option, the probability that it is the cheapest option among all alternatives with the same flight date, origin, destination, and travel class. Ties may exist: more than one option can be the cheapest if they share the exact same minimum price.

Files
- train.csv: training data with features and the binary target is_cheapest.
- test.csv: test data with features only.
- sample_submission.csv: example submission file containing the required columns and random predictions.

Target
- is_cheapest: 1 if the option’s price equals the minimum price within its group (same date, origin, destination, and class), otherwise 0.

Data description
Each row corresponds to a unique flight option scraped from Goibibo, with schedule and context features that help determine competitiveness in price. The dataset is time-split: earlier dates are used for training and later dates for testing; therefore, groups are never split across train/test, and temporal leakage is prevented. The key feature fields are:
- id: unique identifier for each row.
- airline, flight_num, travel_class: categorical descriptors of the carrier and class.
- origin, destination: city/airport names.
- dep_time, arr_time: local times in HH:MM. Useful for schedule-based features.
- duration_mins: total duration in minutes (parsed from the raw duration string).
- stops_count: integer number of stops parsed from the raw stops field (0 for non-stop).
- dep_hour, dep_minute, arr_hour, arr_minute: parsed components of departure/arrival times.
- flight_date: calendar date (format dd-mm-YYYY).

Important note on leakage
- The ground-truth label is derived from price, but the raw price is not provided in train/test. Participants must not use any external source of prices to avoid leakage. The objective is to infer which options tend to be the cheapest based on schedule, route, carrier, and other observable attributes.

Recommended approaches (non-exhaustive)
- Data processing: cast dates and times, handle missing values, normalize/cap durations, robustly parse stops and schedule.
- Feature engineering: route popularity, airline presence and competition on route, time-bucketed schedule indicators (e.g., morning/peak), stop count indicators, airline×class interactions, weekday/weekend and month seasonality.
- Modeling: tabular ML models (e.g., gradient boosting, calibrated tree ensembles), target encodings for high-cardinality categorical fields, and ranking-aware calibration.
- Validation: time-based validation that respects the chronological split.

Evaluation
- Submissions must contain two columns with a header: id,is_cheapest.
- is_cheapest should be a predicted probability in [0,1].
- The official metric is Average Precision (area under the precision–recall curve) computed on the binary target is_cheapest. This metric is appropriate due to class imbalance and rewards correctly ranking the true cheapest options higher.

Rules and constraints
- Do not attempt to reconstruct hidden prices; use only the provided features.
- Keep predictions numeric, finite, and within [0,1].
- The set of ids in your submission must exactly match those in test.csv.

Deliverables
- One CSV file with columns: id,is_cheapest.

Good luck, and build the best probabilistic ranker for the cheapest option!
