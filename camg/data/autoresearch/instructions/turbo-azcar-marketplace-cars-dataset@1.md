# OpenMLE-fast task

Task ID: `turbo-azcar-marketplace-cars-dataset@1`

Native metric: `TurboAzCarPriceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4445 bytes)
- `data/sample_submission.csv` (39483 bytes); columns: ["id", "Price"]
- `data/test.csv` (262163 bytes); columns: ["Brand", "Model", "Currency", "Year", "Engine Size", "Horsepower", "Fuel Type", "Distance", "Color", "Body Type", "Transmission", "Drive Type", "New", "Seats", "Owners", "Condition", "Market", "City", "id"]
- `data/train.csv` (1085779 bytes); columns: ["Brand", "Model", "Currency", "Year", "Engine Size", "Horsepower", "Fuel Type", "Distance", "Color", "Body Type", "Transmission", "Drive Type", "New", "Seats", "Owners", "Condition", "Market", "City", "id", "Price"]

## Public description

```
description.txt (50 lines)
sample_submission.csv (1650 lines)
test.csv (1650 lines)
train.csv (6593 lines)```

-> sample_submission.csv has 1649 rows and 2 columns.
Here is some information about the columns:
Price (float64) has range: 1900.00 - 440000.00, 0 nan values
id (object) has 1649 unique values. Some example values: ['id_a2744b925657', 'id_efdec3e423e0', 'id_c20c0f125164', 'id_4c906cba0eae']

-> test.csv has 1649 rows and 19 columns.
Here is some information about the columns:
Body Type (object) has 21 unique values. Some example values: ['Sedan', 'Offroader / SUV, 5 qapı', 'Hetçbek, 5 qapı', 'Liftbek']
Brand (object) has 85 unique values. Some example values: ['Hyundai', 'Toyota', 'Mercedes', 'Kia']
City (object) has 33 unique values. Some example values: ['Bakı', 'Sumqayıt', 'Gəncə', 'Lənkəran']
Color (object) has 18 unique values. Some example values: ['Ağ', 'Qara', 'Yaş Asfalt', 'Göy']
Condition (object) has 4 unique values: ['Vuruğu yoxdur, rənglənməyib', 'Vuruğu yoxdur, rənglənib', 'Vuruğu var, rənglənməyib', 'Vuruğu var, rənglənib']
Currency (object) has 3 unique values: ['AZN', 'USD', 'EUR']
Distance (object) has 611 unique values. Some example values: ['0 km', '110 000 km', '250 000 km', '260 000 km']
Drive Type (object) has 3 unique values: ['Arxa', 'Tam', 'Ön']
Engine Size (object) has 77 unique values. Some example values: ['2.0 L', '1.5 L', '1.6 L', '3.0 L']
Fuel Type (object) has 35 unique values. Some example values: ['Benzin', 'Dizel', 'Plug-in Hibrid', 'Hibrid']
Horsepower (object) has 257 unique values. Some example values: ['150', '184', '245', '215']
Market (object) has 9 unique values: ['Avropa', 'Digər', 'Amerika', 'Rəsmi diler', 'Dubay', 'Çin', nan, 'Rusiya', 'Koreya', 'Yaponiya']
Model (object) has 403 unique values. Some example values: ['Elantra', 'Sorento', 'Rover Range Rover', 'Sonata']
New (object) has 2 unique values: ['Xeyr', 'Bəli']
Owners (object) has 5 unique values: ['1', '2', '0', nan, '3', '4 və daha çox']
Seats (object) has 8 unique values: ['8+', '4', '5', '7', nan, '3', '2', '6', '1']
Transmission (object) has 5 unique values: ['Avtomat', 'Reduktor', 'Variator', 'Robot', 'Mexaniki']
Year (int64) has range: 1969.00 - 2025.00, 0 nan values
id (object) has 1649 unique values. Some example values: ['id_a2744b925657', 'id_efdec3e423e0', 'id_c20c0f125164', 'id_4c906cba0eae']

-> train.csv has 6592 rows and 20 columns.
Here is some information about the columns:
Body Type (object) has 25 unique values. Some example values: ['Sedan', 'Offroader / SUV, 5 qapı', 'Hetçbek, 5 qapı', 'Liftbek']
Brand (object) has 109 unique values. Some example values: ['Toyota', 'Mercedes', 'Hyundai', 'Kia']
City (object) has 46 unique values. Some example values: ['Bakı', 'Sumqayıt', 'Gəncə', 'Lənkəran']
Color (object) has 18 unique values. Some example values: ['Ağ', 'Qara', 'Yaş Asfalt', 'Göy']
Condition (object) has 4 unique values: ['Vuruğu yoxdur, rənglənməyib', 'Vuruğu yoxdur, rənglənib', 'Vuruğu var, rənglənməyib', 'Vuruğu var, rənglənib']
Currency (object) has 3 unique values: ['AZN', 'USD', 'EUR']
Distance (object) has 1084 unique values. Some example values: ['0 km', '250 000 km', '110 000 km', '200 000 km']
Drive Type (object) has 3 unique values: ['Ön', 'Tam', 'Arxa']
Engine Size (object) has 121 unique values. Some example values: ['2.0 L', '1.5 L', '1.6 L', '3.0 L']
Fuel Type (object) has 73 unique values. Some example values: ['Benzin', 'Dizel', 'Hibrid', 'Plug-in Hibrid']
Horsepower (object) has 352 unique values. Some example values: ['150', '184', '245', '140']
Market (object) has 9 unique values: ['Rəsmi diler', nan, 'Çin', 'Amerika', 'Avropa', 'Koreya', 'Yaponiya', 'Rusiya', 'Dubay', 'Digər']
Model (object) has 668 unique values. Some example values: ['Elantra', 'Sorento', 'Rover Range Rover', 'Camry']
New (object) has 2 unique values: ['Bəli', 'Xeyr']
Owners (object) has 5 unique values: [nan, '0', '1', '2', '3', '4 və daha çox']
Price (int64) has range: 1200.00 - 440000.00, 0 nan values
Seats (object) has 8 unique values: [nan, '5', '4', '3', '7', '2', '6', '8+', '1']
Transmission (object) has 5 unique values: ['Robot', 'Mexaniki', 'Variator', 'Avtomat', 'Reduktor']
Year (int64) has range: 1969.00 - 2025.00, 0 nan values
id (object) has 6592 unique values. Some example values: ['id_cb59bd0909cc', 'id_8bc87b9b944f', 'id_ae3699b9720e', 'id_3e276680153e']
