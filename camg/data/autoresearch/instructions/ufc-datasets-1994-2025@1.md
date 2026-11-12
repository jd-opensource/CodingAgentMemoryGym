# OpenMLE-fast task

Task ID: `ufc-datasets-1994-2025@1`

Native metric: `UFCMatchOutcomeMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2980 bytes)
- `data/sample_submission.csv` (31622 bytes); columns: ["fight_id", "red_win_prob"]
- `data/test.csv` (322793 bytes); columns: ["fight_id", "event_id", "event_name", "date", "location", "division", "title_fight", "referee", "r_name", "r_id", "r_nick_name", "r_wins", "r_losses", "r_draws", "r_height", "r_weight", "r_reach", "r_stance", "r_dob", "r_splm", "r_str_acc", "r_sapm", "r_str_def", "r_td_avg", "r_td_avg_acc", "r_td_def", "r_sub_avg", "b_name", "b_id", "b_nick_name", "b_wins", "b_losses", "b_draws", "b_height", "b_weight", "b_reach", "b_stance", "b_dob", "b_splm", "b_str_acc", "b_sapm", "b_str_def", "b_td_avg", "b_td_avg_acc", "b_td_def", "b_sub_avg"]
- `data/train.csv` (2682357 bytes); columns: ["fight_id", "event_id", "event_name", "date", "location", "division", "title_fight", "referee", "r_name", "r_id", "r_nick_name", "r_wins", "r_losses", "r_draws", "r_height", "r_weight", "r_reach", "r_stance", "r_dob", "r_splm", "r_str_acc", "r_sapm", "r_str_def", "r_td_avg", "r_td_avg_acc", "r_td_def", "r_sub_avg", "b_name", "b_id", "b_nick_name", "b_wins", "b_losses", "b_draws", "b_height", "b_weight", "b_reach", "b_stance", "b_dob", "b_splm", "b_str_acc", "b_sapm", "b_str_def", "b_td_avg", "b_td_avg_acc", "b_td_def", "b_sub_avg", "target"]

## Public description

Competition: UFC Red-Corner Win Probability

Problem statement
Given pre-fight information about two UFC fighters and bout context, predict the probability that the red-corner fighter wins the fight. Your submission must provide a calibrated probability for each fight in the test set.

Files provided
- train.csv: Training rows with features and the target column target (1 if red-corner fighter wins, otherwise 0).
- test.csv: Test rows with the same feature columns as train.csv, without the target.
- sample_submission.csv: Template with columns [fight_id, red_win_prob]. Submit probabilities in [0, 1] for each fight_id.

Target definition
- target = 1 if winner_id == r_id, else 0 (not included in test.csv).

Data description (columns)
Rows represent single fights. Key identifiers and context:
- fight_id: Unique fight identifier (use this as the submission key).
- event_id, event_name: Event metadata.
- date: Fight date (string); participants may featurize time if desired.
- location: Event location (string).
- division: Official weight class (string).
- title_fight: 1 if a title fight, else 0.
- referee: Assigned referee (string).

Fighter attributes (pre-fight; available for both red r_* and blue b_*). These are present as two mirrored sets of columns:
- *_name, *_id, *_nick_name
- *_wins, *_losses, *_draws
- *_height, *_weight, *_reach, *_stance, *_dob
- *_splm, *_str_acc, *_sapm, *_str_def
- *_td_avg, *_td_avg_acc, *_td_def, *_sub_avg

Important: All realized in-fight statistics (e.g., significant strikes landed/attempted, control time, ground/clinch/distance breakdowns, finish round/time, and similar) are NOT included in train.csv/test.csv to prevent label leakage.

Evaluation metric
- Binary Log Loss on the red-corner win probability.
- Lower is better.
- For each test fight i with label y_i in {0,1} and predicted probability p_i in [0,1], the loss is: -mean(y_i * log(p_i) + (1 - y_i) * log(1 - p_i)).

Train/test split
- Temporal split to reflect real deployment.
- Train: fights dated before 2024-01-01.
- Test: fights dated on or after 2024-01-01.

Notes and rules
- Use only pre-fight information to build your features. Do not reconstruct or inject any in-fight realized statistics.
- Some text/categorical fields (e.g., stance, referee, division, location) may require encoding. Handle missing values robustly.
- Both classes (target 0 and 1) are present in the training set. The test set contains only fights whose labels occur in the training set (binary setting).
- Predictions must include all and only the fight_id values from test.csv.

Submission format
- A CSV with two columns and no header changes:
  - fight_id: The unique fight identifier.
  - red_win_prob: Your predicted probability that the red-corner fighter wins.

Good luck. This is a challenging, real-world sports analytics task with temporal drift, missing attributes, and rich context—perfect for rigorous feature engineering and calibrated probabilistic modeling.
