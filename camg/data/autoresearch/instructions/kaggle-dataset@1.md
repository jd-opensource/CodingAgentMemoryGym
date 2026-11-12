# OpenMLE-fast task

Task ID: `kaggle-dataset@1`

Native metric: `MedalTierMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2084 bytes)
- `data/sample_submission.csv` (23808 bytes); columns: ["Id", "Medals"]
- `data/test.csv` (239920 bytes); columns: ["Id", "Dataset_name", "Author_name", "Author_id", "No_of_files", "size", "Type_of_file", "Date", "Day", "Time"]
- `data/train.csv` (998161 bytes); columns: ["Id", "Dataset_name", "Author_name", "Author_id", "No_of_files", "size", "Type_of_file", "Date", "Day", "Time", "Medals"]

## Public description

Title: Medal Tier Prediction Challenge (Ordinal Classification)

Problem statement
Build a model that predicts the final medal tier of a Kaggle dataset using only metadata available at upload time. Medal tiers are ordered: No Medal < Bronze < Silver < Gold. This is an ordinal classification task with time-aware generalization.

Data description
You are provided with dataset-level metadata for thousands of Kaggle datasets. Each row describes one dataset at or near the time of publication. The train split includes the medal label; the test split does not. The split is chronological to emulate forward-in-time prediction.

Final files
- train.csv: rows with features and the target column Medals.
- test.csv: rows with features only (no Medals).
- sample_submission.csv: example submission with the required format.

Columns
- Medals (target in train.csv only): one of {No Medal, Bronze, Silver, Gold}.
- Features: dataset metadata fields such as Dataset_name, Author_name, Author_id, No_of_files, size, Type_of_file, Date, Day, Time. Columns that would cause target leakage (e.g., Upvotes, Usability, Image_link) are excluded. An Id column is provided to uniquely identify rows; it must be used in the submission.

Split strategy
- Chronological split by upload timestamp (Date and Time). The test set contains the most recent ~20% of datasets; the train set contains the earlier ~80%.
- All classes present in the test set also occur at least once in the train set.
- Deterministic behavior: the split and Id assignment are reproducible.

Evaluation metric
- Quadratic Weighted Kappa (QWK) between the true medal tiers and your predictions.
- QWK respects the order of classes and penalizes larger mis-ranks more than adjacent mistakes, while being robust to class imbalance.
- Submission format: a CSV file with columns [Id, Medals], where Medals is one of {No Medal, Bronze, Silver, Gold}.

Submission
- Submit a CSV with columns [Id, Medals]. Id must match the test.csv Id values; Medals must be one of the four allowed tiers.
- The leaderboard score is QWK on the test set.
