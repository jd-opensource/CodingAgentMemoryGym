from __future__ import annotations

from collections import defaultdict
from typing import Any, Sequence

from collections.abc import Mapping

import numpy as np
import torch

from camp.action_gae import (
    IMMEDIATE_REWARD,
    IS_PADDING,
    ROLLOUT_DONE_FLAG,
    ROUTE_ID,
    DATA_SOURCE,
    TRAJECTORY_ROW_ORDER,
    TRAJECTORY_ROW_UID,
    TRAJECTORY_TERMINAL,
    TRAJECTORY_UID,
    _as_bool,
    _as_finite_float,
    _as_nonempty_str,
    _as_nonnegative_int,
    _config_value,
    _equal_route_token_mean_weighting,
    _require_metadata,
    _route_centered_global_scale,
    _routewise_masked_whiten,
)
from verl.trainer.ppo.core_algos import register_adv_est
import verl.utils.torch_functional as verl_F


@register_adv_est("amg_token_axis_gae")
def compute_amg_token_gae(
    *,
    batch: Mapping[str, torch.Tensor],
    non_tensor_batch: Mapping[str, Any],
    config: Any,
) -> tuple[torch.Tensor, torch.Tensor]:


    required_tensors = (
        "token_level_rewards",
        "values",
        "response_mask",
        "rollout_log_probs",
        "old_log_probs",
    )
    missing = [name for name in required_tensors if name not in batch]
    if missing:
        raise ValueError(f"AMG token GAE is missing tensor fields: {missing}")

    rewards = batch["token_level_rewards"]
    values = batch["values"]
    response_mask = batch["response_mask"]
    if (
        rewards.ndim != 2
        or values.shape != rewards.shape
        or response_mask.shape != rewards.shape
    ):
        raise ValueError(
            "AMG token GAE requires equal rank-2 reward/value/response-mask tensors: "
            f"rewards={tuple(rewards.shape)} values={tuple(values.shape)} "
            f"mask={tuple(response_mask.shape)}"
        )
    if not rewards.is_floating_point() or not values.is_floating_point():
        raise TypeError("AMG token GAE reward and value tensors must be floating point")
    if rewards.device != values.device or response_mask.device != values.device:
        raise ValueError("AMG token GAE tensors must share a device")
    if not bool(torch.logical_or(response_mask == 0, response_mask == 1).all().item()):
        raise ValueError("AMG token GAE response_mask must contain only zero or one")
    rollout_log_probs = batch["rollout_log_probs"]
    old_log_probs = batch["old_log_probs"]
    if rollout_log_probs.shape != rewards.shape or old_log_probs.shape != rewards.shape:
        raise ValueError(
            "AMG PPO requires rollout/old logprob tensors aligned with response tokens: "
            f"rollout={tuple(rollout_log_probs.shape)} "
            f"old={tuple(old_log_probs.shape)} rewards={tuple(rewards.shape)}"
        )
    if (
        not rollout_log_probs.is_floating_point()
        or not old_log_probs.is_floating_point()
    ):
        raise TypeError("AMG rollout and old logprob tensors must be floating point")
    if (
        rollout_log_probs.device != values.device
        or old_log_probs.device != values.device
    ):
        raise ValueError("AMG rollout and old logprob tensors must share the batch device")
    valid_token_mask = response_mask.to(dtype=torch.bool)
    rollout_policy_log_probs = rollout_log_probs[valid_token_mask]
    old_policy_log_probs = old_log_probs[valid_token_mask]
    if not bool(torch.isfinite(rollout_policy_log_probs).all().item()) or not bool(
        torch.isfinite(old_policy_log_probs).all().item()
    ):
        raise ValueError("AMG rollout and old policy-token logprobs must be finite")
    if not torch.equal(old_policy_log_probs, rollout_policy_log_probs):
        mismatch_count = int(
            torch.count_nonzero(old_policy_log_probs != rollout_policy_log_probs).item()
        )
        raise ValueError(
            "AMG bypass PPO requires old_log_probs to be exactly the rollout behavior "
            f"logprobs on every sampled policy token; mismatches={mismatch_count}"
        )

    row_count = rewards.shape[0]
    trajectory_uids = _require_metadata(non_tensor_batch, TRAJECTORY_UID, row_count)
    row_uids = _require_metadata(non_tensor_batch, TRAJECTORY_ROW_UID, row_count)
    row_orders = _require_metadata(non_tensor_batch, TRAJECTORY_ROW_ORDER, row_count)
    terminals = _require_metadata(non_tensor_batch, TRAJECTORY_TERMINAL, row_count)
    done_flags = _require_metadata(non_tensor_batch, ROLLOUT_DONE_FLAG, row_count)
    immediate_rewards = _require_metadata(non_tensor_batch, IMMEDIATE_REWARD, row_count)
    is_padding = non_tensor_batch.get(IS_PADDING, np.zeros(row_count, dtype=bool))
    if len(is_padding) != row_count:
        raise ValueError(f"AMG token GAE {IS_PADDING!r} must align with {row_count} rows")

    gamma = float(_config_value(config, "gamma", 1.0))
    lam = float(_config_value(config, "lam", 1.0))
    tolerance = float(_config_value(config, "amg_reward_tolerance", 1e-6))
    normalization = str(_config_value(config, "amg_advantage_normalization", "none"))
    route_weighting = str(_config_value(config, "amg_actor_route_weighting", "none"))
    if not np.isfinite(gamma) or not 0.0 <= gamma <= 1.0:
        raise ValueError(f"AMG token GAE gamma must be in [0, 1], got {gamma!r}")
    if not np.isfinite(lam) or not 0.0 <= lam <= 1.0:
        raise ValueError(f"AMG token GAE lambda must be in [0, 1], got {lam!r}")
    if not np.isfinite(tolerance) or tolerance < 0.0:
        raise ValueError(
            "AMG token GAE reward tolerance must be finite and non-negative"
        )
    if normalization not in {
        "none",
        "upstream_masked_whiten",
        "routewise_masked_whiten",
        "route_centered_global_scale",
    }:
        raise ValueError(
            "AMG token GAE amg_advantage_normalization must be 'none', "
            "'upstream_masked_whiten', 'routewise_masked_whiten', or "
            f"'route_centered_global_scale', got {normalization!r}"
        )
    if route_weighting not in {"none", "equal_route_token_mean"}:
        raise ValueError(
            "AMG token GAE amg_actor_route_weighting must be 'none' or "
            f"'equal_route_token_mean', got {route_weighting!r}"
        )
    if (
        route_weighting == "equal_route_token_mean"
        and normalization != "route_centered_global_scale"
    ):
        raise ValueError(
            "equal_route_token_mean actor weighting requires "
            "amg_advantage_normalization='route_centered_global_scale'"
        )

    route_ids: Sequence[Any] | None = None
    data_sources: Sequence[Any] | None = None
    if normalization in {
        "routewise_masked_whiten",
        "route_centered_global_scale",
    } or route_weighting == "equal_route_token_mean":
        route_ids = _require_metadata(non_tensor_batch, ROUTE_ID, row_count)
        data_sources = _require_metadata(non_tensor_batch, DATA_SOURCE, row_count)

    accumulator_dtype = torch.promote_types(rewards.dtype, values.dtype)
    if accumulator_dtype in (torch.float16, torch.bfloat16):
        accumulator_dtype = torch.float32
    real_policy_mask = valid_token_mask.clone()
    trajectories: dict[str, list[dict[str, Any]]] = defaultdict(list)
    seen_row_uids: set[str] = set()
    normalized_route_ids: list[str] = []
    for physical_row in range(row_count):
        if route_ids is not None and data_sources is not None:
            route_id = _as_nonempty_str(
                route_ids[physical_row], field=ROUTE_ID, row=physical_row
            )
            data_source = _as_nonempty_str(
                data_sources[physical_row], field=DATA_SOURCE, row=physical_row
            )
            if route_id != data_source:
                raise ValueError(
                    "AMG route metadata must agree between route_id and data_source: "
                    f"row={physical_row} route_id={route_id!r} "
                    f"data_source={data_source!r}"
                )
            normalized_route_ids.append(route_id)

        if _as_bool(is_padding[physical_row], field=IS_PADDING, row=physical_row):
            real_policy_mask[physical_row] = False
            continue

        trajectory_uid = str(trajectory_uids[physical_row])
        row_uid = str(row_uids[physical_row])
        if not trajectory_uid or not row_uid:
            raise ValueError(
                f"AMG token GAE requires non-empty trajectory/row UID at row {physical_row}"
            )
        if row_uid in seen_row_uids:
            raise ValueError(f"duplicate AMG trajectory row UID {row_uid!r}")
        seen_row_uids.add(row_uid)

        token_indices = torch.nonzero(
            valid_token_mask[physical_row], as_tuple=False
        ).flatten()
        if token_indices.numel() == 0:
            raise ValueError(
                f"real AMG token row {physical_row} has no sampled response token"
            )
        expected_prefix = torch.arange(
            token_indices.numel(),
            device=token_indices.device,
            dtype=token_indices.dtype,
        )
        if not torch.equal(token_indices, expected_prefix):
            raise ValueError(
                f"AMG token row {physical_row} response mask is not a contiguous prefix"
            )
        if not torch.isfinite(values[physical_row, token_indices]).all():
            raise ValueError(
                f"AMG token row {physical_row} contains non-finite values"
            )
        if not torch.isfinite(rewards[physical_row, token_indices]).all():
            raise ValueError(
                f"AMG token row {physical_row} contains non-finite rewards"
            )

        immediate_reward = _as_finite_float(
            immediate_rewards[physical_row], field=IMMEDIATE_REWARD, row=physical_row
        )
        packed_reward = rewards[physical_row, token_indices].to(accumulator_dtype).sum()
        expected_reward = torch.as_tensor(
            immediate_reward, device=values.device, dtype=accumulator_dtype
        )
        if not torch.isclose(packed_reward, expected_reward, rtol=0.0, atol=tolerance):
            raise ValueError(
                "AMG packed token reward differs from the immediate action reward: "
                f"row={physical_row} packed={float(packed_reward.item())} "
                f"immediate={immediate_reward}"
            )

        trajectories[trajectory_uid].append(
            {
                "physical_row": physical_row,
                "row_order": _as_nonnegative_int(
                    row_orders[physical_row], field=TRAJECTORY_ROW_ORDER, row=physical_row
                ),
                "terminal": _as_bool(
                    terminals[physical_row], field=TRAJECTORY_TERMINAL, row=physical_row
                ),
                "done": _as_bool(
                    done_flags[physical_row], field=ROLLOUT_DONE_FLAG, row=physical_row
                ),
                "reward": expected_reward,
                "token_count": int(token_indices.numel()),
                "route_id": (
                    normalized_route_ids[physical_row]
                    if normalization
                    in {"routewise_masked_whiten", "route_centered_global_scale"}
                    or route_weighting == "equal_route_token_mean"
                    else None
                ),
            }
        )

    if not trajectories:
        raise ValueError("AMG token GAE requires at least one real trajectory row")

    advantages = torch.zeros(
        values.shape, device=values.device, dtype=accumulator_dtype
    )
    returns = torch.zeros_like(advantages)
    with torch.no_grad():
        for trajectory_uid, rows in trajectories.items():
            rows.sort(key=lambda row: row["row_order"])
            actual_orders = [row["row_order"] for row in rows]
            expected_orders = list(range(len(rows)))
            if actual_orders != expected_orders:
                raise ValueError(
                    "AMG trajectory row order is incomplete or duplicated: "
                    f"trajectory={trajectory_uid!r} expected={expected_orders} actual={actual_orders}"
                )
            terminal_orders = [row["row_order"] for row in rows if row["terminal"]]
            if terminal_orders != [len(rows) - 1]:
                raise ValueError(
                    "exactly the final AMG row must be trajectory-terminal: "
                    f"trajectory={trajectory_uid!r} actual={terminal_orders}"
                )
            premature_done = [row["row_order"] for row in rows[:-1] if row["done"]]
            if premature_done:
                raise ValueError(
                    "AMG environment done appears before the final trajectory row: "
                    f"trajectory={trajectory_uid!r} rows={premature_done}"
                )

            if normalization in {
                "routewise_masked_whiten",
                "route_centered_global_scale",
            } or route_weighting == "equal_route_token_mean":
                trajectory_routes = {row["route_id"] for row in rows}
                if len(trajectory_routes) != 1:
                    raise ValueError(
                        "one AMG trajectory cannot span multiple routes: "
                        f"trajectory={trajectory_uid!r} "
                        f"routes={sorted(trajectory_routes)}"
                    )

            next_advantage = torch.zeros(
                (), device=values.device, dtype=accumulator_dtype
            )
            for reverse_index in range(len(rows) - 1, -1, -1):
                row = rows[reverse_index]
                physical_row = row["physical_row"]
                token_count = row["token_count"]
                if reverse_index + 1 < len(rows):


                    assert not row["done"], "row followed by more rows but marked done"
                    has_next = True
                    next_row = rows[reverse_index + 1]
                    next_row_state_value = values[
                        next_row["physical_row"], 0
                    ].to(accumulator_dtype)
                else:


                    has_next = False
                    next_row_state_value = torch.zeros(
                        (), device=values.device, dtype=accumulator_dtype
                    )
                for token_offset in range(token_count - 1, -1, -1):
                    state_value = values[physical_row, token_offset].to(
                        accumulator_dtype
                    )
                    if token_offset == token_count - 1:
                        token_reward = row["reward"]
                        if has_next:
                            next_value = next_row_state_value
                            continuation = 1.0
                        else:
                            next_value = torch.zeros(
                                (), device=values.device, dtype=accumulator_dtype
                            )
                            continuation = 0.0
                    else:
                        token_reward = torch.zeros(
                            (), device=values.device, dtype=accumulator_dtype
                        )
                        next_value = values[physical_row, token_offset + 1].to(
                            accumulator_dtype
                        )
                        continuation = 1.0
                    delta = (
                        token_reward
                        + gamma * continuation * next_value
                        - state_value
                    )
                    token_advantage = (
                        delta + gamma * lam * continuation * next_advantage
                    )
                    token_return = token_advantage + state_value
                    advantages[physical_row, token_offset] = token_advantage
                    returns[physical_row, token_offset] = token_return
                    next_advantage = token_advantage

    if normalization == "upstream_masked_whiten":
        advantages = verl_F.masked_whiten(advantages, real_policy_mask)
        advantages = advantages * real_policy_mask.to(dtype=advantages.dtype)
    elif normalization == "routewise_masked_whiten":
        advantages = _routewise_masked_whiten(
            advantages, real_policy_mask, normalized_route_ids
        )
    elif normalization == "route_centered_global_scale":
        advantages = _route_centered_global_scale(
            advantages, real_policy_mask, normalized_route_ids
        )

    if route_weighting == "equal_route_token_mean":
        advantages = _equal_route_token_mean_weighting(
            advantages, real_policy_mask, normalized_route_ids
        )

    return advantages, returns
