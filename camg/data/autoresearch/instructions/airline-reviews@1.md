# OpenMLE-fast task

Task ID: `airline-reviews@1`

Native metric: `AirlineReviewQWKMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (616 bytes)
- `data/sample_submission.csv` (89345 bytes); columns: ["review_id", "overall_rating"]
- `data/test.csv` (4074319 bytes); columns: ["review_id", "airline_name", "review_title", "review_date", "verified", "review_text", "aircraft", "type_of_traveller", "seat_type", "route", "date_flown"]
- `data/train.csv` (15450239 bytes); columns: ["review_id", "airline_name", "review_title", "review_date", "verified", "review_text", "aircraft", "type_of_traveller", "seat_type", "route", "date_flown", "overall_rating"]

## Public description

```
description.txt (50 lines)
sample_submission.csv (4467 lines)
test.csv (4467 lines)
train.csv (17864 lines)```

-> sample_submission.csv has 4466 rows and 2 columns.
The columns are: review_id, overall_rating

-> test.csv has 4466 rows and 11 columns.
The columns are: review_id, airline_name, review_title, review_date, verified, review_text, aircraft, type_of_traveller, seat_type, route, date_flown

-> train.csv has 17863 rows and 12 columns.
The columns are: review_id, airline_name, review_title, review_date, verified, review_text, aircraft, type_of_traveller, seat_type, route, date_flown, overall_rating
