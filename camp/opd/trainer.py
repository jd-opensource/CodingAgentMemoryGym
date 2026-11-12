"""Compute advantages and integrate the method with the asynchronous learner."""
import json
import logging
import os
from enum import Enum

import numpy as np
import torch
import transfer_queue as tq
from omegaconf import DictConfig
from tensordict import TensorDict

from verl.protocol import DataProto
from verl.trainer.ppo.v1.trainer_base import register_trainer
from verl.trainer.ppo.v1.trainer_separate_async import PPOTrainerSeparateAsync
from verl.utils.transferqueue_utils import KVBatchMeta
from verl.workers.utils.padding import response_to_nested

from camp.action_gae import (
    DATA_SOURCE,
    IMMEDIATE_REWARD,
    IS_PADDING,
    ROLLOUT_DONE_FLAG,
    ROUTE_ID,
    TRAJECTORY_ROW_ORDER,
    TRAJECTORY_ROW_UID,
    TRAJECTORY_TERMINAL,
    TRAJECTORY_UID,
)

from camp.token_gae import compute_amg_token_gae

logger = logging.getLogger(__name__)

_AMG_ESTIMATOR_FNS = {
    "amg_token_axis_gae": compute_amg_token_gae,
}

_AMG_METADATA_KEYS = (
    TRAJECTORY_UID,
    TRAJECTORY_ROW_UID,
    TRAJECTORY_ROW_ORDER,
    TRAJECTORY_TERMINAL,
    ROLLOUT_DONE_FLAG,
    IMMEDIATE_REWARD,
    ROUTE_ID,
    DATA_SOURCE,
)

def _extra_fields_to_dicts(column) -> list:

    elements = []
    for element in column:
        if not isinstance(element, dict):
            data_attr = getattr(element, "data", None)
            if isinstance(data_attr, dict):
                element = data_attr
        elements.append(element)
    return elements

@register_trainer("amg_separate_async")
class AMGPPOTrainerSeparateAsync(PPOTrainerSeparateAsync):

    def __init__(self, config: DictConfig):

        estimator_name = config.algorithm.adv_estimator
        if isinstance(estimator_name, Enum):
            estimator_name = estimator_name.value
        estimator_name = str(estimator_name)
        estimator_fn = _AMG_ESTIMATOR_FNS.get(estimator_name)
        if estimator_fn is None:
            raise ValueError(
                f"amg_separate_async only supports algorithm.adv_estimator in "
                f"{sorted(_AMG_ESTIMATOR_FNS)}, got {estimator_name!r}"
            )

        print(
            f"amg_separate_async advantage estimator resolved: {estimator_name} "
            f"-> {estimator_fn.__name__}",
            flush=True,
        )
        self._amg_estimator_fn = estimator_fn
        super().__init__(config)

    def _compute_advantage(self, batch: KVBatchMeta, metrics: dict) -> KVBatchMeta:

        fields = [
            "uid",
            "response_mask",
            "rm_scores",
            "rollout_log_probs",
            "old_log_probs",
            "ref_log_prob",
            "values",
            "extra_fields",
        ]
        data = tq.kv_batch_get(keys=batch.keys, partition_id=batch.partition_id, select_fields=fields)

        response_mask = data["response_mask"]
        extra_fields = _extra_fields_to_dicts(data.pop("extra_fields"))
        data = DataProto(batch=data.to_padded_tensor())

        if self.config.algorithm.use_kl_in_reward:
            raise NotImplementedError(
                "amg_separate_async does not support algorithm.use_kl_in_reward; "
                "AMG rewards are per-action environment rewards"
            )
        data.batch["token_level_rewards"] = data.batch["rm_scores"]

        if "values" not in data.batch:
            data.batch["values"] = torch.zeros_like(data.batch["token_level_rewards"])

        row_count = len(extra_fields)
        if row_count != len(batch.keys):
            raise ValueError(
                f"AMG advantage step row mismatch: extra_fields={row_count} keys={len(batch.keys)}"
            )
        non_tensor_batch = {
            IS_PADDING: np.array([tag.get("is_padding", False) for tag in batch.tags], dtype=bool),
        }
        for key in _AMG_METADATA_KEYS:
            values = np.empty(row_count, dtype=object)
            for row, extra in enumerate(extra_fields):
                if not isinstance(extra, dict) or key not in extra:
                    raise ValueError(
                        f"AMG action GAE requires non-tensor metadata {key!r} on row {row} "
                        f"(TQ key={batch.keys[row]}); the manager bridge or the agent loop "
                        "dropped it"
                    )
                values[row] = extra[key]
            non_tensor_batch[key] = values
        data.non_tensor_batch.update(non_tensor_batch)

        advantages, returns = self._amg_estimator_fn(
            batch=data.batch,
            non_tensor_batch=data.non_tensor_batch,
            config=self.config.algorithm,
        )

        output = {
            "advantages": response_to_nested(advantages, response_mask),
            "returns": response_to_nested(returns, response_mask),
        }
        output = TensorDict(output, batch_size=len(batch))

        batch = tq.kv_batch_put(keys=batch.keys, partition_id=batch.partition_id, fields=output)

        return batch

    def _log_rollout_data(self, batch: KVBatchMeta, timing_raw: dict, rollout_data_dir: str):

        super()._log_rollout_data(batch, timing_raw, rollout_data_dir)

        data = tq.kv_batch_get(
            keys=batch.keys, partition_id=batch.partition_id, select_fields=["extra_fields"]
        )
        extra_fields = _extra_fields_to_dicts(data["extra_fields"])

        os.makedirs(rollout_data_dir, exist_ok=True)
        path = os.path.join(rollout_data_dir, f"amg_step_records_globalstep{self.global_steps}.jsonl")
        written = 0
        with open(path, "w") as fh:
            for key, tag, extra in zip(batch.keys, batch.tags, extra_fields, strict=True):
                if tag.get("is_padding", False):
                    continue
                record = extra.get("step_record_json") if isinstance(extra, dict) else None
                if record is None:
                    raise ValueError(
                        f"AMG step record missing on real row {key!r}; the task-neutral "
                        "loop must emit step_record_json in extra_fields"
                    )
                json.loads(record)  
                fh.write(record + "\n")
                written += 1
        logger.info("AMG step records dumped: %d real rows -> %s", written, path)
