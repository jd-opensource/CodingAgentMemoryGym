# OpenMLE-fast task

Task ID: `parents-heights-vs-children-heights-galton-data@1`

Native metric: `GaltonHeightMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2943 bytes)
- `data/sample_submission.csv` (5915 bytes); columns: ["Id", "childHeight"]
- `data/test.csv` (8819 bytes); columns: ["Id", "father", "mother", "midparentHeight", "children", "childNum", "gender"]
- `data/train.csv` (24915 bytes); columns: ["Id", "father", "mother", "midparentHeight", "children", "childNum", "gender", "childHeight"]

## Public description

Competition: Predict Adult Child Height from Parental Heights and Family Context

Problem statement
Build a regression model to predict an adult child’s height (inches) from parental heights and family context. Your model must generalize to entirely unseen families, not just siblings of families it has already seen.

Data description
- Task: Regression — predict childHeight.
- Features available to participants:
  - father: Father’s height (inches)
  - mother: Mother’s height (inches)
  - midparentHeight: Galton’s mid-parent height (inches)
  - children: Number of children in the family (integer)
  - childNum: Birth order index within the family (integer)
  - gender: Child’s sex, one of {male, female}
- Target (train only):
  - childHeight: Adult child’s height (inches)

Files you will use
- train.csv: One row per child. Columns: Id, father, mother, midparentHeight, children, childNum, gender, childHeight.
- test.csv: Same columns as train.csv except childHeight is withheld. Columns: Id, father, mother, midparentHeight, children, childNum, gender.
- sample_submission.csv: Example submission with random but valid predictions. Columns: Id, childHeight.

Important notes
- The split is group-aware by family: all siblings from a given family appear entirely in train or entirely in test. Family identifiers are not included in train/test files to prevent leakage; design your own group-aware validation if you create internal folds.
- Do not rely on row order as a signal. Use only the provided feature columns.
- Units are inches throughout and there are no missing values in the provided data.

Evaluation
Your submission is evaluated using the average of per-gender RMSE:
1) Compute RMSE over the male subset and RMSE over the female subset of the test set, using your predictions and the hidden ground truth for each subset.
2) The final score is the simple average of these two RMSE values.

This metric encourages balanced performance across males and females, preventing over-optimization for one group at the expense of the other, while retaining the precision and interpretability of RMSE.

Submission format
- A CSV file with two columns: Id, childHeight
- Id values must match those in test.csv exactly, with no duplicates or missing rows.
- childHeight must be numeric (floats in inches); predictions must be finite numbers.

Tips
- Consider interactions and non-linearities (e.g., gender × midparentHeight) and regularization to avoid overfitting on this relatively small dataset.
- Use group-aware validation (by family) to estimate generalization to unseen families.
- Standard feature preprocessing (encoding gender, scaling numeric features) is allowed but not required.

Starter baseline idea
- A simple baseline is a gender-specific regularized linear regression on the provided features. Stronger models may incorporate interaction terms and non-linear transforms or use tree-based ensembles.
