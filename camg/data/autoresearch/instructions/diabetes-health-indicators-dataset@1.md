# OpenMLE-fast task

Task ID: `diabetes-health-indicators-dataset@1`

Native metric: `DiabetesHealthIndicatorsMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2955 bytes)
- `data/sample_submission.csv` (507376 bytes); columns: ["Id", "Diabetes_012"]
- `data/test.csv` (4751003 bytes); columns: ["Id", "HighBP", "HighChol", "CholCheck", "BMI", "Smoker", "Stroke", "HeartDiseaseorAttack", "PhysActivity", "Fruits", "Veggies", "HvyAlcoholConsump", "AnyHealthcare", "NoDocbcCost", "GenHlth", "MentHlth", "PhysHlth", "DiffWalk", "Sex", "Age", "Education", "Income"]
- `data/train.csv` (19407959 bytes); columns: ["Id", "HighBP", "HighChol", "CholCheck", "BMI", "Smoker", "Stroke", "HeartDiseaseorAttack", "PhysActivity", "Fruits", "Veggies", "HvyAlcoholConsump", "AnyHealthcare", "NoDocbcCost", "GenHlth", "MentHlth", "PhysHlth", "DiffWalk", "Sex", "Age", "Education", "Income", "Diabetes_012"]

## Public description

Competition: Ordinal Diabetes Risk Prediction from BRFSS 2015

Problem statement
Build a machine learning model that predicts an individual’s diabetes status on an ordinal 3-class scale from 21 health indicators collected by the CDC’s 2015 BRFSS survey. The target Diabetes_012 has three ordered classes:
- 0: No diabetes or only during pregnancy
- 1: Prediabetes
- 2: Diabetes

Your goal is to produce accurate, well-calibrated predictions that respect the ordinal nature of the target. Models should capture non-linear interactions and handle class imbalance.

Files
- train.csv: Contains Id, 21 features, and the target column Diabetes_012.
- test.csv: Contains Id and the 21 features. The Diabetes_012 column is withheld.
- sample_submission.csv: Shows the required submission format. It contains Id and Diabetes_012 with example (random) predictions.

Data description
Each row represents a survey respondent. The feature set includes cardiovascular/metabolic risk factors and health status indicators, encoded numerically. Example features: HighBP, HighChol, CholCheck, BMI, Smoker, Stroke, HeartDiseaseorAttack, PhysActivity, Fruits, Veggies, HvyAlcoholConsump, AnyHealthcare, NoDocbcCost, GenHlth, MentHlth, PhysHlth, DiffWalk, Sex, Age, Education, Income. The Diabetes_012 target is integer-valued in {0, 1, 2}.

Train/test split
The data are split into train and test with a deterministic stratified 80/20 split that preserves the natural, imbalanced prevalence of the target classes. All target classes appear in the training set.

Submission format
Submit a single CSV file with exactly two columns and a header:
- Id: integer identifier matching test.csv
- Diabetes_012: your predicted class label for that Id, an integer in {0, 1, 2}
The order of rows in your submission does not matter, but Ids must match those in test.csv without duplicates, and every Id in test.csv must appear exactly once.

Evaluation metric
Submissions are evaluated using Quadratic Weighted Kappa (QWK) between the true labels and your predicted class labels. QWK measures agreement between two ordinal ratings, penalizing larger disagreements more than smaller ones and accounting for class imbalance via expected agreement under chance. It ranges from -1 (complete disagreement) to 1 (perfect agreement), with 0 indicating chance-level performance.

Notes and guidance
- Treat the target as ordinal. Techniques such as ordinal logistic regression, cumulative link models, or post-processing with isotonic regression on cumulative probabilities can improve performance under QWK.
- Handle class imbalance thoughtfully (e.g., class weights, appropriate loss functions). Avoid naive resampling that harms probability calibration.
- Linear models may benefit from feature scaling; tree-based models typically do not require it.
- Ensure predictions are valid integers in {0, 1, 2} and that the submission format is strictly followed.

Good luck and happy modeling!
