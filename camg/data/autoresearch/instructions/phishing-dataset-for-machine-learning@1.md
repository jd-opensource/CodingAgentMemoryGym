# OpenMLE-fast task

Task ID: `phishing-dataset-for-machine-learning@1`

Native metric: `PhishingDetectionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3028 bytes)
- `data/sample_submission.csv` (72529 bytes); columns: ["id", "phishing_probability"]
- `data/test.csv` (371063 bytes); columns: ["id", "NumDots", "SubdomainLevel", "PathLevel", "UrlLength", "NumDash", "NumDashInHostname", "AtSymbol", "TildeSymbol", "NumUnderscore", "NumPercent", "NumQueryComponents", "NumAmpersand", "NumHash", "NumNumericChars", "NoHttps", "RandomString", "IpAddress", "DomainInSubdomains", "DomainInPaths", "HttpsInHostname", "HostnameLength", "PathLength", "QueryLength", "DoubleSlashInPath", "NumSensitiveWords", "EmbeddedBrandName", "PctExtHyperlinks", "PctExtResourceUrls", "ExtFavicon", "InsecureForms", "RelativeFormAction", "ExtFormAction", "AbnormalFormAction", "PctNullSelfRedirectHyperlinks", "FrequentDomainNameMismatch", "FakeLinkInStatusBar", "RightClickDisabled", "PopUpWindow", "SubmitInfoToEmail", "IframeOrFrame", "MissingTitle", "ImagesOnlyInForm", "SubdomainLevelRT", "UrlLengthRT", "PctExtResourceUrlsRT", "AbnormalExtFormActionR", "ExtMetaScriptLinkRT", "PctExtNullSelfRedirectHyperlinksRT"]
- `data/train.csv` (879671 bytes); columns: ["id", "NumDots", "SubdomainLevel", "PathLevel", "UrlLength", "NumDash", "NumDashInHostname", "AtSymbol", "TildeSymbol", "NumUnderscore", "NumPercent", "NumQueryComponents", "NumAmpersand", "NumHash", "NumNumericChars", "NoHttps", "RandomString", "IpAddress", "DomainInSubdomains", "DomainInPaths", "HttpsInHostname", "HostnameLength", "PathLength", "QueryLength", "DoubleSlashInPath", "NumSensitiveWords", "EmbeddedBrandName", "PctExtHyperlinks", "PctExtResourceUrls", "ExtFavicon", "InsecureForms", "RelativeFormAction", "ExtFormAction", "AbnormalFormAction", "PctNullSelfRedirectHyperlinks", "FrequentDomainNameMismatch", "FakeLinkInStatusBar", "RightClickDisabled", "PopUpWindow", "SubmitInfoToEmail", "IframeOrFrame", "MissingTitle", "ImagesOnlyInForm", "SubdomainLevelRT", "UrlLengthRT", "PctExtResourceUrlsRT", "AbnormalExtFormActionR", "ExtMetaScriptLinkRT", "PctExtNullSelfRedirectHyperlinksRT", "CLASS_LABEL"]

## Public description

Phish or Legit — Probabilistic URL/DOM Feature Classification Challenge

Problem statement
You are given engineered URL and DOM features for webpages. Your task is to predict, for each page in the test set, the probability that it is a phishing page (CLASS_LABEL=1). Submissions must be probabilistic (a value in [0,1] per id), not hard class assignments.

Data description
- train.csv: Tabular data containing id, all numeric features, and the target column CLASS_LABEL (0=legitimate, 1=phishing).
- test.csv: Same columns as train.csv but without CLASS_LABEL. Includes id and all features.
- sample_submission.csv: Example of a valid submission with columns: id, phishing_probability.

Features
- The dataset includes dozens of engineered numeric attributes derived from webpage URL structure and rendered HTML/DOM behavior (e.g., NumDots, PathLevel, UrlLength, PctExtHyperlinks, InsecureForms, RelativeFormAction, SubmitInfoToEmail, IframeOrFrame, and several rate/ratio features like PctExtResourceUrlsRT). Most features are counts, binary flags, or proportions (in [0,1]). Some features can be -1 to indicate non-applicable or rule-based conditions; treat them as numeric.
- id is a unique identifier and should not be used as a predictive feature.
- Note: HttpsInHostname is constant in this dataset and can be safely ignored for modeling, though it remains present in the files for consistency.

Train/test split
- The competition uses a single stratified split preserving the class balance.
- Approximately 70% of the rows are in train.csv and 30% in test.csv.
- The split is deterministic and ensures that both classes (0 and 1) appear in the training set.

Submission format
- File must contain exactly two columns: id and phishing_probability.
- Include every id from the test set exactly once. Order does not matter.
- phishing_probability must be a numeric value in [0,1].

Evaluation
- Metric: Binary Log Loss (cross-entropy) on the probability of CLASS_LABEL=1.
  - Each prediction p is clipped to a small epsilon near 0 and 1 to avoid numerical issues.
  - The final score is the average negative log-likelihood over all test rows.
- Why log loss? It fairly evaluates probabilistic predictions, penalizes overconfident errors, and rewards calibration—ideal for this balanced, feature-rich tabular dataset.

Guidance for participants (optional)
- Baselines: Regularized logistic regression, gradient boosting machines (e.g., XGBoost/LightGBM), random forests, and calibrated SVMs work well on tabular data.
- Feature engineering: Consider interactions between binary indicators and proportions; scaling can help linear models, while tree-based models can handle raw values.
- Calibration matters: Techniques like Platt scaling or isotonic regression (on held-out validation slices from train.csv) can improve log loss.

Files provided to participants
- train.csv
- test.csv
- sample_submission.csv

Make sure your solution loads train.csv to build a model and produces a submission that matches test.csv ids.
