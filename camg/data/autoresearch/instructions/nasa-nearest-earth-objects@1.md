# OpenMLE-fast task

Task ID: `nasa-nearest-earth-objects@1`

Native metric: `NearEarthObjectsMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2815 bytes)
- `data/sample_submission.csv` (295346 bytes); columns: ["row_id", "hazardous"]
- `data/test.csv` (1347796 bytes); columns: ["row_id", "est_diameter_min", "est_diameter_max", "relative_velocity", "miss_distance", "absolute_magnitude"]
- `data/train.csv` (5417383 bytes); columns: ["row_id", "est_diameter_min", "est_diameter_max", "relative_velocity", "miss_distance", "absolute_magnitude", "hazardous"]

## Public description

Title: Predict Potentially Hazardous Near-Earth Objects

Problem statement
You are given tabular records describing close-approach characteristics and physical properties of Near-Earth Objects (NEOs). Your task is to build a machine learning model that predicts the probability that an object is classified as “potentially hazardous.” Predictions must be provided as calibrated probabilities for the hazardous label.

Data description
Each row corresponds to a single NEO record with the following columns:
- row_id: anonymized row identifier for the record (used for submission indexing)
- est_diameter_min: estimated minimum diameter (km)
- est_diameter_max: estimated maximum diameter (km)
- relative_velocity: relative velocity during close approach (km/s)
- miss_distance: miss distance during close approach (km)
- absolute_magnitude: absolute magnitude (H)
- hazardous: binary target label (only in train.csv)

Final files provided
- train.csv: training data including the hazardous label
- test.csv: test data without the hazardous label
- sample_submission.csv: a sample submission file demonstrating the expected format

Important notes
- The class distribution is imbalanced. Careful preprocessing, feature engineering, and probability calibration are strongly recommended.
- Non-informative attributes are omitted; focus on physical and kinematic features.
- Suggested feature engineering: log transforms for heavy-tailed variables (e.g., miss_distance, relative_velocity, diameters), diameter ratio (est_diameter_max / est_diameter_min), and interactions between size and absolute magnitude.

Submission format
- A single CSV file with two columns: row_id and hazardous
- row_id must match the row_ids in test.csv
- hazardous must be the predicted probability in [0, 1] for the record being hazardous (not a hard class label)

Evaluation metric
- Average Precision (AP), also known as PR-AUC, computed on the hazardous class.
Rationale: AP is well-suited for imbalanced binary classification. It evaluates the quality of ranking predicted probabilities for the positive class and rewards models that achieve high precision at high recall.

Train/test split
- The split is stratified by the hazardous label at the object level to preserve class ratios and avoid leakage across records belonging to the same object.
- All test labels appear at least once in the training set.

Good practices to achieve strong performance
- Robust scaling or standardization of numeric features
- Thoughtful handling of outliers and heavy-tailed distributions
- Model selection (e.g., gradient boosting, calibrated ensembles, generalized additive models, properly normalized neural networks)
- Probability calibration (Platt scaling, isotonic regression) and threshold selection guided by precision–recall behavior
