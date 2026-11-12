# OpenMLE-fast task

Task ID: `students-adaptability-level-in-online-education@1`

Native metric: `StudentsAdaptabilityMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2652 bytes)
- `data/sample_submission.csv` (1440 bytes); columns: ["Adaptivity Level"]
- `data/test.csv` (18169 bytes); columns: ["Gender", "Age", "Education Level", "Institution Type", "IT Student", "Location", "Load-shedding", "Financial Condition", "Internet Type", "Network Type", "Class Duration", "Self Lms", "Device"]
- `data/train.csv` (78148 bytes); columns: ["Gender", "Age", "Education Level", "Institution Type", "IT Student", "Location", "Load-shedding", "Financial Condition", "Internet Type", "Network Type", "Class Duration", "Self Lms", "Device", "Adaptivity Level"]

## Public description

Title: Students’ Adaptability Level in Online Education

Problem statement
Build a machine learning model that predicts a student’s adaptability level to online education from demographic, institutional, connectivity, and study-habit factors. The target is a three-class categorical variable: {Low, Moderate, High}. This is a fairness-aware, imbalanced, fully-categorical tabular classification task.

Data
- Training data: train.csv
  - Columns: 13 categorical features plus the target column Adaptivity Level.
- Test data: test.csv
  - Columns: the same 13 categorical features (no target column).
- Sample submission: sample_submission.csv
  - One column named Adaptivity Level with one label per test row.

Features
- Gender
- Age
- Education Level
- Institution Type
- IT Student
- Location
- Load-shedding
- Financial Condition
- Internet Type
- Network Type
- Class Duration
- Self Lms
- Device

Split strategy
- Stratified by Adaptivity Level to preserve class proportions.
- Group-aware: identical feature signatures (exact duplicates across all 13 features) are confined entirely to either train or test to prevent leakage and make generalization non-trivial.
- Deterministic split and outputs to support reproducibility.

Evaluation
- Metric: Macro F1 across the three classes {Low, Moderate, High}.
  - Per-class F1 is computed from precision and recall for each class treated as the positive class.
  - The final score is the unweighted mean of the three per-class F1 scores.
- Rationale: The dataset is moderately imbalanced across three classes. Macro F1 equally weights per-class performance, discouraging models from ignoring the minority class while remaining precise and interpretable for multi-class classification.

Submission format
- A single CSV file named however you like with one header column: Adaptivity Level.
- The number of rows must exactly match test.csv.
- Each entry must be one of the valid labels: Low, Moderate, High.

What makes this challenging and meaningful
- Small dataset with many exact duplicates demands careful encoding and regularization.
- Fully categorical feature space with mixed nominal/ordinal semantics.
- Class imbalance across three outcomes emphasizes fairness across classes.

Expectations for participants
- End-to-end ML workflow: data preprocessing (categorical encoding), feature engineering (e.g., ordinal treatment for banded variables, interactions), model training (e.g., regularized linear models, tree ensembles, CatBoost), and rigorous evaluation.
- Handle class imbalance thoughtfully (class weights, resampling, focal loss).
- Keep solutions deterministic and reproducible.
