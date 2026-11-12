# Source provenance and packaging changes

This repository combines the selected **CAMP RL** implementation and **CAMP-II OPD** implementation with one shared **CAMG-II** environment suite. The source version to record in a new experiment is the public Git commit used for that experiment.

## What is preserved

- Separate RL and OPD recipes, model roles, optimizer settings, sampling configuration and advantage/loss implementations.
- Native task action parsers, policy-visible prompts, context/file-memory behavior, natural rewards and grading decisions.
- The five-domain task schedule's 12,800 task references, their order and environment-specific indices.
- Coding task identities and image digests; AutoResearch's train/held-out selection and individual file hashes; General/Visual's selected rows and order.

The shipped examples default to 100 optimizer updates. That is a recipe setting, not a claim that this newly packaged source has completed a training run.

## What changed for this repository

1. Training integrations are exposed as `camp.rl` and `camp.opd`; clients and services live under `camg`. Package imports follow that layout.
2. Machine-specific directories and service addresses were replaced by user-supplied paths and loopback defaults. Deployment generation binds the new paths/source identities to the schedule without resampling tasks.
3. Local launch scripts were replaced by documented Python commands. New runs require empty output directories; resume is explicit. Diagnostic counters are isolated per invocation.
4. Private endpoints, credentials, operational notes and unrelated environment implementations were excluded. Public prose uses the method/environment names above.
5. The isolated AutoResearch executor has consistent documented install paths, a from-source native build and a regenerated inventory of actual build outputs. An unused auxiliary communication-directory mount was removed; neither released method uses that extension. Its security checks were retained; successful installation status must come from real probes.
6. General/Visual judge settings are explicit; diagnostic endpoints require a token. Foreground service shutdown closes owned episodes, and AutoResearch supervises its private grader.
7. General task asset paths are replaced with a preparation placeholder and resolved locally. General/Visual Parquet rows are distributed as JSONL plus content hashes. AutoResearch task instructions remain byte-identical to the selected task descriptions.

These portability changes still need the Linux and GPU checks in [verification](verification.md). Static source comparison is useful evidence of preserved algorithms; it does not demonstrate identical runtime behavior.

## Upstream identities

| Component | Source identity |
|---|---|
| Training framework | Modified [veRL](https://github.com/verl-project/verl) snapshot included in `verl/`; installed dependency versions are recorded in `requirements.lock` |
| Base environment interfaces | [AgentGym](https://github.com/FudanNLP/AgentGym), with project-specific file-memory and lifecycle adapters |
| Shop code | [MemoryArena](https://github.com/ZexueHe/MemoryArena), commit `6cd9de14b71915e39ac742a20dc33785e14b6aab` |
| Coding source | [SWE-smith](https://github.com/SWE-bench/SWE-smith), commit `9b74ac08118a85c39c356802f7961893af73e07f`; dataset revision and image digests are in `camg/data/coding/` |
| AutoResearch source tasks | [OpenMLE-Tasks](https://huggingface.co/datasets/FrontisAI/OpenMLE-Tasks/tree/f56e4b31252a9b81d95fea100098cd49b7290398), revision `f56e4b31252a9b81d95fea100098cd49b7290398`; source URLs and terms are recorded per task |
| General/Visual | [MiMo recipes](https://github.com/XiaomiMiMo/verl/tree/mimo-oss), [MiMo agent](https://github.com/XiaomiMiMo/mimoagent) and [MiMo data](https://huggingface.co/datasets/XiaomiMiMo/MiMo-V2.6-RL-oss); selected-table hashes and asset-download revision are in each `source.json` |

## Remaining provenance limits

The required MiMo code was recovered and included, but its exact historical upstream commit and container-image digests have not yet been established. The pinned public asset-download revision provides a reproducible download target; it has not yet been shown to match every asset used in the original experiment. The modified veRL source is fully included, but a clean upstream-to-project commit map is not yet recorded here.

Of 931 AutoResearch tasks, 651 have public ready archives matching the selected hashes. The remaining 280 have upstream recipes; exact reconstruction of their selected archives remains unverified. Shop's catalog and derived product selection are not redistributed pending confirmed redistribution terms. These limitations are not resolved by a passing source test or an installation command.

No training checkpoint, unpublished result, internal infrastructure configuration or private task solution is included. Consult [third-party notices](../THIRD_PARTY.md) and [dataset terms](../camg/data/LICENSES.md) before downloading or redistributing assets.
