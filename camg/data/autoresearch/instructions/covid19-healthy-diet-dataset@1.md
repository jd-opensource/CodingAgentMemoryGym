# OpenMLE-fast task

Task ID: `covid19-healthy-diet-dataset@1`

Native metric: `HealthyDietObesityMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1203 bytes)
- `data/sample_submission.csv` (982 bytes); columns: ["country", "obesity_rate"]
- `data/test.csv` (22374 bytes); columns: ["country", "alcoholic_beverages_kcal", "animal_products_kcal", "animal_fats_kcal", "aquatic_products_other_kcal", "cereals_excluding_beer_kcal", "eggs_kcal", "fish_seafood_kcal", "fruits_excluding_wine_kcal", "meat_kcal", "milk_excluding_butter_kcal", "miscellaneous_kcal", "offals_kcal", "oilcrops_kcal", "pulses_kcal", "spices_kcal", "starchy_roots_kcal", "stimulants_kcal", "sugar_crops_kcal", "sugar_and_sweeteners_kcal", "treenuts_kcal", "vegetal_products_kcal", "vegetable_oils_kcal", "vegetables_kcal", "alcoholic_beverages_kg", "animal_fats_kg", "animal_products_kg", "aquatic_products_other_kg", "cereals_excluding_beer_kg", "eggs_kg", "fish_seafood_kg", "fruits_excluding_wine_kg", "meat_kg", "milk_excluding_butter_kg", "miscellaneous_kg", "offals_kg", "oilcrops_kg", "pulses_kg", "spices_kg", "starchy_roots_kg", "stimulants_kg", "sugar_and_sweeteners_kg", "sugar_crops_kg", "treenuts_kg", "vegetable_oils_kg", "vegetables_kg", "vegetal_products_kg", "alcoholic_beverages_fat", "animal_products_fat", "animal_fats_fat", "aquatic_products_other_fat", "cereals_excluding_beer_fat", "eggs_fat", "fish_seafood_fat", "fruits_excluding_wine_fat", "meat_fat", "miscellaneous_fat", "milk_excluding_butter_fat", "offals_fat", "oilcrops_fat", "pulses_fat", "spices_fat", "starchy_roots_fat", "stimulants_fat", "sugar_crops_fat", "sugar_and_sweeteners_fat", "treenuts_fat", "vegetal_products_fat", "vegetable_oils_fat", "vegetables_fat", "alcoholic_beverages_protein", "animal_products_protein", "animal_fats_protein", "aquatic_products_other_protein", "cereals_excluding_beer_protein", "eggs_protein", "fish_seafood_protein", "fruits_excluding_wine_protein", "meat_protein", "milk_excluding_butter_protein", "offals_protein", "oilcrops_protein", "pulses_protein", "spices_protein", "starchy_roots_protein", "stimulants_protein", "sugar_crops_protein", "sugar_and_sweeteners_protein", "treenuts_protein", "vegetal_products_protein", "vegetable_oils_protein", "vegetables_protein", "miscellaneous_protein"]
- `data/train.csv` (86044 bytes); columns: ["country", "alcoholic_beverages_kcal", "animal_products_kcal", "animal_fats_kcal", "aquatic_products_other_kcal", "cereals_excluding_beer_kcal", "eggs_kcal", "fish_seafood_kcal", "fruits_excluding_wine_kcal", "meat_kcal", "milk_excluding_butter_kcal", "miscellaneous_kcal", "offals_kcal", "oilcrops_kcal", "pulses_kcal", "spices_kcal", "starchy_roots_kcal", "stimulants_kcal", "sugar_crops_kcal", "sugar_and_sweeteners_kcal", "treenuts_kcal", "vegetal_products_kcal", "vegetable_oils_kcal", "vegetables_kcal", "alcoholic_beverages_kg", "animal_fats_kg", "animal_products_kg", "aquatic_products_other_kg", "cereals_excluding_beer_kg", "eggs_kg", "fish_seafood_kg", "fruits_excluding_wine_kg", "meat_kg", "milk_excluding_butter_kg", "miscellaneous_kg", "offals_kg", "oilcrops_kg", "pulses_kg", "spices_kg", "starchy_roots_kg", "stimulants_kg", "sugar_and_sweeteners_kg", "sugar_crops_kg", "treenuts_kg", "vegetable_oils_kg", "vegetables_kg", "vegetal_products_kg", "alcoholic_beverages_fat", "animal_products_fat", "animal_fats_fat", "aquatic_products_other_fat", "cereals_excluding_beer_fat", "eggs_fat", "fish_seafood_fat", "fruits_excluding_wine_fat", "meat_fat", "miscellaneous_fat", "milk_excluding_butter_fat", "offals_fat", "oilcrops_fat", "pulses_fat", "spices_fat", "starchy_roots_fat", "stimulants_fat", "sugar_crops_fat", "sugar_and_sweeteners_fat", "treenuts_fat", "vegetal_products_fat", "vegetable_oils_fat", "vegetables_fat", "alcoholic_beverages_protein", "animal_products_protein", "animal_fats_protein", "aquatic_products_other_protein", "cereals_excluding_beer_protein", "eggs_protein", "fish_seafood_protein", "fruits_excluding_wine_protein", "meat_protein", "milk_excluding_butter_protein", "offals_protein", "oilcrops_protein", "pulses_protein", "spices_protein", "starchy_roots_protein", "stimulants_protein", "sugar_crops_protein", "sugar_and_sweeteners_protein", "treenuts_protein", "vegetal_products_protein", "vegetable_oils_protein", "vegetables_protein", "miscellaneous_protein", "obesity_rate"]

## Public description

Title: Predict National Obesity Rate from Dietary Supply Profiles

Background
Country-level dietary composition reflects what populations consume in aggregate. Obesity prevalence is a key public health indicator linked to nutrition balance. This competition challenges you to infer national adult obesity prevalence (%) from diet composition across complementary nutrient modalities.

Problem Statement
Build a model that predicts each country’s adult obesity rate (%) from tabular features representing dietary composition across four modalities: energy intake (kcal), physical quantity (kg), fat supply, and protein supply.

Files provided (all under public/)
- train.csv: country identifier, obesity_rate, and the full feature set.
- test.csv: country identifier and the full feature set (no obesity_rate).
- sample_submission.csv: example submission file with country and predicted obesity_rate for the test set.

Evaluation
Submissions are evaluated using Mean Absolute Error (MAE) between predictions and the ground truth obesity_rate for the test countries. Lower is better.

Submission Format
Submit a CSV with exactly two columns in this order:
- country
- obesity_rate (numeric in [0, 100])
