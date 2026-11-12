# OpenMLE-fast task

Task ID: `web-page-phishing-detection-dataset@1`

Native metric: `PhishingWebPageDetectionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2565 bytes)
- `data/sample_submission.csv` (98866 bytes); columns: ["id", "phishing"]
- `data/test.csv` (757424 bytes); columns: ["url", "length_url", "length_hostname", "ip", "nb_dots", "nb_hyphens", "nb_at", "nb_qm", "nb_and", "nb_or", "nb_eq", "nb_underscore", "nb_tilde", "nb_percent", "nb_slash", "nb_star", "nb_colon", "nb_comma", "nb_semicolumn", "nb_dollar", "nb_space", "nb_www", "nb_com", "nb_dslash", "http_in_path", "https_token", "ratio_digits_url", "ratio_digits_host", "punycode", "port", "tld_in_path", "tld_in_subdomain", "abnormal_subdomain", "nb_subdomains", "prefix_suffix", "random_domain", "shortening_service", "path_extension", "nb_redirection", "nb_external_redirection", "length_words_raw", "char_repeat", "shortest_words_raw", "shortest_word_host", "shortest_word_path", "longest_words_raw", "longest_word_host", "longest_word_path", "avg_words_raw", "avg_word_host", "avg_word_path", "phish_hints", "domain_in_brand", "brand_in_subdomain", "brand_in_path", "suspecious_tld", "statistical_report", "nb_hyperlinks", "ratio_intHyperlinks", "ratio_extHyperlinks", "ratio_nullHyperlinks", "nb_extCSS", "ratio_intRedirection", "ratio_extRedirection", "ratio_intErrors", "ratio_extErrors", "login_form", "external_favicon", "links_in_tags", "submit_email", "ratio_intMedia", "ratio_extMedia", "sfh", "iframe", "popup_window", "safe_anchor", "onmouseover", "right_clic", "empty_title", "domain_in_title", "domain_with_copyright", "whois_registered_domain", "domain_registration_length", "domain_age", "web_traffic", "dns_record", "google_index", "page_rank", "id"]
- `data/train.csv` (3142334 bytes); columns: ["url", "length_url", "length_hostname", "ip", "nb_dots", "nb_hyphens", "nb_at", "nb_qm", "nb_and", "nb_or", "nb_eq", "nb_underscore", "nb_tilde", "nb_percent", "nb_slash", "nb_star", "nb_colon", "nb_comma", "nb_semicolumn", "nb_dollar", "nb_space", "nb_www", "nb_com", "nb_dslash", "http_in_path", "https_token", "ratio_digits_url", "ratio_digits_host", "punycode", "port", "tld_in_path", "tld_in_subdomain", "abnormal_subdomain", "nb_subdomains", "prefix_suffix", "random_domain", "shortening_service", "path_extension", "nb_redirection", "nb_external_redirection", "length_words_raw", "char_repeat", "shortest_words_raw", "shortest_word_host", "shortest_word_path", "longest_words_raw", "longest_word_host", "longest_word_path", "avg_words_raw", "avg_word_host", "avg_word_path", "phish_hints", "domain_in_brand", "brand_in_subdomain", "brand_in_path", "suspecious_tld", "statistical_report", "nb_hyperlinks", "ratio_intHyperlinks", "ratio_extHyperlinks", "ratio_nullHyperlinks", "nb_extCSS", "ratio_intRedirection", "ratio_extRedirection", "ratio_intErrors", "ratio_extErrors", "login_form", "external_favicon", "links_in_tags", "submit_email", "ratio_intMedia", "ratio_extMedia", "sfh", "iframe", "popup_window", "safe_anchor", "onmouseover", "right_clic", "empty_title", "domain_in_title", "domain_with_copyright", "whois_registered_domain", "domain_registration_length", "domain_age", "web_traffic", "dns_record", "google_index", "page_rank", "id", "status"]

## Public description

Title: Phishing Web Page Detection

Problem statement:
Build a machine learning model that predicts the probability that a given web page is a phishing page. Each example includes the raw URL string and 87 engineered features capturing URL syntax, page content signals, and external indicators. Your task is to output well-calibrated probabilities for unseen URLs.

Data description:
- train.csv: Training set with all features, the raw URL string, an id column, and the target label.
- test.csv: Test set with the same features and url and an id column, but without the target label.
- sample_submission.csv: Example submission file showing the required format.

Columns overview:
- id: Unique identifier for each example.
- url: Raw URL string associated with the example.
- 87 engineered feature columns: Numeric indicators derived from URL structure, page content, and external signals.
- status (train.csv only): Target label with values phishing or legitimate.

Submission format:
- CSV with two columns: id and phishing
- id: the identifier provided in test.csv
- phishing: the predicted probability (between 0 and 1) that the URL is phishing

Evaluation metric:
- Binary LogLoss (cross-entropy). Lower is better.
- Rationale: LogLoss is threshold-independent and rewards calibrated probabilities. The dataset is balanced and includes diverse signals, making LogLoss a precise and fair measure of model quality.

Train/test split details:
- Deterministic split with fixed random seed to ensure reproducibility.
- Group-aware by hostname: all samples sharing the same hostname are kept in the same split to reduce memorization leakage.
- Stratified to approximately preserve class balance across splits.

Guidance for participants:
- Use all provided features and the raw URL string.
- Handle missing values robustly; some features use sentinel values such as -1.
- Consider feature engineering from the URL string (e.g., character-level n-grams, regex counts) to complement the engineered features.
- Recommended validation within train: Group-aware cross-validation (e.g., GroupKFold by hostname) to avoid leakage and overfitting.
- Tree-based ensembles (GBMs, Random Forests) and regularized linear models are strong baselines. Careful preprocessing and calibration (e.g., Platt scaling/Isotonic) will improve performance.

Files provided to participants:
- train.csv
- test.csv
- sample_submission.csv

Notes:
- Do not rely on external services or new labels; use only the provided data.
- Ensure your submission covers every id in test.csv exactly once.
