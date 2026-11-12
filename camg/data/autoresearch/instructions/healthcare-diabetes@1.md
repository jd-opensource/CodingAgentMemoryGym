# OpenMLE-fast task

Task ID: `healthcare-diabetes@1`

Native metric: `DiabetesRiskMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (698 bytes)
- `data/sample_submission.csv` (4776 bytes); columns: ["Id", "Outcome"]
- `data/test.csv` (18291 bytes); columns: ["Id", "Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"]
- `data/train.csv` (77139 bytes); columns: ["Id", "Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age", "Outcome"]

## Public description

Competition: Diabetes Risk Probability Prediction

Problem Statement
Given tabular clinical features for each individual, predict the probability that the individual has diabetes (Outcome ∈ {0,1}). Your model must output probabilities in [0,1] for each test example.

Data Files (under this public directory)
- train.csv: Features plus the binary target column Outcome.
- test.csv: The same features as train.csv except Outcome.
- sample_submission.csv: Example of the expected submission format.

Submission Format
CSV with exactly two columns: [Id, Outcome], where Outcome is a probability in [0,1].

Evaluation
Binary Log Loss (lower is better) computed against the hidden labels for test.csv.
