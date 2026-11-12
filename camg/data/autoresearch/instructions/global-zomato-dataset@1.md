# OpenMLE-fast task

Task ID: `global-zomato-dataset@1`

Native metric: `ZomatoRatingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3239 bytes)
- `data/sample_submission.csv` (17394 bytes); columns: ["Id", "Aggregate rating"]
- `data/test.csv` (284150 bytes); columns: ["Id", "Restaurant ID", "Restaurant Name", "City", "Address", "Locality", "Longitude", "Latitude", "Cuisines", "Average Cost for two", "Currency", "Has Table booking", "Has Online delivery", "Is delivering now", "Price range", "Votes"]
- `data/train.csv` (1162702 bytes); columns: ["Id", "Restaurant ID", "Restaurant Name", "City", "Address", "Locality", "Longitude", "Latitude", "Cuisines", "Average Cost for two", "Currency", "Has Table booking", "Has Online delivery", "Is delivering now", "Price range", "Aggregate rating", "Votes"]

## Public description

Global Zomato Rating Prediction Challenge

Problem statement
Predict the continuous Aggregate rating (0–5 scale) for restaurants using their observable attributes such as location, cuisines, pricing, delivery/booking options, and popularity signals.

Provided files
- train.csv: Training data with features and the target column Aggregate rating.
- test.csv: Test data with the same features as train.csv except the target is withheld.
- sample_submission.csv: A sample of the required submission format with deterministic mock predictions.

Target and features
- Target (train.csv only):
  - Aggregate rating (float in [0, 5])
- Features (present in both train.csv and test.csv):
  - Id (int): Unique row identifier used for submission matching
  - Restaurant ID (int)
  - Restaurant Name (string)
  - City (string)
  - Address (string)
  - Locality (string)
  - Longitude (float)
  - Latitude (float)
  - Cuisines (string; comma-separated multi-cuisine)
  - Average Cost for two (numeric)
  - Currency (string)
  - Has Table booking (string; Yes/No)
  - Has Online delivery (string; Yes/No)
  - Is delivering now (string; Yes/No)
  - Price range (int from 1 to 4)
  - Votes (int)

Notes
- Rating colour and Rating text are not included in the released data to avoid target leakage.
- Rows with Not rated (Aggregate rating = 0) are excluded from the split and evaluation to ensure a well-defined regression target.

Submission format
- A CSV file with exactly the following columns and header (order matters):
  - Id
  - Aggregate rating
- Each row corresponds to one row in test.csv (matched by Id). Predictions should be real numbers; any values outside [0, 5] will be clipped to this range during evaluation.

Evaluation metric
- Root Mean Squared Error (RMSE) between your predictions and the ground truth Aggregate rating on the test set.
- Implementation details:
  - Submissions are validated to match all and only the Id values from test.csv.
  - If duplicate Ids appear in a submission, they are averaged before scoring.
  - Predictions are coerced to float, checked for NaN/Inf, and clipped to [0, 5] to ensure stable scoring.

Train/test split
- A single deterministic train/test split is provided. The split preserves the overall rating distribution via stratification over rating buckets. The test labels are withheld and used only for scoring.

Recommended approaches
- Data processing: handle missing values (e.g., Cuisines), normalize monetary features (per-currency or per-city), encode high-cardinality categoricals (City, Locality, Cuisines), and use geospatial signals (Latitude/Longitude).
- Feature engineering: multi-hot or target encoding for cuisines; interaction features among price, delivery options, and city; chain detection from Restaurant Name; geohash or clustering.
- Models: tree ensembles (e.g., Gradient Boosting, Random Forest, CatBoost, LightGBM, XGBoost), linear models with robust encoders, or neural models with text embeddings.
- Evaluation: use cross-validation on train.csv to select models; the public leaderboard is based on the provided test.csv.

File naming
- Final data files: train.csv, test.csv, sample_submission.csv.
- Do not include any file paths in your submission or features.
