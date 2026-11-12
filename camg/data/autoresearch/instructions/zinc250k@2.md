# OpenMLE-fast task

Task ID: `zinc250k@2`

Native metric: `ZincSASRegressionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2947 bytes)
- `data/sample_submission.csv` (1200137 bytes); columns: ["id", "SAS"]
- `data/test.csv` (2551110 bytes); columns: ["id", "smiles"]
- `data/train.csv` (14000177 bytes); columns: ["id", "smiles", "SAS"]

## Public description

ZINC-250k Synthetic Accessibility Regression Challenge

Objective:
Predict the Synthetic Accessibility Score (SAS) of small molecules directly from their SMILES strings. SAS quantifies synthesis difficulty: lower scores indicate easier synthesis; higher scores indicate harder synthesis. Build ML models that learn a robust mapping from molecular structure to a continuous SAS value and generalize to unseen molecules.

Data files and columns:
- train.csv
  - id: Unique identifier (sequential integer) for each training molecule.
  - smiles: Canonicalized SMILES string of the molecule.
  - SAS: Synthetic Accessibility Score (continuous target to be predicted).
- test.csv
  - id: Unique identifier (sequential integer) for each test molecule.
  - smiles: Canonicalized SMILES string of the molecule.
- sample_submission.csv
  - id: Must match the ids from test.csv, in exactly the same order.
  - SAS: Your predicted SAS for each id.

Data processing recommendations:
- SMILES parsing: Strip whitespace and embedded newlines before featurization; preserve stereochemistry, charges, aromaticity, and ring information. The provided files exclude invalid entries.
- Representations: You may use any ML-feasible features derived from SMILES, including but not limited to ECFP/Morgan fingerprints, cheminformatics descriptors (e.g., ring counts, TPSA, heteroatom counts), and graph neural networks operating on atom-bond graphs.
- External resources: Computing descriptors from SMILES is allowed. No property columns other than SMILES are provided to avoid leakage.

Evaluation metric:
- Root Mean Squared Error (RMSE) on SAS.
  - RMSE = sqrt(mean((y_true - y_pred)^2)) computed over all test examples after matching by id.
  - Predictions must be valid finite numeric values. Non-finite values (NaN/Inf) are invalid.
  - RMSE is a fair and precise metric for continuous targets, emphasizing larger errors proportionally.

Split and scale:
- A single deterministic 80/20 split is provided, stratified by SAS distribution via binning to preserve distributional characteristics across train and test.
- The full dataset scale is preserved; all available molecules are included in the split.

Submission format rules:
- Submit a CSV with exactly two columns named: id,SAS
- Include every id from test.csv exactly once and in any order; duplicate or missing ids are invalid.
- SAS values must be finite numeric values (floats).

What to build:
- Construct a complete ML pipeline, including data processing, feature engineering, model training, and evaluation.
- Strong baselines include gradient boosting on fingerprints/descriptors and modern GNNs over molecular graphs. Ensembling and uncertainty-aware training are encouraged.

Goal:
Minimize RMSE on SAS predictions for the test molecules. Design your approach to capture complex substructure patterns, ring systems, stereochemistry, and fragment rarity signals present in SMILES-derived structures.
