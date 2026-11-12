"""Assemble trajectory rows for distributed training."""
import logging
import os
from typing import Any

import ray
import torch
import transfer_queue as tq
from tensordict import TensorDict

from verl.experimental.agent_loop import AgentLoopOutput
from verl.trainer.ppo.v1.agent_loop_tq import AgentLoopManagerTQ, AgentLoopWorkerTQ
from verl.utils.tensordict_utils import list_of_dict_to_tensordict

from .agent_loop import check_exclusion_fast_fail

logger = logging.getLogger(__name__)
logger.setLevel(os.getenv("VERL_LOGGING_LEVEL", "INFO"))

_AMG_REQUIRED_EXTRA_FIELDS = (
    "trajectory_uid",
    "trajectory_row_uid",
    "trajectory_row_order",
    "trajectory_terminal",
    "rollout_done_flag",
    "immediate_reward",
    "route_id",
    "data_source",
)

_TQ_WORKER_ACCESSORS = (
    lambda cls: cls.__ray_metadata__.modified_class,
    lambda cls: cls.modified_class,
)
_AgentLoopWorkerTQ = None
for _access in _TQ_WORKER_ACCESSORS:
    try:
        _candidate = _access(AgentLoopWorkerTQ)
    except AttributeError:
        continue
    if isinstance(_candidate, type):
        _AgentLoopWorkerTQ = _candidate
        break
if _AgentLoopWorkerTQ is None:
    raise TypeError(
        "could not recover the plain class behind the AgentLoopWorkerTQ actor "
        "on this ray version; refactor verl/trainer/ppo/v1/agent_loop_tq.py to "
        "expose the undecorated worker class instead."
    )

class _AgentLoopWorkerAMG(_AgentLoopWorkerTQ):
    async def _agent_loop_postprocess(
        self, output: AgentLoopOutput | list[AgentLoopOutput], validate, **kwargs
    ) -> None:

        uid, session_id = kwargs["uid"], kwargs["session_id"]
        outputs = output if isinstance(output, list) else [output]
        if not outputs:
            logger.warning(f"Empty output for prompt {uid}_{session_id}")
            return

        await self._compute_score(outputs, kwargs=kwargs)

        for output in outputs:
            await self._compute_teacher_logprobs(
                output,
                prompt_ids=output.prompt_ids,
                response_ids=output.response_ids,
                validate=validate,
                sample_kwargs=kwargs,
            )

        for i, output in enumerate(outputs):
            missing = [key for key in _AMG_REQUIRED_EXTRA_FIELDS if key not in output.extra_fields]
            if missing:
                raise ValueError(
                    f"AMG agent loop output {uid}_{session_id}_{i} is missing required "
                    f"metadata {missing}; the task-neutral loop must emit all of "
                    f"{_AMG_REQUIRED_EXTRA_FIELDS} in extra_fields"
                )

        keys, fields, tags = [], [], []
        for i, output in enumerate(outputs):
            prompts = torch.tensor(output.prompt_ids, dtype=torch.int64)
            responses = torch.tensor(output.response_ids, dtype=torch.int64)
            input_ids = torch.cat([prompts, responses], dim=0)
            attention_mask = torch.ones_like(input_ids, dtype=torch.int64)
            multi_modal_inputs = self._compute_multi_modal_inputs(output, input_ids)
            position_ids = self._compute_position_ids(
                input_ids.unsqueeze(0), attention_mask.unsqueeze(0), multi_modal_inputs
            ).squeeze(0)

            keys.append(f"{uid}_{session_id}_{i}")
            field = output.as_dict()
            field.update(kwargs)
            
            field.pop("multi_modal_data", None)
            
            field["loss_mask"] = field["response_mask"]
            field["input_ids"] = input_ids
            field["position_ids"] = position_ids
            field["multi_modal_inputs"] = multi_modal_inputs
            fields.append(field)
            prompt_len, response_len = field["prompts"].size(0), field["responses"].size(0)
            tags.append(
                {
                    "status": "success",
                    "prompt_len": prompt_len,
                    "response_len": response_len,
                    "seq_len": prompt_len + response_len,

                    "global_steps": kwargs["global_steps"],
                    
                    "min_global_steps": field["extra_fields"].get("min_global_steps"),
                    
                    "max_global_steps": field["extra_fields"].get("max_global_steps"),
                }
            )

        await tq.async_kv_batch_put(
            keys=keys,
            fields=list_of_dict_to_tensordict(fields),
            tags=tags,
            partition_id="train" if not validate else "val",
        )

AgentLoopWorkerAMG = ray.remote(_AgentLoopWorkerAMG)

def _dispatched_global_step(prompts: Any) -> Any:

    try:
        value = prompts["global_steps"]
    except Exception:
        return None
    value = getattr(value, "data", value)  
    try:
        return int(value)
    except (TypeError, ValueError):
        return None

class AgentLoopManagerAMG(AgentLoopManagerTQ):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.agent_loop_workers_class = AgentLoopWorkerAMG

    def generate_sequences(self, prompts: TensorDict) -> None:

        check_exclusion_fast_fail(_dispatched_global_step(prompts))
        super().generate_sequences(prompts)
