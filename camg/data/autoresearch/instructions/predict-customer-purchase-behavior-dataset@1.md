# OpenMLE-fast task

Task ID: `predict-customer-purchase-behavior-dataset@1`

Native metric: `CustomerPurchaseBehaviorMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2683 bytes)
- `data/sample_submission.csv` (3785 bytes); columns: ["row_id", "purchase_probability"]
- `data/test.csv` (16234 bytes); columns: ["row_id", "Age", "Gender", "AnnualIncome", "NumberOfPurchases", "ProductCategory", "TimeSpentOnWebsite", "LoyaltyProgram", "DiscountsAvailed"]
- `data/train.csv` (67537 bytes); columns: ["row_id", "Age", "Gender", "AnnualIncome", "NumberOfPurchases", "ProductCategory", "TimeSpentOnWebsite", "LoyaltyProgram", "DiscountsAvailed", "PurchaseStatus"]

## Public description

Title: Predict Customer Purchase Intention from Behavior and Demographics

Problem statement
Predict the likelihood that a customer will make a purchase based on demographics, browsing behavior, loyalty status, and discount usage. For each row in the test set, submit a calibrated probability of purchase for the positive class (PurchaseStatus = 1).

Data description
A curated train/test split is provided with mixed numerical and categorical features:
- Age (numeric)
- Gender (binary: 0=Male, 1=Female)
- AnnualIncome (numeric, USD)
- NumberOfPurchases (integer count)
- ProductCategory (categorical integer: 0–4)
- TimeSpentOnWebsite (numeric, minutes)
- LoyaltyProgram (binary: 0/1)
- DiscountsAvailed (integer count, 0–5)
Target label:
- PurchaseStatus (binary: 0=No, 1=Yes)

Provided files
- train.csv: Contains row_id, all eight features, and the target PurchaseStatus.
- test.csv: Contains row_id and all eight features (no target).
- sample_submission.csv: Shows the required submission format with random but valid probabilities.

Submission format
- A single CSV with exactly two columns:
  - row_id: The identifier provided in test.csv.
  - purchase_probability: The predicted probability of PurchaseStatus=1 for each row.
- Requirements:
  - Include every row from test.csv exactly once; row_id order must match test.csv.
  - Probabilities must be numeric, finite, and in [0, 1].

Evaluation metric
- Primary metric: ROC AUC (Area Under the Receiver Operating Characteristic Curve).
- Your purchase_probability values are compared with hidden test labels to compute ROC AUC.
- Fairness and precision:
  - Threshold-independent and robust to mild class imbalance.
  - Standard tie handling by average rank; probabilities are validated and clipped to [0,1] during scoring.

Guidance and expectations
- Use the full training set for modeling. Internal cross-validation is encouraged on train.csv.
- Suggested processing:
  - Encode categorical variables (e.g., one-hot or target encoding for ProductCategory).
  - Scale or normalize numerical features if beneficial.
  - Engineer interactions and consider non-linear models (e.g., tree ensembles) to capture relationships among browsing time, discounts, loyalty, and income.
  - Calibrate outputs (e.g., Platt scaling or isotonic) to improve probability quality.
- No missing values are present; expect wide ranges in AnnualIncome and TimeSpentOnWebsite. Robust scaling and regularization can help.

Goal
Develop a strong ML pipeline covering data processing, feature engineering, model training, calibration, and careful evaluation to produce high-quality purchase probabilities that maximize ROC AUC on the test set.
