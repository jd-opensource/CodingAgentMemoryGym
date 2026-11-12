# OpenMLE-fast task

Task ID: `worlds-best-universities-qs-rankings-2025@1`

Native metric: `QS2025RankPredictionMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2059 bytes)
- `data/sample_submission.csv` (5122 bytes); columns: ["Id", "PredictedRank"]
- `data/test.csv` (13435 bytes); columns: ["Id", "2024 Rank", "Location", "Location Full", "Size", "Academic Reputation", "Employer Reputation", "Faculty Student", "Citations per Faculty", "International Faculty", "International Students", "International Research Network", "Employment Outcomes", "Sustainability"]
- `data/train.csv` (32864 bytes); columns: ["Id", "2024 Rank", "Location", "Location Full", "Size", "Academic Reputation", "Employer Reputation", "Faculty Student", "Citations per Faculty", "International Faculty", "International Students", "International Research Network", "Employment Outcomes", "Sustainability", "Rank2025"]

## Public description

Title: QS 2025 Rank Prediction (Top 600)

Problem statement:
Predict the official 2025 numeric rank for globally ranked universities using their performance indicators and metadata.
Your goal is to learn the complex mapping from indicators (reputation, internationalization, research impact, employability, sustainability, etc.) and context (country, size, prior rank) to the final 2025 integer rank.

Data description:
- Train file: train.csv
  - Columns:
    - Id: anonymized unique identifier for each university
    - Rank2025: integer target label (1–600)
    - 2024 Rank: prior year rank (integer if available, otherwise a numeric approximation for ranges or -1 if unavailable)
    - Location: country/region code (categorical)
    - Location Full: country/region name (categorical)
    - Size: size category (S/M/L/XL, categorical)
    - Academic Reputation: 0–100
    - Employer Reputation: 0–100
    - Faculty Student: 0–100
    - Citations per Faculty: 0–100
    - International Faculty: 0–100
    - International Students: 0–100
    - International Research Network: 0–100
    - Employment Outcomes: 0–100
    - Sustainability: 0–100

- Test file: test.csv
  - Same columns as train.csv except Rank2025 is not included. Contains Id plus all feature columns required for prediction.

- Sample submission: sample_submission.csv
  - A CSV with columns: Id, PredictedRank
  - Id must match the Ids in test.csv exactly and appear exactly once.
  - PredictedRank can be any real-valued score; it will be converted to ranks internally for evaluation. Integer predictions are acceptable but not required.

Evaluation metric:
- Primary metric: Spearman rank correlation (rho) between PredictedRank and the true Rank2025 over the test set.
- Spearman’s rho measures how well the ordering induced by your predictions matches the official 2025 ordering. Ties are handled by assigning average ranks.
- Higher is better; the score ranges from -1 to 1.

Final files provided:
- train.csv
- test.csv
- sample_submission.csv
- description.txt
