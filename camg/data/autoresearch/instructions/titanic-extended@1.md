# OpenMLE-fast task

Task ID: `titanic-extended@1`

Native metric: `TitanicExtendedMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3437 bytes)
- `data/sample_submission.csv` (8488 bytes); columns: ["PassengerId", "Survived", "Died_body_recovered", "Died_missing"]
- `data/test.csv` (45519 bytes); columns: ["PassengerId", "Pclass", "Name", "Sex", "Age", "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked", "WikiId", "Name_wiki", "Age_wiki", "Hometown", "Boarded", "Destination", "Class"]
- `data/train.csv` (193879 bytes); columns: ["PassengerId", "Pclass", "Name", "Sex", "Age", "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked", "WikiId", "Name_wiki", "Age_wiki", "Hometown", "Boarded", "Destination", "Class", "Outcome"]

## Public description

Title: Titanic Outcomes Triad — Predict survival vs. recovered vs. missing

Problem statement
Given passenger records for the RMS Titanic with enriched pre-boarding attributes, predict each passenger’s final outcome category after the sinking using only information that would be known before or at boarding. This is a three-class classification problem:
- Survived
- Died_body_recovered (died and body was later recovered)
- Died_missing (died and body was not recovered)

Your task is to train a model that outputs calibrated probabilities over the three classes for a held-out test set.

Data description
The dataset consists of passenger-level tabular records combining the classic Titanic manifest with additional fields consolidated from historical sources. The competition data files are:
- train.csv — Training rows with features and the target column Outcome.
- test.csv — Test rows with the same features as train.csv, but without Outcome.
- sample_submission.csv — A sample submission file showing the expected format (probabilities per class).

Train/test contain these types of fields:
- IDs: PassengerId (identifier only)
- Original Titanic attributes: Pclass, Name, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked
- Wikipedia-enriched attributes: WikiId, Name_wiki, Age_wiki, Hometown, Boarded, Destination, Class

Important feature usage rules
- The following columns are deliberately excluded from the public feature set to avoid label leakage: Lifeboat, Body, Survived. Do not use them for modeling.
- Participants should focus on using only pre-boarding and on-boarding information. Examples of useful engineered features include: title extraction from Name/Name_wiki, age reconciliation (e.g., Age vs. Age_wiki), deck extraction from Cabin, family size (SibSp + Parch + 1), ticket normalization and group indicators, and standardized embarkation ports.

Target definition
The hidden ground truth Outcome is defined from historical records as follows (used internally to build the target and not available in test.csv):
- If Body is non-empty → Died_body_recovered
- Else if Lifeboat is non-empty → Survived
- Else → Died_missing

Submission format
- File must be a CSV with columns: PassengerId, Survived, Died_body_recovered, Died_missing
- Each row corresponds to a PassengerId present in test.csv and must appear exactly once.
- Provide probabilities for each class that are non-negative, finite, and sum to 1 per row.

Evaluation metric
- Multiclass Log Loss (cross-entropy) computed over the three classes listed above.
- This is a proper scoring rule that rewards well-calibrated probabilities and penalizes overconfident mistakes. Each test instance contributes equally, which helps manage class imbalance.

Notes and guidance
- Expect class imbalance. Calibrated models, class-weighting, or appropriate loss functions can help.
- Information-rich text-like fields (Hometown, Destination, Ticket, Name, Name_wiki) benefit from careful normalization and feature extraction.
- Age and embarkation fields appear in both original and enriched forms; reconcile or impute sensibly.
- Use cross-validation on train.csv as you see fit. The official leaderboard is based solely on test.csv.

Files delivered
- train.csv (features + Outcome)
- test.csv (features only)
- sample_submission.csv (PassengerId + three probability columns)

Good luck, and build robust, fair, and well-calibrated models!
