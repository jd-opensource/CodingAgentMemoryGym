# OpenMLE-fast task

Task ID: `construction-and-project-management-example-data@2`

Native metric: `ConstructionCauseClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4243 bytes)
- `data/forms.csv` (2194687 bytes); columns: ["Ref", "Status", "Location", "Name", "Created", "Type", "Status Changed", "Open Actions", "Total Actions", "Association", "OverDue", "Images", "Comments", "Documents", "Project", "Report Forms Status", "Report Forms Group"]
- `data/sample_submission.csv` (51028 bytes); columns: ["Ref", "Cause"]
- `data/test.csv` (493737 bytes); columns: ["Ref", "Status", "Location", "Description", "Created", "Target", "Type", "To Package", "Status Changed", "Association", "OverDue", "Images", "Comments", "Documents", "Priority", "project", "Report Status", "Task Group"]
- `data/train.csv` (2173924 bytes); columns: ["Ref", "Status", "Location", "Description", "Created", "Target", "Type", "To Package", "Status Changed", "Association", "OverDue", "Images", "Comments", "Documents", "Priority", "Cause", "project", "Report Status", "Task Group"]

## Public description

Competition: Root Cause Classification for Construction Field Tasks

Problem statement
Site teams log thousands of field tasks with short free-text descriptions and metadata across safety, quality, and site management. Correctly tagging each task with its Cause category (e.g., "JPC - Safety - House Keeping", "JPC - Quality - Workmanship") improves triage and accountability. Your goal is to build a model that predicts the Cause for new tasks at creation time using fields available in the task record and historical project context.

Files
- train.csv — Task records with labels. Includes task metadata and the Cause column (target).
- test.csv — Same schema as train.csv but without the Cause column. Predict Cause for these tasks.
- forms.csv — Project forms data for contextual feature engineering (e.g., counts by form type/date). Use carefully to avoid leakage by only using information prior to the task Created date.
- sample_submission.csv — Example of a valid submission format.

Target
- Cause (multi-class string label).

Input features (non-exhaustive suggestions)
- Text: Description (free text describing the task).
- Locations: Location (hierarchical path separated by '>'); consider tokens and hierarchical levels.
- Categorical: Type, To Package, Association, Task Group, project, Status (avoid using post-hoc outcome fields; see notes).
- Dates: Created, Target, Status Changed (for historical aggregation with forms.csv; ensure time-safe processing).
- Binary flags: OverDue, Images, Comments, Documents.
- Cross-file context (optional): Aggregations from forms.csv by project and time window (e.g., counts by Report Forms Group/Type in the 14/30 days before a task).

Important notes to avoid leakage
- The task Cause is expected to be determined at or near task creation. Do not engineer features from outcomes or edits made after Created for the same task.
- If you derive features from forms.csv, only use forms with Created strictly before the task’s Created timestamp. Similarly, any rolling/statistical features must be based on past data only.

Evaluation
- Metric: Macro-averaged F1 score computed across all Cause classes present in the test set.
- Rationale: The class distribution is long-tailed and imbalanced; macro-F1 gives equal weight to each class and rewards models that perform well on minority classes.

Submission format
- CSV with two columns and exact header: Ref,Cause
- Ref values must match exactly the test set IDs; one row per test Ref.
- Cause must be one of the valid strings for the task’s class space. You are free to predict any string; scoring will compare strings directly.

Recommended baseline approaches
- Text-first: TF-IDF on Description with linear models (logistic regression) and class weighting.
- Text + tabular: N-grams + one-hot/frequency-encoded categorical features (Type, Task Group, To Package, Association, project) and location tokens.
- Temporal context: Time-aware aggregation features from forms.csv (counts/ratios by project and Report Forms Group/Type in rolling windows prior to Created).
- Modern NLP: Fine-tune a lightweight transformer on Description; optionally fuse tabular features via concatenation.

Data quality and preprocessing tips
- Normalize Description text (lowercase, strip punctuation and repeated whitespace) while retaining construction-specific abbreviations (e.g., PPE, WAH, ITP, QA/QC).
- Parse Location into levels (e.g., building/block/floor/area) and include both tokens and depth indicators.
- Treat booleans (OverDue, Images, Comments, Documents) as integers 0/1.
- Handle categorical cardinality by grouping infrequent categories to "__rare__" based on training frequency only.

Train/test split details
- A single deterministic stratified split by Cause has been prepared. All test classes appear in the training set at least once. Use all rows; do not further subsample.

Final deliverables
- Submit a single CSV with predictions: Ref,Cause. No additional files are needed.

Expectations
- Build a robust pipeline: preprocessing, feature engineering, model training, and evaluation using macro-F1. Use cross-validation inside the training data if you wish to estimate generalization. Solutions should be reproducible.
