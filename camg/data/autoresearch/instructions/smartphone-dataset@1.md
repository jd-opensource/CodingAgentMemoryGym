# OpenMLE-fast task

Task ID: `smartphone-dataset@1`

Native metric: `SmartphonePriceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3209 bytes)
- `data/sample_submission.csv` (5132 bytes); columns: ["id", "discounted_price"]
- `data/test.csv` (27204 bytes); columns: ["id", "brand_name", "model_name", "colour", "rom", "ram", "screen_size_cm", "display_size_inch", "display_type", "front_camera", "rear_camera", "battery", "processor"]
- `data/train.csv` (119700 bytes); columns: ["id", "brand_name", "model_name", "colour", "rom", "ram", "screen_size_cm", "display_size_inch", "display_type", "front_camera", "rear_camera", "battery", "processor", "discounted_price"]

## Public description

```
description.txt (55 lines)
sample_submission.csv (228 lines)
test.csv (228 lines)
train.csv (930 lines)```

-> sample_submission.csv has 227 rows and 2 columns.
Here is some information about the columns:
discounted_price (float64) has range: 2886.26 - 181489.25, 0 nan values
id (int64) has range: 1.00 - 1148.00, 0 nan values

-> test.csv has 227 rows and 13 columns.
Here is some information about the columns:
battery (object) has 17 unique values. Some example values: ['5000 mAh Battery', '5000 mAh Lithium Ion Battery', '5000 mAh Lithium-ion Polymer Battery', '5000 mAh Lithium Battery']
brand_name (object) has 16 unique values. Some example values: ['Redmi', 'Apple', 'Samsung', 'Motorola']
colour (object) has 106 unique values. Some example values: ['Cosmic Black', 'Blue', 'Black', 'Feather Gold']
display_size_inch (float64) has range: 5.00 - 6.80, 0 nan values
display_type (object) has 9 unique values: [' Full HD+ ', ' HD+ ', ' ', ' Super Retina XDR ', ' Full HD+ Super AMOLED ', ' Full HD ', ' Full HD+ AMOLED ', ' Liquid Retina HD ', ' Full HD+ E3 Super AMOLED ']
front_camera (float64) has range: 2.00 - 50.00, 44 nan values
id (int64) has range: 1.00 - 1148.00, 0 nan values
model_name (object) has 60 unique values. Some example values: ['iphone 15 pro', '13c 5g', 'e13', 'narzo n53']
processor (object) has 56 unique values. Some example values: ['1 Year', 'Dimensity 8020 ', 'Unisoc T606 ', 'Helio G88 ']
ram (float64) has 6 unique values: [12.0, 8.0, 4.0, 3.0, 6.0, nan, 2.0]
rear_camera (object) has 40 unique values. Some example values: ['50MP Rear Camera5000 ', '50MP + 2MP ', '50MP + 8MP + 2MP ', '48MP + 12MP + 12MP ']
rom (int64) has 6 unique values: [256, 128, 64, 32, 1000, 512]
screen_size_cm (float64) has range: 12.70 - 17.27, 0 nan values

-> train.csv has 922 rows and 14 columns.
Here is some information about the columns:
battery (object) has 38 unique values. Some example values: ['5000 mAh Battery', '6000 mAh Battery', '5000 mAh Lithium Polymer Battery', '4600 mAh Battery']
brand_name (object) has 22 unique values. Some example values: ['Samsung', 'Poco', 'Redmi', 'Infinix']
colour (object) has 342 unique values. Some example values: ['Power Black', 'Blue', 'Yellow', 'Forest Green']
discounted_price (int64) has range: 3199.00 - 179900.00, 0 nan values
display_size_inch (float64) has range: 4.50 - 6.95, 0 nan values
display_type (object) has 12 unique values. Some example values: [' Full HD+ ', ' ', ' HD+ ', ' Super Retina XDR ']
front_camera (float64) has range: 0.00 - 60.00, 199 nan values
id (int64) has range: 0.00 - 1147.00, 0 nan values
model_name (object) has 236 unique values. Some example values: ['nord ce 3 lite 5g', 'c55', 't2x 5g', 'iphone 14']
processor (object) has 181 unique values. Some example values: ['Dimensity 6100+ ', 'Helio G36 ', 'Dimensity 6020 ', 'Helio G85 ']
ram (float64) has 8 unique values: [8.0, 4.0, 6.0, 12.0, nan, 2.0, 16.0, 3.0, 1.0]
rear_camera (object) has 122 unique values. Some example values: ['50MP + 2MP ', '50MP Rear Camera5000 ', '12MP + 12MP ', '108MP Rear Camera5000 ']
rom (int64) has 7 unique values: [256, 64, 128, 512, 32, 1000, 8]
screen_size_cm (float64) has range: 11.43 - 17.65, 0 nan values
