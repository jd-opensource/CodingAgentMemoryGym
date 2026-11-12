# OpenMLE-fast task

Task ID: `migraine-symptom-dataset-for-classification@2`

Native metric: `MigraineHemiplegicDetectionMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3032 bytes)
- `data/sample_submission.csv` (2319 bytes); columns: ["row_id", "hemiplegic_migraine"]
- `data/test.csv` (5074 bytes); columns: ["row_id", "Age", "Duration", "Frequency", "Location", "Character", "Intensity", "Nausea", "Vomit", "Phonophobia", "Photophobia", "Visual", "Sensory", "Dysphasia", "Dysarthria", "Vertigo", "Tinnitus", "Hypoacusis", "Diplopia", "Defect", "Conscience", "Paresthesia", "DPF"]
- `data/train.csv` (15429 bytes); columns: ["row_id", "Age", "Duration", "Frequency", "Location", "Character", "Intensity", "Nausea", "Vomit", "Phonophobia", "Photophobia", "Visual", "Sensory", "Dysphasia", "Dysarthria", "Vertigo", "Tinnitus", "Hypoacusis", "Diplopia", "Defect", "Conscience", "Paresthesia", "DPF", "target"]

## Public description

Migraine Hemiplegic Subtype Detection (Imbalanced Binary Classification)

Problem statement
- Goal: Predict the probability that a migraine episode belongs to a hemiplegic subtype based on demographics, attack attributes, and neurological symptoms.
- Positive class: {Familial hemiplegic migraine, Sporadic hemiplegic migraine}
- Negative class: all other migraine types
- Participants must produce calibrated probabilities for the positive class.

Data description
- Tabular data describing 400 clinical episodes with 23 usable predictors plus target.
- Features include demographics (Age), episode characteristics (Duration, Frequency, Intensity, Location, Character), and neurological symptoms (Nausea, Vomit, Phonophobia, Photophobia, Visual, Sensory, Dysphasia, Dysarthria, Vertigo, Tinnitus, Hypoacusis, Diplopia, Defect, Conscience, Paresthesia, DPF).
- One non-informative variable Ataxia is excluded as it is constant across all records.
- The original multi-class label (Type) is mapped to a binary target.

Files provided
- train.csv: Training data with features and target column target. Also includes a unique row_id column.
- test.csv: Test data with features and row_id only (no target). Same schema as train.csv except target.
- sample_submission.csv: Example submission file with columns [row_id, hemiplegic_migraine], where hemiplegic_migraine is a probability in [0,1].

Target definition
- target = 1 if Type ∈ {Familial hemiplegic migraine, Sporadic hemiplegic migraine}; otherwise target = 0.

Important feature notes
- Keep integer codings as categorical/ordinal as appropriate; do not coerce to boolean.
  - Visual (0–4) and Sensory (0–2) are ordinal severities, not simple yes/no.
  - 0 in Location/Character/Intensity may represent Unknown/Not specified in some rows; treat as a valid category if present.
- No missing values are expected; handle them robustly if they arise during modeling.

Evaluation
- Metric: Average Precision (area under the precision–recall curve, a.k.a. PR AUC) on the positive class.
- Submission format: CSV with columns [row_id, hemiplegic_migraine].
  - row_id must match exactly the IDs in test.csv.
  - hemiplegic_migraine must be a numeric probability within [0,1].
- The leaderboard is computed using the official evaluation script equivalent to sklearn.metrics.average_precision_score with y_true as the binary target and y_score as hemiplegic_migraine.

Suggested approach
- Handle strong class imbalance (minority ≈ 10%) via class weights, focal/weighted losses, or resampling.
- Consider robust feature engineering for mixed ordinal/binary variables and calibration of predicted probabilities.
- Cross-validation and threshold tuning are recommended for stability.

Final deliverables
- train.csv, test.csv, sample_submission.csv

This challenge focuses on rare-event detection under clinically realistic ambiguity, emphasizing probability estimation quality over mere ranking accuracy. Please ensure your submission adheres to the required format and metric.
