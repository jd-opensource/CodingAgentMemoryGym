# OpenMLE-fast task

Task ID: `4000-indian-cities-names-states-lat-lon@2`

Native metric: `IndianCitiesMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2307 bytes)
- `data/sample_submission.csv` (16693 bytes); columns: ["id", "State"]
- `data/test.csv` (22260 bytes); columns: ["id", "Latitude", "Longitude"]
- `data/train.csv` (126471 bytes); columns: ["id", "Latitude", "Longitude", "State"]

## Public description

Title: Reverse Geocoding India — Predict State/UT from Latitude & Longitude

Problem statement
Participants must build a model that predicts the Indian State/Union Territory (34 classes) given only geographic coordinates (latitude and longitude). This is a reverse geocoding classification task that rewards robust handling of class imbalance and challenging state boundaries.

Files provided
- train.csv: Training data with columns [id, Latitude, Longitude, State].
- test.csv: Test data with columns [id, Latitude, Longitude].
- sample_submission.csv: A sample file with the expected format [id, State].

Target and features
- Target: State (string categorical; 34 unique classes).
- Features: Latitude (float), Longitude (float). No other features are provided to focus the task on spatial learning.

Evaluation
- The leaderboard metric is Macro-averaged F1 score over the ground-truth classes present in test.csv.
  - For each class, F1 = 2 * precision * recall / (precision + recall), with 0 assigned if division is undefined.
  - The macro score is the unweighted mean of per-class F1 values.
- Secondary metric (reported in descriptions/examples only): overall accuracy.

Rules and expectations
- Use only the provided features. External data, maps, or lookup tables that directly encode state boundaries are not allowed.
- Models may use any ML approach, including k-NN, tree ensembles, neural networks, or custom distance-aware methods. Thoughtful preprocessing (e.g., scaling, sin/cos positional encodings) is encouraged.

Suggested approaches
- Baselines: k-NN on raw or standardized coordinates; decision trees; gradient-boosted trees.
- Feature engineering: standardization; trigonometric embeddings of latitude/longitude; clustering features; spatial smoothing.
- Handling imbalance: class-weighted losses; calibration; sampling strategies.

Submission format
- A valid submission is a CSV with columns [id, State].
- The ids must exactly match those in test.csv and appear once each. State predictions must be non-empty strings.

Notes
- The dataset covers 4k+ Indian cities with precise geo-coordinates and state labels. The split is stratified to preserve class coverage.
- Boundary cases between neighboring states are intentionally challenging; careful modeling and validation are key.
