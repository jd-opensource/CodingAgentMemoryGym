# OpenMLE-fast task

Task ID: `predicting-hiring-decisions-in-recruitment-data@1`

Native metric: `HiringDecisionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2736 bytes)
- `data/sample_submission.csv` (5776 bytes); columns: ["HiringDecision"]
- `data/test.csv` (12263 bytes); columns: ["Age", "Gender", "EducationLevel", "ExperienceYears", "PreviousCompanies", "DistanceFromCompany", "InterviewScore", "SkillScore", "PersonalityScore", "RecruitmentStrategy"]
- `data/train.csv` (51072 bytes); columns: ["Age", "Gender", "EducationLevel", "ExperienceYears", "PreviousCompanies", "DistanceFromCompany", "InterviewScore", "SkillScore", "PersonalityScore", "RecruitmentStrategy", "HiringDecision"]

## Public description

Title: Predicting Hiring Decisions in Recruitment Data

Background
Organizations evaluate candidates using education, experience, interview results, skills, personality, and recruitment strategy. Automating the prediction of hiring decisions can help standardize and improve recruitment efficiency while enabling better calibration of risk in human resources workflows.

Problem Statement
Given tabular candidate attributes, predict the probability that a candidate is hired. Your model should output well-calibrated probabilities for the binary target HiringDecision on held-out test data.

Data Description
- Rows: 1,500 candidates
- Features (10): Age, Gender, EducationLevel, ExperienceYears, PreviousCompanies, DistanceFromCompany, InterviewScore, SkillScore, PersonalityScore, RecruitmentStrategy
- Target: HiringDecision (0 = not hired, 1 = hired)
- All columns are numeric. EducationLevel, RecruitmentStrategy, and Gender are integer-coded categorical variables. There are no missing values.

Files Provided (after running prepare.py)
- train.csv: Training data including all features and the target column HiringDecision
- test.csv: Test data including all features without the target column
- sample_submission.csv: A valid example submission containing one column HiringDecision with probability values in [0, 1] for each row of the test set

Evaluation
Submissions must provide a single column HiringDecision containing the predicted probability of class 1 (hired) for each test row, in the same order as test.csv.

Primary Metric: Weighted Log Loss
We evaluate predictions using class-weighted log loss, where class weights are computed from the training set class prevalence to avoid leakage into the test set.
- Let y ∈ {0, 1} be the true label and p ∈ [0, 1] be the submitted probability for class 1.
- Per-sample loss: if y = 1, loss = −log(max(min(p, 1 − 1e-15), 1e-15)); if y = 0, loss = −log(max(min(1 − p, 1 − 1e-15), 1e-15)).
- Compute training class prevalences: p0_train = n0_train / (n0_train + n1_train), p1_train = n1_train / (n0_train + n1_train).
- Class weights: w0 = 1 / p0_train, w1 = 1 / p1_train.
- Final score: sum_i w_{y_i} * loss_i divided by sum_i w_{y_i}.
This metric rewards calibrated probabilities and reduces majority-class dominance while remaining sensitive to overconfident mistakes.

Notes
- Treat integer-coded categorical variables appropriately (e.g., one-hot encoding or learned embeddings) and consider scaling continuous variables for model stability.
- The split is stratified to preserve class balance; all test classes appear in training.
- To maximize performance, consider feature engineering, non-linear models, ensembles, and probability calibration techniques.
