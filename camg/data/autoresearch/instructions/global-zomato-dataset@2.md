# OpenMLE-fast task

Task ID: `global-zomato-dataset@2`

Native metric: `ZomatoPricePredictionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2966 bytes)
- `data/sample_submission.csv` (25485 bytes); columns: ["Restaurant ID", "Average Cost for two"]
- `data/test.csv` (339774 bytes); columns: ["Restaurant ID", "Restaurant Name", "City", "Address", "Locality", "Longitude", "Latitude", "Cuisines", "Currency", "Has Table booking", "Has Online delivery", "Is delivering now", "Aggregate rating", "Votes"]
- `data/train.csv` (1440352 bytes); columns: ["Restaurant ID", "Restaurant Name", "City", "Address", "Locality", "Longitude", "Latitude", "Cuisines", "Average Cost for two", "Currency", "Has Table booking", "Has Online delivery", "Is delivering now", "Aggregate rating", "Votes"]

## Public description

Global Restaurant Price Prediction (Zomato)

Problem statement
Build a model that predicts a restaurant’s “Average Cost for two” (numeric) given its attributes. The dataset spans thousands of restaurants across many cities and currencies. Your model should generalize across geographies, cuisines, and service configurations and predict prices in the restaurant’s own currency.

Data description
Each row represents one restaurant. The provided competition files are:
- train.csv: feature columns plus the target column “Average Cost for two”.
- test.csv: the same feature columns as train.csv but without the target.
- sample_submission.csv: a submission template with example predictions for the test set.

Recommended features available in the files:
- Restaurant ID (identifier to be used in submissions)
- Restaurant Name
- City
- Locality
- Longitude, Latitude
- Cuisines (comma-separated multi-label)
- Currency
- Has Table booking, Has Online delivery, Is delivering now
- Aggregate rating
- Votes

Notes:
- The target column is “Average Cost for two”.
- Columns that trivially leak the target (e.g., “Price range”) have been removed.
- Textual fields are kept as-is to allow custom processing (tokenization, hashing, embeddings, etc.).

Submission format
- A CSV file with exactly two columns and the same number of rows as test.csv:
  - Restaurant ID
  - Average Cost for two (your predicted price in the currency of the corresponding row)
- The Restaurant ID values must exactly match those in test.csv (order does not matter).

Evaluation metric
- Macro-averaged RMSLE (Root Mean Squared Log Error) computed per currency:
  1) For each currency present in the test set, compute RMSLE between your predictions and the ground truth for that currency: sqrt(mean((log1p(y_pred) − log1p(y_true))^2)).
  2) Average the per-currency RMSLE scores (unweighted mean) to get the final score.
- Rationale: RMSLE is robust to multiplicative scale, and macro-averaging across currencies prevents domination by currencies with larger numeric scales or more rows.
- Predictions will be clipped to be non-negative before scoring. Numerical stability is enforced using log1p.

What you can model
- Price dynamics across currencies and cities
- Effects of cuisines (multi-label), ratings, delivery/booking options, and popularity (votes)
- Spatial patterns from latitude/longitude
- Text signals from restaurant names and locality

Final files
- train.csv
- test.csv
- sample_submission.csv

Tips
- Handle high-cardinality categorical features (City, Locality, Cuisines) via encoders, hashing, target encoding with care, or embeddings.
- Consider multi-hot encoding for frequent cuisines and robust handling for the long tail.
- Geo-features (e.g., clusters or geohashes) and log-transformed votes often help.
- Ensure your pipeline is robust to missing values and rare categories.

Good luck and have fun building a strong, generalizable price model!
