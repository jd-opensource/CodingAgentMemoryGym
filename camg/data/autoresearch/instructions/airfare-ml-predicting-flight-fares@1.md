# OpenMLE-fast task

Task ID: `airfare-ml-predicting-flight-fares@1`

Native metric: `AirfareFareRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (5077 bytes)
- `data/sample_submission.csv` (1352723 bytes); columns: ["id", "Fare"]
- `data/test.csv` (9836117 bytes); columns: ["id", "Date_of_journey", "Journey_day", "Airline", "Flight_code", "Class", "Source", "Departure", "Total_stops", "Arrival", "Destination", "Duration_in_hours", "Days_left"]
- `data/train.csv` (41410953 bytes); columns: ["id", "Date_of_journey", "Journey_day", "Airline", "Flight_code", "Class", "Source", "Departure", "Total_stops", "Arrival", "Destination", "Duration_in_hours", "Days_left", "Fare"]

## Public description

Airfare ML: Predicting Flight Fares

Overview
Predict the fare (in INR) for domestic flight options in India given their attributes at the time of search. You are provided with a curated, cleaned tabular dataset plus an auxiliary table with richer time-level features parsed from the original scrape. Your goal is to build a model that generalizes across routes, airlines, classes, stops, and time-of-day to minimize error on unseen flight options.

Files you will use
- train_cleaned.csv
  - Columns (features + label):
    - id: Unique integer identifier for a flight option.
    - Date_of_journey: YYYY-MM-DD journey date.
    - Journey_day: Day-of-week string.
    - Airline: Airline name.
    - Flight_code: Flight code (airline code + number).
    - Class: Cabin class (e.g., Economy, Business).
    - Source, Destination: Origin and destination cities.
    - Departure: Departure time bucket (Before 6 AM, 6 AM - 12 PM, 12 PM - 6 PM, After 6 PM).
    - Arrival: Arrival time bucket (same categories as Departure).
    - Total_stops: Categorical stops indicator (e.g., non-stop, 1-stop, 2-stop).
    - Duration_in_hours: Flight duration in hours (decimal).
    - Days_left: Days from the fixed booking date to the journey date.
    - Fare: Target label (positive float, INR).

- test_cleaned.csv
  - Same columns as train_cleaned.csv except Fare is withheld. Contains id to facilitate joining with other files.

- train_scraped.csv
  - Additional engineered features parsed from the original scrape for a large subset of rows; keyed by id for a clean join:
    - id
    - Date_of_journey, Airline, Flight_code, Class, Source, Destination
    - dep_time_hhmm, arr_time_hhmm: Exact clock times (HH:MM).
    - dep_minutes, arr_minutes: Minutes-from-midnight.
    - Departure_bucket, Arrival_bucket: Time-of-day buckets derived from exact times.
    - Total_stops: Normalized stops indicator.
    - duration_minutes: Duration in minutes.
    - overnight_flag: 1 if arrival is next day relative to departure clock time, else 0.
  - Note: The original scrape’s price field is intentionally removed to avoid leakage.

- test_scraped.csv
  - Same feature schema as train_scraped.csv (no labels), keyed by id.

- sample_submission.csv
  - Example of a valid submission with columns id,Fare.

Train/Test split design
- The split is forward in time by Date_of_journey to reflect real-world generalization to future journey dates. The last portion of unique journey dates is used for test. There is no overlap of (Flight_code, Date_of_journey) between train and test.
- Use id to merge cleaned and scraped tables. Not every id necessarily appears in the scraped table; when present, these features provide additional signal. Models should remain robust to missing auxiliary features after join.

Task and expectations
- This is a tabular regression problem. You are encouraged to:
  - Perform data processing and feature engineering (e.g., route features, categorical encodings, time-of-day and cyclic time features, interactions like Class×Stops or Airline×Route, log transforms of duration, etc.).
  - Combine train_cleaned with train_scraped via id for richer features.
  - Train strong regressors (e.g., gradient boosting, tree-based models, linear models with regularization, or deep tabular approaches).
  - Carefully validate and calibrate predictions to handle heavy-tailed prices.

Submission format
- Submit a CSV file with exactly these columns and header:
  - id: Integer identifiers that exactly match the ids provided in test_cleaned.csv.
  - Fare: Your predicted fare (positive numeric).
- Each id must appear exactly once. No extra or missing ids. All values must be finite numbers.

Evaluation metric
- Root Mean Squared Logarithmic Error (RMSLE) on Fare.
- Computed as the square root of the mean squared difference between log1p of the true and predicted fares. This treats relative errors more fairly across the wide price range and reduces the undue influence of rare high fares.

Rules and guidance
- Use only the provided files for training and prediction. External data or manual labels are not allowed.
- Do not attempt to infer labels from file names or text patterns; any price field from the original scrape is not present here by design.
- Handle categorical cardinality thoughtfully (e.g., target/cat encoding, regularization). Ensure numerical stability (e.g., avoid producing zeros/negatives for Fare predictions when using log transforms).

Tips to get started
- Start by training a baseline model on train_cleaned.csv using one-hot or target encoding for categorical variables and log-transforming Fare during training.
- Enhance with features from train_scraped.csv (exact times, duration_minutes, overnight_flag). Consider route = Source–Destination, day-of-week, time-of-day cyclic encodings, class and stops interactions, and per-airline or per-flight-code effects with regularization.
- Validate with a time-based split aligned to Date_of_journey to better estimate generalization to the provided test set.

Good luck, and happy modeling!
