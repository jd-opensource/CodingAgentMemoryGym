# OpenMLE-fast task

Task ID: `perth-house-prices@2`

Native metric: `PerthHousePriceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3813 bytes)
- `data/sample_submission.csv` (260727 bytes); columns: ["ID", "LOG_REL_PRICE"]
- `data/test.csv` (1406499 bytes); columns: ["ID", "SUBURB", "POSTCODE", "BEDROOMS", "BATHROOMS", "GARAGE", "LAND_AREA", "FLOOR_AREA", "BUILD_YEAR", "CBD_DIST", "NEAREST_STN", "NEAREST_STN_DIST", "LATITUDE", "LONGITUDE", "NEAREST_SCH", "NEAREST_SCH_DIST", "NEAREST_SCH_RANK", "YEAR_SOLD", "SUBURB_YEAR_MEDIAN"]
- `data/train.csv` (3301516 bytes); columns: ["ID", "SUBURB", "POSTCODE", "BEDROOMS", "BATHROOMS", "GARAGE", "LAND_AREA", "FLOOR_AREA", "BUILD_YEAR", "CBD_DIST", "NEAREST_STN", "NEAREST_STN_DIST", "LATITUDE", "LONGITUDE", "NEAREST_SCH", "NEAREST_SCH_DIST", "NEAREST_SCH_RANK", "YEAR_SOLD", "SUBURB_YEAR_MEDIAN", "LOG_REL_PRICE"]

## Public description

Title: Perth Micro-Valuation: Price Uplift over Suburb-Year Baseline

Background
House prices vary substantially across suburbs and over time. Broad market trends and suburb-level effects can dominate absolute prices, making it hard to assess property-specific value drivers. In this competition, we anchor each sale to its local market baseline so participants focus on micro-valuation: predicting how much a specific property sells above or below the typical price for its suburb and sale year.

Problem Statement
Given tabular features describing a property sale in the Perth metropolitan area, predict the log-relative price uplift (LOG_REL_PRICE) compared to the median price for the same suburb and sale year. This targets percentage deviation from the local baseline and emphasizes structural and micro-location effects.

Data Description
- Train file (train.csv): rows up to and including sale year 2018. Contains all features and the label column LOG_REL_PRICE.
- Test file (test.csv): rows in sale years 2019–2020. Contains the same features but no labels.
- Sample submission (sample_submission.csv): a template with the required columns.

Key columns provided in both train and test:
- ID: unique identifier for each row (used in submissions).
- SUBURB, POSTCODE: categorical/suburb-level location.
- BEDROOMS, BATHROOMS, GARAGE: basic structural counts.
- LAND_AREA, FLOOR_AREA: size features (square meters).
- BUILD_YEAR: construction year.
- CBD_DIST: distance to Perth CBD (meters).
- NEAREST_STN, NEAREST_STN_DIST: nearest train station and its distance.
- LATITUDE, LONGITUDE: geocoordinates.
- NEAREST_SCH, NEAREST_SCH_DIST, NEAREST_SCH_RANK: nearest ATAR-applicable school, its distance, and ranking (may be missing if unranked).
- YEAR_SOLD: sale year extracted from the raw sale date.
- SUBURB_YEAR_MEDIAN: precomputed median price within each split for the corresponding (SUBURB, YEAR_SOLD) group. This baseline is computed strictly from train rows for train.csv and strictly from test rows for test.csv.

Label (train only):
- LOG_REL_PRICE = log(PRICE) − log(SUBURB_YEAR_MEDIAN).

Important notes
- The absolute price (PRICE) is not provided in the released train/test files; modeling targets the deviation from the local median baseline.
- ADDRESS and raw DATE_SOLD are removed to prevent any label leakage; YEAR_SOLD is provided instead.
- To avoid leakage across splits, addresses that appear in both train and test were removed from the test set.

Evaluation Metric
Submissions must contain two columns: ID and LOG_REL_PRICE. The score is the Root Mean Squared Error (RMSE) between the submitted LOG_REL_PRICE and the ground truth LOG_REL_PRICE for the test set. RMSE on the log-relative target emphasizes percentage deviations, is robust to outliers, and fairly evaluates micro-valuation performance independent of suburb-level and macro timing effects.

Submission Format
- Columns: ID, LOG_REL_PRICE
- ID values must exactly match those in test.csv.
- LOG_REL_PRICE must be finite numeric values (no NaN/Inf).

Recommended Approach
- Data processing: handle missing values (e.g., school rank), parse YEAR_SOLD, and consider winsorization for extreme areas/distances.
- Feature engineering: ratios (floor-to-land), interactions, spatial encodings, categorical encodings for high-cardinality variables (SUBURB, stations, schools), and temporal effects via YEAR_SOLD.
- Modeling: regularized regression, gradient boosting, or tabular neural models; consider geospatial features and non-linearities.
- Evaluation: cross-validation aware of YEAR_SOLD, and careful use of SUBURB_YEAR_MEDIAN as a baseline.

Files to use
- train.csv: training features and LOG_REL_PRICE label
- test.csv: test features and SUBURB_YEAR_MEDIAN baseline
- sample_submission.csv: template for submissions
