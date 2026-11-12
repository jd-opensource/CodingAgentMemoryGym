# OpenMLE-fast task

Task ID: `top-cryptocurrencies-by-volume@1`

Native metric: `CryptoReturnRankingMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3574 bytes)
- `data/sample_submission.csv` (50159 bytes); columns: ["id", "score"]
- `data/test.csv` (99121 bytes); columns: ["id", "date", "asset", "close", "volume"]
- `data/train.csv` (8770988 bytes); columns: ["id", "date", "asset", "close", "volume", "target"]

## Public description

Competition: Cross-Sectional Crypto Return Ranking

Problem statement
Given daily closing prices and trading volumes for a broad universe of cryptocurrencies, predict which assets will outperform the others the next trading day. For each date t in the test set, you must submit a per-asset score that ranks assets by their next-day log return r_{t+1} = ln(close_{t+1} / close_t). You are evaluated on how well your cross-sectional scores align with realized next-day returns.

What you are given
- A long-format panel of crypto assets with daily close and volume.
- Train labels are next-day log returns computed from observed closes. Test labels are hidden.
- The per-day asset universe varies over time.

Files provided
- train.csv: Columns [id, date, asset, close, volume, target]. The target is the next-day log return for (date, asset).
- test.csv: Columns [id, date, asset, close, volume]. Your task is to predict a score for each row (higher score = higher expected next-day return).
- sample_submission.csv: Columns [id, score]. An example submission with random scores.

Target definition
For each (date = t, asset = a), the target is r_{t+1}(a) = ln(close_{t+1}(a) / close_t(a)). Targets are only defined when both close_t and close_{t+1} exist for the asset. The released train.csv contains only rows with valid targets. The test set contains rows where targets exist but are withheld.

Important characteristics and constraints
- Universe turnover: The set of assets present each day changes due to listings/delistings and data availability. You should design features that are robust to sparse histories.
- Information usage: Use only information available up to and including date t to predict r_{t+1}. Do not leak future information (e.g., do not use data from dates > t for a given row’s prediction).
- Assets included: Stable/pegged assets and wrapped duplicates have been excluded to avoid degenerate targets and leakage. The remaining assets are diverse and include both large-cap and lower-liquidity coins.

Train/test split
- Train period: Start of data through 2024-12-31 (inclusive).
- Test period: 2025-01-01 through the latest available date. Only rows with valid next-day returns are included.

Evaluation metric
- Primary metric: Average daily Spearman rank correlation (Information Coefficient, IC).
  - For each test date, compute the Spearman rank correlation between your submitted scores and the realized next-day log returns across all assets listed that date.
  - The final score is the simple average of these daily correlations.

Why this metric?
- It is scale-invariant and robust to heavy tails, focusing the evaluation on cross-sectional ranking quality rather than calibration.
- Averaging per-date correlations prevents overweighting dates with more assets and mitigates the impact of universe turnover.

Submission format
- A CSV with columns [id, score]. IDs match those in test.csv and uniquely identify each (date, asset) pair. Scores may be any real numbers; higher = higher expected next-day return.

Starter ideas (not required)
- Momentum features: recent returns over multiple horizons, breakout indicators.
- Volatility and turnover: rolling standard deviation of returns, volume spikes (e.g., volume/rolling volume), dollar volume.
- Seasonality and regime features: weekday effects, rolling drawdowns, trend filters.
- Cross-sectional normalization: z-scores within each date to stabilize inputs to models.

Good luck, and have fun building robust, leakage-free ranking models for a challenging, evolving crypto market!
