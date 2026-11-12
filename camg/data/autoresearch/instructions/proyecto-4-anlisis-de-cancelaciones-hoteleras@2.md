# OpenMLE-fast task

Task ID: `proyecto-4-anlisis-de-cancelaciones-hoteleras@2`

Native metric: `HotelCancellationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3184 bytes)
- `data/sample_submission.csv` (422125 bytes); columns: ["id", "late_cancel_or_noshow"]
- `data/test.csv` (4128293 bytes); columns: ["id", "hotel", "lead_time", "arrival_date_year", "arrival_date_month", "arrival_date_week_number", "arrival_date_day_of_month", "stays_in_weekend_nights", "stays_in_week_nights", "adults", "children", "babies", "meal", "country", "market_segment", "distribution_channel", "is_repeated_guest", "previous_cancellations", "previous_bookings_not_canceled", "reserved_room_type", "agent", "company", "customer_type", "required_car_parking_spaces", "total_of_special_requests"]
- `data/train.csv` (8286047 bytes); columns: ["id", "hotel", "lead_time", "arrival_date_year", "arrival_date_month", "arrival_date_week_number", "arrival_date_day_of_month", "stays_in_weekend_nights", "stays_in_week_nights", "adults", "children", "babies", "meal", "country", "market_segment", "distribution_channel", "is_repeated_guest", "previous_cancellations", "previous_bookings_not_canceled", "reserved_room_type", "agent", "company", "customer_type", "required_car_parking_spaces", "total_of_special_requests", "late_cancel_or_noshow"]

## Public description

Predict Late Cancellations and No‑Shows (Operational Risk)

Problem statement
Hotels incur significant costs when a reservation is canceled shortly before arrival or the guest does not show up. Your task is to build a model that, at reservation time, predicts the probability that a booking will become a late cancellation (within 3 days of arrival) or a no‑show. Accurate, calibrated probabilities enable better overbooking, waitlist and pricing decisions.

Data description
We provide a tabular dataset of hotel reservations collected between 2015 and 2017. Each row is a booking at reservation time. The dataset has been split by arrival year to emulate real deployment conditions.

Files
- train.csv: Training data with features and the binary target late_cancel_or_noshow.
- test.csv: Test data with the same features but without the target.
- sample_submission.csv: Example submission file with the required format and random probabilities.

Target
- late_cancel_or_noshow: 1 if the booking turned into a late cancellation (canceled with fewer than 3 days before arrival) or a no‑show; 0 otherwise.

Features
Only features available at reservation time are included. They cover guest composition, timing, and channel information:
- id: Unique row identifier.
- hotel, lead_time, arrival_date_year, arrival_date_month, arrival_date_week_number, arrival_date_day_of_month
- stays_in_weekend_nights, stays_in_week_nights, adults, children, babies
- meal, country, market_segment, distribution_channel
- is_repeated_guest, previous_cancellations, previous_bookings_not_canceled
- reserved_room_type, agent, company, customer_type
- required_car_parking_spaces, total_of_special_requests

Important notes
- Some categorical fields have high cardinality (country, agent, company). Robust encoders and careful cross‑validation are recommended.
- The data is imbalanced: late cancellations and no‑shows are rare events. Use techniques suited to imbalanced classification and ensure probability calibration.
- A temporal split is used: train covers arrivals in 2015–2016; test covers arrivals in 2017. Avoid any target leakage across time.

Submission format
Submit a CSV with two columns and one row per test id:
- id: integer identifier from test.csv
- late_cancel_or_noshow: predicted probability in [0, 1]

Evaluation
Submissions are evaluated using Average Precision (area under the precision–recall curve, AP) on the positive class (late_cancel_or_noshow = 1). AP strongly reflects ranking quality for rare positives and is robust to the heavy class imbalance present in this dataset. Higher is better.

Starter tips
- Begin with gradient‑boosted trees or linear models with strong regularization.
- Engineer calendar features (e.g., quarters, weekdays) and group‑level statistics. Be careful to compute them without peeking into test data.
- Tune class weighting and evaluate with temporal cross‑validation.

Rules and constraints
- Use only the provided features; do not derive features from any external data that would not be known at reservation time.
- Predictions must be probabilities in [0,1].
- Ensure your pipeline is deterministic and reproducible.
