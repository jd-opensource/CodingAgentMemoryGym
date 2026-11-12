# OpenMLE-fast task

Task ID: `movies-updated-data@1`

Native metric: `MovieGrossRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3517 bytes)
- `data/sample_submission.csv` (16721 bytes); columns: ["row_id", "gross"]
- `data/test.csv` (124323 bytes); columns: ["row_id", "name", "rating", "genre", "year", "released", "score", "votes", "director", "writer", "star", "country", "budget", "company", "runtime"]
- `data/train.csv` (531431 bytes); columns: ["name", "rating", "genre", "year", "released", "score", "votes", "director", "writer", "star", "country", "budget", "company", "runtime", "gross"]

## Public description

```
description.txt (48 lines)
sample_submission.csv (753 lines)
test.csv (753 lines)
train.csv (3080 lines)```

-> sample_submission.csv has 752 rows and 2 columns.
Here is some information about the columns:
gross (float64) has range: 15703.05 - 2593400707.95, 0 nan values
row_id (int64) has range: 1.00 - 752.00, 0 nan values

-> test.csv has 752 rows and 15 columns.
Here is some information about the columns:
budget (int64) has range: 0.00 - 170000000.00, 0 nan values
company (object) has 395 unique values. Some example values: ['Universal Pictures', 'Columbia Pictures', 'Warner Bros.', 'Twentieth Century Fox']
country (object) has 22 unique values. Some example values: ['United States', 'United Kingdom', 'France', 'Canada']
director (object) has 553 unique values. Some example values: ['John Carpenter', 'Alan Parker', 'Joel Coen', 'Ivan Reitman']
genre (object) has 15 unique values. Some example values: ['Comedy', 'Drama', 'Action', 'Crime']
name (object) has 752 unique values. Some example values: ['Birthday Girl', 'The Blue Lagoon', 'Superman II', 'Dressed to Kill']
rating (object) has 9 unique values: ['R', 'PG', nan, 'G', 'Not Rated', 'PG-13', 'Unrated', 'TV-PG', 'NC-17', 'TV-MA']
released (object) has 608 unique values. Some example values: ['October 28, 1983 (United States)', 'August 25, 1995 (United States)', 'October 6, 2000 (United States)', 'October 30, 1992 (United States)']
row_id (int64) has range: 1.00 - 752.00, 0 nan values
runtime (float64) has range: 72.00 - 357.00, 10 nan values
score (float64) has range: 2.70 - 8.60, 0 nan values
star (object) has 507 unique values. Some example values: ['Sylvester Stallone', 'Michael J. Fox', 'Jeff Bridges', 'Burt Reynolds']
votes (int64) has range: 105.00 - 1500000.00, 0 nan values
writer (object) has 681 unique values. Some example values: ['Stephen King', 'John Hughes', 'Simon Moore', 'Larry Cohen']
year (int64) has range: 1980.00 - 2001.00, 0 nan values

-> train.csv has 3079 rows and 15 columns.
Here is some information about the columns:
budget (int64) has range: 0.00 - 200000000.00, 0 nan values
company (object) has 1019 unique values. Some example values: ['Paramount Pictures', 'Universal Pictures', 'Columbia Pictures', 'Warner Bros.']
country (object) has 39 unique values. Some example values: ['United States', 'United Kingdom', 'France', 'Canada']
director (object) has 1402 unique values. Some example values: ['Woody Allen', 'Directors', 'Clint Eastwood', 'Barry Levinson']
genre (object) has 16 unique values. Some example values: ['Comedy', 'Drama', 'Action', 'Crime']
gross (float64) has range: 309.00 - 2201647264.00, 0 nan values
name (object) has 3063 unique values. Some example values: ['Hamlet', 'Paradise', 'Pulse', 'Bad Boys']
rating (object) has 10 unique values. Some example values: ['R', 'PG-13', 'PG', 'G']
released (object) has 1481 unique values. Some example values: ['March 9, 1990 (United States)', 'December 22, 1995 (United States)', 'September 18, 1987 (United States)', 'March 22, 1985 (United States)']
runtime (float64) has range: 69.00 - 271.00, 35 nan values
score (float64) has range: 2.20 - 9.30, 0 nan values
star (object) has 1345 unique values. Some example values: ['Robert De Niro', 'Tom Hanks', 'Mel Gibson', 'John Travolta']
votes (int64) has range: 67.00 - 2400000.00, 0 nan values
writer (object) has 2160 unique values. Some example values: ['Stephen King', 'John Hughes', 'Woody Allen', 'William Shakespeare']
year (int64) has range: 1980.00 - 2001.00, 0 nan values
