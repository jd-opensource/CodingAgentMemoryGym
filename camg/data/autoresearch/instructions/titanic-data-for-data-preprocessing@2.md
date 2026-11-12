# OpenMLE-fast task

Task ID: `titanic-data-for-data-preprocessing@2`

Native metric: `TitanicFareMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2454 bytes)
- `data/sample_submission.csv` (3682 bytes); columns: ["row_id", "fare"]
- `data/test.csv` (11370 bytes); columns: ["row_id", "pclass", "sex", "age", "sibsp", "parch", "embarked", "who", "adult_male", "deck", "alone"]
- `data/train.csv` (30291 bytes); columns: ["row_id", "pclass", "sex", "age", "sibsp", "parch", "embarked", "who", "adult_male", "deck", "alone", "fare"]

## Public description

Titanic Ticket Fare Estimation Challenge

Problem statement:
Estimate the ticket fare paid by a Titanic passenger using their manifest attributes. You are provided with a training set containing passenger features and the target fare, and a test set containing the same features without the target. Build a robust regression pipeline that handles skewed targets, categorical variables, and missing values.

Data description:
- Train data file: train.csv
  - Columns: row_id, pclass, sex, age, sibsp, parch, embarked, who, adult_male, deck, alone, fare
  - The target is fare (non-negative continuous).
- Test data file: test.csv
  - Columns: row_id, pclass, sex, age, sibsp, parch, embarked, who, adult_male, deck, alone
  - No fare column is provided.
- Sample submission file: sample_submission.csv
  - Columns: row_id, fare
  - The sample contains random but valid placeholder predictions.

Notes on features and preprocessing:
- Categorical features include sex, embarked, who, deck; the deck and age fields have substantial missingness.
- Boolean-like fields adult_male and alone are provided as strings (TRUE/FALSE).
- Useful feature engineering may include: imputation (e.g., age by group medians), one-hot encoding for categorical variables, and careful treatment of rare categories.
- To avoid redundancy and potential leakage, columns such as survived, alive, class, and embark_town are excluded from the final files.

Evaluation metric:
- Submissions are evaluated using RMSLE (root mean squared logarithmic error) between predicted fares and the ground truth:
  - For each prediction y_pred and true fare y_true, we compute log1p(y) = ln(1 + y).
  - RMSLE = sqrt( mean( (log1p(max(y_pred, 0)) - log1p(max(y_true, 0)))^2 ) ).
  - Predictions less than 0 will be treated as 0 for scoring. All values must be finite; NaN/inf will be rejected.
- Rationale: RMSLE emphasizes relative error and is robust to the long-tailed distribution of fares.

Submission format:
- Submit a CSV file with the following columns:
  - row_id: the identifier aligned with the rows of test.csv
  - fare: your predicted fare for each row_id
- The set of row_id values must exactly match those in test.csv (order does not matter).

Goal:
Build a high-quality regression model with thoughtful preprocessing to minimize RMSLE on the test set. Handling missing values, encoding categorical variables, and coping with target skew will be essential for strong performance.
