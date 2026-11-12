# OpenMLE-fast task

Task ID: `alzheimers-disease-risk-us-machine-learning-enc@1`

Native metric: `AlzheimerRiskRegressionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2856 bytes)
- `data/sample_submission.csv` (883501 bytes); columns: ["Id", "Data_Value"]
- `data/test.csv` (5318618 bytes); columns: ["Id", "QuestionCode_at_risk_pneumococcal_vaccine_ever", "QuestionCode_binge_drinking_past_30d", "QuestionCode_care_20plus_hours_per_week", "QuestionCode_cholesterol_screen_5yrs", "QuestionCode_colorectal_screening_upto_date", "QuestionCode_current_obesity_bmi_30plus", "QuestionCode_current_smoker_ever_100cigs", "QuestionCode_eat_2plus_fruits_daily", "QuestionCode_eat_3plus_vegetables_daily", "QuestionCode_ever_diagnosed_arthritis", "QuestionCode_ever_told_high_blood_pressure", "QuestionCode_fair_or_poor_health_with_arthritis", "QuestionCode_fall_injury_past_year", "QuestionCode_flu_vaccine_past_year", "QuestionCode_freq_mental_distress", "QuestionCode_lifetime_depression_diagnosis", "QuestionCode_lost_5_or_fewer_teeth", "QuestionCode_men_up_to_date_clinical_prevention", "QuestionCode_no_diabetes_test_within_3yrs", "QuestionCode_no_leisure_time_physical_activity", "QuestionCode_not_currently_care_expect_care_2yrs", "QuestionCode_on_bp_meds_if_high_bp", "QuestionCode_physically_unhealthy_days_mean", "QuestionCode_provided_care_6months_plus", "QuestionCode_provided_care_dementia_past_month", "QuestionCode_provided_care_past_month", "QuestionCode_reported_disability_sensory_mobility", "QuestionCode_scd_discussed_with_provider", "QuestionCode_scd_interferes_social_household", "QuestionCode_scd_needs_daily_assistance", "QuestionCode_scd_worsening_past_year", "QuestionCode_self_reported_fair_or_poor_health", "QuestionCode_self_reported_good_or_better_health", "QuestionCode_severe_joint_pain_with_arthritis", "QuestionCode_sufficient_sleep_over_6h", "QuestionCode_women_mammogram_2yrs", "QuestionCode_women_paptest_3yrs", "QuestionCode_women_up_to_date_clinical_prevention", "QuestionCode_nan", "StratificationCategory1_nan", "Stratification1_65 years or older", "Stratification1_Overall", "Stratification1_nan", "StratificationCategory2_Sex", "StratificationCategory2_nan", "Stratification2_Black, non-Hispanic", "Stratification2_Female", "Stratification2_Hispanic", "Stratification2_Male", "Stratification2_Native Am/Alaskan Native", "Stratification2_White, non-Hispanic", "Stratification2_nan", "LocationDesc_code", "Class_code", "question"]
- `data/train.csv` (21149296 bytes); columns: ["Data_Value", "QuestionCode_at_risk_pneumococcal_vaccine_ever", "QuestionCode_binge_drinking_past_30d", "QuestionCode_care_20plus_hours_per_week", "QuestionCode_cholesterol_screen_5yrs", "QuestionCode_colorectal_screening_upto_date", "QuestionCode_current_obesity_bmi_30plus", "QuestionCode_current_smoker_ever_100cigs", "QuestionCode_eat_2plus_fruits_daily", "QuestionCode_eat_3plus_vegetables_daily", "QuestionCode_ever_diagnosed_arthritis", "QuestionCode_ever_told_high_blood_pressure", "QuestionCode_fair_or_poor_health_with_arthritis", "QuestionCode_fall_injury_past_year", "QuestionCode_flu_vaccine_past_year", "QuestionCode_freq_mental_distress", "QuestionCode_lifetime_depression_diagnosis", "QuestionCode_lost_5_or_fewer_teeth", "QuestionCode_men_up_to_date_clinical_prevention", "QuestionCode_no_diabetes_test_within_3yrs", "QuestionCode_no_leisure_time_physical_activity", "QuestionCode_not_currently_care_expect_care_2yrs", "QuestionCode_on_bp_meds_if_high_bp", "QuestionCode_physically_unhealthy_days_mean", "QuestionCode_provided_care_6months_plus", "QuestionCode_provided_care_dementia_past_month", "QuestionCode_provided_care_past_month", "QuestionCode_reported_disability_sensory_mobility", "QuestionCode_scd_discussed_with_provider", "QuestionCode_scd_interferes_social_household", "QuestionCode_scd_needs_daily_assistance", "QuestionCode_scd_worsening_past_year", "QuestionCode_self_reported_fair_or_poor_health", "QuestionCode_self_reported_good_or_better_health", "QuestionCode_severe_joint_pain_with_arthritis", "QuestionCode_sufficient_sleep_over_6h", "QuestionCode_women_mammogram_2yrs", "QuestionCode_women_paptest_3yrs", "QuestionCode_women_up_to_date_clinical_prevention", "QuestionCode_nan", "StratificationCategory1_nan", "Stratification1_65 years or older", "Stratification1_Overall", "Stratification1_nan", "StratificationCategory2_Sex", "StratificationCategory2_nan", "Stratification2_Black, non-Hispanic", "Stratification2_Female", "Stratification2_Hispanic", "Stratification2_Male", "Stratification2_Native Am/Alaskan Native", "Stratification2_White, non-Hispanic", "Stratification2_nan", "LocationDesc_code", "Class_code", "question"]

## Public description

US Cognitive Health Indicators Estimation (Grouped-Normalized Regression)

Problem statement
- Predict Data_Value (a percentage or mean days in [0,100]) for population health indicators among older U.S. adults. Each row represents one indicator (question) measured for a specific location and demographic stratum.
- Participants must build models that generalize across indicators, demographics, and locations.

Data description
- Target: Data_Value (float in [0,100]).
- Features:
  - Question identity flags: all columns starting with QuestionCode_. Exactly one is 1 per row in the provided data.
  - Stratification 1: Stratification1_65 years or older, Stratification1_Overall.
  - Stratification 2: Stratification2_Female, Stratification2_Male, Stratification2_White, non-Hispanic, Stratification2_Black, non-Hispanic, Stratification2_Hispanic, Stratification2_Native Am/Alaskan Native.
  - Location: LocationDesc_code (categorical state/area code).
- Additionally provided convenience field: question (categorical), the collapsed identity derived from QuestionCode_* columns. You may ignore it and use the one-hot flags directly.
- Rows with ambiguous question identity were removed during preparation to ensure exactly one indicator per row.

Files
- train.csv: Training rows with features and Data_Value.
- test.csv: Test rows with features only. Includes an Id column used for submissions.
- sample_submission.csv: Expected submission format with random but valid predictions for the Ids in test.csv.

Submission format
- CSV with two columns: Id, Data_Value
- One row per Id in test.csv. Do not add, remove, or reorder Ids (order-insensitive scoring; Ids must match exactly).

Evaluation
- Metric: Group-normalized RMSE (GNRMSE) by indicator.
  - For each indicator question q, compute RMSE on its test rows.
  - Normalize by the training-set standard deviation σ_q of Data_Value for that question.
  - The final score is the mean over questions: score = mean_q RMSE_q / (σ_q + ε), with ε=1e-6 to avoid division by zero. Predictions are clipped to [0,100] before scoring.
- Rationale: Different indicators have different variances and natural scales; per-question normalization yields a fair comparison and rewards models that perform well across all indicators.

Split protocol
- Deterministic 80/20 split per indicator question, preserving representation across demographics and locations as much as possible. Each question appears in both train and test.

Modeling notes
- Treat LocationDesc_code and stratification columns as categorical. The QuestionCode_* one-hot flags encode the target indicator identity; models can learn per-indicator patterns and hierarchical structure.
- Clip predictions to [0,100] to respect the target’s domain.
- Useful baselines include per-question means and hierarchical smoothing across location/strata.
