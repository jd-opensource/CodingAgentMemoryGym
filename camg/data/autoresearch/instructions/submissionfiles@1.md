# OpenMLE-fast task

Task ID: `submissionfiles@1`

Native metric: `FertilizerClozeMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2492 bytes)
- `data/sample_submission.csv` (580252 bytes); columns: ["example_id", "target_token"]
- `data/test.csv` (1126430 bytes); columns: ["example_id", "id", "masked_text", "mask_index"]
- `data/train.csv` (5166513 bytes); columns: ["example_id", "id", "masked_text", "mask_index", "target_token"]

## Public description

Fertilizer Combo Cloze — Predict the Missing Token in Short Product Names

Problem statement
Participants are given short fertilizer product-name strings composed of 2–3 tokens drawn from a small, imbalanced vocabulary (e.g., NPK formulations like 10-26-26, 14-35-14, 17-17-17, 20-20, 28-28 and descriptors like Urea, DAP). Each training example masks exactly one token with a special placeholder [MASK]. The task is to predict the exact missing token based on the remaining context tokens.

Data provided
- train.csv: Labeled masked examples with columns
  - example_id: Unique identifier for each masked example
  - id: Numeric identifier grouping related strings; all examples derived from the same id are either all in train or all in test
  - masked_text: A single string consisting of 2–3 tokens separated by single spaces, with exactly one token replaced by [MASK]
  - mask_index: Integer position of the masked token (0-based)
  - target_token: The ground-truth token that replaces [MASK]
- test.csv: Unlabeled masked examples with columns
  - example_id
  - id
  - masked_text
  - mask_index
- sample_submission.csv: A sample template demonstrating the required submission format with columns
  - example_id
  - target_token

Notes on tokenization and formatting
- Tokens are separated by single spaces; hyphens inside tokens (e.g., 10-26-26) are preserved.
- The masked_text always contains exactly one [MASK] token.
- Strings are normalized to single-space separation; no stemming or lowercasing is applied.
- Sequence length is either 2 or 3 tokens.

Evaluation
- Primary metric: Macro-averaged F1 across token classes present in the test set. This treats rare tokens fairly and avoids majority-class dominance.

Submission format
- The submitted CSV must contain exactly the rows corresponding to test.csv and must have columns: example_id, target_token.
- Each row’s example_id must match one row in test.csv.
- target_token must be a single token string (e.g., Urea, DAP, 10-26-26, 20-20, 28-28, 17-17-17, 14-35-14, …).

Train/test split design
- All examples derived from the same id are grouped and placed entirely in either train or test to prevent leakage.
- The train set covers every token class that appears in the test set at least once, ensuring feasibility for classification models.

Goal
Build a model that, for each masked example in test.csv, outputs the exact missing token in target_token. Optimize macro-F1 while maintaining strong overall accuracy.
