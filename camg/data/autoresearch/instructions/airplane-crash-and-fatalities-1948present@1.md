# OpenMLE-fast task

Task ID: `airplane-crash-and-fatalities-1948present@1`

Native metric: `AircraftDamageSeverityMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2228 bytes)
- `data/sample_submission.csv` (57859 bytes); columns: ["id", "dmg"]
- `data/test.csv` (487507 bytes); columns: ["id", "acc. date", "type", "reg.", "operator", "location"]
- `data/train.csv` (1467022 bytes); columns: ["acc. date", "type", "reg.", "operator", "location", "dmg"]

## Public description

Accident Damage Severity Classification

Problem statement
Predict the damage severity category for recorded aircraft accidents/incidents using contextual fields (date, aircraft type, registration, operator, location). The target has four classes:
- w/o: written off / destroyed
- sub: substantial damage
- non: no damage
- min: minor damage

Final data files
- train.csv: Training data with features and the target column dmg.
- test.csv: Test data with features only and a unique id column.
- sample_submission.csv: A sample submission file with id and dmg columns.

Target and features
- Target column: dmg ∈ {w/o, sub, non, min}.
- Feature columns: acc. date, type, reg., operator, location.
- The fatalities column (fat.) is excluded to prevent target leakage.

Split strategy
- A single time-based split is used: training contains earlier years and test contains later years. This evaluates temporal generalization under realistic distribution shifts. All four target classes appear in both splits.

Evaluation metric
- Macro F1 score across the four classes {w/o, sub, non, min}.
- Rationale: Classes are imbalanced; macro F1 fairly weights each class and penalizes models that ignore minority classes. Scores range from 0 (worst) to 1 (best).

Submission format
- CSV with exactly two columns: id and dmg.
- id must match the ids in test.csv (one prediction per test row).
- dmg must be one of {w/o, sub, non, min}.

Modeling notes and recommendations
- Date parsing: The acc. date field uses mixed formats (e.g., dd-Mon-yy, dd-Mon-yyyy, partially unknown day like "xx May 2010"). Map two-digit years: 48–99 → 1948–1999, 00–24 → 2000–2024.
- Derive features from acc. date: year, month, day-of-week, decade.
- Text normalization: Lowercase, trim, normalize punctuation for type, operator, and location.
- High-cardinality features: operator, type, location, and reg. benefit from robust encoders (e.g., hashing, bag-of-words, or frequency-thresholded categorical encodings). Regularize to avoid overfitting.
- Class imbalance and concept drift: Expect severe imbalance and shifts across decades. Use appropriate techniques (class weights, resampling, calibrated decision thresholds) and robust validation.
