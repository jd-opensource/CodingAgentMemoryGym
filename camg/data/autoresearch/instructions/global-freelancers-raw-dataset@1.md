# OpenMLE-fast task

Task ID: `global-freelancers-raw-dataset@1`

Native metric: `FreelancerHourlyRateMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3430 bytes)
- `data/sample_submission.csv` (2950 bytes); columns: ["row_id", "hourly_rate_usd"]
- `data/test.csv` (12426 bytes); columns: ["row_id", "gender", "age", "country", "language", "primary_skill", "years_of_experience", "rating", "is_active", "client_satisfaction"]
- `data/train.csv` (53189 bytes); columns: ["row_id", "gender", "age", "country", "language", "primary_skill", "years_of_experience", "rating", "is_active", "client_satisfaction", "hourly_rate_usd"]

## Public description

Competition: Predict Freelancer Hourly Rate (USD) from Messy Global Profiles

Problem statement
You are given messy, real-world-style freelancer profile data spanning demographics, skills, and platform attributes. Your task is to predict the standardized hourly rate in USD for each freelancer in the test set. Success requires robust data cleaning, thoughtful feature engineering, and effective modeling on tabular data.

Data description
The competition data is constructed from a raw collection of 1,000 fictional freelancer profiles. Features include demographic and professional information with realistic noise and formatting issues. You will receive the following files:
- train.csv: Cleaned training data with features and the target.
- test.csv: Cleaned test data with features only.
- sample_submission.csv: An example submission file with the correct format.

Columns
- row_id: Unique identifier for each row. Use this to merge predictions to rows.
- gender: Messy categorical indicators (mapped during preparation to normalized categories).
- age: Age in years (may contain missing values and outliers corrected to a plausible range).
- country: Country of residence.
- language: Primary language spoken (correlated with country but not identical).
- primary_skill: Primary freelance domain (e.g., Web Development, Data Analysis, AI, UI/UX Design, Graphic Design, Cybersecurity, DevOps, Blockchain Development, Mobile Apps).
- years_of_experience: Years of professional experience.
- rating: Client rating on a 1.0–5.0 scale (may include zeros and missing values).
- is_active: Platform activity status normalized to 0/1.
- client_satisfaction: Satisfaction score on a 0–100 scale.
- hourly_rate_usd: Target variable (only in train.csv). The test set does not include this column.

Important notes
- The data contains messy formatting and missing values. Effective preprocessing is expected (e.g., mapping gender variants, parsing boolean and percentage fields, handling missing values, and normalizing text case).
- The column hourly_rate_usd is the prediction target in train.csv and must not be used as a feature. The same column is absent from test.csv.
- The row_id column is the only column required in the submission along with the predicted hourly_rate_usd.

Submission format
- A valid submission is a CSV file with exactly two columns and the same number of rows as test.csv:
  - row_id
  - hourly_rate_usd
- The row_id values must match exactly those provided in test.csv.

Evaluation metric
- Mean Absolute Error (MAE): the average absolute difference between your predictions and the ground truth hourly_rate_usd. Lower MAE is better. MAE directly reflects the average dollar error and is robust to outliers while remaining interpretable.

Modeling guidance
- You are encouraged to perform feature engineering, including (but not limited to):
  - Categorical encodings for gender, country, language, and primary_skill
  - Numeric transformations and scaling for age, years_of_experience, rating, and client_satisfaction
  - Interaction features (e.g., country-skill combinations)
- Reasonable approaches include linear models with regularization, tree-based ensembles (e.g., random forests, gradient boosting), and tabular neural networks.

Final files provided
- train.csv
- test.csv
- sample_submission.csv

Good luck building robust pipelines that turn messy tabular data into accurate predictions!
