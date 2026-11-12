# OpenMLE-fast task

Task ID: `brain-stroke-dataset@1`

Native metric: `StrokeRiskPredictionMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3238 bytes)
- `data/sample_submission.csv` (13968 bytes); columns: ["id", "stroke"]
- `data/test.csv` (66001 bytes); columns: ["id", "gender", "age", "hypertension", "heart_disease", "ever_married", "work_type", "Residence_type", "avg_glucose_level", "bmi", "smoking_status"]
- `data/train.csv` (272705 bytes); columns: ["id", "gender", "age", "hypertension", "heart_disease", "ever_married", "work_type", "Residence_type", "avg_glucose_level", "bmi", "smoking_status", "stroke"]

## Public description

Title: Stroke Risk Prediction from Demographics and Clinical Indicators

Problem statement
Build a machine learning model that predicts, for each individual, the probability of having experienced a stroke. This is a binary classification task with severe class imbalance (~5% positives). Submissions must provide well-calibrated probabilities in [0,1] for the stroke outcome.

Data description
You will receive tabular data with demographic and clinical variables per individual. Mixed feature types include numerical and categorical variables. The target variable is stroke (1 if the individual has experienced a stroke, 0 otherwise).

Final files provided
- train.csv: Labeled training data. Columns: id, gender, age, hypertension, heart_disease, ever_married, work_type, Residence_type, avg_glucose_level, bmi, smoking_status, stroke.
- test.csv: Unlabeled test data. Columns: id, gender, age, hypertension, heart_disease, ever_married, work_type, Residence_type, avg_glucose_level, bmi, smoking_status.
- sample_submission.csv: Submission template with example probabilities. Columns: id, stroke.

Target and features
- Target: stroke (binary, 1=stroke, 0=no stroke).
- Features: gender, age, hypertension, heart_disease, ever_married, work_type, Residence_type, avg_glucose_level, bmi, smoking_status.

Train/test split
- Host-provided split is stratified by the stroke label to preserve the minority class rate in both train and test sets.
- Approximately 80% of rows are in train.csv and 20% in test.csv.
- The id column is a synthetic, non-informative identifier; it exists only to align rows across files.

Submission format
- A CSV file with two columns: id and stroke.
- id must match the ids provided in test.csv.
- stroke must be a probability in [0,1] for each test row, aligned by id.

Evaluation metric
- Primary metric: Average Precision (PR-AUC).
- Rationale: With strong class imbalance, PR-AUC emphasizes correctly ranking the minority (positive) class and is threshold-independent. It robustly reflects precision-recall tradeoffs and penalizes false positives.

Guidance and expectations
- Handle categorical variables via sound encodings (e.g., one-hot or target encoding). Treat smoking_status="Unknown" as a distinct category rather than imputing.
- Scale/standardize continuous features (age, avg_glucose_level, bmi) as appropriate; binary flags (hypertension, heart_disease) can be used as-is.
- Address class imbalance using techniques such as class weights, adjusted decision thresholds, focal loss, or carefully designed resampling on the training set.
- Calibrate predicted probabilities (e.g., via Platt scaling or isotonic regression) if your model is not naturally calibrated.
- Avoid target leakage and overfitting; perform robust cross-validation within the training set when developing your approach.

Quality and challenge
- The dataset’s mixed types, severe imbalance, and feature interactions (e.g., age × comorbidities × smoking) make the problem non-trivial while solvable with classical ML (regularized logistic regression, gradient boosting) or modern tabular deep learning methods. Strong solutions will combine careful preprocessing, class-imbalance handling, and probability calibration.
