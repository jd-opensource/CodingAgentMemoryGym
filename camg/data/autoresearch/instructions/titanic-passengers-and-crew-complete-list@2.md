# OpenMLE-fast task

Task ID: `titanic-passengers-and-crew-complete-list@2`

Native metric: `TitanicSurvivalMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2211 bytes)
- `data/sample_submission.csv` (21633 bytes); columns: ["id", "survived"]
- `data/test.csv` (64169 bytes); columns: ["id", "name", "gender", "age", "class", "embarked", "country", "ticketno", "fare", "sibsp", "parch"]
- `data/train.csv` (107676 bytes); columns: ["id", "name", "gender", "age", "class", "embarked", "country", "ticketno", "fare", "sibsp", "parch", "survived"]

## Public description

Shipboard Domain-Shift Survival Generalization

Problem
You are given a complete manifest of Titanic passengers and crew. Your task is to train on passengers only and predict survival probabilities for all crew members, under a strong real-world domain shift (different roles and systematic missingness in several fields for crew).

Data
Final files provided:
- train.csv: All passengers with labels. Columns include:
  - id: unique integer identifier
  - name, gender, age, class, embarked, country, ticketno, fare, sibsp, parch
  - survived: binary target (1=survived, 0=did not)
- test.csv: All crew without labels. Same columns as train.csv except the survived column is removed.
- sample_submission.csv: Submission example with the correct format.

Notes
- The class column includes passenger classes {1st, 2nd, 3rd} and crew categories {engineering crew, deck crew, victualling crew, restaurant staff}. Only passenger rows are in train; only crew rows are in test.
- Crew records systematically lack fare, sibsp, and parch values. Design your pipeline to be robust to domain shift and missing values.
- Feature engineering is encouraged, for example extracting title from name, deriving is_crew/crew_category from class, handling high-cardinality country, and choosing encoders that generalize to unseen categories.

Target
- survived (binary): predict the probability of survival for each crew member in test.csv.

Evaluation
- Metric: LogLoss (negative log-likelihood of the Bernoulli model) computed over all rows in test.csv.
- Submission format: CSV with two columns
  - id
  - survived: predicted probability in [0, 1]
- Requirements:
  - Must predict for all and only the ids in test.csv.
  - No duplicate ids. All values must be finite and within [0, 1].

Tips
- Expect covariate shift: crew have different distributions in gender/age and entirely different class categories. Some features (fare, sibsp, parch) are missing for all crew and thus carry little direct signal in test; if used, include missingness indicators and robust encoders.
- Strong baselines include gradient-boosted trees (LightGBM/XGBoost/CatBoost) or regularized logistic regression with thoughtful encoding and calibration.
