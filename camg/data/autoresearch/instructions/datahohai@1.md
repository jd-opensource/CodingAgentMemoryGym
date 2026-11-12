# OpenMLE-fast task

Task ID: `datahohai@1`

Native metric: `GPT2ParameterDriftMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3705 bytes)
- `data/sample_submission.csv` (173534 bytes); columns: ["id", "target"]
- `data/test.csv` (538445 bytes); columns: ["id", "tensor_name", "flat_index", "value_230k", "tensor_mean_230k", "tensor_std_230k", "layer_type", "shape_dim0", "shape_dim1", "global_step", "lr_hint"]
- `data/train.csv` (898636 bytes); columns: ["id", "tensor_name", "flat_index", "value_230k", "tensor_mean_230k", "tensor_std_230k", "layer_type", "shape_dim0", "shape_dim1", "global_step", "lr_hint", "target"]

## Public description

Competition: Forecasting GPT-2 Parameter Drift (230k → 240k)

Problem statement
- Given the state of a fine-tuned GPT-2 (small) model at global training step 230,000, predict the future parameter values at step 240,000 for a masked subset of scalar parameters. Each training example corresponds to a single parameter entry identified by its tensor and flattened index. This is a large-scale supervised regression task grounded in realistic optimizer and schedule dynamics.

What you are given
- train.csv: parameter entries with features from the 230k checkpoint and the ground-truth target values at 240k.
- test.csv: parameter entries with the same features but without target values.
- sample_submission.csv: a valid submission template with randomized but plausible numeric predictions.

Targets
- For each row in the test data, predict the scalar parameter value at 240k for the specified tensor and flattened index.

Final files
- train.csv: features + target column.
- test.csv: features only.
- sample_submission.csv: submission template with columns [id, target].

Feature schema (columns)
- id: unique identifier for a parameter entry, constructed as "{tensor_name}__{flat_index}".
- tensor_name: name of the tensor in the model state dict.
- flat_index: index of the parameter within the flattened tensor.
- value_230k: the parameter value at step 230,000 at that position.
- tensor_mean_230k: mean of the entire tensor at 230k.
- tensor_std_230k: standard deviation of the entire tensor at 230k (epsilon applied if numerically zero).
- layer_type: coarse layer role derived from the tensor name (e.g., embeddings, attention QKV/proj, MLP in/out, layernorm).
- shape_dim0, shape_dim1: the first two dimensions of the tensor shape (1 for missing dims in 1D tensors).
- global_step: constant 230000 for all rows.
- lr_hint: learning-rate hint extracted from trainer logs near 230k (constant across rows).
- target: only present in train.csv; the scalar parameter value at 240k.

Evaluation
- Metric: macro-averaged Normalized RMSE (NRMSE) across tensors.
  - For each tensor t present in the test set, compute RMSE of predictions vs. targets over only the rows of that tensor. Normalize that RMSE by the tensor’s standard deviation at 230k. Average NRMSE equally across tensors. Lower is better.
- Rationale: Normalization by per-tensor scale prevents large tensors from dominating and yields a fair comparison across tensors and layer roles. RMSE penalizes large deviations and rewards models that capture true update dynamics.

Submission format
- CSV with columns:
  - id: must match exactly the ids in test.csv.
  - target: your predicted scalar parameter value at 240k for each id.
- The order of rows may differ, but ids must be a permutation of test.csv ids. No extra or missing ids.

Notes and guidance
- Strong baseline: identity (predict value_230k) is reasonable but not optimal. Improving beyond it typically requires leveraging tensor-wise statistics, layer roles, and the lr_hint.
- Feature engineering examples: per-tensor z-scores, layer-type grouping, interaction terms, or modeling updates as functions of value_230k and lr_hint.
- You may design models per tensor/layer type or a single global regressor; tree-based and neural baselines are viable.
- Numerical care: handle potential degenerate std values with a small epsilon; ensure predictions are finite floats.

Important
- Do not assume access to the 240k checkpoint. Targets in train.csv and the hidden answers for test.csv are derived from that checkpoint by the host and are not distributed.
- The test set contains rows across a range of tensors and indices; model generalization across layer types is essential.
