# OpenMLE-fast task

Task ID: `dynamic-pricing-dataset@1`

Native metric: `DynamicPricingMAEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2783 bytes)
- `data/sample_submission.csv` (5664 bytes); columns: ["id", "Historical_Cost_of_Ride"]
- `data/test.csv` (11480 bytes); columns: ["id", "Number_of_Riders", "Number_of_Drivers", "Location_Category", "Customer_Loyalty_Status", "Number_of_Past_Rides", "Average_Ratings", "Time_of_Booking", "Vehicle_Type", "Expected_Ride_Duration"]
- `data/train.csv` (60148 bytes); columns: ["id", "Number_of_Riders", "Number_of_Drivers", "Location_Category", "Customer_Loyalty_Status", "Number_of_Past_Rides", "Average_Ratings", "Time_of_Booking", "Vehicle_Type", "Expected_Ride_Duration", "Historical_Cost_of_Ride"]

## Public description

Dynamic Pricing: Predict Ride Fares from Supply–Demand Context

Problem statement
A ride-hailing platform wants to set accurate, real-time fares that reflect supply–demand balance, vehicle class, timing, and rider history. You are given historical trips with contextual features. Your task is to predict the realized ride price (Historical_Cost_of_Ride) for unseen trips.

Data description
Each row represents one ride request with pre-ride context:
- Number_of_Riders: integer count of concurrent rider requests in the area
- Number_of_Drivers: integer count of available drivers in the area
- Location_Category: categorical (Urban, Suburban, Rural)
- Customer_Loyalty_Status: categorical (Regular, Silver, Gold)
- Number_of_Past_Rides: integer prior rides by the customer
- Average_Ratings: float average rating of the customer
- Time_of_Booking: categorical (Morning, Afternoon, Evening, Night)
- Vehicle_Type: categorical (Economy, Premium)
- Expected_Ride_Duration: integer expected duration in minutes
- Historical_Cost_of_Ride: float realized price (target)

Files provided
- train.csv: id, all features, and the target column Historical_Cost_of_Ride
- test.csv: id and all features (no target)
- sample_submission.csv: id and a column Historical_Cost_of_Ride with random valid values to illustrate the required format

Target
- Historical_Cost_of_Ride (continuous, strictly positive)

Evaluation
- Primary metric: Mean Absolute Error (MAE) between your predictions and ground truth prices on the hidden test set.
- Submission format: a CSV with two columns: id and Historical_Cost_of_Ride. The id values must exactly match those in test.csv, with one row per id and no duplicates.

Guidance and baseline ideas
- Make strong use of the contextual features beyond duration. Useful engineered features include:
  - riders_to_drivers_ratio = Number_of_Riders / max(1, Number_of_Drivers)
  - demand_gap = Number_of_Riders − Number_of_Drivers
  - interactions between Time_of_Booking, Vehicle_Type, and Expected_Ride_Duration
  - centered/standardized numeric features
- Model families that work well include regularized linear models, tree ensembles (e.g., gradient boosting), and calibrated monotonic models. Cross-validation is recommended.
- Categorical handling: one-hot encoding or target/impact encoding (with care to avoid leakage) for Location_Category, Customer_Loyalty_Status, Time_of_Booking, and Vehicle_Type.

Constraints and notes
- The split is stratified by (Location_Category, Time_of_Booking, Vehicle_Type) to preserve segment coverage.
- No paths are included in any CSV files; id is a synthetic identifier.
- Ensure your submission has no missing/NaN/Inf values and the correct column names.

Good luck building a fair and accurate dynamic pricing model!
