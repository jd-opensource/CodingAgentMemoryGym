# OpenMLE-fast task

Task ID: `gambling-comments-from-youtube-platform@1`

Native metric: `GamblingCommentClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2474 bytes)
- `data/sample_submission.csv` (22833 bytes); columns: ["id", "label"]
- `data/test.csv` (89529 bytes); columns: ["id", "text"]
- `data/train.csv` (363638 bytes); columns: ["id", "text", "label"]

## Public description

Title: Indonesian YouTube Gambling Comment Detection

Problem statement:
Build a robust text classifier to detect gambling-related comments in Indonesian YouTube conversations. Each comment should be predicted as gambling-related (1) or clean/non-gambling (0). The language is informal and may include slang, emojis, code-mixing, obfuscated brand names, and domain-like tokens.

Files provided to participants:
- train.csv: Columns id, text, label.
- test.csv: Columns id, text.
- sample_submission.csv: Columns id, label.

Data characteristics:
- Comments are short, noisy, and varied. Expect colloquial Indonesian, emojis, stylized spelling, and obfuscated tokens (e.g., brand-like strings and URL patterns).
- Duplicated/templated spam exists. The official split groups exact/near-duplicate variants by a normalized key so a given template appears only in one split, preventing leakage.

Evaluation metric:
- Macro F1 over classes {0,1}. F1 is computed per class and averaged. This balances precision and recall for both classes and avoids majority-class bias.

Submission format:
- A CSV file with header and two columns: id,label.
- Labels must be discrete integers in {0,1}.
- The id order must exactly match test.csv.

Notes and guidance:
- Preprocessing: Consider Indonesian-aware tokenization and Unicode handling. Useful steps include case normalization, emoji handling, URL/domain normalization, and managing repeated characters. Be cautious with stopwords—important cues may be in short functional words.
- Feature engineering: Character n-grams, word/subword n-grams, domain/URL patterns, numeric/alphanumeric token features, and emoji patterns often help. Modern transformer models (e.g., Indonesian or multilingual) can capture semantics and code-mixing.
- Modeling: Both classical ML (e.g., linear models on n-grams) and deep models are applicable. Tune thresholds to optimize macro F1 on your validation strategy.

Split policy:
- A single official train/test split (~80/20) is provided.
- Grouping by normalized text prevents identical or near-identical comments from appearing across splits.
- The test set includes a representative mix of clear gambling promos and benign comments.

Important:
- Keep the id order and values unchanged when creating your submission.
- Labels must be 0 or 1. Numerical stability issues (NaN/inf) are not applicable since labels are discrete.
- The dataset scale is kept; use all provided rows in train.csv for learning.
