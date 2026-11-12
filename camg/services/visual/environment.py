from __future__ import annotations

import json
import logging
import os
import re
import threading
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from .actions import parse_policy_action
from .bridge import WebdevBridge, load_mimoagent_config

logger = logging.getLogger("camg.services.visual.environment")

EPISODE_SCHEMA = "webdev_website_v1"
REWARD_CONTRACT = "webdev_vision_rubric_outcome_finish_only_v1"
COMPACTION_CONTRACT = "policy_filesystem_checkpoint_then_client_replace_v2"
INVALID_ACTION_REWARD = -0.1
HORIZON_FAILURE_REWARD = 0.0
NO_SUBMISSION_PENALTY = -0.01
DEFAULT_MAX_STEPS = 64
DEFAULT_MAX_OBSERVATION_BYTES = 32768
FINISH_TOOL = "finish"

PREVIEW_MARKER_BEGIN = "[[WDIMG:"
PREVIEW_MARKER_END = "]]"
PREVIEW_MARKER_RE = re.compile(
    re.escape(PREVIEW_MARKER_BEGIN)
    + r"(data:image/jpeg;base64,[A-Za-z0-9+/=]+)"
    + re.escape(PREVIEW_MARKER_END)
)
DEFAULT_DIMS_DIR = "/dev/shm/webdev-dims"

def split_preview_markers(text: str) -> tuple[str, list[str]]:

    images: list[str] = []
    parts: list[str] = []
    last = 0
    for match in PREVIEW_MARKER_RE.finditer(text):
        parts.append(text[last : match.start()])
        images.append(match.group(1))
        last = match.end()
    parts.append(text[last:])
    return "".join(parts), images

@dataclass(frozen=True)
class EpisodeStep:
    observation: str
    reward: float
    done: bool
    info: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return {
            "observation": self.observation,
            "state": self.observation,
            "reward": self.reward,
            "done": self.done,
            "info": dict(self.info),
        }

@dataclass
class _Episode:
    slot_id: int
    audit_id: str
    started_at: str
    data_idx: int
    instance_id: str
    bridge: WebdevBridge | None = None
    observation: str = ""
    initial_observation: str = ""
    reward: float = 0.0
    done: bool = False
    step_count: int = 0
    terminal_reason: str | None = None
    grade: float | None = None
    checkpoint_before: dict[str, Any] | None = None
    raw_tool_output: str = ""
    evidence: list[dict[str, Any]] = field(default_factory=list)

@dataclass
class _Slot:
    slot_id: int
    lock: threading.Lock = field(default_factory=threading.Lock)
    episode: _Episode | None = None

def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

