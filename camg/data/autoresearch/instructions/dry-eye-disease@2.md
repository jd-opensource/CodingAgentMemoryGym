# OpenMLE-fast task

Task ID: `dry-eye-disease@2`

Native metric: `DryEyeSleepDisorderMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3012 bytes)
- `data/sample_submission.csv` (104878 bytes); columns: ["id", "Sleep_disorder"]
- `data/test.csv` (255475 bytes); columns: ["id", "gender", "age", "stress_level", "bp_sys", "bp_dia", "heart_rate", "daily_steps", "physical_activity", "height_cm", "weight_kg", "caffeine_consumption", "alcohol_consumption", "smoking", "medical_issue", "ongoing_medication", "smart_device_before_bed", "average_screen_time", "blue_light_filter", "discomfort_eye_strain", "redness_in_eye", "itchiness_irritation_in_eye"]
- `data/train.csv` (1053146 bytes); columns: ["id", "gender", "age", "stress_level", "bp_sys", "bp_dia", "heart_rate", "daily_steps", "physical_activity", "height_cm", "weight_kg", "caffeine_consumption", "alcohol_consumption", "smoking", "medical_issue", "ongoing_medication", "smart_device_before_bed", "average_screen_time", "blue_light_filter", "discomfort_eye_strain", "redness_in_eye", "itchiness_irritation_in_eye", "Sleep_disorder"]

## Public description

Dry Eye Sleep Disorder Risk Prediction (Leakage-Controlled)

Problem
Predict the risk of Sleep disorder (Y/N) from demographics, physiology, lifestyle, device/screen behavior, and ocular-surface symptoms — while intentionally excluding direct sleep-experience items that would cause label leakage. Your model should output a calibrated probability P(Sleep_disorder = Y) for each test subject.

Files provided
- train.csv — Training data with features and the target column Sleep_disorder (Y/N).
- test.csv — Test data with features only; predict a probability for Sleep_disorder.
- sample_submission.csv — Example submission file with random valid probabilities.

Target
- Sleep_disorder (Y/N): whether the subject has a sleep disorder.

Features (columns in train.csv/test.csv)
- id: unique row identifier.
- gender: M/F.
- age: years.
- stress_level: integer scale.
- bp_sys, bp_dia: systolic/diastolic blood pressure (mmHg), parsed from the original blood pressure field.
- heart_rate: beats per minute.
- daily_steps: steps per day.
- physical_activity: self-reported physical activity scale.
- height_cm: body height.
- weight_kg: body weight.
- caffeine_consumption: Y/N.
- alcohol_consumption: Y/N.
- smoking: Y/N.
- medical_issue: Y/N.
- ongoing_medication: Y/N.
- smart_device_before_bed: Y/N.
- average_screen_time: average daily screen time (hours).
- blue_light_filter: Y/N.
- discomfort_eye_strain: Y/N.
- redness_in_eye: Y/N.
- itchiness_irritation_in_eye: Y/N.

Important modeling note (leakage control)
The following near-definitional sleep items are not present in the final train/test files and must not be used: sleep duration, sleep quality, waking during night, feeling sleepy during day. Another diagnosis label (Dry Eye Disease) is also excluded to avoid proxy leakage. Your model should rely on the features listed above.

Evaluation
- Metric: Binary log loss (cross-entropy). For each test row i with ground truth y_i in {0,1} and submitted probability p_i in [0,1], the score is the average of −[y_i*log(p_i) + (1−y_i)*log(1−p_i)]. Lower is better. Submissions must contain probabilities, not class labels.

Submission format
- CSV with the following columns:
  - id
  - Sleep_disorder: probability in [0,1] that Sleep_disorder = Y
- The set of ids must exactly match test.csv and contain no duplicates, missing values, NaN/inf, or out-of-range probabilities.

Suggested approach (not required)
- Process types (numeric casting, Y/N encoding if needed), and consider feature engineering (e.g., BMI from height/weight) and interaction effects.
- Train and calibrate probabilistic classifiers (e.g., logistic regression, gradient boosting, tabular neural networks) using cross-validation on train.csv.
- Evaluate with log loss and consider calibration methods (Platt scaling, isotonic regression) if beneficial.

Data scale and split
- All available rows are used (20,000 subjects). A single fixed train/test split is provided; do your own validation strategy on train.csv.
