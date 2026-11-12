# OpenMLE-fast task

Task ID: `sports-car-prices-dataset@1`

Native metric: `SportsCarPriceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3015 bytes)
- `data/sample_submission.csv` (4398 bytes); columns: ["Id", "Price (in USD)"]
- `data/test.csv` (11249 bytes); columns: ["Id", "Car Make", "Car Model", "Year", "Engine Size (L)", "Horsepower", "Torque (lb-ft)", "0-60 MPH Time (seconds)"]
- `data/train.csv` (44773 bytes); columns: ["Id", "Car Make", "Car Model", "Year", "Engine Size (L)", "Horsepower", "Torque (lb-ft)", "0-60 MPH Time (seconds)", "Price (in USD)"]

## Public description

Sports Car Price Prediction

Problem statement
Participants must build a regression model that predicts the price (in USD) of a sports car given its attributes. The task is designed to be challenging: the target distribution is heavy-tailed, the dataset contains duplicates at the make–model–year level, and several features include non-numeric tokens. Models should leverage robust preprocessing, careful categorical encoding, and regularization to generalize across brands and performance tiers.

Final data files
- train.csv: training set with features and the target column
- test.csv: test set with features only
- sample_submission.csv: a sample submission file with the correct format

Input features
- Car Make (categorical)
- Car Model (categorical)
- Year (numeric/categorical)
- Engine Size (L) (numeric or text annotations such as Electric/Hybrid)
- Horsepower (numeric or text variants such as 1,000+)
- Torque (lb-ft) (numeric or text variants such as N/A)
- 0-60 MPH Time (seconds) (numeric or text variant such as < 1.9)

Target
- Price (in USD): heavy-tailed numeric target, ranging from tens of thousands to several million USD

Important notes on data characteristics
- Group-aware split: all rows sharing the same (Car Make, Car Model, Year) are assigned entirely to either train or test. This prevents leakage from duplicated groups.
- Ambiguous tokens: some feature cells are textual (e.g., Electric, N/A, 1000+). Handle these thoughtfully in preprocessing (e.g., categorical flags, imputation, robust encoders).
- No external data is required or provided.

Evaluation metric
- Root Mean Squared Logarithmic Error (RMSLE) on Price (in USD).
  - The organizer computes RMSLE as the root mean squared error on log1p(pred) versus log1p(true).
  - Predictions must be provided for every Id in test.csv.
  - During scoring, non-negative predictions are required; negative predictions are clipped to zero to ensure numerical stability.

Submission format
- A CSV file with two columns:
  - Id: identifiers matching the Ids in test.csv
  - Price (in USD): your predicted price for each Id
- The set of Ids must match test.csv exactly, with no duplicates or missing/extraneous rows.

What makes this competition challenging and meaningful
- Strong brand/model effects and multicollinearity among performance features (horsepower, torque, and 0–60 times) necessitate non-linear modeling or careful regularization.
- Heavy-tailed targets demand scale-appropriate losses and evaluation; RMSLE makes the task fair by measuring multiplicative error.
- Duplicated groups and rare categories require leakage-safe validation and robust encoders.

Recommendations
- Parse numeric fields carefully (e.g., remove thousands separators and symbols).
- Consider categorical encoders (one-hot for frequent levels; target/leave-one-out encoders with group-aware CV).
- Explore transformations (e.g., log) and scaling for continuous features.
- Handle missing/ambiguous tokens explicitly to avoid silent errors.
