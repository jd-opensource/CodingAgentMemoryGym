# OpenMLE-fast task

Task ID: `loan-default@2_duplicate_1`

Native metric: `LoanDefaultMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3373 bytes)
- `data/sample_submission.csv` (1546115 bytes); columns: ["LoanID", "DefaultProbability"]
- `data/test.csv` (4863268 bytes); columns: ["LoanID", "Age", "Income", "LoanAmount", "CreditScore", "MonthsEmployed", "NumCreditLines", "InterestRate", "LoanTerm", "DTIRatio", "Education", "EmploymentType", "MaritalStatus", "HasMortgage", "HasDependents", "LoanPurpose", "HasCoSigner"]
- `data/train.csv` (19869653 bytes); columns: ["LoanID", "Age", "Income", "LoanAmount", "CreditScore", "MonthsEmployed", "NumCreditLines", "InterestRate", "LoanTerm", "DTIRatio", "Education", "EmploymentType", "MaritalStatus", "HasMortgage", "HasDependents", "LoanPurpose", "HasCoSigner", "Default"]

## Public description

Title: Default Risk Ranking: Who is most likely to default?

Background
Credit risk teams must prioritize borrowers by likelihood of default to allocate underwriting resources, design interventions, and manage portfolio risk. This competition asks you to model default risk at loan origination and produce a ranking of loans by risk.

Problem statement
Given borrower demographics, employment, credit attributes, and loan terms at origination, predict the likelihood that a loan will default. Submit a continuous risk score per loan; the leaderboard evaluates how well your scores rank defaulters above non-defaulters.

Data description
- Rows: 255,347 loans.
- Target: Default (binary: 1 = default, 0 = non-default). Positive rate ≈ 11.6%.
- Identifier: LoanID (unique per loan). Use this only to align predictions; do not use it as a feature.
- Features: All columns except LoanID and Default are available for modeling. Typical columns include: Age, Income, LoanAmount, CreditScore, MonthsEmployed, NumCreditLines, InterestRate, LoanTerm, DTIRatio, Education, EmploymentType, MaritalStatus, HasMortgage, HasDependents, LoanPurpose, HasCoSigner.
- Missing values: None in the provided dataset.

Files provided
- train.csv: Training data with all features plus the target column Default.
- test.csv: Test data with the same features as train.csv except Default (not provided). Includes LoanID for alignment.
- sample_submission.csv: Example submission with two columns: LoanID and DefaultProbability.

Submission format
- A CSV file with exactly two columns:
  - LoanID: Must match the IDs in test.csv.
  - DefaultProbability: A numeric risk score for default. Any real-valued score is accepted for ranking; for calibration (tie-breaker), scores will be clipped to [0,1].
- Every LoanID in test.csv must appear exactly once in your submission. No extra or missing IDs. No duplicates. All score values must be finite numbers (no NaN/Inf).

Evaluation
- Primary metric: ROC-AUC computed on the test set using your submitted DefaultProbability scores. ROC-AUC focuses on ranking quality and is robust to class imbalance.
- Tie-breaker metric: LogLoss computed on the same predictions after clipping to [0,1]. This rewards better-calibrated probabilities when ROC-AUC ties.
- The public leaderboard uses ROC-AUC; LogLoss is used only to break ties when ROC-AUC is identical.

Split strategy
- A deterministic stratified split (80% train, 20% test) is applied to the full dataset, ensuring both classes appear in the training set and that class distribution is preserved in the test set.

Modeling guidance
- Recommended practices:
  - Exclude LoanID from features to avoid leakage and overfitting.
  - Fit preprocessing (e.g., one-hot encoding for categorical features, scaling for numeric features) on training data only.
  - Use stratified cross-validation for model selection.
  - Consider class imbalance techniques (e.g., class weights, focal loss, threshold tuning) if optimizing for calibration.
- Suitable models include tree ensembles (e.g., XGBoost, LightGBM, CatBoost), regularized linear models with interactions, and modern tabular neural networks.

Goal
Produce a submission that ranks higher-risk loans above lower-risk loans, maximizing ROC-AUC on the test set. The dataset size and cleanliness are designed to support strong, reproducible modeling results.
