# OpenMLE-fast task

Task ID: `indian-city-state-map@1`

Native metric: `IndianCityStateMacroF1Metrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2608 bytes)
- `data/sample_submission.csv` (4556 bytes); columns: ["city", "state"]
- `data/test.csv` (2234 bytes); columns: ["city"]
- `data/train.csv` (18651 bytes); columns: ["city", "state"]

## Public description

Indian City → State Text Classification (2015 reference)

Problem statement
Given only the city name string, predict its Indian state or union territory (as of February 2015). The task requires learning linguistic and morphological cues in city names that correlate with regional patterns across India.

Data description
- train.csv: The training set with two columns: city, state. City names are canonicalized (lowercased, whitespace-normalized, hyphen normalized, bracketed segments removed, common trailing markers like "*" stripped).
- test.csv: The test set with a single column: city. It is prepared with the same canonicalization rules used for training.

Construction details (for transparency)
- Exact duplicate city–state pairs were removed to avoid redundancy.
- City names that appear in multiple states (ambiguous under city-only input) were removed to ensure a well-posed mapping task.
- Three singleton classes with only one reliable example were removed to ensure stable evaluation: Andaman and Nicobar Islands, Chandigarh, Dadra and Nagar Haveli.
- The split is stratified by state so that class proportions are preserved as much as possible. Very small classes receive at least one sample in both train and test when feasible.

Evaluation
- Primary metric: Macro F1 score across the states present in the test set. For each state appearing at least once in the test labels, F1 is computed and averaged with equal weight. Classes absent from the test labels are ignored in the average.
- Submission format: A CSV file with exactly two columns: city, state. The city values must exactly match those provided in test.csv (order-insensitive, no duplicates), and the predicted state must be a valid state label from the training set.

Why this challenge is meaningful
- Real-world relevance: Mapping cities to states is foundational for data cleaning, aggregation, and geospatial analysis in Indian datasets.
- Difficulty: Subtle morphological overlaps across states (e.g., "-pur", "-garh", "nagar"), orthographic variations, and class imbalance make the task non-trivial.
- Solvable with ML: Character/subword n-grams, TF-IDF + linear models, and neural text classifiers can all learn robust signals from city names, especially with thoughtful preprocessing and calibration.

Files provided
- train.csv — labeled training data (city, state)
- test.csv — unlabeled test data (city)
- sample_submission.csv — example of the required submission format (city, state)

Note
- Do not include any paths in CSV files; use the city string exactly as provided in test.csv to align predictions.
