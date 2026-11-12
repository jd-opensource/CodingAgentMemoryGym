# OpenMLE-fast task

Task ID: `worlds-real-estate-data147k@2`

Native metric: `CityPricePerM2Metrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3312 bytes)
- `data/listing_test.csv` (3290819 bytes); columns: ["title", "country", "location", "building_construction_year", "building_total_floors", "apartment_floor", "apartment_rooms", "apartment_bedrooms", "apartment_bathrooms", "apartment_total_area", "apartment_living_area", "cell_id"]
- `data/listing_train.csv` (16012475 bytes); columns: ["title", "country", "location", "building_construction_year", "building_total_floors", "apartment_floor", "apartment_rooms", "apartment_bedrooms", "apartment_bathrooms", "apartment_total_area", "apartment_living_area", "price_in_USD", "cell_id"]
- `data/sample_submission.csv` (4911 bytes); columns: ["cell_id", "median_ppm2"]
- `data/test.csv` (122993 bytes); columns: ["cell_id", "country", "n_listings", "title_len_median", "title_len_mean", "title_len_std", "title_len_q25", "title_len_q75", "title_len_iqr", "title_len_min", "title_len_max", "title_words_median", "title_words_mean", "title_words_std", "title_words_q25", "title_words_q75", "title_words_iqr", "title_words_min", "title_words_max", "location_len_median", "location_len_mean", "location_len_std", "location_len_q25", "location_len_q75", "location_len_iqr", "location_len_min", "location_len_max", "location_words_median", "location_words_mean", "location_words_std", "location_words_q25", "location_words_q75", "location_words_iqr", "location_words_min", "location_words_max", "building_construction_year_median", "building_construction_year_mean", "building_construction_year_std", "building_construction_year_q25", "building_construction_year_q75", "building_construction_year_iqr", "building_construction_year_min", "building_construction_year_max", "building_construction_year_missing_frac", "building_total_floors_median", "building_total_floors_mean", "building_total_floors_std", "building_total_floors_q25", "building_total_floors_q75", "building_total_floors_iqr", "building_total_floors_min", "building_total_floors_max", "building_total_floors_missing_frac", "apartment_floor_median", "apartment_floor_mean", "apartment_floor_std", "apartment_floor_q25", "apartment_floor_q75", "apartment_floor_iqr", "apartment_floor_min", "apartment_floor_max", "apartment_floor_missing_frac", "apartment_rooms_median", "apartment_rooms_mean", "apartment_rooms_std", "apartment_rooms_q25", "apartment_rooms_q75", "apartment_rooms_iqr", "apartment_rooms_min", "apartment_rooms_max", "apartment_rooms_missing_frac", "apartment_bedrooms_median", "apartment_bedrooms_mean", "apartment_bedrooms_std", "apartment_bedrooms_q25", "apartment_bedrooms_q75", "apartment_bedrooms_iqr", "apartment_bedrooms_min", "apartment_bedrooms_max", "apartment_bedrooms_missing_frac", "apartment_bathrooms_median", "apartment_bathrooms_mean", "apartment_bathrooms_std", "apartment_bathrooms_q25", "apartment_bathrooms_q75", "apartment_bathrooms_iqr", "apartment_bathrooms_min", "apartment_bathrooms_max", "apartment_bathrooms_missing_frac", "apartment_total_area_num_median", "apartment_total_area_num_mean", "apartment_total_area_num_std", "apartment_total_area_num_q25", "apartment_total_area_num_q75", "apartment_total_area_num_iqr", "apartment_total_area_num_min", "apartment_total_area_num_max", "apartment_total_area_num_missing_frac", "apartment_living_area_num_median", "apartment_living_area_num_mean", "apartment_living_area_num_std", "apartment_living_area_num_q25", "apartment_living_area_num_q75", "apartment_living_area_num_iqr", "apartment_living_area_num_min", "apartment_living_area_num_max", "apartment_living_area_num_missing_frac"]
- `data/train.csv` (496264 bytes); columns: ["cell_id", "country", "n_listings", "title_len_median", "title_len_mean", "title_len_std", "title_len_q25", "title_len_q75", "title_len_iqr", "title_len_min", "title_len_max", "title_words_median", "title_words_mean", "title_words_std", "title_words_q25", "title_words_q75", "title_words_iqr", "title_words_min", "title_words_max", "location_len_median", "location_len_mean", "location_len_std", "location_len_q25", "location_len_q75", "location_len_iqr", "location_len_min", "location_len_max", "location_words_median", "location_words_mean", "location_words_std", "location_words_q25", "location_words_q75", "location_words_iqr", "location_words_min", "location_words_max", "building_construction_year_median", "building_construction_year_mean", "building_construction_year_std", "building_construction_year_q25", "building_construction_year_q75", "building_construction_year_iqr", "building_construction_year_min", "building_construction_year_max", "building_construction_year_missing_frac", "building_total_floors_median", "building_total_floors_mean", "building_total_floors_std", "building_total_floors_q25", "building_total_floors_q75", "building_total_floors_iqr", "building_total_floors_min", "building_total_floors_max", "building_total_floors_missing_frac", "apartment_floor_median", "apartment_floor_mean", "apartment_floor_std", "apartment_floor_q25", "apartment_floor_q75", "apartment_floor_iqr", "apartment_floor_min", "apartment_floor_max", "apartment_floor_missing_frac", "apartment_rooms_median", "apartment_rooms_mean", "apartment_rooms_std", "apartment_rooms_q25", "apartment_rooms_q75", "apartment_rooms_iqr", "apartment_rooms_min", "apartment_rooms_max", "apartment_rooms_missing_frac", "apartment_bedrooms_median", "apartment_bedrooms_mean", "apartment_bedrooms_std", "apartment_bedrooms_q25", "apartment_bedrooms_q75", "apartment_bedrooms_iqr", "apartment_bedrooms_min", "apartment_bedrooms_max", "apartment_bedrooms_missing_frac", "apartment_bathrooms_median", "apartment_bathrooms_mean", "apartment_bathrooms_std", "apartment_bathrooms_q25", "apartment_bathrooms_q75", "apartment_bathrooms_iqr", "apartment_bathrooms_min", "apartment_bathrooms_max", "apartment_bathrooms_missing_frac", "apartment_total_area_num_median", "apartment_total_area_num_mean", "apartment_total_area_num_std", "apartment_total_area_num_q25", "apartment_total_area_num_q75", "apartment_total_area_num_iqr", "apartment_total_area_num_min", "apartment_total_area_num_max", "apartment_total_area_num_missing_frac", "apartment_living_area_num_median", "apartment_living_area_num_mean", "apartment_living_area_num_std", "apartment_living_area_num_q25", "apartment_living_area_num_q75", "apartment_living_area_num_iqr", "apartment_living_area_num_min", "apartment_living_area_num_max", "apartment_living_area_num_missing_frac", "median_ppm2"]

## Public description

City-level Price-per-m² Forecasting (Leave-City-Out Generalization)

Problem statement
You are given a global collection of property listings. The task is to predict the median price-per-square-meter (USD/m²) for each target city cell in the test set. A city cell is defined by the combination of country and the top-level place extracted from the location field (the first comma-separated token). Models must generalize to unseen city cells: train and test contain disjoint sets of cells.

Files provided
- train.csv: Cell-level table with features and the target median_ppm2 (median price-per-m²).
- test.csv: Cell-level table with the same features but without the target.
- listing_train.csv: Listing-level records for the training cells (with price_in_USD). This allows feature engineering beyond the provided aggregates.
- listing_test.csv: Listing-level records for the test cells (price is removed to prevent leakage).
- sample_submission.csv: Template for submissions.

Target and features
- Target: median_ppm2, the median of price_in_USD / apartment_total_area (in m²) across listings within a cell.
- Features in train.csv/test.csv include:
  - country and n_listings
  - Aggregated numeric attributes (median/mean/std/quantiles/IQR/min/max) and missingness fraction for: building_construction_year, building_total_floors, apartment_floor, apartment_rooms, apartment_bedrooms, apartment_bathrooms, apartment_total_area, apartment_living_area
  - Simple text descriptors: per-cell statistics of title and location lengths (characters and words)
- listing_train.csv/listing_test.csv contain the raw listing-level counterparts to support custom aggregation or text modeling. The cell_id column links listings to their cell.

Submission format
- CSV with two columns in this order: cell_id, median_ppm2
- Include exactly one row per cell_id in test.csv
- Values must be numeric and finite (negatives are allowed but will be clipped to zero during scoring).

Evaluation
- Metric: Weighted Absolute Percentage Error (WAPE) across test cells
  WAPE = sum_c |pred_c - true_c| / sum_c true_c
- Properties: scale-aware, robust to varying city price levels, and straightforward to interpret as a percentage error. Using medians for ground truth reduces sensitivity to outliers.

Data split and guarantees
- Train and test cells are disjoint (leave-cell-out).
- Each test cell has at least 10 listings; training cells also satisfy this threshold.
- All files are anonymized via cell_id to avoid label leakage. No file paths are included in any CSV.

Recommended approach (non-exhaustive)
- Aggregate listing-level features to the cell level using robust statistics; combine with textual features (e.g., TF-IDF on title/location pooled per cell).
- Train regression models (e.g., gradient boosting, regularized linear models, tree-based ensembles, or neural architectures) to predict median_ppm2 for unseen cells.
- Pay attention to missingness patterns and distribution shift between cities and countries.

Final files
- train.csv
- test.csv
- sample_submission.csv
- listing_train.csv
- listing_test.csv

Notes
- This is a challenging leave-city-out generalization task using real-world, multilingual listings. Strong solutions will blend careful preprocessing, aggregation strategies, and robust modeling.
