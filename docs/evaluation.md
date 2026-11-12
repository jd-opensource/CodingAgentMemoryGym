# Evaluation

Evaluate the student alone, after its declared training endpoint. The OPD teacher is a training dependency, not an evaluation service.

## Required inputs

- An exported student checkpoint and its exact tokenizer/chat template.
- A frozen list of held-out task identities, separate from the training schedule.
- The same CAMG-II tool interface and context/output/action budgets for every method.
- The same judge model, version and rubric for General and Visual.

Task indices are meaningful only together with their dataset manifest. Do not reuse indices after changing dataset row order. AutoResearch train and held-out manifests are source-family disjoint; its full held-out pool is not itself a claim that every task belongs to a paper's reporting panel.

## Metrics

Report native task success for Shop, Coding, AutoResearch and General. Report the visual judge score for Visual. Include task counts, environment failures and the complete per-task records; do not silently remove failed environment instances from a fixed benchmark denominator.

Any mean across environments must specify the weighting and units. Training rewards, average purchase progress and task success are different quantities. A short installation test should be described as an installation test, not a benchmark score.

## Current boundary

The training checkpoint utilities are included in `verl/model_merger/`. A paper-matched evaluation command and its frozen reporting panels require a separate verification step. This source-preparation release does not claim that an arbitrary OpenAI-compatible inference loop reproduces the original token-level tool dispatch. In particular, multi-call responses, reasoning removal and context resets must be checked against the training clients before reporting scores.
