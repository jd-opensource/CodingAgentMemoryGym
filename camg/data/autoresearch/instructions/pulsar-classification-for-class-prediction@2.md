# OpenMLE-fast task

Task ID: `pulsar-classification-for-class-prediction@2`

Native metric: `PulsarProbabilityMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1058 bytes)
- `data/sample_submission.csv` (94070 bytes); columns: ["Id", "target"]
- `data/test.csv` (364180 bytes); columns: ["Id", "Mean_Integrated", "SD", "EK", "Skewness", "Mean_DMSNR_Curve", "SD_DMSNR_Curve", "EK_DMSNR_Curve", "Skewness_DMSNR_Curve"]
- `data/train.csv` (1384331 bytes); columns: ["Mean_Integrated", "SD", "EK", "Skewness", "Mean_DMSNR_Curve", "SD_DMSNR_Curve", "EK_DMSNR_Curve", "Skewness_DMSNR_Curve", "Class"]

## Public description

Calibrated Pulsar Probability Estimation

Overview
You are given tabular features extracted from candidate radio signals and must predict the probability that each candidate is a true pulsar. The evaluation metric is binary log loss computed on submitted probabilities.

Public files
- train.csv: Training data with columns
  [Mean_Integrated, SD, EK, Skewness, Mean_DMSNR_Curve, SD_DMSNR_Curve, EK_DMSNR_Curve, Skewness_DMSNR_Curve, Class]
- test.csv: Test data for which predictions are required; columns
  [Id, Mean_Integrated, SD, EK, Skewness, Mean_DMSNR_Curve, SD_DMSNR_Curve, EK_DMSNR_Curve, Skewness_DMSNR_Curve]
- sample_submission.csv: Example submission with columns [Id, target], where target is the predicted probability of Class==1
- description.txt: This file

Task and metric
- Predict target = P(Class==1) for each row in test.csv
- Submissions are evaluated using binary log loss on column "target"

Submission format
- CSV with columns [Id, target]
- Id values must exactly match those in test.csv
- target must be a probability in [0, 1]
