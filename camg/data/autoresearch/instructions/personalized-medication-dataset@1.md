# OpenMLE-fast task

Task ID: `personalized-medication-dataset@1`

Native metric: `AdverseReactionRiskMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4099 bytes)
- `data/sample_submission.csv` (5637 bytes); columns: ["Sample_ID", "Adverse_Reactions"]
- `data/test.csv` (21802 bytes); columns: ["Sample_ID", "Age", "Gender", "Weight_kg", "Height_cm", "BMI", "Chronic_Conditions", "Drug_Allergies", "Genetic_Disorders", "Diagnosis", "Symptoms", "Recommended_Medication", "Dosage", "Duration"]
- `data/train.csv` (90415 bytes); columns: ["Sample_ID", "Age", "Gender", "Weight_kg", "Height_cm", "BMI", "Chronic_Conditions", "Drug_Allergies", "Genetic_Disorders", "Diagnosis", "Symptoms", "Recommended_Medication", "Dosage", "Duration", "Adverse_Reactions"]

## Public description

Competition: Adverse Reaction Risk Prediction for Personalized Medication

Problem statement
Given a patient’s profile, medical history, diagnosis, symptoms, and planned treatment details, predict the probability that the patient will experience an adverse reaction (ADR) to the prescribed medication. Your model should output a calibrated probability for ADR = Yes for each test case.

Why this matters
Preventing adverse drug reactions is central to safe personalized pharmacotherapy. Accurate ADR risk estimates enable clinicians to tailor treatment choices and monitoring strategies.

Data
Each row represents a patient-treatment instance. The following columns are provided in the competition files:
- Sample_ID: Unique identifier for a row (do not use to learn clinical signal).
- Age: Numeric age in years.
- Gender: Categorical (e.g., Male, Female, Other).
- Weight_kg: Numeric weight (kg).
- Height_cm: Numeric height (cm).
- BMI: Body mass index as provided.
- Chronic_Conditions: Categorical string; may include a single condition or the literal None.
- Drug_Allergies: Categorical string; may include a single allergen or the literal None.
- Genetic_Disorders: Categorical string; may include a single disorder or the literal None.
- Diagnosis: Primary diagnosis string.
- Symptoms: Comma-separated list of symptoms (text). Values may include multiple items and varying capitalization.
- Recommended_Medication: Medication name string or None.
- Dosage: String with numeric magnitude and unit (e.g., "200 mg", "5 mg", or None).
- Duration: String duration (e.g., "7 days", "30 days", or None).
- Adverse_Reactions: Target label in train.csv only. Binary string with values Yes or No.

Note: Outcome-like fields are excluded from the competition files to avoid target leakage. Dosage and duration are kept in their original textual format; participants may choose to parse units and magnitudes.

Files provided
- train.csv: Training data with features and the target column Adverse_Reactions.
- test.csv: Test data with the same features as train.csv but without Adverse_Reactions.
- sample_submission.csv: Example of a valid submission with columns [Sample_ID, Adverse_Reactions], where Adverse_Reactions contains a probability in [0, 1] for ADR = Yes.

Task
Build a model to estimate P(ADR = Yes) for each row in test.csv using the features above. You may apply any feature engineering and modeling approach, provided that only train.csv is used to learn parameters and no external data with target leakage is used.

Recommended considerations (non-exhaustive)
- Handle missing values: literal "None" strings indicate missingness in several columns.
- Normalize and parse: consider extracting numeric magnitude and units from Dosage and days from Duration.
- Mixed-type encodings: categorical encoding for medical history fields; multi-hot or text features for Symptoms; numeric scaling as needed for continuous features.
- Interactions: clinically plausible interactions (e.g., Age×Dosage, BMI×Dosage, allergy–medication matches) may improve performance.

Evaluation
- Metric: Area Under the ROC Curve (AUROC) on the positive class (ADR = Yes).
  - AUROC is threshold-independent and measures ranking quality across class balances.
- Submission format: a CSV file with two columns (no header changes):
  - Sample_ID
  - Adverse_Reactions: a probability in [0, 1] for ADR = Yes for the corresponding Sample_ID in test.csv.
- Rows in your submission must correspond exactly to the Sample_IDs in test.csv. Order does not matter; matching is performed by Sample_ID.

Rules and checks
- The test set contains both classes; the train/test split is stratified and deterministic.
- Only the columns listed above are present; there is no file path or data outside of these CSVs.
- Do not attempt to infer or use hidden labels. Any label-like columns are withheld from test.csv by design.

Deliverables
- A valid submission CSV [Sample_ID, Adverse_Reactions] with probabilities for all rows in test.csv.

Good luck and build responsibly calibrated models for safer personalized medication!
