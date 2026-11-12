# OpenMLE-fast task

Task ID: `google-job-skills@1`

Native metric: `GoogleJobCategoryMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2770 bytes)
- `data/sample_submission.csv` (7551 bytes); columns: ["Id", "Category"]
- `data/test.csv` (331810 bytes); columns: ["Id", "Title", "Location", "Responsibilities", "Minimum Qualifications", "Preferred Qualifications"]
- `data/train.csv` (1393250 bytes); columns: ["Id", "Title", "Location", "Responsibilities", "Minimum Qualifications", "Preferred Qualifications", "Category"]

## Public description

Title: Google Job Category Prediction

Problem statement
Predict the job Category for Google job postings using the full textual content and metadata of each posting. Each row represents one posting and contains long-form text (Responsibilities, Minimum Qualifications, Preferred Qualifications) plus Title and Location. The task is multi-class text classification with 23 categories and notable class imbalance.

Data description
- train.csv: Training set containing Id, Title, Location, Responsibilities, Minimum Qualifications, Preferred Qualifications, and Category (label).
- test.csv: Test set containing Id, Title, Location, Responsibilities, Minimum Qualifications, Preferred Qualifications; Category is hidden.
- sample_submission.csv: A template showing the required submission format with random valid example labels.

Notes
- Id is a stable identifier generated from the posting content to avoid leakage and ensure determinism.
- Some samples may have missing text in Responsibilities or Qualifications; treat missing values as empty strings.
- Duplicates have been removed based on a normalized fingerprint of the feature fields to prevent leakage.
- The Company column is intentionally excluded since it is constant and non-informative.

Target variable
- Category: The curated job category assigned by Google Careers.

Evaluation
- Macro-averaged F1 score across all categories present in the ground truth.
- Rationale: Macro F1 counteracts class imbalance by equally weighting each category. It captures both precision and recall per class and averages them, discouraging models that predict only dominant categories.

Submission format
- A single CSV file with exactly two columns named Id and Category.
- Ids must match those in the test set exactly and be unique.
- Category values must be strings corresponding to predicted labels for each test Id.

Suggested approach
- Data processing: Normalize casing/whitespace; preserve technical tokens (e.g., C++, C#, SQL). Handle missing text as empty strings. Optionally, remove obvious boilerplate while safeguarding language tokens.
- Feature engineering: Concatenate text fields (Title + Responsibilities + Minimum Qualifications + Preferred Qualifications) into a single document; encode Location as a categorical feature (one-hot or embedding). Consider field-aware encoders and late fusion.
- Modeling: Try TF‑IDF with linear classifiers (logistic regression, linear SVM), or fine-tune pretrained transformers (e.g., BERT/RoBERTa). Multi-class softmax is standard. Use class weights to address imbalance.
- Evaluation: Use stratified cross‑validation locally for model selection, then train on full train.csv. Submit predictions for test.csv.

Files
- train.csv
- test.csv
- sample_submission.csv
