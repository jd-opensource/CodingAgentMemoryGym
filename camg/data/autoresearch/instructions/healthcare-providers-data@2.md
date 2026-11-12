# OpenMLE-fast task

Task ID: `healthcare-providers-data@2`

Native metric: `HealthcareProvidersMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3806 bytes)
- `data/sample_submission.csv` (197034 bytes); columns: ["index", "Place of Service"]
- `data/test.csv` (4618938 bytes); columns: ["index", "National Provider Identifier", "Last Name/Organization Name of the Provider", "First Name of the Provider", "Middle Initial of the Provider", "Credentials of the Provider", "Gender of the Provider", "Entity Type of the Provider", "Street Address 1 of the Provider", "Street Address 2 of the Provider", "City of the Provider", "Zip Code of the Provider", "State Code of the Provider", "Country Code of the Provider", "Provider Type", "Medicare Participation Indicator", "HCPCS Code", "HCPCS Description", "HCPCS Drug Indicator", "Number of Services", "Number of Medicare Beneficiaries", "Number of Distinct Medicare Beneficiary/Per Day Services", "Average Medicare Allowed Amount", "Average Submitted Charge Amount", "Average Medicare Payment Amount", "Average Medicare Standardized Amount"]
- `data/train.csv` (18704742 bytes); columns: ["index", "National Provider Identifier", "Last Name/Organization Name of the Provider", "First Name of the Provider", "Middle Initial of the Provider", "Credentials of the Provider", "Gender of the Provider", "Entity Type of the Provider", "Street Address 1 of the Provider", "Street Address 2 of the Provider", "City of the Provider", "Zip Code of the Provider", "State Code of the Provider", "Country Code of the Provider", "Provider Type", "Medicare Participation Indicator", "Place of Service", "HCPCS Code", "HCPCS Description", "HCPCS Drug Indicator", "Number of Services", "Number of Medicare Beneficiaries", "Number of Distinct Medicare Beneficiary/Per Day Services", "Average Medicare Allowed Amount", "Average Submitted Charge Amount", "Average Medicare Payment Amount", "Average Medicare Standardized Amount"]

## Public description

Title: Predict Place of Service from Medicare Claim Line Items

Background
Health systems and payers analyze where care is delivered—facility (e.g., hospital/outpatient department) versus non‑facility/office—to optimize operations, cost, and quality. This dataset contains 100,000 Medicare physician/supplier claim line items with rich provider, service, geographic, and payment details. The task is to infer the care setting from heterogeneous signals across high‑cardinality codes, free‑text descriptions, demographics, geography, and monetary aggregates.

Problem Statement
Given a claim line item with provider/service attributes, predict the Place of Service:
- F = facility setting
- O = non‑facility/office setting
This is a binary classification problem with moderate class imbalance.

Files Provided
- train.csv: Full training data including the target column Place of Service. Each row is a claim line item. Use the index column as the row identifier.
- test.csv: Test data with the same columns as train.csv except Place of Service is withheld.
- sample_submission.csv: Example submission file with two columns: index and Place of Service. Replace the sample labels with your predictions on test.csv.

Target and Features
- Target: Place of Service (values: F, O).
- Candidate features include, but are not limited to:
  - Provider identifiers and demographics: National Provider Identifier, Last/First/Middle name tokens, Credentials, Gender, Entity Type
  - Location: Street Address 1/2 tokens, City, Zip Code, State Code, Country Code
  - Practice/participation: Provider Type, Medicare Participation Indicator
  - Service characterization: HCPCS Code, HCPCS Description, HCPCS Drug Indicator
  - Utilization and payment aggregates: Number of Services, Number of Medicare Beneficiaries, Number of Distinct Medicare Beneficiary/Per Day Services, Average Medicare Allowed Amount, Average Submitted Charge Amount, Average Medicare Payment Amount, Average Medicare Standardized Amount

Notes for Modeling
- Expect heterogeneous data types: categorical (high cardinality), numeric with heavy tails, and free text (HCPCS Description and potentially names/addresses after tokenization).
- Consider robust numeric parsing and transformations (e.g., removing thousands separators, log transforms) and careful encoding for high‑cardinality categoricals (e.g., hashing, target encoding with cross‑validation, or learned embeddings).
- Text features can help but beware of accidental leakage by using literal tokens that exactly duplicate the target concepts (e.g., “facility”, “office”).

Evaluation
- Metric: Matthews Correlation Coefficient (MCC) computed on the predicted labels for the test set. MCC is robust to class imbalance and accounts for all four cells of the confusion matrix.
- Optimization goal: Maximize MCC.

Submission Format
- A valid submission is a CSV with exactly two columns and a header:
  - index: copied from test.csv
  - Place of Service: your predicted label for each test row, each value must be either F or O
- Do not reorder or drop test rows; your file must contain exactly one prediction per index from test.csv.

Train/Test Split Details
- The data are split by provider to better assess generalization:
  - All rows for a given National Provider Identifier appear entirely in either train or test.
  - The split preserves overall class proportions as much as possible.
- Participants do not need this information to submit, but it informs generalization expectations.

Ethical Use
- This dataset is for research and model development only. Do not attempt to identify individuals.

Good luck building robust solutions that combine thoughtful preprocessing, feature engineering, and strong modeling for this realistic healthcare operations task.
