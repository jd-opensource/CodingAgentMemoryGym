# OpenMLE-fast task

Task ID: `updated-resume-dataset@1`

Native metric: `ResumeClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2446 bytes)
- `data/sample_submission.csv` (8868 bytes); columns: ["id", "Category"]
- `data/test.csv` (1215422 bytes); columns: ["id", "Resume"]
- `data/train.csv` (1893092 bytes); columns: ["id", "Resume", "Category"]

## Public description

Problem statement
Build a robust multi-class text classifier to automatically route resumes to the correct professional role category. Given a raw resume text, predict one of 25 job categories (e.g., Java Developer, Data Science, HR, Mechanical Engineer). The data consists of long, noisy resumes with varied formatting and occasional encoding artifacts, reflecting real applicant tracking system (ATS) conditions.

Data description
- train.csv: Contains the training set with columns:
  - id: A stable integer identifier for each resume
  - Resume: The raw resume text
  - Category: The ground-truth job category label
- test.csv: Contains the test set with columns:
  - id: A stable integer identifier for each resume
  - Resume: The raw resume text
- sample_submission.csv: A valid example submission with the required columns and format.

Notes on the split and leakage prevention
- The split is stratified to preserve class proportions and is group-aware: identical normalized resume texts are assigned wholly to either train or test to prevent duplicate leakage. The split is deterministic and approximately 65% train, 35% test.
- All categories present in the test set are guaranteed to appear at least once in the training set.

Task and expected approach
- Preprocess and normalize the resume text to address encoding artifacts and noisy boilerplate.
- Engineer features suitable for long documents (e.g., word/character n-grams with TF–IDF, or transformer-based models with long-context strategies such as chunking and pooling).
- Train multi-class classifiers that generalize across imbalanced classes and overlapping vocabulary (e.g., logistic regression, linear SVMs, transformers).
- Evaluate predictions on the test set using the specified metric.

Evaluation
Submissions must be a CSV with exactly two columns: id and Category, and must contain exactly the same ids and order as in test.csv. The evaluation metric is Macro F1 score computed across all categories present in the test labels. Macro F1 treats all classes equally and is robust to class imbalance.

Important considerations
- Do not include any file paths in the CSV content.
- Some resumes may be very long and include boilerplate sections; handling long-context and de-noising is crucial.
- Tokenization, normalization, and careful handling of Unicode are recommended to mitigate encoding artifacts.

Files provided
- train.csv
- test.csv
- sample_submission.csv