class WebdevEpisodeManager:
    def __init__(
        self,
        *,
        parquet_path: str,
        mimoagent_config_path: str,
        max_steps: int = DEFAULT_MAX_STEPS,
        prompt_policy_turns: int | None = None,
        max_observation_bytes: int = DEFAULT_MAX_OBSERVATION_BYTES,
        reward_timeout: float = 900.0,
    ):
        self.parquet_path = str(parquet_path)
        self.mimoagent_config = load_mimoagent_config(mimoagent_config_path)
        self.max_steps = int(max_steps)
        if prompt_policy_turns is None:
            prompt_policy_turns = max_steps
        if type(prompt_policy_turns) is not int or prompt_policy_turns <= 0:
            raise ValueError(
                "Webdev prompt_policy_turns must be a positive integer"
            )
        self.prompt_policy_turns = int(prompt_policy_turns)
        self.max_observation_bytes = int(max_observation_bytes)
        self.reward_timeout = float(reward_timeout)
        self._dataset_lock = threading.Lock()
        self._dataset: list[dict[str, Any]] | None = None
        self._slots: dict[int, _Slot] = {}
        self._slots_lock = threading.Lock()

    def _load_dataset(self) -> list[dict[str, Any]]:
        import pandas as pd

        with self._dataset_lock:
            if self._dataset is not None:
                return self._dataset
            frame = pd.read_parquet(self.parquet_path)
            records: list[dict[str, Any]] = []
            for position, row in frame.iterrows():
                extra = row.get("extra_info")
                extra = extra if isinstance(extra, dict) else {}
                instance_json = extra.get("instance_json")
                if isinstance(instance_json, str):
                    try:
                        instance = json.loads(instance_json)
                    except json.JSONDecodeError:
                        logger.warning("row %s: instance_json unreadable", position)
                        continue
                elif isinstance(instance_json, dict):
                    instance = instance_json
                else:
                    instance = dict(extra)
                prompt = row.get("prompt")
                task_text = ""
                if prompt is not None and hasattr(prompt, "__len__"):
                    for message in list(prompt):
                        if (
                            isinstance(message, dict)
                            and message.get("role") == "user"
                        ):
                            task_text = str(message.get("content") or "")
                            break
                if not task_text:
                    task_text = str(instance.get("problem_statement") or "")
                records.append(
                    {
                        "data_idx": int(position),
                        "instance_id": str(
                            instance.get("instance_id")
                            or extra.get("instance_id")
                            or f"row_{position}"
                        ),
                        "instance": instance,
                        "task_text": task_text,
                    }
                )
            self._dataset = records
            return records

    def create(self) -> int:
        with self._slots_lock:
            slot_id = 0
            while slot_id in self._slots:
                slot_id += 1
            self._slots[slot_id] = _Slot(slot_id=slot_id)
            return slot_id

    def _slot(self, slot_id: int) -> _Slot:
        with self._slots_lock:
            slot = self._slots.get(slot_id)
        if slot is None:
            raise KeyError(f"unknown slot {slot_id}")
        return slot

    def _episode(self, slot: _Slot) -> _Episode:
        if slot.episode is None:
            raise RuntimeError(f"slot {slot.slot_id} has no active episode")
        return slot.episode

    def reset(self, slot_id: int, data_idx: int) -> EpisodeStep:
        slot = self._slot(slot_id)
        with slot.lock:
            self._close_episode(slot, close_reason="reset")
            record = self._load_dataset()[data_idx]
            episode = _Episode(
                slot_id=slot_id,
                audit_id=uuid.uuid4().hex,
                started_at=_utc_now(),
                data_idx=record["data_idx"],
                instance_id=record["instance_id"],
            )
            bridge = WebdevBridge(
                instance=record["instance"],
                config=self.mimoagent_config,
                instance_id=record["instance_id"],
            )
            try:
                bridge.setup()
            except Exception as exc:
                bridge.close()
                raise RuntimeError(
                    f"webdev env setup failed for {record['instance_id']}: {exc}"
                ) from exc
            episode.bridge = bridge
            bridge.touch_step_marker()
            episode.checkpoint_before = bridge.checkpoint_state()
            episode.initial_observation = self._initial_observation(record, bridge)
            episode.observation = episode.initial_observation
            episode.evidence.append(
                {
                    "event": "reset",
                    "slot_id": slot_id,
                    "audit_id": episode.audit_id,
                    "data_idx": record["data_idx"],
                    "instance_id": record["instance_id"],
                    "tool_names": bridge.tool_names(),
                    "observation": episode.initial_observation,
                }
            )
            slot.episode = episode
            return self._public_step(episode, action_kind="reset")

    def step(self, slot_id: int, raw_output: str) -> EpisodeStep:
        slot = self._slot(slot_id)
        with slot.lock:
            episode = self._episode(slot)
            if episode.done:
                raise RuntimeError("webdev episode is already terminal")
            episode.step_count += 1
            episode.reward = 0.0
            action = parse_policy_action(raw_output)
            evidence: dict[str, Any] = {
                "event": "policy_step",
                "step": episode.step_count,
                "observation_before": episode.observation,
                "action": action.as_evidence(),
            }
            public_action_kind = action.kind

            if action.kind == "parser_error":
                episode.observation = self._parser_error_observation(action)
                episode.reward = INVALID_ACTION_REWARD
                evidence["result"] = {"parser_error": action.error}
            else:
                assert episode.bridge is not None
                calls = list(action.calls) if action.calls else [
                    (action.function_name or "", dict(action.parameters or {}))
                ]
                total = len(calls)
                obs_parts: list[str] = []
                for call_index, (function_name, params) in enumerate(
                    calls, start=1
                ):
                    labeled = total > 1
                    if function_name == FINISH_TOOL:
                        answer = params.get("answer", "")
                        if episode.bridge is not None:
                            episode.bridge.set_final_answer(answer)
                        episode.done = True
                        episode.terminal_reason = "policy_finish"
                        public_action_kind = "final"
                        if episode.bridge is not None:

                            reward, output, extra = episode.bridge.calculate_reward(
                                timeout=self.reward_timeout
                            )
                            episode.grade = reward
                            episode.reward = float(reward)
                            obs_parts.append(
                                "Episode finished and graded. "
                                f"reward={float(reward):.4f}"
                            )
                            evidence["result"] = {
                                "finished": True,
                                "grade": float(reward),
                                "grading_output": str(output)[:2000],
                                "grading_extra": {
                                    k: v
                                    for k, v in (extra or {}).items()
                                    if isinstance(v, (str, int, float, bool, dict))
                                },
                            }
                            self._persist_grading_extra(
                                episode, float(reward), str(output), extra
                            )
                        else:
                            obs_parts.append(
                                "Episode finished. Grading unavailable (no bridge)."
                            )
                            evidence["result"] = {"finished": True}
                        break
                    if function_name not in episode.bridge.tool_names():
                        message = (
                            f"Unknown tool '{function_name}'. Available tools: "
                            + ", ".join(episode.bridge.tool_names())
                            + "."
                        )
                        episode.reward = INVALID_ACTION_REWARD
                        if labeled:
                            evidence.setdefault("unknown_tools", []).append(
                                function_name
                            )
                            obs_parts.append(
                                f"[call {call_index}/{total} | {function_name}]\n{message}"
                            )
                        else:
                            evidence["result"] = {"unknown_tool": function_name}
                            obs_parts.append(message)
                        continue
                    coerced = episode.bridge.coerce_params(
                        function_name, dict(params)
                    )
                    outcome = episode.bridge.execute(function_name, coerced)
                    entry = {
                        k: v for k, v in outcome.items() if k != "result"
                    }
                    if outcome["kind"] == "ok":
                        result = outcome.get("result")
                        episode.raw_tool_output = (
                            str(result.get("output", ""))
                            if isinstance(result, Mapping)
                            else ""
                        )
                        part = self._format_tool_result(result)
                    elif outcome["kind"] == "tool_exception":
                        part = (
                            "Tool error (recoverable): "
                            + str(outcome.get("message", ""))[:4000]
                        )
                        entry["recoverable"] = True
                    elif outcome["kind"] == "limits_exceeded":
                        episode.done = True
                        episode.terminal_reason = "limits_exceeded"
                        part = (
                            "Tool budget exceeded; episode terminated. "
                            + str(outcome.get("message", ""))[:1000]
                        )
                    else:  
                        episode.done = True
                        episode.terminal_reason = "infra_error"
                        part = (
                            "Environment infrastructure error; episode terminated."
                        )
                    if labeled:
                        evidence.setdefault("results", []).append(entry)
                        obs_parts.append(
                            f"[call {call_index}/{total} | {function_name}]\n{part}"
                        )
                    else:
                        evidence["result"] = entry
                        obs_parts.append(part)
                    if episode.done:
                        break
                if obs_parts:
                    episode.observation = (
                        obs_parts[0] if total == 1 else "\n\n".join(obs_parts)
                    )

            evidence["observation_after"] = episode.observation
            episode.evidence.append(evidence)

            wrapper_evidence = self._build_wrapper_evidence(
                episode, action=action
            )
            return self._public_step(
                episode,
                action_kind=public_action_kind,
                wrapper_evidence=wrapper_evidence,
            )

    def observation(self, slot_id: int) -> str:
        slot = self._slot(slot_id)
        with slot.lock:
            return self._episode(slot).observation

    def finalize_horizon(self, slot_id: int) -> EpisodeStep:

        slot = self._slot(slot_id)
        with slot.lock:
            episode = self._episode(slot)
            episode.done = True
            if episode.terminal_reason is None:
                episode.terminal_reason = "horizon"
                episode.reward = NO_SUBMISSION_PENALTY
                episode.observation = (
                    "Policy budget exhausted without a submission. "
                    f"reward={NO_SUBMISSION_PENALTY:.4f}"
                )
            else:
                episode.observation = (
                    f"Episode already terminal ({episode.terminal_reason}). "
                    f"reward={episode.reward:.4f}"
                )
            episode.evidence.append(
                {
                    "event": "finalize_horizon",
                    "reward": episode.reward,
                    "terminal_reason": episode.terminal_reason,
                }
            )
            return self._public_step(episode, action_kind="horizon")

    def detail(self, slot_id: int) -> dict[str, Any]:
        slot = self._slot(slot_id)
        with slot.lock:
            episode = self._episode(slot)
            return {
                "schema": EPISODE_SCHEMA,
                "audit_id": episode.audit_id,
                "instance_id": episode.instance_id,
                "data_idx": episode.data_idx,
                "step_count": episode.step_count,
                "terminal_reason": episode.terminal_reason,
                "grade": episode.grade,
                "tool_names": (
                    episode.bridge.tool_names() if episode.bridge else []
                ),
                "evidence": list(episode.evidence),
            }

    def close(self, slot_id: int) -> dict[str, Any]:
        slot = self._slot(slot_id)
        with slot.lock:
            self._close_episode(slot, close_reason="close")
            with self._slots_lock:
                self._slots.pop(slot_id, None)
            return {"schema": EPISODE_SCHEMA, "closed": slot_id}

    def metadata(self) -> dict[str, Any]:
        dataset = self._load_dataset()
        with self._slots_lock:
            active = sum(
                1 for slot in self._slots.values() if slot.episode is not None
            )
        return {
            "schema": EPISODE_SCHEMA,
            "domain_id": "webdev",
            "task_count": len(dataset),
            "parquet_path": self.parquet_path,
            "max_steps": self.max_steps,
            "max_policy_steps": self.max_steps,
            "max_policy_steps_enforced_by": "shared_policy_runner",
            "prompt_policy_turns": self.prompt_policy_turns,
            "configured_max_policy_turns": self.prompt_policy_turns,
            "max_observation_bytes": self.max_observation_bytes,
            "reward_contract": REWARD_CONTRACT,
            "reward_judge": os.environ.get("WD_JUDGE_MODEL", "kimi-k2.6"),
            "reward_rubric": "rva1:mean(visual,query,asset)",
            "compaction_contract": COMPACTION_CONTRACT,
            "memory_contract": COMPACTION_CONTRACT,
            "tool_contract": "mimoagent_registry_v1",
            "tool_serialization": "qwen35_native_single_function_v1",
            "context_contract": "webdev_task_plus_tool_surface_v1",
            "invalid_action_reward": INVALID_ACTION_REWARD,
            "invalid_action_terminal": False,
            "horizon_failure_reward": HORIZON_FAILURE_REWARD,
            "no_submission_penalty": NO_SUBMISSION_PENALTY,
            "finish_tool": FINISH_TOOL,
        }

    def _close_episode(self, slot: _Slot, *, close_reason: str) -> None:
        if slot.episode is None:
            return
        episode = slot.episode
        if episode.bridge is not None:
            episode.bridge.close()
        episode.evidence.append(
            {"event": "episode_closed", "reason": close_reason}
        )
        slot.episode = None

    def _initial_observation(
        self, record: dict[str, Any], bridge: WebdevBridge
    ) -> str:
        parts = [
            "== Task ==",
            record["task_text"],
            "",
            "== Delivery ==",
            "Your working directory is /workspace. Build the website the "
            "task asks for and deliver it under dist/ — opening "
            "dist/index.html in a browser must show the finished site, with "
            "every asset it needs under dist/ alongside it. The Bash "
            "tool already runs from the working directory, so use "
            "workspace-relative paths there.",
            "",
            "== Tool surface ==",
            bridge.render_tool_surface(),
            "",
            f"When the site is delivered, call the '{FINISH_TOOL}' tool with "
            "an optional 'answer' parameter. The episode is graded once, at "
            "finish, on the delivered page. You have "
            f"{self.prompt_policy_turns} turns in total; every response "
            "spends exactly one turn, however many tool calls it carries.",
        ]
        return self._truncate("\n".join(parts))

    def _parser_error_observation(self, action) -> str:
        return (
            "Invalid action (not penalized beyond a small fixed penalty; the "
            "episode continues). Reason: "
            f"{action.error}. Emit at least one complete Qwen XML envelope; "
            "when several independent calls are useful together, emit them as "
            "consecutive envelopes in the same response. Plain prose before "
            "the first envelope is allowed, but nothing may follow the last "
            "one."
        )

    def _format_tool_result(self, result: Any) -> str:
        if result is None:
            return "(tool returned no output)"
        if isinstance(result, Mapping):
            output = result.get("output")
            if isinstance(output, str):
                text = output
                if not result.get("success", True):
                    text += "\n(tool reported failure)"
                return self._truncate(text)
        if isinstance(result, str):
            text = result
        else:
            try:
                text = json.dumps(result, ensure_ascii=False, indent=2)
            except (TypeError, ValueError):
                text = str(result)
        return self._truncate(text)

    def _truncate(self, text: str) -> str:
        if PREVIEW_MARKER_RE.search(text) is None:
            if len(text.encode("utf-8")) <= self.max_observation_bytes:
                return text
            keep = self.max_observation_bytes
            while keep > 0 and len(text[:keep].encode("utf-8")) > self.max_observation_bytes:
                keep -= 256
            return (
                text[:keep]
                + "\n...[output truncated to fit the observation budget]..."
            )

        body, images = split_preview_markers(text)
        marker_tail = "".join(
            PREVIEW_MARKER_BEGIN + uri + PREVIEW_MARKER_END for uri in images
        )
        if len(body.encode("utf-8")) > self.max_observation_bytes:
            keep = self.max_observation_bytes
            while keep > 0 and len(body[:keep].encode("utf-8")) > self.max_observation_bytes:
                keep -= 256
            body = (
                body[:keep]
                + "\n...[output truncated to fit the observation budget]..."
            )
        return body + marker_tail

    def _persist_grading_extra(
        self,
        episode: Any,
        reward: float,
        grading_output: str,
        extra: Mapping[str, Any] | None,
    ) -> None:

        try:
            dims_dir = os.environ.get("WEBDEV_DIMS_DIR", DEFAULT_DIMS_DIR)
            os.makedirs(dims_dir, exist_ok=True)
            payload = {
                "schema": "webdev_grading_dims_v1",
                "instance_id": getattr(episode, "instance_id", None),
                "episode_id": getattr(episode, "episode_id", None),
                "step_count": getattr(episode, "step_count", None),
                "terminal_reason": getattr(episode, "terminal_reason", None),
                "reward": reward,
                "grading_output_head": grading_output[:2000],
                "grading_extra": {
                    k: v
                    for k, v in (extra or {}).items()
                    if isinstance(v, (str, int, float, bool, dict))
                },
                "ts": datetime.now(timezone.utc).isoformat(),
            }
            fname = (
                f"{payload.get('instance_id') or 'inst'}"
                f"-{uuid.uuid4().hex[:8]}.json"
            )
            with open(
                os.path.join(dims_dir, fname), "w", encoding="utf-8"
            ) as handle:
                json.dump(payload, handle, ensure_ascii=False, indent=1)
        except Exception:
            logger.warning("webdev dims persistence failed", exc_info=True)

    def _build_wrapper_evidence(
        self, episode: _Episode, *, action: Any
    ) -> dict[str, Any]:

        bridge = episode.bridge
        if bridge is None:
            return {}
        evidence: dict[str, Any] = {}
        checkpoint_after = bridge.checkpoint_state()
        checkpoint_receipt = self._checkpoint_receipt(
            episode, checkpoint_after
        )
        episode.checkpoint_before = checkpoint_after
        if checkpoint_receipt is not None:
            evidence["filesystem_checkpoint"] = checkpoint_receipt

        read_receipt = self._checkpoint_read_receipt(
            episode, action, checkpoint_after
        )
        if read_receipt is not None:
            evidence["filesystem_checkpoint_read"] = read_receipt
        changed_paths = bridge.workspace_changes_since_marker()
        bridge.touch_step_marker()
        if changed_paths:
            evidence["workspace_changed_paths"] = changed_paths
        return evidence

    def _checkpoint_receipt(
        self,
        episode: _Episode,
        checkpoint_after: dict[str, Any] | None,
    ) -> dict[str, Any] | None:

        before = episode.checkpoint_before
        exists = checkpoint_after is not None
        size = checkpoint_after.get("size_bytes") if exists else None
        sha = checkpoint_after.get("sha256") if exists else None
        changed = bool(
            exists
            and before is not None
            and (
                before.get("sha256") != sha
                or before.get("size_bytes") != size
            )
        )
        added = bool(exists and before is None)
        content_changed = bool(changed or added)
        return {
            "schema": "agentmemory_filesystem_checkpoint_receipt_v2",
            "path": ".agent_memory/CONTINUATION.md",
            "action_kind": "bash",
            "action_completed": True,
            "changed": content_changed,
            "idempotent_overwrite": False,
            "write_observed": content_changed,
            "exists": exists,
            "regular_file": exists,
            "size_bytes": size,
            "sha256": sha,
        }

    def _checkpoint_read_receipt(
        self,
        episode: _Episode,
        action: Any,
        checkpoint_after: dict[str, Any] | None,
    ) -> dict[str, Any] | None:
        if checkpoint_after is None:
            return None
        bridge = episode.bridge
        if bridge is None:
            return None
        action_text = getattr(action, "raw_output", "") or ""
        if "CONTINUATION" not in action_text:
            return None
        content = bridge.checkpoint_content()
        if content is None:
            return None
        raw_output = episode.raw_tool_output
        exact_read = bool(
            content.strip()
            and raw_output.strip()
            and content.strip() == raw_output.strip()
        )
        if exact_read:
            return {
                "schema": "agentmemory_filesystem_checkpoint_read_receipt_v1",
                "path": ".agent_memory/CONTINUATION.md",
                "observed": True,
                "size_bytes": checkpoint_after.get("size_bytes"),
                "sha256": checkpoint_after.get("sha256"),
            }
        return None

    def _public_step(
        self,
        episode: _Episode,
        *,
        action_kind: str,
        wrapper_evidence: dict[str, Any] | None = None,
    ) -> EpisodeStep:
        info: dict[str, Any] = {
            "schema": EPISODE_SCHEMA,
            "step": episode.step_count,
            "action_kind": action_kind,
            "terminal": episode.done,
            "episode_success": bool(
                episode.done and episode.grade is not None and episode.grade > 0
            ),
            "terminal_reason": episode.terminal_reason,
        }
        if wrapper_evidence:
            wrapper = dict(wrapper_evidence)
            tool_ok = action_kind == "tool_call"
            wrapper.setdefault("workspace_action_completed", tool_ok)
            if action_kind == "tool_call":
                wrapper.setdefault(
                    "workspace_op", "BASH"
                )
            info["wrapper_evidence"] = wrapper
        return EpisodeStep(
            observation=episode.observation,
            reward=episode.reward,
            done=episode.done,
            info=info,
        )
