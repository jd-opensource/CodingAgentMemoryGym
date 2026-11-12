# OpenMLE-fast task

Task ID: `huntington-disease-dataset@1`

Native metric: `HuntingtonDiseaseStagingMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3487 bytes)
- `data/sample_submission.csv` (441563 bytes); columns: ["Patient_ID", "Disease_Stage"]
- `data/test.csv` (1480911 bytes); columns: ["Patient_ID", "Age", "Sex", "Family_History", "HTT_CAG_Repeat_Length", "Gene_Mutation_Type", "HTT_Gene_Expression_Level", "Protein_Aggregation_Level", "Gene/Factor", "Chromosome_Location", "Function", "Effect", "Category"]
- `data/train.csv` (6252955 bytes); columns: ["Patient_ID", "Age", "Sex", "Family_History", "HTT_CAG_Repeat_Length", "Gene_Mutation_Type", "HTT_Gene_Expression_Level", "Protein_Aggregation_Level", "Gene/Factor", "Chromosome_Location", "Function", "Effect", "Category", "Disease_Stage"]

## Public description

Title: Ordinal Staging of Huntington’s Disease from Genetics and Biomarkers

Problem statement
Predict the clinical disease stage of Huntington’s disease (HD) patients using demographic, genetic, and molecular biomarkers captured at a single visit. The target, Disease_Stage, is an ordered category with four levels: Pre-Symptomatic < Early < Middle < Late. The challenge emphasizes order-aware modeling and robust handling of heterogeneous tabular features.

Files provided
- train.csv: Feature matrix with the target label Disease_Stage.
- test.csv: Feature matrix without labels; same schema as train.csv except for the missing target.
- sample_submission.csv: A template demonstrating the exact submission format.

Columns in train/test
- Patient_ID: Unique identifier for each patient (used to align submissions; do not train on it).
- Age: Age at data collection (numeric).
- Sex: Biological sex (categorical).
- Family_History: Family history of HD (categorical Yes/No).
- HTT_CAG_Repeat_Length: CAG repeat length in the HTT gene (numeric).
- Gene_Mutation_Type: Mutation type (categorical; e.g., Insertion/Deletion/Duplication/Point Mutation).
- HTT_Gene_Expression_Level: HTT gene expression level proxy (numeric).
- Protein_Aggregation_Level: Huntingtin protein aggregation level proxy (numeric).
- Gene/Factor: Gene or biological factor associated with progression (categorical; e.g., HTT, MLH1, MSH3).
- Chromosome_Location: Genomic locus (categorical; e.g., 4p16.3).
- Function: Biological function annotation (categorical).
- Effect: Functional impact annotation (categorical).
- Category: Broad biological category (categorical).
- Disease_Stage: Target label (only in train.csv). One of: Pre-Symptomatic, Early, Middle, Late.

Important note on provided schema
To prevent trivial solutions and label leakage, variables that directly encode clinical severity, imaging severity proxies, or explicit random/noise controls have been removed from the provided train/test schema. The provided columns focus modeling on genetics, biomarkers, and demographics.

Submission format
- A CSV with exactly two columns and this exact header:
  - Patient_ID
  - Disease_Stage
- Each Patient_ID from test.csv must appear exactly once.
- Disease_Stage must be one of: Pre-Symptomatic, Early, Middle, Late.

Evaluation
- Metric: Quadratic Weighted Kappa (QWK)
  - Disease_Stage is mapped to ordered integers: Pre-Symptomatic→0, Early→1, Middle→2, Late→3.
  - QWK rewards order-aware predictions and penalizes larger disagreements more than smaller ones.
  - Scoring aligns rows by Patient_ID and ignores submission order.

Guidance and considerations
- Categorical handling: Several columns have moderate to high cardinality; consider one-hot encoding with regularization, target-agnostic encoders, and grouping rare levels.
- Numeric preprocessing: Robust scaling or clipping can help with heteroscedastic biomarkers.
- Ordinal modeling: Explore ordinal regression losses, threshold-based approaches on a latent score, or calibrated probability estimates optimized for QWK.
- Feature interactions: Nonlinear interactions (e.g., Age × HTT_CAG_Repeat_Length × modifier genes) can be important; gradient boosting and tabular neural networks are natural fits.

Reproducibility
The official split is stratified by Disease_Stage with a fixed random seed. sample_submission.csv contains valid, randomized labels from the allowed set to illustrate format without revealing answers.
