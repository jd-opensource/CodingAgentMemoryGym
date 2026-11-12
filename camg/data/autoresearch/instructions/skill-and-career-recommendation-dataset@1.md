# OpenMLE-fast task

Task ID: `skill-and-career-recommendation-dataset@1`

Native metric: `CareerRecommendationMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/data_dictionary.json` (692 bytes)
- `data/description.txt` (3736 bytes)
- `data/sample_submission.csv` (1088077 bytes); columns: ["s/p", "Actor / Actress", "Actuary", "Anthropologist", "Archeologist", "Artist", "Astronomer", "Athlete", "Audiologist", "Banking", "Broadcaster", "Business Analyst", "Business manager", "Chartered Accountant", "Chief financial officer", "Company secretary", "Computer analyst", "Computer programmer", "Consultant", "Counselor", "Criminologist", "Dancer", "Database designer", "Economist", "Editor", "Engineer", "Fashion Designer", "Financial Advisor", "Geologist", "Graphic Designer", "Historian", "Interior Decorator", "Internal auditor", "Journalist", "Language Teacher", "Lawyer", "Leader", "Librarian", "Logistics manager", "Manager", "Marine Biologist", "Marketing", "Mathematician", "Mechanic", "Medical", "Middle, Higher School Teacher and Professors", "Militry", "Music teacher", "Nature photographer", "Para Medical (physiotherapy, occupational theropy, audio and speech language theropy, nursing)", "Para Militry (https://en.wikipedia.org/wiki/Paramilitary_forces_of_India)", "Pharmacist", "Philosopher", "Physical Therapist", "Physician", "Physicist", "Pilot", "Poet", "Police Force (Spies, CBI officials, CID, Detectives)", "Politician", "Pre Primary Teacher (2020 NEP and Mental Health)", "Primary Teacher", "Psychologist", "Receptionist", "Recording engineer", "Research analyst", "Sales Representative", "Social Worker", "Sound editor", "Stock Broker", "Technician", "Veterinarian", "Writer"]
- `data/test.csv` (62488 bytes); columns: ["s/p", "student", "linguistic", "musical", "bodily", "logical_mathematical", "spatial_visualization", "interpersonal", "intrapersonal", "naturalist", "P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P1_enc", "P2_enc", "P3_enc", "P4_enc", "P5_enc", "P6_enc", "P7_enc", "P8_enc"]
- `data/train.csv` (297108 bytes); columns: ["s/p", "student", "linguistic", "musical", "bodily", "logical_mathematical", "spatial_visualization", "interpersonal", "intrapersonal", "naturalist", "P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P1_enc", "P2_enc", "P3_enc", "P4_enc", "P5_enc", "P6_enc", "P7_enc", "P8_enc", "job_profession"]

## Public description

Title: 72-way Career Recommendation from Aptitude and Performance Profiles

Problem statement
Given a student’s aptitude scores (8 numeric multiple-intelligence dimensions) and performance indicators across 8 subjects/competencies (categorical: POOR/AVG/BEST), predict the most suitable job profession among 72 possible classes. Build a model that outputs calibrated probabilities for every profession.

Files
- train.csv: Training data with features and the target column job_profession.
- test.csv: Test data with the same feature schema as train.csv but without job_profession.
- sample_submission.csv: Example submission showing the required format (probabilities per profession that sum to 1 for each row).

Data description
Each row represents one unique student profile.
- s/p: Unique identifier for the row. Use this as the key in submissions.
- student: Secondary identifier (non-essential).
- Numeric aptitude features (integers):
  - linguistic, musical, bodily, logical_mathematical, spatial_visualization, interpersonal, intrapersonal, naturalist.
- Categorical performance indicators (strings in {POOR, AVG, BEST} with minor missingness):
  - P1, P2, P3, P4, P5, P6, P7, P8.
- Ordinal-encoded performance indicators (integers in {0,1,2}):
  - P1_enc, P2_enc, P3_enc, P4_enc, P5_enc, P6_enc, P7_enc, P8_enc.
- Target (train.csv only):
  - job_profession: One of 72 professions. The dataset is balanced with 50 examples per class.

Notes and conventions
- Column naming is standardized to lowercase with underscores (e.g., Logical - Mathematical → logical_mathematical; Spatial-Visualization → spatial_visualization). The label strings in job_profession (and in the submission headers) retain their original capitalization and spacing after trimming whitespace.
- The categorical P1..P8 columns may contain a few missing values. The corresponding _enc columns are ordinal encodings with missing values imputed using the mode computed from the training split (participants are free to re-impute as part of their pipelines).
- The columns Sr.No. and Course are not included because they are uninformative or largely missing.

Evaluation
- Metric: Multiclass Log Loss (cross-entropy) over the 72 professions.
  - For each test row i with true class y_i and submitted probability vector p_i over classes C,
    LogLoss = -(1/N) * sum_i log(max(eps, p_i[y_i])) with eps = 1e-15 to avoid log(0).
    Submissions are row-wise renormalized if needed, but exact one-hot rows are preserved.
  - This metric rewards well-calibrated probabilities and penalizes overconfident errors, which is important given the high number of classes and potential confusability.

Submission format
- A CSV with one row per s/p in the test set.
- Columns: s/p followed by 72 probability columns, one for each profession label present in job_profession.
- Requirements:
  - All test s/p must be present exactly once.
  - The set of profession columns must match the 72 labels used in the data (order does not matter).
  - Each row’s probabilities must be numeric and non-negative. The evaluator will handle minor deviations from row-sum=1 by renormalizing.

Train/test split
- The host split is stratified by job_profession to ensure every class appears in both train and test. The test labels are hidden and must be inferred from features.

Modeling hints
- Mixed tabular data benefits from careful preprocessing (e.g., ordinal encoding for P1..P8, handling missing values, feature scaling if using linear models).
- Gradient-boosted trees, regularized linear models with appropriate encodings, or calibrated ensembles are effective baselines.
- Given 72 classes with 50 examples each, probability calibration and regularization are important.
