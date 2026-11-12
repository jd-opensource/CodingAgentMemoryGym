# OpenMLE-fast task

Task ID: `galactism-analysis-prfm@1`

Native metric: `StarFormationSurfaceDensityMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3375 bytes)
- `data/sample_submission.csv` (225652 bytes); columns: ["id", "SigmaSFR"]
- `data/test.csv` (4363174 bytes); columns: ["id", "galaxy_id", "r_idx", "phi_idx", "time_idx", "R_kpc", "sin_phi", "cos_phi", "t_Myr", "Kappa", "Force", "ForceLeft", "ForceRight", "SigmaGas", "SigmaH2Gas", "Ptot", "Ptherm", "Pturb", "midplane_count", "midplane_dens", "PtlMinIdcs", "Count"]
- `data/train.csv` (18304412 bytes); columns: ["id", "galaxy_id", "r_idx", "phi_idx", "time_idx", "R_kpc", "sin_phi", "cos_phi", "t_Myr", "Kappa", "Force", "ForceLeft", "ForceRight", "SigmaGas", "SigmaH2Gas", "Ptot", "Ptherm", "Pturb", "midplane_count", "midplane_dens", "PtlMinIdcs", "Count", "SigmaSFR"]

## Public description

```
description.txt (39 lines)
sample_submission.csv (14881 lines)
test.csv (14881 lines)
train.csv (59521 lines)```

-> sample_submission.csv has 14880 rows and 2 columns.
Here is some information about the columns:
SigmaSFR (float64) has 1 unique values: [0.5]
id (object) has 14880 unique values. Some example values: ['g5_26_8_24', 'g5_26_9_24', 'g5_26_10_24', 'g5_26_11_24']

-> test.csv has 14880 rows and 22 columns.
Here is some information about the columns:
Count (float64) has range: 0.00 - 28986.00, 0 nan values
Force (float64) has range: -62518471.12 - 79815669.08, 0 nan values
ForceLeft (float64) has range: -62525674.21 - 816076.32, 0 nan values
ForceRight (float64) has range: -6174597.63 - 82578912.07, 0 nan values
Kappa (float64) has range: 0.01 - 0.99, 0 nan values
Ptherm (float64) has range: 0.00 - 72865800117466497024.00, 0 nan values
PtlMinIdcs (float64) has range: 0.00 - 170.00, 0 nan values
Ptot (float64) has range: 0.00 - 4410538.59, 614 nan values
Pturb (float64) has range: 0.00 - 4410538.59, 614 nan values
R_kpc (float64) has range: 0.40 - 12.90, 0 nan values
SigmaGas (float64) has range: 0.00 - 85.40, 0 nan values
SigmaH2Gas (float64) has range: 0.00 - 69.31, 0 nan values
cos_phi (float64) has range: -0.99 - 0.99, 0 nan values
galaxy_id (int64) has 6 unique values: [0, 1, 2, 3, 4, 5]
id (object) has 14880 unique values. Some example values: ['g5_26_8_24', 'g5_26_9_24', 'g5_26_10_24', 'g5_26_11_24']
midplane_count (float64) has range: 0.00 - 6219.00, 0 nan values
midplane_dens (float64) has range: 0.00 - 0.00, 0 nan values
phi_idx (int64) has range: 0.00 - 23.00, 0 nan values
r_idx (int64) has range: 0.00 - 63.00, 0 nan values
sin_phi (float64) has range: -0.99 - 0.99, 0 nan values
t_Myr (float64) has range: 340.00 - 788.00, 0 nan values
time_idx (int64) has 5 unique values: [20, 21, 22, 23, 24]

-> train.csv has 59520 rows and 23 columns.
Here is some information about the columns:
Count (float64) has range: 0.00 - 27123.00, 0 nan values
Force (float64) has range: -24988916.43 - 23812917.50, 0 nan values
ForceLeft (float64) has range: -52762974.06 - 3051029.04, 0 nan values
ForceRight (float64) has range: -23711768.55 - 63185436.03, 0 nan values
Kappa (float64) has range: 0.00 - 0.99, 168 nan values
Ptherm (float64) has range: 0.00 - 82697248735912460288.00, 0 nan values
PtlMinIdcs (float64) has range: 0.00 - 209.00, 0 nan values
Ptot (float64) has range: 0.00 - 13154013.20, 2189 nan values
Pturb (float64) has range: 0.00 - 13154013.20, 2189 nan values
R_kpc (float64) has range: 0.40 - 12.90, 0 nan values
SigmaGas (float64) has range: 0.00 - 116.93, 0 nan values
SigmaH2Gas (float64) has range: 0.00 - 95.73, 0 nan values
SigmaSFR (float64) has range: 0.00 - 7.66, 0 nan values
cos_phi (float64) has range: -0.99 - 0.99, 0 nan values
galaxy_id (int64) has 6 unique values: [0, 1, 2, 3, 4, 5]
id (object) has 59520 unique values. Some example values: ['g5_26_8_19', 'g5_26_9_19', 'g5_26_10_19', 'g5_26_11_19']
midplane_count (float64) has range: 0.00 - 7228.00, 0 nan values
midplane_dens (float64) has range: 0.00 - 0.00, 0 nan values
phi_idx (int64) has range: 0.00 - 23.00, 0 nan values
r_idx (int64) has range: 0.00 - 63.00, 0 nan values
sin_phi (float64) has range: -0.99 - 0.99, 0 nan values
t_Myr (float64) has range: 100.00 - 728.00, 0 nan values
time_idx (int64) has range: 0.00 - 19.00, 0 nan values
