# OpenMLE-fast task

Task ID: `employeeturnover@1`

Native metric: `EmployeeChurnMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/comments_test.csv` (1710912 bytes); columns: ["employee", "companyAlias", "commentId", "txt", "likes", "dislikes", "commentDate"]
- `data/comments_train.csv` (7786952 bytes); columns: ["employee", "companyAlias", "commentId", "txt", "likes", "dislikes", "commentDate"]
- `data/description.txt` (3620 bytes)
- `data/interactions_test.csv` (2586318 bytes); columns: ["employee", "companyAlias", "liked", "disliked", "commentId"]
- `data/interactions_train.csv` (11279075 bytes); columns: ["employee", "companyAlias", "liked", "disliked", "commentId"]
- `data/sample_submission.csv` (24670 bytes); columns: ["uid", "churn_probability"]
- `data/test.csv` (19854 bytes); columns: ["uid"]
- `data/test_employees.csv` (39726 bytes); columns: ["companyAlias", "employee", "uid"]
- `data/train.csv` (86825 bytes); columns: ["uid", "churn"]
- `data/train_employees.csv` (167972 bytes); columns: ["companyAlias", "employee", "churn", "uid"]
- `data/votes_test.csv` (1374999 bytes); columns: ["employee", "companyAlias", "voteDate", "vote"]
- `data/votes_train.csv` (5805092 bytes); columns: ["employee", "companyAlias", "voteDate", "vote"]

## Public description

Employee Churn Risk Prediction from Mood and Social Engagement

Background
Companies use a workplace app where employees report daily happiness (1–4), post comments, and like/dislike peers’ comments. The challenge is to predict which employees are at risk of churning (quitting or being fired) using only behavioral signals available up to a fixed temporal cutoff.

Problem Statement
Given raw behavioral data strictly before a cutoff date, build a model that ranks employees by their probability of churn. You will receive employee-level train data with labels and an unseen test set without labels. Use votes, comments, and social interactions to engineer features that reflect engagement, happiness dynamics, and social reception. Your task is to submit a churn probability for each employee in the test set.

Data Provided
All behavioral events are pre-cut (strictly before 2016-12-01) and split by employee-level train/test membership. Use the following files:
- votes_train.csv, votes_test.csv: Daily happiness votes with timestamps and (employee, company) identifiers.
- comments_train.csv, comments_test.csv: Employee comments with like/dislike counts and timestamps.
- interactions_train.csv, interactions_test.csv: Like/dislike interactions on comments, joined to ensure the interacted comment occurred before the cutoff.
- train_employees.csv: Employee roster for training with labels.
- test_employees.csv: Employee roster for testing (no labels).
- sample_submission.csv: Example submission with random probabilities for the test roster.

Important notes
- Identity key: Use the composite (companyAlias, employee) to identify a person. Negative employee IDs are excluded.
- Temporal cutoff: All event tables are pre-filtered to events strictly before 2016-12-01 to prevent leakage. Do not attempt to infer labels from post-cut artifacts.
- Train/test split: Employees are split deterministically by company with stratification on churn label. Individuals never appear in both sets.

Recommended Feature Engineering (non-exhaustive)
- Engagement: number of voting days, posting frequency, inter-arrival time statistics, fraction of active weeks.
- Happiness dynamics: weekly mean/variance, trend/slope over recent weeks, transition probabilities of ordinal votes.
- Relative happiness: normalize an employee’s happiness by the company mean per week.
- Social signals: likes/dislikes received and given per week; acceptance ratios; z-scores relative to company-wide distributions.
- Time windows: compute features both over the full pre-cut period and recent windows (e.g., last 4/8 weeks).

Evaluation Metric
- Macro-averaged ROC-AUC across companies. Compute ROC-AUC separately for each companyAlias, then average the AUCs equally across companies that have both classes present in the test set. This threshold-free metric is robust to class imbalance and avoids domination by large companies.
- Submission format: A CSV with two columns: uid and churn_probability, where uid uniquely identifies a (company, employee) pair and churn_probability is a numeric score in [0, 1].

Final Files
- Training: votes_train.csv, comments_train.csv, interactions_train.csv, train_employees.csv
- Testing: votes_test.csv, comments_test.csv, interactions_test.csv, test_employees.csv
- Sample: sample_submission.csv

Goal
Design a strong ML solution that leverages temporal and relational structure in the data to accurately rank churn risk. Models such as gradient boosting, regularized logistic regression, or time-aware neural nets are applicable when paired with careful data processing and feature engineering.
