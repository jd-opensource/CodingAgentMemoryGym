# OpenMLE-fast task

Task ID: `scoobydoo-complete@1`

Native metric: `ScoobyDooRatingsMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (948 bytes)
- `data/sample_submission.csv` (2408 bytes); columns: ["id", "imdb"]
- `data/test.csv` (60274 bytes); columns: ["id", "series.name", "network", "season", "title", "date.aired", "run.time", "format", "monster.name", "monster.gender", "monster.type", "monster.subtype", "monster.species", "monster.real", "monster.amount", "caught.fred", "caught.daphne", "caught.velma", "caught.shaggy", "caught.scooby", "captured.fred", "captured.daphne", "captured.velma", "captured.shaggy", "captured.scooby", "unmask.fred", "unmask.daphne", "unmask.velma", "unmask.shaggy", "unmask.scooby", "snack.fred", "snack.daphne", "snack.velma", "snack.shaggy", "snack.scooby", "unmask.other", "caught.other", "caught.not", "trap.work.first", "setting.terrain", "setting.country/state", "suspects.amount", "non-suspect", "arrested", "culprit.gender", "culprit.amount", "motive", "if.it.wasnt.for", "and.that", "door.gag", "number.of.snacks", "split.up", "another.mystery", "set.a.trap", "jeepers", "jinkies", "my.glasses", "just.about.wrapped.up", "zoinks", "groovy", "scooby.doo.where.are.you", "rooby.rooby.roo", "batman", "scooby-dum", "scrappy-doo", "hex.girls", "blue.falcon", "fred.va", "daphne.va", "velma.va", "shaggy.va", "scooby.va"]
- `data/train.csv` (226574 bytes); columns: ["id", "series.name", "network", "season", "title", "date.aired", "run.time", "format", "monster.name", "monster.gender", "monster.type", "monster.subtype", "monster.species", "monster.real", "monster.amount", "caught.fred", "caught.daphne", "caught.velma", "caught.shaggy", "caught.scooby", "captured.fred", "captured.daphne", "captured.velma", "captured.shaggy", "captured.scooby", "unmask.fred", "unmask.daphne", "unmask.velma", "unmask.shaggy", "unmask.scooby", "snack.fred", "snack.daphne", "snack.velma", "snack.shaggy", "snack.scooby", "unmask.other", "caught.other", "caught.not", "trap.work.first", "setting.terrain", "setting.country/state", "suspects.amount", "non-suspect", "arrested", "culprit.gender", "culprit.amount", "motive", "if.it.wasnt.for", "and.that", "door.gag", "number.of.snacks", "split.up", "another.mystery", "set.a.trap", "jeepers", "jinkies", "my.glasses", "just.about.wrapped.up", "zoinks", "groovy", "scooby.doo.where.are.you", "rooby.rooby.roo", "batman", "scooby-dum", "scrappy-doo", "hex.girls", "blue.falcon", "fred.va", "daphne.va", "velma.va", "shaggy.va", "scooby.va", "imdb"]

## Public description

# Scooby-Doo Ratings Prediction (Tabular Regression)

Problem statement
Predict the IMDb rating of Scooby-Doo episodes and movies using the provided metadata.

Data description
- train.csv: Tabular file containing all features and the target column imdb for the training rows, plus a unique id column.
- sample_submission.csv: Example submission with columns id and imdb. Values are valid floating-point predictions for the test set.

Target and evaluation
- Target: imdb rating (continuous).
- Metric: Root Mean Squared Error (RMSE) between your submitted imdb predictions and the ground truth.

Submission format
- Submit a CSV with columns: id, imdb.
- The id values must match those in test.csv. The imdb column must contain valid floating-point predictions.

Files provided
- train.csv
- test.csv
- sample_submission.csv
