# OpenMLE-fast task

Task ID: `sentimental-analysis-for-tweets@1`

Native metric: `TweetDepressionMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1584 bytes)
- `data/sample_submission.csv` (14325 bytes); columns: ["id", "label"]
- `data/test.csv` (202434 bytes); columns: ["id", "text"]
- `data/train.csv` (840965 bytes); columns: ["id", "text", "label"]

## Public description

```
description.txt (33 lines)
sample_submission.csv (2070 lines)
test.csv (2070 lines)
train.csv (8243 lines)```

-> sample_submission.csv has 2069 rows and 2 columns.
Here is some information about the columns:
id (int64) has range: 4.00 - 10300.00, 0 nan values
label (int64) has 2 unique values: [0, 1]

-> test.csv has 2069 rows and 2 columns.
Here is some information about the columns:
id (int64) has range: 4.00 - 10300.00, 0 nan values
text (object) has 2056 unique values. Some example values: ["Mom's depression tied to kids' emotional, intellectual development  https://ift.tt/2HtVZCEÂ\xa0", 'Depression is real', 'Should Mothers Avoid Nighttime Breastfeeding to Decrease Their Risk of Depression. Free handout, share and print.  http://ow.ly/Le9P30jf99GÂ\xa0 #breastfeeding #nursing #sleep #mother #baby  http://ow.ly/Le9P30jf99GÂ\xa0', 'Lonely millennials twice as likely to experience depression or anxiety, finds study  http://www.independent.co.uk/life-style/millennials-lonely-depression-anxiety-mental-health-odds-doubling-unemployed-study-a8319686.htmlÂ\xa0â\x80¦']

-> train.csv has 8242 rows and 3 columns.
Here is some information about the columns:
id (int64) has range: 1.00 - 10311.00, 0 nan values
label (int64) has 2 unique values: [0, 1]
text (object) has 8224 unique values. Some example values: ['25-04-2018', 'More than 1 in 20 US children and teens have anxiety or depression  https://www.sciencedaily.com/releases/2018/04/180424184119.htmÂ\xa0â\x80¦', 'Good morning ', 'suffering from chronic depression https://vine.co/v/iu3l2lPBhiKÂ\xa0']
