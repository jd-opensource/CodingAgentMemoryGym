# OpenMLE-fast task

Task ID: `az-medicine-dataset-of-india@2`

Native metric: `MedicineDiscontinuationAUPRCMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3635 bytes)
- `data/sample_submission.csv` (1311964 bytes); columns: ["id", "is_discontinued"]
- `data/test.csv` (6159814 bytes); columns: ["id", "name", "price_inr", "manufacturer_name", "type", "pack_size_label", "short_composition1", "short_composition2"]
- `data/train.csv` (25060551 bytes); columns: ["id", "name", "price_inr", "manufacturer_name", "type", "pack_size_label", "short_composition1", "short_composition2", "is_discontinued"]

## Public description

Competition: Discontinued Medicine Availability Prediction

Background
As of November 2022, the dataset provides a snapshot of whether a medicine SKU is discontinued (no longer available in the market). Anticipating discontinuation from product descriptors helps inventory planners, distributors, and pharmacy platforms mitigate stock risks, identify substitutes early, and improve procurement decisions.

Problem statement
Given textual and categorical descriptors of a medicine SKU (e.g., product name, manufacturer, type, pack size, composition) together with numerical price information, predict the probability that the SKU is discontinued. This is a binary classification task evaluated using area under the precision–recall curve (AUPRC), with higher values indicating better ranking of discontinued items.

Files provided
- train.csv: Feature columns and target label for training. Target column is "is_discontinued" with values 0/1.
- test.csv: Same feature columns as train.csv, but without the target label. Participants must predict the probability of discontinuation for each row.
- sample_submission.csv: Example submission format with random but valid probabilities.

Data description
Each row corresponds to a medicine SKU. The final columns include:
- id: Unique integer identifier.
- name: Product name (text).
- price_inr: Price in INR as of Nov 2022 (numeric).
- manufacturer_name: Manufacturer name (text).
- type: Broad category (e.g., allopathy).
- pack_size_label: Packaging descriptor (text).
- short_composition1: Main composition string (text; may be empty).
- short_composition2: Secondary composition string (text; may be empty).
- is_discontinued: Target label in train.csv only (0 for available, 1 for discontinued).

Participants are encouraged to:
- Clean and normalize messy text fields (spelling variants, case, punctuation).
- Engineer features from compositions and pack size (e.g., extract dosages, counts, volume, ingredient indicators).
- Use robust models that handle high-cardinality categorical variables (e.g., target encoding, embeddings) and text (e.g., TF-IDF, transformer models, or hybrid approaches).
- Leverage price and manufacturer details to capture market signals.

Submission format
- CSV file with exactly two columns: id, is_discontinued
- id must match all and only the ids in test.csv, with exactly one prediction per id.
- is_discontinued must be a probability in [0, 1].
- Do not include any additional columns.

Evaluation metric
- Primary metric: Area Under the Precision–Recall Curve (AUPRC, a.k.a. Average Precision).
- AUPRC focuses on ranking positive (discontinued) items ahead of negatives and is well-suited for imbalanced datasets.
- We compute Average Precision by sorting predictions in descending order, tracing the precision–recall curve across thresholds, and integrating precision with respect to recall. Predictions must be valid probabilities; invalid values (NaN/inf/out of [0,1]) will be rejected.

Train/test split details
- The split is stratified by the target label to ensure both classes appear in the training set.
- The test set contains a representative class distribution.
- The train.csv and test.csv contain identical feature columns in the same order; only train.csv includes the target label.

Tips
- Treat extreme or missing prices carefully; consider log transforms.
- Extract dosage and pack counts from text fields.
- Handle manufacturer and product name high cardinality via appropriate encodings.
- Use calibrated probability outputs (e.g., Platt scaling or isotonic) for better AUPRC performance.

Good luck and happy modeling!
