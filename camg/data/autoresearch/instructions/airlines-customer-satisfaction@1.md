# OpenMLE-fast task

Task ID: `airlines-customer-satisfaction@1`

Native metric: `AirlineSatisfactionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2063 bytes)
- `data/sample_submission.csv` (1182964 bytes); columns: ["id", "dissatisfied", "satisfied"]
- `data/test.csv` (2435499 bytes); columns: ["id", "Gender", "Customer Type", "Age", "Type of Travel", "Class", "Flight Distance", "Seat comfort", "Departure/Arrival time convenient", "Food and drink", "Gate location", "Inflight wifi service", "Inflight entertainment", "Online support", "Ease of Online booking", "On-board service", "Leg room service", "Baggage handling", "Checkin service", "Cleanliness", "Online boarding", "Departure Delay in Minutes", "Arrival Delay in Minutes"]
- `data/train.csv` (10809547 bytes); columns: ["id", "Gender", "Customer Type", "Age", "Type of Travel", "Class", "Flight Distance", "Seat comfort", "Departure/Arrival time convenient", "Food and drink", "Gate location", "Inflight wifi service", "Inflight entertainment", "Online support", "Ease of Online booking", "On-board service", "Leg room service", "Baggage handling", "Checkin service", "Cleanliness", "Online boarding", "Departure Delay in Minutes", "Arrival Delay in Minutes", "satisfaction"]

## Public description

Invistico Airline Satisfaction Prediction

Problem statement:
Predict the probability that a passenger is satisfied with Invistico Airlines given flight context (e.g., travel type, class, distance, delays) and post-flight service ratings.

Data description:
- Training file: train.csv. Each row represents one passenger trip and includes all features plus the target column.
- Test file: test.csv. Same features as train.csv but without the target column.
- ID: A unique integer id is provided for every row in both train and test to enable submission alignment.
- Target: satisfaction (binary class: satisfied or dissatisfied).
- Features: A mix of categorical, ordinal, and numeric attributes, including demographics, travel context, flight distance, departure/arrival delays, and multiple 0–5 service ratings (e.g., seat comfort, online boarding, cleanliness). Missing values may be present in the arrival delay feature.

Evaluation metric:
- Primary metric: Log Loss (binary cross-entropy).
- Submission format: A CSV with columns [id, dissatisfied, satisfied], containing class probability predictions for each test row. For every row, probabilities must be real numbers in [0, 1] and sum to 1 across the two class columns. The id values must exactly match those in test.csv.

Files provided:
- train.csv: Features + satisfaction label.
- test.csv: Features only (no label).
- sample_submission.csv: Example submission with random probabilities for the two classes that sum to 1 per row.

Notes:
- Participants may use any ML techniques for data processing, feature engineering, model training, and evaluation. Treat 0–5 service ratings as ordered numerical features; consider robust handling of heavy-tailed delays and potential missing values. Categorical features can be encoded appropriately (e.g., one-hot, target encoding, or native categorical handling).
- Use the provided single split for official evaluation and manage your own validation strategy locally.
- Ensure submissions are well-calibrated probabilities to perform well under Log Loss.
