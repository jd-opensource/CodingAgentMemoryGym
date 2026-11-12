# OpenMLE-fast task

Task ID: `ultimate-ufc-dataset@1`

Native metric: `UFCOutcomeMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (260 bytes)
- `data/sample_submission.csv` (196816 bytes); columns: ["bout_id", "Red-DEC", "Red-KO/TKO", "Red-SUB", "Blue-DEC", "Blue-KO/TKO", "Blue-SUB"]
- `data/test.csv` (562646 bytes); columns: ["bout_id", "RedFighter", "BlueFighter", "RedOdds", "BlueOdds", "RedExpectedValue", "BlueExpectedValue", "Date", "Location", "Country", "TitleBout", "WeightClass", "Gender", "NumberOfRounds", "BlueCurrentLoseStreak", "BlueCurrentWinStreak", "BlueDraws", "BlueAvgSigStrLanded", "BlueAvgSigStrPct", "BlueAvgSubAtt", "BlueAvgTDLanded", "BlueAvgTDPct", "BlueLongestWinStreak", "BlueLosses", "BlueTotalRoundsFought", "BlueTotalTitleBouts", "BlueWinsByDecisionMajority", "BlueWinsByDecisionSplit", "BlueWinsByDecisionUnanimous", "BlueWinsByKO", "BlueWinsBySubmission", "BlueWinsByTKODoctorStoppage", "BlueWins", "BlueStance", "BlueHeightCms", "BlueReachCms", "BlueWeightLbs", "RedCurrentLoseStreak", "RedCurrentWinStreak", "RedDraws", "RedAvgSigStrLanded", "RedAvgSigStrPct", "RedAvgSubAtt", "RedAvgTDLanded", "RedAvgTDPct", "RedLongestWinStreak", "RedLosses", "RedTotalRoundsFought", "RedTotalTitleBouts", "RedWinsByDecisionMajority", "RedWinsByDecisionSplit", "RedWinsByDecisionUnanimous", "RedWinsByKO", "RedWinsBySubmission", "RedWinsByTKODoctorStoppage", "RedWins", "RedStance", "RedHeightCms", "RedReachCms", "RedWeightLbs", "RedAge", "BlueAge", "LoseStreakDif", "WinStreakDif", "LongestWinStreakDif", "WinDif", "LossDif", "TotalRoundDif", "TotalTitleBoutDif", "KODif", "SubDif", "HeightDif", "ReachDif", "AgeDif", "SigStrDif", "AvgSubAttDif", "AvgTDDif", "EmptyArena", "BMatchWCRank", "RMatchWCRank", "RWFlyweightRank", "RWFeatherweightRank", "RWStrawweightRank", "RWBantamweightRank", "RHeavyweightRank", "RLightHeavyweightRank", "RMiddleweightRank", "RWelterweightRank", "RLightweightRank", "RFeatherweightRank", "RBantamweightRank", "RFlyweightRank", "RPFPRank", "BWFlyweightRank", "BWFeatherweightRank", "BWStrawweightRank", "BWBantamweightRank", "BHeavyweightRank", "BLightHeavyweightRank", "BMiddleweightRank", "BWelterweightRank", "BLightweightRank", "BFeatherweightRank", "BBantamweightRank", "BFlyweightRank", "BPFPRank", "BetterRank", "RedDecOdds", "BlueDecOdds", "RSubOdds", "BSubOdds", "RKOOdds", "BKOOdds"]
- `data/train.csv` (2332296 bytes); columns: ["bout_id", "RedFighter", "BlueFighter", "RedOdds", "BlueOdds", "RedExpectedValue", "BlueExpectedValue", "Date", "Location", "Country", "TitleBout", "WeightClass", "Gender", "NumberOfRounds", "BlueCurrentLoseStreak", "BlueCurrentWinStreak", "BlueDraws", "BlueAvgSigStrLanded", "BlueAvgSigStrPct", "BlueAvgSubAtt", "BlueAvgTDLanded", "BlueAvgTDPct", "BlueLongestWinStreak", "BlueLosses", "BlueTotalRoundsFought", "BlueTotalTitleBouts", "BlueWinsByDecisionMajority", "BlueWinsByDecisionSplit", "BlueWinsByDecisionUnanimous", "BlueWinsByKO", "BlueWinsBySubmission", "BlueWinsByTKODoctorStoppage", "BlueWins", "BlueStance", "BlueHeightCms", "BlueReachCms", "BlueWeightLbs", "RedCurrentLoseStreak", "RedCurrentWinStreak", "RedDraws", "RedAvgSigStrLanded", "RedAvgSigStrPct", "RedAvgSubAtt", "RedAvgTDLanded", "RedAvgTDPct", "RedLongestWinStreak", "RedLosses", "RedTotalRoundsFought", "RedTotalTitleBouts", "RedWinsByDecisionMajority", "RedWinsByDecisionSplit", "RedWinsByDecisionUnanimous", "RedWinsByKO", "RedWinsBySubmission", "RedWinsByTKODoctorStoppage", "RedWins", "RedStance", "RedHeightCms", "RedReachCms", "RedWeightLbs", "RedAge", "BlueAge", "LoseStreakDif", "WinStreakDif", "LongestWinStreakDif", "WinDif", "LossDif", "TotalRoundDif", "TotalTitleBoutDif", "KODif", "SubDif", "HeightDif", "ReachDif", "AgeDif", "SigStrDif", "AvgSubAttDif", "AvgTDDif", "EmptyArena", "BMatchWCRank", "RMatchWCRank", "RWFlyweightRank", "RWFeatherweightRank", "RWStrawweightRank", "RWBantamweightRank", "RHeavyweightRank", "RLightHeavyweightRank", "RMiddleweightRank", "RWelterweightRank", "RLightweightRank", "RFeatherweightRank", "RBantamweightRank", "RFlyweightRank", "RPFPRank", "BWFlyweightRank", "BWFeatherweightRank", "BWStrawweightRank", "BWBantamweightRank", "BHeavyweightRank", "BLightHeavyweightRank", "BMiddleweightRank", "BWelterweightRank", "BLightweightRank", "BFeatherweightRank", "BBantamweightRank", "BFlyweightRank", "BPFPRank", "BetterRank", "RedDecOdds", "BlueDecOdds", "RSubOdds", "BSubOdds", "RKOOdds", "BKOOdds", "target"]

## Public description

Dataset: UFC outcome prediction
Files:
- train.csv: Training data with features and target label (one of six classes).
- test.csv: Test data with features (no target).
- sample_submission.csv: Example submission with probabilities for six classes per bout_id.
