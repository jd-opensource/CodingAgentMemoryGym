# OpenMLE-fast task

Task ID: `datos-morfolgicos-de-100-especies-de-hongos@1`

Native metric: `FungalMorphologyMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2779 bytes)
- `data/sample_submission.csv` (394907 bytes); columns: ["Id", "Especie"]
- `data/test.csv` (3302536 bytes); columns: ["Id", "color_red_mean", "color_red_std", "color_green_mean", "color_green_std", "color_blue_mean", "color_blue_std", "texture_contrast", "texture_correlation", "texture_homogeneity", "texture_energy", "shape_area", "shape_perimeter", "shape_circularity"]
- `data/train.csv` (14400370 bytes); columns: ["Id", "color_red_mean", "color_red_std", "color_green_mean", "color_green_std", "color_blue_mean", "color_blue_std", "texture_contrast", "texture_correlation", "texture_homogeneity", "texture_energy", "shape_area", "shape_perimeter", "shape_circularity", "Especie"]

## Public description

Title: 100-Species Fungal Morphology Classification (Tabular)

Problem statement
Participants are given computer-vision-derived morphology descriptors (color, texture, and shape) for individual fungi specimens. The task is to predict the species label (Especie) among 100 possible classes using machine learning on tabular data.

Data description
- train.csv: Contains an Id column, 13 numerical morphology features, and the target column Especie. Id is a row identifier and not a predictive feature.
- test.csv: Contains an Id column and the same 13 numerical morphology features, without labels.
- sample_submission.csv: Example submission file with columns Id and Especie. The Id values correspond one-to-one with rows in test.csv.

Features
All 13 numeric features are available for modeling:
- Color (means and standard deviations): color_red_mean, color_red_std, color_green_mean, color_green_std, color_blue_mean, color_blue_std
- Texture (GLCM statistics): texture_contrast, texture_correlation, texture_homogeneity, texture_energy
- Shape: shape_area, shape_perimeter, shape_circularity
The dataset contains 100 species classes in total (Especie). Categorical columns related to toxicity and psilocybin presence are excluded from the feature set to avoid label leakage.

Recommended approach
- Data processing: Standardize/scale features (e.g., StandardScaler or RobustScaler). Consider monotone transforms (e.g., log1p) on heavy-tailed features such as shape_area, shape_perimeter, and texture_contrast.
- Feature engineering: Ratios between color channels, colorfulness indices, interaction terms, or alternative shape compactness formulations can be informative.
- Modeling: Try regularized linear models, gradient boosting (e.g., XGBoost/LightGBM/CatBoost), SVMs, or neural networks for tabular data. Address class imbalance with class weights or resampling.
- Validation: Use stratified cross-validation (e.g., StratifiedKFold) to maintain class balance across folds.

Evaluation
Submissions are evaluated using macro-averaged F1 score over the 100 species classes.
- Macro F1 equally weights each class, preventing dominance by frequent species and encouraging balanced performance across rare classes as well.
- F1 balances precision and recall, rewarding models that both detect rare species and avoid overpredicting common ones.
The submission file must contain columns Id and Especie with predictions for all rows in test.csv.

Final data files
- train.csv
- test.csv
- sample_submission.csv

Notes
- Do not use Id as a feature; it is only a unique row identifier.
- Do not use categorical columns like Toxicidad or Psilocibina.
- Ensure deterministic training and evaluation setup.
- All test labels are guaranteed to occur at least once in the training set.
