# OpenMLE-fast task

Task ID: `go-to-college-dataset@1`

Native metric: `CollegeEnrollmentMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2348 bytes)
- `data/sample_submission.csv` (6985 bytes); columns: ["id", "will_go_to_college"]
- `data/test.csv` (20828 bytes); columns: ["type_school", "school_accreditation", "gender", "interest", "residence", "parent_age", "parent_salary", "house_area", "average_grades", "parent_was_in_college", "id"]
- `data/train.csv` (49769 bytes); columns: ["type_school", "school_accreditation", "gender", "interest", "residence", "parent_age", "parent_salary", "house_area", "average_grades", "parent_was_in_college", "will_go_to_college", "id"]

## Public description

Title: Go-To-College: Predicting Probability of College Enrollment

Problem statement
You are given tabular records of high school students with demographic, socioeconomic, academic, and school-related attributes. Your task is to build a machine learning model that outputs calibrated probabilities for whether a student will go to college.

Data description
Each row corresponds to one student. Features include:
- type_school, school_accreditation, gender, interest, residence
- parent_age, parent_salary, house_area, average_grades
- parent_was_in_college
Target:
- will_go_to_college (binary outcome)

Provided files
- train.csv: All features and the target will_go_to_college.
- test.csv: All features and an id column; will_go_to_college is withheld.
- sample_submission.csv: A template containing id and will_go_to_college (probability).

Evaluation metric
Submissions must provide a probability for will_go_to_college in [0, 1] for every id in test.csv. The leaderboard is ranked using LogLoss (binary cross-entropy):
LogLoss = - (1/N) * Σ [ y_i * log(p_i) + (1 - y_i) * log(1 - p_i) ]
where y_i ∈ {0,1} is the ground truth and p_i ∈ (0,1) is the predicted probability. Probabilities are clipped to a small epsilon to avoid numerical issues. LogLoss is threshold-independent and rewards well-calibrated models.

Guidance and expectations
- Use all provided features; no external data.
- Carefully process mixed data types:
  - Encode categorical fields (e.g., one-hot or target/cat-boost encoding).
  - Consider ordinal treatment of interest if desired.
  - Standardize or transform skewed numeric variables (e.g., log-transform parent_salary).
- Train and validate on the training set only; the test set is strictly for inference.
- Strong baselines include regularized logistic regression and gradient boosting with proper encoding and calibration. Naive strategies (e.g., constant predictions) will perform poorly under LogLoss.

Submission format
Upload a CSV file with exactly two columns:
- id: Matches the ids in test.csv.
- will_go_to_college: A probability in [0, 1].

Notes
- The official split is stratified by the target to ensure both classes appear in the training set.
- The dataset is small-to-medium scale, making careful preprocessing, feature engineering, and model calibration important for competitive performance.
