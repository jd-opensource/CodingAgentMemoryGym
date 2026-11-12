# OpenMLE-fast task

Task ID: `diabetes-risk-dataset@2`

Native metric: `DiabetesRiskClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2302 bytes)
- `data/sample_submission.csv` (366927 bytes); columns: ["id", "label"]
- `data/test.csv` (812593 bytes); columns: ["id", "age", "bmi", "physical_activity_level", "family_history", "smoker"]
- `data/train.csv` (3962422 bytes); columns: ["id", "age", "bmi", "physical_activity_level", "family_history", "smoker", "label"]

## Public description

Diabetes Risk Stratification (3-Class Classification)

Problem
Predict an individual’s glucose-based risk category from basic demographic and lifestyle features. The task reflects common clinical bins used for fasting glucose and aims to triage individuals into risk groups without using the glucose measurement at inference time.

Target classes (labels)
- normal: glucose < 100 mg/dL
- prediabetes: 100–125 mg/dL (inclusive)
- diabetes: ≥ 126 mg/dL

You will build a model that maps age, BMI, physical activity, family history, and smoking status to one of the three labels above. The glucose value is not provided in the released train/test files and is only used to derive the labels.

Files
- train.csv: columns [id, age, bmi, physical_activity_level, family_history, smoker, label]
- test.csv: columns [id, age, bmi, physical_activity_level, family_history, smoker]
- sample_submission.csv: columns [id, label]

Features
- age: integer (20–80)
- bmi: float (~15–45)
- physical_activity_level: categorical {low, moderate, high}
- family_history: binary {0,1}
- smoker: binary {0,1}

Label
- label: categorical {normal, prediabetes, diabetes} (case-sensitive; use these exact strings)

Evaluation
- Metric: Macro-averaged F1-score over the three classes {normal, prediabetes, diabetes}.
  Rationale: The classes are imbalanced; macro-F1 balances errors across classes and rewards models that perform well on minority classes.
- Submission format: A CSV with exactly two columns [id, label], where id matches the provided test ids (order and count must match) and label ∈ {normal, prediabetes, diabetes}. Case must match exactly. No extra columns are allowed. Duplicate or missing ids will invalidate the submission.

Starter guidance
- Handle categorical encoding (e.g., one-hot) for physical_activity_level.
- Consider class imbalance and decision boundaries near the clinical thresholds; robust models (e.g., gradient boosted trees, calibrated linear models) tend to perform well.
- Cross-validation is recommended.

Important notes
- The label is derived deterministically from glucose thresholds. The glucose measurement itself is intentionally excluded from the released files to prevent trivial solutions.
- Use only the provided columns. IDs are randomized and carry no meaning.
