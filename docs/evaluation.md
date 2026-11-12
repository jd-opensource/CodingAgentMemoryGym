# Evaluation protocol

Evaluate the trained student alone, with the teacher disabled.

## Required inputs

- An exported student checkpoint and its exact tokenizer/chat template.
- A frozen list of held-out task identities, separate from the training schedule.
- The same CAMG-II tool interface and context/output/action budgets for every method.
- The same judge model, version and rubric for General and Visual.

Task indices are meaningful only together with their dataset manifest. Do not reuse indices after changing dataset row order. AutoResearch train and held-out manifests are source-family disjoint. Record the selected reporting task IDs with each evaluation.

## Metrics

Report native task success for Shop, Coding, AutoResearch and General. Report the visual judge score for Visual. Include task counts, environment failures and the complete per-task records; do not silently remove failed environment instances from a fixed benchmark denominator.

Any mean across environments must specify the weighting and units. Training rewards, average purchase progress and task success are different quantities.

## Checkpoint and tool handling

Checkpoint export utilities are in `verl/model_merger/`. Keep the training client's token-level tool dispatch during evaluation, including multi-call responses, reasoning removal and context resets.
