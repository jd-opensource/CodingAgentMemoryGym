# OpenMLE-fast task

Task ID: `students-mental-health-assessments@1`

Native metric: `MentalHealthSleepQualityMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3825 bytes)
- `data/sample_submission.csv` (2824 bytes); columns: ["Sleep_Quality"]
- `data/test.csv` (146708 bytes); columns: ["Age", "Course", "Gender", "CGPA", "Stress_Level", "Depression_Score", "Anxiety_Score", "Physical_Activity", "Diet_Quality", "Social_Support", "Relationship_Status", "Substance_Use", "Counseling_Service_Use", "Family_History", "Chronic_Illness", "Financial_Stress", "Extracurricular_Involvement", "Semester_Credit_Load", "Residence_Type"]
- `data/train.csv` (596008 bytes); columns: ["Age", "Course", "Gender", "CGPA", "Stress_Level", "Depression_Score", "Anxiety_Score", "Physical_Activity", "Diet_Quality", "Social_Support", "Relationship_Status", "Substance_Use", "Counseling_Service_Use", "Family_History", "Chronic_Illness", "Financial_Stress", "Extracurricular_Involvement", "Semester_Credit_Load", "Residence_Type", "Sleep_Quality"]

## Public description

Title: Predict Students’ Sleep Quality (Ordinal Classification)

Background
Sleep quality profoundly affects students’ mental health, productivity, and academic outcomes. This competition challenges you to model the relationship between academic load, lifestyle, social context, and mental-health-related signals to predict each student’s sleep quality level.

Problem Statement
Given tabular records describing students’ demographics, academics, lifestyle, social support, and mental health indicators, predict the ordinal sleep quality label for each student. The target is Sleep_Quality with ordered classes: Poor < Average < Good.

Data Description
The dataset contains one row per student and diverse feature groups:
- Demographics: Age, Gender, Course, Residence_Type
- Academics: CGPA, Semester_Credit_Load, Extracurricular_Involvement
- Mental health scores: Stress_Level, Depression_Score, Anxiety_Score, Financial_Stress
- Lifestyle and social: Physical_Activity, Diet_Quality, Social_Support, Relationship_Status, Substance_Use, Counseling_Service_Use
- Health history: Family_History, Chronic_Illness
Target variable:
- Sleep_Quality (ordinal): Poor, Average, Good

Files
- train.csv: Labeled training data. Contains all features and a single target column Sleep_Quality encoded as integers {0: Poor, 1: Average, 2: Good}.
- test.csv: Unlabeled test data. Contains the same features as train.csv, excluding Sleep_Quality.
- sample_submission.csv: A sample prediction file with one column Sleep_Quality, containing integer labels {0,1,2} for each row in test.csv.

Evaluation Metric
Primary metric: Quadratic Weighted Kappa (QWK) computed on the ordinal target {Poor=0, Average=1, Good=2}.
- QWK measures agreement between predicted and true labels, penalizing larger ordinal disagreements more heavily than adjacent class mistakes.
- QWK is robust to moderate class imbalance and aligns with the ordered nature of Sleep_Quality.
- Submissions must include one integer per test row in the single column named Sleep_Quality.

Submission Format
- A single-column CSV named Sleep_Quality.
- Each value must be an integer in {0,1,2} matching the order Poor=0, Average=1, Good=2.
- The number of rows must exactly match test.csv.

Suggested Approach
- Data processing: Handle missing values (e.g., median imputation for numeric fields such as CGPA; explicit “Unknown” category for categorical fields such as Substance_Use). Validate ranges (e.g., mental-health scores and Financial_Stress typically fall in 0–5; Semester_Credit_Load is typically 15–30). Do not drop rows unnecessarily.
- Feature engineering: Encode categorical variables (e.g., one-hot, target encoding), consider ordered encodings for ordinal features (e.g., Physical_Activity, Diet_Quality, Social_Support), and optional scaling for numeric features. Explore interaction features between academics and mental health scores.
- Modeling: Try tree-based methods (Gradient Boosting, Random Forest, XGBoost, LightGBM, CatBoost), ordinal regression techniques, or neural networks with embedding layers for categorical features. Consider class weighting or focal loss to address the minority class (Poor).
- Evaluation: Optimize for QWK rather than accuracy to respect label ordering. Use cross-validation, calibration, and threshold optimization if using probabilistic models.

Split Policy
- The train/test split is stratified by Sleep_Quality to preserve class proportions and done with a fixed random seed for reproducibility.
- All classes present in the test set appear at least once in the training set.

Notes
- The target column Sleep_Quality is excluded from test.csv to prevent leakage.
- Use the full dataset scale and all informative features; do not downsample.
- There are no image/audio files; the problem is purely tabular.
