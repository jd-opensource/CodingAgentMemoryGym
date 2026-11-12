# OpenMLE-fast task

Task ID: `perth-house-prices@1`

Native metric: `PerthHousePriceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4062 bytes)
- `data/sample_submission.csv` (263570 bytes); columns: ["Id", "PRICE"]
- `data/test.csv` (1661105 bytes); columns: ["Id", "SUBURB", "BEDROOMS", "BATHROOMS", "GARAGE", "LAND_AREA", "FLOOR_AREA", "BUILD_YEAR", "CBD_DIST", "NEAREST_STN", "NEAREST_STN_DIST", "DATE_SOLD", "POSTCODE", "LATITUDE", "LONGITUDE", "NEAREST_SCH", "NEAREST_SCH_DIST", "NEAREST_SCH_RANK", "SALE_YEAR"]
- `data/train.csv` (3808601 bytes); columns: ["Id", "SUBURB", "PRICE", "BEDROOMS", "BATHROOMS", "GARAGE", "LAND_AREA", "FLOOR_AREA", "BUILD_YEAR", "CBD_DIST", "NEAREST_STN", "NEAREST_STN_DIST", "DATE_SOLD", "POSTCODE", "LATITUDE", "LONGITUDE", "NEAREST_SCH", "NEAREST_SCH_DIST", "NEAREST_SCH_RANK", "SALE_YEAR"]

## Public description

Perth House Price Prediction (time-aware geospatial tabular regression)

Background
- This competition uses a real-world tabular dataset of residential sales across the Perth metropolitan area. Each record describes a property’s structural attributes (bedrooms, bathrooms, garage spaces, land and floor areas, build year), location (suburb, postcode, latitude/longitude, nearest station and school, distances), and market timing (month-year of sale). The goal is to predict the sale price.

Problem statement
- Build a model that predicts the sale PRICE for properties in the test set using the provided features. The evaluation is intentionally time-aware to mirror deployment conditions and avoid trivial memorization: training examples come from older years, while test examples are from later years.

Files provided
- train.csv: Features plus target PRICE and an Id column for each training row.
- test.csv: Features plus an Id column for each test row (no PRICE).
- sample_submission.csv: A valid example of the required submission format with random but realistic positive prices. Use this as a template only.

Target and features
- Target: PRICE (positive numeric, Australian dollars).
- Key feature groups:
  - Structural: BEDROOMS, BATHROOMS, GARAGE, LAND_AREA, FLOOR_AREA, BUILD_YEAR.
  - Location: SUBURB, POSTCODE, LATITUDE, LONGITUDE, CBD_DIST, NEAREST_STN, NEAREST_STN_DIST, NEAREST_SCH, NEAREST_SCH_DIST, NEAREST_SCH_RANK.
  - Time: DATE_SOLD (format mm-YYYY). A parsed SALE_YEAR feature is included for convenience.
- ADDRESS is intentionally excluded to prevent label leakage.

Train/test split and integrity
- Train rows come from sales up to and including 2018. Test rows come from sales in 2019–2020. Properties whose identifiers overlapped across these periods were excluded from the test set to further prevent leakage.
- Each row has a unique Id; train and test Ids are disjoint.

Data considerations (important for strong solutions)
- Missing values: Some columns (e.g., BUILD_YEAR, GARAGE, NEAREST_SCH_RANK) contain missing entries or unranked schools. Use principled imputation and consider missing-indicator features.
- Heavy tails and outliers: PRICE is heavy-tailed; LAND_AREA may contain extreme values. Robust preprocessing (e.g., capping/winsorizing) can help.
- Categorical breadth: SUBURB, NEAREST_SCH, and NEAREST_STN have many levels. Use appropriate encodings (e.g., one-hot, target-independent ordinal/frequency) and regularization.
- Geospatial modeling: LATITUDE/LONGITUDE and distance features enable spatial feature engineering (e.g., spatial smoothing, distance-to-CBD or coastline, clustering).
- Temporal drift: The market evolves over time; consider time-aware feature engineering from DATE_SOLD (e.g., month-of-year seasonality, property age at sale computed from BUILD_YEAR and SALE_YEAR).

Evaluation metric
- Root Mean Squared Logarithmic Error (RMSLE) on PRICE.
  - Motivation: Home values are positive and multiplicative in nature. RMSLE evaluates errors on a relative (percentage-like) scale, balances under- and over-estimation, and is robust to high-end outliers.
  - Requirements for predictions: All predicted prices must be strictly positive, finite numeric values.

Submission format
- Submit a CSV file named submission.csv with exactly two columns:
  - Id: integer identifiers matching those in test.csv.
  - PRICE: your predicted sale price for each Id.
- Ids must match the test set exactly (no duplicates, no missing/extra Ids). Order does not matter; scoring aligns by Id.

Modeling guidance (optional)
- Solid baselines include gradient boosted decision trees or regularized linear models with careful preprocessing. Consider feature interactions, non-linearities, and geospatial/temporal engineering.
- Cross-validation should respect time (e.g., forward-chaining or year-based splits) to avoid optimistic estimates.

Goal
- Achieve the lowest RMSLE by building models that generalize across space and time, leveraging robust preprocessing, feature engineering, and sound training practices.
