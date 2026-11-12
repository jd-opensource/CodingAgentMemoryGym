# OpenMLE-fast task

Task ID: `databricks-dolly-15k@1`

Native metric: `DollyClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1797 bytes)
- `data/sample_submission.csv` (61122 bytes); columns: ["id", "category"]
- `data/test.csv` (237794 bytes); columns: ["id", "instruction"]
- `data/train.csv` (1113787 bytes); columns: ["id", "instruction", "category"]

## Public description

Instruction Category Classification Challenge

Problem statement
Given only an instruction text, predict which task category it belongs to among eight instruction-following behaviors. The goal is to build a robust multiclass text classifier that distinguishes subtle differences between instruction styles (e.g., closed_qa vs open_qa vs general_qa; summarization vs information_extraction).

Why this is challenging
- Categories are overlapping and pragmatically subtle.
- Instructions vary from short prompts to long, constraint-heavy requests.
- Class imbalance exists; strong models must perform well across all classes.

Data description
- train.csv: Labeled training set with columns:
  - id: Unique identifier for the instance
  - instruction: The instruction text
  - category: One of the eight categories
- test.csv: Unlabeled test set with columns:
  - id: Unique identifier for the instance
  - instruction: The instruction text
- sample_submission.csv: Example submission file with columns:
  - id
  - category

Target labels
The eight categories are:
- brainstorming
- classification
- closed_qa
- creative_writing
- general_qa
- information_extraction
- open_qa
- summarization

Evaluation
- Metric: Macro-averaged F1 across the eight classes.
  - Rationale: Fair to minority classes and precise for multiclass imbalanced settings.
  - Computation: F1 is computed per class and averaged uniformly. Your submission must contain exactly the columns id and category. The evaluation matches by id.

Submission format
- A single CSV file with header and exactly two columns: id, category
- One row per id in the test set. Do not include extra columns.

Files provided
- train.csv
- test.csv
- sample_submission.csv

Good luck and have fun building a high-performing instruction classifier!
