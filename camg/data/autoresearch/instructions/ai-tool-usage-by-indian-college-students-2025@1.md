# OpenMLE-fast task

Task ID: `ai-tool-usage-by-indian-college-students-2025@1`

Native metric: `AIToolsGradeImpactMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (297 bytes)
- `data/sample_submission.csv` (7598 bytes); columns: ["Id", "Impact_on_Grades"]
- `data/test.csv` (100652 bytes); columns: ["Id", "College_Name", "Stream", "Year_of_Study", "AI_Tools_Used", "Daily_Usage_Hours", "Use_Cases", "Trust_in_AI_Tools", "Do_Professors_Allow_Use", "Preferred_AI_Tool", "Awareness_Level", "Willing_to_Pay_for_Access", "State", "Device_Used", "Internet_Access"]
- `data/train.csv` (409231 bytes); columns: ["Id", "College_Name", "Stream", "Year_of_Study", "AI_Tools_Used", "Daily_Usage_Hours", "Use_Cases", "Trust_in_AI_Tools", "Impact_on_Grades", "Do_Professors_Allow_Use", "Preferred_AI_Tool", "Awareness_Level", "Willing_to_Pay_for_Access", "State", "Device_Used", "Internet_Access"]

## Public description

Title: AI Tools & Academic Outcomes: Ordinal Grade Impact Prediction

Files:
- train.csv
- test.csv
- sample_submission.csv

Submission format:
- CSV with two columns: Id, Impact_on_Grades
- Impact_on_Grades is an integer in [-5, 5]

Evaluation:
- Quadratic Weighted Kappa (QWK) on classes [-5..5]
