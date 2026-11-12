# OpenMLE-fast task

Task ID: `1000-cameras-dataset@1`

Native metric: `CameraPriceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3782 bytes)
- `data/sample_submission.csv` (7109 bytes); columns: ["Id", "Price"]
- `data/test.csv` (25728 bytes); columns: ["Id", "Model", "Release date", "Max resolution", "Low resolution", "Effective pixels", "Zoom wide (W)", "Zoom tele (T)", "Normal focus range", "Macro focus range", "Storage included", "Weight (inc. batteries)", "Dimensions"]
- `data/train.csv` (62558 bytes); columns: ["Id", "Model", "Release date", "Max resolution", "Low resolution", "Effective pixels", "Zoom wide (W)", "Zoom tele (T)", "Normal focus range", "Macro focus range", "Storage included", "Weight (inc. batteries)", "Dimensions", "Price"]

## Public description

Camera Launch Price Prediction (1994–2007)

Background
Manufacturers and retailers often need to estimate a camera’s launch price from its technical specifications and market positioning. This competition challenges you to build models that predict a camera’s launch price using its specs and model name, and to generalize well to later-year models.

Problem statement
Given technical specifications and the model name for 1,038 cameras released between 1994 and 2007, predict the camera’s launch price. The evaluation uses a time-aware split so that training covers earlier years and testing covers later years.

Files
- train.csv: Training data with features and the target column Price.
- test.csv: Test data with the same feature columns as train.csv, plus an Id column for submission mapping. The target column Price is not included.
- sample_submission.csv: A sample submission file with the required columns Id and Price and random but valid placeholder predictions.

Target
- Price: The launch price (numeric, positive).

Features
All columns in train.csv except Price are available as features. Columns include (but may not be limited to):
- Model: Camera model string (e.g., brand/series/tokens). Textual features can be engineered from this column.
- Release date: Release year as an integer (1994–2007).
- Max resolution, Low resolution, Effective pixels
- Zoom wide (W), Zoom tele (T)
- Normal focus range, Macro focus range
- Storage included
- Weight (inc. batteries)
- Dimensions

Important notes on data quality and feature engineering
- Zeros-as-missing: Several numeric columns use 0.0 to indicate unknown/not applicable (e.g., some zoom/focus/storage fields). Treat such zeros as missing unless physically meaningful in your modeling approach.
- Interchangeable-lens models: If Zoom wide (W) and Zoom tele (T) are both 0, this often indicates no built-in zoom. You may create a binary flag and/or handle these zeros carefully.
- Text features: The Model string can be tokenized to extract brand, series, and alphanumeric tokens (e.g., EOS, PowerShot, Coolpix, A530, 1Ds), which can be predictive of price.
- Heavy-tailed target: Prices range from low-cost to professional models with a long right tail. Modeling log(Price) or using log-aware metrics can improve robustness.

Train/test split
- Time-aware split: Train covers 1994–2005, Test covers 2006–2007. This simulates predicting prices of newer models using prior years’ data and reduces temporal leakage.

Evaluation metric
- Root Mean Squared Logarithmic Error (RMSLE) on Price.
- Definition: Let y_true and y_pred be the true and predicted prices for the test set. We compute RMSLE as:
  RMSLE = sqrt(mean((log1p(y_true_clipped) - log1p(y_pred_clipped))^2))
  where values are clipped to be non-negative before applying log1p, to avoid domain issues.
- Rationale: RMSLE emphasizes relative errors and is robust to the heavy-tailed price distribution, balancing performance across budget and high-end models.

Submission format
- A valid submission is a CSV with two columns: Id, Price
- Id must match exactly the Id values provided in test.csv (one row per test camera, no duplicates or missing entries).
- Price must be finite, non-negative numeric predictions.

Expectations for high-scoring solutions
- Careful handling of missingness and zeros-as-missing in numeric fields
- Thoughtful feature engineering from both numeric specs and the Model text
- Robust modeling for heavy-tailed targets (e.g., log-transform, tree ensembles, regularized linear models, blending)
- Time-aware validation (e.g., using only training years for fitting imputers and models; validation strategies that respect chronology)

Good luck, and have fun building price predictors that stand the test of time!
