# OpenMLE-fast task

Task ID: `top-rated-coffee@1`

Native metric: `CoffeeQualityRegressionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3285 bytes)
- `data/sample_submission.csv` (31839 bytes); columns: ["id", "total_score"]
- `data/test.csv` (99084 bytes); columns: ["id", "coffee_name", "roaster_location", "coffee_origin", "origin_country", "roast_level_clean", "roast_level_raw", "agtron_ground", "agtron_roast", "agtron_raw", "price_per_ounce", "est_price_raw"]
- `data/train.csv` (404068 bytes); columns: ["id", "coffee_name", "roaster_location", "coffee_origin", "origin_country", "roast_level_clean", "roast_level_raw", "agtron_ground", "agtron_roast", "agtron_raw", "price_per_ounce", "est_price_raw", "total_score"]

## Public description

Cup Quality Prediction from Coffee Metadata and Names

Problem statement
Participants must build a regression model that predicts CoffeeReview’s total_score for held-out coffees using rich product metadata and names. Scores are precise and lie in a narrow range (typically 94–98), so small improvements matter. The task challenges you to combine structured attributes (roast level, Agtron color readings, origin country, price per ounce) with messy, real-world text fields (coffee_name, roaster_location, coffee_origin, raw price string, raw Agtron pair) to capture nuanced quality cues.

Files provided
- train.csv: Feature columns plus the target total_score.
- test.csv: Same feature columns as train.csv, without total_score.
- sample_submission.csv: Example submission file with the required format.

Row identifier
- id: A deterministic anonymized identifier string unique to each coffee instance. Use this to match predictions to test rows.

Feature columns
Both normalized and raw variants are included where useful to encourage robust preprocessing and feature engineering.
- coffee_name: Product name text.
- roaster_location: Roaster location text.
- coffee_origin: Origin/region text (keep full text; do not reduce prematurely).
- origin_country: Normalized origin country (categorical text; may be missing for some rows).
- roast_level_clean: Normalized roast taxonomy derived from the cleaned source (e.g., Light, Medium Light, etc.).
- roast_level_raw: Un-normalized roast level from the raw source (e.g., Medium-Light); useful for your own normalization.
- agtron_ground: Numeric Agtron ground measurement (cleaned).
- agtron_roast: Numeric Agtron roast measurement (cleaned).
- agtron_raw: Combined raw Agtron string (e.g., "62/84"); parse if numeric fields are missing.
- price_per_ounce: Numeric price per ounce (cleaned; mixed currencies may inflate values—handle robustly).
- est_price_raw: Raw price string (e.g., "$25.00/250 grams", "NT $550/200 grams"); extract currency/unit flags and pack size if helpful.

Target
- total_score (train.csv only): Continuous score to be predicted for test.csv rows.

Train/test split
- The dataset is split deterministically into train and test. The split preserves the score distribution via stratification on total_score rounded to the nearest integer.

Evaluation
- Metric: Root Mean Squared Error (RMSE) on total_score.
  - RMSE penalizes larger errors and is sensitive in the dataset’s narrow score range, making it fair and precise.
- Submission format: A CSV with exactly two columns and a header row:
  - id: Identifier matching those in test.csv.
  - total_score: The predicted score as a finite numeric value (float).

What makes this challenging and worthwhile
- Narrow target variance demands careful feature engineering and regularization.
- Text normalization across product naming conventions and locations (e.g., Geisha/Gesha, processing methods like anaerobic, honey, carbonic maceration).
- Mixed currencies/units and outlier prices require robust handling.
- Agtron measurements and roast-level taxonomies need sensible interpretation.

Final deliverables
- Predict total_score for all rows in test.csv.
- Submit a CSV named as you wish that follows the sample_submission.csv format (id,total_score).
