# OpenMLE-fast task

Task ID: `restaurant-business-rankings-2020@1`

Native metric: `RestaurantSalesRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (5749 bytes)
- `data/sample_submission.csv` (2846 bytes); columns: ["id", "Sales"]
- `data/test.csv` (8357 bytes); columns: ["id", "source", "Units", "YOY_Sales_Pct", "YOY_Units_Pct", "City", "State", "Segment_Category", "Content", "Franchising"]
- `data/train.csv` (25542 bytes); columns: ["id", "source", "Units", "YOY_Sales_Pct", "YOY_Units_Pct", "City", "State", "Segment_Category", "Content", "Franchising", "Sales"]

## Public description

```
description.txt (57 lines)
sample_submission.csv (100 lines)
test.csv (100 lines)
train.csv (302 lines)```

-> sample_submission.csv has 99 rows and 2 columns.
Here is some information about the columns:
Sales (float64) has range: 11391678.00 - 2499160974.15, 0 nan values
id (object) has 99 unique values. Some example values: ['RAVCQPC296', 'RHQ6L95032', 'R4KL4FQ369', 'RRW9CE3254']

-> test.csv has 99 rows and 10 columns.
Here is some information about the columns:
City (object) has 33 unique values. Some example values: ['New York', 'Chicago', 'Washington', 'Miami']
Content (object) has 9 unique values: [nan, 'The health-focused chain with a rotating menu is in growth mode, with plans for new units as well as its first stand-alone cocktail and juice bar, located next to a new True Food Kitchen location at Caesars Palace in Las Vegas.', "BJ's Restaurants' bullish approach to off-premise has paid off, helping it to pass TGI Fridays and become the No. 10 casual-dining chain. As of July, delivery sales at the chain were growing at a 20% clip, and the chain reported that takeout and catering sales were increasing as well. BJ's also overhauled its back-of-house operations in 2019 to make things more efficient and easier on employees.", 'Waffle House', "Olive Garden became the nation's largest casual-dining chain, growing sales 5% in 2019. The Italian chain seems to have had success bucking the delivery trend, delivering only for large orders of at least $75. It has also been focused on training and staffing to improve the dine-in experience.", "The chain filed for bankruptcy in November and was simultaneously acquired by Landry's for $40 million. The move followed the closure of 12 unprofitable stores. It joins Landry's collection of polished-casual chains such as Morton's The Steakhouse and McCormick & Schmick's.", "While Popeyes got a lot of the chicken buzz in 2019, Chick-fil-A had a busy year in its own right. On top of passing Taco Bell and Subway to become the nation's third-largest chain, it introduced dine-in mobile ordering, eliminated antibiotics from its chicken and added its first new permanent menu item in three years: mac and cheese.", "One of the country's fastest-growing chains over the past five years continued that trajectory in 2019, increasing sales by 13.9% and unit count by 6.7%. Because more than half of its sales come from takeout, it was working to improve its drive-thru technology and add mobile ordering.", 'The family-dining chain closed many underperforming units in 2019, including 23 on one day in April, reducing its unit count by more than 20% for the year. The 86-year-old brand cited "shifting consumer demographics and market dynamics" as challenges.', 'The eatertainment chain developed a new, smaller prototype that will allow it to go into small and midsize cities, greatly expanding its potential market. It was focused on places with between 100,000 and 500,000 residents. The first such location opened in Kirkland, Wash., in January.']
Franchising (object) has 2 unique values: [nan, 'Yes', 'No']
Segment_Category (object) has 32 unique values. Some example values: ['Varied Menu', 'Casual Dining & Varied Menu', 'Quick Service & Burger', 'Steak']
State (object) has 19 unique values. Some example values: ['N.Y.', 'Ill.', 'Fla.', 'TX']
Units (float64) has range: 8.00 - 13846.00, 25 nan values
YOY_Sales_Pct (float64) has range: -21.20 - 130.50, 25 nan values
YOY_Units_Pct (float64) has range: -32.80 - 116.70, 25 nan values
id (object) has 99 unique values. Some example values: ['RAVCQPC296', 'RHQ6L95032', 'R4KL4FQ369', 'RRW9CE3254']
source (object) has 3 unique values: ['Independence100', 'Top250', 'Future50']

-> train.csv has 301 rows and 11 columns.
Here is some information about the columns:
City (object) has 76 unique values. Some example values: ['New York', 'Las Vegas', 'Chicago', 'Washington']
Content (object) has 24 unique values. Some example values: ['The chain followed up on its successful 2018 introduction of zucchini noodles with a cauliflower-based noodle last year. It also saw growth via digital channels and catering, and said it was poised to resume franchise growth that had slowed in recent years as the chain stabilized.', 'The drive-in chain grew same-store sales for the second straight year under new parent Inspire Brands, which acquired Sonic in 2018. It kicked off 2020 with a refreshed look and tag line: "This is how we Sonic."', 'Under the guidance of new President Cherry Hearn, the chain updated its food and beverage menu, starting with the introduction of french fries in July. It also planned to add more chef-created sandwiches in addition to its extensive build-your-own options.', 'The third-largest pizza chain\'s self-service, heated Pizza Portals have helped it stay competitive in the carryout-pizza sector. And in January, Little Caesars made its return to the delivery space, partnering with DoorDash to deliver pies for "at least $5 less" than its competitors.']
Franchising (object) has 2 unique values: [nan, 'No', 'Yes']
Sales (float64) has range: 11391678.00 - 21380000000.00, 0 nan values
Segment_Category (object) has 44 unique values. Some example values: ['Varied Menu', 'Mexican', 'Quick Service & Burger', 'Italian/Pizza']
State (object) has 41 unique values. Some example values: ['N.Y.', 'Calif.', 'TX', 'Ill.']
Units (float64) has range: 7.00 - 23801.00, 75 nan values
YOY_Sales_Pct (float64) has range: -18.80 - 121.90, 75 nan values
YOY_Units_Pct (float64) has range: -24.60 - 94.40, 75 nan values
id (object) has 301 unique values. Some example values: ['RFREG5M036', 'RWTJCAH211', 'RH4ETC6144', 'RLK9ELG387']
source (object) has 3 unique values: ['Top250', 'Future50', 'Independence100']
