# OpenMLE-fast task

Task ID: `stock-pledge-defaults-prediction@1`

Native metric: `StockPledgeDefaultRiskMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (943 bytes)
- `data/sample_submission.csv` (3192 bytes); columns: ["id", "IsDefault"]
- `data/test.csv` (148869 bytes); columns: ["id", "Z-SCORE", "Share pledge ratio of controlling shareholders", "Pledge ratio of limited sale shares", "Pledge ratio of unlimited shares", "Stock Volatility", "P/E ratio", "P/B ratio", "Stock price rise and fall in the last year", "Annual turnover rate", "ST", "ROA", "ROE", "changes in net assets", "changes in operating income", "Gross profit margin on sales", "Net business cycle (days)", "Turnover rate of accounts receivable (Times)", "Inventory turnover rate (Times)", "Total asset turnover rate (Times)", "Current ratio", "Cash ratio", "Asset liability ratio", "Asset liability ratio (excluding advance receipts)", "Asset liability ratio (total liabilities - contract liabilities - advance receipts)/(total assets - goodwill - contract liabilities - advance receipts)", "Current liabilities/total liabilities", "Monetary capital/short-term debt", "EBITDA/interest bearing debt", "EBIT interest cover", "EBITDA interest cover", "Net cash flow from operations has been negative for three consecutive years", "Average cash income ratio in recent three years", "Cash income ratio", "Ratio of accounts receivable to operating income", "Ratio of prepayments to operating income", "Ratio of other receivables to total assets", "Ratio of construction in progress to total assets", "Minority shareholders' equity/owners' equity", "The proportion of goodwill in total assets exceeds", "Downgrade or negative", "audit opinion ", "Company nature (state owned assets 0, others 1)", "High deposit and loan of 90p", "Company size (LN)", "Whether there are four major audits", "Proportion of independent directors", "Equity checks and balances (2-5 large/1 large)", "Two positions in one (1 for the same, 0 for the different)", "Equity concentration (the first largest shareholder)", "Total institutional shareholding ratio", "Audit fee", "Tobin Q", "Debt financing costs", "Enterprise age", "Goodwill impairment ratio", "Asset quality index", "SG&A Expense", "Number of key audit matters", "Number of research institutions concerned", "Number of research reports (+1 LN)", "Financial cycle m2/gdp"]
- `data/train.csv` (594352 bytes); columns: ["id", "Z-SCORE", "Share pledge ratio of controlling shareholders", "Pledge ratio of limited sale shares", "Pledge ratio of unlimited shares", "Stock Volatility", "P/E ratio", "P/B ratio", "Stock price rise and fall in the last year", "Annual turnover rate", "ST", "ROA", "ROE", "changes in net assets", "changes in operating income", "Gross profit margin on sales", "Net business cycle (days)", "Turnover rate of accounts receivable (Times)", "Inventory turnover rate (Times)", "Total asset turnover rate (Times)", "Current ratio", "Cash ratio", "Asset liability ratio", "Asset liability ratio (excluding advance receipts)", "Asset liability ratio (total liabilities - contract liabilities - advance receipts)/(total assets - goodwill - contract liabilities - advance receipts)", "Current liabilities/total liabilities", "Monetary capital/short-term debt", "EBITDA/interest bearing debt", "EBIT interest cover", "EBITDA interest cover", "Net cash flow from operations has been negative for three consecutive years", "Average cash income ratio in recent three years", "Cash income ratio", "Ratio of accounts receivable to operating income", "Ratio of prepayments to operating income", "Ratio of other receivables to total assets", "Ratio of construction in progress to total assets", "Minority shareholders' equity/owners' equity", "The proportion of goodwill in total assets exceeds", "Downgrade or negative", "audit opinion ", "Company nature (state owned assets 0, others 1)", "High deposit and loan of 90p", "Company size (LN)", "Whether there are four major audits", "Proportion of independent directors", "Equity checks and balances (2-5 large/1 large)", "Two positions in one (1 for the same, 0 for the different)", "Equity concentration (the first largest shareholder)", "Total institutional shareholding ratio", "Audit fee", "Tobin Q", "Debt financing costs", "Enterprise age", "Goodwill impairment ratio", "Asset quality index", "SG&A Expense", "Number of key audit matters", "Number of research institutions concerned", "Number of research reports (+1 LN)", "Financial cycle m2/gdp", "IsDefault"]

## Public description

Stock Pledge Default Risk — Tabular Classification Challenge

Problem statement
Predict whether a controlling shareholder’s stock-pledge financing will default (IsDefault = 1) or remain normal (IsDefault = 0) using company-level tabular features. Models should output calibrated probabilities of default for the provided test cases.

Public data files
- train.csv: Labeled tabular data. Columns include an identifier 'id', feature columns, and label 'IsDefault'.
- test.csv: Unlabeled tabular data. Columns include an identifier 'id' and the same feature columns as in train.csv (excluding IsDefault).
- sample_submission.csv: Example submission with columns [id, IsDefault] (probabilities).

Submission format
- CSV with two columns: id and IsDefault (predicted probability in [0, 1]) matching the ids in test.csv.

Evaluation metric
- ROC-AUC computed on predicted probabilities vs. the hidden ground-truth IsDefault for the test split.
