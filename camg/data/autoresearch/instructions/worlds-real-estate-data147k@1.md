# OpenMLE-fast task

Task ID: `worlds-real-estate-data147k@1`

Native metric: `RealEstatePricePerM2Metrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3879 bytes)
- `data/sample_submission.csv` (637432 bytes); columns: ["id", "price_per_m2"]
- `data/test.csv` (4244319 bytes); columns: ["id", "title", "country", "location", "building_construction_year", "building_total_floors", "apartment_floor", "apartment_rooms", "apartment_bedrooms", "apartment_bathrooms", "apartment_total_area", "apartment_total_area_sqm", "apartment_living_area"]
- `data/train.csv` (18836428 bytes); columns: ["id", "title", "country", "location", "building_construction_year", "building_total_floors", "apartment_floor", "apartment_rooms", "apartment_bedrooms", "apartment_bathrooms", "apartment_total_area", "apartment_total_area_sqm", "apartment_living_area", "price_per_m2"]

## Public description

Global Price-per-m² Estimation from Multimodal Real Estate Listings

Problem
Participants must predict the price per square meter (price_per_m2) for international real estate listings using tabular and textual features. Each row corresponds to a property listed worldwide with heterogeneous attributes (country, building specs, number of rooms, free-text title/location, etc.).

Target
- price_per_m2 = price_in_USD / apartment_total_area_sqm
  Note: price_in_USD is not provided in the final train/test files. The target is provided only in train.csv.

Files
- train.csv: Training data with features and the target column price_per_m2.
- test.csv: Test data with the same feature schema as train.csv (except the target is omitted) plus an id column.
- sample_submission.csv: Example submission with columns [id, price_per_m2].

Data description (columns)
- id: Unique identifier for each row.
- title: Listing title (free text; multilingual).
- country: Country name (categorical).
- location: Free-text location string (city/region hierarchy; multilingual).
- building_construction_year: Year the building was constructed (numeric; may be missing).
- building_total_floors: Total floors in the building (numeric; may be missing).
- apartment_floor: Floor number of the apartment (numeric; may be missing).
- apartment_rooms: Number of rooms (numeric; may be missing).
- apartment_bedrooms: Number of bedrooms (numeric; may be missing).
- apartment_bathrooms: Number of bathrooms (numeric; may be missing).
- apartment_total_area: Original area string as provided in the listing (e.g., "120 m²", "65 m2", "25 sqm").
- apartment_total_area_sqm: Parsed numeric total area in square meters (float).
- apartment_living_area: Original living-area string if available (often missing; provided for completeness).

Columns intentionally excluded
- price_in_USD (raw price) and any image/url fields are excluded to avoid leakage and keep the task tabular/text-only.

Train/test split
- Listings are filtered to only those with valid, positive price and a successfully parsed, positive apartment_total_area.
- A single deterministic split is provided, approximately 80% train / 20% test.
- The split is group-aware by a URL-equivalent identifier to avoid duplicate leakage and is stratified by country so countries are represented in both sets when feasible.
- Countries with very few rows may not appear in the test set; the evaluation averages only over countries that appear in test.

Evaluation: Country-balanced RMSLE
- For each country c present in the test set, compute
    RMSLE_c = sqrt( mean( [log(1 + y_pred_i_clipped) − log(1 + y_true_i)]^2 ) over i in country c )
  where y_pred_i_clipped = max(y_pred_i, 0) to ensure numerical stability.
- The final score is the unweighted average of RMSLE_c across all countries present in the test set. Lower is better.
- Why this metric: RMSLE stabilizes heavy-tailed price distributions and the per-country averaging prevents overrepresented countries from dominating the score.

Submission format
- CSV with exactly two columns:
  - id
  - price_per_m2
- The id values must exactly match those in test.csv (order does not matter). Predictions must be finite numbers.

Recommended modeling directions
- Robust preprocessing for numeric fields with missingness indicators.
- Careful parsing/cleaning of area strings (units like m², m2, ㎡, sq m, sqm) and general text normalization.
- Feature engineering from title and location (character/word n-grams, embeddings).
- Categorical encoding for country; optional derivation of region tokens from location.
- Models such as gradient boosting, regularized linear models, or neural approaches over mixed tabular + text features.

Files produced by prepare.py
- train.csv
- test.csv
- sample_submission.csv

Good luck and have fun building robust, multilingual price-per-m² estimators!
