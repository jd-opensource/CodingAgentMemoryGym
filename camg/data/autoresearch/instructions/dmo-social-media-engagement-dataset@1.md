# OpenMLE-fast task

Task ID: `dmo-social-media-engagement-dataset@1`

Native metric: `SocialMediaEngagementRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (968 bytes)
- `data/sample_submission.csv` (109394 bytes); columns: ["row_id", "normalized_engagement_rate"]
- `data/test.csv` (2201384 bytes); columns: ["row_id", "State", "Date1", "OpnHours", "DateDay", "Day", "Time", "3-Phase", "4-phase", "Followers", "Status text", "Vividness", "ContentType", "WC", "Clout", "Cognition", "Affect", "emotion", "emo_pos", "emo_neg", "we__1", "tentat", "Drives", "i", "we__2", "they", "insight", "cause", "discrep", "certitude", "Positive", "Negative", "Total_Sentiment"]
- `data/train.csv` (8793456 bytes); columns: ["row_id", "State", "Date1", "OpnHours", "DateDay", "Day", "Time", "3-Phase", "4-phase", "Followers", "Status text", "Vividness", "ContentType", "WC", "Clout", "Cognition", "Affect", "emotion", "emo_pos", "emo_neg", "we__1", "tentat", "Drives", "i", "we__2", "they", "insight", "cause", "discrep", "certitude", "Positive", "Negative", "Total_Sentiment", "normalized_engagement_rate"]

## Public description

Title: Social Media Engagement Rate Prediction for DMOs

Problem statement:
Predict the normalized engagement rate for each tweet from Indian Destination Marketing Organizations (DMOs).
Given tweet text and metadata, build a model that estimates normalized engagement per 1000 followers.

Data files provided:
- train.csv: Features and the target column normalized_engagement_rate.
- test.csv: Features only with a row_id column for submission mapping.
- sample_submission.csv: Example file containing row_id and a dummy normalized_engagement_rate prediction.

Submission format:
- CSV with two columns: row_id and normalized_engagement_rate.
- One row per entry in test.csv; predictions must be numeric and non-negative.

Evaluation metric:
- Root Mean Squared Log Error (RMSLE).
  Computation: sqrt(mean((log1p(pred) - log1p(true))^2)).

Notes:
- Engagement-derived fields (like_count, retweet_count, reply_count, quote_count, Buzz) are excluded from model features.
