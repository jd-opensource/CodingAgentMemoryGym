# OpenMLE-fast task

Task ID: `airbnbopendata@1`

Native metric: `AirbnbInstantBookMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (752 bytes)
- `data/sample_submission.csv` (573250 bytes); columns: ["id", "instant_bookable"]
- `data/test.csv` (7264934 bytes); columns: ["id", "NAME", "host id", "host_identity_verified", "host name", "neighbourhood group", "neighbourhood", "lat", "long", "country", "country code", "cancellation_policy", "room type", "Construction year", "price", "service fee", "minimum nights", "number of reviews", "last review", "reviews per month", "review rate number", "calculated host listings count", "availability 365", "house_rules", "license"]
- `data/train.csv` (29148495 bytes); columns: ["id", "NAME", "host id", "host_identity_verified", "host name", "neighbourhood group", "neighbourhood", "lat", "long", "country", "country code", "instant_bookable", "cancellation_policy", "room type", "Construction year", "price", "service fee", "minimum nights", "number of reviews", "last review", "reviews per month", "review rate number", "calculated host listings count", "availability 365", "house_rules", "license"]

## Public description

```
description.txt (51 lines)
sample_submission.csv (20392 lines)
test.csv (20480 lines)
train.csv (81878 lines)```

-> sample_submission.csv has 20391 rows and 2 columns.
The columns are: id, instant_bookable

-> test.csv has 20391 rows and 25 columns.
The columns are: id, NAME, host id, host_identity_verified, host name, neighbourhood group, neighbourhood, lat, long, country, country code, cancellation_policy, room type, Construction year, price... and 10 more columns

-> train.csv has 81562 rows and 26 columns.
The columns are: id, NAME, host id, host_identity_verified, host name, neighbourhood group, neighbourhood, lat, long, country, country code, instant_bookable, cancellation_policy, room type, Construction year... and 11 more columns
