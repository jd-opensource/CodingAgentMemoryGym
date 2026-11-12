# OpenMLE-fast task

Task ID: `student-performance-factors@1`

Native metric: `StudentPerformanceRMSEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3360 bytes)
- `data/sample_submission.csv` (30116 bytes); columns: ["row_id", "Exam_Score"]
- `data/test.csv` (129615 bytes); columns: ["row_id", "Hours_Studied", "Attendance", "Parental_Involvement", "Access_to_Resources", "Extracurricular_Activities", "Sleep_Hours", "Previous_Scores", "Motivation_Level", "Internet_Access", "Tutoring_Sessions", "Family_Income", "Teacher_Quality", "School_Type", "Peer_Influence", "Physical_Activity", "Learning_Disabilities", "Parental_Education_Level", "Distance_from_Home", "Gender"]
- `data/train.csv` (534019 bytes); columns: ["row_id", "Hours_Studied", "Attendance", "Parental_Involvement", "Access_to_Resources", "Extracurricular_Activities", "Sleep_Hours", "Previous_Scores", "Motivation_Level", "Internet_Access", "Tutoring_Sessions", "Family_Income", "Teacher_Quality", "School_Type", "Peer_Influence", "Physical_Activity", "Learning_Disabilities", "Parental_Education_Level", "Distance_from_Home", "Gender", "Exam_Score"]

## Public description

```
description.txt (45 lines)
sample_submission.csv (1323 lines)
test.csv (1323 lines)
train.csv (5286 lines)```

-> sample_submission.csv has 1322 rows and 2 columns.
Here is some information about the columns:
Exam_Score (float64) has range: 56.21 - 100.99, 0 nan values
row_id (int64) has range: 8.00 - 6603.00, 0 nan values

-> test.csv has 1322 rows and 20 columns.
Here is some information about the columns:
Access_to_Resources (object) has 3 unique values: ['Low', 'Medium', 'High']
Attendance (int64) has range: 60.00 - 100.00, 0 nan values
Distance_from_Home (object) has 3 unique values: ['Near', 'Moderate', 'Far', nan]
Extracurricular_Activities (object) has 2 unique values: ['No', 'Yes']
Family_Income (object) has 3 unique values: ['Medium', 'Low', 'High']
Gender (object) has 2 unique values: ['Male', 'Female']
Hours_Studied (int64) has range: 2.00 - 44.00, 0 nan values
Internet_Access (object) has 2 unique values: ['Yes', 'No']
Learning_Disabilities (object) has 2 unique values: ['No', 'Yes']
Motivation_Level (object) has 3 unique values: ['High', 'Low', 'Medium']
Parental_Education_Level (object) has 3 unique values: ['High School', 'Postgraduate', 'College', nan]
Parental_Involvement (object) has 3 unique values: ['Medium', 'High', 'Low']
Peer_Influence (object) has 3 unique values: ['Negative', 'Neutral', 'Positive']
Physical_Activity (int64) has 7 unique values: [5, 2, 3, 4, 1, 0, 6]
Previous_Scores (int64) has range: 50.00 - 100.00, 0 nan values
School_Type (object) has 2 unique values: ['Public', 'Private']
Sleep_Hours (int64) has 7 unique values: [7, 6, 8, 10, 9, 4, 5]
Teacher_Quality (object) has 3 unique values: ['Medium', 'High', 'Low', nan]
Tutoring_Sessions (int64) has 7 unique values: [1, 2, 0, 3, 4, 5, 6]
row_id (int64) has range: 8.00 - 6603.00, 0 nan values

-> train.csv has 5285 rows and 21 columns.
Here is some information about the columns:
Access_to_Resources (object) has 3 unique values: ['High', 'Medium', 'Low']
Attendance (int64) has range: 60.00 - 100.00, 0 nan values
Distance_from_Home (object) has 3 unique values: ['Moderate', 'Far', 'Near', nan]
Exam_Score (int64) has range: 56.00 - 101.00, 0 nan values
Extracurricular_Activities (object) has 2 unique values: ['Yes', 'No']
Family_Income (object) has 3 unique values: ['Low', 'Medium', 'High']
Gender (object) has 2 unique values: ['Female', 'Male']
Hours_Studied (int64) has range: 1.00 - 43.00, 0 nan values
Internet_Access (object) has 2 unique values: ['Yes', 'No']
Learning_Disabilities (object) has 2 unique values: ['No', 'Yes']
Motivation_Level (object) has 3 unique values: ['High', 'Medium', 'Low']
Parental_Education_Level (object) has 3 unique values: ['College', 'High School', 'Postgraduate', nan]
Parental_Involvement (object) has 3 unique values: ['Low', 'High', 'Medium']
Peer_Influence (object) has 3 unique values: ['Negative', 'Neutral', 'Positive']
Physical_Activity (int64) has 7 unique values: [5, 3, 1, 2, 4, 0, 6]
Previous_Scores (int64) has range: 50.00 - 100.00, 0 nan values
School_Type (object) has 2 unique values: ['Public', 'Private']
Sleep_Hours (int64) has 7 unique values: [8, 7, 10, 4, 6, 9, 5]
Teacher_Quality (object) has 3 unique values: ['Medium', 'High', nan, 'Low']
Tutoring_Sessions (int64) has 9 unique values: [2, 1, 0, 4, 3, 5, 6, 7, 8]
row_id (int64) has range: 0.00 - 6606.00, 0 nan values
