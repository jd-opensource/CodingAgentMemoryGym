# OpenMLE-fast task

Task ID: `new-york-dataset@2`

Native metric: `NewYorkLicenseStatusMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2672 bytes)
- `data/sample_submission.csv` (96186 bytes); columns: ["id", "license_status"]
- `data/test.csv` (837900 bytes); columns: ["id", "name", "host_id", "host_name", "neighbourhood_group", "neighbourhood", "latitude", "longitude", "room_type", "price", "minimum_nights", "number_of_reviews", "last_review", "reviews_per_month", "calculated_host_listings_count", "availability_365", "number_of_reviews_ltm", "rating", "bedrooms", "beds", "baths"]
- `data/train.csv` (3553713 bytes); columns: ["id", "name", "host_id", "host_name", "neighbourhood_group", "neighbourhood", "latitude", "longitude", "room_type", "price", "minimum_nights", "number_of_reviews", "last_review", "reviews_per_month", "calculated_host_listings_count", "availability_365", "number_of_reviews_ltm", "rating", "bedrooms", "beds", "baths", "license_status"]

## Public description

NYC Short-Term Rental License Status Classification

Problem statement
Predict the short-term rental license status of New York City Airbnb listings using listing metadata, text, and geospatial signals. Each listing belongs to exactly one of three classes:
- Registered: the listing has a valid short‑term rental registration code
- Exempt: the listing is exempt from registration requirements
- No License: the listing has no registration/license

You are given rich tabular features for each listing (location, neighborhood, room type, nights, reviews, host context, title text, etc.). Your task is to train a model that generalizes across hosts to classify each listing’s license status.

Files
- train.csv — training data with features and the target column license_status
- test.csv — test data with the same features as train.csv but without license_status
- sample_submission.csv — an example submission with valid label values

Target and features
- Target: license_status with values in {Registered, Exempt, No License} (present only in train.csv)
- Typical features include: id, name (short title), host_id, neighbourhood_group, neighbourhood, latitude, longitude, room_type, price, minimum_nights, number_of_reviews, last_review, reviews_per_month, calculated_host_listings_count, availability_365, number_of_reviews_ltm, rating, bedrooms, beds, baths
- Note: The license field is intentionally not included as a feature to prevent leakage. Hosts are disjoint between train and test to encourage generalization.

Submission format
- Submit a CSV with two columns and a header:
  - id: the listing identifier exactly matching test.csv
  - license_status: one of Registered, Exempt, or No License for each id

Evaluation
- Macro-averaged F1 score across the three classes (Registered, Exempt, No License)
  - F1 is computed per class and averaged with equal weight across classes
  - This metric rewards balanced performance across all classes, not just the majority

Tips and considerations
- The data contains mixed types: categorical, numeric, text (name), dates (last_review), and geospatial features (latitude/longitude). Sensible preprocessing, encoding, and feature engineering will be important.
- Class imbalance is present. Class weighting, focal losses, resampling, and threshold tuning may help.
- Useful engineered signals may include: geohash/hex binning, distances to landmarks/business districts, text length and keyword flags, review recency, host activity, and interactions with room type and minimum nights.
- The split is host-disjoint; avoid modeling choices that rely on memorizing host-specific artifacts that won’t generalize.
