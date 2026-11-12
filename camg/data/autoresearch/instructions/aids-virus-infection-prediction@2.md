# OpenMLE-fast task

Task ID: `aids-virus-infection-prediction@2`

Native metric: `AIDSOffTreatmentDiscontinuationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2954 bytes)
- `data/sample_submission.csv` (364392 bytes); columns: ["id", "offtrt"]
- `data/test.csv` (824968 bytes); columns: ["id", "trt", "age", "wtkg", "hemo", "homo", "drugs", "karnof", "oprior", "z30", "preanti", "race", "gender", "str2", "strat", "symptom", "treat", "cd40", "cd80"]
- `data/train.csv` (3404817 bytes); columns: ["id", "trt", "age", "wtkg", "hemo", "homo", "drugs", "karnof", "oprior", "z30", "preanti", "race", "gender", "str2", "strat", "symptom", "treat", "offtrt", "cd40", "cd80"]

## Public description

Early Off-Treatment Discontinuation Prediction (Group-averaged ROC-AUC)

Problem statement
- Predict the risk that an HIV/AIDS clinical-trial participant will discontinue antiretroviral therapy early (offtrt = 1) using only baseline and pre-enrollment information.
- The objective is to rank patients by discontinuation risk robustly across treatment arms.

Data files
- train.csv: Tabular training data with all input features and the binary target column offtrt.
- test.csv: Test data with the same feature columns as train.csv (excluding offtrt). An id column is provided to map rows to the submission format.
- sample_submission.csv: Example submission with columns [id, offtrt], where offtrt is a predicted probability in [0, 1].

Features and target
- Target: offtrt (0 = remained on treatment to ~96 weeks, 1 = discontinued early).
- Grouping variable for evaluation: trt (treatment arm; values in {0, 1, 2, 3}).
- Provided features are baseline/pre-enrollment variables (e.g., age, wtkg, hemo, homo, drugs, karnof, oprior, z30, preanti, race, gender, str2, strat, symptom, trt, treat, cd40, cd80). No post-baseline or future-dependent variables are present in the provided train/test files.

Submission format
- A CSV file with header containing exactly two columns in this order:
  1) id: integer identifier matching the ids in test.csv
  2) offtrt: predicted probability that offtrt = 1 for each id (values must lie within [0, 1])

Evaluation
- Primary metric: Group-averaged ROC-AUC across treatment arms (trt).
  1) For each treatment arm value g ∈ {0, 1, 2, 3} present in the test set, compute ROC-AUC between the true offtrt labels and the submitted probabilities for rows with trt = g.
  2) The final score is the unweighted mean of the per-arm ROC-AUC values.
  3) If an arm in the test set contains only one class (all 0 or all 1), its ROC-AUC is defined as 0.5 (random performance) to avoid undefined values.
- Why this metric: ROC-AUC is threshold-independent and robust to class imbalance. Arm-wise averaging prevents domination by the largest arm and encourages subgroup robustness, reflecting real-world generalization across regimens.

Guidance and recommendations
- Use appropriate preprocessing. Typical baselines include one-hot encoding for categorical variables (e.g., trt, strat) and scaling for numeric variables (e.g., age, wtkg, karnof, preanti, cd40, cd80).
- Expect moderate class imbalance; consider calibrated probabilities, regularization, and class-weighted models.
- Use cross-validation as needed to estimate generalization. Do not engineer features that use future information not present in train.csv/test.csv.

Reproducibility and split policy
- The official train/test split is deterministic and stratified by the target within each treatment arm, ensuring coverage across arms. Each arm represented in the test set contains both classes when available in the full data, making per-arm ROC-AUC well-defined.
