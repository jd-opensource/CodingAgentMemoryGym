# OpenMLE-fast task

Task ID: `human-cognitive-performance-analysis@2`

Native metric: `CognitivePerformanceMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2524 bytes)
- `data/label_bins.json` (465 bytes)
- `data/sample_submission.csv` (221608 bytes); columns: ["row_id", "Cognitive_Level"]
- `data/test.csv` (772166 bytes); columns: ["row_id", "Age", "Gender", "Sleep_Duration", "Stress_Level", "Diet_Type", "Daily_Screen_Time", "Exercise_Frequency", "Caffeine_Intake"]
- `data/train.csv` (3535363 bytes); columns: ["row_id", "Age", "Gender", "Sleep_Duration", "Stress_Level", "Diet_Type", "Daily_Screen_Time", "Exercise_Frequency", "Caffeine_Intake", "Cognitive_Level"]

## Public description

Title: Ordinal Cognitive Performance from Lifestyle Only

Problem Statement
Organizations often collect lifestyle and demographic data (sleep, stress, diet, screen time, exercise, caffeine) but lack access to lab-based cognitive tests. Your challenge is to predict a person's overall cognitive performance category using only lifestyle and demographic features. The task is a 5-class ordered classification with labels: very_low, low, medium, high, very_high.

Data
You are provided with tabular files for model development and submission:
- Input features (both train and test):
  - Age (numeric)
  - Gender (categorical)
  - Sleep_Duration (hours, numeric)
  - Stress_Level (integer scale, 0-10)
  - Diet_Type (categorical: e.g., Vegan, Vegetarian, Non-Vegetarian)
  - Daily_Screen_Time (hours, numeric)
  - Exercise_Frequency (categorical: e.g., Low, Medium, High)
  - Caffeine_Intake (mg/day, numeric)
- Target (train only): Cognitive_Level (ordered class in {very_low, low, medium, high, very_high})
- Identifier: row_id (string).

Important constraints
- Only the features listed above are present and allowed as inputs. No lab measurements or model-generated scores are included in the competition files.
- The 5-class Cognitive_Level is derived from an underlying cognitive score using quantile cutoffs computed on the training set only. Those fixed cutoffs are then applied to the test set.

Files
- train.csv: row_id, features, and Cognitive_Level.
- test.csv: row_id and features (no labels).
- sample_submission.csv: row_id and Cognitive_Level.

Evaluation
Submissions are evaluated with Quadratic Weighted Kappa (QWK), which respects the ordinal nature of the labels and penalizes distant errors more than near misses. The label order is: very_low < low < medium < high < very_high.

Submission Format
- A CSV file with two columns and a header:
  - row_id
  - Cognitive_Level (one of: very_low, low, medium, high, very_high)
- The row_id values and their order must exactly match those in test.csv.

Starter Tips
- Encode categorical variables (e.g., one-hot or ordinal encodings) and consider scaling continuous features as needed.
- Nonlinear models (e.g., gradient boosting, random forests, neural networks) and ordinal methods (e.g., ordered logistic, cumulative link models) can perform well.
- Consider interaction effects (e.g., sleep x stress, screen time x exercise) and calibration for better QWK.
- Validate your pipeline to avoid leakage and ensure consistent preprocessing between train and test.
