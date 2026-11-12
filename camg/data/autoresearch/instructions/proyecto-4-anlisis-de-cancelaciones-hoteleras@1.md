# OpenMLE-fast task

Task ID: `proyecto-4-anlisis-de-cancelaciones-hoteleras@1`

Native metric: `HotelBookingCancellationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2884 bytes)
- `data/sample_submission.csv` (1109653 bytes); columns: ["booking_id", "is_canceled"]
- `data/test.csv` (4194445 bytes); columns: ["hotel", "lead_time", "arrival_date_year", "arrival_date_month", "arrival_date_week_number", "arrival_date_day_of_month", "stays_in_weekend_nights", "stays_in_week_nights", "adults", "children", "babies", "meal", "country", "market_segment", "distribution_channel", "is_repeated_guest", "previous_cancellations", "previous_bookings_not_canceled", "reserved_room_type", "agent", "company", "customer_type", "required_car_parking_spaces", "total_of_special_requests", "booking_id"]
- `data/train.csv` (8450401 bytes); columns: ["hotel", "lead_time", "arrival_date_year", "arrival_date_month", "arrival_date_week_number", "arrival_date_day_of_month", "stays_in_weekend_nights", "stays_in_week_nights", "adults", "children", "babies", "meal", "country", "market_segment", "distribution_channel", "is_repeated_guest", "previous_cancellations", "previous_bookings_not_canceled", "reserved_room_type", "agent", "company", "customer_type", "required_car_parking_spaces", "total_of_special_requests", "is_canceled", "booking_id"]

## Public description

Competition: Booking Cancellation Risk at Reservation Time

Problem statement
Predict the probability that a hotel reservation will be canceled (or no-show) given information available at reservation time. Your model should output well-calibrated probabilities for is_canceled = 1 for each reservation in the test set.

Files
- train.csv — Booking-time features and the target label.
- test.csv — Booking-time features for scoring (no target label).
- sample_submission.csv — Example submission file with the required format.

Target
- is_canceled (binary): 1 if the reservation ended as canceled or no-show; 0 otherwise.

Row identifier
- booking_id: Unique identifier for each reservation. Must be used to merge predictions with the correct rows.

Features provided (booking-time only)
- hotel (categorical)
- lead_time (numeric)
- arrival_date_year (numeric)
- arrival_date_month (categorical; month name)
- arrival_date_week_number (numeric)
- arrival_date_day_of_month (numeric)
- stays_in_weekend_nights (numeric)
- stays_in_week_nights (numeric)
- adults (numeric)
- children (numeric; may contain missing values)
- babies (numeric)
- meal (categorical)
- country (categorical; high cardinality)
- market_segment (categorical)
- distribution_channel (categorical)
- is_repeated_guest (binary)
- previous_cancellations (numeric)
- previous_bookings_not_canceled (numeric)
- reserved_room_type (categorical)
- agent (categorical; high cardinality; many unknowns)
- company (categorical; high cardinality; many unknowns)
- customer_type (categorical)
- required_car_parking_spaces (numeric)
- total_of_special_requests (numeric)

Data split
- Train: Reservations with arrival_date_year in 2015–2016.
- Test: Reservations with arrival_date_year in 2017.
This time-based split mimics real-world deployment and prevents temporal leakage.

Evaluation
- Metric: ROC AUC on the predicted probabilities for is_canceled = 1.
- Submission format: A CSV with columns [booking_id, is_canceled], where is_canceled is a probability in [0, 1]. The booking_id set must exactly match test.csv.

Notes and recommendations
- The split introduces temporal drift (2015–2016 → 2017). Expect changes in seasonality and channel/segment mix.
- Several categorical features have high cardinality (country, agent, company). Consider robust encoders (e.g., target encoding with proper CV, hashing) and regularization.
- Handle missing values carefully (e.g., children, agent, company may have missing/unknowns).
- Feature engineering on dates and party composition can help (e.g., total nights, party size, calendar features). Calibration (Platt/Isotonic) can improve probability quality.

Rules
- Use only the provided columns. The test set contains the same feature columns as the train set.
- The order of rows in the submission does not matter, but the IDs must match exactly and be unique.
