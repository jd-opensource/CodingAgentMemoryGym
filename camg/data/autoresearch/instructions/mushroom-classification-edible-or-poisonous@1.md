# OpenMLE-fast task

Task ID: `mushroom-classification-edible-or-poisonous@1`

Native metric: `MushroomPoisoningMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2658 bytes)
- `data/sample_submission.csv` (306400 bytes); columns: ["id", "poisonous"]
- `data/test.csv` (587165 bytes); columns: ["id", "cap-diameter", "cap-shape", "cap-surface", "cap-color", "does-bruise-or-bleed", "gill-attachment", "gill-spacing", "gill-color", "stem-height", "stem-width", "stem-root", "stem-surface", "stem-color", "has-ring", "ring-type", "spore-print-color", "habitat", "season"]
- `data/train.csv` (2446445 bytes); columns: ["id", "class", "cap-diameter", "cap-shape", "cap-surface", "cap-color", "does-bruise-or-bleed", "gill-attachment", "gill-spacing", "gill-color", "stem-height", "stem-width", "stem-root", "stem-surface", "stem-color", "has-ring", "ring-type", "spore-print-color", "habitat", "season"]

## Public description

Mushroom Mayhem — Predict Poisonous Probability

Problem statement
Given morphological and contextual attributes of mushrooms, predict the probability that each mushroom is poisonous (class = p). This is a safety-critical classification task where well-calibrated probabilistic predictions are rewarded.

Files provided
- train.csv: Tabular training data including the target column.
- test.csv: Tabular test data without the target column.
- sample_submission.csv: Example submission file with the required format.

Data schema
- id: Unique integer identifier per row.
- Features (18 total): cap-diameter, cap-shape, cap-surface, cap-color, does-bruise-or-bleed, gill-attachment, gill-spacing, gill-color, stem-height, stem-width, stem-root, stem-surface, stem-color, has-ring, ring-type, spore-print-color, habitat, season.
- Target (train.csv only): class — e (edible) or p (poisonous).

Notes
- Numeric features: cap-diameter, stem-height, stem-width.
- All other features are categorical (single-letter codes). Missing values are present and should be handled explicitly.
- Two veil-related columns were excluded to focus the task on features with broader coverage and clearer semantics.
- The train/test split is stratified to preserve class balance and is deterministic.

Submission format
- A CSV file with exactly two columns: id and poisonous.
  - id: Must match the ids in test.csv (each id exactly once).
  - poisonous: A probability in [0, 1] representing P(class = p) for the corresponding id.

Evaluation
- Metric: Log loss (binary cross-entropy) computed on the poisonous probability.
- Why this metric: Log loss evaluates both discrimination and calibration, penalizing overconfident errors and avoiding threshold dependence—appropriate for moderate class imbalance and safety-critical predictions.

Guidance for participants
- Use the full dataset; do not down-sample.
- Data processing: Treat empty strings as missing values; impute numeric features (e.g., median) and categorical features (e.g., most frequent or a dedicated “missing” category).
- Feature engineering: One-hot encode categorical variables with handle_unknown behavior to safely accommodate rare/unseen levels at test time. Consider scaling numeric features, especially for linear/probabilistic models.
- Modeling: Standard tabular ML methods (regularized linear models, tree ensembles, calibrated classifiers, stacking) are applicable. Pay attention to probability calibration.
- Pitfalls: High-cardinality categories, non-uniform missingness, and non-linear interactions can make overfitting easy. Cross-validate and calibrate predictions to improve log loss.
