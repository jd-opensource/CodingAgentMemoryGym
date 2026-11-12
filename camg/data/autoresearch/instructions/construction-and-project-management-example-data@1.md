# OpenMLE-fast task

Task ID: `construction-and-project-management-example-data@1`

Native metric: `ConstructionTaskClosureMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4304 bytes)
- `data/sample_submission.csv` (60842 bytes); columns: ["id", "days_to_close"]
- `data/test.csv` (622264 bytes); columns: ["id", "created_date", "description", "location_l1", "location_l2", "location_l3", "location_l4", "task_type", "to_package", "association", "priority", "cause", "project_id", "task_group", "overdue", "has_images", "has_comments", "has_documents", "forms_hist_count_project", "forms_hist_open_actions_sum_project", "forms_hist_total_actions_sum_project", "forms_hist_closed_count_project", "forms_hist_open_action_rate_project", "forms_hist_closed_rate_project"]
- `data/train.csv` (2502675 bytes); columns: ["id", "created_date", "description", "location_l1", "location_l2", "location_l3", "location_l4", "task_type", "to_package", "association", "priority", "cause", "project_id", "task_group", "overdue", "has_images", "has_comments", "has_documents", "forms_hist_count_project", "forms_hist_open_actions_sum_project", "forms_hist_total_actions_sum_project", "forms_hist_closed_count_project", "forms_hist_open_action_rate_project", "forms_hist_closed_rate_project", "days_to_close"]

## Public description

Title: Predict Task Time-to-Closure from Construction PM Data

Problem statement
You are given task records from construction project management field apps (quality, safety, and site management). Each task is created with a description, location hierarchy, categorical context (type, package, association, task group), binary media flags, and project identifier. In addition, project-level historical context derived from forms (inspections, diaries, permits, etc.) up to the task creation time is provided as engineered features. Your goal is to predict how many days a newly created task will take to close.

Task type: Regression — predict the continuous label days_to_close.

Files
- train.csv: Training set with features and the target.
- test.csv: Test set with the same features but without the target.
- sample_submission.csv: Sample submission file (ids and a random but valid prediction).

Target
- days_to_close: The time between task creation and closure, measured in days (>= 0). This has been computed from the original raw timestamps and included only for train.csv.

Features
The following columns are provided to build your model. They are all available at creation time (no leakage) and are safe to use.
- id: Unique record id. Use this to join predictions back.
- created_date: UTC date string (YYYY-MM-DD) of task creation (safe to use as a temporal feature).
- description: Free-text description entered by field staff.
- location_l1 to location_l4: Hierarchical location path split into up to four levels.
- task_type, to_package, association, priority, cause, project_id, task_group: Categorical context fields from the task record.
- overdue, has_images, has_comments, has_documents: Binary flags (0/1) indicating media or overdue status at creation.
- forms_hist_count_project: Count of forms previously created in the same project up to (but not including) the task date.
- forms_hist_open_actions_sum_project: Cumulative open actions from forms previously created in the same project.
- forms_hist_total_actions_sum_project: Cumulative total actions from forms previously created in the same project.
- forms_hist_closed_count_project: Cumulative count of forms marked closed previously in the same project.
- forms_hist_open_action_rate_project: Ratio open_actions_sum/total_actions_sum (0 if denominator is 0).
- forms_hist_closed_rate_project: Ratio closed_count/count (0 if denominator is 0).

Submission format
- A single CSV with the following two columns in this exact order:
  - id
  - days_to_close
- The set of ids must match those in test.csv exactly, with one row per id and no duplicates.
- The predicted days_to_close values must be numeric and non-negative.

Evaluation
- Root Mean Squared Logarithmic Error (RMSLE) between the true and predicted days_to_close values is used as the metric. Specifically, we compute sqrt(mean((log1p(y_true) - log1p(y_pred))^2)).
- Motivation: Task closure times are right-skewed and heavy-tailed; RMSLE stabilizes variance, penalizes large relative errors, and remains sensitive for short-duration tasks via the +1 shift.

Recommended approach (non-binding)
- Data processing: parse and clean text, handle rare categories, consider using target encoding with cross-validation on categorical fields, and build robust numeric scalers.
- Feature engineering: n-grams or lightweight text embeddings from description; parse location hierarchy features; interactions between task_type/task_group/project; calendar features from created_date (weekday, month); leverage provided project-level historical aggregates; optionally derive cross-project statistics only on training folds to avoid leakage.
- Models: strong baselines include gradient boosting (XGBoost/LightGBM/CatBoost) with text features or shallow NLP models; more advanced participants may use transformer encoders for text combined with tabular models.
- Validation: use time-aware validation (e.g., forward chaining) to mimic the final split.

Rules and caveats
- Do not assume any paths or filenames beyond those provided (train.csv, test.csv, sample_submission.csv).
- The feature names are stable and can be used directly. Avoid using external data.
- Ensure your preprocessing is robust to missing or unseen categories in the test set.

Good luck and build safely!
