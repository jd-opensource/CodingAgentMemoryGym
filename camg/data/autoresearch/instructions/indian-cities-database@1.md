# OpenMLE-fast task

Task ID: `indian-cities-database@1`

Native metric: `SameStatePairMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2477 bytes)
- `data/sample_submission.csv` (47817 bytes); columns: ["id", "prob_same_state"]
- `data/test.csv` (373873 bytes); columns: ["id", "lat1", "lon1", "lat2", "lon2", "lat_diff", "lon_diff", "abs_lat_diff", "abs_lon_diff", "haversine_km", "bearing_deg", "midpoint_lat", "midpoint_lon"]
- `data/train.csv` (2076054 bytes); columns: ["id", "lat1", "lon1", "lat2", "lon2", "lat_diff", "lon_diff", "abs_lat_diff", "abs_lon_diff", "haversine_km", "bearing_deg", "midpoint_lat", "midpoint_lon", "target"]

## Public description

Competition: Same-State City Pair Classification (India)

Background
India’s administrative states have irregular shapes and complex boundaries. Inferring whether two cities belong to the same state from their geospatial coordinates alone is valuable for logistics, planning, and regional analysis. This competition challenges you to learn spatial patterns that determine state co-membership.

Problem Statement
Given two cities’ latitude and longitude, predict the probability that they belong to the same Indian state. You should leverage geospatial feature engineering and robust ML models to distinguish intra-state from inter-state pairs.

Dataset and Files
The dataset consists of prominent Indian cities with their latitude and longitude. We construct pairwise samples from cities, using only spatial information. Final competition files:
- train.csv: Training pairs with engineered features and the target label.
- test.csv: Test pairs with the same features, without labels.
- sample_submission.csv: Example submission showing required format.

Features and Target
Each row corresponds to an unordered pair of distinct cities. Features include raw coordinates and derived geospatial features. The target is binary:
- target = 1 if both cities are in the same state
- target = 0 otherwise

Evaluation Metric
The official leaderboard metric is Average Precision (area under the precision–recall curve) computed on the positive class (same-state). This is robust to the natural class imbalance and rewards models that rank true positives highly.

Submission Format
Submit a CSV with the following columns:
- id: Row identifier matching test.csv
- prob_same_state: Your predicted probability that the pair belongs to the same state (a number in [0, 1])

Data Split and Leakage Prevention
Cities are split into disjoint train and test sets deterministically, and pairs are constructed only within each set. This prevents models from memorizing identity via overlapping pairs and enforces generalization to unseen cities. No city or state identifiers appear in the features.

Notes
- You may engineer additional geospatial features (e.g., great-circle distance, bearings, midpoints) and use any ML approach suitable for tabular, imbalanced classification.
- Ensure numerical stability and avoid producing NaN/Inf values in submissions.
- Class imbalance is significant; consider appropriate modeling techniques (class weighting, focal loss, calibrated probabilities).
