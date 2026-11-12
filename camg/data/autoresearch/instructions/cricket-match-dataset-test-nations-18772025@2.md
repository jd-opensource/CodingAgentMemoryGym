# OpenMLE-fast task

Task ID: `cricket-match-dataset-test-nations-18772025@2`

Native metric: `CricketMatchOutcomeMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3537 bytes)
- `data/sample_submission.csv` (2870 bytes); columns: ["id", "Team1", "Team2", "Draw"]
- `data/test.csv` (2574 bytes); columns: ["id", "team1", "team2", "ground", "match_date"]
- `data/train.csv` (153504 bytes); columns: ["id", "team1", "team2", "ground", "match_date", "label"]

## Public description

Competition: Test Match Outcome Forecasting (Team1 win vs Team2 win vs Draw)

Problem statement
Given the two competing Test cricket teams, venue (ground), and match date, predict calibrated probabilities for the three mutually exclusive outcomes:
- Team1: Team 1 wins
- Team2: Team 2 wins
- Draw: The match is drawn

Participants must submit one row per test match with a valid probability distribution over these three outcomes. The goal is to produce accurate, well-calibrated probabilistic forecasts.

Data description
You are provided with cleaned historical Test match records spanning 1877–2025. Each row represents a single Test match and includes:
- id: Unique opaque identifier for the match (no label leakage)
- team1: Name of Team 1 as listed in the fixture
- team2: Name of Team 2 as listed in the fixture
- ground: Venue string (city/ground)
- match_date: Original date string (potentially a range). You may parse and engineer time/era features.

Target (provided only in train.csv):
- label: One of {Team1, Team2, Draw}

Notes and constraints
- Only Test-format matches are included. Extremely rare tied Tests are excluded to ensure robust evaluation of the three main outcomes.
- Scorecard identifiers and margin information are not provided to avoid target leakage.
- The split is strictly chronological to mimic real-life forecasting and prevent learning from the future. Train data contains earlier matches; test contains later matches.

Files provided
- train.csv
- test.csv
- sample_submission.csv

Submission format
A CSV with the following columns and no header/column changes:
- id
- Team1
- Team2
- Draw

Each row must be a proper probability distribution: finite, non-negative, and summing to 1 (within a small numerical tolerance). The id column must match the ids in test.csv exactly; duplicates are not allowed.

Evaluation metric
Primary metric: Multiclass log loss (natural logarithm) across the three outcomes.
For each test match i with true outcome yi ∈ {Team1, Team2, Draw} and submitted probabilities p_i(Team1), p_i(Team2), p_i(Draw), the score is:
LogLoss = -(1/N) * Σ_i log p_i(yi)
Lower is better. Submissions are validated for format and probabilities; probabilities are clipped to a small epsilon for numerical stability during scoring.

What makes this challenging and meaningful
- Era shifts: Nearly 150 years of Tests introduce strong non-stationarity in styles, over rates, and draw frequencies.
- Context sparsity: Only teams, venue, and date are provided; strong solutions must infer evolving team/venue strengths, calendar effects, and draw propensity.
- Calibration focus: The metric rewards well-calibrated probabilities, not just hard classification.

Modeling tips
- Derive time-based features (year, month, season, coarse era buckets).
- Encode teams and venues (target encoding, learned embeddings, or rating systems like Elo/Glicko with decay).
- Capture home/away/neutral signals from the ground string if helpful; external data is not required.
- Use cross-entropy–optimized models (gradient boosting, logistic regression with interactions, shallow neural nets) and post-hoc calibration (Platt/Isotonic) if needed.

Reproducibility and fairness
- The split is deterministic and chronological. All classes are present in both train and test and every test label appears at least once in training.
- The provided sample_submission.csv is structurally valid with random but normalized probabilities.

Good luck, and have fun building well-calibrated Test cricket forecasters!
