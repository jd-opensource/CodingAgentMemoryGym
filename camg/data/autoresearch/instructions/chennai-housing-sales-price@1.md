# OpenMLE-fast task

Task ID: `chennai-housing-sales-price@1`

Native metric: `ChennaiHousingSalesPriceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3106 bytes)
- `data/sample_submission.csv` (35639 bytes); columns: ["Id", "SALES_PRICE"]
- `data/test.csv` (156003 bytes); columns: ["Id", "AREA", "INT_SQFT", "DATE_SALE", "DIST_MAINROAD", "N_BEDROOM", "N_BATHROOM", "N_ROOM", "SALE_COND", "PARK_FACIL", "DATE_BUILD", "BUILDTYPE", "UTILITY_AVAIL", "STREET", "MZZONE", "QS_ROOMS", "QS_BATHROOM", "QS_BEDROOM", "QS_OVERALL"]
- `data/train.csv` (679620 bytes); columns: ["Id", "AREA", "INT_SQFT", "DATE_SALE", "DIST_MAINROAD", "N_BEDROOM", "N_BATHROOM", "N_ROOM", "SALE_COND", "PARK_FACIL", "DATE_BUILD", "BUILDTYPE", "UTILITY_AVAIL", "STREET", "MZZONE", "QS_ROOMS", "QS_BATHROOM", "QS_BEDROOM", "QS_OVERALL", "SALES_PRICE"]

## Public description

Chennai Housing Sales Price – Time-aware Tabular Regression

Problem statement
Build a machine learning model to predict the sale price of residential properties in Chennai using tabular attributes such as area, square footage, street access, utilities, build type, rooms, and quality scores. The objective is to deliver robust generalization across time, avoiding label leakage and handling messy real-world data.

Files provided
- train.csv: Training set containing features and the target column SALES_PRICE.
- test.csv: Test set containing the same features as train.csv except the target column.
- sample_submission.csv: Example submission file with the required format.

Target
- SALES_PRICE: Numeric sale price of the property.

Submission format
- A CSV file with exactly two columns: Id and SALES_PRICE.
- Id values must match the Ids in test.csv (no duplicates, no missing or extra Ids).
- SALES_PRICE must be numeric and finite for all rows.

Data description
The dataset includes 7,109 rows and 22 columns derived from Chennai residential transactions. Important columns include:
- Identifiers and core features: Id (derived from PRT_ID), AREA, INT_SQFT, DIST_MAINROAD, N_BEDROOM, N_BATHROOM, N_ROOM.
- Dates and temporal context: DATE_SALE (dd-mm-YYYY), DATE_BUILD (dd-mm-YYYY). Participants may derive YEAR_SALE, MONTH_SALE, and AGE at sale.
- Categorical attributes: SALE_COND, PARK_FACIL, BUILDTYPE, UTILITY_AVAIL, STREET, MZZONE.
- Quality scores: QS_ROOMS, QS_BATHROOM, QS_BEDROOM, QS_OVERALL.

To ensure fairness and avoid label leakage, columns directly derived from price are excluded from train/test features:
- REG_FEE and COMMIS are removed from train.csv and test.csv.

Known data quirks (intended to be handled by participants)
- Typos and variants in categorical values (e.g., area and street names), mixed encodings for utilities and build types.
- Missing values in some quality score columns and a few room counts.
- Wide price range and heteroscedasticity; log-transforming price during training may help.

Train/test split
- Time-aware split to evaluate temporal generalization.
- Train: transactions from 2004–2011.
- Test: transactions from 2012–2015.

Evaluation metric
- Root Mean Squared Error (RMSE) computed on log1p(SALES_PRICE).
Rationale: The price span is large; log RMSE captures relative error and reduces the impact of extreme values, yielding a fair and precise comparison.

Recommendations and constraints
- Perform robust data cleaning: parse dates (day-first format), canonicalize categorical typos, and impute missing values appropriately.
- Encode categorical features using target-independent methods (e.g., one-hot or frequency-based ordinal encoding).
- Avoid target leakage: do not engineer features based on the target or use any information from the test set.
- You may engineer features such as YEAR_SALE, MONTH_SALE, AGE at sale, and interactions.

Final deliverables
- Submit a CSV with columns [Id, SALES_PRICE] containing predictions for all rows in test.csv.
- The leaderboard score is the RMSE on log1p(SALES_PRICE) over the test set.
