# OpenMLE-fast task

Task ID: `rt-iot2022real-time-internet-of-things@1`

Native metric: `IoTAttackClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3044 bytes)
- `data/sample_submission.csv` (542406 bytes); columns: ["flow_id", "Attack_type"]
- `data/test.csv` (9930365 bytes); columns: ["flow_id", "id.orig_p", "id.resp_p", "proto", "service", "flow_duration", "fwd_pkts_tot", "bwd_pkts_tot", "fwd_data_pkts_tot", "bwd_data_pkts_tot", "fwd_pkts_per_sec", "bwd_pkts_per_sec", "flow_pkts_per_sec", "down_up_ratio", "fwd_header_size_tot", "fwd_header_size_min", "fwd_header_size_max", "bwd_header_size_tot", "bwd_header_size_min", "bwd_header_size_max", "flow_FIN_flag_count", "flow_SYN_flag_count", "flow_RST_flag_count", "fwd_PSH_flag_count", "bwd_PSH_flag_count", "flow_ACK_flag_count", "fwd_URG_flag_count", "bwd_URG_flag_count", "flow_CWR_flag_count", "flow_ECE_flag_count", "fwd_pkts_payload.min", "fwd_pkts_payload.max", "fwd_pkts_payload.tot", "fwd_pkts_payload.avg", "fwd_pkts_payload.std", "bwd_pkts_payload.min", "bwd_pkts_payload.max", "bwd_pkts_payload.tot", "bwd_pkts_payload.avg", "bwd_pkts_payload.std", "flow_pkts_payload.min", "flow_pkts_payload.max", "flow_pkts_payload.tot", "flow_pkts_payload.avg", "flow_pkts_payload.std", "fwd_iat.min", "fwd_iat.max", "fwd_iat.tot", "fwd_iat.avg", "fwd_iat.std", "bwd_iat.min", "bwd_iat.max", "bwd_iat.tot", "bwd_iat.avg", "bwd_iat.std", "flow_iat.min", "flow_iat.max", "flow_iat.tot", "flow_iat.avg", "flow_iat.std", "payload_bytes_per_second", "fwd_subflow_pkts", "bwd_subflow_pkts", "fwd_subflow_bytes", "bwd_subflow_bytes", "fwd_bulk_bytes", "bwd_bulk_bytes", "fwd_bulk_packets", "bwd_bulk_packets", "fwd_bulk_rate", "bwd_bulk_rate", "active.min", "active.max", "active.tot", "active.avg", "active.std", "idle.min", "idle.max", "idle.tot", "idle.avg", "idle.std", "fwd_init_window_size", "bwd_init_window_size", "fwd_last_window_size"]
- `data/train.csv` (41041057 bytes); columns: ["flow_id", "id.orig_p", "id.resp_p", "proto", "service", "flow_duration", "fwd_pkts_tot", "bwd_pkts_tot", "fwd_data_pkts_tot", "bwd_data_pkts_tot", "fwd_pkts_per_sec", "bwd_pkts_per_sec", "flow_pkts_per_sec", "down_up_ratio", "fwd_header_size_tot", "fwd_header_size_min", "fwd_header_size_max", "bwd_header_size_tot", "bwd_header_size_min", "bwd_header_size_max", "flow_FIN_flag_count", "flow_SYN_flag_count", "flow_RST_flag_count", "fwd_PSH_flag_count", "bwd_PSH_flag_count", "flow_ACK_flag_count", "fwd_URG_flag_count", "bwd_URG_flag_count", "flow_CWR_flag_count", "flow_ECE_flag_count", "fwd_pkts_payload.min", "fwd_pkts_payload.max", "fwd_pkts_payload.tot", "fwd_pkts_payload.avg", "fwd_pkts_payload.std", "bwd_pkts_payload.min", "bwd_pkts_payload.max", "bwd_pkts_payload.tot", "bwd_pkts_payload.avg", "bwd_pkts_payload.std", "flow_pkts_payload.min", "flow_pkts_payload.max", "flow_pkts_payload.tot", "flow_pkts_payload.avg", "flow_pkts_payload.std", "fwd_iat.min", "fwd_iat.max", "fwd_iat.tot", "fwd_iat.avg", "fwd_iat.std", "bwd_iat.min", "bwd_iat.max", "bwd_iat.tot", "bwd_iat.avg", "bwd_iat.std", "flow_iat.min", "flow_iat.max", "flow_iat.tot", "flow_iat.avg", "flow_iat.std", "payload_bytes_per_second", "fwd_subflow_pkts", "bwd_subflow_pkts", "fwd_subflow_bytes", "bwd_subflow_bytes", "fwd_bulk_bytes", "bwd_bulk_bytes", "fwd_bulk_packets", "bwd_bulk_packets", "fwd_bulk_rate", "bwd_bulk_rate", "active.min", "active.max", "active.tot", "active.avg", "active.std", "idle.min", "idle.max", "idle.tot", "idle.avg", "idle.std", "fwd_init_window_size", "bwd_init_window_size", "fwd_last_window_size", "Attack_type"]

## Public description

Title: Fine-grained IoT Network Flow Attack-Type Classification

Background
RT-IoT2022 captures bidirectional network flow features from an IoT organization under multiple attack scenarios and normal traffic patterns. Each flow includes 80+ behavioral features (payload metrics, inter-arrival times, flags, window sizes, ports) and categorical protocol/service indicators.

Problem statement
Given per-flow features, predict the exact attack type or normal pattern across 12 classes. Build a robust multi-class classifier that generalizes across diverse protocols/services and highly imbalanced traffic patterns.

Data provided
- train.csv: Tabular features for each network flow plus the target column Attack_type.
- test.csv: The same tabular features for held-out flows without labels.
- sample_submission.csv: Example submission file with the required columns.

Key notes
- A synthetic identifier column flow_id uniquely identifies each flow across files. Use it only for submission alignment; do not treat it as a predictive feature.
- Feature-identical duplicate flows were deduplicated before the split to prevent leakage; all remaining flows are unique by feature content.
- Strong class imbalance is present by design (e.g., DOS_SYN_Hping is majority while several attack types are rare). Robust modeling and evaluation are required.

Target classes
12 classes encompassing multiple attacks and normal traffic patterns, including DOS_SYN_Hping, ARP_poisioning, several NMAP scan variants, DDOS_Slowloris, Metasploit_Brute_Force_SSH, and normal classes such as MQTT_Publish, Thing_Speak, Wipro_bulb. The exact label set can be obtained from train.csv (unique values of Attack_type).

Evaluation metric
Macro F1 across all 12 classes.
- Macro F1 equally weights each class and directly measures the precision–recall trade-off.
- This choice prevents dominance by majority classes and encourages accurate detection of minority attacks.

Submission format
- CSV file with exactly two columns in order: flow_id and Attack_type.
- flow_id values must match those in test.csv.
- Attack_type values must be one of the valid class names in train.csv.

Recommended approach for participants
- Data processing: Robust handling of numeric features (standardization or robust scaling), one-hot encoding of categorical proto and service, optional log transforms for heavy-tailed rate features, dropping constant columns if any.
- Feature engineering: Derive interaction features or normalized ratios if helpful; consider domain-informed aggregates.
- Modeling: Try class-weighted linear models, tree ensembles (e.g., gradient boosting), or deep tabular networks. Address imbalance with class weights or focal loss.
- Evaluation: Use stratified cross-validation on train.csv to tune and validate; the official leaderboard metric uses the held-out test.csv labels.

Files for the competition
- Training data: train.csv
- Test data: test.csv
- Sample submission: sample_submission.csv

Your objective is to maximize Macro F1 on the held-out test set.
