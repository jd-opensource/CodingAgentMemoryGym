# OpenMLE-fast task

Task ID: `supermarket-sales-cleaned-dataset@1`

Native metric: `SupermarketSatisfactionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3368 bytes)
- `data/sample_submission.csv` (10368 bytes); columns: ["Invoice ID", "Rating"]
- `data/test.csv` (47614 bytes); columns: ["Invoice ID", "Branch", "City", "Customer type", "Gender", "Product line", "Unit price", "Quantity", "Tax 5%", "Total", "Date", "Time", "Payment", "cogs", "gross margin percentage", "gross income", "Day", "Month", "Year"]
- `data/train.csv` (93038 bytes); columns: ["Invoice ID", "Branch", "City", "Customer type", "Gender", "Product line", "Unit price", "Quantity", "Tax 5%", "Total", "Date", "Time", "Payment", "cogs", "gross margin percentage", "gross income", "Rating", "Day", "Month", "Year"]

## Public description

```
description.txt (45 lines)
sample_submission.csv (346 lines)
test.csv (346 lines)
train.csv (656 lines)```

-> sample_submission.csv has 345 rows and 2 columns.
Here is some information about the columns:
Invoice ID (object) has 345 unique values. Some example values: ['898-04-2717', '101-17-6199', '102-06-2002', '102-77-2261']
Rating (float64) has 1 unique values: [7.042442748091603]

-> test.csv has 345 rows and 19 columns.
Here is some information about the columns:
Branch (object) has 3 unique values: ['A', 'C', 'B']
City (object) has 3 unique values: ['Yangon', 'Naypyitaw', 'Mandalay']
Customer type (object) has 2 unique values: ['Normal', 'Member']
Date (object) has 30 unique values. Some example values: ['2019-03-14', '2019-03-02', '2019-03-05', '2019-03-09']
Day (int64) has range: 1.00 - 30.00, 0 nan values
Gender (object) has 2 unique values: ['Male', 'Female']
Invoice ID (object) has 345 unique values. Some example values: ['898-04-2717', '101-17-6199', '102-06-2002', '102-77-2261']
Month (int64) has 1 unique values: [3]
Payment (object) has 3 unique values: ['Credit card', 'Cash', 'Ewallet']
Product line (object) has 6 unique values: ['Food and beverages', 'Sports and travel', 'Health and beauty', 'Home and lifestyle', 'Fashion accessories', 'Electronic accessories']
Quantity (int64) has range: 1.00 - 10.00, 0 nan values
Tax 5% (float64) has range: 0.78 - 48.69, 0 nan values
Time (object) has 275 unique values. Some example values: ['19:44', '18:14', '17:38', '19:26']
Total (float64) has range: 16.27 - 1022.49, 0 nan values
Unit price (float64) has range: 10.08 - 99.96, 0 nan values
Year (int64) has 1 unique values: [2019]
cogs (float64) has range: 15.50 - 973.80, 0 nan values
gross income (float64) has range: 0.78 - 48.69, 0 nan values
gross margin percentage (float64) has 1 unique values: [4.761904762]

-> train.csv has 655 rows and 20 columns.
Here is some information about the columns:
Branch (object) has 3 unique values: ['C', 'A', 'B']
City (object) has 3 unique values: ['Naypyitaw', 'Yangon', 'Mandalay']
Customer type (object) has 2 unique values: ['Member', 'Normal']
Date (object) has 59 unique values. Some example values: ['2019-02-07', '2019-02-15', '2019-01-08', '2019-01-25']
Day (int64) has range: 1.00 - 31.00, 0 nan values
Gender (object) has 2 unique values: ['Female', 'Male']
Invoice ID (object) has 655 unique values. Some example values: ['896-34-0956', '101-81-4070', '105-10-6182', '105-31-1824']
Month (int64) has 2 unique values: [1, 2]
Payment (object) has 3 unique values: ['Ewallet', 'Credit card', 'Cash']
Product line (object) has 6 unique values: ['Health and beauty', 'Fashion accessories', 'Sports and travel', 'Electronic accessories', 'Food and beverages', 'Home and lifestyle']
Quantity (int64) has range: 1.00 - 10.00, 0 nan values
Rating (float64) has range: 4.00 - 10.00, 0 nan values
Tax 5% (float64) has range: 0.51 - 49.65, 0 nan values
Time (object) has 403 unique values. Some example values: ['14:42', '11:51', '19:48', '11:40']
Total (float64) has range: 10.68 - 1042.65, 0 nan values
Unit price (float64) has range: 10.16 - 99.96, 0 nan values
Year (int64) has 1 unique values: [2019]
cogs (float64) has range: 10.17 - 993.00, 0 nan values
gross income (float64) has range: 0.51 - 49.65, 0 nan values
gross margin percentage (float64) has 1 unique values: [4.761904762]
