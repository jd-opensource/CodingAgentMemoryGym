# OpenMLE-fast task

Task ID: `dark-triad-data-csv@1`

Native metric: `SD3ReferralSourceMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2645 bytes)
- `data/sample_submission.csv` (26151 bytes); columns: ["id", "source"]
- `data/test.csv` (221100 bytes); columns: ["id", "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "N1", "N2", "N3", "N4", "N5", "N6", "N7", "N8", "N9", "P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9", "country"]
- `data/train.csv` (912766 bytes); columns: ["id", "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "N1", "N2", "N3", "N4", "N5", "N6", "N7", "N8", "N9", "P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9", "country", "source"]

## Public description

Title: SD3 Referral Source Prediction

Problem statement
You are given anonymized responses to the Short Dark Triad (SD3) personality inventory alongside the respondent’s country code. Your task is to predict how the respondent arrived at the test (the referral source):
- 1 = front page of the website
- 2 = Google search
- 3 = other referrer

This is a 3-class classification problem with moderate class imbalance. Success requires solid data preprocessing, careful treatment of a high-cardinality categorical feature (country), and robust modeling that performs well across all classes.

Files
- train.csv: Each row represents one respondent. Contains:
  - id: unique identifier
  - M1–M9, N1–N9, P1–P9: 27 Likert-scale item responses (integers typically in [1, 5])
  - country: 2-letter country code
  - source: target label in {1, 2, 3}
- test.csv: Same columns as train.csv except source is withheld. Contains:
  - id, M1–M9, N1–N9, P1–P9, country
- sample_submission.csv: Example of a valid submission file with the correct schema.

Goal
Build a model to predict source for each row in the test set.

Evaluation
- Primary metric: Macro-averaged F1 score across classes {1, 2, 3}.
- Submission format: A CSV with the following columns in any row order:
  - id: matches the id column in test.csv
  - source: your predicted class label for that id, as an integer in {1, 2, 3}
Your score is computed by joining on id and then calculating macro F1 between ground-truth labels and your predicted labels. All classes are weighted equally in the final score.

Notes and recommendations
- Handle class imbalance thoughtfully. Macro F1 penalizes models that ignore minority classes.
- The country feature is high-cardinality; use encoders or models that handle such features well (e.g., one-hot encoding with regularization, target encoding with proper CV, or tree-based methods with careful parameters).
- Consider feature engineering such as subscale aggregates (e.g., mean of M items, N items, P items) while keeping the original items as features.
- Standard ML approaches such as regularized linear models, gradient-boosted decision trees, and neural networks are all applicable. Sound preprocessing, cross-validation, and tuning will matter.

Deliverables
- Submit a CSV file named however you like, but with exactly two columns: id and source. The row order does not matter, but ids must be unique and cover every id in the test set exactly once.

Ethical use
- The task uses anonymized survey data. Avoid attempts at re-identification or inference of sensitive attributes beyond what is necessary to solve the prediction task.
