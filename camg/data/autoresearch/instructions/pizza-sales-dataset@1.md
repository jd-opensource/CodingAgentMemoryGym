# OpenMLE-fast task

Task ID: `pizza-sales-dataset@1`

Native metric: `PizzaDemandForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2753 bytes)
- `data/sample_submission.csv` (218293 bytes); columns: ["date", "pizza_name_id", "daily_qty"]
- `data/test.csv` (692525 bytes); columns: ["date", "pizza_name_id", "pizza_size", "pizza_category", "pizza_ingredients", "pizza_name", "unit_price"]
- `data/train.csv` (3789323 bytes); columns: ["date", "pizza_name_id", "daily_qty", "pizza_size", "pizza_category", "pizza_ingredients", "pizza_name", "unit_price"]

## Public description

```
description.txt (55 lines)
sample_submission.csv (5097 lines)
test.csv (5097 lines)
train.csv (27483 lines)```

-> sample_submission.csv has 5096 rows and 3 columns.
Here is some information about the columns:
daily_qty (float64) has range: 0.00 - 3.25, 0 nan values
date (object) has 56 unique values. Some example values: ['2015-11-04', '2015-11-05', '2015-11-06', '2015-11-07']
pizza_name_id (object) has 91 unique values. Some example values: ['bbq_ckn_l', 'bbq_ckn_m', 'bbq_ckn_s', 'big_meat_s']

-> test.csv has 5096 rows and 7 columns.
Here is some information about the columns:
date (object) has 56 unique values. Some example values: ['2015-11-04', '2015-11-05', '2015-11-06', '2015-11-07']
pizza_category (object) has 4 unique values: ['Chicken', 'Classic', 'Supreme', 'Veggie']
pizza_ingredients (object) has 32 unique values. Some example values: ['Kalamata Olives, Feta Cheese, Tomatoes, Garlic, Beef Chuck Roast, Red Onions', 'Barbecued Chicken, Red Peppers, Green Peppers, Tomatoes, Red Onions, Barbecue Sauce', 'Chicken, Red Onions, Red Peppers, Mushrooms, Asiago Cheese, Alfredo Sauce', '?duja Salami, Pancetta, Tomatoes, Red Onions, Friggitello Peppers, Garlic']
pizza_name (object) has 32 unique values. Some example values: ['The Greek Pizza', 'The Barbecue Chicken Pizza', 'The Chicken Alfredo Pizza', 'The Calabrese Pizza']
pizza_name_id (object) has 91 unique values. Some example values: ['bbq_ckn_l', 'bbq_ckn_m', 'bbq_ckn_s', 'big_meat_s']
pizza_size (object) has 5 unique values: ['L', 'M', 'S', 'XL', 'XXL']
unit_price (float64) has range: 9.75 - 35.95, 0 nan values

-> train.csv has 27482 rows and 8 columns.
Here is some information about the columns:
daily_qty (int64) has range: 0.00 - 15.00, 0 nan values
date (object) has 302 unique values. Some example values: ['2015-11-03', '2015-01-01', '2015-01-02', '2015-01-03']
pizza_category (object) has 4 unique values: ['Chicken', 'Classic', 'Supreme', 'Veggie']
pizza_ingredients (object) has 32 unique values. Some example values: ['Kalamata Olives, Feta Cheese, Tomatoes, Garlic, Beef Chuck Roast, Red Onions', 'Barbecued Chicken, Red Peppers, Green Peppers, Tomatoes, Red Onions, Barbecue Sauce', 'Chicken, Red Onions, Red Peppers, Mushrooms, Asiago Cheese, Alfredo Sauce', '?duja Salami, Pancetta, Tomatoes, Red Onions, Friggitello Peppers, Garlic']
pizza_name (object) has 32 unique values. Some example values: ['The Greek Pizza', 'The Barbecue Chicken Pizza', 'The Chicken Alfredo Pizza', 'The Calabrese Pizza']
pizza_name_id (object) has 91 unique values. Some example values: ['bbq_ckn_l', 'bbq_ckn_m', 'bbq_ckn_s', 'big_meat_s']
pizza_size (object) has 5 unique values: ['L', 'M', 'S', 'XL', 'XXL']
unit_price (float64) has range: 9.75 - 35.95, 0 nan values
