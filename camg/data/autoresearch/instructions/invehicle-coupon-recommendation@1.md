# OpenMLE-fast task

Task ID: `invehicle-coupon-recommendation@1`

Native metric: `InVehicleCouponRecommendationMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2680 bytes)
- `data/sample_submission.csv` (75794 bytes); columns: ["row_id", "prediction"]
- `data/test.csv` (529447 bytes); columns: ["row_id", "destination", "passanger", "weather", "temperature", "time", "coupon", "expiration", "gender", "age", "maritalStatus", "has_children", "education", "occupation", "income", "Bar", "CoffeeHouse", "CarryAway", "RestaurantLessThan20", "Restaurant20To50", "toCoupon_GEQ15min", "toCoupon_GEQ25min", "direction_same"]
- `data/train.csv` (1611080 bytes); columns: ["row_id", "destination", "passanger", "weather", "temperature", "time", "coupon", "expiration", "gender", "age", "maritalStatus", "has_children", "education", "occupation", "income", "Bar", "CoffeeHouse", "CarryAway", "RestaurantLessThan20", "Restaurant20To50", "toCoupon_GEQ15min", "toCoupon_GEQ25min", "direction_same", "Y"]

## Public description

Title: In-vehicle Coupon Acceptance (Group-Robust Probability Prediction)

Problem statement
Given a single offered coupon and the surrounding driving scenario plus driver profile, predict the probability that the driver accepts the coupon. The task is a binary classification with probabilistic outputs.

Files provided
- train.csv: Training data with features and the target column Y (1 = accepted, 0 = rejected). Includes a unique row_id column for each row.
- test.csv: Test data with the same feature columns as train.csv but without Y. Includes row_id for joining with the submission.
- sample_submission.csv: Example submission file containing row_id and prediction.

Target and features
- Target: Y (acceptance; 1 = yes, 0 = no).
- Features (tabular, mixed categorical/ordinal/numeric): scenario context (destination, passanger, weather, temperature, time, expiration, toCoupon_GEQ15min, toCoupon_GEQ25min, direction_same), user profile (gender, age, maritalStatus, has_children, education, occupation, income), behavior frequencies (Bar, CoffeeHouse, CarryAway, RestaurantLessThan20, Restaurant20To50), and the coupon type itself (coupon). The direction_opp, car, and toCoupon_GEQ5min columns are removed as they are redundant, near-fully-missing, or constant respectively.

Evaluation
Primary metric: Macro-averaged Log Loss across coupon categories.
- Compute binary log loss separately within each coupon category, then average the five per-coupon losses to obtain the final score. Lower is better.
- This rewards well-calibrated probabilities and ensures robust performance across coupon types rather than over-optimizing for dominant groups.

Submission format
- A CSV with exactly two columns:
  - row_id: integer identifier matching test.csv
  - prediction: a probability in [0, 1] for Y=1
- The file must contain exactly one row per row_id in the test set, with no duplicates and no missing values. Predictions will be clipped to avoid log(0), but values outside [0,1] are considered invalid.

Recommendations
- Strong baselines include calibrated gradient-boosted trees (e.g., CatBoost, LightGBM, XGBoost) and regularized linear/logistic models with appropriate encoding of categorical and ordinal features.
- Useful feature engineering ideas: interaction terms such as coupon × time, coupon × distance, destination × direction, ordinal encodings for visit-frequency features, and calibration techniques (Platt scaling, isotonic regression).

Final data files
- train.csv
- test.csv
- sample_submission.csv

Note
- The provided split is stratified by both coupon and Y to preserve realistic group distributions and to prevent exploiting inter-group imbalance.
