# OpenMLE-fast task

Task ID: `hotel-booking-dataset@1`

Native metric: `HotelBookingCancellationMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4787 bytes)
- `data/sample_submission.csv` (1611678 bytes); columns: ["id", "is_canceled"]
- `data/test.csv` (5459882 bytes); columns: ["id", "hotel", "lead_time", "arrival_date_year", "arrival_date_month", "arrival_date_week_number", "arrival_date_day_of_month", "stays_in_weekend_nights", "stays_in_week_nights", "adults", "children", "babies", "meal", "country", "market_segment", "distribution_channel", "is_repeated_guest", "previous_cancellations", "previous_bookings_not_canceled", "reserved_room_type", "deposit_type", "agent", "company", "days_in_waiting_list", "customer_type", "adr", "required_car_parking_spaces", "total_of_special_requests"]
- `data/train.csv` (10891252 bytes); columns: ["id", "hotel", "lead_time", "arrival_date_year", "arrival_date_month", "arrival_date_week_number", "arrival_date_day_of_month", "stays_in_weekend_nights", "stays_in_week_nights", "adults", "children", "babies", "meal", "country", "market_segment", "distribution_channel", "is_repeated_guest", "previous_cancellations", "previous_bookings_not_canceled", "reserved_room_type", "deposit_type", "agent", "company", "days_in_waiting_list", "customer_type", "adr", "required_car_parking_spaces", "total_of_special_requests", "is_canceled"]

## Public description

```
description.txt (60 lines)
sample_submission.csv (40688 lines)
test.csv (40688 lines)
train.csv (78704 lines)```

-> sample_submission.csv has 40687 rows and 2 columns.
Here is some information about the columns:
id (uint64) has range: 249194204490780.00 - 18446400725910437888.00, 0 nan values
is_canceled (float64) has range: 0.05 - 0.95, 0 nan values

-> test.csv has 40687 rows and 28 columns.
Here is some information about the columns:
adr (float64) has range: -6.38 - 510.00, 0 nan values
adults (int64) has 5 unique values: [2, 1, 3, 4, 0]
agent (float64) has range: 1.00 - 535.00, 5664 nan values
arrival_date_day_of_month (int64) has range: 1.00 - 31.00, 0 nan values
arrival_date_month (object) has 8 unique values: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August']
arrival_date_week_number (int64) has range: 1.00 - 35.00, 0 nan values
arrival_date_year (int64) has 1 unique values: [2017]
babies (int64) has 3 unique values: [0, 1, 2]
children (float64) has 4 unique values: [0.0, 2.0, 1.0, 3.0]
company (float64) has range: 9.00 - 543.00, 38377 nan values
country (object) has 149 unique values. Some example values: ['PRT', 'GBR', 'FRA', 'DEU']
customer_type (object) has 4 unique values: ['Transient', 'Transient-Party', 'Contract', 'Group']
days_in_waiting_list (int64) has range: 0.00 - 223.00, 0 nan values
deposit_type (object) has 3 unique values: ['No Deposit', 'Non Refund', 'Refundable']
distribution_channel (object) has 4 unique values: ['TA/TO', 'Direct', 'Corporate', 'GDS']
hotel (object) has 2 unique values: ['Resort Hotel', 'City Hotel']
id (uint64) has range: 249194204490780.00 - 18446400725910437888.00, 0 nan values
is_repeated_guest (int64) has 2 unique values: [0, 1]
lead_time (int64) has range: 0.00 - 629.00, 0 nan values
market_segment (object) has 7 unique values: ['Online TA', 'Offline TA/TO', 'Direct', 'Corporate', 'Complementary', 'Groups', 'Aviation']
meal (object) has 5 unique values: ['BB', 'HB', 'Undefined', 'FB', 'SC']
previous_bookings_not_canceled (int64) has range: 0.00 - 72.00, 0 nan values
previous_cancellations (int64) has 7 unique values: [0, 1, 2, 3, 4, 5, 6]
required_car_parking_spaces (int64) has 5 unique values: [0, 1, 2, 8, 3]
reserved_room_type (object) has 9 unique values: ['A', 'D', 'E', 'G', 'H', 'F', 'C', 'B', 'P']
stays_in_week_nights (int64) has range: 0.00 - 40.00, 0 nan values
stays_in_weekend_nights (int64) has range: 0.00 - 16.00, 0 nan values
total_of_special_requests (int64) has 6 unique values: [0, 1, 2, 3, 4, 5]

-> train.csv has 78703 rows and 29 columns.
Here is some information about the columns:
adr (float64) has range: 0.00 - 5400.00, 0 nan values
adults (int64) has range: 0.00 - 55.00, 0 nan values
agent (float64) has range: 1.00 - 481.00, 10676 nan values
arrival_date_day_of_month (int64) has range: 1.00 - 31.00, 0 nan values
arrival_date_month (object) has 12 unique values. Some example values: ['October', 'September', 'August', 'July']
arrival_date_week_number (int64) has range: 1.00 - 53.00, 0 nan values
arrival_date_year (int64) has 2 unique values: [2015, 2016]
babies (int64) has 5 unique values: [0, 1, 2, 10, 9]
children (float64) has 5 unique values: [0.0, 1.0, 2.0, 10.0, 3.0, nan]
company (float64) has range: 6.00 - 499.00, 74216 nan values
country (object) has 159 unique values. Some example values: ['PRT', 'GBR', 'FRA', 'ESP']
customer_type (object) has 4 unique values: ['Transient', 'Contract', 'Transient-Party', 'Group']
days_in_waiting_list (int64) has range: 0.00 - 391.00, 0 nan values
deposit_type (object) has 3 unique values: ['No Deposit', 'Refundable', 'Non Refund']
distribution_channel (object) has 5 unique values: ['Direct', 'Corporate', 'TA/TO', 'Undefined', 'GDS']
hotel (object) has 2 unique values: ['Resort Hotel', 'City Hotel']
id (uint64) has range: 462566098869700.00 - 18446540617835773952.00, 0 nan values
is_canceled (int64) has 2 unique values: [0, 1]
is_repeated_guest (int64) has 2 unique values: [0, 1]
lead_time (int64) has range: 0.00 - 737.00, 0 nan values
market_segment (object) has 8 unique values: ['Direct', 'Corporate', 'Online TA', 'Offline TA/TO', 'Complementary', 'Groups', 'Undefined', 'Aviation']
meal (object) has 5 unique values: ['BB', 'FB', 'HB', 'SC', 'Undefined']
previous_bookings_not_canceled (int64) has range: 0.00 - 58.00, 0 nan values
previous_cancellations (int64) has range: 0.00 - 26.00, 0 nan values
required_car_parking_spaces (int64) has 4 unique values: [0, 1, 2, 3]
reserved_room_type (object) has 10 unique values. Some example values: ['A', 'D', 'E', 'F']
stays_in_week_nights (int64) has range: 0.00 - 50.00, 0 nan values
stays_in_weekend_nights (int64) has range: 0.00 - 19.00, 0 nan values
total_of_special_requests (int64) has 6 unique values: [0, 1, 3, 2, 4, 5]
