# OpenMLE-fast task

Task ID: `fraud-detection-bank-dataset-20k-records-binary@1`

Native metric: `BankFraudDetectionMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2677 bytes)
- `data/sample_submission.csv` (98251 bytes); columns: ["row_id", "prediction"]
- `data/test.csv` (869057 bytes); columns: ["row_id", "col_0", "col_1", "col_2", "col_3", "col_4", "col_5", "col_6", "col_7", "col_13", "col_14", "col_15", "col_16", "col_17", "col_22", "col_23", "col_24", "col_25", "col_26", "col_27", "col_28", "col_29", "col_30", "col_31", "col_32", "col_33", "col_34", "col_36", "col_37", "col_38", "col_39", "col_40", "col_41", "col_42", "col_43", "col_44", "col_45", "col_46", "col_47", "col_48", "col_49", "col_50", "col_54", "col_55", "col_56", "col_57", "col_58", "col_59", "col_60", "col_61", "col_62", "col_63", "col_64", "col_65", "col_66", "col_67", "col_68", "col_69", "col_72", "col_73", "col_74", "col_75", "col_76", "col_77", "col_78", "col_79", "col_80", "col_81", "col_82", "col_83", "col_84", "col_85", "col_86", "col_87", "col_88", "col_89", "col_90", "col_91", "col_92", "col_93", "col_94", "col_95", "col_96", "col_97", "col_98", "col_99", "col_100", "col_101", "col_102", "col_103", "col_104", "col_105", "col_106", "col_107", "col_108", "col_109", "col_110", "col_111"]
- `data/train.csv` (3427330 bytes); columns: ["col_0", "col_1", "col_2", "col_3", "col_4", "col_5", "col_6", "col_7", "col_13", "col_14", "col_15", "col_16", "col_17", "col_22", "col_23", "col_24", "col_25", "col_26", "col_27", "col_28", "col_29", "col_30", "col_31", "col_32", "col_33", "col_34", "col_36", "col_37", "col_38", "col_39", "col_40", "col_41", "col_42", "col_43", "col_44", "col_45", "col_46", "col_47", "col_48", "col_49", "col_50", "col_54", "col_55", "col_56", "col_57", "col_58", "col_59", "col_60", "col_61", "col_62", "col_63", "col_64", "col_65", "col_66", "col_67", "col_68", "col_69", "col_72", "col_73", "col_74", "col_75", "col_76", "col_77", "col_78", "col_79", "col_80", "col_81", "col_82", "col_83", "col_84", "col_85", "col_86", "col_87", "col_88", "col_89", "col_90", "col_91", "col_92", "col_93", "col_94", "col_95", "col_96", "col_97", "col_98", "col_99", "col_100", "col_101", "col_102", "col_103", "col_104", "col_105", "col_106", "col_107", "col_108", "col_109", "col_110", "col_111", "targets"]

## Public description

Competition: Bank Transaction Fraud Probability Ranking

Problem statement:
Given anonymized numerical features describing individual bank transactions, build a machine learning model that assigns a probability of fraud to each transaction. The primary objective is effective risk ranking: fraudulent transactions should receive higher scores than non-fraud.

Files provided:
- train.csv: Labeled training data with feature columns and the binary target column.
- test.csv: Unlabeled test data with the same feature columns and a row_id column.
- sample_submission.csv: A sample submission in the required format with deterministic random probabilities.

Target and features:
- Target: targets (binary, 0 = non-fraud, 1 = fraud).
- Features: anonymized numeric columns named col_0, col_1, ..., col_111, with strictly constant features removed to eliminate noise. There are no missing values. After preprocessing, the train/test feature sets are identical and ordered consistently.
- Identifiers: test.csv includes a row_id column (integer 0..N_test-1) that uniquely identifies test rows for submission alignment.

Task:
- Train an ML model on train.csv to predict the probability of fraud for each transaction in test.csv.
- Submit a CSV with exactly two columns:
  - row_id: the unique identifier for each test row (must match test.csv)
  - prediction: your predicted fraud probability in [0, 1] for each row

Evaluation:
- Metric: ROC AUC (Area Under the Receiver Operating Characteristic Curve).
- Rationale: ROC AUC is threshold-independent and evaluates how well your scores rank fraudulent transactions above non-fraudulent ones. It is fair under moderate class imbalance and widely used for fraud detection.
- Submission checks:
  - The submission must contain exactly the columns row_id and prediction in that order.
  - row_id values must match test.csv exactly and be unique.
  - prediction must be numeric and finite; values are clipped to [0, 1] before scoring.

Guidance and recommendations:
- Data processing: treat all features as numeric; constant features have already been removed in the provided files. Consider robust scaling for linear models; tree-based methods can work on raw values.
- Feature engineering: explore interactions, monotonic constraints, and regularization to manage sparsity and high dimensionality.
- Model training: stratified cross-validation is recommended due to class imbalance. Popular choices include gradient boosting (LightGBM, XGBoost, CatBoost) and regularized linear models.
- Model evaluation: focus on ranking quality; calibration (isotonic or Platt) can improve practical interpretability but does not affect the ROC AUC.
