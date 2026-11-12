# OpenMLE-fast task

Task ID: `global-ai-job-market-and-salary-trends-2025@1`

Native metric: `GlobalAISalaryRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4621 bytes)
- `data/sample_submission.csv` (151850 bytes); columns: ["job_id", "salary_usd"]
- `data/test.csv` (1085461 bytes); columns: ["application_deadline", "benefits_score", "company_location", "company_name", "company_size", "education_required", "employee_residence", "employment_type", "experience_level", "industry", "job_description_length", "job_id", "job_title", "posting_date", "remote_ratio", "required_skills", "salary_currency", "years_experience", "source"]
- `data/train.csv` (4545983 bytes); columns: ["application_deadline", "benefits_score", "company_location", "company_name", "company_size", "education_required", "employee_residence", "employment_type", "experience_level", "industry", "job_description_length", "job_id", "job_title", "posting_date", "remote_ratio", "required_skills", "salary_currency", "years_experience", "source", "salary_usd"]

## Public description

```
description.txt (68 lines)
sample_submission.csv (5956 lines)
test.csv (5956 lines)
train.csv (24046 lines)```

-> sample_submission.csv has 5955 rows and 2 columns.
Here is some information about the columns:
job_id (object) has 5955 unique values. Some example values: ['dataset_AI14821', 'dataset1_AI01022', 'dataset1_AI02112', 'dataset1_AI12129']
salary_usd (float64) has 1 unique values: [102994.0]

-> test.csv has 5955 rows and 19 columns.
Here is some information about the columns:
application_deadline (object) has 156 unique values. Some example values: ['2025-04-07', '2025-05-12', '2025-04-11', '2025-04-19']
benefits_score (float64) has range: 5.00 - 10.00, 0 nan values
company_location (object) has 20 unique values. Some example values: ['Ireland', 'Germany', 'Israel', 'India']
company_name (object) has 16 unique values. Some example values: ['Future Systems', 'Machine Intelligence Group', 'DataVision Ltd', 'AI Innovations']
company_size (object) has 3 unique values: ['M', 'L', 'S']
education_required (object) has 4 unique values: ['Associate', 'Bachelor', 'Master', 'PhD']
employee_residence (object) has 50 unique values. Some example values: ['India', 'Norway', 'Sweden', 'Germany']
employment_type (object) has 4 unique values: ['FT', 'CT', 'PT', 'FL']
experience_level (object) has 4 unique values: ['SE', 'EN', 'MI', 'EX']
industry (object) has 15 unique values. Some example values: ['Automotive', 'Media', 'Retail', 'Real Estate']
job_description_length (int64) has range: 500.00 - 2499.00, 0 nan values
job_id (object) has 5955 unique values. Some example values: ['dataset_AI14821', 'dataset1_AI01022', 'dataset1_AI02112', 'dataset1_AI12129']
job_title (object) has 20 unique values. Some example values: ['Autonomous Systems Engineer', 'Principal Data Scientist', 'Machine Learning Engineer', 'Robotics Engineer']
posting_date (object) has 98 unique values. Some example values: ['2025-04-16', '2025-03-11', '2025-02-04', '2025-01-26']
remote_ratio (int64) has 3 unique values: [0, 50, 100]
required_skills (object) has 5705 unique values. Some example values: ['Python, TensorFlow, AWS', 'Python, TensorFlow, PyTorch', 'PyTorch, Java, TensorFlow', 'Python, TensorFlow, Data Visualization']
salary_currency (object) has 8 unique values: ['CHF', 'USD', 'EUR', 'JPY', 'AUD', 'CAD', 'GBP', 'SGD']
source (object) has 2 unique values: ['dataset1', 'dataset']
years_experience (int64) has range: 0.00 - 19.00, 0 nan values

-> train.csv has 24045 rows and 20 columns.
Here is some information about the columns:
application_deadline (object) has 445 unique values. Some example values: ['2024-10-07', '2024-11-24', '2024-12-28', '2025-02-05']
benefits_score (float64) has range: 5.00 - 10.00, 0 nan values
company_location (object) has 20 unique values. Some example values: ['Switzerland', 'China', 'Canada', 'United Kingdom']
company_name (object) has 16 unique values. Some example values: ['Digital Transformation LLC', 'Quantum Computing Inc', 'TechCorp Inc', 'Cognitive Computing']
company_size (object) has 3 unique values: ['L', 'S', 'M']
education_required (object) has 4 unique values: ['Associate', 'Master', 'Bachelor', 'PhD']
employee_residence (object) has 50 unique values. Some example values: ['China', 'France', 'Switzerland', 'United Kingdom']
employment_type (object) has 4 unique values: ['FL', 'FT', 'CT', 'PT']
experience_level (object) has 4 unique values: ['EN', 'EX', 'SE', 'MI']
industry (object) has 15 unique values. Some example values: ['Consulting', 'Government', 'Telecommunications', 'Retail']
job_description_length (int64) has range: 500.00 - 2499.00, 0 nan values
job_id (object) has 24045 unique values. Some example values: ['dataset_AI11996', 'dataset1_AI00746', 'dataset1_AI01561', 'dataset1_AI01878']
job_title (object) has 20 unique values. Some example values: ['Machine Learning Engineer', 'Computer Vision Engineer', 'AI Product Manager', 'Machine Learning Researcher']
posting_date (object) has 388 unique values. Some example values: ['2024-08-25', '2024-08-28', '2024-10-15', '2024-04-08']
remote_ratio (int64) has 3 unique values: [100, 50, 0]
required_skills (object) has 21091 unique values. Some example values: ['Python, TensorFlow, PyTorch', 'Python, TensorFlow, Tableau', 'Python, TensorFlow, Data Visualization', 'Python, Git, TensorFlow']
salary_currency (object) has 8 unique values: ['USD', 'CAD', 'CHF', 'EUR', 'AUD', 'JPY', 'SGD', 'GBP']
salary_usd (int64) has range: 16975.00 - 410273.00, 0 nan values
source (object) has 2 unique values: ['dataset1', 'dataset']
years_experience (int64) has range: 0.00 - 19.00, 0 nan values
