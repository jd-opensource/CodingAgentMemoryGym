# OpenMLE-fast task

Task ID: `jobs-dataset-from-glassdoor@1`

Native metric: `GlassdoorSalaryEstimationMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3335 bytes)
- `data/sample_submission.csv` (3218 bytes); columns: ["Id", "salary"]
- `data/test.csv` (617812 bytes); columns: ["Id", "Job Title", "Job Description", "Rating", "Company Name", "Location", "Headquarters", "Size", "Founded", "Type of ownership", "Industry", "Sector", "Revenue", "Competitors", "company_txt", "job_state", "same_state", "age", "python_yn", "R_yn", "spark", "aws", "excel", "job_simp", "seniority", "desc_len", "num_comp"]
- `data/train.csv` (2384403 bytes); columns: ["Id", "Job Title", "Job Description", "Rating", "Company Name", "Location", "Headquarters", "Size", "Founded", "Type of ownership", "Industry", "Sector", "Revenue", "Competitors", "salary", "company_txt", "job_state", "same_state", "age", "python_yn", "R_yn", "spark", "aws", "excel", "job_simp", "seniority", "desc_len", "num_comp"]

## Public description

Glassdoor Tech Salary Estimation Challenge

Problem statement
Predict the posted annual average salary (in thousands of USD per year) for a tech job posting using the job description text and non-salary metadata. You will train on examples with known annual salaries and predict salaries for a held-out test set.

Data description
You are given a single labeled training file and an unlabeled test file built from Glassdoor job postings. Each row corresponds to one job posting. The target is the posted annual average salary derived from the original salary range for that posting. Hourly postings were excluded to ensure unit consistency.

Files provided
- train.csv: Labeled training data. Includes features and the target column salary.
- test.csv: Unlabeled test data. Same features as train.csv but without the target.
- sample_submission.csv: A valid example submission with the correct format.

Target
- salary: Annual average salary in thousands of USD (float). Always positive.

Important feature notes and leakage prevention
- Features include a mix of free-text and structured metadata such as: Job Title, Job Description, Rating, Company Name, Location, Headquarters, Size, Founded, Type of ownership, Industry, Sector, Revenue, Competitors, company_txt, job_state, same_state, age, python_yn, R_yn, spark, aws, excel, job_simp, seniority, desc_len, num_comp.
- Columns that directly encode salary information (e.g., Salary Estimate text, min_salary, max_salary, hourly, employer_provided) are not included in train/test to prevent label leakage. Do not attempt to reconstruct or use any external salary text.

Evaluation
Submissions are evaluated using Root Mean Squared Logarithmic Error (RMSLE) between your predictions and the ground truth salaries:
- Let y_true be the true salary and y_pred be your prediction for a row.
- RMSLE = sqrt(mean((log1p(y_pred) - log1p(y_true))^2)).
- y_pred should be non-negative real values. Numerically, negative predictions (if any) will be clipped to 0.0 during scoring.

Submission format
- A CSV with exactly two columns and a header:
  - Id: Integer identifier matching the Id column in test.csv.
  - salary: Your predicted annual average salary (thousands USD) for each Id.
- Include every Id from test.csv exactly once; do not include any extra rows or duplicate Ids.

Modeling guidance
- Text: Job Description is high signal; typical approaches include TF-IDF (word/character n-grams) and modern NLP embeddings. desc_len may also help.
- Categorical: Encode features like Company Name, Location, Headquarters, Size, Type of ownership, Industry, Sector, Revenue, job_state, job_simp, seniority via appropriate encoders.
- Numeric: Rating, Founded (or company age), num_comp can be informative; treat -1 in Rating as missing.
- Avoid leakage: Do not use any salary-derived text or columns.

Train/test split details
- The split is a single 80/20 split over the annual-salary subset and is stratified by job_simp to balance roles across splits. The test set contains only annual postings, and all categories present in the test set also appear in the training set.

Tips
- Salaries span a wide range; RMSLE focuses on relative error and helps stabilize training.
- Consider robust preprocessing, handling of missing values, and regularization for high-dimensional text features.
