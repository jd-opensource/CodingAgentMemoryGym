# OpenMLE-fast task

Task ID: `all-recipes@2`

Native metric: `RecipeTimeEstimationMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2569 bytes)
- `data/sample_submission.csv` (9311 bytes); columns: ["id", "minutes"]
- `data/test.csv` (479552 bytes); columns: ["id", "name", "summary", "ingredient"]
- `data/train.csv` (1922785 bytes); columns: ["id", "name", "summary", "ingredient", "minutes"]

## Public description

Title: Recipe Time Estimation from Text

Background
Home cooks want to know how long a recipe will take before committing to it. The total time for a recipe is often provided on recipe sites, but forecasting it from the high-level description and ingredient list is valuable for planning, search, and recommendation.

Problem Statement
Given the recipe’s textual information, predict the total time (in minutes) it takes to complete the recipe. You will receive training data with the target label (minutes) and test data without labels. Build models that estimate total preparation+cook time from semantic cues in the title, blurb, and ingredients.

Data Description
Each row corresponds to one recipe. The dataset contains rich textual fields:
- id: unique identifier for the recipe row
- name: the recipe title
- summary: a short blurb/description of the recipe
- ingredient: the ingredient list
- minutes: the target label (only in the training set)

Important notes
- The label (minutes) was derived from the original source’s process text, but that source field is not provided in train/test to avoid leakage.
- Time expressions are rare in summaries; where present, explicit time strings were lightly masked to reduce leakage.
- Duplicate recipes across categories were deduplicated so that train and test splits do not share identical entries.

Files Provided
- train.csv: id, name, summary, ingredient, minutes
- test.csv: id, name, summary, ingredient
- sample_submission.csv: id, minutes (example format)

Task and Expectations
- Process the text data effectively (cleaning, normalization, masking, tokenization as needed).
- Engineer features from names, summaries, and ingredient lists.
- Train regression models to predict minutes.
- Evaluate and iterate to improve model performance.

Evaluation Metric
Submissions are evaluated using RMSLE (root mean squared log error) on minutes+1:
RMSLE = sqrt(mean((log1p(y_true) - log1p(y_pred_clipped))^2))
where y_pred_clipped = max(y_pred, 0). The metric emphasizes relative error and is robust to long-tailed durations.

Rules and Fairness
- Predict a non-negative number of minutes for each test id.
- The submission must contain exactly two columns: id and minutes, and cover all test ids exactly once.

Getting Started
The sample_submission.csv demonstrates the required format and value types. You may build models ranging from bag-of-words with linear regressors to advanced NLP models. Careful feature engineering around ingredients, cooking techniques, and cues in names and summaries is encouraged.
