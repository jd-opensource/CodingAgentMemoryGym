# Training

## Installation

Use a dedicated Linux x86-64 Python 3.12 environment. The provided recipes target eight Blackwell GPUs. Their attention-kernel choices and memory budgets are hardware-specific, not a promise of compatibility with every CUDA card.

```bash
python -m pip install -r requirements-training.txt
python -m pip install -e . --no-deps
python scripts/patch_sglang.py
```

`requirements.lock` records the source training environment's installed versions; `runtime-overrides.txt` records additional kernel dependencies. These are provenance inputs, not evidence of a successful fresh installation. GPU installation and execution remain to be verified. Check the patch script's output rather than assuming that a different SGLang version accepts it.

Use local model directories containing configuration, tokenizer/chat template and all weight shards. Do not mix tokenizer files from one model revision with weights from another. Record their hashes with the run.

## What differs between the methods

| Setting | CAMP RL | CAMP-II OPD |
|---|---|---|
| Learning GPUs | 6 | 4 |
| Sampling GPUs | 2 | 2 |
| Teacher GPUs | 0 | 2 |
| Task rewards in actor learning | Yes | No |
| Learned critic | Yes | No |
| Distillation | Disabled | K1 feedback from teacher probabilities of the sampled tokens |
| Actor learning rate | 0.000001 | 0.000001 |
| Critic learning rate | 0.00001 | Not used |
| Optimizer updates | 100 | 100 |
| Completed episodes per update | 64 | 64 |

Both use asynchronous sampling, one shared task-independent sampling implementation per method, and the same five-domain task schedule. Environment state transitions remain in the environments. The OPD recipe scores all sampled response rows with the teacher; it does not use task rewards as an additional actor objective. The inherited `topk=32` setting is inactive for K1: this loss requests the teacher log probability of each sampled token, not a top-32 distribution.

The two method integration directories preserve their respective algorithms, including output-limit handling and critic-free behavior. Shared advantage utilities, clients and task data are outside those directories.

## Inspect before running

```bash
python -m camp.train --method rl --student /models/Qwen3.5-4B \
  --output ./runs/example --print-config
```

The default route template is useful for inspection. For actual execution, generate routes bound to the installed task services and use the corresponding schedule. Their hashes must agree.

Additional Hydra settings can be passed after `--`:

```bash
python -m camp.train --method rl --student /models/Qwen3.5-4B \
  --routes prepared/routes.json --schedule prepared/train_schedule.jsonl \
  --output runs/installation-check -- trainer.total_training_steps=1
```

A one-update run checks the installation; it is not a trained result. Changing episode count, sampling count, context length, task ordering or teacher settings changes the experiment and must be recorded.

## Checkpoints and restart

Checkpoints are written under `OUTPUT/checkpoints/`; trajectory records are under `OUTPUT/rollout_data/`. The default retention policy keeps the most recent checkpoint. Copy any checkpoint you need to retain before continuing a long run.

A fresh command never automatically resumes. To resume, pass the full training checkpoint directory, including actor, critic where applicable, and dataloader state:

```bash
python -m camp.train --method rl --student /models/Qwen3.5-4B \
  --routes prepared/routes.json --schedule prepared/train_schedule.jsonl \
  --output runs/camp-rl --resume runs/camp-rl/checkpoints/global_step_10
```

Do not copy only actor weights and call that an exact training resume. Do not evaluate an incomplete checkpoint as the declared training endpoint.

Each invocation writes diagnostic counters in a new `OUTPUT/state/<attempt>/` directory. Resuming restores the checkpoint, not old transient failure counters. Model, dataset, service, output and resume settings are controlled by named command options and cannot be replaced through raw Hydra overrides.
