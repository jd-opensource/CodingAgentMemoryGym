# OpenMLE-fast task

Task ID: `banknote-authentication-uci@1`

Native metric: `BanknoteAuthenticationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2060 bytes)
- `data/sample_submission.csv` (3203 bytes); columns: ["id", "probability"]
- `data/test.csv` (14251 bytes); columns: ["id", "variance", "skewness", "curtosis", "entropy"]
- `data/train.csv` (35312 bytes); columns: ["id", "variance", "skewness", "curtosis", "entropy", "target"]

## Public description

Title: Banknote Forgery Detection from Wavelet Features

Problem statement
Build a machine learning model to detect forged banknotes using four wavelet-derived features extracted from high-resolution inspection images. Given a tabular row with the features [variance, skewness, curtosis, entropy], predict the likelihood that a banknote is forged.

Data description
- train.csv: Contains columns [id, variance, skewness, curtosis, entropy, target]. The target is a binary label where 0 = genuine and 1 = forged.
- test.csv: Contains columns [id, variance, skewness, curtosis, entropy] without the target.
- sample_submission.csv: Example submission format with columns [id, probability]. The probability should reflect the likelihood of the forged class (target = 1).

Important notes
- Features are continuous and can be heavy-tailed (e.g., skewness and curtosis may span wide ranges). Thoughtful preprocessing (e.g., scaling, robust methods) and regularization can help.
- The split preserves class ratios to ensure a fair evaluation.
- The id column uniquely identifies rows and must be used to align predictions.

Submission format
- Submit a CSV with columns [id, probability].
- id must exactly match the ids in test.csv.
- probability must be a numeric value in [0, 1], representing P(target = 1).

Evaluation metric
- Primary metric: ROC AUC computed on the test set using the submitted probabilities for the forged class (target = 1).
- Why ROC AUC: It is threshold-independent, robust to mild class imbalance, and precisely measures how well your model ranks genuine vs forged notes.

Guidance for participants
- Recommended workflow: data processing (scaling/robust scaling), feature engineering if desired (polynomial interactions, transformations), model training (e.g., logistic regression, SVM, tree ensembles), calibration (Platt/Isotonic if needed), and model evaluation.
- Avoid label leakage: test.csv does not include the target; only use the four features for modeling.

Final files provided
- train.csv
- test.csv
- sample_submission.csv
