# OpenMLE-fast task

Task ID: `-lionel-messi-all-club-goals@1`

Native metric: `MessiGoalTypeMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3347 bytes)
- `data/sample_submission.csv` (2852 bytes); columns: ["row_id", "Type"]
- `data/test.csv` (13212 bytes); columns: ["row_id", "Season", "Competition", "Matchday", "Date", "Venue", "Club", "Opponent", "Result", "Playing_Position", "Minute", "At_score", "Goal_assist"]
- `data/train.csv` (56257 bytes); columns: ["Season", "Competition", "Matchday", "Date", "Venue", "Club", "Opponent", "Result", "Playing_Position", "Minute", "At_score", "Type", "Goal_assist"]

## Public description

```
description.txt (56 lines)
sample_submission.csv (142 lines)
test.csv (142 lines)
train.csv (563 lines)```

-> sample_submission.csv has 141 rows and 2 columns.
Here is some information about the columns:
Type (object) has 7 unique values: ['Tap-in', 'Penalty', 'Penalty rebound', 'Left-footed shot', 'Header', 'Right-footed shot', 'Direct free kick']
row_id (object) has 141 unique values. Some example values: ['T000001', 'T000002', 'T000003', 'T000004']

-> test.csv has 141 rows and 13 columns.
Here is some information about the columns:
At_score (object) has 25 unique values. Some example values: ['1:00', '0:01', '1:01', '2:00']
Club (object) has 2 unique values: ['FC Barcelona', 'Paris Saint-Germain']
Competition (object) has 7 unique values: ['LaLiga', 'UEFA Champions League', 'Copa del Rey', 'Supercopa', 'FIFA Club World Cup', 'Ligue 1', 'Champions League']
Date (object) has 127 unique values. Some example values: ['03/07/12', '03/08-15', '05-01/10', '9/19/12']
Goal_assist (object) has 33 unique values. Some example values: ['Andres Iniesta', 'Xavi', 'Dani Alves', 'Pedro']
Matchday (object) has 44 unique values. Some example values: ['Group Stage', 'last 16', '26', '33']
Minute (object) has 69 unique values. Some example values: ['58', '63', '50', '18']
Opponent (object) has 54 unique values. Some example values: ['Rayo Vallecano', 'Real Madrid', 'Real Betis Balompie', 'CA Osasuna']
Playing_Position (object) has 9 unique values: ['RW', 'LW', 'CF', 'SS', 'CF ', 'RW ', 'AM ', 'AM', 'SS ']
Result (object) has 37 unique values. Some example values: ['3:00', '0:05', '1:02', '2:02']
Season (object) has 18 unique values. Some example values: ['09/10', '10/11', '14/15', '11-Dec']
Venue (object) has 2 unique values: ['H', 'A']
row_id (object) has 141 unique values. Some example values: ['T000001', 'T000002', 'T000003', 'T000004']

-> train.csv has 562 rows and 13 columns.
Here is some information about the columns:
At_score (object) has 44 unique values. Some example values: ['1:00', '2:00', '0:01', '0:02']
Club (object) has 2 unique values: ['FC Barcelona', 'Paris Saint-Germain']
Competition (object) has 9 unique values: ['LaLiga', 'UEFA Champions League', 'Copa del Rey', 'Supercopa', 'FIFA Club World Cup', 'UEFA Super Cup', 'Ligue 1', 'Trophée des Champions', 'Troph�e des Champions']
Date (object) has 393 unique values. Some example values: ['2/19/12', '1/27/13', '04/06/10', '05/05/12']
Goal_assist (object) has 61 unique values. Some example values: ['Luis Suarez', 'Dani Alves', 'Andres Iniesta', 'Xavi']
Matchday (object) has 47 unique values. Some example values: ['Group Stage', 'last 16', 'Quarter-Finals', '25']
Minute (object) has 97 unique values. Some example values: ['55', '90', '85', '87']
Opponent (object) has 94 unique values. Some example values: ['Sevilla FC', 'Atletico de Madrid', 'Valencia CF', 'Athletic Bilbao']
Playing_Position (object) has 8 unique values: ['CF', 'RW', 'CF ', 'AM', 'RW ', 'AM ', 'SS', 'SS ']
Result (object) has 54 unique values. Some example values: ['4:00', '5:00', '3:01', '3:00']
Season (object) has 19 unique values. Some example values: ['11-Dec', 'Dec-13', '16/17', '18/19']
Type (object) has 12 unique values. Some example values: ['Left-footed shot', 'Penalty', 'Right-footed shot', 'Direct free kick']
Venue (object) has 2 unique values: ['H', 'A']
