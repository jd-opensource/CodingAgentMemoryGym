# OpenMLE-fast task

Task ID: `students-performance-dataset-in-physics-education@1`

Native metric: `PhysicsPostTestScoreMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2876 bytes)
- `data/sample_submission.csv` (2416 bytes); columns: ["STUDID", "FINTEST2"]
- `data/test.csv` (229702 bytes); columns: ["STUDID", "SCH", "COH", "GDR", "AGE", "FATHOCC", "MOTHOCC", "FATHEDU", "MOTHEDU", "FATHINC", "MOTHINC", "SIBL", "DOM", "LIT1", "LIT2", "PHYIDE1", "PHYIDE2", "FINTEST1", "FCI1", "FCI2", "FCI3", "FCI4", "FCI5", "FCI6", "FCI7", "FCI8", "FCI9", "FCI10", "FCI11", "FCI12", "FCI13", "FCI14", "FCI15", "FCI16", "FCI17", "FCI18", "FCI19", "FCI20", "FCI21", "FCI22", "FCI23", "FCI24", "FCI25", "FCI26", "FCI27", "FCI28", "FCI29", "FCI30", "FMCE1", "FMCE2", "FMCE3", "FMCE4", "FMCE5", "FMCE6", "FMCE7", "FMCE8", "FMCE9", "FMCE10", "FMCE11", "FMCE12", "FMCE13", "FMCE14", "FMCE15", "FMCE16", "FMCE17", "FMCE18", "FMCE19", "FMCE20", "FMCE21", "FMCE22", "FMCE23", "FMCE24", "FMCE25", "FMCE26", "FMCE27", "FMCE28", "FMCE29", "FMCE30", "FMCE31", "FMCE32", "FMCE33", "FMCE34", "FMCE35", "FMCE36", "FMCE37", "FMCE38", "FMCE39", "FMCE40", "FMCE41", "FMCE42", "FMCE43", "FMCE44", "FMCE45", "FMCE46", "FMCE47", "FMCE46a", "RRMCS1", "RRMCS2", "RRMCS3", "RRMCS4", "RRMCS5", "RRMCS6", "RRMCS7", "RRMCS8", "RRMCS9", "RRMCS10", "RRMCS11", "RRMCS12", "RRMCS13", "RRMCS14", "RRMCS15", "RRMCS16", "RRMCS17", "RRMCS18", "RRMCS19", "RRMCS20", "RRMCS21", "RRMCS22", "RRMCS23", "RRMCS24", "RRMCS25", "RRMCS26", "RRMCS27", "RRMCS28", "RRMCS29", "RRMCS30", "RRMCS1a", "RRMCS2a", "RRMCS3a", "RRMCS4a", "RRMCS5a", "RRMCS6a", "RRMCS7a", "RRMCS8a", "RRMCS9a", "RRMCS10a", "RRMCS11a", "RRMCS12a", "RRMCS13a", "RRMCS14a", "RRMCS15a", "RRMCS16a", "RRMCS17a", "RRMCS18a", "RRMCS19a", "RRMCS20a", "RRMCS21a", "RRMCS22a", "RRMCS23a", "RRMCS24a", "RRMCS25a", "RRMCS26a", "RRMCS27a", "RRMCS28a", "RRMCS29a", "RRMCS30a", "FMCI1", "FMCI2", "FMCI3", "FMCI4", "FMCI5", "FMCI6", "FMCI7", "FMCI8", "FMCI9", "FMCI10", "FMCI11", "FMCI12", "FMCI13", "FMCI14", "FMCI15", "FMCI16", "FMCI17", "FMCI18", "FMCI19", "FMCI20", "FMCI21", "FMCI22", "FMCI23", "FMCI24", "FMCI25", "FMCI26", "FMCI27", "FMCI28", "FMCI29", "FMCI30", "FMCI31", "FMCI32", "MWCS1", "MWCS2", "MWCS3", "MWCS4", "MWCS5", "MWCS6", "MWCS7", "MWCS8", "MWCS9", "MWCS10", "MWCS11", "MWCS12", "MWCS13", "MWCS14", "MWCS15", "MWCS16", "MWCS17", "MWCS18", "MWCS19", "MWCS20", "MWCS21", "MWCS22", "TCE1", "TCE2", "TCE3", "TCE4", "TCE5", "TCE6", "TCE7", "TCE8", "TCE9", "TCE10", "TCE11", "TCE12", "TCE13", "TCE14", "TCE15", "TCE16", "TCE17", "TCE18", "TCE19", "TCE20", "TCE21", "TCE22", "TCE23", "TCE24", "TCE25", "TCE26", "STPFaSL1", "STPFaSL2", "STPFaSL3", "STPFaSL4", "STPFaSL5", "STPFaSL6", "STPFaSL7", "STPFaSL8", "STPFaSL9", "STPFaSL10", "STPFaSL11", "STPFaSL12", "STPFaSL13", "STPFaSL14", "STPFaSL15", "STPFaSL16", "STPFaSL17", "STPFaSL18", "STPFaSL19", "STPFaSL20", "STPFaSL21", "STPFaSL22", "STPFaSL23", "STPFaSL24", "STPFaSL25", "STPFaSL26", "STPFaSL27", "STPFaSL28", "STPFaSL29", "STPFaSL30", "STPFaSL31", "STPFaSL32", "STPFaSL33", "LABGR", "SAAR-B1", "SAAR-B2", "SAAR-B3", "SAAR-B4", "SAAR-B5", "SAAR-B6", "SAAR-B7", "SAAR-B8", "SAAR-B9", "SAAR-F10", "SAAR-F11", "SAAR-G12", "SAAR-G13", "SAAR-G14", "SAAR-G15", "SAAR-G16", "CLASS1", "CLASS2", "CLASS3", "CLASS4", "CLASS5", "CLASS6", "CLASS7", "CLASS8", "CLASS9", "CLASS10", "CLASS11", "CLASS12", "CLASS13", "CLASS14", "CLASS15", "CLASS16", "CLASS17", "CLASS18", "CLASS19", "CLASS20", "CLASS21", "CLASS22", "CLASS23", "CLASS24", "CLASS25", "CLASS26", "CLASS27", "CLASS28", "CLASS29", "CLASS30", "CLASS31", "CLASS32", "CLASS33", "CLASS34", "CLASS35", "CLASS36", "CLASS37", "CLASS38", "CLASS39", "CLASS40", "CLASS41", "CLASS42"]
- `data/train.csv` (1073261 bytes); columns: ["STUDID", "SCH", "COH", "GDR", "AGE", "FATHOCC", "MOTHOCC", "FATHEDU", "MOTHEDU", "FATHINC", "MOTHINC", "SIBL", "DOM", "LIT1", "LIT2", "PHYIDE1", "PHYIDE2", "FINTEST1", "FINTEST2", "FCI1", "FCI2", "FCI3", "FCI4", "FCI5", "FCI6", "FCI7", "FCI8", "FCI9", "FCI10", "FCI11", "FCI12", "FCI13", "FCI14", "FCI15", "FCI16", "FCI17", "FCI18", "FCI19", "FCI20", "FCI21", "FCI22", "FCI23", "FCI24", "FCI25", "FCI26", "FCI27", "FCI28", "FCI29", "FCI30", "FMCE1", "FMCE2", "FMCE3", "FMCE4", "FMCE5", "FMCE6", "FMCE7", "FMCE8", "FMCE9", "FMCE10", "FMCE11", "FMCE12", "FMCE13", "FMCE14", "FMCE15", "FMCE16", "FMCE17", "FMCE18", "FMCE19", "FMCE20", "FMCE21", "FMCE22", "FMCE23", "FMCE24", "FMCE25", "FMCE26", "FMCE27", "FMCE28", "FMCE29", "FMCE30", "FMCE31", "FMCE32", "FMCE33", "FMCE34", "FMCE35", "FMCE36", "FMCE37", "FMCE38", "FMCE39", "FMCE40", "FMCE41", "FMCE42", "FMCE43", "FMCE44", "FMCE45", "FMCE46", "FMCE47", "FMCE46a", "RRMCS1", "RRMCS2", "RRMCS3", "RRMCS4", "RRMCS5", "RRMCS6", "RRMCS7", "RRMCS8", "RRMCS9", "RRMCS10", "RRMCS11", "RRMCS12", "RRMCS13", "RRMCS14", "RRMCS15", "RRMCS16", "RRMCS17", "RRMCS18", "RRMCS19", "RRMCS20", "RRMCS21", "RRMCS22", "RRMCS23", "RRMCS24", "RRMCS25", "RRMCS26", "RRMCS27", "RRMCS28", "RRMCS29", "RRMCS30", "RRMCS1a", "RRMCS2a", "RRMCS3a", "RRMCS4a", "RRMCS5a", "RRMCS6a", "RRMCS7a", "RRMCS8a", "RRMCS9a", "RRMCS10a", "RRMCS11a", "RRMCS12a", "RRMCS13a", "RRMCS14a", "RRMCS15a", "RRMCS16a", "RRMCS17a", "RRMCS18a", "RRMCS19a", "RRMCS20a", "RRMCS21a", "RRMCS22a", "RRMCS23a", "RRMCS24a", "RRMCS25a", "RRMCS26a", "RRMCS27a", "RRMCS28a", "RRMCS29a", "RRMCS30a", "FMCI1", "FMCI2", "FMCI3", "FMCI4", "FMCI5", "FMCI6", "FMCI7", "FMCI8", "FMCI9", "FMCI10", "FMCI11", "FMCI12", "FMCI13", "FMCI14", "FMCI15", "FMCI16", "FMCI17", "FMCI18", "FMCI19", "FMCI20", "FMCI21", "FMCI22", "FMCI23", "FMCI24", "FMCI25", "FMCI26", "FMCI27", "FMCI28", "FMCI29", "FMCI30", "FMCI31", "FMCI32", "MWCS1", "MWCS2", "MWCS3", "MWCS4", "MWCS5", "MWCS6", "MWCS7", "MWCS8", "MWCS9", "MWCS10", "MWCS11", "MWCS12", "MWCS13", "MWCS14", "MWCS15", "MWCS16", "MWCS17", "MWCS18", "MWCS19", "MWCS20", "MWCS21", "MWCS22", "TCE1", "TCE2", "TCE3", "TCE4", "TCE5", "TCE6", "TCE7", "TCE8", "TCE9", "TCE10", "TCE11", "TCE12", "TCE13", "TCE14", "TCE15", "TCE16", "TCE17", "TCE18", "TCE19", "TCE20", "TCE21", "TCE22", "TCE23", "TCE24", "TCE25", "TCE26", "STPFaSL1", "STPFaSL2", "STPFaSL3", "STPFaSL4", "STPFaSL5", "STPFaSL6", "STPFaSL7", "STPFaSL8", "STPFaSL9", "STPFaSL10", "STPFaSL11", "STPFaSL12", "STPFaSL13", "STPFaSL14", "STPFaSL15", "STPFaSL16", "STPFaSL17", "STPFaSL18", "STPFaSL19", "STPFaSL20", "STPFaSL21", "STPFaSL22", "STPFaSL23", "STPFaSL24", "STPFaSL25", "STPFaSL26", "STPFaSL27", "STPFaSL28", "STPFaSL29", "STPFaSL30", "STPFaSL31", "STPFaSL32", "STPFaSL33", "LABGR", "SAAR-B1", "SAAR-B2", "SAAR-B3", "SAAR-B4", "SAAR-B5", "SAAR-B6", "SAAR-B7", "SAAR-B8", "SAAR-B9", "SAAR-F10", "SAAR-F11", "SAAR-G12", "SAAR-G13", "SAAR-G14", "SAAR-G15", "SAAR-G16", "CLASS1", "CLASS2", "CLASS3", "CLASS4", "CLASS5", "CLASS6", "CLASS7", "CLASS8", "CLASS9", "CLASS10", "CLASS11", "CLASS12", "CLASS13", "CLASS14", "CLASS15", "CLASS16", "CLASS17", "CLASS18", "CLASS19", "CLASS20", "CLASS21", "CLASS22", "CLASS23", "CLASS24", "CLASS25", "CLASS26", "CLASS27", "CLASS28", "CLASS29", "CLASS30", "CLASS31", "CLASS32", "CLASS33", "CLASS34", "CLASS35", "CLASS36", "CLASS37", "CLASS38", "CLASS39", "CLASS40", "CLASS41", "CLASS42"]

## Public description

Title: SPHERE Post-Test Score Prediction (Eleventh-Grade Physics)

Problem statement
Build a model that predicts each student’s end-of-course physics post-test score (FINTEST2) using rich pre-course information: demographics, prior achievement (FINTEST1), item-level responses on research-based physics concept inventories, scientific ability measures, and learning attitudes. The goal is robust generalization across schools and cohorts.

Files provided
- train.csv: Training data with all features and the target column FINTEST2.
- test.csv: Test data with the same features; FINTEST2 is not included.
- sample_submission.csv: Example submission file with STUDID and a FINTEST2 prediction column.

Data overview
- Each row represents one eleventh-grade student.
- Feature groups include:
  - Demographics and context: SCH (school), COH (cohort), GDR (gender), AGE, parental occupation/education/income, siblings, domicile, literacy, physics identity.
  - Concept inventories (item-level multiple choice, often A–E/A–J): FCI1–FCI30, FMCE1–FMCE47 (+ FMCE46a), RRMCS1–RRMCS30 (+ RRMCS1a–RRMCS30a), FMCI1–FMCI32, MWCS1–MWCS22, TCE1–TCE26, STPFaSL1–STPFaSL33.
  - Scientific ability: LABGR; SAAR-B1..B9, SAAR-F10..F11, SAAR-G12..G16.
  - Attitudes: CLASS1–CLASS42.
  - FINTEST1 (pre-test). The target FINTEST2 is included only in train.csv.
- Several columns contain free-text justifications (Indonesian/English). Treat them as auxiliary features with standard text processing.

Evaluation
- Metric: Root Mean Squared Error (RMSE) computed on the hidden test labels.
  - Lower RMSE is better; it penalizes larger errors more strongly and is precise for continuous scores.

Submission format
- A CSV file with exactly two columns in order: STUDID, FINTEST2.
- STUDID must match the IDs in test.csv; one row per test sample; no duplicates or missing IDs.
- FINTEST2 predictions must be numeric and finite.

Train/test split protocol
- Deterministic 80/20 split with a fixed seed, stratified by SCH and COH when possible, ensuring disjoint STUDID sets.
- FINTEST2 is present only in train.csv and withheld in test.csv.

Modeling guidance
- Use the full dataset; do not subset.
- Multiple-choice item columns should be treated as categorical features (not ordinals). Handle missing values explicitly (e.g., a dedicated category).
- Numeric fields: impute missing values reasonably (median/mean), scale/normalize if helpful.
- Text fields: handle multilingual content via simple bag-of-ngrams/TF-IDF or multilingual embeddings; clean minimal artifacts while preserving meaning.
- Prevent leakage: Do not attempt to infer the hidden test labels from file order or external cues; use features only.

Goal
Leverage multimodal feature engineering and robust ML training to minimize RMSE on FINTEST2 while ensuring strong generalization across schools and cohorts.
