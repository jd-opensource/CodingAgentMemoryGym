# OpenMLE-fast task

Task ID: `365ds-practice-exams-people-analytics-dataset@2`

Native metric: `PeopleAnalyticsNextTitleMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4201 bytes)
- `data/meta.json` (235 bytes)
- `data/sample_submission.csv` (4312849 bytes); columns: ["event_id", "Engineer", "Manager", "Senior Engineer", "Senior Staff", "Staff", "Technique Leader"]
- `data/test.csv` (2926139 bytes); columns: ["event_id", "emp_no", "event_date", "gender", "age_years", "tenure_days", "prev_title", "time_in_prev_title_days", "prior_title_changes", "dept_no", "dept_tenure_days", "dept_transitions", "is_manager_current", "salary_last", "salary_prev", "days_since_last_salary_change", "salary_change", "salary_change_rate"]
- `data/train.csv` (11491823 bytes); columns: ["event_id", "emp_no", "event_date", "gender", "age_years", "tenure_days", "prev_title", "time_in_prev_title_days", "prior_title_changes", "dept_no", "dept_tenure_days", "dept_transitions", "is_manager_current", "salary_last", "salary_prev", "days_since_last_salary_change", "salary_change", "salary_change_rate", "next_title"]

## Public description

Title: Next-Title Prediction at Promotion/Transition Events (Time-Aware Multiclass Classification)

Problem statement
Organizations must anticipate employees’ next job titles to plan promotions, backfills, and compensation. In this competition, each data point is a title-change event for an employee. Given only information available strictly before the event date, predict which job title will become effective at that date.

Task
- Input: A row-level feature snapshot built strictly from historical data prior to each event date.
- Output: A probability distribution over all possible next-title classes for each test event.

Files
- train.csv: Feature table for training events, including the target column next_title.
- test.csv: Feature table for test events without the target.
- sample_submission.csv: Example submission with event_id and one probability column per title class (columns match the set of classes present in train.csv). Rows correspond 1:1 to test.csv via event_id.

Data description (columns)
Each row represents an employee title-change event occurring on event_date. Features are computed to be leakage-free (only data strictly before event_date is used):
- event_id: Unique identifier for the event (key for submissions).
- emp_no: Employee identifier.
- event_date: Date when the new title becomes effective.
- gender: Employee gender.
- age_years: Employee age (in years) at event_date.
- tenure_days: Days since hire at event_date.
- prev_title: Title held immediately before event_date.
- time_in_prev_title_days: Days spent in previous title up to event_date.
- prior_title_changes: Count of title changes before event_date.
- dept_no: Active department just before event_date (categorical).
- dept_tenure_days: Days in the active department up to event_date.
- dept_transitions: Number of prior department transitions up to event_date.
- is_manager_current: 1 if the employee held a manager assignment just before event_date, else 0.
- salary_last: Most recent salary strictly before event_date.
- salary_prev: Salary immediately prior to salary_last (if available).
- days_since_last_salary_change: Days since the last salary change as of event_date.
- salary_change: salary_last − salary_prev (if salary_prev exists).
- salary_change_rate: (salary_last − salary_prev) / |salary_prev| (if salary_prev exists).
- next_title (train only): The title that becomes effective at event_date (the target class).

Important notes
- Temporal validity: All features are constructed strictly from data before each event_date to prevent label leakage.
- Event construction: Events are derived from the titles history; for each employee, the first title entry is skipped, and every subsequent titles.from_date defines an event with label equal to that row’s title.
- Time split: Train and test events are split by a global cutoff date to emulate real forecasting.

Submission format
- The submission must contain:
  - Column event_id.
  - One column per title class appearing in train.csv. Column names must exactly match those class names.
- For each row, class probabilities must be non-negative and sum to 1 (the evaluation script will safely clip/renormalize small numerical deviations).

Evaluation
- Metric: Multiclass Logarithmic Loss (log loss) over the next_title classes.
- Formal definition: For each test row i with true class y_i and submitted probability p_i(y_i), the score is −(1/N) Σ_i log(max(eps, min(1 − eps, p_i(y_i)))), where eps is a small constant for numerical stability.
- Why this metric: It rewards calibrated probabilities, handles class imbalance, and reflects uncertainty in real promotion pathways.

Best practices
- Engineer time-aware features (e.g., tenure dynamics, title transition patterns, department history, salary momentum) and avoid peeking at post-event data.
- Consider class imbalance and temporal nonstationarity across years and departments.

Deliverables expected from participants
- Train a multiclass model on train.csv, generate calibrated probabilities for all classes on test.csv, and submit a CSV matching sample_submission.csv’s structure.

Good luck and enjoy exploring promotion dynamics in people analytics!
