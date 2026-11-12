# OpenMLE-fast task

Task ID: `body-signal-of-smoking@1`

Native metric: `SmokingStatusMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2356 bytes)
- `data/sample_submission.csv` (279278 bytes); columns: ["ID", "smoking"]
- `data/test.csv` (1241423 bytes); columns: ["ID", "gender", "age", "height(cm)", "weight(kg)", "waist(cm)", "eyesight(left)", "eyesight(right)", "hearing(left)", "hearing(right)", "systolic", "relaxation", "fasting blood sugar", "Cholesterol", "triglyceride", "HDL", "LDL", "hemoglobin", "Urine protein", "serum creatinine", "AST", "ALT", "Gtp", "dental caries", "tartar"]
- `data/train.csv` (5054477 bytes); columns: ["ID", "gender", "age", "height(cm)", "weight(kg)", "waist(cm)", "eyesight(left)", "eyesight(right)", "hearing(left)", "hearing(right)", "systolic", "relaxation", "fasting blood sugar", "Cholesterol", "triglyceride", "HDL", "LDL", "hemoglobin", "Urine protein", "serum creatinine", "AST", "ALT", "Gtp", "dental caries", "tartar", "smoking"]

## Public description

Smoking status prediction from routine health signals

Problem
Build a machine learning model that predicts whether an individual is a current smoker based on routine health examination features. This is a binary classification task.

Data
You are provided with:
- train.csv: Training data containing feature columns and the target column smoking.
- test.csv: Test data containing the same feature columns as train.csv (except smoking).
- sample_submission.csv: A valid submission template with the required columns.

Columns
- ID: Unique identifier for each record (do not use as a predictive feature directly).
- gender: Categorical, values typically {M, F}.
- age: Age in 5-year bins (integer).
- height(cm), weight(kg), waist(cm): Anthropometrics.
- eyesight(left), eyesight(right): Numeric visual acuity measures.
- hearing(left), hearing(right): Ordinal hearing measures.
- systolic, relaxation: Blood pressure readings.
- fasting blood sugar
- Cholesterol (total)
- triglyceride
- HDL, LDL
- hemoglobin
- Urine protein
- serum creatinine
- AST, ALT, Gtp (liver enzymes)
- dental caries: Binary (0/1)
- tartar: Categorical {Y, N}
- smoking (train.csv only): Binary target {0, 1}

Note: The oral column present in some source versions is constant and excluded from the final files.

Task considerations
- Feature engineering (e.g., encoding for categorical variables, handling skewed distributions, interaction terms) can improve performance.
- Consider robust scaling or transformations for heavy-tailed labs (e.g., triglyceride, Gtp).
- Stratified cross-validation is recommended due to moderate class imbalance.

Submission format
- File must contain two columns with headers: ID, smoking.
- ID must match the test.csv IDs exactly (no duplicates or missing).
- smoking must be a probability in [0, 1] representing P(smoking=1).

Evaluation metric
- Primary metric: ROC-AUC (Area Under the Receiver Operating Characteristic Curve).
- The ROC-AUC is computed on your submitted probabilities against the hidden true labels.
- Higher is better; ties are handled correctly.

Files
- train.csv
- test.csv
- sample_submission.csv

Best practices
- Do not leak target information into features.
- Ensure consistent preprocessing across train/test (e.g., fit scalers on train only).
- Validate the submission format prior to upload to avoid scoring errors.
