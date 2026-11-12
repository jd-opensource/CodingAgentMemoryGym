# OpenMLE-fast task

Task ID: `students-employability-dataset@1`

Native metric: `StudentsEmployabilityMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2464 bytes)
- `data/sample_submission.csv` (22647 bytes); columns: ["id", "probability_of_Employable"]
- `data/test.csv` (19856 bytes); columns: ["id", "GENERAL APPEARANCE", "MANNER OF SPEAKING", "PHYSICAL CONDITION", "MENTAL ALERTNESS", "SELF-CONFIDENCE", "ABILITY TO PRESENT IDEAS", "COMMUNICATION SKILLS", "Student Performance Rating"]
- `data/train.csv` (72551 bytes); columns: ["id", "GENERAL APPEARANCE", "MANNER OF SPEAKING", "PHYSICAL CONDITION", "MENTAL ALERTNESS", "SELF-CONFIDENCE", "ABILITY TO PRESENT IDEAS", "COMMUNICATION SKILLS", "Student Performance Rating", "CLASS"]

## Public description

Mock Interview Employability Prediction (Philippines)

Problem statement
Given a candidate’s mock interview rubric scores, predict the probability that the candidate will be judged Employable. The task is binary classification with probability outputs, evaluated on ranking quality.

Data description
- Each row corresponds to one student evaluated in a mock job interview.
- Features (integer, ordinal): GENERAL APPEARANCE, MANNER OF SPEAKING, PHYSICAL CONDITION, MENTAL ALERTNESS, SELF-CONFIDENCE, ABILITY TO PRESENT IDEAS, COMMUNICATION SKILLS, Student Performance Rating.
- Target label: CLASS (binary: Employable, LessEmployable).
- Identifier: id (an anonymized student identifier; do not use it as a feature).
- No missing values; scores typically range from 2–5 for rubric traits and 3–5 for the overall rating.

Provided files
- train.csv: id, 8 features, and CLASS.
- test.csv: id and 8 features.
- sample_submission.csv: id and probability_of_Employable.

Submission format
Submit a CSV with exactly two columns:
- id: must match the provided ids in test.csv exactly (one row per id, unique).
- probability_of_Employable: a numeric value in [0, 1] representing the predicted probability that CLASS = Employable.

Evaluation metric
- Official metric: ROC AUC computed on the submitted probability_of_Employable against the true CLASS labels for the test set.
- Rationale: ROC AUC is threshold-free, robust to moderate class imbalance, and measures ranking quality directly.

Expectations for participants
- Use appropriate data processing (sanity-check feature ranges and types), feature engineering (respect ordinal nature of scores), model training (e.g., regularized logistic regression, calibrated gradient boosted trees with optional monotonic constraints), and probability calibration to improve ranking.
- Employ stratified cross-validation due to class imbalance (~58% Employable, ~42% LessEmployable).
- Do not use id as a feature; it is purely an identifier.

Guidance and caveats
- Consider that higher rubric scores should generally increase Employable probability; monotonic constraints can help enforce this.
- Beware of overfitting: small dataset size (~3k rows) warrants careful validation and robust pipelines.
- Treat features as ordinal integers; one-hot encoding is not required.

This competition focuses on practical HR analytics: ranking students by their employability potential using interpretable interview rubric scores.
