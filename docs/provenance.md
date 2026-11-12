# Source components

CAMP RL and CAMP-II OPD share the CAMG-II clients, task services and data preparation code. Record the public Git commit with each run.

## Organization

- `camp.rl` and `camp.opd` contain the two training integrations and their respective algorithms.
- `camg` contains the five environment clients, services and task manifests.
- `runtimes/autoresearch` contains the isolated executor and private grader.
- `verl` and `third_party` contain the training framework and required upstream runtime components.

## Upstream sources

| Component | Source identity |
|---|---|
| Training framework | Modified [veRL](https://github.com/verl-project/verl) snapshot included in `verl/`; installed dependency versions are recorded in `requirements.lock` |
| Base environment interfaces | [AgentGym](https://github.com/FudanNLP/AgentGym), with project-specific file-memory and lifecycle adapters |
| Shop code | [MemoryArena](https://github.com/ZexueHe/MemoryArena), commit `6cd9de14b71915e39ac742a20dc33785e14b6aab` |
| Coding source | [SWE-smith](https://github.com/SWE-bench/SWE-smith), commit `9b74ac08118a85c39c356802f7961893af73e07f`; dataset revision and image digests are in `camg/data/coding/` |
| AutoResearch source tasks | [OpenMLE-Tasks](https://huggingface.co/datasets/FrontisAI/OpenMLE-Tasks/tree/f56e4b31252a9b81d95fea100098cd49b7290398), revision `f56e4b31252a9b81d95fea100098cd49b7290398`; source URLs and terms are recorded per task |
| General/Visual | [MiMo recipes](https://github.com/XiaomiMiMo/verl/tree/mimo-oss), [MiMo agent](https://github.com/XiaomiMiMo/mimoagent) and [MiMo data](https://huggingface.co/datasets/XiaomiMiMo/MiMo-V2.6-RL-oss); selected-table hashes and asset-download revision are in each `source.json` |

## Project adaptations

The integrations add file-memory behavior, asynchronous RL/OPD training, CAMG-II task selection and configurable deployment paths. Service configuration records source and asset hashes while preserving task identities and order. AutoResearch uses a from-source native build with an inventory of its outputs; General and Visual take judge settings from environment variables. Foreground services manage their episode workspaces and shutdown cleanup.

General/Visual task tables are stored as JSONL and converted to Parquet during preparation. General asset paths are resolved locally. AutoResearch instructions retain the selected task descriptions, with file hashes recorded in the manifests.

See [third-party notices](../THIRD_PARTY.md) for code attribution and [dataset terms](../camg/data/LICENSES.md) for data licenses.
