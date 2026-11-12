# OpenMLE-fast task

Task ID: `versatileproductionsystem@1`

Native metric: `FillingStateClassificationMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (965 bytes)
- `data/sample_submission.csv` (217792 bytes); columns: ["id", "0", "1", "2", "3", "4"]
- `data/test.csv` (565261 bytes); columns: ["Timestamp", "I_BottleAtAirpipe", "I_BottleClampClose", "I_BottleClampOpen", "I_BottleGateClosed", "I_BottleReserveGateClosed", "I_BottlesAvailable", "I_BottleSlot1", "I_BottleSlot2_H2O", "I_BottleSlot3_Corn", "I_BottleSlot5_CapOn", "I_BottleSlot6_CapScrewer", "I_BottleSlot8_Output", "I_BottlesReserveAvailable", "I_BottleStorageFull", "I_CapGrabberDown", "I_CapGrabberUp", "I_CapOnConveyor", "I_CapScrewer_Down", "I_CapScrewer_Up", "I_CapScrewerClosePos", "I_CapScrewerGrabClosed", "I_CapScrewerOpenPos", "I_CornTankFull", "I_LinAxisCapInGrabber", "I_LinAxisDown", "I_LinAxisEmptyGrabber", "I_LinAxisUp", "I_NoCapOnConveyor", "I_Portioning", "I_Pump_Down", "I_Pump_Up", "I_RotaryTablePosReached", "I_UltrasonicCorn", "I_UltrasonicCorn_Distance", "I_UltrasonicH2O", "I_UltrasonicH2O_Distance", "I_WaterTankMinFull", "I_WaterTankNotFull", "O_ActivateAirpipe", "O_BottleClampClose", "O_CapGrabberOpenClose", "O_CapGrabberUpDown", "O_CapScrewDown", "O_CapScrewerGrabberOpenClose", "O_CloseCap", "O_ConveyorCapsEnable", "O_ConveyorCapsForward", "O_ConveyorModuleIn", "O_ConveyorModuleOut", "O_GateBottleClose", "O_GateReserveClose", "O_LinAxisUpDown", "O_PortionerForward", "O_PortionerReverse", "O_PortionerSlow", "O_PumpUpDown", "O_RotaryTable", "O_ValvePumpCloseOpen", "PendingOrder", "Portions", "PumpStrokes", "Rotating", "SlowPortioning", "BottlesAvailable", "BottleSlot1", "BottleSlot2_H2O", "BottleSlot3_Corn", "BottleSlot5_CapOn", "BottleSlot6_CapCloser", "BottleSlot8_ModuleOut", "BottlesNotUsed", "UltraSonic_Corn.DistanceM", "UltraSonic_H2O.DistanceM", "I_CapGrabberDown__capgrabber", "I_CapGrabberUp__capgrabber", "I_CapOnConveyor__capgrabber", "I_LinAxisDown__capgrabber", "I_LinAxisUp__capgrabber", "O_BottleClampClose__capscrewer", "O_CapScrewDown__capscrewer", "O_CapScrewerGrabberOpenClose__capscrewer", "O_CloseCap__capscrewer", "O_PortionerForward__portioner", "O_PortionerReverse__portioner", "O_PortionerSlow__portioner", "Portions__portioner", "I_Pump_Down__pump", "I_Pump_Up__pump", "O_PumpUpDown__pump", "O_ValvePumpCloseOpen__pump", "PumpStrokes__pump"]
- `data/train.csv` (2272052 bytes); columns: ["Timestamp", "I_BottleAtAirpipe", "I_BottleClampClose", "I_BottleClampOpen", "I_BottleGateClosed", "I_BottleReserveGateClosed", "I_BottlesAvailable", "I_BottleSlot1", "I_BottleSlot2_H2O", "I_BottleSlot3_Corn", "I_BottleSlot5_CapOn", "I_BottleSlot6_CapScrewer", "I_BottleSlot8_Output", "I_BottlesReserveAvailable", "I_BottleStorageFull", "I_CapGrabberDown", "I_CapGrabberUp", "I_CapOnConveyor", "I_CapScrewer_Down", "I_CapScrewer_Up", "I_CapScrewerClosePos", "I_CapScrewerGrabClosed", "I_CapScrewerOpenPos", "I_CornTankFull", "I_LinAxisCapInGrabber", "I_LinAxisDown", "I_LinAxisEmptyGrabber", "I_LinAxisUp", "I_NoCapOnConveyor", "I_Portioning", "I_Pump_Down", "I_Pump_Up", "I_RotaryTablePosReached", "I_UltrasonicCorn", "I_UltrasonicCorn_Distance", "I_UltrasonicH2O", "I_UltrasonicH2O_Distance", "I_WaterTankMinFull", "I_WaterTankNotFull", "O_ActivateAirpipe", "O_BottleClampClose", "O_CapGrabberOpenClose", "O_CapGrabberUpDown", "O_CapScrewDown", "O_CapScrewerGrabberOpenClose", "O_CloseCap", "O_ConveyorCapsEnable", "O_ConveyorCapsForward", "O_ConveyorModuleIn", "O_ConveyorModuleOut", "O_GateBottleClose", "O_GateReserveClose", "O_LinAxisUpDown", "O_PortionerForward", "O_PortionerReverse", "O_PortionerSlow", "O_PumpUpDown", "O_RotaryTable", "O_ValvePumpCloseOpen", "PendingOrder", "Portions", "PumpStrokes", "Rotating", "SlowPortioning", "State", "BottlesAvailable", "BottleSlot1", "BottleSlot2_H2O", "BottleSlot3_Corn", "BottleSlot5_CapOn", "BottleSlot6_CapCloser", "BottleSlot8_ModuleOut", "BottlesNotUsed", "UltraSonic_Corn.DistanceM", "UltraSonic_H2O.DistanceM", "I_CapGrabberDown__capgrabber", "I_CapGrabberUp__capgrabber", "I_CapOnConveyor__capgrabber", "I_LinAxisDown__capgrabber", "I_LinAxisUp__capgrabber", "O_BottleClampClose__capscrewer", "O_CapScrewDown__capscrewer", "O_CapScrewerGrabberOpenClose__capscrewer", "O_CloseCap__capscrewer", "O_PortionerForward__portioner", "O_PortionerReverse__portioner", "O_PortionerSlow__portioner", "Portions__portioner", "I_Pump_Down__pump", "I_Pump_Up__pump", "O_PumpUpDown__pump", "O_ValvePumpCloseOpen__pump", "PumpStrokes__pump"]

## Public description

Versatile Production System — Filling Line State Classification

Problem statement
Predict the operating state of the industrial filling module at each timestamp from synchronized sensor and actuator signals.

Data description
- The provided data aggregates signals from the filling module and its submodules.
- All signals are synchronized by nearest timestamp alignment and presented as a single tabular time-series.
- Diagnostic EURangeViolation columns were removed.

Files
- train.csv: Feature matrix with target column State.
- test.csv: Same schema as train.csv without State.
- sample_submission.csv: Example submission with valid probability distributions.

Target
- State: Multi-class label representing operating phase.

Evaluation
- Metric: Multiclass log loss. Lower is better.
- Submission format: CSV with columns id and one column per class (e.g., 0, 1, 2, ...).
- The id column corresponds to the row index of test.csv starting from 0, in order.
