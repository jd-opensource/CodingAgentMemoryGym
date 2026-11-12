# OpenMLE-fast task

Task ID: `temperature-controlled-drying-system-dataset@1`

Native metric: `PreheatingEnergyMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2627 bytes)
- `data/sample_submission.csv` (11982 bytes); columns: ["Batch_ID", "Energy_Consumed"]
- `data/test.csv` (29995 bytes); columns: ["Batch_ID", "Start_Temp", "Target_Temp", "Ambient_Temp", "Airflow_Rate", "Humidity_Level", "Material_Load", "Fan_Speed", "Heater_Power_Level", "Control_Strategy"]
- `data/train.csv` (75079 bytes); columns: ["Batch_ID", "Start_Temp", "Target_Temp", "Ambient_Temp", "Airflow_Rate", "Humidity_Level", "Material_Load", "Fan_Speed", "Heater_Power_Level", "Control_Strategy", "Energy_Consumed"]

## Public description

Energy-Efficient Preheating Prediction

Problem statement
Industrial fluid bed dryers must preheat materials to target temperatures under varying ambient conditions and loads. Energy consumption during preheating directly impacts cost and sustainability. Your task is to predict Energy_Consumed (kWh equivalent) for each preheating run using process inputs known before and at the start of control execution.

Data description
You are provided with a tabular dataset of preheating operations with the following usable inputs:
- Batch_ID: identifier for each run (used only to link predictions to rows)
- Start_Temp, Target_Temp, Ambient_Temp: initial and target temperatures, ambient conditions
- Airflow_Rate, Fan_Speed: operational airflow parameters
- Humidity_Level, Material_Load: environmental and material-specific influences
- Heater_Power_Level: heating intensity level
- Control_Strategy: categorical label indicating applied control logic (e.g., PID, Fixed-Time, FA-PID-LSSVM)

Fields excluded from modeling due to leakage and not present in the training features:
- Preheating_Time, Temp_Fluctuation_Index, Steady_State_Achieved

Files
- train.csv: features and the target Energy_Consumed
- test.csv: features only; you must predict Energy_Consumed for these rows
- sample_submission.csv: example submission format with placeholder predictions

Submission format
- CSV file with two columns: Batch_ID,Energy_Consumed
- Include predictions for all and only the Batch_IDs in the test set
- Energy_Consumed must be numeric and finite

Evaluation
- Metric: Mean Absolute Error (MAE) on Energy_Consumed over the test set
- MAE is chosen for interpretability in physical units and fairness (equal penalty for over/under prediction), and is robust to outliers

Guidance and expectations
- Use the full training data—no subsampling is necessary
- Apply sound preprocessing: type casting, handling missing values if present, encoding of Control_Strategy (e.g., one-hot)
- Feature engineering is encouraged, e.g., delta_temp = Target_Temp − Start_Temp, energy intensity interactions (Heater_Power_Level × delta_temp), and non-linear transforms
- Model training: any regression-capable ML model is allowed (e.g., gradient boosting, random forests, regularized linear models, neural networks)
- Evaluation: consider cross-validation on train.csv to select hyperparameters; report performance using MAE

Fairness and difficulty
- The split is stratified by Control_Strategy to preserve its distribution
- The problem is nonlinear and requires thoughtful feature engineering, but remains solvable with tabular ML techniques
