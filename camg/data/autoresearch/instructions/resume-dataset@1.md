# OpenMLE-fast task

Task ID: `resume-dataset@1`

Native metric: `ResumeRankingMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (875 bytes)
- `data/sample_submission.csv` (59550 bytes); columns: ["id", "matched_score"]
- `data/test.csv` (3373588 bytes); columns: ["address", "career_objective", "skills", "educational_institution_name", "degree_names", "passing_years", "educational_results", "result_types", "major_field_of_studies", "professional_company_names", "company_urls", "start_dates", "end_dates", "related_skils_in_job", "positions", "locations", "responsibilities", "extra_curricular_activity_types", "extra_curricular_organization_names", "extra_curricular_organization_links", "role_positions", "languages", "proficiency_levels", "certification_providers", "certification_skills", "online_links", "issue_dates", "expiry_dates", "job_position_name", "educationaL_requirements", "experiencere_requirement", "age_requirement", "responsibilities.1", "skills_required", "id"]
- `data/train.csv` (13728346 bytes); columns: ["address", "career_objective", "skills", "educational_institution_name", "degree_names", "passing_years", "educational_results", "result_types", "major_field_of_studies", "professional_company_names", "company_urls", "start_dates", "end_dates", "related_skils_in_job", "positions", "locations", "responsibilities", "extra_curricular_activity_types", "extra_curricular_organization_names", "extra_curricular_organization_links", "role_positions", "languages", "proficiency_levels", "certification_providers", "certification_skills", "online_links", "issue_dates", "expiry_dates", "job_position_name", "educationaL_requirements", "experiencere_requirement", "age_requirement", "responsibilities.1", "skills_required", "matched_score", "id"]

## Public description

```
description.txt (44 lines)
sample_submission.csv (1905 lines)
test.csv (43385 lines)
train.csv (174089 lines)```

-> sample_submission.csv has 1904 rows and 2 columns.
The columns are: id, matched_score

-> test.csv has 1904 rows and 35 columns.
The columns are: address, career_objective, skills, educational_institution_name, degree_names, passing_years, educational_results, result_types, major_field_of_studies, professional_company_names, company_urls, start_dates, end_dates, related_skils_in_job, positions... and 20 more columns

-> train.csv has 7640 rows and 36 columns.
The columns are: address, career_objective, skills, educational_institution_name, degree_names, passing_years, educational_results, result_types, major_field_of_studies, professional_company_names, company_urls, start_dates, end_dates, related_skils_in_job, positions... and 21 more columns
