# OpenMLE-fast task

Task ID: `pulsar-dataset@1`

Native metric: `PulsarAveragePrecisionMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1812 bytes)
- `data/sample_submission.csv` (88929 bytes); columns: ["row_id", "target_class"]
- `data/test.csv` (355981 bytes); columns: ["row_id", "Mean_of_the_integrated_profile", "Standard_deviation_of_the_integrated_profile", "Excess_kurtosis_of_the_integrated_profile", "Skewness_of_the_integrated_profile", "Mean_of_the_DM-SNR_curve", "Standard_deviation_of_the_DM-SNR_curve", "Excess_kurtosis_of_the_DM-SNR_curve", "Skewness_of_the_DM-SNR_curve"]
- `data/train.csv` (1459442 bytes); columns: ["row_id", "Mean_of_the_integrated_profile", "Standard_deviation_of_the_integrated_profile", "Excess_kurtosis_of_the_integrated_profile", "Skewness_of_the_integrated_profile", "Mean_of_the_DM-SNR_curve", "Standard_deviation_of_the_DM-SNR_curve", "Excess_kurtosis_of_the_DM-SNR_curve", "Skewness_of_the_DM-SNR_curve", "target_class"]

## Public description

Pulsar Candidate Discovery: Imbalanced Tabular Classification

Problem statement
- Identify real pulsars among many non-pulsar candidates using 8 statistical descriptors derived from the integrated pulse profile and the DM–SNR curve. Submit well-ranked probabilities for the positive class (target_class=1) to prioritize true pulsars for follow-up.

Files provided
- train.csv: Training data with all 8 numeric features and the binary label target_class. Includes a row_id column.
- test.csv: Test set with the same features and row_id, but without labels.
- sample_submission.csv: Example submission file containing row_id and a plausible predicted probability for target_class.

Data description
- Features (all numeric and continuous):
  1) Mean_of_the_integrated_profile
  2) Standard_deviation_of_the_integrated_profile
  3) Excess_kurtosis_of_the_integrated_profile
  4) Skewness_of_the_integrated_profile
  5) Mean_of_the_DM-SNR_curve
  6) Standard_deviation_of_the_DM-SNR_curve
  7) Excess_kurtosis_of_the_DM-SNR_curve
  8) Skewness_of_the_DM-SNR_curve
- Target: target_class — 1 indicates a pulsar, 0 indicates a non-pulsar.
- Class imbalance: The positive class is rare (≈9% of examples). Handle imbalance carefully.

Task
- Train any supervised model(s) to produce predicted probabilities for target_class on the test set.
- You may use any feature preprocessing, scaling, and model ensembling techniques.

Evaluation
- Submissions are evaluated using Average Precision (area under the precision–recall curve) for the positive class.
- Submission format: A CSV with two columns in this exact order and header names:
  - row_id: integer identifiers matching those in test.csv
  - target_class: predicted probability in [0, 1]

Submission example
row_id,target_class
0,0.031
1,0.742
2,0.015
...
