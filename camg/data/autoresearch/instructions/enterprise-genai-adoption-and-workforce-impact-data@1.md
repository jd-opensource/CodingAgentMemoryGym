# OpenMLE-fast task

Task ID: `enterprise-genai-adoption-and-workforce-impact-data@1`

Native metric: `GenAIProductivityImpactMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3091 bytes)
- `data/sample_submission.csv` (335201 bytes); columns: ["Id", "Productivity Change (%)"]
- `data/test.csv` (3145053 bytes); columns: ["Id", "Industry", "Country", "GenAI Tool", "Adoption Year", "Number of Employees Impacted", "New Roles Created", "Training Hours Provided", "Employee Sentiment"]
- `data/train.csv` (12958494 bytes); columns: ["Id", "Industry", "Country", "GenAI Tool", "Adoption Year", "Number of Employees Impacted", "New Roles Created", "Training Hours Provided", "Employee Sentiment", "Productivity Change (%)"]

## Public description

```
description.txt (50 lines)
sample_submission.csv (20001 lines)
test.csv (20001 lines)
train.csv (80001 lines)```

-> sample_submission.csv has 20000 rows and 2 columns.
Here is some information about the columns:
Id (object) has 20000 unique values. Some example values: ['EGAI_094593', 'EGAI_061191', 'EGAI_023903', 'EGAI_010716']
Productivity Change (%) (float64) has range: 2.00 - 35.00, 0 nan values

-> test.csv has 20000 rows and 9 columns.
Here is some information about the columns:
Adoption Year (int64) has 3 unique values: [2024, 2022, 2023]
Country (object) has 14 unique values. Some example values: ['Brazil', 'Australia', 'South Korea', 'Canada']
Employee Sentiment (object) has 100 unique values. Some example values: ["We now finish tasks faster, but some older employees are struggling. Overall, it's a big shift.", 'New roles are exciting; transition was smoother than expected. Managers were initially skeptical.', 'Our workflows have improved drastically with generative AI. It changed how we communicate internally.', 'Collaboration improved; documentation and meetings are more efficient. HR hosted webinars weekly.']
GenAI Tool (object) has 6 unique values: ['Groq', 'ChatGPT', 'Claude', 'Mixtral', 'Gemini', 'LLaMA']
Id (object) has 20000 unique values. Some example values: ['EGAI_094593', 'EGAI_061191', 'EGAI_023903', 'EGAI_010716']
Industry (object) has 14 unique values. Some example values: ['Healthcare', 'Advertising', 'Education', 'Entertainment']
New Roles Created (int64) has range: 1.00 - 30.00, 0 nan values
Number of Employees Impacted (int64) has range: 101.00 - 20000.00, 0 nan values
Training Hours Provided (int64) has range: 500.00 - 25000.00, 0 nan values

-> train.csv has 80000 rows and 10 columns.
Here is some information about the columns:
Adoption Year (int64) has 3 unique values: [2023, 2022, 2024]
Country (object) has 14 unique values. Some example values: ['Brazil', 'Australia', 'Canada', 'South Korea']
Employee Sentiment (object) has 100 unique values. Some example values: ["Collaboration improved; documentation and meetings are more efficient. Overall, it's a big shift.", 'Mixed responses—management excited, staff feel uncertain. Internal newsletters now highlight AI use cases.', 'Collaboration improved; documentation and meetings are more efficient. It changed how we communicate internally.', 'New roles are exciting; transition was smoother than expected. HR hosted webinars weekly.']
GenAI Tool (object) has 6 unique values: ['LLaMA', 'Mixtral', 'ChatGPT', 'Groq', 'Claude', 'Gemini']
Id (object) has 80000 unique values. Some example values: ['EGAI_039744', 'EGAI_066937', 'EGAI_085817', 'EGAI_041797']
Industry (object) has 14 unique values. Some example values: ['Healthcare', 'Advertising', 'Entertainment', 'Education']
New Roles Created (int64) has range: 1.00 - 30.00, 0 nan values
Number of Employees Impacted (int64) has range: 100.00 - 20000.00, 0 nan values
Productivity Change (%) (float64) has range: 2.00 - 35.00, 0 nan values
Training Hours Provided (int64) has range: 500.00 - 24999.00, 0 nan values
