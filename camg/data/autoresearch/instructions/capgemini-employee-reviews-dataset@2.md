# OpenMLE-fast task

Task ID: `capgemini-employee-reviews-dataset@2`

Native metric: `CapgeminiEmployeeReviewMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2518 bytes)
- `data/sample_submission.csv` (39233 bytes); columns: ["review_id", "overall_rating"]
- `data/test.csv` (925664 bytes); columns: ["review_id", "Title", "Place", "Job_type", "Department", "Date", "Likes", "Dislikes"]
- `data/train.csv` (3686963 bytes); columns: ["review_id", "Title", "Place", "Job_type", "Department", "Date", "Likes", "Dislikes", "overall_rating"]

## Public description

```
description.txt (48 lines)
sample_submission.csv (5181 lines)
test.csv (6091 lines)
train.csv (24586 lines)```

-> sample_submission.csv has 5180 rows and 2 columns.
Here is some information about the columns:
overall_rating (int64) has 5 unique values: [2, 4, 1, 5, 3]
review_id (int64) has range: 15.00 - 25896.00, 0 nan values

-> test.csv has 5180 rows and 8 columns.
Here is some information about the columns:
Date (object) has 673 unique values. Some example values: ['6 May 2022', '9 Jun 2022', '9 Apr 2022', '0 Apr 2022']
Department (object) has 220 unique values. Some example values: ['Software Development Department', 'Quality Assurance and Testing Department', 'Accounting & Taxation Department', 'IT Consulting Department']
Dislikes (object) has 3786 unique values. Some example values: ['Nothing', 'Everything', 'Work life balance', 'Good']
Job_type (object) has 4 unique values: [nan, 'Full Time', 'Intern', 'Contractual', 'Part Time']
Likes (object) has 3799 unique values. Some example values: ['Nothing', 'Work life balance', 'Good', 'Job security']
Place (object) has 286 unique values. Some example values: ['Bangalore', 'Pune', 'Bengaluru/Bangalore', 'Mumbai']
Title (object) has 1208 unique values. Some example values: ['Associate Consultant', 'Consultant', 'Senior Consultant', 'Process Associate']
review_id (int64) has range: 15.00 - 25896.00, 0 nan values

-> train.csv has 20718 rows and 9 columns.
Here is some information about the columns:
Date (object) has 736 unique values. Some example values: ['6 May 2022', '9 Jun 2022', '0 Apr 2022', '9 Apr 2022']
Department (object) has 540 unique values. Some example values: ['Software Development Department', 'Quality Assurance and Testing Department', 'Accounting & Taxation Department', 'IT Consulting Department']
Dislikes (object) has 14187 unique values. Some example values: ['Nothing', 'Work life balance', 'Everything', 'No']
Job_type (object) has 5 unique values: ['Full Time', nan, 'Intern', 'Contractual', 'Part Time', 'Freelancer']
Likes (object) has 14141 unique values. Some example values: ['Nothing', 'Work life balance', 'Good', 'Work culture']
Place (object) has 694 unique values. Some example values: ['Bangalore', 'Pune', 'Bengaluru/Bangalore', 'Mumbai']
Title (object) has 3569 unique values. Some example values: ['Associate Consultant', 'Consultant', 'Senior Consultant', 'Process Associate']
overall_rating (int64) has 5 unique values: [3, 5, 4, 1, 2]
review_id (int64) has range: 1.00 - 25898.00, 0 nan values
