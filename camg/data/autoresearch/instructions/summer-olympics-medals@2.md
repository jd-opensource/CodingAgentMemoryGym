# OpenMLE-fast task

Task ID: `summer-olympics-medals@2`

Native metric: `SummerOlympicsMedalMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4116 bytes)
- `data/sample_submission.csv` (93753 bytes); columns: ["Sport", "Discipline", "Event", "Event_gender", "Country", "Medal_Prob_Gold", "Medal_Prob_Silver", "Medal_Prob_Bronze"]
- `data/test.csv` (56767 bytes); columns: ["City", "Year", "Sport", "Discipline", "Event", "Country_Code", "Country", "Event_gender"]
- `data/train.csv` (418232 bytes); columns: ["City", "Year", "Sport", "Discipline", "Event", "Country_Code", "Country", "Event_gender", "Medal"]

## Public description

Summer Olympics Podium Color Prediction (2008)

Problem statement
Predict the medal color (Gold, Silver, Bronze) that each medaling country received in the 2008 Summer Olympics for its event, using historical Olympic results from 1976–2004. You are given athlete-level historical results; your task is to engineer event/country histories and model calibrated probabilities over medal colors for the 2008 medaling (Sport, Discipline, Event, Event_gender, Country) pairs.

What you must predict
- For every row in test.csv (one (Sport, Discipline, Event, Event_gender, Country) that medaled in 2008), output the probability of each medal color: Gold, Silver, Bronze.
- Your submission must contain one row per identifier present in test.csv and the following columns:
  • Sport
  • Discipline
  • Event
  • Event_gender
  • Country
  • Medal_Prob_Gold
  • Medal_Prob_Silver
  • Medal_Prob_Bronze
- Probabilities must be numeric, non-negative, and sum to 1 for each row.

Data description
The data originate from athlete-level medal results between 1976 and 2008. Team medals appear once per team member; multiple athletes from the same country can also medal in the same event. For modeling, the unit is country × event × year with a single medal color per country: if a country earned multiple medals in the same event-year, we keep the best medal color achieved by that country (Gold > Silver > Bronze).

Provided competition files
- train.csv: Country–event outcomes for 1976–2004. Columns include City, Year, Sport, Discipline, Event, Country_Code, Country, Event_gender, and the target Medal (Gold/Silver/Bronze) representing the best color achieved by that country in that event-year.
- test.csv: Country–event rows that medaled in 2008, with the same contextual columns as train.csv but without the Medal column.
- sample_submission.csv: A template showing the required submission format (with random but valid probabilities). Use this as a reference for column names and identifiers.

Important processing notes
- Begin from athlete-level lines and deduplicate team roster duplicates. Then aggregate to a single row per (Year, Sport, Discipline, Event, Event_gender, Country), assigning the best medal color achieved by that country for that event-year.
- Each identifier in a given year maps to exactly one medal color in our files after aggregation.
- Engineer features strictly from the provided data. Example ideas:
  • Event history for (Country, Event): last medal color, color counts, recency, streaks, time since last medal.
  • Discipline/Sport history for (Country, Discipline) and (Country, Sport), including recent editions.
  • Competitive context: turnover of medaling countries in the event, historical volatility of medal colors, number of unique medaling countries.
  • Country form: per-year total medals and color mix; momentum across editions.
  • Host/city effects by year; gender splits via Event_gender.

Evaluation
- Metric: Multiclass Log Loss (cross-entropy), micro-averaged across all rows in test.csv.
- For each row, the log loss is computed from the probability assigned to the true medal color and then averaged across rows.
- Submission rows are matched to the ground truth using (Sport, Discipline, Event, Event_gender, Country). Duplicates or missing rows will invalidate the submission.

Rules and expectations
- Use any modeling approach that produces calibrated class probabilities (e.g., gradient boosted trees, logistic regression, neural networks). Proper feature engineering is expected.
- Do not use external data. All features must be derived from train.csv and test.csv.
- Ensure probabilities are well-formed: finite, non-negative, and summing to 1 per row.

File specifications
- train.csv: Columns include context fields and a target column Medal with values in {Gold, Silver, Bronze} (best color per country–event–year).
- test.csv: Same context fields, but without the Medal column.
- sample_submission.csv: Columns [Sport, Discipline, Event, Event_gender, Country, Medal_Prob_Gold, Medal_Prob_Silver, Medal_Prob_Bronze].
