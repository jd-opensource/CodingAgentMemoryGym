# OpenMLE-fast task

Task ID: `fake-news@1`

Native metric: `FakeNewsMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1664 bytes)
- `data/sample_submission.csv` (120502 bytes); columns: ["id", "real_probability"]
- `data/test.csv` (914653 bytes); columns: ["id", "title", "news_url", "source_domain", "tweet_num"]
- `data/train.csv` (3295633 bytes); columns: ["id", "title", "news_url", "source_domain", "tweet_num", "label"]

## Public description

Headline Reliability Prediction under Domain Shift

Problem statement
Given a news item’s headline (title), its URL/domain, and a social propagation signal (tweet_num), predict the probability that the item is real (from reliable outlets) versus fake (from unreliable outlets). The evaluation emphasizes generalization to unseen publishers by holding out entire source domains from training.

Data description
You will receive three files (all under public/):
- train.csv: id, title, news_url, source_domain, tweet_num, label
- test.csv: id, title, news_url, source_domain, tweet_num
- sample_submission.csv: id, real_probability

Notes
- label is binary: 1 means real, 0 means fake.
- Domains in test.csv are disjoint from train.csv at the registrable-domain level (e.g., example.co.uk). This prevents trivial memorization of outlet names and stresses content-driven modeling.
- Some rows may have missing source_domain; these are recovered from news_url when possible and normalized to the registrable form.
- Ids are unique integers per row; no ordering is implied. The split is deterministic and ensures both classes are present in both train and test while keeping domains disjoint.

Evaluation
- Metric: class-balanced log loss (weighted cross-entropy). Submit probabilities for the “real” class in [0,1] under the column real_probability.
- Class balancing: each class contributes equally (0.5 each) to the final score, implemented by weighting per-class losses by 0.5 / N_class measured on the test set.
- Submission format: a CSV with columns id, real_probability containing exactly the ids from test.csv once each. Values must be numeric in [0,1].
