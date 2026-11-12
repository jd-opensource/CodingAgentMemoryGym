# OpenMLE-fast task

Task ID: `car-accident-dataset@1`

Native metric: `RoadAccidentSeverityMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (5735 bytes)
- `data/sample_submission.csv` (1811077 bytes); columns: ["row_id", "Accident_Severity"]
- `data/test.csv` (20016882 bytes); columns: ["row_id", "Accident Date", "Day_of_Week", "Junction_Control", "Junction_Detail", "Latitude", "Light_Conditions", "Local_Authority_(District)", "Carriageway_Hazards", "Longitude", "Number_of_Vehicles", "Police_Force", "Road_Surface_Conditions", "Road_Type", "Speed_limit", "Time", "Urban_or_Rural_Area", "Weather_Conditions", "Vehicle_Type"]
- `data/train.csv` (21263113 bytes); columns: ["Accident Date", "Day_of_Week", "Junction_Control", "Junction_Detail", "Latitude", "Light_Conditions", "Local_Authority_(District)", "Carriageway_Hazards", "Longitude", "Number_of_Vehicles", "Police_Force", "Road_Surface_Conditions", "Road_Type", "Speed_limit", "Time", "Urban_or_Rural_Area", "Weather_Conditions", "Vehicle_Type", "Accident_Severity"]

## Public description

```
description.txt (41 lines)
sample_submission.csv (94745 lines)
test.csv (94745 lines)
train.csv (102901 lines)```

-> sample_submission.csv has 94744 rows and 2 columns.
Here is some information about the columns:
Accident_Severity (object) has 3 unique values: ['Slight', 'Serious', 'Fatal']
row_id (object) has 94744 unique values. Some example values: ['RID_0094743', 'RID_0000000', 'RID_0000001', 'RID_0000002']

-> test.csv has 94744 rows and 19 columns.
Here is some information about the columns:
Accident Date (object) has 365 unique values. Some example values: ['10/1/2022', '2/1/2022', '9/29/2022', '11/19/2022']
Carriageway_Hazards (object) has 5 unique values: [nan, 'Any animal in carriageway (except ridden horse)', 'Pedestrian in carriageway - not injured', 'Other object on road', 'Vehicle load on road', 'Previous accident']
Day_of_Week (object) has 7 unique values: ['Friday', 'Tuesday', 'Sunday', 'Thursday', 'Saturday', 'Monday', 'Wednesday']
Junction_Control (object) has 7 unique values: ['Give way or uncontrolled', 'Data missing or out of range', 'Not at junction or within 20 metres', 'Auto traffic signal', 'Authorised person', 'Stop sign', 'Auto traffic sigl']
Junction_Detail (object) has 9 unique values: ['Roundabout', 'Not at junction or within 20 metres', 'T or staggered junction', 'Crossroads', 'Mini-roundabout', 'Private drive or entrance', 'More than 4 arms (not roundabout)', 'Slip road', 'Other junction']
Latitude (float64) has range: 49.92 - 60.45, 0 nan values
Light_Conditions (object) has 5 unique values: ['Daylight', 'Darkness - no lighting', 'Darkness - lights lit', 'Darkness - lights unlit', 'Darkness - lighting unknown']
Local_Authority_(District) (object) has 238 unique values. Some example values: ['Birmingham', 'Manchester', 'Westminster', 'Cornwall']
Longitude (float64) has range: -7.52 - 1.76, 0 nan values
Number_of_Vehicles (int64) has range: 1.00 - 19.00, 0 nan values
Police_Force (object) has 30 unique values. Some example values: ['Metropolitan Police', 'West Midlands', 'Thames Valley', 'Greater Manchester']
Road_Surface_Conditions (object) has 5 unique values: ['Wet or damp', 'Dry', 'Frost or ice', 'Snow', 'Flood over 3cm. deep', nan]
Road_Type (object) has 5 unique values: ['Dual carriageway', 'Single carriageway', 'Roundabout', 'One way street', 'Slip road', nan]
Speed_limit (int64) has 7 unique values: [40, 60, 30, 50, 20, 70, 10]
Time (object) has 1439 unique values. Some example values: ['17:00', '17:30', '18:00', '16:00']
Urban_or_Rural_Area (object) has 2 unique values: ['Urban', 'Rural']
Vehicle_Type (object) has 15 unique values. Some example values: ['Car', 'Van / Goods 3.5 tonnes mgw or under', 'Motorcycle over 500cc', 'Bus or coach (17 or more pass seats)']
Weather_Conditions (object) has 8 unique values: ['Fine no high winds', 'Snowing no high winds', 'Fog or mist', 'Raining no high winds', 'Other', 'Raining + high winds', 'Fine + high winds', 'Snowing + high winds', nan]
row_id (object) has 94744 unique values. Some example values: ['RID_0094743', 'RID_0000000', 'RID_0000001', 'RID_0000002']

-> train.csv has 102900 rows and 19 columns.
Here is some information about the columns:
Accident Date (object) has 365 unique values. Some example values: ['10/6/2021', '11/13/2021', '11/3/2021', '12/4/2021']
Accident_Severity (object) has 3 unique values: ['Serious', 'Slight', 'Fatal']
Carriageway_Hazards (object) has 5 unique values: [nan, 'Other object on road', 'Any animal in carriageway (except ridden horse)', 'Pedestrian in carriageway - not injured', 'Previous accident', 'Vehicle load on road']
Day_of_Week (object) has 7 unique values: ['Tuesday', 'Wednesday', 'Monday', 'Saturday', 'Thursday', 'Friday', 'Sunday']
Junction_Control (object) has 7 unique values: ['Give way or uncontrolled', 'Data missing or out of range', 'Not at junction or within 20 metres', 'Auto traffic signal', 'Authorised person', 'Stop sign', 'Auto traffic sigl']
Junction_Detail (object) has 9 unique values: ['T or staggered junction', 'Not at junction or within 20 metres', 'Mini-roundabout', 'Roundabout', 'Private drive or entrance', 'Crossroads', 'More than 4 arms (not roundabout)', 'Slip road', 'Other junction']
Latitude (float64) has range: 49.91 - 60.60, 0 nan values
Light_Conditions (object) has 5 unique values: ['Darkness - no lighting', 'Daylight', 'Darkness - lights lit', 'Darkness - lighting unknown', 'Darkness - lights unlit']
Local_Authority_(District) (object) has 276 unique values. Some example values: ['Birmingham', 'Manchester', 'Glasgow City', 'Sheffield']
Longitude (float64) has range: -7.50 - 1.76, 0 nan values
Number_of_Vehicles (int64) has range: 1.00 - 32.00, 0 nan values
Police_Force (object) has 34 unique values. Some example values: ['Metropolitan Police', 'West Midlands', 'Greater Manchester', 'Thames Valley']
Road_Surface_Conditions (object) has 5 unique values: ['Frost or ice', 'Snow', 'Dry', 'Wet or damp', 'Flood over 3cm. deep', nan]
Road_Type (object) has 5 unique values: ['Single carriageway', 'Dual carriageway', 'Roundabout', nan, 'Slip road', 'One way street']
Speed_limit (int64) has 8 unique values: [30, 60, 40, 20, 70, 50, 10, 15]
Time (object) has 1437 unique values. Some example values: ['17:00', '17:30', '18:00', '15:30']
Urban_or_Rural_Area (object) has 2 unique values: ['Rural', 'Urban']
Vehicle_Type (object) has 14 unique values. Some example values: ['Car', 'Van / Goods 3.5 tonnes mgw or under', 'Motorcycle over 500cc', 'Goods 7.5 tonnes mgw and over']
Weather_Conditions (object) has 8 unique values: ['Fog or mist', 'Other', 'Snowing no high winds', 'Fine no high winds', 'Raining no high winds', 'Fine + high winds', 'Raining + high winds', nan, 'Snowing + high winds']
