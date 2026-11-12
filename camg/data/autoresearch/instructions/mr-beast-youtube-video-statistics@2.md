# OpenMLE-fast task

Task ID: `mr-beast-youtube-video-statistics@2`

Native metric: `MrBeastPairwiseAUCMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4762 bytes)
- `data/sample_submission.csv` (13012 bytes); columns: ["pair_id", "target"]
- `data/test.csv` (483663 bytes); columns: ["pair_id", "a_video", "a_thumb", "a_title", "a_description", "a_tags", "a_topicCategories", "a_defaultLanguage", "a_loc_en_title", "a_loc_en_description", "a_publishTime", "a_duration_seconds", "a_duration_iso", "a_likeCount", "a_commentCount", "a_dimension", "a_ytRating", "b_video", "b_thumb", "b_title", "b_description", "b_tags", "b_topicCategories", "b_defaultLanguage", "b_loc_en_title", "b_loc_en_description", "b_publishTime", "b_duration_seconds", "b_duration_iso", "b_likeCount", "b_commentCount", "b_dimension", "b_ytRating"]
- `data/test_images/img_0169.jpg` (39876 bytes)
- `data/test_images/img_0170.jpg` (37874 bytes)
- `data/test_images/img_0171.jpg` (47366 bytes)
- `data/test_images/img_0172.jpg` (44626 bytes)
- `data/test_images/img_0173.jpg` (41375 bytes)
- `data/test_images/img_0174.jpg` (24294 bytes)
- `data/test_images/img_0175.jpg` (51318 bytes)
- `data/test_images/img_0176.jpg` (43325 bytes)
- `data/test_images/img_0177.jpg` (16951 bytes)
- `data/test_images/img_0178.jpg` (32497 bytes)
- `data/test_images/img_0179.jpg` (34009 bytes)
- `data/test_images/img_0180.jpg` (29101 bytes)
- `data/test_images/img_0181.jpg` (11681 bytes)
- `data/test_images/img_0182.jpg` (37476 bytes)
- `data/test_images/img_0183.jpg` (23656 bytes)
- `data/test_images/img_0184.jpg` (41646 bytes)
- `data/test_images/img_0185.jpg` (46309 bytes)
- `data/test_images/img_0186.jpg` (41534 bytes)
- `data/test_images/img_0187.jpg` (61264 bytes)
- `data/test_images/img_0188.jpg` (33809 bytes)
- `data/test_images/img_0189.jpg` (11883 bytes)
- `data/test_images/img_0190.jpg` (41638 bytes)
- `data/test_images/img_0191.jpg` (34417 bytes)
- `data/test_images/img_0192.jpg` (42967 bytes)
- `data/test_images/img_0193.jpg` (33814 bytes)
- `data/test_images/img_0194.jpg` (47073 bytes)
- `data/test_images/img_0195.jpg` (31016 bytes)
- `data/test_images/img_0196.jpg` (28121 bytes)
- `data/test_images/img_0197.jpg` (27635 bytes)
- `data/test_images/img_0198.jpg` (44384 bytes)
- `data/test_images/img_0199.jpg` (38239 bytes)
- `data/test_images/img_0200.jpg` (39736 bytes)
- `data/test_images/img_0201.jpg` (55361 bytes)
- `data/test_images/img_0202.jpg` (34877 bytes)
- `data/test_images/img_0203.jpg` (54779 bytes)
- `data/test_images/img_0204.jpg` (41911 bytes)
- `data/test_images/img_0205.jpg` (42520 bytes)
- `data/test_images/img_0206.jpg` (45568 bytes)
- `data/test_images/img_0207.jpg` (41522 bytes)
- `data/test_images/img_0208.jpg` (44726 bytes)
- `data/test_images/img_0209.jpg` (46055 bytes)
- `data/test_images/img_0210.jpg` (38455 bytes)
- `data/test_images/img_0211.jpg` (35744 bytes)
- `data/train.csv` (3011884 bytes); columns: ["pair_id", "a_video", "a_thumb", "a_title", "a_description", "a_tags", "a_topicCategories", "a_defaultLanguage", "a_loc_en_title", "a_loc_en_description", "a_publishTime", "a_duration_seconds", "a_duration_iso", "a_likeCount", "a_commentCount", "a_dimension", "a_ytRating", "b_video", "b_thumb", "b_title", "b_description", "b_tags", "b_topicCategories", "b_defaultLanguage", "b_loc_en_title", "b_loc_en_description", "b_publishTime", "b_duration_seconds", "b_duration_iso", "b_likeCount", "b_commentCount", "b_dimension", "b_ytRating", "target"]
- `data/train_images/img_0001.jpg` (18575 bytes)
- `data/train_images/img_0002.jpg` (18971 bytes)
- `data/train_images/img_0003.jpg` (18355 bytes)
- `data/train_images/img_0004.jpg` (17896 bytes)
- `data/train_images/img_0005.jpg` (13286 bytes)
- `data/train_images/img_0006.jpg` (17100 bytes)
- `data/train_images/img_0007.jpg` (18988 bytes)
- `data/train_images/img_0008.jpg` (26265 bytes)
- `data/train_images/img_0009.jpg` (26447 bytes)
- `data/train_images/img_0010.jpg` (35690 bytes)
- `data/train_images/img_0011.jpg` (15858 bytes)
- `data/train_images/img_0012.jpg` (10829 bytes)
- `data/train_images/img_0013.jpg` (24129 bytes)
- `data/train_images/img_0014.jpg` (22658 bytes)
- `data/train_images/img_0015.jpg` (24934 bytes)
- `data/train_images/img_0016.jpg` (17863 bytes)
- `data/train_images/img_0017.jpg` (33124 bytes)
- `data/train_images/img_0018.jpg` (22603 bytes)
- `data/train_images/img_0019.jpg` (33490 bytes)
- `data/train_images/img_0020.jpg` (28049 bytes)
- `data/train_images/img_0021.jpg` (32800 bytes)
- `data/train_images/img_0022.jpg` (38772 bytes)
- `data/train_images/img_0023.jpg` (40550 bytes)
- `data/train_images/img_0024.jpg` (24312 bytes)
- `data/train_images/img_0025.jpg` (43278 bytes)
- `data/train_images/img_0026.jpg` (39754 bytes)
- `data/train_images/img_0027.jpg` (38466 bytes)
- `data/train_images/img_0028.jpg` (34896 bytes)
- `data/train_images/img_0029.jpg` (29670 bytes)
- `data/train_images/img_0030.jpg` (35528 bytes)
- `data/train_images/img_0031.jpg` (29394 bytes)
- `data/train_images/img_0032.jpg` (21652 bytes)
- `data/train_images/img_0033.jpg` (31878 bytes)
- `data/train_images/img_0034.jpg` (38115 bytes)
- `data/train_images/img_0035.jpg` (21299 bytes)
- `data/train_images/img_0036.jpg` (27577 bytes)
- `data/train_images/img_0037.jpg` (13627 bytes)
- `data/train_images/img_0038.jpg` (17852 bytes)
- `data/train_images/img_0039.jpg` (30720 bytes)
- `data/train_images/img_0040.jpg` (23367 bytes)
- `data/train_images/img_0041.jpg` (35356 bytes)
- `data/train_images/img_0042.jpg` (17532 bytes)
- `data/train_images/img_0043.jpg` (29612 bytes)
- `data/train_images/img_0044.jpg` (18823 bytes)
- `data/train_images/img_0045.jpg` (28653 bytes)
- `data/train_images/img_0046.jpg` (79243 bytes)
- `data/train_images/img_0047.jpg` (97776 bytes)
- `data/train_images/img_0048.jpg` (19463 bytes)
- `data/train_images/img_0049.jpg` (30619 bytes)
- `data/train_images/img_0050.jpg` (40847 bytes)
- `data/train_images/img_0051.jpg` (29885 bytes)
- `data/train_images/img_0052.jpg` (18069 bytes)
- `data/train_images/img_0053.jpg` (28750 bytes)
- `data/train_images/img_0054.jpg` (32711 bytes)
- `data/train_images/img_0055.jpg` (21721 bytes)
- `data/train_images/img_0056.jpg` (20022 bytes)
- `data/train_images/img_0057.jpg` (37043 bytes)
- `data/train_images/img_0058.jpg` (27427 bytes)
- `data/train_images/img_0059.jpg` (25236 bytes)
- `data/train_images/img_0060.jpg` (49371 bytes)
- `data/train_images/img_0061.jpg` (33605 bytes)
- `data/train_images/img_0062.jpg` (35910 bytes)
- `data/train_images/img_0063.jpg` (29389 bytes)
- `data/train_images/img_0064.jpg` (49327 bytes)
- `data/train_images/img_0065.jpg` (58227 bytes)
- `data/train_images/img_0066.jpg` (24122 bytes)
- `data/train_images/img_0067.jpg` (37372 bytes)
- `data/train_images/img_0068.jpg` (48686 bytes)
- `data/train_images/img_0069.jpg` (40053 bytes)
- `data/train_images/img_0070.jpg` (37636 bytes)
- `data/train_images/img_0071.jpg` (66517 bytes)
- `data/train_images/img_0072.jpg` (30270 bytes)
- `data/train_images/img_0073.jpg` (34322 bytes)
- `data/train_images/img_0074.jpg` (46276 bytes)
- `data/train_images/img_0075.jpg` (29328 bytes)
- `data/train_images/img_0076.jpg` (30587 bytes)
- `data/train_images/img_0077.jpg` (44858 bytes)
- `data/train_images/img_0078.jpg` (26238 bytes)
- `data/train_images/img_0079.jpg` (37949 bytes)
- `data/train_images/img_0080.jpg` (23490 bytes)
- `data/train_images/img_0081.jpg` (36285 bytes)
- `data/train_images/img_0082.jpg` (44300 bytes)
- `data/train_images/img_0083.jpg` (36238 bytes)
- `data/train_images/img_0084.jpg` (18964 bytes)
- `data/train_images/img_0085.jpg` (31489 bytes)
- `data/train_images/img_0086.jpg` (28966 bytes)
- `data/train_images/img_0087.jpg` (22753 bytes)
- `data/train_images/img_0088.jpg` (44950 bytes)
- `data/train_images/img_0089.jpg` (21725 bytes)
- `data/train_images/img_0090.jpg` (25847 bytes)
- `data/train_images/img_0091.jpg` (39061 bytes)
- `data/train_images/img_0092.jpg` (30712 bytes)
- `data/train_images/img_0093.jpg` (41227 bytes)
- `data/train_images/img_0094.jpg` (30450 bytes)
- `data/train_images/img_0095.jpg` (61465 bytes)
- `data/train_images/img_0096.jpg` (20836 bytes)
- `data/train_images/img_0097.jpg` (28600 bytes)
- `data/train_images/img_0098.jpg` (65624 bytes)
- `data/train_images/img_0099.jpg` (38651 bytes)
- `data/train_images/img_0100.jpg` (57826 bytes)
- `data/train_images/img_0101.jpg` (25561 bytes)
- `data/train_images/img_0102.jpg` (28405 bytes)
- `data/train_images/img_0103.jpg` (40842 bytes)
- `data/train_images/img_0104.jpg` (34714 bytes)
- `data/train_images/img_0105.jpg` (48613 bytes)
- `data/train_images/img_0106.jpg` (16409 bytes)
- `data/train_images/img_0107.jpg` (61703 bytes)
- `data/train_images/img_0108.jpg` (27565 bytes)
- `data/train_images/img_0109.jpg` (23516 bytes)
- `data/train_images/img_0110.jpg` (11588 bytes)
- `data/train_images/img_0111.jpg` (25948 bytes)
- `data/train_images/img_0112.jpg` (52886 bytes)
- `data/train_images/img_0113.jpg` (53213 bytes)
- `data/train_images/img_0114.jpg` (20373 bytes)
- `data/train_images/img_0115.jpg` (32070 bytes)
- `data/train_images/img_0116.jpg` (35618 bytes)
- `data/train_images/img_0117.jpg` (38154 bytes)
- `data/train_images/img_0118.jpg` (27936 bytes)
- `data/train_images/img_0119.jpg` (27495 bytes)
- `data/train_images/img_0120.jpg` (45823 bytes)
- `data/train_images/img_0121.jpg` (75705 bytes)
- `data/train_images/img_0122.jpg` (73147 bytes)
- `data/train_images/img_0123.jpg` (17820 bytes)
- `data/train_images/img_0124.jpg` (28678 bytes)
- `data/train_images/img_0125.jpg` (30972 bytes)
- `data/train_images/img_0126.jpg` (30160 bytes)
- `data/train_images/img_0127.jpg` (24885 bytes)
- `data/train_images/img_0128.jpg` (32220 bytes)
- `data/train_images/img_0129.jpg` (45962 bytes)
- `data/train_images/img_0130.jpg` (46059 bytes)
- `data/train_images/img_0131.jpg` (34448 bytes)
- `data/train_images/img_0132.jpg` (43408 bytes)
- `data/train_images/img_0133.jpg` (47485 bytes)
- `data/train_images/img_0134.jpg` (34947 bytes)
- `data/train_images/img_0135.jpg` (42762 bytes)
- `data/train_images/img_0136.jpg` (49826 bytes)
- `data/train_images/img_0137.jpg` (48311 bytes)
- `data/train_images/img_0138.jpg` (35871 bytes)
- `data/train_images/img_0139.jpg` (39083 bytes)
- `data/train_images/img_0140.jpg` (26384 bytes)
- `data/train_images/img_0141.jpg` (66551 bytes)
- `data/train_images/img_0142.jpg` (34094 bytes)
- `data/train_images/img_0143.jpg` (35743 bytes)
- `data/train_images/img_0144.jpg` (37033 bytes)
- `data/train_images/img_0145.jpg` (34880 bytes)
- `data/train_images/img_0146.jpg` (26606 bytes)
- `data/train_images/img_0147.jpg` (32981 bytes)
- `data/train_images/img_0148.jpg` (30028 bytes)
- `data/train_images/img_0149.jpg` (28473 bytes)
- `data/train_images/img_0150.jpg` (33272 bytes)
- `data/train_images/img_0151.jpg` (42212 bytes)
- `data/train_images/img_0152.jpg` (59741 bytes)
- `data/train_images/img_0153.jpg` (14136 bytes)
- `data/train_images/img_0154.jpg` (41348 bytes)
- `data/train_images/img_0155.jpg` (56334 bytes)
- `data/train_images/img_0156.jpg` (31063 bytes)
- `data/train_images/img_0157.jpg` (46799 bytes)
- `data/train_images/img_0158.jpg` (35514 bytes)
- `data/train_images/img_0159.jpg` (21660 bytes)
- `data/train_images/img_0160.jpg` (41294 bytes)
- `data/train_images/img_0161.jpg` (32769 bytes)
- `data/train_images/img_0162.jpg` (32657 bytes)
- `data/train_images/img_0163.jpg` (46425 bytes)
- `data/train_images/img_0164.jpg` (26193 bytes)
- `data/train_images/img_0165.jpg` (36881 bytes)
- `data/train_images/img_0166.jpg` (51238 bytes)
- `data/train_images/img_0167.jpg` (30620 bytes)
- `data/train_images/img_0168.jpg` (33901 bytes)

## Public description

MrBeast Pairwise Popularity: Multimodal Ranking Challenge

Problem statement
Given two MrBeast YouTube videos (A and B), predict the probability that video A ultimately achieved more views than video B. Each pair provides per-video publish-time metadata (title, description, tags, duration, language, categories, etc.) and the corresponding thumbnail image if available. Your task is to build a model that, using these inputs, estimates P(views(A) > views(B)).

Why this matters
Relative predictions are actionable for choosing between competing video ideas. This pairwise formulation focuses modeling on comparative signals and reduces sensitivity to global scaling effects across time.

Files you will use
- train.csv: Pairwise training data with labels. Each row is one ordered pair (A, B). Columns include:
  - pair_id
  - a_video, b_video: anonymized video identifiers
  - a_thumb, b_thumb: corresponding thumbnail filenames if available, else empty
  - Per-video features at publish time for A and B (prefixed by a_ or b_), including: title, description, tags, topicCategories, defaultLanguage, publishTime, duration_seconds, duration_iso, likeCount, commentCount, dimension
  - target: 1 if views(A) > views(B), otherwise 0 (ties excluded)
- test.csv: Same schema as train.csv but without the target column.
- sample_submission.csv: Correct format for your submission with random example predictions.
- train_images/: Thumbnail images for videos appearing in train.csv, using anonymized filenames.
- test_images/: Thumbnail images for videos appearing in test.csv, using anonymized filenames.

Target and task
- Binary target on ordered pairs: target = 1 if A outranks B by total views in the provided snapshot; otherwise 0. Ties are excluded from evaluation.
- Build models that take both members of a pair as input and output a probability that A outranks B.

Data description
- Source: All rows correspond to MrBeast videos as of a fixed snapshot. Only valid video rows are used; channel/other entities are excluded. Duplicate videos by id are removed.
- Multimodal inputs per video:
  - Text: title, description, tags, topicCategories, defaultLanguage
  - Time and duration: publishTime, duration_seconds, duration_iso
  - Engagement at snapshot: likeCount, commentCount
  - Video metadata: dimension
  - Vision: thumbnail image (if available); some videos do not have a local image and are represented with an empty filename. Handle missing images gracefully.
- Pairs are created within a temporal window to reduce strong confounding from very different accumulation periods.

Evaluation
- Metric: Area Under the ROC Curve (ROC AUC) on the pairwise labels.
  - Submissions must be a CSV with two columns: pair_id and target, where target is a probability in [0, 1].
  - The final score is ROC AUC computed over the entire hidden test set. Predictions will be clipped to [0, 1] for scoring. Pairs with tied ground truth were removed a priori and do not appear in the test set.

Train/test split and construction details
- Chronological split at the video level: the latest 20% of videos by publishTime form the test pool; the earliest 80% form the train pool. No video appears in both sets.
- Pair construction: Within each pool (train and test separately), form ordered pairs (A, B) where the absolute difference between publish times is at most 60 days. The label is 1 if A has more views than B; otherwise 0. Pairs with equal view counts are dropped. If the 60-day window does not yield both classes in a split, the window is automatically widened (up to 120 days) to ensure a valid classification task.
- Images are split consistently with videos and renamed to anonymized filenames so that file names do not reveal identities. CSVs refer only to anonymized video ids and anonymized image filenames (no paths).

Submission format
- A CSV with header containing two columns:
  - pair_id: Must match exactly the pair_id values provided in test.csv
  - target: Your predicted probability that A outranks B, clipped to [0, 1]

What you can build
- Strong baselines: TF-IDF on titles/descriptions/tags combined with engineered numeric features (differences/ratios) in a logistic regression or gradient boosted trees classifier.
- Advanced models: Siamese/twin-tower encoders for text and vision with late fusion, using the provided thumbnails, and a comparator head over concatenated/differenced embeddings.

Notes
- Do not rely on any external resources. Use only the provided CSVs and images. Some videos lack images; treat these as missing values.
- The dataset size is modest, but pairwise construction yields a substantial number of training examples. Handle class balance carefully and use robust cross-validation on the training set if desired.
