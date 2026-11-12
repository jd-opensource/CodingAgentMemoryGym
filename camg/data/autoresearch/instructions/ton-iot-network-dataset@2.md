# OpenMLE-fast task

Task ID: `ton-iot-network-dataset@2`

Native metric: `TonIoTNetworkClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3555 bytes)
- `data/sample_submission.csv` (593020 bytes); columns: ["row_id", "type"]
- `data/test.csv` (5950382 bytes); columns: ["row_id", "src_ip", "src_port", "dst_ip", "dst_port", "proto", "service", "duration", "src_bytes", "dst_bytes", "conn_state", "missed_bytes", "src_pkts", "src_ip_bytes", "dst_pkts", "dst_ip_bytes", "dns_query", "dns_qclass", "dns_qtype", "dns_rcode", "dns_AA", "dns_RD", "dns_RA", "dns_rejected", "ssl_version", "ssl_cipher", "ssl_resumed", "ssl_established", "ssl_subject", "ssl_issuer", "http_trans_depth", "http_method", "http_uri", "http_version", "http_request_body_len", "http_response_body_len", "http_status_code", "http_user_agent", "http_orig_mime_types", "http_resp_mime_types", "weird_name", "weird_addl", "weird_notice"]
- `data/train.csv` (24374814 bytes); columns: ["row_id", "src_ip", "src_port", "dst_ip", "dst_port", "proto", "service", "duration", "src_bytes", "dst_bytes", "conn_state", "missed_bytes", "src_pkts", "src_ip_bytes", "dst_pkts", "dst_ip_bytes", "dns_query", "dns_qclass", "dns_qtype", "dns_rcode", "dns_AA", "dns_RD", "dns_RA", "dns_rejected", "ssl_version", "ssl_cipher", "ssl_resumed", "ssl_established", "ssl_subject", "ssl_issuer", "http_trans_depth", "http_method", "http_uri", "http_version", "http_request_body_len", "http_response_body_len", "http_status_code", "http_user_agent", "http_orig_mime_types", "http_resp_mime_types", "weird_name", "weird_addl", "weird_notice", "type"]

## Public description

Competition: TON_IoT Attack Type Classification

Problem statement
Given per-flow network telemetry from a realistic smart IoT/IIoT environment, predict the attack type among 10 classes (including normal traffic) for unseen devices. You are provided transport- and application-layer features extracted with tools like Argus/Zeek. The challenge is to build models that generalize across devices while handling heavy class imbalance and high-cardinality categorical fields.

Data description
- A single tabular dataset of 211,043 network flows with a multiclass target.
- Target: type (10 classes; includes normal and 9 attack categories such as ddos, dos, backdoor, ransomware, password, scanning, injection, xss, mitm).
- Features: All columns except the binary label column (label) and the target (type). Typical fields include addresses/ports, protocol, duration, bytes/packets, connection state, and optional application-layer artifacts (DNS/HTTP/SSL/weird fields). Missing values appear as '-' or are empty; treat as explicit missing category or impute as you see fit. Do not drop rows.
- High-missing fields (e.g., DNS/HTTP/SSL/weird) are intentionally retained; their presence is informative.

Files provided to participants
- train.csv: Training set with features and the target column type. Includes a row_id column for unique row identity.
- test.csv: Test set with the same feature columns and row_id, but without type.
- sample_submission.csv: A sample submission file with the required format.

Train/Test construction policy (already prepared for you)
- The split is performed by grouping on src_ip to simulate unseen devices in the test set and reduce leakage from trivial IP memorization.
- The split is stratified at the group level to include as many classes as possible in the test set while ensuring that every class appearing in test also appears at least once in train.
- The approximate split proportion is 80% train / 20% test by number of rows.

Evaluation
- Metric: Macro-averaged F1 across the 10 classes. For each class, F1 is computed as the harmonic mean of precision and recall, and the final score is the unweighted average across classes present in the ground truth. This metric treats rare classes (e.g., mitm) on equal footing with majority classes (e.g., normal), rewarding robust per-class performance.

Submission format
- File name: submission.csv
- Required columns: row_id, type
- Row order does not matter, but row_id values must exactly match those in test.csv. Predicted labels must be one of the valid class names used in type. See sample_submission.csv for reference.

Modeling guidance (optional)
- Useful preprocessing: cast numeric fields (durations, bytes, packets, lengths, status codes) to numeric types; keep categorical fields as strings; treat '-' as missing. Consider one-hot encoding of low-cardinality categories and hashing/target encoding/embeddings for high-cardinality text-like fields (e.g., dns_query, http_uri, http_user_agent).
- Potential features: bytes/packets ratios, packet rate, directional asymmetry, private/public IP flags, port bucketization and service/port consistency, presence flags for application-layer artifacts.
- Class imbalance: cost-sensitive losses, class weighting, or focal loss can improve performance on rare classes.

Final deliverables for participants
- Use train.csv to train your model.
- Generate predictions for test.csv and produce a submission.csv with columns row_id and type.
- Your submission will be evaluated by the macro F1 metric as defined above.
