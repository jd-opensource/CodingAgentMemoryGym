# OpenMLE-fast task

Task ID: `mcdonalds-reviews@2`

Native metric: `McDonaldsVisitFrequencyMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2024 bytes)
- `data/sample_submission.csv` (6039 bytes); columns: ["id", "VisitFrequency"]
- `data/test.csv` (16083 bytes); columns: ["id", "yummy", "convenient", "spicy", "fattening", "greasy", "fast", "cheap", "tasty", "expensive", "healthy", "disgusting", "Age", "Gender"]
- `data/train.csv` (80036 bytes); columns: ["id", "yummy", "convenient", "spicy", "fattening", "greasy", "fast", "cheap", "tasty", "expensive", "healthy", "disgusting", "Age", "Gender", "VisitFrequency"]

## Public description

Problem: Predict McDonald’s Visit Frequency (ordinal classification)

Overview
You are given survey responses from 1,453 Australian adults about their perceptions of McDonald’s and basic demographics. Your task is to predict each respondent’s VisitFrequency, an ordered categorical variable with six levels, using the provided perceptions and demographics.

Target
VisitFrequency with the following order (from least to most frequent):
0 Never
1 Once a year
2 Every three months
3 Once a month
4 Once a week
5 More than once a week

Files
- train.csv: Training data with columns [id, 11 perception attributes, Age, Gender, VisitFrequency].
- test.csv: Test data with columns [id, 11 perception attributes, Age, Gender].
- sample_submission.csv: Example submission with columns [id, VisitFrequency].

Features
- 11 perception attributes: yummy, convenient, spicy, fattening, greasy, fast, cheap, tasty, expensive, healthy, disgusting (values: Yes/No)
- Age (integer)
- Gender (Male/Female)

Task
Build a model that maps perceptions and demographics to VisitFrequency, respecting its ordinal structure.

Evaluation
Submissions are evaluated using Quadratic Weighted Kappa (QWK), computed by mapping the six VisitFrequency categories to integers [0..5] in the order listed above. QWK rewards near-misses more than far-misses and naturally handles class imbalance.

Submission Format
- A CSV file with exactly two columns: id, VisitFrequency
- id must match the id values in test.csv exactly (same set, any order).
- VisitFrequency values must be one of: Never, Once a year, Every three months, Once a month, Once a week, More than once a week.

Notes & Tips
- Encode Yes/No attributes as binary indicators and consider ordinal-aware models or losses.
- The data are imbalanced, especially for the most frequent visitors. Calibration and proximity-aware metrics matter.
- Feature interactions (e.g., tasty vs. healthy vs. fattening) can be important.
- Do not assume any external information beyond the provided features.
