# OpenMLE-fast task

Task ID: `stocknews@1`

Native metric: `NewsDJIADirectionMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2861 bytes)
- `data/sample_submission.csv` (7965 bytes); columns: ["Date", "PredictedProbability"]
- `data/test.csv` (1077676 bytes); columns: ["Date", "Top1", "Top2", "Top3", "Top4", "Top5", "Top6", "Top7", "Top8", "Top9", "Top10", "Top11", "Top12", "Top13", "Top14", "Top15", "Top16", "Top17", "Top18", "Top19", "Top20", "Top21", "Top22", "Top23", "Top24", "Top25"]
- `data/train.csv` (4539352 bytes); columns: ["Date", "Label", "Top1", "Top2", "Top3", "Top4", "Top5", "Top6", "Top7", "Top8", "Top9", "Top10", "Top11", "Top12", "Top13", "Top14", "Top15", "Top16", "Top17", "Top18", "Top19", "Top20", "Top21", "Top22", "Top23", "Top24", "Top25"]

## Public description

Competition: News-Driven DJIA Direction Prediction

Problem Statement
Predict whether the Dow Jones Industrial Average (DJIA) adjusted close for the next trading day will rise/stay the same (label 1) or decrease (label 0), using only the text of the current day’s top-25 Reddit r/worldnews headlines. Participants must output calibrated probabilities for the DJIA rising/staying the same on the next trading day.

Data Description
- train.csv: Daily samples for the training period, containing Date, Label, and Top1–Top25 headlines for that date. Each row corresponds to one trading day; the label indicates the next trading day’s DJIA adjusted close direction vs the previous trading day.
- test.csv: Daily samples for the test period, containing Date and Top1–Top25 headlines. Labels are withheld.
- sample_submission.csv: Example submission with Date and PredictedProbability columns.

Temporal Split
- Train: 2008-08-08 to 2014-12-31 (inclusive)
- Test: 2015-01-02 to 2016-07-01 (inclusive)
This split respects causality and mirrors a realistic forward-looking evaluation. All dates are trading days.

Modeling Guidance
- Use the full text from Top1–Top25 headlines. Preserve their ordering (Top1 is most upvoted) to exploit ranking information.
- Robust text processing is essential: handle encoding artifacts (e.g., leading b'...', doubled quotes, HTML entities), normalize Unicode, and remove malformed/empty strings.
- Consider feature engineering beyond raw text, constrained to information available at prediction time: sentiment and subject/topic scores, entity extraction, geopolitical focus, burstiness signals, and rolling aggregates computed strictly from prior headlines.
- Do not use price-derived features at inference time. The official test data provides only headlines.

Submission Format
Submit a CSV with two columns and no extra header/columns:
- Date: YYYY-MM-DD, exactly matching and in the same order as in test.csv
- PredictedProbability: a numeric probability in [0,1] that Label==1

Evaluation Metric
- Primary metric: ROC AUC computed on the test set using the submitted probabilities and the hidden labels.
Why AUC: It is threshold-free, resilient to mild class imbalance, and measures ranking quality of probabilistic outputs under noisy text-to-market relationships.

Rules and Integrity
- Use only information available up to and including the headline date when generating predictions for the next trading day.
- No external leakage of labels (e.g., prices) is allowed in test-time features.
- Keep deterministic pipelines for reproducibility.

Files Provided
- train.csv
- test.csv
- sample_submission.csv

Notes
- The task is challenging: it spans multiple economic regimes with noisy, indirect signals. Effective solutions typically combine strong NLP modeling with time-aware feature design and regularization.
