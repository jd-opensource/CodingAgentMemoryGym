# OpenMLE-fast task

Task ID: `behavioral-risk-factor-surveillance-system@1`

Native metric: `BRFSSHealthMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (587 bytes)
- `data/sample_submission.csv` (98485 bytes); columns: ["row_id", "genhlth"]
- `data/test.csv` (4201135 bytes); columns: ["row_id", "ADDEPEV2", "ALCDAY5", "ASACTLIM", "ASATTACK", "ASDRVIST", "ASERVIST", "ASINHALR", "ASNOSLEP", "ASRCHKUP", "ASTHMA3", "ASTHMAGE", "ASTHMED3", "ASTHNOW", "ASYMPTOM", "AVEDRNK2", "BLDSTOOL", "BLDSUGAR", "CADULT", "CASTHDX2", "CASTHNO2", "CELLFON2", "CHCKIDNY", "CHCOCNCR", "CHCSCNCR", "CHECKUP1", "CHILDREN", "CHKHEMO3", "CPDEMO1", "CSTATE", "CTELENUM", "CTELNUM1", "CVDCRHD4", "CVDINFR4", "CVDSTRK3", "DIABAGE2", "DIABEDU", "DIABETE3", "DIABEYE", "DOCTDIAB", "DRNK3GE5", "DRNKANY5", "DROCDY3_", "EDUCA", "EMTSUPRT", "EXERANY2", "EYEEXAM", "FEETCHK", "FEETCHK2", "FLSHTMY2", "HADHYST2", "HADMAM", "HADPAP2", "HADSGCO1", "HADSIGM3", "HAVARTH3", "HEIGHT3", "HIVTST6", "HIVTSTD3", "HLTHPLN1", "HOWLONG", "HPVADSHT", "HPVADVC2", "HTIN4", "HTM4", "IMFVPLAC", "INCOME2", "INSULIN", "LANDLINE", "LASTPAP2", "LASTSIG3", "LASTSMK2", "LENGEXAM", "LSATISFY", "LSTBLDS3", "MARITAL", "MAXDRNKS", "MEDCOST", "MENTHLTH", "MSCODE", "NUMADULT", "NUMHHOL2", "NUMMEN", "NUMPHON2", "NUMWOMEN", "PAINACT2", "PDIABTST", "PERSDOC2", "PHYSHLTH", "PNEUVAC3", "POORHLTH", "PREDIAB1", "PREGNANT", "PROFEXAM", "PSATEST1", "PSATIME", "PVTRESD2", "QLACTLM2", "QLHLTH2", "QLMENTL2", "QLSTRES2", "QSTLANG", "QSTVER", "RCSGENDR", "RCSRLTN2", "RENTHOM1", "SCNTLPAD", "SCNTLWK1", "SCNTPAID", "SCNTWRK1", "SEATBELT", "SEX", "SMOKDAY2", "SMOKE100", "STOPSMK2", "USEEQUIP", "USENOW3", "VETERAN3", "WEIGHT2", "WTKG3", "_AGE65YR", "_AGEG5YR", "_AGE_G", "_AIDTST3", "_ASTHMS1", "_BMI5", "_BMI5CAT", "_CASTHM1", "_CHLDCNT", "_DRDXAR1", "_EDUCAG", "_HCVU651", "_INCOMG", "_LTASTH1", "_PNEUMO2", "_RFBING5", "_RFBMI5", "_RFSEAT2", "_RFSEAT3", "_RFSMOK3", "_SMOKER3", "_STATE", "_TOTINDA"]
- `data/train.csv` (17257174 bytes); columns: ["row_id", "genhlth", "ADDEPEV2", "ALCDAY5", "ASACTLIM", "ASATTACK", "ASDRVIST", "ASERVIST", "ASINHALR", "ASNOSLEP", "ASRCHKUP", "ASTHMA3", "ASTHMAGE", "ASTHMED3", "ASTHNOW", "ASYMPTOM", "AVEDRNK2", "BLDSTOOL", "BLDSUGAR", "CADULT", "CASTHDX2", "CASTHNO2", "CELLFON2", "CHCKIDNY", "CHCOCNCR", "CHCSCNCR", "CHECKUP1", "CHILDREN", "CHKHEMO3", "CPDEMO1", "CSTATE", "CTELENUM", "CTELNUM1", "CVDCRHD4", "CVDINFR4", "CVDSTRK3", "DIABAGE2", "DIABEDU", "DIABETE3", "DIABEYE", "DOCTDIAB", "DRNK3GE5", "DRNKANY5", "DROCDY3_", "EDUCA", "EMTSUPRT", "EXERANY2", "EYEEXAM", "FEETCHK", "FEETCHK2", "FLSHTMY2", "HADHYST2", "HADMAM", "HADPAP2", "HADSGCO1", "HADSIGM3", "HAVARTH3", "HEIGHT3", "HIVTST6", "HIVTSTD3", "HLTHPLN1", "HOWLONG", "HPVADSHT", "HPVADVC2", "HTIN4", "HTM4", "IMFVPLAC", "INCOME2", "INSULIN", "LANDLINE", "LASTPAP2", "LASTSIG3", "LASTSMK2", "LENGEXAM", "LSATISFY", "LSTBLDS3", "MARITAL", "MAXDRNKS", "MEDCOST", "MENTHLTH", "MSCODE", "NUMADULT", "NUMHHOL2", "NUMMEN", "NUMPHON2", "NUMWOMEN", "PAINACT2", "PDIABTST", "PERSDOC2", "PHYSHLTH", "PNEUVAC3", "POORHLTH", "PREDIAB1", "PREGNANT", "PROFEXAM", "PSATEST1", "PSATIME", "PVTRESD2", "QLACTLM2", "QLHLTH2", "QLMENTL2", "QLSTRES2", "QSTLANG", "QSTVER", "RCSGENDR", "RCSRLTN2", "RENTHOM1", "SCNTLPAD", "SCNTLWK1", "SCNTPAID", "SCNTWRK1", "SEATBELT", "SEX", "SMOKDAY2", "SMOKE100", "STOPSMK2", "USEEQUIP", "USENOW3", "VETERAN3", "WEIGHT2", "WTKG3", "_AGE65YR", "_AGEG5YR", "_AGE_G", "_AIDTST3", "_ASTHMS1", "_BMI5", "_BMI5CAT", "_CASTHM1", "_CHLDCNT", "_DRDXAR1", "_EDUCAG", "_HCVU651", "_INCOMG", "_LTASTH1", "_PNEUMO2", "_RFBING5", "_RFBMI5", "_RFSEAT2", "_RFSEAT3", "_RFSMOK3", "_SMOKER3", "_STATE", "_TOTINDA"]

## Public description

Title: BRFSS Ordinal Health Prediction Challenge (2011–2015)

Files in this directory:
- train.csv: Training data with columns [row_id, genhlth, <features...>].
- test.csv: Test data with columns [row_id, <features...>] (no labels).
- sample_submission.csv: Example submission with columns [row_id, genhlth].

Target and metric:
- Target column: genhlth (integer in {1,2,3,4,5}).
- Evaluation: Quadratic Weighted Kappa on genhlth.

Notes:
- Feature columns are the intersection of variables consistently available across 2011–2015,
  excluding identifiers and direct target recodes.
