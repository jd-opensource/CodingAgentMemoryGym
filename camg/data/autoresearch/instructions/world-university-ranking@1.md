# OpenMLE-fast task

Task ID: `world-university-ranking@1`

Native metric: `WorldUniversityRankingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1870 bytes)
- `data/sample_submission.csv` (78599 bytes); columns: ["Id", "overall_score_next_year"]
- `data/test.csv` (1127408 bytes); columns: ["entity_id", "year_t", "country", "student_population", "students_to_staff_ratio", "international_students_pct", "female_male_ratio_female_share", "teaching_score", "research_environment_score", "research_quality_score", "industry_impact_score", "international_outlook_score", "overall_rank", "teaching_rank", "research_rank", "citations_rank", "industry_income_rank", "international_outlook_rank", "w_snapshot_student_population", "w_snapshot_student_staff_ratio", "w_snapshot_intl_students_pct", "w_snapshot_female_share", "subjects_offered", "Id"]
- `data/train.csv` (7246196 bytes); columns: ["entity_id", "year_t", "country", "student_population", "students_to_staff_ratio", "international_students_pct", "female_male_ratio_female_share", "teaching_score", "research_environment_score", "research_quality_score", "industry_impact_score", "international_outlook_score", "overall_rank", "teaching_rank", "research_rank", "citations_rank", "industry_income_rank", "international_outlook_rank", "w_snapshot_student_population", "w_snapshot_student_staff_ratio", "w_snapshot_intl_students_pct", "w_snapshot_female_share", "subjects_offered", "overall_score_next_year", "Id"]

## Public description

Title: Next-Year University Overall Score Forecasting

Overview
- Predict the next-year Overall Score for each institution using features up to the current year. You will train on 2011–2023 features to predict 2012–2024 scores and then forecast 2025 from 2024 features.

Data files
- train.csv: One row per institution–year t, with features and the label overall_score_next_year.
- test.csv: Same features (no label) for the 2024 cohort to predict 2025.
- sample_submission.csv: Example file containing Id and overall_score_next_year columns.

Target and submission
- Target: overall_score_next_year (continuous, roughly 0–100).
- Submission CSV with two columns:
  - Id: match exactly the Id values in test.csv (same order)
  - overall_score_next_year: your predictions as floats

Evaluation
- Root Mean Squared Error (RMSE) on overall_score_next_year.
- RMSE = sqrt(mean((prediction − ground_truth)^2)). Predictions must be finite.

Features
- Id: anonymized per institution–year sample identifier.
- entity_id: hashed institution identifier to support grouping without revealing names.
- year_t: feature year (test is 2024).
- country.
- student_population, students_to_staff_ratio, international_students_pct, female_male_ratio_female_share.
- teaching_score, research_environment_score, research_quality_score, industry_impact_score, international_outlook_score.
- overall_rank and available metric rank counterparts.
- w_snapshot_* demographic signals and subjects_offered when available.

Guidance
- Use only year t features to predict year t+1. Harmonize schema across years; handle missing values, mixed formats (percents, ratios, counts), and consider engineered features (e.g., deltas and rolling means).
- Any ML approach is allowed. Strong baselines include GBDTs and regularized regression; sequence models may help leverage temporal dynamics.
