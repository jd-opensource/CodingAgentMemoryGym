# OpenMLE-fast task

Task ID: `alcohol-effects-on-study@1`

Native metric: `StudentGradesPredictionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2669 bytes)
- `data/sample_submission.csv` (1568 bytes); columns: ["G3"]
- `data/test.csv` (33402 bytes); columns: ["school", "sex", "age", "address", "famsize", "Pstatus", "Medu", "Fedu", "Mjob", "Fjob", "reason", "guardian", "traveltime", "studytime", "failures", "schoolsup", "famsup", "paid", "activities", "nursery", "higher", "internet", "romantic", "famrel", "freetime", "goout", "Dalc", "Walc", "health", "absences", "subject"]
- `data/train.csv` (79714 bytes); columns: ["school", "sex", "age", "address", "famsize", "Pstatus", "Medu", "Fedu", "Mjob", "Fjob", "reason", "guardian", "traveltime", "studytime", "failures", "schoolsup", "famsup", "paid", "activities", "nursery", "higher", "internet", "romantic", "famrel", "freetime", "goout", "Dalc", "Walc", "health", "absences", "subject", "G3"]

## Public description

Title: Predict Final-Year Student Grades Without Prior Grades

Overview
Build a machine learning model to predict each student’s final-year grade (G3, range 0–20) using only non-leaky attributes describing demographics, study habits, social/health factors, alcohol consumption, and a subject indicator. The task spans two subjects (Mathematics and Portuguese) and focuses on understanding signals from lifestyle and study behavior without relying on earlier period grades.

Files provided
- train.csv: features plus target column G3.
- test.csv: the same features, without G3.
- sample_submission.csv: an example submission with the correct format.

Features
All exogenous attributes shared by both subjects, plus a subject indicator:
- school, sex, age, address, famsize, Pstatus, Medu, Fedu, Mjob, Fjob, reason, guardian,
- traveltime, studytime, failures, schoolsup, famsup, paid, activities, nursery, higher,
- internet, romantic, famrel, freetime, goout, Dalc, Walc, health, absences,
- subject (indicator: "Math" or "Portuguese").

Target
- G3: final grade (0–20).
- The earlier grades G1 and G2 are intentionally excluded to prevent label leakage.

Submission format
- A CSV containing exactly one column named G3.
- The number of rows must equal the number of rows in test.csv, and the order must match.
- Predictions may be real-valued floats; values outside the 0–20 range will be clipped during evaluation.

Evaluation metric
- Root Mean Squared Error (RMSE) on G3.
- RMSE penalizes large errors strongly, is well-suited to the 0–20 grade scale, and compares predictions fairly across both subjects.

Notes and guidance
- The data contains mixed types:
  - Binary/nominal categories (e.g., school, sex, address, famsize, Pstatus, Mjob, Fjob, reason, guardian, schoolsup, famsup, paid, activities, nursery, higher, internet, romantic, subject).
  - Ordinal/numeric features (e.g., age, traveltime, studytime, failures, famrel, freetime, goout, Dalc, Walc, health, absences).
- Recommended practices:
  - Encode categorical variables appropriately (e.g., one-hot for nominal; preserve order for ordinal).
  - Consider subject effects (Math vs Portuguese) and feature interactions.
  - Manage skew and scale for numeric features such as absences.
  - Use cross-validation to tune models and assess generalization.
- There are no missing values in the provided data.
- The split preserves both subjects in train and test for robust evaluation.

Goal
Develop accurate, generalizable predictors of student achievement from non-leaky behavioral and contextual signals, highlighting the relationships among study habits, alcohol consumption, and outcomes.
