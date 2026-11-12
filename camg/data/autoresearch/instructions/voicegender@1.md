# OpenMLE-fast task

Task ID: `voicegender@1`

Native metric: `VoiceGenderProbabilityMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2464 bytes)
- `data/sample_submission.csv` (12663 bytes); columns: ["id", "female_probability"]
- `data/test.csv` (214519 bytes); columns: ["id", "meanfreq", "sd", "median", "Q25", "Q75", "IQR", "skew", "kurt", "sp.ent", "sfm", "mode", "centroid", "meanfun", "minfun", "maxfun", "meandom", "mindom", "maxdom", "dfrange", "modindx"]
- `data/train.csv` (875674 bytes); columns: ["id", "meanfreq", "sd", "median", "Q25", "Q75", "IQR", "skew", "kurt", "sp.ent", "sfm", "mode", "centroid", "meanfun", "minfun", "maxfun", "meandom", "mindom", "maxdom", "dfrange", "modindx", "label"]

## Public description

Title: Voice Gender Probability Estimation

Problem statement:
Predict the probability that a recorded voice belongs to a female speaker using pre-computed acoustic features. Participants must build models that output well-calibrated probabilities for the female class.

Data description:
- The dataset contains 3,168 voice samples with 20 numeric acoustic properties per sample extracted over the 0–280 Hz range using standard audio analysis tools.
- Each sample is represented by tabular features including mean frequency, spectral statistics (sd, median, Q25, Q75, IQR), shape descriptors (skew, kurt), spectral entropy/flatness (sp.ent, sfm), mode, centroid, peak frequency, and several fundamental/dominant frequency descriptors (meanfun, minfun, maxfun, meandom, mindom, maxdom, dfrange, modindx).
- The training file includes the features and the binary label indicating male/female; the test file includes only the features and an id column.

Files provided:
- train.csv: id, 20 acoustic feature columns, label (male/female)
- test.csv: id, 20 acoustic feature columns
- sample_submission.csv: id, female_probability (a number in [0, 1])

Submission format:
- A single CSV file with two columns: id and female_probability.
- female_probability must be a numeric value in [0, 1] for each id.

Evaluation metric:
- Submissions are evaluated using LogLoss (binary cross-entropy) on the female class. This proper scoring rule is strict: it penalizes overconfident errors and rewards well-calibrated probabilities, making the task more challenging than simple accuracy.
- To avoid numerical instability, probabilities will be clipped to a small epsilon near 0 and 1 during evaluation.

Guidance and expectations:
- Use the full dataset and all features; do not drop columns. Missing values are not expected.
- Standardization/normalization may help models sensitive to feature scales.
- The problem is balanced across male/female classes, but careful modeling and calibration (e.g., Platt scaling, isotonic regression) are encouraged to achieve strong LogLoss.
- Any supervised ML approach is acceptable (e.g., logistic regression, SVM, gradient boosting, random forests, neural networks), as long as the output is a probability for the female class.

Important notes:
- Train/test splits are stratified and deterministic so participants can focus on modeling and evaluation.
- The final test set does not include labels and should be treated as unseen data.
