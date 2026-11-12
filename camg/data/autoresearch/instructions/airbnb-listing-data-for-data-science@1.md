# OpenMLE-fast task

Task ID: `airbnb-listing-data-for-data-science@1`

Native metric: `AirbnbPriceRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3485 bytes)
- `data/sample_submission.csv` (6442 bytes); columns: ["id", "price_usd"]
- `data/test.csv` (28736 bytes); columns: ["id", "name", "details", "date_text", "month_start", "trip_length_days", "rating", "rating_count", "beds_num", "has_queen", "has_king", "has_double", "distance_km", "segment"]
- `data/train.csv` (127950 bytes); columns: ["id", "name", "details", "date_text", "month_start", "trip_length_days", "rating", "rating_count", "beds_num", "has_queen", "has_king", "has_double", "distance_km", "segment", "price_usd"]

## Public description

Airbnb Multi-Segment Nightly Price Prediction

Problem statement
Build a model to predict the nightly price (USD) of Airbnb listings given heterogeneous listing metadata spanning three market segments: general stays, desert experiences, and luxe villas. Listings vary widely in presentation (text fields, ratings, distances) and price scale. Your goal is to generalize across segments and minimize multiplicative error on the target price.

Files
- train.csv: Training data with features and the target column price_usd.
- test.csv: Test data with the same features but without price_usd.
- sample_submission.csv: A sample file showing the required submission format (id, price_usd).

Target
- price_usd: Nightly price in USD (non-negative float). Present only in train.csv.

Features (unified schema)
Each row corresponds to a listing snapshot, merged from multiple raw sources and normalized. Columns in train.csv and test.csv:
- id: Unique identifier for the row. Use this to align predictions to rows in test.csv.
- name: Listing name/title text, standardized across sources.
- details: Secondary descriptive text (amenities, short description). May be empty.
- date_text: Unstructured date window text (e.g., "Jun 11 - 16", "May 1 - 29"). Normalized dash characters.
- month_start: Month name/abbreviation parsed from date_text when available (e.g., "Jun", "May"). Empty if not parsable.
- trip_length_days: Integer trip length estimated from the date_text when start/end days are both present; otherwise empty.
- rating: Average rating (float 0–5) when available; empty otherwise.
- rating_count: Number of reviews when available; empty otherwise.
- beds_num: Number of beds parsed from bed text when available; empty otherwise.
- has_queen, has_king, has_double: Binary indicators inferred from bed text when available (0/1); empty otherwise.
- distance_km: Distance in kilometers for luxe listings parsed from distance text; empty otherwise.
- segment: Categorical segment label: one of {general, desert, luxe}.

Evaluation
- Metric: Root Mean Squared Logarithmic Error (RMSLE) on price_usd.
  - Let y be the true price and y_hat be your prediction (both must be non-negative). The score is sqrt(mean((log1p(y_hat) - log1p(y))^2)).
  - Submissions with negative, NaN, or infinite predictions are invalid.

Submission format
- CSV with two columns and a header: id, price_usd
- One row per id in test.csv.

Train/test split
- A single, fixed 80/20 train/test split is provided. The split is stratified by segment and price bands and groups duplicate listings by name to reduce leakage. Use the provided files as-is.

Modeling tips
- The data intentionally combines three segments with different schema richness (e.g., ratings mainly in general and desert, distances in luxe). Robust feature engineering on text (name, details, date_text), careful numeric parsing, and handling of missingness are key.
- Consider text vectorization (word/character n-grams) combined with tree-based models or linear models; add simple numeric features (trip_length_days, rating, rating_count, beds_num, distance_km) and one-hot encode the segment.
- The target distribution is heavy-tailed; RMSLE emphasizes relative error and reduces outlier dominance.

What is allowed
- Any modeling approach that uses only the provided training data. External data or labels are not permitted.

Deliverables you will produce
- A CSV file following the submission format above.

Good luck and happy modeling!
