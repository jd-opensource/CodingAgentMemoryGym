# OpenMLE-fast task

Task ID: `data-for-admission-in-the-university@1`

Native metric: `GraduateAdmissionsMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1902 bytes)
- `data/sample_submission.csv` (1858 bytes); columns: ["Id", "Chance of Admit"]
- `data/test.csv` (2334 bytes); columns: ["Id", "GRE Score", "TOEFL Score", "University Rating", "SOP", "LOR", "CGPA", "Research"]
- `data/train.csv` (10757 bytes); columns: ["Id", "GRE Score", "TOEFL Score", "University Rating", "SOP", "LOR", "CGPA", "Research", "Chance of Admit"]

## Public description

Title: Graduate Admissions Probability Prediction

Problem statement
Predict the Chance of Admit (a continuous value between 0 and 1) for graduate program applicants using standardized test scores, academic performance, and application strength indicators.

Data description
Each row represents an applicant. The provided features are:
- Id: Unique row identifier. Use it only for mapping submissions.
- GRE Score: Out of 340 (numeric).
- TOEFL Score: Out of 120 (numeric).
- University Rating: Ordinal 1–5.
- SOP: Statement of Purpose strength, ordinal 1–5.
- LOR: Letter of Recommendation strength, ordinal 1–5.
- CGPA: Undergraduate GPA on a 10-point scale (numeric).
- Research: Binary indicator (0/1).
Target label:
- Chance of Admit: Continuous value in [0,1].

Files
- train.csv: Contains Id, all features, and the target (Chance of Admit).
- test.csv: Contains Id and all features (no target).
- sample_submission.csv: Example submission file with the expected format.

Task guidance
- Clean column names (e.g., trim whitespace) and ensure numeric parsing of all features.
- Treat Research as numeric 0/1.
- Consider feature scaling, interaction features, regularization, and calibration.
- Models may include linear regression, tree-based methods, ensembles, etc.
- Ensure predictions lie within [0,1]; clipping extreme values is recommended.

Evaluation
- Metric: Root Mean Squared Error (RMSE) computed between submitted predictions and the true Chance of Admit values.
- Submission format: A CSV with exactly two columns: Id and Chance of Admit. Ids must match those in test.csv and the file must contain exactly one prediction per Id. Predictions must be finite numeric values in [0,1].

Notes
- The dataset has mixed scales and small sample size; robust validation and regularization will help generalization.
- Do not use Id as a feature; it is solely an identifier for alignment.
