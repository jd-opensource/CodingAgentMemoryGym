# OpenMLE-fast task

Task ID: `fortune-500-companies@1`

Native metric: `FortuneIndustryClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2925 bytes)
- `data/sample_submission.csv` (86361 bytes); columns: ["id", "industry"]
- `data/test.csv` (147161 bytes); columns: ["id", "rank", "year", "headquarters_state", "headquarters_city", "market_value_mil", "revenue_mil", "profit_mil", "asset_mil", "employees", "founder_is_ceo", "female_ceo", "newcomer_to_fortune_500", "global_500"]
- `data/train.csv` (769954 bytes); columns: ["rank", "year", "industry", "headquarters_state", "headquarters_city", "market_value_mil", "revenue_mil", "profit_mil", "asset_mil", "employees", "founder_is_ceo", "female_ceo", "newcomer_to_fortune_500", "global_500"]

## Public description

Competition: Fortune 500 Industry Classifier (1996–2023)

Problem statement
Given a company-year profile from the Fortune 500 (financials, headquarters, governance flags, rank, year), predict its industry category. This is a 94-class multiclass classification problem. The same company may appear across multiple years; the data split is grouped so that the same company never appears in both train and test, forcing models to generalize beyond memorizing identities.

Files
- train.csv: Features and the target industry label for training.
- test.csv: Features only; participants must predict the industry label for each row.
- sample_submission.csv: Example submission file containing the required columns and a random valid industry label for each test row.

Target
- industry: One of 94 industry categories used by Fortune.

Features
The following columns are provided as model inputs:
- year (int)
- rank (int)
- revenue_mil (numeric)
- profit_mil (numeric)
- asset_mil (numeric)
- market_value_mil (numeric)
- employees (numeric; may be provided in scientific notation)
- headquarters_state (string; two-letter state code or empty)
- headquarters_city (string; city name or empty)
- founder_is_ceo (string; typically "yes"/"no" or empty)
- female_ceo (string; typically "yes"/"no" or empty)
- newcomer_to_fortune_500 (string; typically "yes"/"no" or empty)
- global_500 (string; typically "yes"/"no" or empty)

Notes
- The train/test split is grouped by company to avoid leakage and stratified to preserve industry distribution. All industries present in test are guaranteed to appear in train at least once.
- Certain columns that could cause leakage or redundancy (such as the company name and a coarser sector taxonomy) are not included as features.
- Missing values are present in several numeric and categorical fields; thoughtful preprocessing and encoding are essential.

Evaluation
Submissions are evaluated using macro-averaged F1 score over all industry classes present in the test set. For each class c:
- precision_c = TP_c / (TP_c + FP_c), recall_c = TP_c / (TP_c + FN_c)
- F1_c = 2 * precision_c * recall_c / (precision_c + recall_c) (defined as 0 if precision_c + recall_c = 0)
The final score is the unweighted mean of F1_c across classes.

Submission format
- A CSV file with exactly two columns: id, industry
- The id values must match those in test.csv exactly and appear once each.
- The industry values should be predicted labels as strings.

Recommended approaches
- Robust missing-value handling for financials and employees; consider log1p transforms for heavy-tailed numerics.
- Careful encoding of high-cardinality categoricals (e.g., city) and binary flags.
- Use grouped cross-validation by company to mimic the leaderboard split and avoid leakage.
- Models such as gradient-boosted trees, regularized linear models, and tabular neural networks can perform well with appropriate features.
