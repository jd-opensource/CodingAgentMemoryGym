# OpenMLE-fast task

Task ID: `nlu-nlg-dataset@1`

Native metric: `CustomerIntentSentimentMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (571 bytes)
- `data/sample_submission.csv` (447486 bytes); columns: ["id", "intent", "sentiment"]
- `data/test.csv` (2508118 bytes); columns: ["id", "instruction", "context"]
- `data/train.csv` (11083135 bytes); columns: ["id", "instruction", "context", "intent", "sentiment"]

## Public description

Customer Query Intent + Sentiment Classification (Multi-Task)

Files provided
- train.csv: id, instruction, context, intent, sentiment
- test.csv: id, instruction, context
- sample_submission.csv: id, intent, sentiment (example format)

Submission format
- A CSV file with columns: id, intent, sentiment
- All ids from test.csv must be present exactly once and in the same order.
- Predicted labels must be valid: intent in {booking, refund, cancellation}; sentiment in {NEGATIVE, POSITIVE}.

Evaluation
- Primary metric: 0.5 * macroF1(intent) + 0.5 * macroF1(sentiment)
