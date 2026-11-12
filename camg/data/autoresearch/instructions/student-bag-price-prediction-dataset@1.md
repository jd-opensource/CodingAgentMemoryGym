# OpenMLE-fast task

Task ID: `student-bag-price-prediction-dataset@1`

Native metric: `StudentBagPricePredictionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2039 bytes)
- `data/sample_submission.csv` (253095 bytes); columns: ["Id", "Price"]
- `data/test.csv` (678599 bytes); columns: ["Id", "Brand", "Material", "Size", "Compartments", "Laptop Compartment", "Waterproof", "Style", "Color", "Weight Capacity (kg)"]
- `data/train.csv` (3428967 bytes); columns: ["Id", "Brand", "Material", "Size", "Compartments", "Laptop Compartment", "Waterproof", "Style", "Color", "Weight Capacity (kg)", "Price"]

## Public description

```
description.txt (47 lines)
sample_submission.csv (9976 lines)
test.csv (9976 lines)
train.csv (39901 lines)```

-> sample_submission.csv has 9975 rows and 2 columns.
Here is some information about the columns:
Id (int64) has range: 139900.00 - 149874.00, 0 nan values
Price (float64) has range: 15.02 - 149.99, 0 nan values

-> test.csv has 9975 rows and 10 columns.
Here is some information about the columns:
Brand (object) has 5 unique values: ['Puma', 'Jansport', 'Adidas', 'Nike', 'Under Armour', nan]
Color (object) has 6 unique values: ['Black', 'Gray', 'Blue', 'Red', 'Green', 'Pink', nan]
Compartments (float64) has range: 1.00 - 10.00, 509 nan values
Id (int64) has range: 139900.00 - 149874.00, 0 nan values
Laptop Compartment (object) has 2 unique values: ['No', 'Yes', nan]
Material (object) has 4 unique values: ['Canvas', 'Polyester', 'Nylon', 'Leather', nan]
Size (object) has 3 unique values: ['Small', 'Large', 'Medium', nan]
Style (object) has 3 unique values: ['Tote', 'Messenger', nan, 'Backpack']
Waterproof (object) has 2 unique values: ['No', 'Yes', nan]
Weight Capacity (kg) (float64) has range: 5.00 - 30.00, 491 nan values

-> train.csv has 39900 rows and 11 columns.
Here is some information about the columns:
Brand (object) has 5 unique values: ['Under Armour', 'Nike', nan, 'Adidas', 'Puma', 'Jansport']
Color (object) has 6 unique values: ['Black', 'Pink', 'Green', 'Red', 'Blue', 'Gray', nan]
Compartments (float64) has range: 1.00 - 10.00, 1991 nan values
Id (int64) has range: 100000.00 - 139899.00, 0 nan values
Laptop Compartment (object) has 2 unique values: ['Yes', 'No', nan]
Material (object) has 4 unique values: ['Nylon', nan, 'Leather', 'Canvas', 'Polyester']
Price (float64) has range: 15.00 - 150.00, 0 nan values
Size (object) has 3 unique values: ['Large', 'Small', nan, 'Medium']
Style (object) has 3 unique values: ['Backpack', 'Messenger', 'Tote', nan]
Waterproof (object) has 2 unique values: [nan, 'No', 'Yes']
Weight Capacity (kg) (float64) has range: 5.00 - 30.00, 2007 nan values
