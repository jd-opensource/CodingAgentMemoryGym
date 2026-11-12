# OpenMLE-fast task

Task ID: `u-s-first-names-popularity-and-counts@2`

Native metric: `NamePopularityPairwiseMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2125 bytes)
- `data/sample_submission.csv` (13182 bytes); columns: ["pair_id", "p"]
- `data/test.csv` (26433 bytes); columns: ["pair_id", "name1", "sex1", "name2", "sex2"]
- `data/train.csv` (456521 bytes); columns: ["pair_id", "name1", "sex1", "name2", "sex2", "y"]

## Public description

Title: Name Popularity Head-to-Head (Pairwise Ranking)

Overview
Predict which of two U.S. first names is more popular. Each example is a pair of names with their associated sex; your task is to output the probability that name1 is more popular than name2. Popularity is defined by historical usage counts (not provided in the files). This is a learning-to-rank task over names using only name strings and sex.

Files (under public/)
- train.csv: Training pairs with labels.
  - columns: pair_id, name1, sex1, name2, sex2, y
  - y ∈ {0,1} indicates whether name1 is more popular than name2.
- test.csv: Test pairs without labels.
  - columns: pair_id, name1, sex1, name2, sex2
- sample_submission.csv: Example submission file with random but valid probabilities.
  - columns: pair_id, p
  - p is your predicted probability P(name1 more popular than name2).

Task
Given train.csv, build a model that maps (name, sex) to a scalar popularity score and outputs calibrated probabilities for test.csv comparisons.

Data description
- Name strings are typical U.S. first names (case-preserved as in source). Sex values are in {male, female}.
- Labels were created by comparing underlying usage counts (hidden). Counts and ranks are not included anywhere in the competition files to avoid leakage.
- Split protocol: unique names were split into train and test sets stratified by sex. Pairwise examples were then generated within each split, including within-sex and cross-sex pairs. There are no ties in the labels used.

Evaluation
- Metric: Binary log loss (cross-entropy) on the probability p for each test pair.
  - For each pair i with ground-truth y_i ∈ {0,1} and prediction p_i ∈ [0,1],
    LogLoss = −(1/N) * Σ [ y_i * log(p_i) + (1 − y_i) * log(1 − p_i) ].
  - Submissions must contain exactly the columns: pair_id, p. pair_id must match test.csv.

Deliverables
- Submit a CSV with columns pair_id, p for all rows in public/test.csv.

Reproducibility and fairness
- Names in test do not appear in train. Counts and ranks are never present in the released files. The split and pair generation are deterministic.
