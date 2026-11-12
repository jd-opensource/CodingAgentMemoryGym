# OpenMLE-fast task

Task ID: `kuesioner-gaya-belajar-vak@1`

Native metric: `VAKLearningStyleMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2529 bytes)
- `data/sample_submission.csv` (2154 bytes); columns: ["id", "label"]
- `data/test.csv` (18579 bytes); columns: ["id", "text"]
- `data/train.csv` (76546 bytes); columns: ["id", "text", "label"]

## Public description

Indonesian Learning Style Classification (VAK)

Problem statement
Build a model that predicts a person’s dominant learning style from Indonesian free-text descriptions of their study habits. Each text is labeled as one of three classes:
- V: Visual
- A: Auditory
- K: Kinesthetic
Your task is to train a robust text classifier that generalizes across formal and colloquial Indonesian, slang, and paraphrases.

Data description
You are given pre-split files:
- train.csv: Training set with columns [id, text, label].
- test.csv: Test set with columns [id, text]. Labels are hidden.
- sample_submission.csv: Example submission with columns [id, label].

Notes and constraints
- Texts are Indonesian sentences/short paragraphs about learning habits. Register varies from formal to colloquial and may include quotes and punctuation.
- Duplicate-aware split: exact duplicate texts never appear in both train and test. Some near-duplicates or paraphrases may exist within the same split.
- All three classes occur in the train set. The class balance is moderately uneven: use robust training and evaluation.
- IDs are opaque and do not reveal labels. Do not assume any ordering signal.
- No external paths or file references are embedded in the CSVs.

Evaluation
Submissions must be a CSV file with columns [id, label] (in this exact order), one row per test example. Labels must be one of {V, A, K}.
Leaderboard metric: Macro-averaged F1 across the three classes. For each class c in {V, A, K}:
- F1_c = 2 * TP_c / (2 * TP_c + FP_c + FN_c)
- Macro-F1 = mean(F1_V, F1_A, F1_K)
This metric is fair for moderately imbalanced multiclass classification and rewards balanced performance across all classes.

Rules and recommendations
- You are encouraged to use any text-processing or ML approach, including bag-of-ngrams, classical linear models, or pretrained Indonesian/multilingual language models.
- Consider normalization for colloquialisms and punctuation, but avoid over-cleaning that removes useful lexical cues.
- Feature engineering ideas: character n-grams (robust to slang), subword tokenization, length or punctuation density features.
- Regularization and careful hyperparameter tuning are important due to dataset size.
- Be mindful of potential data leakage when experimenting with duplicate handling.

Files to submit and format
- Submit a single CSV named however you like, with header and columns exactly [id, label].
- id must match those in test.csv; label must be in {V, A, K}.

Good luck and selamat berkompetisi!
