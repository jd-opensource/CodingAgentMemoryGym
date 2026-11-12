# OpenMLE-fast task

Task ID: `pakistanintellectualcapitalcs@1`

Native metric: `PakistanCSFacultyRankMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3590 bytes)
- `data/sample_submission.csv` (7250 bytes); columns: ["id", "designation_canonical"]
- `data/test.csv` (50730 bytes); columns: ["id", "University Currently Teaching", "Department", "Province University Located", "Terminal Degree", "Graduated from", "Country", "Year", "Area of Specialization/Research Interests", "Other Information"]
- `data/train.csv` (222364 bytes); columns: ["id", "University Currently Teaching", "Department", "Province University Located", "Terminal Degree", "Graduated from", "Country", "Year", "Area of Specialization/Research Interests", "Other Information", "designation_canonical"]

## Public description

CS Faculty Rank Prediction (Tabular + Text)

Problem statement
Build a model that predicts the academic rank (designation) of a Computer Science/IT faculty member in Pakistan based on their profile: university, department, province, terminal degree, graduation institution/country, year, specialization/interests, and other notes. The target rank is standardized into five canonical classes:
- Instructor
- Lecturer
- Assistant Professor
- Associate Professor
- Professor

Why this problem is interesting and challenging
- The data mixes structured categories (province, degree, year) with noisy free text (specializations, notes) across two versions of the dataset.
- Real-world heterogeneity: inconsistent capitalization, spelling variants (e.g., PhD/Ph.D/Phd), and missing values.
- Class imbalance: senior ranks (Professor/Associate) are less common than mid-level ranks (Lecturer/Assistant Professor).
- High-quality labels: designations are curated from university sources, enabling meaningful supervised learning.

Files provided
- train.csv: Deduplicated, schema-aligned rows with features and the mapped target column designation_canonical.
- test.csv: Same columns as train.csv minus designation_canonical.
- sample_submission.csv: A valid example submission file with the correct id list and label format.

Data description (columns)
Each row describes one faculty profile. The following feature columns are included in both train.csv and test.csv (order may vary):
- id: Unique row identifier.
- University Currently Teaching
- Department
- Province University Located
- Terminal Degree
- Graduated from
- Country
- Year (best-effort parsed numeric; may be empty if unknown)
- Area of Specialization/Research Interests
- Other Information

Notes
- Teacher Name is intentionally excluded to avoid person-specific leakage and improve generalization.
- The original Designation column is normalized to designation_canonical in train.csv and removed from test.csv.
- Non-academic/ambiguous titles (e.g., Lab Engineer, Research Associate, Administrator) are removed from the labeled dataset to keep targets precise.

Evaluation metric
- Macro F1-score across the five classes.
- Definition: For each class, compute F1 = 2 * (precision * recall) / (precision + recall) with zero-safe handling when a class has no predictions or no true instances; the final score is the unweighted mean across all five classes.
- Rationale: Macro F1 treats all ranks equally and is robust to class imbalance.

Submission format
- CSV file with exactly two columns and no header changes:
  - id
  - designation_canonical (one of: Instructor, Lecturer, Assistant Professor, Associate Professor, Professor)
- The set and order of ids must exactly match those in test.csv.

Recommended modeling approaches
- Robust text preprocessing (lowercasing, punctuation/whitespace normalization, n-grams/character n-grams) over University/Department/Specializations/Notes.
- Categorical encoders for province/degree/country; explicit Unknown handling for missing values.
- Models: linear classifiers (e.g., logistic regression) on bag-of-words features, gradient-boosted trees over encoded features, or shallow neural models. Address class imbalance via class weights or resampling.

Ethical/fairness notes
- No external data is required. Avoid using features derived from the target itself. Ensure your model’s decisions do not encode sensitive attributes not present in the dataset.

Good luck and have fun building a robust classifier that generalizes across universities and roles in Pakistan’s CS academia!
