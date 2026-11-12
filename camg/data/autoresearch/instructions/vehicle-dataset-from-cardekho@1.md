# OpenMLE-fast task

Task ID: `vehicle-dataset-from-cardekho@1`

Native metric: `UsedCarPriceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3937 bytes)
- `data/sample_submission.csv` (35120 bytes); columns: ["id", "selling_price"]
- `data/test.csv` (280981 bytes); columns: ["id", "name", "year", "km_driven", "fuel", "seller_type", "transmission", "owner", "mileage", "engine", "max_power", "torque", "seats", "location", "color", "drivetrain", "length", "width", "height", "seating_capacity", "fuel_tank_capacity"]
- `data/train.csv` (1206006 bytes); columns: ["id", "name", "year", "km_driven", "fuel", "seller_type", "transmission", "owner", "mileage", "engine", "max_power", "torque", "seats", "location", "color", "drivetrain", "length", "width", "height", "seating_capacity", "fuel_tank_capacity", "selling_price"]

## Public description

Used Car Price Prediction (India) — Multi-source, Real-world Tabular Regression

Background
Pricing used vehicles is a core decision for dealers, marketplaces, and consumers. Real-world data mixes multiple sources with heterogeneous feature sets, duplicate listings, and outliers. This competition challenges you to build models that robustly predict selling price from noisy, partially missing attributes across diverse car brands, years, and geographies in India.

Problem Statement
Given listing attributes for used cars, predict the final selling price (in INR rupees). You will receive a training set with features and the target, and a held-out test set with only features. Submit price predictions for the test set; submissions are evaluated using Root Mean Squared Logarithmic Error (RMSLE).

What makes this challenging
- Multiple real-world sources with different schemas merged into one dataset
- Heterogeneous feature availability (technical specs present only for subsets)
- High-cardinality text features (model/variant names)
- Long-tailed target distribution spanning budget to luxury segments
- Potential near-duplicates and noisy entries that require careful preprocessing

Files provided
- train.csv: Feature columns plus the target column selling_price.
- test.csv: Same feature columns as train.csv but without selling_price.
- sample_submission.csv: A correctly formatted example submission with random but valid predictions.

Target and Features
- Target: selling_price (numeric INR).
- Core features (present for all rows):
  - name: car make/model/variant text
  - year: model year (integer)
  - km_driven: odometer reading in kilometers (integer)
  - fuel: fuel type (categorical)
  - seller_type: seller type (categorical)
  - transmission: transmission type (categorical)
  - owner: owner count normalized to integers (0 for test-drive/demo, 1 for first, 2 for second, etc.)
- Additional features (provided where available; may be missing elsewhere): mileage, engine, max_power, torque, seats, location, color, drivetrain, length, width, height, seating_capacity, fuel_tank_capacity.
Notes:
- Some additional features may contain units within strings (e.g., "1498 CC", "74 bhp", dimensions). Participants may parse/clean these as desired.
- The feature set has been harmonized across sources and deduplicated by a composite key to avoid the same listing appearing more than once.

Evaluation Metric
- Submissions are evaluated on RMSLE between your predictions and the ground truth selling_price for the test set.
- RMSLE is defined as: sqrt( mean( (log1p(y_true) - log1p(y_pred))^2 ) ).
- Predictions must be non-negative. During scoring, any non-positive values may be clipped to a small positive epsilon for numerical stability.

Submission Format
- CSV file with two columns and a header row: id,selling_price
- id must match exactly the ids provided in test.csv.
- selling_price should be numeric predictions in INR. Ensure values are finite numbers.

Getting Started Tips
- Basic preprocessing: deduplicate if you reconstruct from raw, normalize owner to counts, and consider log-transforming target during training.
- Feature engineering: parse technical specifications (engine CC, power bhp, mileage kmpl), derive car age (current year - model year), interactions like age×km.
- Modeling: gradient boosting trees or regularized linear models are strong baselines. Handle missing values carefully and encode high-cardinality text (e.g., target-encoding or hashing).
- Evaluation: optimize RMSLE; consider training on log1p(selling_price) and exponentiating at inference.

Rules and Integrity
- The files are split to prevent leakage across train/test. Do not attempt to infer labels from file names or ordering.
- External data is allowed if publicly available and equally accessible to all participants; declare it clearly in your solution.

Good luck and have fun building robust price predictors!
