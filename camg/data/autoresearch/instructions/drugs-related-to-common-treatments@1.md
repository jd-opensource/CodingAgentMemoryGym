# OpenMLE-fast task

Task ID: `drugs-related-to-common-treatments@1`

Native metric: `DrugsActivityRankingMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4007 bytes)
- `data/sample_submission.csv` (14304 bytes); columns: ["row_id", "activity"]
- `data/test.csv` (1768848 bytes); columns: ["row_id", "drug_name", "medical_condition", "medical_condition_description", "rx_otc", "pregnancy_category", "csa", "alcohol"]
- `data/train.csv` (6847532 bytes); columns: ["row_id", "drug_name", "medical_condition", "medical_condition_description", "rx_otc", "pregnancy_category", "csa", "alcohol", "activity"]

## Public description

Title: Condition-aware Drug Activity Ranking Challenge

Problem statement
Given a medical condition and a drug entry with accompanying attributes and text, predict the drug’s activity score (0–100) and, by extension, produce a high-quality ranking of drugs within each condition. The activity score reflects recent relative interest compared with peer drugs for the same condition.

You will build models that learn from multi-modal features (text + categorical attributes) to produce accurate per-condition rankings.

Files provided
- train.csv: Training data with features and the target activity.
- test.csv: Test data with features only.
- sample_submission.csv: A valid submission example with random predictions.

Do not assume any extra files. The objective is to predict activity for rows in test.csv.

Columns
Input features in train.csv and test.csv:
- row_id: Unique identifier of the row. Use this to align predictions with rows in the test set.
- drug_name: Drug name string (may include generic/brand/combinations).
- medical_condition: Condition the drug is associated with. The ranking is evaluated within each condition.
- medical_condition_description: Textual description of the medical condition.
- rx_otc: Categorical: {Rx, Rx/OTC, OTC}. Missing values may appear.
- pregnancy_category: Categorical: {A,B,C,D,X,N}. Missing values may appear.
- csa: Categorical Controlled Substances Act schedule: {N,1,2,3,4,5,M,U}. Missing values may appear.
- alcohol: Binary-like flag: value "X" means interaction with alcohol is noted; missing means not flagged.

Target in train.csv only:
- activity: Numeric target in the range [0, 100]. This reflects recent relative interest. It is not present in test.csv.

Submission format
- A CSV with exactly two columns and a header: row_id,activity
- row_id must exactly match those in test.csv (order does not matter).
- activity must be numeric; any real number is accepted. Continuous scores are typical, as their ordering produces the ranking.

Evaluation metric
- Primary metric: Mean NDCG@50 (linear gain), computed condition-wise and averaged across medical conditions present in the test set.
  - For each medical_condition, we compute DCG@50 over the test rows for that condition using the ground-truth activity as graded relevance and the submission’s predicted scores for ranking. Linear gain is used: DCG@K = sum_{i=1..K} rel_i / log2(i+1), where rel_i is the ground-truth activity of the i-th ranked item for the condition.
  - We compute the ideal DCG@50 (IDCG@50) by sorting by true activity descending and apply the same formula. If IDCG@50 is 0 (e.g., all relevances are 0), the NDCG for that condition is defined as 1.0.
  - The final score is the unweighted mean of per-condition NDCG@50 across all conditions represented in test.csv.

Recommended approach (non-binding)
- Text features: drug_name and medical_condition_description can be featurized via TF-IDF, bag-of-ngrams, or transformer embeddings. Lowercasing and basic normalization are typical starting points.
- Categorical features: one-hot encode rx_otc, pregnancy_category, csa; handle missing explicitly. Encode alcohol as a binary indicator.
- Model: Any regressor/ranker producing continuous scores (e.g., gradient boosting, linear models over n-grams, or neural models). You may train a regressor on activity and use the predicted scores for ranking, or directly use pairwise/listwise ranking losses.

Data split protocol (how this dataset was prepared)
- The split is stratified by medical_condition: within each condition, a fixed random seed determines an 80/20 split to test while ensuring at least 5 items in test when the condition has sufficient size. Small conditions are kept with at least one training example and at least one test example when possible. All test conditions also appear in training.

What to submit
- Submit a CSV with columns row_id,activity for every row in test.csv. Your score on the leaderboard is the Mean NDCG@50 described above.
