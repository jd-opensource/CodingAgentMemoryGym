# OpenMLE-fast task

Task ID: `palmers-penguin-dataset-extended@2`

Native metric: `PenguinBodyMassMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3027 bytes)
- `data/sample_submission.csv` (67325 bytes); columns: ["row_id", "body_mass_g"]
- `data/test.csv` (107894 bytes); columns: ["row_id", "species", "island", "sex", "year", "bill_length_mm", "bill_depth_mm", "flipper_length_mm"]
- `data/train.csv` (142388 bytes); columns: ["row_id", "species", "island", "sex", "year", "bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]

## Public description

Penguin Body Mass Estimation under Temporal & Ecological Shift

Overview
Ecologists routinely estimate penguin body mass from simple field measurements. Your goal is to build a robust regressor that predicts individual body mass (in grams) from accessible morphometrics and demographics, and that generalizes across islands and years under temporal/ecological shift.

Task
Given measurements for penguins (species, island, sex, year, bill length/depth, flipper length), predict body_mass_g for the unseen test set. Training data spans historical and recent years; the test set consists of future years to enforce distribution shift.

Files
- train.csv: Training table with features and the target body_mass_g.
- test_data.csv: Test table with the same features as train.csv but without body_mass_g. Includes a unique row_id for pairing.
- sample_submission.csv: Example submission with columns [row_id, body_mass_g]. Replace body_mass_g with your predictions.

Columns
- row_id: Unique identifier (present in train.csv, test_data.csv and sample_submission.csv).
- species: {adelie, chinstrap, gentoo}
- island: {biscoe, dream, torgensen}
- sex: {male, female}
- year: Numeric year of observation
- bill_length_mm: Bill length in millimeters (float)
- bill_depth_mm: Bill depth in millimeters (float)
- flipper_length_mm: Flipper length in millimeters (float)
- body_mass_g: Target column in grams (float; train.csv only)

Official split
- Train years: 2007–2009 and 2021–2023
- Test years: 2024–2025
This enforces a temporal and ecological distribution shift. Robust modeling and validation schemes that respect time are recommended.

Important notes
- Extended-only attributes (diet, life_stage, health_metrics) are excluded to maintain a consistent schema and avoid potential leakage.
- Rows with missing predictors or target are removed; units are consistent across the dataset.

Evaluation
- Metric: Mean Absolute Error (MAE) in grams.
- Computation: MAE is computed between your predictions and the hidden ground truth for matching row_id values. Submissions must include exactly the same set of row_id values as in test_data.csv with no duplicates.

Submission format
- CSV with two columns and a header: row_id,body_mass_g
- row_id must match exactly the values provided in test_data.csv (order is irrelevant, alignment is by row_id).
- body_mass_g must be finite numeric values (no NaN/Inf).

Guidance and baseline ideas
- Consider careful preprocessing: categorical encoding (species, island, sex), handling year as numeric or categorical, feature scaling for numeric features, and interaction terms.
- Strong baselines include linear models (ridge/elastic net) and tree-based methods (random forests, GBDT). Robust validation schemes that respect temporal splits are recommended.

Rules
- Use only the provided data files. External data is not required.

Deliverables
- Submit a CSV named as you like that follows the submission format. The platform will compute MAE using the hidden answers aligned by row_id.
