# OpenMLE-fast task

Task ID: `tehran-houses@1`

Native metric: `HousePriceRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2901 bytes)
- `data/sample_submission.csv` (18448 bytes); columns: ["id", "price"]
- `data/test.csv` (142840 bytes); columns: ["id", "title", "location", "scraped_time", "meterage", "build_year", "rooms", "floor", "has_parking", "has_warehouse", "has_balcony", "has_elevator", "is_renovated"]
- `data/train.csv` (601858 bytes); columns: ["id", "title", "location", "scraped_time", "meterage", "build_year", "rooms", "floor", "has_parking", "has_warehouse", "has_balcony", "has_elevator", "is_renovated", "price"]

## Public description

```
description.txt (48 lines)
sample_submission.csv (790 lines)
test.csv (790 lines)
train.csv (3153 lines)```

-> sample_submission.csv has 789 rows and 2 columns.
Here is some information about the columns:
id (int64) has range: 3153.00 - 3941.00, 0 nan values
price (float64) has range: 32688181.19 - 664482393298.71, 0 nan values

-> test.csv has 789 rows and 13 columns.
Here is some information about the columns:
build_year (float64) has range: 1371.00 - 1404.00, 11 nan values
floor (float64) has range: 1.00 - 29.00, 27 nan values
has_balcony (bool) is 49.94% True, 50.06% False
has_elevator (bool) is 79.09% True, 20.91% False
has_parking (bool) is 76.68% True, 23.32% False
has_warehouse (bool) is 87.58% True, 12.42% False
id (int64) has range: 3153.00 - 3941.00, 0 nan values
is_renovated (bool) is 22.69% True, 77.31% False
location (object) has 434 unique values. Some example values: ['تهران، شهر\u200cزیبا', 'تهران، چیتگر', 'تهران، مبارک\u200cآباد بهشتی', 'تهران، دریاچه شهدای خلیج فارس']
meterage (int64) has range: 30.00 - 1611.00, 0 nan values
rooms (float64) has 4 unique values: [2.0, 1.0, 3.0, nan, 4.0]
scraped_time (object) has 789 unique values. Some example values: ['2025-06-27 21:26:50', '2025-06-27 13:52:35', '2025-06-27 13:52:48', '2025-06-27 13:53:03']
title (object) has 780 unique values. Some example values: ['فروش آپارتمان', 'آپارتمان', 'فرصتی استثنایی برای خانه اولی ها', 'فروش اپارتمان']

-> train.csv has 3152 rows and 14 columns.
Here is some information about the columns:
build_year (float64) has range: 1371.00 - 1404.00, 27 nan values
floor (float64) has range: 1.00 - 29.00, 104 nan values
has_balcony (bool) is 48.38% True, 51.62% False
has_elevator (bool) is 79.06% True, 20.94% False
has_parking (bool) is 81.35% True, 18.65% False
has_warehouse (bool) is 87.98% True, 12.02% False
id (int64) has range: 1.00 - 3152.00, 0 nan values
is_renovated (bool) is 22.56% True, 77.44% False
location (object) has 1190 unique values. Some example values: ['تهران، شهر\u200cزیبا', 'تهران، چیتگر', 'تهران، شهر زیبا', 'تهران، مبارک\u200cآباد بهشتی']
meterage (int64) has range: 8.00 - 100000.00, 0 nan values
price (int64) has range: 111.00 - 32500000000000.00, 0 nan values
rooms (float64) has 4 unique values: [3.0, 2.0, 1.0, 4.0, nan]
scraped_time (object) has 3152 unique values. Some example values: ['2025-06-27 13:52:21', '2025-06-24 15:29:40', '2025-06-24 15:29:44', '2025-06-24 15:29:49']
title (object) has 3070 unique values. Some example values: ['فروش آپارتمان', 'اپارتمان 100 متری به صورت اقساطی', '((اطلاعیه مهم)) شرایط ویژه خانه دار شدن', 'اپارتمان 105 متری رویاهاتو بساز']
