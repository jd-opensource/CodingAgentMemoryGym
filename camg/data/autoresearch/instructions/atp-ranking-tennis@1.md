# OpenMLE-fast task

Task ID: `atp-ranking-tennis@1`

Native metric: `ATPTennisRankingMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2710 bytes)
- `data/sample_submission.csv` (4701 bytes); columns: ["player_id", "strength"]
- `data/test.csv` (4053 bytes); columns: ["player_id", "Country", "Tournaments_Played", "Best_Rank"]
- `data/train.csv` (10673 bytes); columns: ["player_id", "Country", "Tournaments_Played", "Best_Rank", "Rank"]

## Public description

ATP Rank-Ordering from Limited Metadata

Overview
You are given a single snapshot of ATP top-ranked tennis players with minimal metadata. Your task is to predict a real-valued “strength” score for each player in the test set such that sorting by this score (higher is better) reproduces the true ranking order as closely as possible. This is a learning-to-rank problem evaluated with Spearman’s rank correlation.

Files provided
- train.csv: Training table with features and the target Rank.
- test.csv: Test table with the same features, without Rank.
- sample_submission.csv: Example submission with random but valid strength values.

Columns
- player_id: Stable anonymized identifier for each player.
- Country: Player’s country (categorical string).
- Tournaments_Played: Number of tournaments counted (numeric).
- Best_Rank: Player’s historic best ATP rank (numeric).
- Rank: Target column present only in train.csv; lower is better (1 is best).

Important constraints (anti-leakage)
- The near-deterministic Points field and the Name identity are intentionally excluded from the provided files. Do not attempt to reconstruct or infer them.

Submission format
- CSV with exactly two columns in this order:
  - player_id
  - strength (a real-valued score; higher = better expected ranking)
- Include one row per player_id in test.csv, no duplicates, any row order.
- All values must be finite (no NaN/Inf).

Evaluation metric
- We compute Spearman’s rank correlation (rho) between your submitted strength and the negative of the true Rank on the test set.
  - Ties in your strength are allowed; they are handled via average ranks.
  - The score ranges from −1 (perfectly reversed order) to +1 (perfect order). Higher is better.

Train/test split
- A single deterministic 70/30 split stratified by rank bands (1–50, 51–100, …, 451–500) is used to preserve difficulty across the spectrum. Use train.csv for model development; submit predictions for all player_id in test.csv.

Modeling tips
- Encode Country (one-hot or target encoding). Cast numeric types and handle potential skew.
- Useful interactions include Best_Rank × Tournaments_Played or non-linear transforms of Best_Rank.
- Consider linear models with regularization, gradient-boosted trees, or learning-to-rank objectives. Calibrating to the Rank target (e.g., predicting −Rank or log-transforms) can help, but final scoring uses only the order induced by strength.

Notes
- The full dataset scale is preserved; no subsampling is necessary.
- This competition emphasizes feature engineering and learning-to-rank. While signals are limited, careful preprocessing and modeling can extract meaningful ordering information.
