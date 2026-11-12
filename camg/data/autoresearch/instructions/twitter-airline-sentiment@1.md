# OpenMLE-fast task

Task ID: `twitter-airline-sentiment@1`

Native metric: `AirlineTweetSentimentMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3405 bytes)
- `data/sample_submission.csv` (56974 bytes); columns: ["tweet_id", "airline_sentiment"]
- `data/test.csv` (425482 bytes); columns: ["tweet_id", "text", "airline", "retweet_count", "tweet_coord", "tweet_created", "tweet_location", "user_timezone", "name"]
- `data/test.sqlite` (458752 bytes)
- `data/train.csv` (2641147 bytes); columns: ["tweet_id", "airline_sentiment", "text", "airline", "retweet_count", "tweet_coord", "tweet_created", "tweet_location", "user_timezone", "name"]
- `data/train.sqlite` (2809856 bytes)

## Public description

```
description.txt (50 lines)
sample_submission.csv (2059 lines)
test.csv (2079 lines)
test.sqlite (458.8 kB)
train.csv (12768 lines)
train.sqlite (2.8 MB)```

-> sample_submission.csv has 2058 rows and 2 columns.
Here is some information about the columns:
airline_sentiment (object) has 3 unique values: ['neutral', 'positive', 'negative']
tweet_id (int64) has range: 567591480085463040.00 - 570307026263384064.00, 0 nan values

-> test.csv has 2058 rows and 9 columns.
Here is some information about the columns:
airline (object) has 6 unique values: ['United', 'US Airways', 'Southwest', 'Delta', 'Virgin America', 'American']
name (object) has 1723 unique values. Some example values: ['otisday', 'c_cgottlieb', '_mhertz', 'scoobydoo9749']
retweet_count (int64) has 8 unique values: [0, 1, 4, 3, 8, 2, 9, 5]
text (object) has 2057 unique values. Some example values: ['@JetBlue Thank you!', '@USAirways Southern Hospitality luggage delivery service from SAV is AWFUL. Great @ delivering empty promises but not luggage #8hrs&amp;waiting', '@USAirways  flight missed due to mech issue. No food voucher, transported to different airport, no rental reimbursement 😡', '@USAirways - flights 4500 AND 403 delayed for "crew availability?"  What gives? I\'m getting to TPA 2.5 hrs past my scheduled arrival.']
tweet_coord (object) has 120 unique values. Some example values: ['[0.0, 0.0]', '[40.35805521, -111.78241283]', '[36.08576903, -115.14953095]', '[35.99558298, -78.89974547]']
tweet_created (object) has 2056 unique values. Some example values: ['2015-02-21 18:40:33 -0800', '2015-02-23 09:46:54 -0800', '2015-02-22 18:18:46 -0800', '2015-02-22 18:16:42 -0800']
tweet_id (int64) has range: 567591480085463040.00 - 570307026263384064.00, 0 nan values
tweet_location (object) has 840 unique values. Some example values: ['Washington, DC', 'New York, NY', 'Boston, MA', 'San Francisco, CA']
user_timezone (object) has 48 unique values. Some example values: ['Eastern Time (US & Canada)', 'Central Time (US & Canada)', 'Pacific Time (US & Canada)', 'Quito']

-> train.csv has 12564 rows and 10 columns.
Here is some information about the columns:
airline (object) has 6 unique values: ['Delta', 'United', 'Southwest', 'US Airways', 'Virgin America', 'American']
airline_sentiment (object) has 3 unique values: ['neutral', 'negative', 'positive']
name (object) has 7001 unique values. Some example values: ['JetBlueNews', 'kbosspotter', '_mhertz', 'throthra']
retweet_count (int64) has range: 0.00 - 44.00, 0 nan values
text (object) has 12370 unique values. Some example values: ['@united thanks', '@SouthwestAir sent', '@JetBlue thanks!', '@AmericanAir thanks']
tweet_coord (object) has 716 unique values. Some example values: ['[0.0, 0.0]', '[40.64656067, -73.78334045]', '[40.64646912, -73.79133606]', '[39.83426941, -104.69960636]']
tweet_created (object) has 12249 unique values. Some example values: ['2015-02-24 11:43:05 -0800', '2015-02-24 09:54:34 -0800', '2015-02-24 11:38:11 -0800', '2015-02-24 11:32:49 -0800']
tweet_id (int64) has range: 567588278875213824.00 - 570310600460525568.00, 0 nan values
tweet_location (object) has 2844 unique values. Some example values: ['Boston, MA', 'New York, NY', 'Washington, DC', 'USA']
user_timezone (object) has 84 unique values. Some example values: ['Eastern Time (US & Canada)', 'Central Time (US & Canada)', 'Pacific Time (US & Canada)', 'Quito']
