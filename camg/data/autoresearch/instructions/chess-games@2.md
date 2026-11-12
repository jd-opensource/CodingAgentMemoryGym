# OpenMLE-fast task

Task ID: `chess-games@2`

Native metric: `ChessTimeForfeitMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3110 bytes)
- `data/sample_submission.csv` (28326 bytes); columns: ["game_id", "time_forfeit_probability"]
- `data/test.csv` (125584 bytes); columns: ["game_id", "event_bucket", "UTCDate", "UTCTime", "WhiteElo", "BlackElo", "TimeControl", "base_seconds", "increment_seconds", "tc_bucket", "moves_trunc"]
- `data/train.csv` (509433 bytes); columns: ["game_id", "event_bucket", "UTCDate", "UTCTime", "WhiteElo", "BlackElo", "TimeControl", "base_seconds", "increment_seconds", "tc_bucket", "moves_trunc", "time_forfeit"]

## Public description

Title: Predicting Time-Forfeit Risk from Early Chess Moves

Problem statement
Given online chess games with pre-game metadata and only the earliest portion of the move sequence, predict the probability that a game will end by time forfeit (either side) versus other terminations. Your task is to output well-calibrated probabilities for time-forfeit.

Data description
You are provided with a train/test split derived from a large corpus of Lichess games. The train set contains features plus the target label; the test set contains the same features without the label.

Features provided per game
- game_id: Unique identifier of the game.
- event_bucket: Coarse event type parsed from the original event field (e.g., blitz, blitz_tournament, classical, correspondence, etc.).
- UTCDate: UTC date string of when the game started.
- UTCTime: UTC time string of when the game started.
- WhiteElo, BlackElo: Pre-game ratings of the players.
- TimeControl: Original time control string in the form base+increment or '-' for correspondence.
- base_seconds, increment_seconds: Parsed base and increment in seconds from TimeControl ('-' yields 0 and 0, respectively).
- tc_bucket: Time-control bucket derived from base and increment (ultrabullet, bullet, blitz, rapid, classical, correspondence).
- moves_trunc: The first N=16 plies (half-moves) of the game in normalized SAN-like tokens, with move numbers and trailing results removed and checks/mates symbols stripped.

Target label in train
- time_forfeit: Binary indicator (1 if the game terminated by time forfeit, 0 otherwise).

Files
- train.csv: Training data with all features and the time_forfeit label.
- test.csv: Test data with the same features but without the label.
- sample_submission.csv: A valid example submission with random probabilities.

Submission format
- A CSV with the following columns:
  - game_id
  - time_forfeit_probability (float in [0, 1])
- Each game_id from test.csv must appear exactly once.

Evaluation metric
- Binary log loss (cross-entropy) between your predicted probability and the true time_forfeit label, averaged over the test set. Predictions are clipped to [1e-15, 1 - 1e-15] before scoring to avoid numerical issues. Lower is better.

Notes and guidelines
- The test set omits any post-game or leakage-prone fields. The label depends strictly on a recorded termination type. The moves_trunc field only includes the earliest plies to avoid late-game leakage.
- You may engineer additional features from the provided columns (e.g., Elo gap, weekday/time-of-day, text features over moves_trunc, or parsed opening patterns) and try a range of models (linear/regularized models with n-grams, boosted trees on mixed tabular/text features, or neural sequence models).
- Class imbalance is expected (time forfeit is typically a minority), so consider class-weighting, calibration, and proper regularization.
- The split is stratified to stabilize class prevalence across time-control regimes. All test labels occur in the training set at least once.

Good luck and have fun blending tabular context with early-move patterns!
