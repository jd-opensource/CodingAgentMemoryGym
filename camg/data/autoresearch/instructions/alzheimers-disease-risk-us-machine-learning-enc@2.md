# OpenMLE-fast task

Task ID: `alzheimers-disease-risk-us-machine-learning-enc@2`

Native metric: `PopulationHealthHotspotMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3284 bytes)
- `data/sample_submission.csv` (1939024 bytes); columns: ["row_id", "probability"]
- `data/test.csv` (4743898 bytes); columns: ["row_id", "QuestionCode_at_risk_pneumococcal_vaccine_ever", "QuestionCode_binge_drinking_past_30d", "QuestionCode_care_20plus_hours_per_week", "QuestionCode_cholesterol_screen_5yrs", "QuestionCode_colorectal_screening_upto_date", "QuestionCode_current_obesity_bmi_30plus", "QuestionCode_current_smoker_ever_100cigs", "QuestionCode_eat_2plus_fruits_daily", "QuestionCode_eat_3plus_vegetables_daily", "QuestionCode_ever_diagnosed_arthritis", "QuestionCode_ever_told_high_blood_pressure", "QuestionCode_fair_or_poor_health_with_arthritis", "QuestionCode_fall_injury_past_year", "QuestionCode_flu_vaccine_past_year", "QuestionCode_freq_mental_distress", "QuestionCode_lifetime_depression_diagnosis", "QuestionCode_lost_5_or_fewer_teeth", "QuestionCode_men_up_to_date_clinical_prevention", "QuestionCode_no_diabetes_test_within_3yrs", "QuestionCode_no_leisure_time_physical_activity", "QuestionCode_not_currently_care_expect_care_2yrs", "QuestionCode_on_bp_meds_if_high_bp", "QuestionCode_physically_unhealthy_days_mean", "QuestionCode_provided_care_6months_plus", "QuestionCode_provided_care_dementia_past_month", "QuestionCode_provided_care_past_month", "QuestionCode_reported_disability_sensory_mobility", "QuestionCode_scd_discussed_with_provider", "QuestionCode_scd_interferes_social_household", "QuestionCode_scd_needs_daily_assistance", "QuestionCode_scd_worsening_past_year", "QuestionCode_self_reported_fair_or_poor_health", "QuestionCode_self_reported_good_or_better_health", "QuestionCode_severe_joint_pain_with_arthritis", "QuestionCode_sufficient_sleep_over_6h", "QuestionCode_women_mammogram_2yrs", "QuestionCode_women_paptest_3yrs", "QuestionCode_women_up_to_date_clinical_prevention", "Stratification1_65 years or older", "Stratification1_Overall", "Stratification2_Black, non-Hispanic", "Stratification2_Female", "Stratification2_Hispanic", "Stratification2_Male", "Stratification2_Native Am/Alaskan Native", "Stratification2_White, non-Hispanic", "LocationDesc_code"]
- `data/train.csv` (19267010 bytes); columns: ["row_id", "QuestionCode_at_risk_pneumococcal_vaccine_ever", "QuestionCode_binge_drinking_past_30d", "QuestionCode_care_20plus_hours_per_week", "QuestionCode_cholesterol_screen_5yrs", "QuestionCode_colorectal_screening_upto_date", "QuestionCode_current_obesity_bmi_30plus", "QuestionCode_current_smoker_ever_100cigs", "QuestionCode_eat_2plus_fruits_daily", "QuestionCode_eat_3plus_vegetables_daily", "QuestionCode_ever_diagnosed_arthritis", "QuestionCode_ever_told_high_blood_pressure", "QuestionCode_fair_or_poor_health_with_arthritis", "QuestionCode_fall_injury_past_year", "QuestionCode_flu_vaccine_past_year", "QuestionCode_freq_mental_distress", "QuestionCode_lifetime_depression_diagnosis", "QuestionCode_lost_5_or_fewer_teeth", "QuestionCode_men_up_to_date_clinical_prevention", "QuestionCode_no_diabetes_test_within_3yrs", "QuestionCode_no_leisure_time_physical_activity", "QuestionCode_not_currently_care_expect_care_2yrs", "QuestionCode_on_bp_meds_if_high_bp", "QuestionCode_physically_unhealthy_days_mean", "QuestionCode_provided_care_6months_plus", "QuestionCode_provided_care_dementia_past_month", "QuestionCode_provided_care_past_month", "QuestionCode_reported_disability_sensory_mobility", "QuestionCode_scd_discussed_with_provider", "QuestionCode_scd_interferes_social_household", "QuestionCode_scd_needs_daily_assistance", "QuestionCode_scd_worsening_past_year", "QuestionCode_self_reported_fair_or_poor_health", "QuestionCode_self_reported_good_or_better_health", "QuestionCode_severe_joint_pain_with_arthritis", "QuestionCode_sufficient_sleep_over_6h", "QuestionCode_women_mammogram_2yrs", "QuestionCode_women_paptest_3yrs", "QuestionCode_women_up_to_date_clinical_prevention", "Stratification1_65 years or older", "Stratification1_Overall", "Stratification2_Black, non-Hispanic", "Stratification2_Female", "Stratification2_Hispanic", "Stratification2_Male", "Stratification2_Native Am/Alaskan Native", "Stratification2_White, non-Hispanic", "LocationDesc_code", "label"]

## Public description

Competition: Population Health Hotspot Classification (Per-Indicator Above-Median)

Overview
You are given tabular public-health data for older adults across U.S. locations and demographic strata. Each row corresponds to an indicator × location × demographic stratum. Your goal is to predict whether a row is an above-median “hotspot” within its indicator category, using the training data to learn patterns from indicator identity, demographics, and location.

Files provided
- train.csv: Features and the binary target label.
- test.csv: Features only (with row_id). Predict probabilities for these rows.
- sample_submission.csv: Submission template with row_id and probability columns.

Features
Each row contains:
- row_id: Unique identifier for the row (string).
- Indicator identity as one-hot columns: QuestionCode_* (exactly one is 1 per row).
- Demographic stratifications:
  - Stratification1_* (e.g., 65 years or older, Overall)
  - Stratification2_* (e.g., Female, Male, White non-Hispanic, Black non-Hispanic, Hispanic, Native Am/Alaskan Native)
- LocationDesc_code: Numeric code representing the U.S. location (categorical).

Important
- The original numeric Data_Value used to define the hotspot label is not included in train.csv or test.csv to avoid leakage.
- Rows without a valid indicator (i.e., not exactly one QuestionCode_* = 1) are excluded from the competition data.

Target definition (already computed for train; used internally for evaluation on test)
- For each indicator q, the median of Data_Value is computed using only the training rows that belong to q.
- The binary label is: 1 if Data_Value > median_q_train, else 0.

Submission format
- A single CSV with exactly two columns in this order:
  - row_id: Must match the row_id values supplied in test.csv.
  - probability: A probability in [0, 1] that label = 1 for the corresponding row.
- Your submission must cover all and only the row_id values in test.csv.

Evaluation
- Metric: Macro-average ROC AUC by indicator.
  1) For each indicator q, compute ROC AUC between your submitted probabilities and the true labels on that indicator’s test rows.
  2) The final score is the unweighted mean of the per-indicator AUCs across all indicators present in the test set.
- Edge case handling: If all test labels for an indicator are the same class, that indicator’s AUC is defined as 0.5 (chance) and included in the average.
- Rationale: AUC is threshold-independent and robust to imbalance; macro-averaging gives equal weight to each indicator, ensuring fairness across heterogeneous sample sizes.

Split policy (for your understanding)
- A single deterministic train/test split preserves representation across indicators. Every indicator in test also appears in train; when both classes appear in an indicator’s test rows, both classes are also represented in training for that indicator.

Modeling guidance
- This is a tabular classification task. Strong solutions will often:
  - Use regularized linear models, tree-based ensembles, or neural networks.
  - Apply appropriate encodings for high-cardinality categorical features (e.g., target encoding or embeddings for LocationDesc_code).
  - Incorporate interactions between indicator identity and demographics.

Good luck and have fun!
