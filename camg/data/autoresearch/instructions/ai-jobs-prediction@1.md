# OpenMLE-fast task

Task ID: `ai-jobs-prediction@1`

Native metric: `AIJobSalaryMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4276 bytes)
- `data/sample_submission.csv` (79051 bytes); columns: ["job_id", "salary_usd"]
- `data/test.csv` (497319 bytes); columns: ["job_id", "job_title", "salary_currency", "experience_level", "employment_type", "company_location", "company_size", "employee_residence", "remote_ratio", "required_skills", "education_required", "years_experience", "industry", "posting_date", "application_deadline", "job_description_length", "benefits_score", "company_name"]
- `data/train.csv` (2062566 bytes); columns: ["job_id", "job_title", "salary_usd", "salary_currency", "experience_level", "employment_type", "company_location", "company_size", "employee_residence", "remote_ratio", "required_skills", "education_required", "years_experience", "industry", "posting_date", "application_deadline", "job_description_length", "benefits_score", "company_name"]

## Public description

```
description.txt (51 lines)
sample_submission.csv (3001 lines)
test.csv (3001 lines)
train.csv (12001 lines)```

-> sample_submission.csv has 3000 rows and 2 columns.
Here is some information about the columns:
job_id (object) has 3000 unique values. Some example values: ['AI04203', 'AI01671', 'AI13380', 'AI10235']
salary_usd (float64) has range: 14749.68 - 462863.78, 0 nan values

-> test.csv has 3000 rows and 18 columns.
Here is some information about the columns:
application_deadline (object) has 529 unique values. Some example values: ['2025-01-05', '2024-10-31', '2024-06-28', '2025-04-23']
benefits_score (float64) has range: 5.00 - 10.00, 0 nan values
company_location (object) has 20 unique values. Some example values: ['Germany', 'China', 'Netherlands', 'France']
company_name (object) has 16 unique values. Some example values: ['Cloud AI Solutions', 'Advanced Robotics', 'Future Systems', 'Autonomous Tech']
company_size (object) has 3 unique values: ['L', 'M', 'S']
education_required (object) has 4 unique values: ['Bachelor', 'Associate', 'PhD', 'Master']
employee_residence (object) has 20 unique values. Some example values: ['Germany', 'France', 'Denmark', 'Ireland']
employment_type (object) has 4 unique values: ['CT', 'FL', 'PT', 'FT']
experience_level (object) has 4 unique values: ['EN', 'EX', 'SE', 'MI']
industry (object) has 15 unique values. Some example values: ['Automotive', 'Finance', 'Technology', 'Real Estate']
job_description_length (int64) has range: 500.00 - 2499.00, 0 nan values
job_id (object) has 3000 unique values. Some example values: ['AI04203', 'AI01671', 'AI13380', 'AI10235']
job_title (object) has 20 unique values. Some example values: ['Autonomous Systems Engineer', 'NLP Engineer', 'Data Analyst', 'Computer Vision Engineer']
posting_date (object) has 486 unique values. Some example values: ['2024-04-12', '2024-05-24', '2024-06-26', '2024-04-08']
remote_ratio (int64) has 3 unique values: [0, 50, 100]
required_skills (object) has 2943 unique values. Some example values: ['Python, TensorFlow, PyTorch', 'Kubernetes, Linux, Python', 'Docker, Python, Deep Learning', 'Spark, Kubernetes, Tableau']
salary_currency (object) has 3 unique values: ['USD', 'EUR', 'GBP']
years_experience (int64) has range: 0.00 - 19.00, 0 nan values

-> train.csv has 12000 rows and 19 columns.
Here is some information about the columns:
application_deadline (object) has 542 unique values. Some example values: ['2025-01-04', '2024-12-28', '2024-07-22', '2025-04-07']
benefits_score (float64) has range: 5.00 - 10.00, 0 nan values
company_location (object) has 20 unique values. Some example values: ['Austria', 'Germany', 'Denmark', 'Canada']
company_name (object) has 16 unique values. Some example values: ['TechCorp Inc', 'AI Innovations', 'Cognitive Computing', 'Digital Transformation LLC']
company_size (object) has 3 unique values: ['M', 'S', 'L']
education_required (object) has 4 unique values: ['Master', 'PhD', 'Associate', 'Bachelor']
employee_residence (object) has 20 unique values. Some example values: ['Sweden', 'Austria', 'India', 'Canada']
employment_type (object) has 4 unique values: ['FT', 'PT', 'CT', 'FL']
experience_level (object) has 4 unique values: ['SE', 'EX', 'EN', 'MI']
industry (object) has 15 unique values. Some example values: ['Retail', 'Media', 'Consulting', 'Gaming']
job_description_length (int64) has range: 500.00 - 2499.00, 0 nan values
job_id (object) has 12000 unique values. Some example values: ['AI00798', 'AI00756', 'AI10201', 'AI08292']
job_title (object) has 20 unique values. Some example values: ['Machine Learning Researcher', 'AI Software Engineer', 'Machine Learning Engineer', 'Robotics Engineer']
posting_date (object) has 486 unique values. Some example values: ['2024-07-05', '2025-04-05', '2024-05-25', '2024-08-25']
remote_ratio (int64) has 3 unique values: [100, 0, 50]
required_skills (object) has 11058 unique values. Some example values: ['Python, TensorFlow, PyTorch', 'Python, TensorFlow, Tableau', 'Python, TensorFlow, Linux', 'Python, TensorFlow, Data Visualization']
salary_currency (object) has 3 unique values: ['USD', 'EUR', 'GBP']
salary_usd (int64) has range: 32519.00 - 399095.00, 0 nan values
years_experience (int64) has range: 0.00 - 19.00, 0 nan values
