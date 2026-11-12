# OpenMLE-fast task

Task ID: `coffee-quality-database-from-cqi@1`

Native metric: `CoffeeQualityMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3520 bytes)
- `data/sample_submission.csv` (6946 bytes); columns: ["sample_id", "Total.Cup.Points"]
- `data/test.csv` (22120 bytes); columns: ["sample_id", "Species", "Country.of.Origin", "Region", "Variety", "Processing.Method", "Harvest.Year", "altitude_low_meters", "altitude_high_meters", "altitude_mean_meters"]
- `data/train.csv` (83044 bytes); columns: ["Species", "Country.of.Origin", "Region", "Variety", "Processing.Method", "Harvest.Year", "altitude_low_meters", "altitude_high_meters", "altitude_mean_meters", "Total.Cup.Points"]

## Public description

Coffee Quality Forecasting Challenge: Predict Total Cup Points from Pre-harvest Metadata

Background
Specialty coffee is graded by certified cuppers following a standardized protocol. While sensory attributes are measured post-harvest, producers and buyers often need to anticipate coffee quality earlier using farm metadata and declared processing choices. This competition challenges you to predict a coffee lot’s final Total Cup Points using only non-sensory, pre-harvest and declared process information.

Problem Statement
Given farm origin, altitude, species, variety, processing method, region, and related non-sensory metadata, build a model to estimate the Total Cup Points assigned by expert graders. Sensory scores and defect counts are explicitly excluded to prevent leakage.

Files
- train.csv: Training data with features and the target column Total.Cup.Points.
- test.csv: Test data with the same feature columns as train.csv, plus a sample_id column. The target is not included.
- sample_submission.csv: A valid example submission with two columns: sample_id and Total.Cup.Points.

Target
- Total.Cup.Points (continuous regression target).

Features
Only non-sensory, non-identifier columns are retained. Key feature columns include:
- Species
- Country.of.Origin
- Region
- Variety
- Processing.Method
- Harvest.Year
- altitude_low_meters
- altitude_high_meters
- altitude_mean_meters

Notes
- Sensory-derived columns such as Aroma, Flavor, Aftertaste, Acidity, Body, Balance, Uniformity, Clean.Cup, Sweetness, Cupper.Points, Moisture, Category.One.Defects, Category.Two.Defects, and Quakers are excluded, as are obvious identifiers/logistics (e.g., Owner, Farm.Name, Producer, Lot.Number, Mill, Company, Certification.*, Grading.Date, Expiration, Number.of.Bags, Bag.Weight, ICO.Number, Color, text Altitude string, unit_of_measurement). These exclusions prevent target leakage or trivial lookup.
- Expect missing values in several features (e.g., Region, Variety, Processing.Method, altitude_* and Harvest.Year). Your pipeline should handle missingness and potential outliers (e.g., extreme altitude parsing errors). Feature engineering is encouraged.

Evaluation Metric
- Mean Absolute Error (MAE) between your predictions and the ground truth Total.Cup.Points on the hidden test set.
- MAE is robust and interpretable in the context of small point differences typical of cupping scores.

Submission Format
- A CSV with exactly two columns in this order: sample_id, Total.Cup.Points.
- sample_id must match exactly the sample_id values in test.csv.
- Total.Cup.Points must be finite real numbers.

Suggested Approaches
- Encode categorical variables (e.g., country, region, species, variety, processing method) appropriately. One-hot encoding or target-aware regularized encoders are common choices.
- Treat Harvest.Year as either numeric or categorical. Consider imputations or indicators for missing values.
- Clip implausible altitude values and/or add outlier indicators. Median imputation by country or region can be effective for altitude.
- Try tree ensembles (e.g., Gradient Boosting, Random Forests, XGBoost, LightGBM), linear models with regularization, or stacked models. Proper cross-validation is recommended.

Data Scale and Split
- All available rows with valid target values are used. The train/test split is group-aware by producer/farm/lot/year to reduce identity leakage and is deterministic. Both Arabica and Robusta are present in train and test.

Good luck and happy modeling!
