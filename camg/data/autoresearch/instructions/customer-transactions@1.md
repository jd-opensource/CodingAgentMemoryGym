# OpenMLE-fast task

Task ID: `customer-transactions@1`

Native metric: `TransactionCategoryMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2431 bytes)
- `data/sample_submission.csv` (1145676 bytes); columns: ["TransactionID", "Clothing", "Cosmetic", "Electronics", "Market", "Restaurant", "Travel"]
- `data/test.csv` (511380 bytes); columns: ["TransactionID", "Gender", "Birthdate", "Transaction Amount", "Date", "Merchant Name"]
- `data/train.csv` (2703979 bytes); columns: ["TransactionID", "Gender", "Birthdate", "Transaction Amount", "Date", "Merchant Name", "Category"]

## Public description

Unseen-Merchant Transaction Category Classification

Problem
Predict the transaction category from merchant name text and contextual attributes. Models must generalize to merchants not seen during training.

Files
- Train: train.csv
  - Columns: TransactionID, Gender, Birthdate, Transaction Amount, Date, Merchant Name, Category
- Test: test.csv
  - Columns: TransactionID, Gender, Birthdate, Transaction Amount, Date, Merchant Name
- Sample submission: sample_submission.csv
  - Columns: TransactionID plus probability columns for each class in this exact order:
    Clothing, Cosmetic, Electronics, Market, Restaurant, Travel

Target
- Category ∈ {Clothing, Cosmetic, Electronics, Market, Restaurant, Travel}

Split design (important)
- Merchant-disjoint split: no merchant string in train appears in test. This prevents trivial memorization and stresses generalization to unseen merchants.
- All classes present in test also occur in train.

Modeling guidance
- Make use of both text and tabular signals:
  - Merchant Name: normalize text (lowercasing, punctuation stripping), tokenize, character/word n-grams, TF‑IDF, or learned embeddings.
  - Date: derive year, month, weekday, week-of-year, day-of-year, weekend/seasonality features.
  - Birthdate: compute age at transaction time; consider bucketing and interactions.
  - Transaction Amount: log-transform, scaling, interactions.
  - Gender: treat missing explicitly as its own category.
- Any supervised ML approach is allowed (linear models, tree-based methods, neural networks, etc.).

Evaluation
- Metric: Multiclass LogLoss (cross-entropy) averaged over all test rows.
- Submission format: probability distribution per test row over all 6 classes.
  - Columns: TransactionID, Clothing, Cosmetic, Electronics, Market, Restaurant, Travel
  - Each row’s probabilities must be non-negative, finite, and sum to 1 (submissions are normalized and clipped for stability, e.g., to [1e-15, 1]).
  - TransactionID values must match those in test.csv (order can differ; duplicates are not allowed).

Notes
- Personal-identifying fields (Customer ID, Name, Surname) are intentionally excluded from the train/test files.
- The dataset scale is preserved; you are encouraged to engineer features and blend modalities.
- Strong baselines include: logistic regression or linear SVM on TF‑IDF n‑grams + simple tabular features; or gradient-boosted trees with text encodings.
