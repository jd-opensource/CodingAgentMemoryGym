# OpenMLE-fast task

Task ID: `sales-and-customer-data@1`

Native metric: `DigitalSalesPaymentMethodMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2793 bytes)
- `data/sample_submission.csv` (324537 bytes); columns: ["row_id", "payment_method"]
- `data/test.csv` (1188758 bytes); columns: ["row_id", "category", "quantity", "price", "invoice_date", "shopping_mall", "gender", "age"]
- `data/train.csv` (4891863 bytes); columns: ["category", "quantity", "price", "invoice_date", "shopping_mall", "gender", "age", "payment_method"]

## Public description

Digital Sales & Customer Data Challenge: Predict Payment Method per Transaction

Problem statement
Build a machine learning model to predict the payment method used for each transaction in a multi-mall retail environment. You are given transactional basket attributes (category, quantity, price, date, mall) and customer demographics (age, gender). The task is to classify the payment method for unseen customers and transactions.

What you will model
- Input: Each row is a single transaction with fields such as category, quantity, price, invoice_date, shopping_mall, age, and gender.
- Target: payment_method with three classes: Credit Card, Debit Card, Cash.
- Constraint: The split is customer-disjoint to prevent memorization; customers in the test set do not appear in the training set.

Files provided
- train.csv: Transactions for training. Includes the target column payment_method.
- test.csv: Transactions for testing. Same feature columns as train.csv but without payment_method. Includes a unique row_id to key your predictions.
- sample_submission.csv: Example submission file containing row_id and a valid payment_method per row.

Data details
- Transactional attributes: category, quantity, price, invoice_date, shopping_mall.
- Customer attributes: age, gender.
- Identifiers: A synthetic row_id is provided for submission alignment. Operational identifiers like invoice_no and customer_id are not included to avoid leakage.
- Dates: The invoice_date is in day-month-year format. Feature engineering on dates (month, day-of-week, seasonality) is encouraged.

Evaluation
- Metric: Macro F1 score over the three classes (Credit Card, Debit Card, Cash). Macro F1 treats each class equally, rewarding a balance of precision and recall across classes and is robust to class imbalance.
- Submission format: CSV with exactly two columns: row_id and payment_method. The row_id must match those in test.csv, and payment_method must be one of the three allowed classes.

Guidelines and tips
- Feature engineering ideas: price × quantity (line value), log-transform of skewed numeric features, calendar features (month, weekday), and interactions between category, mall, and demographics.
- Categorical handling: Encode category, shopping_mall, and gender. Fit encoders only on training data, then transform test data consistently.
- Modeling: Gradient-boosted trees, calibrated linear models, and tabular neural networks are strong baselines. Tune class weights to handle any imbalance.
- Pitfalls to avoid: Do not use row_id, invoice_no, or customer_id as features. Ensure submission labels are exactly one of the three allowed values.

Submission
- Create a CSV with columns: row_id,payment_method
- Ensure every row_id from test.csv appears exactly once and that labels are valid.
