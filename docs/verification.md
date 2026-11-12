# Verification status

This source-preparation phase does not include GPU allocation or training.

The release separates three kinds of evidence:

1. **Local code checks:** syntax, imports that do not require CUDA, configuration construction, task-manifest integrity, privacy checks and focused unit tests.
2. **Linux environment checks:** real task materialization, sandbox isolation, reset/action/termination, native reward and cleanup. These require the task assets and a suitably isolated Linux host.
3. **GPU checks:** installation of the pinned CUDA dependencies, one complete RL update, one complete OPD update and teacher-free evaluation from the resulting checkpoints.

Only checks actually run are reported in the release record. Successful local checks do not imply successful environment deployment or GPU training. A package or command that has not passed its target-runtime check remains unverified.

Before claiming reproduced results, run both methods from the same immutable source/data/model versions, reach each declared training endpoint, then evaluate on the same held-out tasks. Save logs, resolved configurations, checkpoint identities, per-task outcomes and aggregate metrics outside the source repository.

## Checks performed during source preparation

The following checks were run locally with Python 3.12, without CUDA or task-service startup:

- 101 unit tests plus two subtests: task/action protocols, training-command construction, explicit resume, per-attempt state, protected configuration paths, dataset/index/hash consistency, archive extraction safety, lossless Visual table conversion and shutdown error handling. This also includes content-verified runtime inventories, tamper rejection and required training/export-module presence.
- Python syntax, JSON parsing, shell syntax, local documentation links and common private-path/credential disclosure patterns across the release files.
- Source-package and wheel builds. The wheel carries training/client modules and task manifests; service deployment still requires the complete source checkout, including `runtimes/` and `third_party/`.
- One real AutoResearch archive downloaded from the pinned public source and materialized. Its selected public files, provenance files, private answer and native metric matched their recorded SHA-256 values. No task or grader code was executed in this check.
- Separate source comparisons for the training implementations and five environment adapters. Native parsers, prompts, rewards and task budgets were preserved; portability changes are listed in [provenance](provenance.md).

The reproducible local checks are:

```bash
python -m pytest tests/unit
python scripts/check_release.py
python -m build
```

The full training tests are opt-in after the Linux/CUDA dependencies are installed:

```bash
CAMP_TEST_TRAINING=1 python -m pytest tests/training
```

These tests have **not** been run in the source-preparation phase. The default test collection skips them rather than implying CUDA functionality was tested.

## Still required before an end-to-end release

- Clean Linux dependency installation and the complete native lifecycle of all five environments.
- AutoResearch runtime build, isolation probes and exact reconstruction of the 280 recipe-only task archives.
- Shop catalog/selection acquisition and redistribution review; General/Visual container-side setup and historical asset/image identity checks.
- One full update for each training method with real sampling, loss/backward, checkpointing and clean restart.
- The paper-matched held-out evaluation driver/panels and their clean-machine execution.
- Declared endpoint training and matched teacher-free evaluation before reporting reproduced results.

These are explicit remaining work, not completed tests and not optional substitutes for the local checks above.
