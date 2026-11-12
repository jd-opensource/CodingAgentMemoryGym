# OpenMLE-fast task

Task ID: `symptomsxdiagnose-sxd@1`

Native metric: `SymptomsXDiagnosisMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2913 bytes)
- `data/sample_submission.csv` (15821 bytes); columns: ["id", "disease"]
- `data/test.csv` (80168 bytes); columns: ["id", "symptom"]
- `data/train.csv` (357060 bytes); columns: ["id", "symptom", "disease"]

## Public description

SymptomsXDiagnosis (SXD): Symptom-to-Disease Classification

Problem statement
Build a robust multi-class text classifier that maps free-text patient symptom descriptions to the most likely disease. You will be given short-to-long natural-language complaints (lay and clinical phrasing) and must predict a single disease label for each case.

Dataset
We provide a curated, leakage-safe split derived from a large symptoms–diagnoses corpus. Key characteristics:
- Input text only: features are symptom descriptions in natural language. Long and diverse expressions, often multi-sentence.
- Target: a single disease label among dozens of classes (imbalanced, long-tail distribution).
- Curation for quality: contradictory duplicates removed (same text mapped to different labels), exact duplicates deduplicated, and ultra-rare labels pruned to ensure learnability and stable evaluation.
- Split strategy: deterministic, stratified, and group-aware by normalized symptom text so identical texts never appear in both train and test.

Files
- train.csv: columns [id, symptom, disease]
- test.csv: columns [id, symptom]
- sample_submission.csv: example label-format submission with random but valid labels

Target
- disease: a single categorical class per row.

Submission format
Two formats are accepted:
1) Label submission
   - CSV columns: [id, disease]
   - disease values must match one of the labels present in train.csv.

2) Probability submission (supported and encouraged for analysis)
   - CSV columns: [id, <one column per class label>]
   - Column names for class probabilities must exactly match the label strings in train.csv.
   - Values should be probabilities in [0, 1]. Minor numerical issues are handled safely at evaluation.

Evaluation
- Official metric: Macro-averaged F1 across all disease classes present in the test set.
- Scoring details:
  - Probability submissions are converted to labels via row-wise argmax after safe renormalization; label submissions are used directly.
  - Macro-F1 equally weights each class, improving fairness for less frequent conditions compared to accuracy.

Recommended approach
- Text preprocessing: sensible normalization (lowercasing, whitespace normalization), tokenization, handling of long sequences; avoid removing medically relevant tokens.
- Features/models: TF-IDF + linear classifiers (e.g., logistic regression, linear SVM) or fine-tuned transformer encoders; consider class weighting or focal loss.
- Validation: use cross-validation on train.csv; optimize macro-F1.
- Analysis: inspect class balance, calibrate probabilities, and watch for overfitting to phrasing artifacts.

Important notes
- Use only the symptom column as input. No other text or metadata is needed.
- The split is deterministic and group-aware to prevent identical symptom texts from leaking across train and test.
- Every test label occurs in the training set at least once.
