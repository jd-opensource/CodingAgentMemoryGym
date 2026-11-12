# OpenMLE-fast task

Task ID: `emg-4@1`

Native metric: `EMGGestureClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1892 bytes)
- `data/sample_submission.csv` (3896 bytes); columns: ["label"]
- `data/test.csv` (599861 bytes); columns: ["f_0", "f_1", "f_2", "f_3", "f_4", "f_5", "f_6", "f_7", "f_8", "f_9", "f_10", "f_11", "f_12", "f_13", "f_14", "f_15", "f_16", "f_17", "f_18", "f_19", "f_20", "f_21", "f_22", "f_23", "f_24", "f_25", "f_26", "f_27", "f_28", "f_29", "f_30", "f_31", "f_32", "f_33", "f_34", "f_35", "f_36", "f_37", "f_38", "f_39", "f_40", "f_41", "f_42", "f_43", "f_44", "f_45", "f_46", "f_47", "f_48", "f_49", "f_50", "f_51", "f_52", "f_53", "f_54", "f_55", "f_56", "f_57", "f_58", "f_59", "f_60", "f_61", "f_62", "f_63"]
- `data/train.csv` (3048811 bytes); columns: ["f_0", "f_1", "f_2", "f_3", "f_4", "f_5", "f_6", "f_7", "f_8", "f_9", "f_10", "f_11", "f_12", "f_13", "f_14", "f_15", "f_16", "f_17", "f_18", "f_19", "f_20", "f_21", "f_22", "f_23", "f_24", "f_25", "f_26", "f_27", "f_28", "f_29", "f_30", "f_31", "f_32", "f_33", "f_34", "f_35", "f_36", "f_37", "f_38", "f_39", "f_40", "f_41", "f_42", "f_43", "f_44", "f_45", "f_46", "f_47", "f_48", "f_49", "f_50", "f_51", "f_52", "f_53", "f_54", "f_55", "f_56", "f_57", "f_58", "f_59", "f_60", "f_61", "f_62", "f_63", "label"]

## Public description

EMG-4 Gesture Classification Challenge

Problem statement
Given a short window of surface electromyography (EMG) from an 8-sensor MYO armband (64 numeric features: 8 consecutive readings × 8 sensors), predict the hand gesture class among four options: 0, 1, 2, 3.

Data files provided
- train.csv: Each row contains 64 feature columns (f_0 … f_63) and one target column named label with values in {0,1,2,3}.
- test.csv: Each row contains the same 64 feature columns (f_0 … f_63) without the target.
- sample_submission.csv: A file showing the expected submission format. It has a single column named label and the same number of rows as test.csv.

Task
- Build a machine learning model that generalizes across recording segments and accurately classifies EMG windows into the four gesture classes.
- You may use any ML techniques. Typical pipelines will include data processing (e.g., per-sensor normalization using training statistics), feature engineering (e.g., temporal statistics across the 8-step window, per-sensor z-scores, denoising), model training (e.g., tree ensembles, MLPs, CNNs), and model evaluation.

Evaluation
- Official metric: Macro-averaged F1 score over the four classes.
- Rationale: Class sizes are slightly imbalanced and EMG is noisy; macro F1 equally weights each class and captures the balance of precision and recall.
- Submission format: A single-column CSV with header label and N rows (N = number of rows in test.csv). Each value must be an integer in {0,1,2,3}.

Notes
- The split simulates session-wise generalization by holding out contiguous segments from each gesture class for testing. Train.csv and test.csv already follow this split; no additional metadata is required.
- Use only training statistics for any normalization to avoid leakage.
- Ensure numerical stability in your implementation (handle potential scale differences across sensors).
