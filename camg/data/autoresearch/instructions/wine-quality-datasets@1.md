# OpenMLE-fast task

Task ID: `wine-quality-datasets@1`

Native metric: `WineQualityMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4247 bytes)
- `data/sample_submission.csv` (2580 bytes); columns: ["id", "quality"]
- `data/test.csv` (21476 bytes); columns: ["id", "fixed acidity", "volatile acidity", "citric acid", "residual sugar", "chlorides", "free sulfur dioxide", "total sulfur dioxide", "density", "pH", "sulphates", "alcohol"]
- `data/train.csv` (87466 bytes); columns: ["id", "fixed acidity", "volatile acidity", "citric acid", "residual sugar", "chlorides", "free sulfur dioxide", "total sulfur dioxide", "density", "pH", "sulphates", "alcohol", "quality"]

## Public description

```
description.txt (27 lines)
sample_submission.csv (322 lines)
test.csv (322 lines)
train.csv (1279 lines)```

-> description.txt has content:

Wine Quality Prediction (Ordinal Classification)

Problem statement
Predict the sensory quality rating of wines from laboratory physicochemical measurements. Each wine has 11 numeric attributes (e.g., acidity, sugar, sulphates, alcohol) and a discrete, ordered target label "quality". Your task is to build models that best predict the ordinal quality class for unseen wines.

Data description
- Input features (11 numeric columns): fixed acidity, volatile acidity, citric acid, residual sugar, chlorides, free sulfur dioxide, total sulfur dioxide, density, pH, sulphates, alcohol.
- Target: quality (integer class). Ratings are discrete and ordered, with noticeable class imbalance.
- Train/test split: Provided train/test files preserve label distribution and prevent leakage by grouping exact duplicate rows so that duplicates never cross splits. The split is deterministic.
- Identifiers: An id column is provided to uniquely identify each row.

Files provided
- train.csv: id, 11 feature columns, and quality.
- test.csv: id and 11 feature columns (no quality).
- sample_submission.csv: id and a placeholder quality column containing valid integer labels.

Evaluation
- Metric: Quadratic Weighted Kappa (QWK). QWK measures agreement between predicted and true ordinal labels, penalizing distant errors more than near misses and accounting for class imbalance.
- Submission format: A single CSV file with columns [id, quality]. The id values must match those in test.csv; quality must be an integer belonging to the allowed label set.

Modeling guidance
- Scale/normalize features due to heterogeneous ranges; robust scaling often helps.
- Consider transformations for skewed variables (e.g., log for chlorides/residual sugar) and interactions (e.g., acidity balance between fixed and volatile acidity, and pH).
- Leverage models that respect ordinality (e.g., ordinal regression or boosting with monotonic constraints). Handle class imbalance via class weights if needed.

Goal
Maximize QWK on the hidden test labels by effective data processing, feature engineering, model training, and evaluation. The dataset is moderately small, imbalanced, and ordinal—requiring careful regularization and validation choices to perform well.

-> sample_submission.csv has 321 rows and 2 columns.
Here is some information about the columns:
id (int64) has range: 1279.00 - 1599.00, 0 nan values
quality (int64) has 6 unique values: [8, 3, 5, 4, 7, 6]

-> test.csv has 321 rows and 12 columns.
Here is some information about the columns:
alcohol (float64) has range: 8.40 - 13.60, 0 nan values
chlorides (float64) has range: 0.04 - 0.37, 0 nan values
citric acid (float64) has range: 0.00 - 0.76, 0 nan values
density (float64) has range: 0.99 - 1.00, 0 nan values
fixed acidity (float64) has range: 5.00 - 15.60, 0 nan values
free sulfur dioxide (float64) has range: 3.00 - 57.00, 0 nan values
id (int64) has range: 1279.00 - 1599.00, 0 nan values
pH (float64) has range: 2.88 - 3.75, 0 nan values
residual sugar (float64) has range: 1.30 - 15.50, 0 nan values
sulphates (float64) has range: 0.40 - 1.56, 0 nan values
total sulfur dioxide (float64) has range: 6.00 - 278.00, 0 nan values
volatile acidity (float64) has range: 0.18 - 1.13, 0 nan values

-> train.csv has 1278 rows and 13 columns.
Here is some information about the columns:
alcohol (float64) has range: 8.40 - 14.90, 0 nan values
chlorides (float64) has range: 0.01 - 0.61, 0 nan values
citric acid (float64) has range: 0.00 - 1.00, 0 nan values
density (float64) has range: 0.99 - 1.00, 0 nan values
fixed acidity (float64) has range: 4.60 - 15.90, 0 nan values
free sulfur dioxide (float64) has range: 1.00 - 72.00, 0 nan values
id (int64) has range: 1.00 - 1278.00, 0 nan values
pH (float64) has range: 2.74 - 4.01, 0 nan values
quality (int64) has 6 unique values: [5, 6, 7, 4, 8, 3]
residual sugar (float64) has range: 0.90 - 15.40, 0 nan values
sulphates (float64) has range: 0.33 - 2.00, 0 nan values
total sulfur dioxide (float64) has range: 6.00 - 289.00, 0 nan values
volatile acidity (float64) has range: 0.12 - 1.58, 0 nan values
