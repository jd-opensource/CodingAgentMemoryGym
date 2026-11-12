# OpenMLE-fast task

Task ID: `honda-data@2`

Native metric: `HondaMileageMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3289 bytes)
- `data/sample_submission.csv` (13136 bytes); columns: ["id", "Mileage"]
- `data/test.csv` (145162 bytes); columns: ["id", "Year", "Model", "Condition", "Price", "Consumer_Rating", "Consumer_Review_Count", "Exterior_Color", "Interior_Color", "Drivetrain", "MPG", "Fuel_Type", "Transmission", "Engine", "State", "Seller_Type"]
- `data/train.csv` (595298 bytes); columns: ["id", "Year", "Model", "Condition", "Price", "Consumer_Rating", "Consumer_Review_Count", "Exterior_Color", "Interior_Color", "Drivetrain", "MPG", "Fuel_Type", "Transmission", "Engine", "State", "Seller_Type", "Mileage"]

## Public description

Honda Listing Mileage Estimation (Tabular Regression)

Problem statement
- Goal: Predict the odometer mileage (integer, miles) of a Honda vehicle listing using its specs, pricing, and contextual attributes.
- Background: Online listings frequently omit or misreport mileage. Robust estimation from other attributes supports quality checks and downstream pricing models.

Data description
- You are given cleaned tabular files built from scraped listings on cars.com. Each row is one listing.
- Target: Mileage (non-negative integer, miles).
- Identifier: id (string). Use id to align your predictions with test rows.
- Features available (raw, lightly cleaned; no label leakage fields):
  - Year (int)
  - Model (str) – model/trim as scraped
  - Condition (str) – e.g., New, Used, Honda Certified
  - Price (str) – raw string as listed (e.g., "$34,150", "Not Priced")
  - Consumer_Rating (float)
  - Consumer_Review_Count (int)
  - Exterior_Color (str)
  - Interior_Color (str)
  - Drivetrain (str) – e.g., All-wheel Drive, Front-wheel Drive, AWD
  - MPG (str) – raw range as listed (e.g., "19–25", "27–32")
  - Fuel_Type (str)
  - Transmission (str)
  - Engine (str) – free-form (e.g., "3.5L V6 24V GDI SOHC")
  - State (str)
  - Seller_Type (str)
- Deliberately excluded to avoid leakage or redundancy: VIN, Stock_#, Comfort_Rating, Interior_Design_Rating, Performance_Rating, Value_For_Money_Rating, Exterior_Styling_Rating, Reliability_Rating, Make (constant).

Provided files
- train.csv – Training rows with columns: [id, Year, Model, Condition, Price, Consumer_Rating, Consumer_Review_Count, Exterior_Color, Interior_Color, Drivetrain, MPG, Fuel_Type, Transmission, Engine, State, Seller_Type, Mileage].
- test.csv – Test rows with the same columns as train.csv except Mileage is withheld: [id, Year, Model, Condition, Price, Consumer_Rating, Consumer_Review_Count, Exterior_Color, Interior_Color, Drivetrain, MPG, Fuel_Type, Transmission, Engine, State, Seller_Type].
- sample_submission.csv – Example submission with columns [id, Mileage]. Values are random but plausible and should be replaced by your predictions.

Submission format
- CSV with exactly two columns and a header: [id, Mileage].
- id must match exactly the ids in test.csv.
- Mileage predictions must be numeric and non-negative. Any negative values will be clipped to zero during scoring.

Evaluation
- Root Mean Squared Logarithmic Error (RMSLE) on Mileage:
  - For each test row i with ground truth y_i and prediction p_i, we compute: E = mean((log(1 + p_i_clipped) − log(1 + y_i))^2) and RMSLE = sqrt(E), where p_i_clipped = max(p_i, 0).
  - Motivation: Mileage errors are multiplicative in nature (e.g., 60k vs 80k ~ 6k vs 8k). RMSLE is robust to skew and near-zero mileages.

Notes and recommendations
- Useful preprocessing ideas: parse numeric values from Price; split MPG ranges into city/highway; normalize drivetrain; map transmission/engine strings to standardized categories; extract displacement/cylinders/turbo/hybrid flags; treat missing values explicitly and consider missingness indicators.
- This is a real-world dataset: expect heterogeneous missingness and noisy text features. Gradient boosting, regularized linear models, and robust preprocessing often perform well.
