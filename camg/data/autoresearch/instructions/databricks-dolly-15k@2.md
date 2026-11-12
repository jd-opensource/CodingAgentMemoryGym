# OpenMLE-fast task

Task ID: `databricks-dolly-15k@2`

Native metric: `EvidenceGroundedQAMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3303 bytes)
- `data/sample_submission.csv` (42660 bytes); columns: ["id", "response"]
- `data/test.csv` (370561 bytes); columns: ["id", "instruction", "context"]
- `data/train.csv` (2660917 bytes); columns: ["id", "instruction", "context", "response"]

## Public description

Title: Evidence-Grounded Short-Form QA Challenge

Problem statement
Given an instruction (question or extraction directive) and an accompanying reference passage (context), predict a concise, factual answer grounded in the provided context. Outputs are short free-form strings; long-form generation is out of scope.

Data description
- train.csv: id, instruction, context, response
  - instruction: The question or extraction instruction.
  - context: The supporting passage. Wikipedia-style citation markers like [42] have been removed and whitespace normalized.
  - response: The short gold answer (≤ 40 tokens) to be predicted.
- test.csv: id, instruction, context
  - The same fields as train.csv, without the response.
- sample_submission.csv: id, response
  - A valid example submission file using the test ids.

Source and selection
Examples are drawn from two objective, evidence-grounded categories with reliable automatic scoring:
- closed_qa
- information_extraction
Only items with non-empty context and short answers (≤ 40 whitespace tokens) are included. Items with empty instruction/response are removed. Contexts are lightly cleaned to remove bracketed citation markers (e.g., [42]) and to normalize whitespace.

Split protocol
- Deterministic 85/15 train/test split.
- Grouped by identical context (hash) to prevent near-duplicate leakage across splits.
- Category balance is preserved at the group level as much as possible.
- Each example has a unique opaque id; train/test are disjoint and cover the full selected set.

Task
Predict the response for each row in test.csv using the instruction and context. Solutions typically involve:
- Data preprocessing (e.g., tokenization, truncation, normalization)
- Feature engineering or retrieval (e.g., TF-IDF, dense retrieval, reranking)
- Reader/generator modeling (e.g., span extractors, encoder-decoders)
- Inference and post-processing

Evaluation
Primary metric: SQuAD-style token-level F1, averaged over all test examples (higher is better).
- Normalization prior to scoring:
  - Lowercasing
  - Remove punctuation
  - Remove English articles: a, an, the
  - Normalize/condense whitespace
- Per-example F1 is the harmonic mean of precision and recall over normalized token sets. Empty-vs-empty yields 1.0; otherwise, empty vs non-empty yields 0.0.
- Exact Match (EM) at the same normalization is reported for analysis but not used for ranking.

Submission format
- CSV with headers: id,response
- Each id from test.csv must appear exactly once; no extra/missing ids; responses must be finite strings (no NaN/Inf).

Modeling tips
- Start simple: lexical retrieval (TF-IDF/BM25) + span reader.
- Strong baselines: encoder-based readers (e.g., BERT/RoBERTa), or encoder–decoder generators with constrained decoding.
- Pay attention to normalization and short, factual outputs; paraphrases that preserve meaning are rewarded by F1 even if surface forms differ.

Files you will use
- train.csv — training set with gold responses
- test.csv — test set without responses
- sample_submission.csv — correct format to submit predictions

This challenge is precise (objective metric), meaningful (evidence-grounded), and challenging (long/varied contexts and semi-abstractive answers), yet solvable with standard ML/NLP techniques.
