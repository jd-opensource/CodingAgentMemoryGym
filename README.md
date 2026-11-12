# Coding Agent Memory Gym

Train language-model agents to use files as memory during long tasks.

[CAMP paper](https://arxiv.org/abs/2609.34422) · [CAMP-II paper](https://liruiluo.github.io/agentmemorygym-v2/assets/paper.pdf) · [CAMP-II project](https://liruiluo.github.io/agentmemorygym-v2/)

This repository brings together **one environment suite, CAMG-II**, and two training methods:

| Method | Learning signal | Teacher during training | Teacher during evaluation |
|---|---|---|---|
| **CAMP — reinforcement learning (RL)** | Task rewards, with an actor and a learned value function | No | No |
| **CAMP-II — on-policy distillation (OPD)** | Token-level feedback from a frozen teacher on the student's own trajectories | Yes | No |

Both recipes use the **same CAMG-II tasks and environment interfaces**.

## 1. What the environments do

| Environment | Task | Feedback |
|---|---|---|
| **Shop** | Complete six related shopping sessions while remembering earlier requirements | Purchase correctness and task progress |
| **Coding** | Fix a software issue in a repository | Executable tests |
| **AutoResearch** | Build and improve a machine-learning solution | The task's native metric, checked separately from the agent |
| **General** | Complete knowledge-work tasks using tools | Task-specific verification and rubric-based judging |
| **Visual** | Implement a website from a user request | Screenshot-based visual assessment |

The agent works in an episode-specific directory. Its files survive context resets; the active model context does not. Memory is written and read through ordinary file operations, without a separate reward for writing notes. Environment-specific task actions are also preserved.

## 2. Install

The CUDA training environment requires **Linux x86-64, Python 3.12 and eight compatible NVIDIA GPUs**. Task services have additional dependencies; see [environment setup](docs/environments.md). Configuration inspection and lightweight tests also run on a Mac or CPU machine.

```bash
git clone https://github.com/jd-opensource/CodingAgentMemoryGym.git
cd CodingAgentMemoryGym
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test]'
python -m pytest tests/unit
```

For training, install the [pinned training dependencies](docs/training.md#installation) in a separate environment and use the modified framework included in `verl/`.

## 3. Prepare data and task services

Follow [data preparation](docs/data.md), then [environment setup](docs/environments.md). Downloads come from the original publishers. Dataset, model and container terms remain separate from this repository's code license.

The included `camg/data/train_schedule.jsonl` specifies **12,800 ordered task references**. Download the corresponding task assets with the data-preparation commands. The default recipes run for 100 updates with 64 completed episodes per update.

All task services bind to loopback by default. Run the services and their clients on the same host. Never expose these execution services directly to the Internet.

## 4. Train

First obtain local copies of [Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B) and, for OPD, [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B). Preserve the model, tokenizer and chat-template versions together.

**CAMP reinforcement learning:**

```bash
python -m camp.train --method rl \
  --student /models/Qwen3.5-4B \
  --routes ./prepared/routes.json \
  --schedule ./prepared/train_schedule.jsonl \
  --output ./runs/camp-rl
```

**CAMP-II on-policy distillation:**

```bash
python -m camp.train --method opd \
  --student /models/Qwen3.5-4B \
  --teacher /models/Qwen3.8-27B \
  --routes ./prepared/routes.json \
  --schedule ./prepared/train_schedule.jsonl \
  --output ./runs/camp-ii-opd
```

Append `--print-config` to inspect the resolved command, or `--check-inputs` to validate local input files. A new run requires an empty output directory. Resuming requires an explicit `--resume` checkpoint.

See [training](docs/training.md) for hardware allocation, algorithm settings, checkpoints and troubleshooting.

## 5. Evaluate

Evaluate the trained student without a teacher, using the same task split, tool interface, context budget and judge configuration for both methods. See the [evaluation protocol](docs/evaluation.md).

## 6. Repository guide

```text
camp/                     RL and OPD training code
  rl/                     Task-reward RL integration
  opd/                    On-policy distillation integration
  configs/                Separate method recipes
camg/                     Shared clients, task services and data preparation
  services/               Shop, Coding, AutoResearch, General and Visual
  data/                   Ordered task references and dataset manifests
runtimes/autoresearch/    Isolated execution and private grading runtime
third_party/mimo_runtime/ Required General/Visual runtime components
verl/                    Distributed training framework snapshot
scripts/                  Installation and verification helpers
tests/                    Local and training-runtime tests
docs/                     Setup, methods, data, evaluation and testing
```

The interface keys `webshop`, `swesmith`, `openmle_fast`, `agentgeneral` and `webdev` correspond to Shop, Coding, AutoResearch, General and Visual, respectively. See [testing](docs/verification.md) for development commands.

## 7. Licenses and attribution

Repository code is distributed under [Apache-2.0](LICENSE), with retained MIT and Apache notices for incorporated components. See [third-party notices](THIRD_PARTY.md). In particular, OpenMLE materials and their underlying datasets can carry noncommercial or other source-specific terms. The repository license does not replace those terms.

Please cite the relevant CAMP/CAMP-II work and the original task sources when using them. Source and packaging changes are recorded in [provenance](docs/provenance.md).
