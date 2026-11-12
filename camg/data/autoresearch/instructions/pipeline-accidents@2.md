# OpenMLE-fast task

Task ID: `pipeline-accidents@2`

Native metric: `PipelineIncidentCauseMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2866 bytes)
- `data/sample_submission.csv` (12176 bytes); columns: ["Report Number", "Cause Category"]
- `data/test.csv` (80867 bytes); columns: ["Report Number", "Accident Year", "Accident Date/Time", "Operator ID", "Operator Name", "Pipeline/Facility Name", "Pipeline Location", "Pipeline Type", "Liquid Type", "Liquid Subtype", "Liquid Name", "Accident City", "Accident County", "Accident State", "Accident Latitude", "Accident Longitude"]
- `data/train.csv` (509091 bytes); columns: ["Report Number", "Accident Year", "Accident Date/Time", "Operator ID", "Operator Name", "Pipeline/Facility Name", "Pipeline Location", "Pipeline Type", "Liquid Type", "Liquid Subtype", "Liquid Name", "Accident City", "Accident County", "Accident State", "Accident Latitude", "Accident Longitude", "Cause Category"]

## Public description

Competition: Pipeline Incident Cause Prediction

Problem statement:
Predict the investigated Cause Category (7 classes) of a hazardous liquid pipeline incident from descriptors available at or near the time of occurrence. Participants must build a robust multiclass classifier that generalizes temporally.

Files provided:
- train.csv: Tabular incident records with features plus the target column Cause Category.
- test.csv: Same columns as train.csv except Cause Category is withheld.
- sample_submission.csv: Example submission with the required format.

Target and labels:
- Target column: Cause Category
- Classes (labels to predict; case-sensitive):
  ALL OTHER CAUSES; CORROSION; EXCAVATION DAMAGE; INCORRECT OPERATION; MATERIAL/WELD/EQUIP FAILURE; NATURAL FORCE DAMAGE; OTHER OUTSIDE FORCE DAMAGE

Feature columns included (no outcome/severity columns):
- Report Number (identifier for correspondence)
- Accident Year
- Accident Date/Time (local timestamp as recorded)
- Operator ID; Operator Name
- Pipeline/Facility Name; Pipeline Location; Pipeline Type
- Liquid Type; Liquid Subtype; Liquid Name
- Accident City; Accident County; Accident State
- Accident Latitude; Accident Longitude

Recommended feature engineering and preprocessing (participants are expected to do this):
- Calendar features from Accident Date/Time: month, hour, day-of-week, season.
- Clean and encode categorical text (trim, unify case, handle stray quotes). Consider one-hot, target/frequency encoding, or hashing for high-cardinality fields (e.g., Operator Name, Pipeline/Facility Name).
- Geospatial features: use state; bucket latitude/longitude into coarse grids to capture regional effects; distances are optional.
- Handle missing values explicitly (e.g., "Unknown").

Split strategy:
- Chronological split to reflect realistic deployment: train contains earlier years (2010–2015) and test contains later years (2016–2017). This reduces leakage from future distributions into past.

Evaluation:
- Metric: Macro F1-score across the 7 classes. The macro average treats each class equally, encouraging balanced performance across both common and rarer causes. Per-class F1 is computed from precision and recall; if a class has no true positives and no predicted positives, its F1 is defined as 0.
- Submission format: A CSV with exactly two columns in this order: [Report Number, Cause Category].
  - Report Number must match test.csv exactly and be in the same order; no extra/missing/duplicated IDs.
  - Cause Category predictions must exactly match one of the allowed class names above (case-sensitive).

Notes:
- No severity, response, or cost/outcome columns are included, keeping the task focused on descriptors available at or near occurrence.
- Do not include data paths in any CSV.
- Ensure deterministic training/evaluation in your workflow to replicate results.
