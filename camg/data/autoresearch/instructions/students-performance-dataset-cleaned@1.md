# OpenMLE-fast task

Task ID: `students-performance-dataset-cleaned@1`

Native metric: `StudentsWritingScoreMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2581 bytes)
- `data/sample_submission.csv` (5173 bytes); columns: ["row_id", "writing_score"]
- `data/test.csv` (8814 bytes); columns: ["row_id", "gender", "race_ethnicity", "parental_level_of_education", "lunch", "test_preparation_course", "math_score", "reading_score"]
- `data/train.csv` (37476 bytes); columns: ["row_id", "gender", "race_ethnicity", "parental_level_of_education", "lunch", "test_preparation_course", "math_score", "reading_score", "writing_score"]

## Public description

Students’ Writing Score Prediction Challenge

Problem statement
Educational systems often have math and reading scores available before writing is graded. Your task is to build a model that predicts each student’s writing score (0–100) from their demographics and peer subject scores.

Data description
You are provided with a single tabular dataset split into train and test:
- train.csv: Feature columns plus the target writing_score.
- test.csv: Feature columns only, with the same schema as train.csv except without writing_score.
- sample_submission.csv: A valid example of the required submission format.

Feature columns
- gender: Binary indicator (0/1).
- race_ethnicity: Categorical string, e.g., group A–E.
- parental_level_of_education: Categorical string, e.g., high school, some college, bachelor’s degree, etc.
- lunch: Binary indicator (0/1).
- test_preparation_course: Binary indicator (0/1).
- math_score: Integer in [0, 100].
- reading_score: Integer in [0, 100].

Target
- writing_score: Integer in [0, 100]. Present only in train.csv.

Important note on leakage
The original source data contained total_score and average_score, which are deterministic functions of the subject scores and include writing_score. These columns are excluded from train.csv and test.csv to prevent target leakage. Do not attempt to reconstruct or use them.

Submission format
- A single CSV file with exactly two columns and a header:
  - row_id: Identifier provided in test.csv.
  - writing_score: Your predicted writing score for each row_id.
- The order of rows does not matter, but row_id must match the provided test.csv exactly and appear once per row.

Evaluation
- Metric: Root Mean Squared Error (RMSE) computed between your predictions and the hidden ground truth writing_score.
- Numerical handling: During evaluation, predictions are validated to be finite numbers; non-finite values will cause your submission to be rejected. Predictions are clipped to [0, 100] before scoring for fairness.
- Lower RMSE is better.

Recommended approach (non-binding)
- Encode categorical features (e.g., one-hot encoding for race_ethnicity and parental_level_of_education).
- Consider interactions and nonlinearities between demographics and subject scores.
- Try regularized linear models, tree-based ensembles, or neural networks. Calibrate predictions to the [0, 100] range.

Files provided
- train.csv
- test.csv
- sample_submission.csv

Your goal
Build an ML model that generalizes well from train.csv to predict writing_score for test.csv with the lowest possible RMSE.
