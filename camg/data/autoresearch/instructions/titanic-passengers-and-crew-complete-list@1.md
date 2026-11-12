# OpenMLE-fast task

Task ID: `titanic-passengers-and-crew-complete-list@1`

Native metric: `TitanicSurvivalMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2922 bytes)
- `data/sample_submission.csv` (4636 bytes); columns: ["Id", "Survived"]
- `data/test.csv` (41493 bytes); columns: ["Id", "Name", "Gender", "Age", "Class", "Embarked", "Country", "TicketNo", "Fare", "SibSp", "Parch"]
- `data/train.csv` (131093 bytes); columns: ["Id", "Name", "Gender", "Age", "Class", "Embarked", "Country", "TicketNo", "Fare", "SibSp", "Parch", "Survived"]

## Public description

Titanic Full Manifest Survival Prediction (Passengers + Crew)

Problem
- Given demographic and booking/assignment information for every recorded individual aboard RMS Titanic (passengers and multiple crew groups), predict the probability that the individual survived.
- Submit well-calibrated survival probabilities for the test set.

Files
- train.csv: Tabular training data with features and the target column Survived (0/1).
- test.csv: Test data with the same feature columns as train.csv, without Survived.
- sample_submission.csv: Example submission file with the required format.

Target
- Survived (binary): 1 if the person survived, 0 otherwise.

Features
- Id: Unique identifier for each row (integer).
- Name: Full name (string, UTF-8 with diacritics preserved).
- Gender: male/female.
- Age: Age in years (float; infants encoded as fractional years).
- Class: One of 1st, 2nd, 3rd, engineering crew, deck crew, victualling crew, restaurant staff.
- Embarked: Port code (S/C/Q/B).
- Country: Nationality string (high cardinality).
- TicketNo: Alphanumeric ticket identifier (categorical/group; do not treat as numeric magnitude).
- Fare: Fare paid (float; many crew have missing values).
- SibSp: Count of siblings/spouses aboard (integer; many crew have missing values).
- Parch: Count of parents/children aboard (integer; many crew have missing values).

Notes and recommendations
- You may engineer additional features (e.g., title from Name; family size from shared TicketNo and/or surname; child indicator; interactions between Class, Gender, and Age).
- Handle missing values carefully: crew rows often have missing Fare, SibSp, Parch; a small number of Age are missing.
- High-cardinality Country and TicketNo benefit from techniques like frequency/target encoding, hashing, or suitable tree models.

Evaluation
- Metric: LogLoss (cross-entropy) on the probability of Survived.
- Submission format: A CSV with two columns: Id and Survived, where Survived is a probability in [0, 1] for Id being a survivor.
- Lower LogLoss is better. Invalid probabilities (NaN/inf/out of range) will be clipped or rejected.

Split policy used to create the provided files
- Deterministic split with a fixed random seed.
- Group-aware split to reduce leakage: passengers are grouped by TicketNo; crew are grouped by surname (from Name) so families/teams don’t cross train/test.
- The split preserves both classes in train and test.

What’s provided vs hidden
- train.csv and test.csv share the same columns except that train.csv includes Survived and test.csv does not.
- The ground-truth labels for the test set are withheld and used only for evaluation.

Constraints
- Use the full data; do not downsample.
- No file paths are included in CSVs. Names do not encode labels; group-aware splitting mitigates leakage across splits.

Deliverables
- Your submission must be a CSV with columns: Id, Survived (probability).
