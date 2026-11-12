# OpenMLE-fast task

Task ID: `social-media-popularity-2009-2023@1`

Native metric: `SocialMediaShareJSDMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4093 bytes)
- `data/sample_submission.csv` (10933 bytes); columns: ["Date", "Platform", "Share"]
- `data/test.csv` (5194 bytes); columns: ["Date", "Platform"]
- `data/train.csv` (107709 bytes); columns: ["Date", "Platform", "Share"]

## Public description

Competition: Global Social Media Share Forecasting (2009–2024)

Problem statement
- You are given a multivariate monthly time series of worldwide market-share percentages for social media platforms. Each month is a probability distribution over platforms that sums to 100%.
- Task: Forecast the full platform-by-platform market-share distribution for each month in a held-out future window.
- Predict the percentage share for each platform for every month in the test set. Predictions must be non-negative and, after per-month renormalization, form valid distributions.

Files provided
- train.csv: Long-format labeled data with columns [Date, Platform, Share]. Contains monthly market-share percentages from April 2009 through December 2022.
- test.csv: Long-format unlabeled data with columns [Date, Platform]. Contains the same platforms as train.csv for each month from January 2023 through February 2024.
- sample_submission.csv: Example submission with columns [Date, Platform, Share]. It contains valid random distributions for every test month; you should overwrite Share with your predictions.

Data dictionary
- Date: Month identifier in YYYY-MM.
- Platform: The name of a social network bucket (e.g., Facebook, Twitter, Instagram, LinkedIn, Google+, Digg, MySpace, Pinterest, YouTube, StumbleUpon, Tumblr, reddit, VKontakte, news.ycombinator.com, etc., plus Other). The set of platforms is fixed by test.csv and identical in train and test.
- Share: Percentage share (0–100), not necessarily summing to 100 across rows until per-month renormalization in evaluation. Your submission should provide percentage values; the evaluator converts to probabilities per month.

Target and features
- Target: Share (percentage) for each (Date, Platform) in the test set.
- Features: You may engineer any features from the historical data (e.g., trends, seasonality, cross-platform interactions, compositional transforms like CLR/ILR). External data is allowed if publicly available and properly cited, but is not required to perform well.

Evaluation
- Metric: Jensen–Shannon divergence (JSD) between the predicted and true distributions for each test month, averaged across months. Lower is better.
- Computation details:
  - For each test month, let P (prediction) and Q (ground truth) be vectors over the ordered list of platforms found in test.csv.
  - Values are clipped to [0, +inf) and renormalized per month so they sum to 1. A small epsilon (1e-12) is added before normalization to avoid numerical issues.
  - JSD(P, Q) = 0.5 * KL(P || M) + 0.5 * KL(Q || M), where M = 0.5*(P + Q), using log base 2.
  - Final score is the mean JSD across all test months. The metric is symmetric, bounded in [0, 1], and robust to zeros via epsilon smoothing.

Submission format
- CSV with columns [Date, Platform, Share]. The set of (Date, Platform) pairs must match test.csv exactly (order does not matter; duplicates are not allowed). Extra or missing pairs will invalidate the submission.
- Share should be your predicted percentage for that platform in that month. Any negative or non-finite values are treated as 0; the evaluator renormalizes each month to sum to 100% (then to 1.0 probability) before scoring.

Modeling guidance
- The data are compositional: increases in one platform imply decreases elsewhere. Respect the closure constraint by modeling in a transformed space (e.g., CLR/ILR), with softmax/renormalization layers, or by forecasting relative changes and renormalizing.
- Expect structural change (platform births/declines), gradual trends, and possible seasonality. Many legacy platforms are near zero for long periods; handle zero inflation carefully.
- Baselines: last-observation-carried-forward with per-month renormalization; seasonal naive (last year’s same month); ARIMA/ETS/state-space on ILR/CLR components; RNN/Transformer with compositional output.

Deliverables
- Build a model that outputs Share predictions for all (Date, Platform) pairs in test.csv.
- Submit a CSV named arbitrarily (e.g., my_submission.csv) following the required columns and coverage.
