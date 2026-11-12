# OpenMLE-fast task

Task ID: `open-exoplanet-catalogue@1`

Native metric: `ExoRadiusRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3333 bytes)
- `data/sample_submission.csv` (7124 bytes); columns: ["Id", "RadiusJpt"]
- `data/test.csv` (92448 bytes); columns: ["PlanetIdentifier", "TypeFlag", "PlanetaryMassJpt", "PeriodDays", "SemiMajorAxisAU", "Eccentricity", "PeriastronDeg", "LongitudeDeg", "AscendingNodeDeg", "InclinationDeg", "SurfaceTempK", "AgeGyr", "DiscoveryMethod", "DiscoveryYear", "LastUpdated", "RightAscension", "Declination", "DistFromSunParsec", "HostStarMassSlrMass", "HostStarRadiusSlrRad", "HostStarMetallicity", "HostStarTempK", "HostStarAgeGyr", "ListsPlanetIsOn", "RightAscensionDeg", "DeclinationDeg", "Id"]
- `data/train.csv` (381232 bytes); columns: ["PlanetIdentifier", "TypeFlag", "PlanetaryMassJpt", "PeriodDays", "SemiMajorAxisAU", "Eccentricity", "PeriastronDeg", "LongitudeDeg", "AscendingNodeDeg", "InclinationDeg", "SurfaceTempK", "AgeGyr", "DiscoveryMethod", "DiscoveryYear", "LastUpdated", "RightAscension", "Declination", "DistFromSunParsec", "HostStarMassSlrMass", "HostStarRadiusSlrRad", "HostStarMetallicity", "HostStarTempK", "HostStarAgeGyr", "ListsPlanetIsOn", "RightAscensionDeg", "DeclinationDeg", "Id", "RadiusJpt"]

## Public description

Competition: ExoRadius — Predict Exoplanet Radius

Problem statement
Predict the radius of confirmed exoplanets (in Jupiter radii) using host-star properties, orbital parameters, sky position, and discovery metadata. Radii span orders of magnitude and depend on non-linear physics (e.g., irradiation, composition, inflation), making this a challenging tabular ML problem with missing values and domain shift across discovery methods.

Files
- train.csv — rows are confirmed exoplanets with features and the target RadiusJpt.
- test.csv — same schema as train.csv but without RadiusJpt.
- sample_submission.csv — example of the required submission format.

Schema
Every row contains a unique Id plus the columns below. RightAscension/Declination are provided as decimal degrees.
- Identification: Id, PlanetIdentifier (string identifier; provided for reference — treat as a non-predictive ID)
- Discovery/meta: DiscoveryMethod (categorical), DiscoveryYear
- Orbit: PeriodDays, SemiMajorAxisAU, Eccentricity, PeriastronDeg, LongitudeDeg, AscendingNodeDeg, InclinationDeg
- Planet: TypeFlag, PlanetaryMassJpt, SurfaceTempK, AgeGyr
- Host star: HostStarMassSlrMass, HostStarRadiusSlrRad, HostStarMetallicity, HostStarTempK, HostStarAgeGyr
- Position/distance: RightAscensionDeg, DeclinationDeg, DistFromSunParsec
Target
- RadiusJpt (Jupiter radii). Present only in train.csv.

Evaluation
- Metric: Root Mean Squared Logarithmic Error (RMSLE) on RadiusJpt.
  - RMSLE = sqrt(mean((log(1 + y_pred) − log(1 + y_true))^2)).
  - Predictions must be non-negative real numbers; negatives (if any) are clipped to 0 for scoring.
  - Motivation: Radius varies over orders of magnitude; RMSLE rewards relative accuracy and reduces heavy-tail penalties.

Submission format
- CSV with exactly two columns, no header changes: Id, RadiusJpt
- Id values must match those in test.csv (unique, one row per Id).
- RadiusJpt values must be finite, non-negative real numbers.

Data split and challenge characteristics
- The split is stratified by DiscoveryMethod and by quantile-binned PeriodDays and HostStarTempK to preserve key distributions while remaining challenging.
- Features exhibit substantial and systematic missingness (e.g., SemiMajorAxisAU, Eccentricity). Handle missing values appropriately; adding missingness indicators often helps.
- Discovery methods induce domain shift (e.g., transit vs. radial-velocity vs. microlensing), requiring robust generalization.

Guidance and good practices
- Encoding: Treat DiscoveryMethod as categorical. PlanetIdentifier is an identifier and is not intended as a predictive feature.
- Transformations: Consider training/predicting in log space (e.g., model log1p(RadiusJpt)) to stabilize variance. Log transforms of positive features (e.g., PeriodDays, SemiMajorAxisAU, DistFromSunParsec) may help.
- Physics-inspired features: Derived proxies like incident flux or equilibrium temperature from HostStarTempK and SemiMajorAxisAU can materially improve performance.
- Validation: Use cross-validation stratified by discovery method or grouped by host star (if you construct such a grouping) to assess robustness.

Objective
Build models that generalize across discovery methods and sky regions to accurately predict planetary radius for confirmed exoplanets with withheld radii in the test set.
