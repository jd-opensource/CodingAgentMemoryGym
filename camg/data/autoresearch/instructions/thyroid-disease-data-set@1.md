# OpenMLE-fast task

Task ID: `thyroid-disease-data-set@1`

Native metric: `ThyroidDiseaseMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3212 bytes)
- `data/sample_submission.csv` (18128 bytes); columns: ["id", "target"]
- `data/test.csv` (56126 bytes); columns: ["id", "age", "sex", "on thyroxine", "query on thyroxine", "on antithyroid medication", "sick", "pregnant", "thyroid surgery", "I131 treatment", "query hypothyroid", "query hyperthyroid", "lithium", "goitre", "tumor", "hypopituitary", "psych", "TSH measured", "T3 measured", "TT4 measured", "T4U measured", "FTI measured", "TSH", "T3", "TT4", "T4U", "FTI"]
- `data/train.csv` (229555 bytes); columns: ["id", "age", "sex", "on thyroxine", "query on thyroxine", "on antithyroid medication", "sick", "pregnant", "thyroid surgery", "I131 treatment", "query hypothyroid", "query hyperthyroid", "lithium", "goitre", "tumor", "hypopituitary", "psych", "TSH measured", "T3 measured", "TT4 measured", "T4U measured", "FTI measured", "TSH", "T3", "TT4", "T4U", "FTI", "target"]

## Public description

Problem: Predict hypothyroidism from mixed clinical and laboratory tabular data

Overview
- Task: Given patient demographics, clinical flags (e.g., on thyroxine, antithyroid meds, goitre), and thyroid lab test results when measured, predict the probability that the patient is hypothyroid (target = 1) versus euthyroid (target = 0).
- Context: Real-world thyroid screening mixes clinical indicators with labs (TSH, TT4, T4U, FTI, optionally T3). Records contain structured missingness depending on which tests were measured. Prior treatments and history may confound lab values, and measurement flags are informative.

Files provided
- train.csv: Training set with features and the target column for learning.
- test.csv: Test set with the same features but without the target.
- sample_submission.csv: Example submission file with the correct format.

Target
- Binary classification target named target.
  - 1 = hypothyroid (positive)
  - 0 = euthyroid (negative)

Features
- Demographics and clinical flags (mostly binary 0/1):
  - age, sex (1 = male, 0 = female, missing if unknown)
  - on thyroxine, query on thyroxine, on antithyroid medication, sick, pregnant, thyroid surgery, I131 treatment, query hypothyroid, query hyperthyroid, lithium, goitre, tumor, hypopituitary, psych
- Lab measurement flags (binary 0/1):
  - TSH measured, T3 measured (if available), TT4 measured, T4U measured, FTI measured
- Lab results (numeric; may be missing if not measured or not available):
  - TSH, T3 (if available), TT4, T4U, FTI

Notes on missingness and fairness
- Measurement flags indicate whether a lab value was measured in that encounter and are included as explicit features.
- Some lab values may be missing even when measured. Participants should handle missing values appropriately.
- Irrelevant or potentially confounding identifiers (e.g., site/referral source) are excluded to improve generalization.

Evaluation
- Submissions must predict probabilities for the positive class (target = 1) for each row in test.csv.
- Metric: ROC AUC (Area Under the Receiver Operating Characteristic Curve).
  - Why ROC AUC: It is threshold-independent, robust to class imbalance, and focuses on ranking quality. It is standard for imbalanced medical classification tasks.

Submission format
- CSV file with two columns and a header:
  - id: integer identifier for each test row (matches the id column in test.csv)
  - target: predicted probability in [0, 1] that the row belongs to the positive class (hypothyroid)
- The number of rows must exactly match test.csv, and ids must match one-for-one.

Train/test split
- A single stratified split is used to form train.csv and test.csv, preserving class balance. The split is deterministic so participants can reproduce local validation.

Modeling tips (optional)
- Use measurement flags to mask/impute labs correctly. For example, avoid imputing lab values when the corresponding measured flag is 0.
- Nonlinear models (e.g., gradient boosting) and careful preprocessing (log transforms, robust scalers, missing-value strategies) can improve performance.
- Consider calibration if you care about well-calibrated probabilities, although the leaderboard metric is ROC AUC.
