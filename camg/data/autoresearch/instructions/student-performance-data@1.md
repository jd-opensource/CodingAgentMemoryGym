# OpenMLE-fast task

Task ID: `student-performance-data@1`

Native metric: `StudentPerformanceMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3018 bytes)
- `data/sample_submission.csv` (3374 bytes); columns: ["StudentID", "GradeClass"]
- `data/test.csv` (22667 bytes); columns: ["StudentID", "Age", "Gender", "Ethnicity", "ParentalEducation", "StudyTimeWeekly", "Absences", "Tutoring", "ParentalSupport", "Extracurricular", "Sports", "Music", "Volunteering"]
- `data/train.csv` (94020 bytes); columns: ["StudentID", "Age", "Gender", "Ethnicity", "ParentalEducation", "StudyTimeWeekly", "Absences", "Tutoring", "ParentalSupport", "Extracurricular", "Sports", "Music", "Volunteering", "GradeClass"]

## Public description

Competition: Ordinal Student Grade Classification

Problem statement
You are given student records with demographic, behavioral, and support-related attributes. Your task is to predict each student’s end-of-term GradeClass, an ordinal label where 0 represents the highest performance and 4 represents the lowest. The labels are ordered, so predicting a class close to the true class is better than predicting a distant one.

Data description
Each row corresponds to one student.
- Identifier: StudentID (unique per student; used for submission alignment)
- Features:
  - Age (numeric)
  - Gender (categorical; encoded as 0/1)
  - Ethnicity (categorical; encoded as integer levels)
  - ParentalEducation (ordinal/categorical; integer levels)
  - StudyTimeWeekly (numeric; hours per week)
  - Absences (numeric; number of missed school days)
  - Tutoring (binary; 0/1)
  - ParentalSupport (ordinal/categorical; integer levels)
  - Extracurricular (binary; 0/1)
  - Sports (binary; 0/1)
  - Music (binary; 0/1)
  - Volunteering (binary; 0/1)
- Target:
  - GradeClass (ordinal class in {0, 1, 2, 3, 4}; 0 is the best, 4 is the worst)

Note: A continuous GPA feature is intentionally excluded from the competition files to prevent target leakage.

Files provided
- train.csv: Training data containing StudentID, all feature columns, and the target column GradeClass.
- test.csv: Test data containing StudentID and all feature columns. The GradeClass column is withheld.
- sample_submission.csv: Example submission with random but valid labels.

Submission format
Submit a single CSV file with the following columns and no index:
- StudentID
- GradeClass
Each StudentID in the test set must appear exactly once. GradeClass must be an integer in {0, 1, 2, 3, 4}.

Evaluation
Submissions are evaluated using Quadratic Weighted Kappa (QWK) between the true GradeClass and your predictions. QWK measures agreement on an ordinal scale and penalizes larger mistakes more than smaller ones. The score ranges from -1 (complete disagreement) to 1 (perfect agreement), with 0 indicating chance-level agreement.

Why this is challenging and meaningful
- Ordinal target: GradeClass has meaningful order, encouraging the use of ordinal-aware models or losses.
- Mixed feature types: Numeric, binary, and categorical features require careful preprocessing/encoding.
- Class imbalance: Some grade tiers may be less frequent, rewarding robust modeling and calibration.
- Realistic setting: Signals like attendance and study time are predictive but imperfect, requiring thoughtful feature engineering and modeling.

Recommended approaches
- Handle categorical features via encoders (e.g., one-hot, target, ordinal encodings) or tree-based models that handle integers as categories.
- Consider ordinal regression losses or post-processing (e.g., thresholding) for classifiers.
- Use stratified cross-validation and monitor QWK during model selection.
- Apply regularization and robust scaling for outlier-resistant performance.

Good luck!
