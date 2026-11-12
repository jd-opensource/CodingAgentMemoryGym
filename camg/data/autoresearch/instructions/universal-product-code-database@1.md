# OpenMLE-fast task

Task ID: `universal-product-code-database@1`

Native metric: `UPCMatchingMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2988 bytes)
- `data/sample_submission.csv` (44880 bytes); columns: ["id", "score"]
- `data/test.csv` (480190 bytes); columns: ["id", "name1", "name2"]
- `data/train.csv` (2082183 bytes); columns: ["id", "name1", "name2", "label"]

## Public description

Title: Product Title Matching via UPC Ground Truth

Problem statement
Online marketplaces aggregate listings from many sellers. The same physical item often appears under slightly different titles (languages, abbreviations, sizes, punctuation). Your task is to predict whether two product titles refer to the exact same trade item. We use the UPC/EAN code as the authoritative ground truth of sameness to derive labels, but the codes themselves are not provided in the modeling inputs.

What you need to do
Given a pair of product titles (name1, name2), produce a match probability score in [0, 1] indicating how likely the titles refer to the same product.

Data description
The data is derived from a large corpus of product titles and their UPC/EAN identifiers. Labels are built using strict equality on the identifier:
- Positive (label=1): two titles share the exact same identifier.
- Negative (label=0): two titles come from different identifiers.

You are provided with pairwise datasets constructed to be realistic and challenging:
- train_pairs.csv: id, name1, name2, label
- test_pairs.csv: id, name1, name2
- sample_submission.csv: id, score

The train and test splits are constructed by partitioning identifiers: all pairs involving a given identifier appear in only one split. This prevents leakage from memorizing specific pairs across splits. Titles are messy, multilingual, and include numbers (sizes, counts, volumes). Negative pairs are sampled using hard-blocking heuristics (e.g., shared tokens or numbers) to be non-trivial.

Evaluation
Submissions must be a CSV with columns: id, score
- id must match exactly the ids provided in test_pairs.csv (one row per id, no duplicates, no missing/extra ids).
- score is a real number; higher means more likely to be a match.

Metric: Average Precision (AP)
We compute the micro-averaged Average Precision on the entire test set by ranking test pairs in descending order of score and averaging the precision at ranks where true positives occur. AP is well-suited for imbalanced binary classification and rewards ranking true matches higher than non-matches without requiring a fixed threshold.

Rules and notes
- Only the provided textual titles are inputs; no identifier columns are given in the pairs files to avoid trivial solutions.
- The distribution is imbalanced (non-matches outnumber matches). Calibrated probabilities are not required; the metric evaluates ranking quality.
- You may use any ML techniques for text similarity and entity resolution, including feature engineering, vectorization, learned embeddings, and cross-encoders.

Files you will see
- train_pairs.csv: training pairs with labels for supervised learning
- test_pairs.csv: test pairs without labels
- sample_submission.csv: a sample submission template with placeholder scores

Submission format
- CSV with columns: id, score
- Include each id exactly once, and no other columns.

Good luck, and have fun building robust product-matching models!
