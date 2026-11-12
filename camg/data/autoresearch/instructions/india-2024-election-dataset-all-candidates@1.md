# OpenMLE-fast task

Task ID: `india-2024-election-dataset-all-candidates@1`

Native metric: `IndiaElectionVoteShareMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4023 bytes)
- `data/sample_submission.csv` (31794 bytes); columns: ["id", "vote_share"]
- `data/test.csv` (237878 bytes); columns: ["id", "candidate", "party", "state", "constituency", "constituency_raw", "reservation", "phase_electors", "phase_poll_pct", "phase_votes_polled", "evm_votes_counted", "postal_votes_counted", "evm_votes_polled", "n_candidates_pc"]
- `data/train.csv` (962396 bytes); columns: ["candidate", "party", "state", "constituency", "vote_share", "constituency_raw", "reservation", "phase_electors", "phase_poll_pct", "phase_votes_polled", "evm_votes_counted", "postal_votes_counted", "evm_votes_polled", "n_candidates_pc"]

## Public description

Competition: Candidate Vote-Share Prediction and Ranking for India’s 2024 Lok Sabha PCs

Background
India’s 2024 Lok Sabha election produced rich, candidate-level results across all 543 Parliamentary Constituencies (PCs). Each PC has multiple candidates from national/regional parties and independents, with strong state-wise heterogeneity and varying turnout. This competition tasks you with predicting each candidate’s final vote share given only non-leaking, pre-result descriptors of the candidate and constituency, plus PC-level turnout context.

Problem Statement
Given candidate- and constituency-level descriptors that are known prior to the release of results, predict the percentage of votes (% of Votes) obtained by every candidate in the held election. Accurate share prediction naturally yields better intra-constituency ranking quality, but the target to optimize is the candidate-level vote share.

Provided Files
- train.csv: Training rows with non-leaking features and the target column vote_share.
- test.csv: Test rows with the same non-leaking features but without vote_share.
- sample_submission.csv: Example submission with the expected format.

Target
- vote_share: Percentage of votes for a candidate (float in [0, 100]).

Features (non-exhaustive; you may engineer more in your pipeline)
- candidate: Candidate name (string)
- party: Party name (string)
- state: State/UT name (string)
- constituency: Cleaned PC name, normalized across sources (string)
- reservation: Reservation tag parsed from the constituency, e.g., General/SC/ST (string)
- n_candidates_pc: Number of candidates contesting in the PC (integer)
- phase_electors: Elector count for the PC (float)
- phase_poll_pct: Polling percentage for the PC (float)
- phase_votes_polled: Votes polled for the PC (float)
- evm_votes_counted: EVM votes counted (PC-level context) (float)
- postal_votes_counted: Postal votes counted (PC-level context) (float)
- evm_votes_polled: EVM votes polled (PC-level context) (float)

Notes
- All features are pre-result context or roster information and are safe to use. Candidate-level vote counts and any columns derived directly from the final results (e.g., margin, rank, S.N) are not provided as features.
- You are encouraged to perform feature engineering such as categorical encodings, constituency-level aggregates, and party presence indicators.

Evaluation
Submissions are evaluated using Weighted Mean Absolute Error (WMAE) on vote_share, computed per candidate i in the test set as:
- weight w_i = 0.2 + 0.8*(y_true_i / 100)
- WMAE = sum_i w_i * |y_true_i − y_pred_i| / sum_i w_i
This emphasizes accuracy for higher-share candidates (winners/runner-ups) while still scoring minor candidates, encouraging robust forecasting across the distribution.

Submission Format
- CSV with two columns and a header:
  - id: Identifier for each test row (integer)
  - vote_share: Your predicted percentage of votes (float)
- The id must match the id values in test.csv. The order does not matter, but all rows must be present exactly once.

Train/Test Split
- The split is done by constituency (group split) so that no constituency appears in both train and test.
- Stratification by state helps maintain similar state distributions across splits.
- All test-side categorical values for key fields (e.g., party, state) occur at least once in training.

Practical Tips
- Treat vote_share as regression. Typical approaches include gradient-boosted trees, linear models with encodings, and neural models with embeddings for categorical variables.
- Ensure careful preprocessing of categorical values (case, punctuation, diacritics) and consider constituency-level aggregates (e.g., number of major parties present).
- Many PCs have numerous low-share candidates; robust models should avoid trivial near-zero predictions and model turnout/context appropriately.

Files to Use
- Use train.csv to train models and test.csv for generating predictions. Submit predictions in the format described above.
