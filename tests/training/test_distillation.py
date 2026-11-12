import importlib.util
from pathlib import Path
from types import SimpleNamespace

import torch
from tensordict import TensorDict

from verl.trainer.distillation.losses import distillation_loss, compute_distillation_loss_range
from verl.experimental.teacher_loop.teacher_manager import _get_teacher_sampling_params
from verl.workers.config import ActorConfig, DistillationLossConfig


def test_sampled_token_distillation_backward():
    config = ActorConfig(strategy="fsdp2", rollout_n=1, ppo_micro_batch_size_per_gpu=1, loss_agg_mode="token-mean")
    loss_config = DistillationLossConfig(loss_mode="k1", topk=32, use_task_rewards=False, use_policy_gradient=True, loss_max_clamp=10.0, clip_ratio=0.2)
    distill_config = SimpleNamespace(distillation_loss=loss_config)
    student = torch.tensor([-1.0, -3.0, 0.0], requires_grad=True)
    data = TensorDict({
        "prompts": torch.tensor([[1]]),
        "responses": torch.tensor([[2, 3]]),
        "attention_mask": torch.ones(1, 3, dtype=torch.long),
        "response_mask": torch.ones(1, 2, dtype=torch.bool),
        "teacher_logprobs": torch.tensor([[-1.5], [-2.5], [0.0]]),
        "old_log_probs": student.detach()[:2].view(1, 2),
        "dp_size": 1,
        "batch_num_tokens": 2,
        "global_batch_size": 1,
    }, batch_size=[])
    loss, metrics = distillation_loss(config, distill_config, {"log_probs": student}, data)
    assert torch.isfinite(loss)
    loss.backward()
    torch.testing.assert_close(student.grad, torch.tensor([0.25, -0.25, 0.0]))
    assert "distillation/pg_clipfrac" in metrics


def test_empty_distillation_span():
    metrics = compute_distillation_loss_range(torch.zeros(1, 2), torch.zeros(1, 2, dtype=torch.bool))
    assert metrics == {}


def test_teacher_sampling_contract():
    teacher = SimpleNamespace(inference=SimpleNamespace(temperature=1.0))
    loss = DistillationLossConfig(loss_mode="k1", use_policy_gradient=True, topk=32)
    params = _get_teacher_sampling_params(teacher, loss)
    assert params["prompt_logprobs"] == 0
    assert params["detokenize"] is False


def test_sampling_api_compatibility(tmp_path):
    import sglang.srt.sampling.sampling_params as sampling
    root = Path(__file__).resolve().parents[2]
    spec = importlib.util.spec_from_file_location("camp_sampling_patch", root / "scripts/patch_sglang.py")
    patcher = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(patcher)
    source = Path(sampling.__file__).read_text()
    patched = patcher.patched_source(source)
    assert patcher.patched_source(patched) == patched
    path = tmp_path / "sampling_params.py"
    path.write_text(patched)
    spec = importlib.util.spec_from_file_location("camp_patched_sampling", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    params = module.SamplingParams(max_new_tokens=1, detokenize=False)
    assert params.detokenize is False
