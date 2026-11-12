# OpenMLE-fast task

Task ID: `airbnb-prices-in-european-cities@1`

Native metric: `AirbnbPricePredictionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3107 bytes)
- `data/sample_submission.csv` (250795 bytes); columns: ["id", "realSum"]
- `data/test.csv` (1902666 bytes); columns: ["room_type", "room_shared", "room_private", "person_capacity", "host_is_superhost", "multi", "biz", "cleanliness_rating", "guest_satisfaction_overall", "bedrooms", "dist", "metro_dist", "attr_index", "attr_index_norm", "rest_index", "rest_index_norm", "lng", "lat", "city", "is_weekend", "id"]
- `data/train.csv` (8374991 bytes); columns: ["realSum", "room_type", "room_shared", "room_private", "person_capacity", "host_is_superhost", "multi", "biz", "cleanliness_rating", "guest_satisfaction_overall", "bedrooms", "dist", "metro_dist", "attr_index", "attr_index_norm", "rest_index", "rest_index_norm", "lng", "lat", "city", "is_weekend", "id"]

## Public description

EuroAirbnb Price Prediction (Weekdays vs Weekends)

Problem statement
Predict the total listing price (realSum) for Airbnb listings across multiple European cities. Each row is a listing snapshot with attributes such as room type, capacity, host characteristics, cleanliness and satisfaction ratings, distance to city center and metro, geolocation, and indicators for weekday/weekend. Your model should generalize across cities and both weekday and weekend periods.

Files provided
- train.csv: Labeled training data with all features and the target column realSum.
- test.csv: Unlabeled test data with the same feature columns as train.csv (but without realSum).
- sample_submission.csv: Example submission file with the correct format and plausible random predictions.

Target
- realSum: Total price of the listing.

Features
The following columns are present (names may vary slightly depending on original data), including but not limited to:
- Categorical / indicator: room_type, room_shared, room_private, host_is_superhost, multi, biz, city, is_weekend
- Numeric: person_capacity, cleanliness_rating, guest_satisfaction_overall, bedrooms, dist, metro_dist, attr_index, attr_index_norm, rest_index, rest_index_norm, lng, lat

Notes
- city and is_weekend are derived from the source of each record (city extracted from file name; is_weekend indicates weekend vs weekday). They are included as standard features for modeling temporal and spatial effects.
- Some datasets may contain a leading unnamed index column; this has been removed.

Evaluation
- Metric: Root Mean Squared Logarithmic Error (RMSLE)
  - Definition: sqrt( mean( (log1p(y_pred) - log1p(y_true))^2 ) )
  - Rationale: Prices are typically right-skewed, and multiplicative errors are more meaningful than absolute errors. RMSLE reduces the undue influence of high-price outliers while rewarding accurate relative predictions across the distribution.
  - Constraints: Predictions must be non-negative finite numbers. The scorer will validate submission format strictly and compute RMSLE after aligning by id.

Submission format
- A CSV with exactly two columns: id, realSum
- id must match the ids in test.csv
- realSum must be non-negative finite numeric values (floats or ints)

Rules and tips
- You are free to use any features present in train/test and to engineer new features from them (e.g., encodings, interactions, spatial clusters, log transforms), but do not use any external data with labels.
- Handle mixed data types: booleans, categoricals (room_type, city), continuous (distances, ratings), and geospatial (lng, lat).
- Consider target transformation (e.g., modeling log1p(realSum)) and robust validation to avoid overfitting to specific cities or periods. Interactions like city×is_weekend or room_type×is_weekend can be useful.
- The split preserves diversity across cities, room types, and periods to ensure generalization is required.

Data scale
- All available records across the covered European cities and both weekday and weekend periods are included. Runtime constraints are not enforced; use the full dataset.
