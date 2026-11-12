# OpenMLE-fast task

Task ID: `netflix-tv-shows-and-movies@2`

Native metric: `NetflixIMDbRegressionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (5422 bytes)
- `data/sample_submission.csv` (18447 bytes); columns: ["id", "imdb_score"]
- `data/test.csv` (231401 bytes); columns: ["id", "title", "type", "description", "release_year", "age_certification", "runtime", "genres", "production_countries", "seasons", "imdb_votes", "tmdb_popularity"]
- `data/test_credits.csv` (576111 bytes); columns: ["person_id", "id", "name", "character", "role"]
- `data/train.csv` (925132 bytes); columns: ["id", "title", "type", "description", "release_year", "age_certification", "runtime", "genres", "production_countries", "seasons", "imdb_score", "imdb_votes", "tmdb_popularity"]
- `data/train_credits.csv` (2293721 bytes); columns: ["person_id", "id", "name", "character", "role"]

## Public description

```
description.txt (63 lines)
sample_submission.csv (690 lines)
test.csv (699 lines)
test_credits.csv (11788 lines)
train.csv (2795 lines)
train_credits.csv (47044 lines)```

-> sample_submission.csv has 689 rows and 2 columns.
Here is some information about the columns:
id (object) has 689 unique values. Some example values: ['tm438994', 'tm404690', 'ts42120', 'tm409817']
imdb_score (float64) has range: 3.39 - 9.93, 0 nan values

-> test.csv has 689 rows and 12 columns.
Here is some information about the columns:
age_certification (object) has 11 unique values. Some example values: ['TV-MA', 'R', 'PG-13', 'TV-14']
description (object) has 689 unique values. Some example values: ['A talented photographer stuck in a dead-end job inherits an antique Advent calendar that may be predicting the future -- and pointing her toward love.', 'A quirky couple spends their three-year dating anniversary looking back at their relationship and contemplating whether they should break up.', 'Hundreds of years from now, the last surviving humans discover the means of sending consciousness back through time, directly into people in the 21st century. These "travelers" assume the lives of seemingly random people, while secretly working as teams to perform missions in order to save humanity from a terrible future.', 'A young widow is hired as the domestic helper for a wealthy architect, but social divides come to the fore as an unlikely attraction grows between them.']
genres (object) has 383 unique values. Some example values: ["['comedy']", "['documentation']", "['drama']", "['comedy', 'drama']"]
id (object) has 689 unique values. Some example values: ['tm438994', 'tm404690', 'ts42120', 'tm409817']
imdb_votes (float64) has range: 1007.00 - 2294231.00, 0 nan values
production_countries (object) has 111 unique values. Some example values: ["['US']", "['IN']", "['JP']", "['GB']"]
release_year (int64) has range: 1967.00 - 2022.00, 0 nan values
runtime (int64) has range: 3.00 - 206.00, 0 nan values
seasons (float64) has range: 1.00 - 42.00, 461 nan values
title (object) has 689 unique values. Some example values: ['The Holiday Calendar', 'Happy Anniversary', 'Travelers', 'Sir']
tmdb_popularity (float64) has range: 1.11 - 1387.39, 2 nan values
type (object) has 2 unique values: ['MOVIE', 'SHOW']

-> test_credits.csv has 11787 rows and 5 columns.
Here is some information about the columns:
character (object) has 8922 unique values. Some example values: ['Himself', 'Self', 'Herself', 'Additional Voices (voice)']
id (object) has 671 unique values. Some example values: ['tm155787', 'tm979026', 'tm458585', 'tm849022']
name (object) has 10696 unique values. Some example values: ['Yuki Kaji', 'Takahiro Sakurai', 'Murali Sharma', 'Rikiya Koyama']
person_id (int64) has range: 7.00 - 2462818.00, 0 nan values
role (object) has 2 unique values: ['ACTOR', 'DIRECTOR']

-> train.csv has 2752 rows and 13 columns.
Here is some information about the columns:
age_certification (object) has 11 unique values. Some example values: ['TV-MA', 'R', 'PG-13', 'TV-14']
description (object) has 2752 unique values. Some example values: ['A disillusioned Delhi wife (Dolly), and her new-in-town cousin (Kitty), navigate damning secrets, dreams and their thorny dynamic on their respective roads to freedom.', 'Armed with boyish charm and a sharp wit, the former "SNL" writer offers sly takes on marriage, his beef with babies and the time he met Bill Clinton.', "Kept locked inside the house by her father, 7-year-old Chloe lives in fear and fascination of the outside world, where Abnormals create a constant threat—or so she believes. When a mysterious stranger offers her a glimpse of what's really happening outside, Chloe soon finds that while the truth isn't so simple, the danger is very real.", 'Chasing his dream to join an elite K-9 unit, a state trooper partners with a fellow underdog: clever but naughty shelter pup Ruby. Based on a true story.']
genres (object) has 1140 unique values. Some example values: ["['comedy']", "['documentation']", "['drama']", "['comedy', 'drama']"]
id (object) has 2752 unique values. Some example values: ['tm838007', 'tm229542', 'tm427335', 'tm1166288']
imdb_score (float64) has range: 1.70 - 9.50, 0 nan values
imdb_votes (float64) has range: 1001.00 - 2021343.00, 0 nan values
production_countries (object) has 252 unique values. Some example values: ["['US']", "['IN']", "['GB']", "['JP']"]
release_year (int64) has range: 1954.00 - 2022.00, 0 nan values
runtime (int64) has range: 2.00 - 224.00, 0 nan values
seasons (float64) has range: 1.00 - 37.00, 1802 nan values
title (object) has 2735 unique values. Some example values: ['The Call', 'Bodyguard', 'Zero', 'The Gift']
tmdb_popularity (float64) has range: 0.60 - 2274.04, 7 nan values
type (object) has 2 unique values: ['MOVIE', 'SHOW']

-> train_credits.csv has 47043 rows and 5 columns.
Here is some information about the columns:
character (object) has 31238 unique values. Some example values: ['Self', 'Himself', 'Self (archive footage)', 'Herself']
id (object) has 2702 unique values. Some example values: ['tm32982', 'tm244149', 'tm39888', 'tm467467']
name (object) has 35868 unique values. Some example values: ['Kareena Kapoor Khan', 'Boman Irani', 'Shah Rukh Khan', 'Amitabh Bachchan']
person_id (int64) has range: 7.00 - 2460188.00, 0 nan values
role (object) has 2 unique values: ['ACTOR', 'DIRECTOR']
