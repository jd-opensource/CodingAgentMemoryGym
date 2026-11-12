# OpenMLE-fast task

Task ID: `airfare-ml-predicting-flight-fares@2`

Native metric: `FlightFareRankingMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2855 bytes)
- `data/sample_submission.csv` (2370399 bytes); columns: ["row_id", "score"]
- `data/test.csv` (12549540 bytes); columns: ["Date_of_journey", "Journey_day", "Airline", "Flight_code", "Class", "Source", "Departure", "Total_stops", "Arrival", "Destination", "Duration_in_hours", "Days_left", "group_id", "row_id"]
- `data/train.csv` (52259837 bytes); columns: ["Date_of_journey", "Journey_day", "Airline", "Flight_code", "Class", "Source", "Departure", "Total_stops", "Arrival", "Destination", "Duration_in_hours", "Days_left", "Fare", "group_id", "row_id"]

## Public description

Title
Route–Date Flight Option Ranking (Learning-to-Rank)

Problem statement
You are given all available flight options for many route–date queries within India (e.g., Delhi→Mumbai on 2023‑01‑16). Your task is to rank the options within each query so that cheaper options appear higher. Submit a single relevance score per test row; higher scores should indicate a better (cheaper) option. The leaderboard evaluates the quality of your within‑group rankings.

Data description
Each row is a candidate flight option observed for a specific Source–Destination and Date_of_journey. The training set provides the label Fare (INR); the test set withholds it. All rows belong to a route–date group and are evaluated only within their group.

Columns
- row_id: Unique identifier for each row.
- group_id: Identifier of the route–date query. Rankings are computed within each group only.
- Date_of_journey, Journey_day
- Airline, Flight_code, Class
- Source, Destination
- Departure, Arrival (time buckets)
- Total_stops
- Duration_in_hours
- Days_left (lead time in days)
- Fare (label; present only in train.csv)

Provided files
- train.csv: Features + group_id/row_id + Fare.
- test.csv: Same columns as train.csv except Fare is absent.
- sample_submission.csv: Template with columns row_id,score.

Submission format
- A CSV file with exactly two columns and a header: row_id,score
- Include each row_id from test.csv exactly once.
- score is any real number; higher means “rank higher” within its group.

Evaluation metric
- Metric: NDCG@20 averaged over groups.
  - For each test group, compute gains = 1 / log1p(Fare). Lower fares yield larger gains while smoothly damping extremes.
  - Sort by your predicted score in descending order, take the top 20 (or fewer if the group has <20 items), and compute DCG with logarithmic position discount. Normalize by the ideal DCG for that group (sorted by true gains), then average NDCG across all groups (unweighted).
  - The metric lies in [0, 1]; perfect within‑group ordering scores 1.0.

Data split policy
- Entire route–date groups are assigned to either train or test. For each (Source, Destination) route, earlier journey dates are kept for training and later dates are assigned to test. Every test route also appears in training.

Modeling notes
- This is a tabular learning‑to‑rank problem. Strong baselines include gradient‑boosted tree rankers (LambdaMART/LightGBM/CatBoost). A competitive approach is to learn a fare regressor and use negative predicted fare as the score.
- You may engineer features from the provided columns (e.g., categorical encoders, interactions, log transforms, within‑group statistics that do not use test labels). External data is allowed if it is publicly available to all participants and does not use private information about test labels.
