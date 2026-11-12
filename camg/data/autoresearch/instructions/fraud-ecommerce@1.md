# OpenMLE-fast task

Task ID: `fraud-ecommerce@1`

Native metric: `FraudDetectionMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/IpAddress_to_Country.csv` (4894783 bytes); columns: ["lower_bound_ip_address", "upper_bound_ip_address", "country"]
- `data/description.txt` (2943 bytes)
- `data/sample_submission.csv` (1409267 bytes); columns: ["row_id", "is_fraud"]
- `data/test.csv` (4501382 bytes); columns: ["row_id", "signup_time", "purchase_time", "purchase_value", "device_id", "source", "browser", "sex", "age", "ip_address"]
- `data/train.csv` (9834377 bytes); columns: ["row_id", "signup_time", "purchase_time", "purchase_value", "device_id", "source", "browser", "sex", "age", "ip_address", "is_fraud"]

## Public description

```
IpAddress_to_Country.csv (138847 lines)
description.txt (54 lines)
sample_submission.csv (48147 lines)
test.csv (48147 lines)
train.csv (102967 lines)```

-> IpAddress_to_Country.csv has 138846 rows and 3 columns.
Here is some information about the columns:
country (object) has 235 unique values. Some example values: ['United States', 'Canada', 'Russian Federation', 'Australia']
lower_bound_ip_address (float64) has range: 16777216.00 - 3758096128.00, 0 nan values
upper_bound_ip_address (int64) has range: 16777471.00 - 3758096383.00, 0 nan values

-> sample_submission.csv has 48146 rows and 2 columns.
Here is some information about the columns:
is_fraud (float64) has range: 0.00 - 1.00, 0 nan values
row_id (object) has 48146 unique values. Some example values: ['RID151111', 'RID102966', 'RID102967', 'RID102968']

-> test.csv has 48146 rows and 10 columns.
Here is some information about the columns:
age (int64) has range: 18.00 - 73.00, 0 nan values
browser (object) has 5 unique values: ['IE', 'Chrome', 'FireFox', 'Safari', 'Opera']
device_id (object) has 47494 unique values. Some example values: ['XFXQZDURPTABX', 'CUGZZQSSGCIDS', 'ESTKJLLKCHBMW', 'SWHJOBVGERQIP']
ip_address (int64) has range: 155399.00 - 4294822242.00, 0 nan values
purchase_time (object) has 48001 unique values. Some example values: ['2015-09-10 09:04:53', '2015-09-09 05:54:05', '2015-08-25 21:18:00', '2015-10-08 09:56:54']
purchase_value (int64) has range: 9.00 - 129.00, 0 nan values
row_id (object) has 48146 unique values. Some example values: ['RID151111', 'RID102966', 'RID102967', 'RID102968']
sex (object) has 2 unique values: ['F', 'M']
signup_time (object) has 48146 unique values. Some example values: ['2015-08-18 04:19:56', '2015-06-06 09:22:03', '2015-05-05 08:00:26', '2015-04-09 10:13:38']
source (object) has 3 unique values: ['SEO', 'Direct', 'Ads']

-> train.csv has 102966 rows and 11 columns.
Here is some information about the columns:
age (int64) has range: 18.00 - 76.00, 0 nan values
browser (object) has 5 unique values: ['Chrome', 'IE', 'Safari', 'FireFox', 'Opera']
device_id (object) has 92814 unique values. Some example values: ['ZUSVMDEZRBDTX', 'NGQCKIADMZORL', 'ITUMJCKWEYNDD', 'KIPFSCNUGOLDP']
ip_address (int64) has range: 52093.00 - 4294850500.00, 0 nan values
is_fraud (int64) has 2 unique values: [1, 0]
purchase_time (object) has 102678 unique values. Some example values: ['2015-06-08 09:42:04', '2015-07-17 23:22:55', '2015-05-16 01:30:22', '2015-06-22 21:19:53']
purchase_value (int64) has range: 9.00 - 154.00, 0 nan values
row_id (object) has 102966 unique values. Some example values: ['RID102965', 'RID000000', 'RID000001', 'RID000002']
sex (object) has 2 unique values: ['F', 'M']
signup_time (object) has 102966 unique values. Some example values: ['2015-05-05 10:37:10', '2015-01-01 00:00:43', '2015-01-01 00:00:44', '2015-01-01 00:00:45']
source (object) has 3 unique values: ['Ads', 'SEO', 'Direct']
