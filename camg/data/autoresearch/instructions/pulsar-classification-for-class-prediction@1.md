# OpenMLE-fast task

Task ID: `pulsar-classification-for-class-prediction@1`

Native metric: `PulsarClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2423 bytes)
- `data/sample_submission.csv` (31122 bytes); columns: ["Id", "Class"]
- `data/test.csv` (355903 bytes); columns: ["Id", "Mean_Integrated", "SD", "EK", "Skewness", "Mean_DMSNR_Curve", "SD_DMSNR_Curve", "EK_DMSNR_Curve", "Skewness_DMSNR_Curve"]
- `data/train.csv` (1459146 bytes); columns: ["Id", "Mean_Integrated", "SD", "EK", "Skewness", "Mean_DMSNR_Curve", "SD_DMSNR_Curve", "EK_DMSNR_Curve", "Skewness_DMSNR_Curve", "Class"]

## Public description

Pulsar Candidate Detection: Imbalanced Binary Classification

Background
Radio astronomy surveys produce vast numbers of candidate pulse detections, but only a small fraction are genuine pulsars. Each candidate can be summarized by statistical features computed from the integrated pulse profile and the dispersion measure signal-to-noise ratio (DM SNR) curve.

Problem statement
You are given 8 numerical features per candidate observation. Your task is to predict the probability that a candidate is a true pulsar (Class=1). The challenge is substantially imbalanced: positives are rare compared to negatives. Models must be robust to heavy-tailed feature distributions and class imbalance.

Data description
- Train file: train.csv
  - Columns: Id, Mean_Integrated, SD, EK, Skewness, Mean_DMSNR_Curve, SD_DMSNR_Curve, EK_DMSNR_Curve, Skewness_DMSNR_Curve, Class
  - Class is the binary target label (0 = non-pulsar, 1 = pulsar).
- Test file: test.csv
  - Columns: Id, Mean_Integrated, SD, EK, Skewness, Mean_DMSNR_Curve, SD_DMSNR_Curve, EK_DMSNR_Curve, Skewness_DMSNR_Curve
  - No label is provided for test rows.
- Sample submission: sample_submission.csv
  - Columns: Id, Class
  - Class must be your predicted probability P(Class=1) per Id.

Notes
- Id is an arbitrary integer identifier that carries no information about the label and does not reveal any ordering.
- The dataset is purely numerical and clean. Nevertheless, several features are heavy-tailed and may benefit from robust scaling and/or transformation.

Evaluation
- Metric: Average Precision (area under the precision-recall curve, AUPRC) for the positive class (Class=1).
  - This metric is threshold-free and appropriate for class-imbalanced detection problems. Random guessing yields a baseline close to the positive class prevalence.
- Submission format: A CSV file with exactly two columns: Id and Class. The Id set must exactly match the Ids in test.csv, and Class must be a valid probability in [0, 1].

Suggested approaches (optional)
- Carefully handle class imbalance (e.g., stratified CV, class weights, focal loss, resampling).
- Consider feature transformations for skewed distributions (e.g., log1p on positive features) and robust scaling.
- Strong baselines include calibrated linear models, tree ensembles (Random Forests, Gradient Boosting/GBMs), and modern tabular methods. Ensemble and calibration can improve probability quality.
