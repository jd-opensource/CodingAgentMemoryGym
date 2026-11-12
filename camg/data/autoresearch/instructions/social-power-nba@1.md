# OpenMLE-fast task

Task ID: `social-power-nba@1`

Native metric: `SalaryPredictionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3349 bytes)
- `data/sample_submission.csv` (2084 bytes); columns: ["Id", "salary_millions"]
- `data/test.csv` (31296 bytes); columns: ["Id", "player_name", "position", "age", "team_name", "team_conf", "team_elo", "G", "GS", "MP", "FG", "FGA", "FG%", "3P", "3PA", "3P%", "2P", "2PA", "2P%", "eFG%", "FT", "FTA", "FT%", "ORB", "DRB", "TRB", "AST", "STL", "BLK", "TOV", "PF", "PS/G", "age_pie", "gp_pie", "min_pie", "OFFRTG", "DEFRTG", "NETRTG", "AST%", "AST/TO", "AST_RATIO", "OREB%", "DREB%", "REB%", "TO_RATIO", "EFG%", "TS%", "USG%", "PACE", "PIE", "ORPM", "DRPM", "RPM", "WINS", "TWITTER_FAVORITE_COUNT", "TWITTER_RETWEET_COUNT", "tw_fav_log1p", "tw_rt_log1p", "wiki_pageviews_sum", "wiki_pageviews_log1p"]
- `data/train.csv` (126012 bytes); columns: ["Id", "player_name", "position", "age", "team_name", "team_conf", "team_elo", "G", "GS", "MP", "FG", "FGA", "FG%", "3P", "3PA", "3P%", "2P", "2PA", "2P%", "eFG%", "FT", "FTA", "FT%", "ORB", "DRB", "TRB", "AST", "STL", "BLK", "TOV", "PF", "PS/G", "age_pie", "gp_pie", "min_pie", "OFFRTG", "DEFRTG", "NETRTG", "AST%", "AST/TO", "AST_RATIO", "OREB%", "DREB%", "REB%", "TO_RATIO", "EFG%", "TS%", "USG%", "PACE", "PIE", "ORPM", "DRPM", "RPM", "WINS", "TWITTER_FAVORITE_COUNT", "TWITTER_RETWEET_COUNT", "tw_fav_log1p", "tw_rt_log1p", "wiki_pageviews_sum", "wiki_pageviews_log1p", "salary_millions"]

## Public description

Competition: Predict NBA Player Salaries from On-Court Performance and Social Influence (2016–2017)

Problem statement
Build a regression model that predicts each NBA player’s 2016–2017 season salary (in millions USD) using player performance, impact metrics, social media engagement, Wikipedia pageviews, and team context. The dataset is designed to reward thoughtful feature processing and robust modeling.

Data description
Final files provided to participants:
- train.csv: Player-level features and the target column salary_millions.
- test.csv: Player-level features (same schema as train.csv except without salary_millions).
- sample_submission.csv: Example of a valid submission format (Ids matching test.csv).

Schema overview
- Id: Unique integer identifier for each player row.
- player_name: Player name (string). Use as an optional feature or drop if preferred.
- position: Primary playing position (PG, SG, SF, PF, C).
- age: Player age.
- team_name: Team full name for the season.
- team_conf: Team conference (East/West).
- team_elo: Team-level ELO rating (numeric).
- Box score features: Per-game shooting and counting stats (e.g., G, GS, MP, FG, FGA, FG%, 3P, 3PA, 3P%, 2P, 2PA, 2P%, eFG%, FT, FTA, FT%, ORB, DRB, TRB, AST, STL, BLK, TOV, PF, PS/G).
- Impact metrics (RPM): ORPM, DRPM, RPM, WINS.
- Efficiency metrics (PIE): OFFRTG, DEFRTG, NETRTG, AST%, AST/TO, AST_RATIO, OREB%, DREB%, REB%, TO_RATIO, EFG%, TS%, USG%, PACE, PIE.
- Social features (Twitter): TWITTER_FAVORITE_COUNT, TWITTER_RETWEET_COUNT, plus log-transformed versions tw_fav_log1p and tw_rt_log1p.
- Popularity features (Wikipedia): wiki_pageviews_sum and wiki_pageviews_log1p.
- Target (train.csv only): salary_millions (continuous numeric value).

Notes
- Features have been assembled from multiple sources and normalized; numeric missing values were imputed with column medians to ensure usability. Categorical features are provided as strings.
- There are no salary-related leakage features in the inputs; the only target is salary_millions in train.csv.
- Ids are unique and correspond one-to-one across test.csv and sample_submission.csv.

Submission format
- A CSV file with exactly two columns: Id and salary_millions.
- Each Id must match a player row in test.csv exactly once.
- salary_millions must be a finite numeric value.

Evaluation
- Metric: Root Mean Squared Error (RMSE) between submitted salary_millions and the ground truth.
- Computation: RMSE = sqrt(mean((y_pred - y_true)^2)) over all rows in the test set.
- RMSE fairly penalizes larger errors and is appropriate for the continuous, heavy-tailed nature of salaries.

Modeling expectations
- This is a tabular regression task well-suited for methods such as regularized linear models, tree-based ensembles, gradient boosting, and stacking.
- Consider transformations for skewed inputs (e.g., log of social/pageview counts already provided), interaction features (e.g., efficiency × usage), and robust validation.
- You may use position, team, and conference as categorical features; numeric encoders or target-independent encodings are recommended.

Deliverables
- Submit a single CSV with columns: Id, salary_millions. Do not include extra columns.

Good luck building models that blend on-court performance with social influence and team context to estimate player compensation!
