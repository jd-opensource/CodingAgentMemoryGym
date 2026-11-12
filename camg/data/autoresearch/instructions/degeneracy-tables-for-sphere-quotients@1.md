# OpenMLE-fast task

Task ID: `degeneracy-tables-for-sphere-quotients@1`

Native metric: `HarmonicDegeneracyRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3281 bytes)
- `data/sample_submission.csv` (19459 bytes); columns: ["id", "y"]
- `data/test.csv` (60194 bytes); columns: ["id", "dimension", "space_id", "type", "k", "weights", "p", "q"]
- `data/train.csv` (175446 bytes); columns: ["id", "dimension", "space_id", "type", "k", "weights", "p", "q", "y"]

## Public description

Competition: Invariant Harmonic Degeneracy Prediction across Sphere Quotients (2D–7D)

Problem statement
Participants are given tabular entries describing quotient spaces of spheres under cyclic group actions (including lens spaces and matrix-generated actions), alongside polynomial bidegrees (p, q). The task is to predict the degeneracy: the integer dimension of the space of invariant harmonic homogeneous polynomials of bidegree (p, q) under the specified action.

Data description
- We provide a single consolidated tabular dataset split into train and test, drawn from actions across ambient dimensions 2D–7D.
- Each row corresponds to one (space, p, q) triple with an associated degeneracy.
- Columns in train/test:
  - id: unique identifier per row.
  - dimension: integer ambient dimension (2–7).
  - space_id: string identifier of the action/space (e.g., lens space notation L(k; w1, w2, …) or a generator Matrix([...]) string).
  - type: categorical feature with values {lens, matrix}.
  - k: integer order parameter for lens spaces (present when type=lens; empty otherwise).
  - weights: comma-separated integer weight list for lens spaces (present when type=lens; empty otherwise).
  - p: nonnegative integer (column index in the degeneracy table).
  - q: nonnegative integer (row index in the degeneracy table).
  - y: nonnegative integer degeneracy (only in train).
- Train file contains labels y for supervised learning; Test file omits y.
- A sample_submission.csv is provided, listing all test ids and a placeholder y column to be replaced by your predictions.

Train/test files
- train.csv
- test.csv
- sample_submission.csv

How the data was constructed (for participant clarity)
- The source tables are ragged grids per space/action. Rows correspond to q = 0, 1, 2, … and each row contains a list of degeneracies for p = 0, 1, 2, … until truncation. Placeholders "-" denote out-of-scope entries and were excluded.
- The train/test split is stratified so that every space_id and every dimension appears in both sets, and higher-degree entries (larger p+q) are more frequent in test to assess generalization.

Recommended feature engineering
- Categorical encoding for space_id and type.
- For lens spaces: numerical features from k and weights, such as sums, means, parity flags, gcd(k, wi), residues p·wi mod k and q·wi mod k, (p±q) mod k, etc.
- Core degree features: p, q, p+q, |p−q|, parity indicators, modular residues (p mod k, q mod k, when applicable).
- Dimension indicator.

Evaluation metric
- Root Mean Squared Logarithmic Error (RMSLE) between predictions and ground truth:
  - y_pred is clipped to be ≥ 0 before evaluation.
  - Computation: sqrt(mean((log1p(y_true) − log1p(y_pred_clipped))^2)).
  - This choice balances errors across a wide dynamic range, handles zeros robustly, and reduces dominance of large counts.

Submission format
- A single CSV file with columns:
  - id: matching the ids in test.csv.
  - y: your predicted nonnegative real-valued degeneracy for each id.

Notes
- There is no timeline or prize specified. Focus on building robust models that generalize across dimensions, actions, and degree ranges.
- Validation sets are not provided; participants may use cross-validation as desired on train.csv.
