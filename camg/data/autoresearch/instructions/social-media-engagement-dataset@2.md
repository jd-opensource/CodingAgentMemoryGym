# OpenMLE-fast task

Task ID: `social-media-engagement-dataset@2`

Native metric: `SocialMediaViralityMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1604 bytes)
- `data/sample_submission.csv` (72718 bytes); columns: ["row_id", "viral_probability"]
- `data/test.csv` (892872 bytes); columns: ["row_id", "timestamp", "day_of_week", "platform", "user_id", "location", "language", "text_content", "hashtags", "mentions", "keywords", "topic_category", "sentiment_score", "sentiment_label", "emotion_type", "toxicity_score", "brand_name", "product_name", "campaign_name", "campaign_phase", "user_past_sentiment_avg", "user_engagement_growth", "buzz_change_rate"]
- `data/train.csv` (3584796 bytes); columns: ["row_id", "timestamp", "day_of_week", "platform", "user_id", "location", "language", "text_content", "hashtags", "mentions", "keywords", "topic_category", "sentiment_score", "sentiment_label", "emotion_type", "toxicity_score", "brand_name", "product_name", "campaign_name", "campaign_phase", "user_past_sentiment_avg", "user_engagement_growth", "buzz_change_rate", "label_viral"]

## Public description

Title: Platform-normalized virality classification

Problem statement
Predict whether a social media post will be viral at the moment of posting. A post is considered viral if it ranks in the top 10% by engagement rate within its platform-and-month cohort (e.g., Twitter–2024-09).

Files provided
- public/train.csv: Training rows with features and the target column label_viral.
- public/test.csv: Test rows with features only.
- public/sample_submission.csv: Example submission file with the required format.

Data description
Each row describes a single social media post with the following fields (examples):
- Identifiers and time: row_id, timestamp, day_of_week, platform, user_id, location, language
- Textual inputs: text_content, hashtags, mentions, keywords
- Context: topic_category, brand_name, product_name, campaign_name, campaign_phase
- Pre-computed signals available at posting time: sentiment_label, sentiment_score, emotion_type, toxicity_score, user_past_sentiment_avg, user_engagement_growth, buzz_change_rate

Excluded outcome fields (not present in train/test): likes_count, shares_count, comments_count, impressions, engagement_rate, and any original opaque IDs.

Target definition
label_viral = 1 if a post’s engagement_rate is in the top 10% within its (platform, month) cohort; otherwise 0.

Evaluation
Submissions must contain two columns: row_id and viral_probability (probability in [0,1]).
Metric: Average Precision (AUPRC) computed on the hidden test labels.

Submission format
CSV with two columns and a header:
row_id,viral_probability
<id_1>,<p_1>
<id_2>,<p_2>
...
