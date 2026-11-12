# OpenMLE-fast task

Task ID: `airbnb-cleaned-europe-dataset@2`

Native metric: `AirbnbSatisfactionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (308 bytes)
- `data/sample_submission.csv` (89600 bytes); columns: ["id", "Guest Satisfaction"]
- `data/test.csv` (1638986 bytes); columns: ["id", "City", "Price", "Day", "Room Type", "Shared Room", "Private Room", "Person Capacity", "Superhost", "Multiple Rooms", "Business", "Cleanliness Rating", "Bedrooms", "City Center (km)", "Metro Distance (km)", "Attraction Index", "Normalised Attraction Index", "Restraunt Index", "Normalised Restraunt Index"]
- `data/train.csv` (6728508 bytes); columns: ["id", "City", "Price", "Day", "Room Type", "Shared Room", "Private Room", "Person Capacity", "Superhost", "Multiple Rooms", "Business", "Cleanliness Rating", "Guest Satisfaction", "Bedrooms", "City Center (km)", "Metro Distance (km)", "Attraction Index", "Normalised Attraction Index", "Restraunt Index", "Normalised Restraunt Index"]

## Public description

Airbnb Guest Satisfaction Prediction (Europe)

Public directory contents:
- train.csv: Training data with features and target (Guest Satisfaction).
- test.csv: Test data with the same features and id (no target).
- sample_submission.csv: Expected submission format with columns ['id', 'Guest Satisfaction'].
