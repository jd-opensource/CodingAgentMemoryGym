# OpenMLE-fast task

Task ID: `e-coli-resistance-dataset@1`

Native metric: `EColiResistanceMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3613 bytes)
- `data/sample_submission.csv` (143735 bytes); columns: ["row_id", "phenotype"]
- `data/test.csv` (812789 bytes); columns: ["row_id", "antibiotic", "measurement_value", "measurement_sign", "measurement_unit", "testing_standard", "testing_standard_year", "laboratory_typing_method", "laboratory_typing_platform", "vendor", "genome_id", "evidence"]
- `data/train.csv` (1372419 bytes); columns: ["row_id", "antibiotic", "measurement_value", "measurement_sign", "measurement_unit", "testing_standard", "testing_standard_year", "laboratory_typing_method", "laboratory_typing_platform", "vendor", "genome_id", "evidence", "phenotype"]

## Public description

Problem title: Breakpoint Learning Challenge — Predict AST Phenotypes (S/I/R) from MIC/Zone + Standards

Overview
Clinical microbiology reports antimicrobial susceptibility as categorical phenotypes (susceptible/intermediate/resistant) derived from quantitative measurements (e.g., MIC in mg/L or disk diffusion zone in mm) using interpretive standards such as CLSI or EUCAST that vary by antibiotic and year. Your task is to learn these decision rules directly from raw historical records without relying on external breakpoint tables.

Task
Given rows describing E. coli antimicrobial susceptibility tests with quantitative measurements and metadata (antibiotic name, testing standard, etc.), predict the susceptibility phenotype category for each record in the hidden test set.

Data files
- train.csv: Labeled training data with features and the target column.
- test.csv: Unlabeled test data with the same feature columns.
- sample_submission.csv: Example submission file with the required format.

Target and features
- Target column in train.csv: phenotype (values: susceptible, intermediate, resistant; all lowercase).
- Candidate feature columns include (names as in train/test files):
  - row_id: Unique identifier of the record.
  - antibiotic: Normalized antibiotic name (lowercase, trimmed).
  - measurement_value: Numeric value from the test (float; e.g., MIC value or zone diameter).
  - measurement_sign: One of <=, <, =, >=, >.
  - measurement_unit: Either mg/L (MIC) or mm (disk diffusion).
  - testing_standard: Normalized testing standard (e.g., CLSI, EUCAST, NARMS, BSAC).
  - testing_standard_year: Year of the testing standard when available (integer or empty).
  - laboratory_typing_method: Lab method (e.g., MIC, Broth dilution, Disk diffusion).
  - laboratory_typing_platform: Platform/instrument when available (e.g., VITEK 2, Sensititre).
  - vendor: Vendor/manufacturer when available.
  - genome_id: Identifier of the genome/isolate (may act as a random effect).
  - evidence: Evidence/source tag.

Notes
- All features are provided as-is to enable flexible feature engineering (e.g., encoding units, handling measurement signs, interacting with antibiotic and standard/year).
- The test set does not contain the phenotype column.

Evaluation
- Metric: Macro F1 across classes {susceptible, intermediate, resistant}.
  - F1 is computed per class and averaged. Classes with zero support in the test set are ignored in the average to ensure fairness.
  - The submission must include exactly the test row_id values and one predicted label from the allowed set for each row.

Submission format
- A CSV file with the following columns in this exact order:
  - row_id: Integer identifier found in test.csv.
  - phenotype: One of susceptible, intermediate, resistant (lowercase).

Suggested modeling approach
- Parse and encode measurement_value together with measurement_sign and measurement_unit.
- Use antibiotic, testing_standard, and testing_standard_year to allow class-specific decision boundaries.
- Gradient boosted trees or similar tabular models usually work well; careful preprocessing and per-antibiotic modeling can improve performance.
- Consider class imbalance (intermediate is often rare); class-weighting or focal losses may help.

Data integrity and leakage
- The provided files remove the target from test.csv and avoid any columns that directly reveal labels.
- No external breakpoint tables are provided; solutions must learn from the provided training data.

Good luck and have fun pushing the limits of interpretable clinical ML on antibiotic susceptibility data!
