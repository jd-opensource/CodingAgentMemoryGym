# OpenMLE-fast task

Task ID: `advertising-sales-dataset@1`

Native metric: `AdvertisingSalesRegressionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2058 bytes)
- `data/sample_submission.csv` (1560 bytes); columns: ["row_id", "sales"]
- `data/test.csv` (1331 bytes); columns: ["row_id", "tv_budget", "radio_budget", "newspaper_budget"]
- `data/train.csv` (3123 bytes); columns: ["row_id", "tv_budget", "radio_budget", "newspaper_budget", "sales"]

## Public description

Title: Ad Budget to Sales – Robust Regression Challenge

Problem statement:
Predict retail sales ($) from channel-level advertising budgets. Each row records the budget allocation across TV, Radio, and Newspaper channels and the resulting sales. Your task is to build a model that generalizes well, especially to budget extremes and atypical mixes.

Files provided:
- train.csv: Training data with features and target.
- test.csv: Test data with features only. Submit predictions for its rows.
- sample_submission.csv: Example of the expected submission format.

Columns:
- row_id: Unique identifier for each row.
- tv_budget: TV advertising budget ($).
- radio_budget: Radio advertising budget ($).
- newspaper_budget: Newspaper advertising budget ($).
- sales: Sales ($). Present only in train.csv and in the expected submission; not present in test.csv.

Task details:
- Use all provided rows and features. The split is single and fixed.
- The test set is enriched with budget extremes (e.g., very high or very low values on one or more channels) to evaluate robustness beyond mid-range regimes. The training set still contains representative coverage across the range to keep the task solvable.

Submission:
- A CSV with columns: row_id, sales.
- Include one prediction per row_id from test.csv.

Evaluation metric:
- Root Mean Squared Error (RMSE) on sales.
- RMSE is computed between your submitted sales predictions and the ground truth sales of the test set. The metric is scale-consistent and penalizes larger errors more heavily, providing a precise and fair evaluation of forecasting quality.

Guidance:
- Explore linear and regularized regression, interaction terms (e.g., tv_budget × radio_budget), and nonlinear feature transforms if helpful.
- Pay attention to preprocessing (numeric types, scaling, outlier handling) and robust model validation.

Goal:
Deliver accurate, generalizable predictions across typical and extreme budget allocations using sound ML practices (data processing, feature engineering, model training, and evaluation).
