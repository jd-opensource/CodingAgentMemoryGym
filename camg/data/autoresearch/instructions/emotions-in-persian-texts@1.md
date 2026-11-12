# OpenMLE-fast task

Task ID: `emotions-in-persian-texts@1`

Native metric: `PersianEmotionMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2484 bytes)
- `data/sample_submission.csv` (11379 bytes); columns: ["id", "emotion"]
- `data/test.csv` (332440 bytes); columns: ["id", "text"]
- `data/train.csv` (1313673 bytes); columns: ["id", "text", "emotion"]

## Public description

Competition: Persian Emotion Classification from Informal Text

Task
Predict the most likely emotion for a given Persian text among seven classes:
ANGRY, HATE, SAD, FEAR, HAPPY, SURPRISED, OTHER.
Build robust models that handle colloquialisms, hashtags, non-standard spellings, variable text lengths, and class imbalance.

Data
Final files provided:
- train.csv: id, text, emotion
- test.csv: id, text
- sample_submission.csv: id, emotion

Notes:
- Texts are Persian and may include slang, emojis, hashtags, digits, and occasional URLs.
- Labels are single-class per text; emotions are case-insensitive in evaluation (canonical set shown above).
- The training set covers all emotion classes present in the test set.
- Index artifacts were dropped, exact duplicates in train were removed, and cross-split text overlaps were eliminated to prevent leakage.
- id values are arbitrary identifiers and carry no signal; do not use them as features.

Recommended approach (non-mandatory)
- Normalize Persian text (e.g., unify ی/ي, ک/ك, remove diacritics, normalize zero-width non-joiner).
- Use tokenization suitable for Persian (handle half-space, clitics).
- Consider noise sources: hashtags, mentions, digits, rare URLs.
- Handle wide length variability via truncation/padding, hierarchical encoders, or character/subword models.
- Address class imbalance (e.g., macro-aware losses, resampling, focal loss).
- Strong baselines: multilingual/Persian pretrained Transformers, subword/character CNN/RNN hybrids.

Evaluation
- Metric: Macro-averaged F1 across the seven classes.
- Rationale: Balances performance across all classes, penalizing models that ignore minority classes.

Submission format
- A single CSV file with columns: id, emotion.
- Each id from test.csv must appear exactly once; no extras or duplicates.
- emotion must be one of: ANGRY, HATE, SAD, FEAR, HAPPY, SURPRISED, OTHER (case-insensitive accepted; normalized during scoring).

How to use the data
- Train your model with train.csv.
- Predict emotions for every row in test.csv.
- Submit a CSV following the submission format. A sample_submission.csv is provided for reference.

Quality and challenge
This competition is challenging yet solvable: informal Persian introduces noise and variability; “OTHER” is broad and nuanced; and class imbalance demands careful modeling. Macro-F1 enforces attention to all classes. With thoughtful preprocessing and modern NLP techniques, strong performance is attainable.
