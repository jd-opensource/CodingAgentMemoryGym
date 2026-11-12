# OpenMLE-fast task

Task ID: `car-details-dataset@2`

Native metric: `SellerTypeClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2449 bytes)
- `data/sample_submission.csv` (18771 bytes); columns: ["id", "seller_type"]
- `data/test.csv` (63865 bytes); columns: ["id", "name", "year", "km_driven", "fuel", "transmission", "owner"]
- `data/train.csv` (290559 bytes); columns: ["id", "name", "year", "km_driven", "fuel", "transmission", "owner", "seller_type"]

## Public description

Title: Seller Type Classification for Used-Car Listings

Problem statement
Predict the seller_type for each used-car listing from its listing attributes. Classes are: Individual, Dealer, and Trustmark Dealer.

Why this matters
Accurate seller profiling supports marketplace moderation, verification, and inventory curation. The task blends text, categorical, and numeric signals and requires handling class imbalance.

Data description
Each row represents a used-car listing with the following columns:
- name: vehicle model/variant string
- year: manufacturing year (integer)
- km_driven: odometer reading (integer)
- fuel: categorical fuel type
- transmission: categorical gearbox type
- owner: categorical ownership status
- seller_type: target label (Individual, Dealer, Trustmark Dealer)

Important: selling_price has been removed from the modeling files to avoid reverse-causal leakage. Focus your features on the columns listed above.

Files provided
- train.csv: training set with features and the target column seller_type.
- test.csv: test set with the same feature columns as train.csv (no seller_type).
- sample_submission.csv: a sample submission file with the required format.

Recommended approach
- Data processing: clean text in name; derive brand (first token), tokenize variants; normalize numeric fields (e.g., age = reference_year − year, log1p(km_driven)).
- Feature engineering: one-hot or target encoding for fuel, transmission, owner, and brand; n-gram or hashed features for name tokens.
- Modeling: try tree-based models, linear models over token features, or lightweight neural nets. Address class imbalance via class weights or focal loss.
- Evaluation: use cross-validation in training and ensure robust handling of minority classes.

Evaluation metric
Submissions are evaluated using macro F1, the unweighted average of per-class F1 scores over {Individual, Dealer, Trustmark Dealer}. This treats all classes fairly and emphasizes performance on minority classes.

Submission format
- CSV with two columns: id and seller_type.
- id must match the ids in test.csv exactly and appear once each.
- seller_type must be one of: Individual, Dealer, Trustmark Dealer.

Notes
- The split is group-aware to prevent near-duplicate leakage based on the key name|year|km_driven|fuel, and stratified by seller_type to preserve class distribution.
- No external data is required.
- Deterministic behavior ensures reproducibility.
