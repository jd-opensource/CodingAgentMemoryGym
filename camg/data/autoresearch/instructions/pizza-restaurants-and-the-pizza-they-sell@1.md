# OpenMLE-fast task

Task ID: `pizza-restaurants-and-the-pizza-they-sell@1`

Native metric: `PizzaPriceRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3581 bytes)
- `data/sample_submission.csv` (56156 bytes); columns: ["row_id", "price"]
- `data/test.csv` (997740 bytes); columns: ["row_id", "address", "categories", "city", "country", "dateAdded", "dateUpdated", "id", "keys", "latitude", "longitude", "menuPageURL", "menus.currency", "menus.dateSeen", "menus.description", "menus.name", "name", "postalCode", "priceRangeCurrency", "priceRangeMax", "priceRangeMin", "primaryCategories", "province"]
- `data/train.csv` (4188943 bytes); columns: ["row_id", "address", "categories", "city", "country", "dateAdded", "dateUpdated", "id", "keys", "latitude", "longitude", "menuPageURL", "menus.currency", "menus.dateSeen", "menus.description", "menus.name", "name", "postalCode", "priceRangeCurrency", "priceRangeMax", "priceRangeMin", "primaryCategories", "province", "price"]

## Public description

Pizza Price Prediction: NLP + Tabular + Geospatial Regression

Problem statement
Given a pizza menu item and its associated restaurant/location metadata, predict the item’s listed menu price (in USD). Menu items include textual names and descriptions (e.g., "Large Pepperoni", "BBQ Chicken 12-inch"), alongside business, geographic, and price-range information for the restaurant.

Why this is interesting
- Prices vary widely across styles, sizes, toppings, and cities. Predicting them requires fusing noisy text features with high-cardinality categorical and geospatial signals.
- The task is realistic (true menu prices), sizable, and non-trivial: it favors careful data processing, feature engineering, and robust modeling.

Data description
The data is preprocessed from two public pizza menu datasets into a single, harmonized table. Each row in the final files corresponds to a unique pizza menu item at a restaurant. All prices are in USD and strictly positive.

Key columns (non-exhaustive):
- row_id: unique identifier for each menu item row.
- Text: menus.name, menus.description
- Business: name (restaurant name), categories, primaryCategories
- Location: address, city, province, postalCode, country, latitude, longitude
- Web/meta: keys, menuPageURL, dateAdded, dateUpdated (if available)
- Establishment price anchors: priceRangeCurrency, priceRangeMin, priceRangeMax
- Target (train only): price — the label to predict; derived from menus.amountMin/menus.amountMax where available and filtered to USD.

Notes
- Rows were deduplicated by a stable key (including restaurant and menu name) and consolidated if duplicate records reported different prices.
- Data was split by restaurant group to prevent leakage. All items from the same restaurant (name + city + province + postalCode) are entirely in train or test, never both.
- Direct price fields used to construct the target (menus.amountMin, menus.amountMax) are removed from train/test features to avoid leakage.

Files provided
- train.csv: feature columns plus the target column price, and row_id.
- test.csv: identical feature columns as train.csv (excluding price), and row_id.
- sample_submission.csv: a valid example with columns [row_id, price].

Do not rely on the presence of any one feature; the schema includes heterogeneous, occasionally missing columns by design. Robust preprocessing is encouraged.

Evaluation
- Metric: RMSLE (root mean squared logarithmic error) on price.
  - Definition: RMSLE = sqrt(mean((log1p(y_pred) − log1p(y_true))^2)).
  - Requirements: Predictions must be non-negative. The metric is computed on the full test set.
  - Rationale: Emphasizes relative error and reduces undue influence from very expensive outliers while rewarding proportional accuracy.

Train/test split
- Train/test are pre-split by restaurant group to ensure generalization to unseen restaurants. There is no official validation split; participants may create their own CV (e.g., group-based) using the provided features.

Baseline guidance (non-binding)
- Start by cleaning text (lowercasing, punctuation normalization) and extracting size/topping signals from menus.name/menus.description.
- Combine with categorical encodings for city/province/restaurant and continuous geospatial features (latitude/longitude).
- Tree-based models (e.g., gradient boosting) and models with text embeddings can perform well.

Submission format
- A CSV with exactly two columns: row_id, price
- One row per row_id present in test.csv.

Good luck, and enjoy building a robust, multimodal price prediction model!
