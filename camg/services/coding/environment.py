from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import stat
import threading
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Mapping, Protocol

from .actions import (
    UPSTREAM_SUBMISSION_SENTINEL,
    ParsedPolicyAction,
    parse_policy_action,
)
from .audit import SwesmithEpisodeAuditSink
from .dataset import SwesmithDataset, SwesmithRecord
from .grader import SwesmithGradeResult, SwesmithHiddenGrader
from .profile import SwesmithProfileBinding
from .sandbox import (
    LinuxNamespaceEpisodeSandbox,
    SwesmithSandboxError,
    WorkspaceTreeSnapshot,
    diff_workspace_trees,
    snapshot_workspace_tree,
)
from .workspace import (
    SwesmithWorkspace,
    SwesmithWorkspaceMaterializer,
    _remove_episode_tree,
)

logger = logging.getLogger(__name__)

EPISODE_SCHEMA = "agentmemory_swesmith_native_episode_v1"
DEFAULT_TRAINING_MAX_POLICY_TURNS = 75
UPSTREAM_REFERENCE_MAX_POLICY_TURNS = 250
UPSTREAM_AGENT_REPOSITORY = "SWE-agent/mini-swe-agent"
UPSTREAM_AGENT_REVISION = "a83fcae82d2a08f0ee0c688f9d137b3566c097f8"
INVALID_ACTION_REWARD = -0.01
FAILED_SUBMISSION_REWARD = 0.0
HORIZON_FAILURE_REWARD = -0.01

CLEAN_SUBMISSION_FLOOR_REWARD = 0.1
FIRST_SOURCE_EDIT_MILESTONE_REWARD = 0.05
FIRST_TEST_RUN_MILESTONE_REWARD = 0.05
REWARD_CONTRACT = "submission_success1_cleanfloor0p1_edit_test_milestones0p05_v3"
SUBMISSION_CONTRACT = "upstream_shell_output_sentinel_source_change_required_v2"
HORIZON_CONTRACT = "unified_policy_step_terminal_failure_minus0p01_v3"

DEFAULT_MAX_OBSERVATION_BYTES = 8192
GENERATED_PATH_PARTS = frozenset(
    {
        ".agent_memory",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        ".tox",
        ".nox",
    }
)
GENERATED_FILE_NAMES = frozenset({".coverage", "coverage.xml"})
ACTOR_CREDIT_SCHEMA = "task_neutral_actor_credit_v1"
ACTION_PROGRESS_SCHEMA = "swesmith_action_progress_v1"
MAX_VISIBLE_CHANGED_PATHS_BYTES = 1024
FILESYSTEM_CHECKPOINT_RECEIPT_SCHEMA = (
    "agentmemory_filesystem_checkpoint_receipt_v1"
)
FILESYSTEM_CHECKPOINT_READ_RECEIPT_SCHEMA = (
    "agentmemory_filesystem_checkpoint_read_receipt_v1"
)
FILESYSTEM_CHECKPOINT_PATH = ".agent_memory/CONTINUATION.md"
FILESYSTEM_CHECKPOINT_MAX_BYTES = 8 * 1024

class ProfileResolver(Protocol):
    def resolve(self, instance: Mapping[str, Any]) -> SwesmithProfileBinding: ...

class SandboxFactory(Protocol):
    def __call__(
        self,
        record: SwesmithRecord,
        profile: SwesmithProfileBinding,
    ) -> LinuxNamespaceEpisodeSandbox: ...

@dataclass(frozen=True)
class EpisodeStep:
    observation: str
    reward: float
    done: bool
    info: Mapping[str, Any]

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
    record: SwesmithRecord
    profile: SwesmithProfileBinding
    workspace: SwesmithWorkspace
    sandbox: LinuxNamespaceEpisodeSandbox
    initial_snapshot: WorkspaceTreeSnapshot
    observation: str
    initial_observation: str
    step_count: int = 0

    last_active: float = field(default_factory=time.monotonic)
    done: bool = False
    reward: float = 0.0
    evidence: list[dict[str, Any]] = field(default_factory=list)
    grade: SwesmithGradeResult | None = None
    sample_excluded: bool = False
    sample_exclusion_reason: str | None = None

    first_source_edit_milestone_awarded: bool = False
    first_test_run_milestone_awarded: bool = False

@dataclass
class _Slot:
    episode: _Episode | None = None
    lock: threading.Lock = field(default_factory=threading.Lock)

def _actor_credit(positive_eligible: bool, basis: str) -> dict[str, Any]:
    return {
        "schema": ACTOR_CREDIT_SCHEMA,
        "positive_eligible": positive_eligible,
        "basis": basis,
    }

def _stable_json_sha256(value: Mapping[str, Any]) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()

def _shell_action_progress(
    action: ParsedPolicyAction,
    *,
    result: Mapping[str, Any],
) -> dict[str, Any]:
    workspace_diff = result.get("workspace_diff")
    if not isinstance(workspace_diff, Mapping):
        raise RuntimeError("SWE-smith shell result lost its workspace diff")
    action_payload = {
        "kind": action.kind,
        "arguments": dict(action.arguments or {}),
    }
    result_payload = {
        key: result.get(key)
        for key in (
            "exit_code",
            "timed_out",
            "stdout",
            "stderr",
            "stdout_truncated",
            "stderr_truncated",
            "termination_reason",
        )
    }
    result_payload.update(
        {
            "before_tree_sha256": workspace_diff.get("before_tree_sha256"),
            "after_tree_sha256": workspace_diff.get("after_tree_sha256"),
        }
    )
    return {
        "schema": ACTION_PROGRESS_SCHEMA,
        "action_fingerprint": _stable_json_sha256(action_payload),
        "result_fingerprint": _stable_json_sha256(result_payload),
        "workspace_changed": bool(workspace_diff.get("changed_paths")),
    }

class SwesmithEpisodeManager:

    def __init__(
        self,
        *,
        dataset: SwesmithDataset,
        materializer: SwesmithWorkspaceMaterializer,
        profile_resolver: ProfileResolver,
        sandbox_factory: SandboxFactory,
        grader: SwesmithHiddenGrader,
        audit_sink: SwesmithEpisodeAuditSink | None = None,
        max_steps: int = DEFAULT_TRAINING_MAX_POLICY_TURNS,
        max_observation_bytes: int = DEFAULT_MAX_OBSERVATION_BYTES,
        runtime_metadata: Mapping[str, Any] | None = None,
        prompt_policy_turns: int | None = None,
    ) -> None:
        if type(max_steps) is not int or max_steps <= 0:
            raise ValueError("SWE-smith max_steps must be a positive integer")
        if prompt_policy_turns is None:
            prompt_policy_turns = max_steps
        if type(prompt_policy_turns) is not int or prompt_policy_turns <= 0:
            raise ValueError(
                "SWE-smith prompt_policy_turns must be a positive integer"
            )
        if type(max_observation_bytes) is not int or max_observation_bytes <= 0:
            raise ValueError(
                "SWE-smith max_observation_bytes must be a positive integer"
            )
        self.dataset = dataset
        self.materializer = materializer
        self.profile_resolver = profile_resolver
        self.sandbox_factory = sandbox_factory
        self.grader = grader
        self.audit_sink = audit_sink
        self.max_steps = max_steps

        self.prompt_policy_turns = prompt_policy_turns
        self.max_observation_bytes = max_observation_bytes
        self.runtime_metadata = dict(runtime_metadata or {})
        self._slots: dict[int, _Slot] = {}
        self._next_slot = 0
        self._slots_lock = threading.Lock()
        self._reaper_lock = threading.Lock()
        self._reaper_started = False

    def create(self) -> int:
        with self._slots_lock:
            slot_id = self._next_slot
            self._next_slot += 1
            self._slots[slot_id] = _Slot()
        return slot_id

    def reset(self, slot_id: int, data_idx: int) -> EpisodeStep:
        slot = self._slot(slot_id)
        with slot.lock:
            self._close_episode(slot, close_reason="reset")
            record = self.dataset[data_idx]
            profile = self.profile_resolver.resolve(record.instance)
            sandbox: LinuxNamespaceEpisodeSandbox | None = None
            workspace: SwesmithWorkspace | None = None
            try:
                sandbox = self.sandbox_factory(record, profile)
                workspace = self.materializer.materialize(
                    record.instance,
                    test_paths=profile.all_test_paths,
                    model_uid=sandbox.model_uid,
                    model_gid=sandbox.model_gid,
                )
                initial_snapshot = sandbox.attach_workspace(workspace.policy_root)
                observation = _initial_observation(
                    record.problem_statement,
                    max_policy_turns=self.prompt_policy_turns,
                )
                episode = _Episode(
                    slot_id=slot_id,
                    audit_id=uuid.uuid4().hex,
                    started_at=_utc_now(),
                    record=record,
                    profile=profile,
                    workspace=workspace,
                    sandbox=sandbox,
                    initial_snapshot=initial_snapshot,
                    observation=observation,
                    initial_observation=observation,
                )
                episode.evidence.append(
                    {
                        "event": "reset",
                        "slot_id": slot_id,
                        "audit_id": episode.audit_id,
                        "data_idx": record.data_idx,
                        "physical_index": record.physical_index,
                        "instance_id": record.instance_id,
                        "dataset_shard_sha256": record.shard_sha256,
                        "profile": profile.as_private_metadata(),
                        "workspace_contract": workspace.contract,
                        "workspace_initial": initial_snapshot.as_summary(),
                        "sandbox": dict(sandbox.metadata),
                        "observation": observation,
                    }
                )
                slot.episode = episode
                return self._public_step(episode, action_kind="reset")
            except Exception:
                try:
                    if workspace is not None:
                        self.materializer.close(workspace)
                except Exception:  
                    logger.exception(
                        "SWE-smith reset: workspace cleanup failed"
                    )
                try:
                    if sandbox is not None:
                        sandbox.close()
                except Exception:  
                    logger.exception(
                        "SWE-smith reset: sandbox cleanup failed"
                    )
                raise

    def step(self, slot_id: int, raw_output: str) -> EpisodeStep:
        slot = self._slot(slot_id)
        with slot.lock:
            episode = self._episode(slot)
            if episode.done:
                raise RuntimeError("SWE-smith episode is already terminal")
            episode.last_active = time.monotonic()
            episode.step_count += 1

            episode.reward = 0.0
            observation_before = episode.observation
            action = parse_policy_action(raw_output)
            evidence: dict[str, Any] = {
                "event": "policy_step",
                "step": episode.step_count,
                "observation_before": observation_before,
                "action": action.as_evidence(),
            }
            public_action_kind = action.kind
            completed_any = False
            if action.kind == "parser_error":
                episode.observation = _parser_error_observation(
                    action,
                    turn_count=episode.step_count,
                    max_policy_turns=self.prompt_policy_turns,
                )
                evidence["result"] = {"parser_error": action.error}
                episode.reward = INVALID_ACTION_REWARD
                actor_credit = _actor_credit(False, "parser_rejected")
            elif action.kind == "bash":
                sub_actions = list(action.calls) if action.calls else [action]
                sub_total = len(sub_actions)
                obs_parts: list[str] = []
                for call_index, sub_action in enumerate(sub_actions, start=1):
                    actor_credit = self._run_shell(episode, sub_action, evidence)
                    if _action_completed_for_checkpoint(
                        "bash", actor_credit, evidence.get("result")
                    ):
                        completed_any = True
                    if actor_credit["basis"] == "terminal_submission":
                        public_action_kind = "final"
                    if sub_total > 1:
                        obs_parts.append(
                            f"[call {call_index}/{sub_total}]\n{episode.observation}"
                        )
                    if episode.done:
                        break
                if sub_total > 1 and obs_parts:
                    episode.observation = "\n\n".join(obs_parts)
            else:  
                raise RuntimeError(f"unsupported SWE-smith action kind: {action.kind}")
            evidence["actor_credit"] = dict(actor_credit)
            evidence["observation_after"] = episode.observation
            episode.evidence.append(evidence)

            if not episode.done and episode.step_count >= self.max_steps:
                horizon: dict[str, Any] = {
                    "event": "horizon_exhaustion",
                    "step": episode.step_count,
                    "observation_before": episode.observation,
                    "action": {"kind": "horizon"},
                }
                self._terminate_policy_failure(
                    episode,
                    horizon,
                    termination_reason="max_steps",
                    reward=HORIZON_FAILURE_REWARD,
                )
                horizon["observation_after"] = episode.observation
                episode.evidence.append(horizon)
            action_result = evidence.get("result")
            if action.kind == "bash":

                action_completed = completed_any
            else:
                action_completed = _action_completed_for_checkpoint(
                    action.kind, actor_credit, action_result
                )
            checkpoint_receipt = _filesystem_checkpoint_receipt(
                episode.workspace.policy_root,
                action_kind=action.kind,
                action_completed=action_completed,
                workspace_diff=(
                    action_result.get("workspace_diff")
                    if isinstance(action_result, Mapping)
                    else None
                ),
            )
            checkpoint_read_receipt = _filesystem_checkpoint_read_receipt(
                checkpoint_receipt,
                action_kind=action.kind,
                action_completed=action_completed,
                result=action_result,
            )
            if (
                checkpoint_read_receipt["observed"]
                and isinstance(action_result, Mapping)
                and isinstance(action_result.get("stdout"), str)
            ):

                episode.observation = action_result["stdout"]
                separator = (
                    "" if episode.observation.endswith("\n") else "\n"
                )
                episode.observation += separator + _swe_turn_budget_footnote(
                    episode.step_count, self.prompt_policy_turns
                )
                evidence["observation_after"] = episode.observation
            workspace_changed_paths: tuple[str, ...] = ()
            if isinstance(action_result, Mapping):
                workspace_diff = action_result.get("workspace_diff")
                if isinstance(workspace_diff, Mapping):
                    raw_changed_paths = workspace_diff.get("changed_paths")
                    if isinstance(raw_changed_paths, (list, tuple)):
                        workspace_changed_paths = tuple(
                            sorted(
                                {
                                    str(path)
                                    for path in raw_changed_paths
                                    if isinstance(path, str) and path
                                }
                            )
                        )
            return self._public_step(
                episode,
                action_kind=public_action_kind,
                actor_credit=actor_credit,
                action_progress=evidence.get("action_progress"),
                filesystem_checkpoint=checkpoint_receipt,
                filesystem_checkpoint_read=checkpoint_read_receipt,
                workspace_changed_paths=workspace_changed_paths,
                shell_action_succeeded=bool(
                    action.kind == "bash" and action_completed
                ),
            )

    def observation(self, slot_id: int) -> str:
        slot = self._slot(slot_id)
        with slot.lock:
            episode = self._episode(slot)
            episode.last_active = time.monotonic()
            return episode.observation

    def finalize_horizon(self, slot_id: int) -> EpisodeStep:

        slot = self._slot(slot_id)
        with slot.lock:
            episode = self._episode(slot)
            if episode.done:
                raise RuntimeError("SWE-smith episode is already terminal")
            episode.last_active = time.monotonic()
            horizon: dict[str, Any] = {
                "event": "horizon_exhaustion",
                "step": episode.step_count,
                "observation_before": episode.observation,
                "action": {"kind": "policy_turn_horizon"},
            }
            self._terminate_policy_failure(
                episode,
                horizon,
                termination_reason="policy_turn_horizon",
                reward=HORIZON_FAILURE_REWARD,
            )
            horizon["observation_after"] = episode.observation
            episode.evidence.append(horizon)
            return self._public_step(episode, action_kind="policy_turn_horizon")

    def detail(self, slot_id: int) -> dict[str, Any]:
        slot = self._slot(slot_id)
        with slot.lock:
            episode = self._episode(slot)
            return {
                "schema": EPISODE_SCHEMA,
                "slot_id": episode.slot_id,
                "audit_id": episode.audit_id,
                "started_at": episode.started_at,
                "data_idx": episode.record.data_idx,
                "physical_index": episode.record.physical_index,
                "instance_id": episode.record.instance_id,
                "step_count": episode.step_count,
                "done": episode.done,
                "reward": episode.reward,
                "sample_excluded": episode.sample_excluded,
                "sample_exclusion_reason": episode.sample_exclusion_reason,
                "workspace": {
                    "episode_root": str(episode.workspace.episode_root),
                    "policy_root": str(episode.workspace.policy_root),
                    "model_uid": episode.sandbox.model_uid,
                    "model_gid": episode.sandbox.model_gid,
                },
                "evidence": list(episode.evidence),
                "grade": (
                    None if episode.grade is None else episode.grade.as_private_dict()
                ),
            }

    def close(self, slot_id: int) -> dict[str, Any]:
        slot = self._slot(slot_id)
        with slot.lock:
            close_report = self._close_episode(slot, close_reason="client_close")
        with self._slots_lock:
            self._slots.pop(slot_id, None)
        return {"closed": True, "id": slot_id, "close_report": close_report}

    def metadata(self) -> dict[str, Any]:
        provenance = self.dataset.provenance
        slot_count, active_count = self._active_counts()
        metadata = {
            "schema": EPISODE_SCHEMA,
            "task_count": len(self.dataset),
            "dataset_id": provenance.dataset_id,
            "dataset_role": provenance.role,
            "upstream_repository": provenance.upstream_repository,
            "dataset_revision": provenance.upstream_revision,
            
            "upstream_revision": provenance.upstream_revision,
            "dataset_manifest_sha256": provenance.manifest_sha256,
            "selection_mode": provenance.selection_mode,
            "max_steps": self.max_steps,
            "configured_max_policy_turns": self.max_steps,
            "prompt_policy_turns": self.prompt_policy_turns,
            "training_max_policy_turns": DEFAULT_TRAINING_MAX_POLICY_TURNS,
            "upstream_reference_max_policy_turns": (
                UPSTREAM_REFERENCE_MAX_POLICY_TURNS
            ),
            "upstream_agent_repository": UPSTREAM_AGENT_REPOSITORY,
            "upstream_agent_revision": UPSTREAM_AGENT_REVISION,
            "tool_contract": "codex_bash_only_v2",
            "tool_serialization": "qwen35_native_single_function_v1",
            "observation_contract": "bounded_combined_shell_output_v1",
            "max_observation_bytes": self.max_observation_bytes,
            "reward_contract": REWARD_CONTRACT,
            "context_contract": "one_native_issue_continuous_episode_v1",
            "memory_contract": (
                "policy_filesystem_checkpoint_then_client_replace_v3"
            ),
            "submission_contract": SUBMISSION_CONTRACT,
            "horizon_contract": HORIZON_CONTRACT,
            "invalid_action_reward": INVALID_ACTION_REWARD,
            "invalid_action_terminal": False,
            "failed_submission_reward": FAILED_SUBMISSION_REWARD,
            "horizon_failure_reward": HORIZON_FAILURE_REWARD,

            "clean_submission_floor_reward": CLEAN_SUBMISSION_FLOOR_REWARD,
            "first_source_edit_milestone_reward": (
                FIRST_SOURCE_EDIT_MILESTONE_REWARD
            ),
            "first_test_run_milestone_reward": (
                FIRST_TEST_RUN_MILESTONE_REWARD
            ),
            "milestone_rewards_nonterminal": True,
            "penalized_nonterminal_conditions": [
                "parser_rejected",
                "executor_rejected",
            ],
            "penalized_terminal_conditions": [
                "max_steps",
                "policy_turn_horizon",
            ],
            "zero_reward_submission_conditions": [
                "submission_without_source_change",

                "test_infra_tampering",
                "runner_tampering",
                "workspace_integrity_violation",
            ],

            "clean_floor_submission_conditions": [
                "grader_unresolved",
            ],
            "valid_shell_nonzero_exit_is_terminal": False,
            "grader_infrastructure_failure": "sample_excluded",
            "grader_execution_contract": "single_full_official_command_v1",
            "grader_phase_count": 1,
            "grader_timeout_ms": self.grader.timeout_ms,
            "active_slot_count": slot_count,
            "active_environment_count": active_count,
            "active_workspace_count": active_count,
            "private_audit_contract": (
                "agentmemory_swesmith_private_episode_audit_v1"
                if self.audit_sink is not None
                else "disabled"
            ),
        }
        metadata.update(self.runtime_metadata)
        return metadata

    def _active_counts(self) -> tuple[int, int]:
        with self._slots_lock:
            slots = list(self._slots.values())
        active_count = 0
        for slot in slots:
            with slot.lock:
                active_count += int(slot.episode is not None)
        return len(slots), active_count

    def _run_shell(
        self,
        episode: _Episode,
        action: ParsedPolicyAction,
        evidence: dict[str, Any],
    ) -> Mapping[str, Any]:
        assert action.arguments is not None
        timeout_ms = action.arguments.get(
            "timeout_ms", episode.sandbox.limits.default_timeout_ms
        )
        try:
            execution = episode.sandbox.run(
                command=str(action.arguments["command"]),
                workdir=str(action.arguments["workdir"]),
                timeout_ms=int(timeout_ms),
            )
        except SwesmithSandboxError as exc:
            poisoned = episode.sandbox.poisoned_reason
            evidence["result"] = {
                "error": f"{type(exc).__name__}: {exc}",
                "poisoned": poisoned,
            }
            if poisoned is not None:
                if episode.sandbox.poisoned_by_policy_command:

                    evidence["workspace_integrity_violation"] = {
                        "poisoned_reason": poisoned,
                        "provenance": "policy_command_window",
                    }
                    self._terminate_policy_failure(
                        episode,
                        evidence,
                        termination_reason="workspace_integrity_violation",
                        reward=FAILED_SUBMISSION_REWARD,
                        observation=(
                            "Shell command ended the episode: the workspace "
                            "now contains an entry the sandbox rejects "
                            "(socket, device, FIFO, hard link, or setuid/"
                            "setgid bit). The submission was not graded."
                        ),
                    )
                    return _actor_credit(False, "workspace_integrity_violation")

                episode.reward = 0.0
                episode.done = True
                episode.sample_excluded = True
                episode.sample_exclusion_reason = (
                    "sandbox_poisoned_out_of_band_modification"
                )
                episode.observation = (
                    "Workspace changed outside the attested episode action "
                    "path; episode excluded."
                )
                return _actor_credit(False, "environment_excluded")
            episode.observation = f"bash failed: {exc}"
            episode.reward = INVALID_ACTION_REWARD
            return _actor_credit(False, "executor_rejected")
        result = execution.result
        stdout = result.stdout.decode("utf-8", errors="replace")
        stderr = result.stderr.decode("utf-8", errors="replace")
        evidence["result"] = {
            "exit_code": result.exit_code,
            "elapsed_ms": result.elapsed_ms,
            "timed_out": result.timed_out,
            "stdout": stdout,
            "stderr": stderr,
            "stdout_truncated": result.stdout_truncated,
            "stderr_truncated": result.stderr_truncated,
            "observation_output_budget_bytes": self.max_observation_bytes,
            "observation_output_truncated": bool(
                result.stdout_truncated or result.stderr_truncated
            ),
            "termination_reason": result.termination_reason,
            "workspace_diff": execution.workspace_diff.as_dict(),
        }
        evidence["action_progress"] = _shell_action_progress(
            action,
            result=evidence["result"],
        )
        episode.observation = _shell_observation(
            exit_code=result.exit_code,
            elapsed_ms=result.elapsed_ms,
            timed_out=result.timed_out,
            stdout=stdout,
            stderr=stderr,
            stdout_truncated=result.stdout_truncated,
            stderr_truncated=result.stderr_truncated,
            changed_paths=execution.workspace_diff.changed_paths,
            max_observation_bytes=self.max_observation_bytes,
            turn_count=episode.step_count,
            max_policy_turns=self.prompt_policy_turns,
        )
        submission = _submission_from_shell_result(
            stdout=stdout,
            exit_code=result.exit_code,
            timed_out=result.timed_out,
        )
        if submission is not None:
            final_diff = diff_workspace_trees(
                episode.initial_snapshot,
                execution.workspace_after,
            )
            source_changed_paths = _meaningful_changed_paths(final_diff.changed_paths)
            evidence["submission"] = {
                "sentinel": UPSTREAM_SUBMISSION_SENTINEL,
                "output_bytes": len(submission.encode("utf-8")),
                "output_sha256": hashlib.sha256(
                    submission.encode("utf-8")
                ).hexdigest(),
                "workspace_diff_from_reset": final_diff.as_dict(),
                "source_changed_paths": list(source_changed_paths),
            }
            infra_violations = _test_infra_violation_paths(
                final_diff.changed_paths, episode.profile
            )
            runner_patch_violations = _runner_patch_violations(
                source_changed_paths,
                episode.profile,
                episode.workspace.policy_root,
            )
            if infra_violations or runner_patch_violations:

                if infra_violations:
                    evidence["test_infra_tampering"] = {
                        "violations": list(infra_violations),
                    }
                if runner_patch_violations:
                    evidence["runner_patch_tampering"] = [
                        dict(violation) for violation in runner_patch_violations
                    ]
                self._terminate_policy_failure(
                    episode,
                    evidence,
                    termination_reason="test_infra_tampering",
                    reward=FAILED_SUBMISSION_REWARD,
                    observation=(
                        "Submission ended the episode: the workspace changed "
                        "files that control how the hidden tests run "
                        "(conftest/pytest configuration), so the change "
                        "was not graded."
                    ),
                )
            elif not source_changed_paths:
                self._terminate_policy_failure(
                    episode,
                    evidence,
                    termination_reason="submission_without_source_change",
                    reward=FAILED_SUBMISSION_REWARD,
                    observation=(
                        "Submission ended the episode without a source change. "
                        "The workspace was not graded."
                    ),
                )
            else:
                self._grade_terminal(
                    episode,
                    evidence,
                    termination_reason="submission_sentinel",
                )
            return _actor_credit(True, "terminal_submission")

        milestones: dict[str, Any] = {}
        if not episode.first_source_edit_milestone_awarded:
            meaningful_now = _meaningful_changed_paths(
                execution.workspace_diff.changed_paths
            )
            if meaningful_now:
                episode.first_source_edit_milestone_awarded = True
                episode.reward += FIRST_SOURCE_EDIT_MILESTONE_REWARD
                milestones["first_source_edit"] = {
                    "reward": FIRST_SOURCE_EDIT_MILESTONE_REWARD,
                    "changed_paths": list(meaningful_now),
                }
        if not episode.first_test_run_milestone_awarded:
            if _is_test_run_command(str(action.arguments["command"])):
                episode.first_test_run_milestone_awarded = True
                episode.reward += FIRST_TEST_RUN_MILESTONE_REWARD
                milestones["first_test_run"] = {
                    "reward": FIRST_TEST_RUN_MILESTONE_REWARD,
                    "command": str(action.arguments["command"]),
                }
        if milestones:
            evidence["milestones"] = milestones
        return _actor_credit(True, "shell_executed")

    def _grade_terminal(
        self,
        episode: _Episode,
        evidence: dict[str, Any],
        *,
        termination_reason: str,
    ) -> None:
        grade = self.grader.grade(
            instance=episode.record.instance,
            profile=episode.profile,
            workspace=episode.workspace,
            sandbox=episode.sandbox,
        )
        episode.grade = grade
        evidence["termination_reason"] = termination_reason
        evidence["terminal_grade"] = {
            "native_reward": grade.reward,
            "resolved": grade.resolved,
            "grader_error": grade.error,
        }
        episode.done = True
        if grade.runner_tampering is not None:

            evidence["termination_reason"] = "runner_tampering"
            evidence["runner_tampering"] = dict(grade.runner_tampering)
            evidence["terminal_grade"] = {
                "reward": FAILED_SUBMISSION_REWARD,
                "resolved": False,
                "grader_error": grade.error,
                "graded": False,
                "sample_excluded": False,
            }
            episode.reward = FAILED_SUBMISSION_REWARD
            episode.observation = (
                "Submission ended the episode: the grading runner detected "
                "that the test framework was tampered with, so the change "
                "was not graded."
            )
        elif grade.error is not None and grade.policy_caused:

            evidence["termination_reason"] = "workspace_integrity_violation"
            evidence["terminal_grade"] = {
                "reward": FAILED_SUBMISSION_REWARD,
                "resolved": False,
                "grader_error": grade.error,
                "graded": False,
                "sample_excluded": False,
                "policy_caused": True,
            }
            episode.reward = FAILED_SUBMISSION_REWARD
            episode.observation = (
                "Submission ended the episode: a hidden test path is "
                "blocked by a non-file entry in the workspace, so the "
                "tests could not be restored and the change was not "
                "graded."
            )
        elif grade.error is not None:
            episode.reward = 0.0
            episode.sample_excluded = True
            episode.sample_exclusion_reason = "grader_infrastructure_failure"
            episode.observation = (
                "Submission reached the grader, but infrastructure prevented a valid score."
            )
            evidence["terminal_grade"]["reward"] = 0.0
            evidence["terminal_grade"]["sample_excluded"] = True
        elif grade.resolved and grade.reward == 1.0:
            episode.reward = 1.0
            episode.observation = "Submission accepted and graded. The issue is resolved."
            evidence["terminal_grade"]["reward"] = 1.0
            evidence["terminal_grade"]["sample_excluded"] = False
        elif not grade.resolved and grade.reward == 0.0:

            episode.reward = CLEAN_SUBMISSION_FLOOR_REWARD
            episode.observation = (
                "Submission accepted and graded. The issue is not resolved."
            )
            evidence["termination_reason"] = "grader_unresolved"
            evidence["terminal_grade"]["reward"] = CLEAN_SUBMISSION_FLOOR_REWARD
            evidence["terminal_grade"]["sample_excluded"] = False
            evidence["terminal_grade"][
                "clean_submission_floor_reward"
            ] = CLEAN_SUBMISSION_FLOOR_REWARD
        else:
            episode.reward = 0.0
            episode.sample_excluded = True
            episode.sample_exclusion_reason = "unexpected_grader_contract"
            episode.observation = "Submission returned an unsupported grader result."
            evidence["termination_reason"] = "unexpected_grader_contract"
            evidence["terminal_grade"]["reward"] = 0.0
            evidence["terminal_grade"]["sample_excluded"] = True

    def _terminate_policy_failure(
        self,
        episode: _Episode,
        evidence: dict[str, Any],
        *,
        termination_reason: str,
        reward: float,
        observation: str | None = None,
    ) -> None:
        episode.done = True
        episode.reward = reward
        if observation is None:
            episode.observation = (
                "Episode ended without a successful official submission."
            )
        else:
            episode.observation = observation
        evidence["termination_reason"] = termination_reason
        evidence["terminal_grade"] = {
            "reward": reward,
            "resolved": False,
            "grader_error": None,
            "graded": False,
            "sample_excluded": False,
        }

    def _public_step(
        self,
        episode: _Episode,
        *,
        action_kind: str,
        actor_credit: Mapping[str, Any] | None = None,
        action_progress: Mapping[str, Any] | None = None,
        filesystem_checkpoint: Mapping[str, Any] | None = None,
        filesystem_checkpoint_read: Mapping[str, Any] | None = None,
        workspace_changed_paths: tuple[str, ...] = (),
        shell_action_succeeded: bool = False,
    ) -> EpisodeStep:
        info: dict[str, Any] = {
            "schema": EPISODE_SCHEMA,
            "step": episode.step_count,
            "action_kind": action_kind,
            "terminal": episode.done,
            "sample_excluded": episode.sample_excluded,
            "sample_exclusion_reason": episode.sample_exclusion_reason,
            "episode_success": bool(
                episode.done
                and episode.grade is not None
                and episode.grade.resolved
            ),
        }
        if actor_credit is not None:
            info["actor_credit"] = dict(actor_credit)
        if action_progress is not None:
            info["action_progress"] = dict(action_progress)
        if filesystem_checkpoint is not None:
            info["filesystem_checkpoint"] = dict(filesystem_checkpoint)
        if filesystem_checkpoint_read is not None:
            info["filesystem_checkpoint_read"] = dict(filesystem_checkpoint_read)
        if workspace_changed_paths:
            info["workspace_changed_paths"] = list(workspace_changed_paths)
        if action_kind == "bash":
            info["shell_action_succeeded"] = bool(shell_action_succeeded)
        return EpisodeStep(
            observation=episode.observation,
            reward=episode.reward,
            done=episode.done,
            info=info,
        )

    def _slot(self, slot_id: int) -> _Slot:
        if isinstance(slot_id, bool) or not isinstance(slot_id, int):
            raise KeyError("SWE-smith slot id must be an integer")
        with self._slots_lock:
            try:
                return self._slots[slot_id]
            except KeyError as exc:
                raise KeyError(f"unknown SWE-smith slot id: {slot_id}") from exc

    @staticmethod
    def _episode(slot: _Slot) -> _Episode:
        if slot.episode is None:
            raise RuntimeError("SWE-smith slot must be reset before use")
        return slot.episode

    def _close_episode(
        self, slot: _Slot, *, close_reason: str
    ) -> dict[str, Any] | None:

        episode = slot.episode
        slot.episode = None
        if episode is None:
            return None
        close_report: dict[str, Any] = {
            "slot_id": episode.slot_id,
            "audit_id": episode.audit_id,
            "close_reason": close_reason,
            "audit_error": None,
            "sandbox_close_error": None,
            "workspace_close_error": None,
            "workspace_residue": False,
        }
        try:
            if self.audit_sink is not None:
                self.audit_sink.write(
                    audit_id=episode.audit_id,
                    payload={
                        "episode_schema": EPISODE_SCHEMA,
                        "closed_at": _utc_now(),
                        "close_reason": close_reason,
                        "slot_id": episode.slot_id,
                        "started_at": episode.started_at,
                        "data_idx": episode.record.data_idx,
                        "physical_index": episode.record.physical_index,
                        "instance_id": episode.record.instance_id,
                        "dataset_shard_sha256": episode.record.shard_sha256,
                        "problem_statement": episode.record.problem_statement,
                        "initial_observation": episode.initial_observation,
                        "step_count": episode.step_count,
                        "done": episode.done,
                        "reward": episode.reward,
                        "sample_excluded": episode.sample_excluded,
                        "sample_exclusion_reason": episode.sample_exclusion_reason,
                        "runtime_metadata": dict(self.runtime_metadata),
                        "evidence": list(episode.evidence),
                        "grade": (
                            None
                            if episode.grade is None
                            else episode.grade.as_private_dict()
                        ),
                    },
                )
        except Exception as exc:  
            close_report["audit_error"] = repr(exc)
            logger.exception(
                "SWE-smith close: audit write failed for slot %s", episode.slot_id
            )
        try:
            episode.sandbox.close()
        except Exception as exc:  
            close_report["sandbox_close_error"] = repr(exc)
            logger.exception(
                "SWE-smith close: sandbox close failed for slot %s", episode.slot_id
            )
        try:
            self.materializer.close(episode.workspace)
        except Exception as exc:  
            close_report["workspace_close_error"] = repr(exc)
            logger.exception(
                "SWE-smith close: workspace close failed for slot %s", episode.slot_id
            )
        try:
            workspace_residue = Path(episode.workspace.episode_root).exists()
        except OSError:
            workspace_residue = True
        if workspace_residue:
            close_report["workspace_residue"] = True
            logger.warning(
                "SWE-smith close: episode tree still present after close: %s",
                episode.workspace.episode_root,
            )
        return close_report

    def sweep_orphan_episodes(self) -> dict[str, Any]:

        report: dict[str, Any] = {
            "episodes_root": str(self.materializer.episodes_root),
            "swept": 0,
            "failed": [],
        }
        try:
            entries = sorted(self.materializer.episodes_root.iterdir())
        except OSError as exc:
            report["failed"].append({"path": "<root>", "error": repr(exc)})
            logger.warning(
                "swesmith boot sweep: cannot list episodes root: %r", exc
            )
            return report
        for entry in entries:
            if not entry.name.startswith("swesmith-episode-"):
                continue
            if entry.is_symlink() or not entry.is_dir():
                report["failed"].append(
                    {"path": entry.name, "error": "not a real episode directory"}
                )
                continue
            try:
                _remove_episode_tree(entry)
                report["swept"] += 1
            except Exception as exc:  
                report["failed"].append({"path": entry.name, "error": repr(exc)})
        if report["swept"] or report["failed"]:
            logger.info("swesmith boot sweep: %s", report)
        else:
            logger.info(
                "swesmith boot sweep: no residue in %s",
                report["episodes_root"],
            )
        return report

    def start_idle_reaper(self) -> None:
        raw_ttl = os.environ.get("SWESMITH_IDLE_TTL", "3600")
        try:
            ttl = float(raw_ttl)
        except ValueError:
            ttl = 3600.0
        if ttl <= 0:
            logger.info(
                "swesmith idle reaper disabled (SWESMITH_IDLE_TTL=%s)", raw_ttl
            )
            return
        with self._reaper_lock:
            if self._reaper_started:
                return
            self._reaper_started = True
            thread = threading.Thread(
                target=self._reaper_loop,
                args=(ttl,),
                name="swesmith-idle-reaper",
                daemon=True,
            )
            thread.start()
        logger.info("swesmith idle reaper started: ttl=%.0fs", ttl)

    def _reaper_loop(self, ttl: float) -> None:
        while True:
            time.sleep(60)
            self._reaper_pass(ttl)

    def _reaper_pass(self, ttl: float) -> None:
        try:
            now = time.monotonic()
            with self._slots_lock:
                candidates = sorted(self._slots.items())
            for slot_id, slot in candidates:
                with slot.lock:
                    episode = slot.episode
                    if episode is None:
                        continue
                    idle = now - episode.last_active
                    if idle <= ttl:
                        continue
                    logger.info(
                        "swesmith idle reaper closing slot %d "
                        "(idle %.0fs > ttl %.0fs)",
                        slot_id,
                        idle,
                        ttl,
                    )
                    self._close_episode(slot, close_reason="idle_reaper")
                    with self._slots_lock:
                        self._slots.pop(slot_id, None)
        except Exception:  
            logger.exception("swesmith idle reaper iteration failed")

def _action_completed_for_checkpoint(
    action_kind: str,
    actor_credit: Mapping[str, Any],
    result: Any,
) -> bool:
    if not isinstance(result, Mapping):
        return False
    if action_kind == "bash":
        exit_code = result.get("exit_code")
        return bool(
            actor_credit.get("basis") in {
                "shell_executed",
                "terminal_submission",
                "no_workspace_change",
                "zero_progress_repeat",
            }
            and isinstance(exit_code, int)
            and not isinstance(exit_code, bool)
            and exit_code == 0
            and result.get("timed_out") is False
        )
    return False

def _checkpoint_diff_entry_size(entry: Any) -> int | None:
    if not isinstance(entry, Mapping):
        return None
    value = entry.get("bytes", entry.get("size"))
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return None
    return value

def _explicit_regular_checkpoint_diff_entry(entry: Any) -> bool:
    if not isinstance(entry, Mapping) or entry.get("kind") != "file":
        return False
    digest = entry.get("sha256")
    return bool(
        _checkpoint_diff_entry_size(entry) is not None
        and isinstance(digest, str)
        and len(digest) == 64
        and all(character in "0123456789abcdef" for character in digest)
    )

def _filesystem_checkpoint_receipt(
    root: Path,
    *,
    action_kind: str,
    action_completed: bool,
    workspace_diff: Mapping[str, Any] | None,
) -> dict[str, Any]:
    diff = workspace_diff if isinstance(workspace_diff, Mapping) else {}
    changed_entry: Mapping[str, Any] | None = None
    added = diff.get("added", ())
    if isinstance(added, (list, tuple)):
        for item in added:
            if (
                isinstance(item, Mapping)
                and item.get("path") == FILESYSTEM_CHECKPOINT_PATH
                and _explicit_regular_checkpoint_diff_entry(item)
            ):
                changed_entry = item
                break
    modified = diff.get("modified", ())
    if changed_entry is None and isinstance(modified, (list, tuple)):
        for item in modified:
            if not isinstance(item, Mapping):
                continue
            before = item.get("before")
            after = item.get("after")
            if (
                isinstance(before, Mapping)
                and isinstance(after, Mapping)
                and before.get("path") == FILESYSTEM_CHECKPOINT_PATH
                and after.get("path") == FILESYSTEM_CHECKPOINT_PATH
                and _explicit_regular_checkpoint_diff_entry(before)
                and _explicit_regular_checkpoint_diff_entry(after)
                and before.get("sha256") != after.get("sha256")
            ):
                changed_entry = after
                break
    exists, regular_file, size_bytes, digest, _payload = (
        _read_filesystem_checkpoint_beneath(root)
    )
    changed = bool(
        changed_entry is not None
        and exists
        and regular_file
        and _checkpoint_diff_entry_size(changed_entry) == size_bytes
        and changed_entry.get("sha256") == digest
    )
    return {
        "schema": FILESYSTEM_CHECKPOINT_RECEIPT_SCHEMA,
        "path": FILESYSTEM_CHECKPOINT_PATH,
        "action_kind": str(action_kind).lower(),
        "action_completed": bool(action_completed),
        "changed": changed,
        "exists": exists,
        "regular_file": regular_file,
        "size_bytes": size_bytes,
        "sha256": digest,
    }

def _filesystem_checkpoint_read_receipt(
    checkpoint_receipt: Mapping[str, Any],
    *,
    action_kind: str,
    action_completed: bool,
    result: Any,
) -> dict[str, Any]:
    result_map = result if isinstance(result, Mapping) else {}
    stdout = result_map.get("stdout")
    payload = stdout.encode("utf-8") if isinstance(stdout, str) else None
    size = checkpoint_receipt.get("size_bytes")
    digest = checkpoint_receipt.get("sha256")
    observed = bool(
        action_kind == "bash"
        and action_completed
        and result_map.get("stdout_truncated") is False
        and checkpoint_receipt.get("changed") is False
        and checkpoint_receipt.get("exists") is True
        and checkpoint_receipt.get("regular_file") is True
        and isinstance(size, int)
        and not isinstance(size, bool)
        and 0 < size <= FILESYSTEM_CHECKPOINT_MAX_BYTES
        and isinstance(digest, str)
        and payload is not None
        and len(payload) == size
        and hashlib.sha256(payload).hexdigest() == digest
    )
    return {
        "schema": FILESYSTEM_CHECKPOINT_READ_RECEIPT_SCHEMA,
        "path": FILESYSTEM_CHECKPOINT_PATH,
        "observed": observed,
        "size_bytes": size if isinstance(size, int) and not isinstance(size, bool) else None,
        "sha256": digest if isinstance(digest, str) else None,
    }

def _read_filesystem_checkpoint_beneath(
    root: Path,
) -> tuple[bool, bool, int | None, str | None, bytes | None]:

    directory_flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        directory_flags |= os.O_DIRECTORY
    if hasattr(os, "O_NOFOLLOW"):
        directory_flags |= os.O_NOFOLLOW
    if hasattr(os, "O_CLOEXEC"):
        directory_flags |= os.O_CLOEXEC
    file_flags = os.O_RDONLY | os.O_NONBLOCK
    if hasattr(os, "O_NOFOLLOW"):
        file_flags |= os.O_NOFOLLOW
    if hasattr(os, "O_CLOEXEC"):
        file_flags |= os.O_CLOEXEC

    root_fd: int | None = None
    memory_fd: int | None = None
    checkpoint_fd: int | None = None
    try:
        root_fd = os.open(root, directory_flags)
        try:
            memory_fd = os.open(".agent_memory", directory_flags, dir_fd=root_fd)
        except OSError:
            return False, False, None, None, None
        try:
            path_before = os.stat(
                "CONTINUATION.md", dir_fd=memory_fd, follow_symlinks=False
            )
        except OSError:
            return False, False, None, None, None
        try:
            checkpoint_fd = os.open(
                "CONTINUATION.md", file_flags, dir_fd=memory_fd
            )
        except OSError:
            return True, False, None, None, None

        before = os.fstat(checkpoint_fd)
        if not _same_file_identity(path_before, before):
            return True, False, None, None, None
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            return True, False, None, None, None
        size = int(before.st_size)
        payload: bytes | None = None
        if size <= FILESYSTEM_CHECKPOINT_MAX_BYTES:
            chunks: list[bytes] = []
            remaining = FILESYSTEM_CHECKPOINT_MAX_BYTES + 1
            while remaining > 0:
                chunk = os.read(checkpoint_fd, min(remaining, 64 * 1024))
                if not chunk:
                    break
                chunks.append(chunk)
                remaining -= len(chunk)
            payload = b"".join(chunks)

        after = os.fstat(checkpoint_fd)
        try:
            path_after = os.stat(
                "CONTINUATION.md", dir_fd=memory_fd, follow_symlinks=False
            )
        except OSError:
            return True, False, None, None, None
        if not (
            _same_file_identity(before, after)
            and _same_file_identity(before, path_after)
        ):
            return True, False, None, None, None
        if size > FILESYSTEM_CHECKPOINT_MAX_BYTES:
            return True, True, size, None, None
        if payload is None or len(payload) != size:
            return True, False, None, None, None
        return True, True, size, hashlib.sha256(payload).hexdigest(), payload
    except OSError:
        return False, False, None, None, None
    finally:
        for descriptor in (checkpoint_fd, memory_fd, root_fd):
            if descriptor is not None:
                os.close(descriptor)

def _same_file_identity(left: os.stat_result, right: os.stat_result) -> bool:
    fields = ("st_dev", "st_ino", "st_mode", "st_nlink", "st_size")
    if any(getattr(left, name) != getattr(right, name) for name in fields):
        return False
    for name in ("st_mtime_ns", "st_ctime_ns", "st_blocks"):
        if hasattr(left, name) and hasattr(right, name):
            if getattr(left, name) != getattr(right, name):
                return False
    return True

def _meaningful_changed_paths(changed_paths: tuple[str, ...]) -> tuple[str, ...]:
    meaningful: list[str] = []
    for raw_path in changed_paths:
        path = PurePosixPath(raw_path)
        if path.name in GENERATED_FILE_NAMES:
            continue
        if path.suffix in {".pyc", ".pyo"}:
            continue
        if any(part in GENERATED_PATH_PARTS for part in path.parts):
            continue
        meaningful.append(raw_path)
    return tuple(sorted(set(meaningful)))

_TEST_RUN_COMMAND_RE = re.compile(r"\b(pytest|unittest)\b")
_PACKAGE_INSTALL_RE = re.compile(
    r"\b(pip|pip3|conda|apt|apt-get|uv)\s+(install|add)\b"
)

def _is_test_run_command(command: str) -> bool:
    return bool(_TEST_RUN_COMMAND_RE.search(command)) and not bool(
        _PACKAGE_INSTALL_RE.search(command)
    )

_PYTEST_CONTROL_BASENAMES = frozenset(
    {"conftest.py", "pytest.ini", "tox.ini", "pyproject.toml", "setup.cfg"}
)

def _test_infra_violation_paths(
    changed_paths: tuple[str, ...], profile: SwesmithProfileBinding
) -> tuple[str, ...]:

    declared_test_paths = set(profile.all_test_paths)
    direct_test_dirs = {
        str(PurePosixPath(test_path).parent)
        for test_path in profile.all_test_paths
    }
    violations: list[str] = []
    for raw_path in changed_paths:
        path = PurePosixPath(raw_path)
        if str(path) in declared_test_paths:
            continue
        if path.name in _PYTEST_CONTROL_BASENAMES:
            violations.append(raw_path)
        elif path.name == "__init__.py" and str(path.parent) in direct_test_dirs:
            violations.append(raw_path)
    return tuple(sorted(set(violations)))

_RUNNER_PATCH_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("pytest_attribute_assignment", re.compile(
        r"(?<![\w.])pytest\s*\.\s*[A-Za-z_][A-Za-z0-9_]*"
        r"(?:\s*\.\s*[A-Za-z_][A-Za-z0-9_]*)*\s*=(?!=)"
    )),
    ("monkeypatch_setattr_pytest", re.compile(
        r"monkeypatch\s*\.\s*setattr\s*\(\s*['\"]?pytest\b"
    )),
    ("sys_modules_pytest_replacement", re.compile(
        r"sys\s*\.\s*modules\s*\[\s*['\"]pytest['\"]\s*\]"
    )),

    ("pytest_addopts_steering", re.compile(
        r"PYTEST_ADDOPTS(?:['\"]\s*\]\s*=|\s*=(?!=))"
    )),
    ("direct_runtest_assignment", re.compile(
        r"\bFunction\s*\.\s*runtest\s*=(?!=)"
    )),

    ("atexit_registration", re.compile(r"\batexit\s*\.\s*register\s*\(")),
    ("interpreter_hard_exit", re.compile(r"\bos\s*\.\s*_exit\s*\(\s*0\s*\)")),
)
_RUNNER_PATCH_SCAN_MAX_BYTES = 2 * 1024 * 1024
_HARD_EXIT_ZERO_RE = re.compile(r"\bos\s*\.\s*_exit\s*\(\s*0\s*\)")

def _runner_patch_violations(
    source_changed_paths: tuple[str, ...],
    profile: SwesmithProfileBinding,
    policy_root: Path,
) -> tuple[dict[str, str], ...]:

    declared_test_paths = set(profile.all_test_paths)
    violations: list[dict[str, str]] = []
    for raw_path in source_changed_paths:
        if str(PurePosixPath(raw_path)) in declared_test_paths:
            continue
        if not raw_path.endswith(".py"):
            continue
        candidate = policy_root / PurePosixPath(raw_path)
        try:
            if not candidate.is_file() or candidate.is_symlink():
                continue
            text = candidate.read_text(
                encoding="utf-8", errors="replace"
            )[:_RUNNER_PATCH_SCAN_MAX_BYTES]
        except OSError:
            continue
        for label, pattern in _RUNNER_PATCH_PATTERNS:
            match = pattern.search(text)
            if match is None:
                continue
            if label == "atexit_registration" and not _HARD_EXIT_ZERO_RE.search(text):

                continue
            violations.append(
                {"path": raw_path, "pattern": label, "snippet": match.group(0)}
            )
            break
    return tuple(violations)

def _submission_from_shell_result(
    *, stdout: str, exit_code: int, timed_out: bool
) -> str | None:
    if timed_out or exit_code != 0:
        return None
    lines = stdout.lstrip().splitlines(keepends=True)
    if not lines or lines[0].strip() != UPSTREAM_SUBMISSION_SENTINEL:
        return None
    return "".join(lines[1:])

def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

def _initial_observation(
    problem_statement: str,
    *,
    max_policy_turns: int,
) -> str:
    return (
        "Repair the persistent repository in /testbed for this issue. Independent actions may "
        "share one turn as consecutive Qwen XML tool calls. Use bash for inspection, editing, and tests through "
        "Qwen XML tool calls in this exact shape:\n"
        "<tool_call>\n"
        "<function=bash>\n"
        "<parameter=command>\n"
        "ls\n"
        "</parameter>\n"
        "</function>\n"
        "</tool_call>\n"
        "Write command text directly instead of JSON-escaping quotes or backslashes. "
        "Start each call at byte zero with <tool_call> and output only complete calls, without prose between or after them, "
        "Markdown, or a <think> tag. Keep edits localized: never paste or "
        "rewrite an entire existing file in one action. Use a bounded shell "
        "command (sed in-place replacement or a quoted here-document), and stay "
        "below the response limit. "
        "The workspace persists for the whole episode and has no .git directory. After a "
        "source path changed and relevant tests ran, submit with exactly this Qwen XML "
        "tool call:\n"
        "<tool_call>\n"
        "<function=bash>\n"
        "<parameter=command>\n"
        "echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT\n"
        "</parameter>\n"
        "</function>\n"
        "</tool_call>\n"
        "The successful command must print the upstream submission "
        "sentinel as its first stdout line; then the current persistent workspace receives "
        "one official grade. Any plain text is invalid. Reaching the turn limit without "
        "that sentinel ends the episode with reward -0.01 and does not grade the workspace. "
        f"You have at most {max_policy_turns} total policy turns; task-neutral context "
        "compactions consume this same budget. Verify and submit as soon as the repair is "
        "ready; do not wait for the horizon.\n\n"
        "Issue:\n"
        + problem_statement.strip()
        + "\n\nBegin with real bash Qwen XML tool calls in the exact form above."
    )

def _parser_error_observation(
    action: ParsedPolicyAction,
    *,
    turn_count: int | None = None,
    max_policy_turns: int | None = None,
) -> str:
    result = (
        f"Invalid action syntax: {action.error}. This action received reward -0.01; "
        "the episode remains open. Start at byte zero and retry with one corrected Qwen XML "
        "tool call:\n"
        "<tool_call>\n"
        "<function=bash>\n"
        "<parameter=command>\n"
        "pwd\n"
        "</parameter>\n"
        "</function>\n"
        "</tool_call>\n"
        "Output complete tool "
        "calls only, with no reasoning, Markdown, or surrounding text. Keep the "
        "edit localized instead of pasting or rewriting an entire file. Submit "
        "only by running the upstream submission sentinel in a Qwen XML bash "
        "after editing and testing."
    )
    if turn_count is not None and max_policy_turns is not None:
        result += "\n" + _swe_turn_budget_footnote(turn_count, max_policy_turns)
    return result

def _swe_turn_budget_footnote(
    turn_count: int,
    max_policy_turns: int,
) -> str:

    remaining = max(0, max_policy_turns - turn_count)
    return (
        f"[SWE turn budget: turn {turn_count} of {max_policy_turns}; "
        f"{remaining} turns remain.]"
    )

def _shell_observation(
    *,
    exit_code: int,
    elapsed_ms: int,
    timed_out: bool,
    stdout: str,
    stderr: str,
    stdout_truncated: bool,
    stderr_truncated: bool,
    changed_paths: tuple[str, ...],
    max_observation_bytes: int = DEFAULT_MAX_OBSERVATION_BYTES,
    turn_count: int | None = None,
    max_policy_turns: int | None = None,
) -> str:
    if type(max_observation_bytes) is not int or max_observation_bytes <= 0:
        raise ValueError("max_observation_bytes must be a positive integer")

    stdout_limit = max(1, max_observation_bytes // 2)
    stderr_limit = max(1, max_observation_bytes - stdout_limit)
    visible_stdout, stdout_was_bounded = _bound_shell_output(
        stdout,
        limit=stdout_limit,
        truncated=stdout_truncated,
        label="stdout",
    )
    visible_stderr, stderr_was_bounded = _bound_shell_output(
        stderr,
        limit=stderr_limit,
        truncated=stderr_truncated,
        label="stderr",
    )
    observation = (
        f"bash exit_code={exit_code} elapsed_ms={elapsed_ms} "
        f"timed_out={str(timed_out).lower()} "
        f"stdout_truncated={str(stdout_truncated).lower()} "
        f"stderr_truncated={str(stderr_truncated).lower()} "
        f"visible_output_truncated={str(stdout_was_bounded or stderr_was_bounded).lower()} "
        f"visible_output_budget_bytes={max_observation_bytes}\n"
        "stdout:\n"
        + (visible_stdout if visible_stdout else "<empty>")
        + "\nstderr:\n"
        + (visible_stderr if visible_stderr else "<empty>")
        + "\nworkspace changed paths: "
        + _changed_paths_observation(changed_paths)
    )
    if turn_count is not None and max_policy_turns is not None:
        separator = "" if observation.endswith("\n") else "\n"
        observation += separator + _swe_turn_budget_footnote(
            turn_count, max_policy_turns
        )
    return observation

def _changed_paths_observation(
    changed_paths: tuple[str, ...],
    *,
    max_bytes: int = MAX_VISIBLE_CHANGED_PATHS_BYTES,
) -> str:

    if type(max_bytes) is not int or max_bytes <= 0:
        raise ValueError("max_bytes must be a positive integer")
    if not changed_paths:
        return "none"

    encoded_paths = [path.encode("utf-8", errors="replace") for path in changed_paths]
    digest = hashlib.sha256(b"\n".join(encoded_paths)).hexdigest()
    prefix = f"{len(changed_paths)} paths; sha256={digest}; sample="
    suffix = "; sample_truncated=true"
    
    budget = max(0, max_bytes - len(prefix.encode("utf-8")) - len(suffix.encode("utf-8")))
    selected: list[str] = []
    used = 2  
    candidates = list(dict.fromkeys((changed_paths[0], changed_paths[-1])))
    for path in candidates:
        rendered = path.replace("\\", "/")
        token = rendered if not selected else ", " + rendered
        token_bytes = len(token.encode("utf-8", errors="replace"))
        if used + token_bytes > budget:
            continue
        selected.append(rendered)
        used += token_bytes
    sample = "[" + ", ".join(selected) + "]"
    omitted = len(changed_paths) - len(selected)
    result = prefix + sample
    if omitted:
        result += f"; omitted={omitted}"
    if len(result.encode("utf-8", errors="replace")) > max_bytes:
        result = (prefix + suffix).encode("utf-8", errors="replace")[:max_bytes].decode(
            "utf-8", errors="ignore"
        )
    return result

def _bound_shell_output(
    text: str,
    *,
    limit: int,
    truncated: bool,
    label: str,
) -> tuple[str, bool]:

    raw = text.encode("utf-8", errors="replace")
    marker = f"\n[{label} truncated: visible output budget reached]\n".encode(
        "utf-8"
    )
    if not truncated and len(raw) <= limit:
        return text, False
    if limit <= len(marker):
        return marker[:limit].decode("utf-8", errors="ignore"), True
    payload_limit = limit - len(marker)
    head_limit = (payload_limit + 1) // 2
    tail_limit = payload_limit - head_limit
    head = raw[:head_limit].decode("utf-8", errors="ignore")
    tail = raw[-tail_limit:].decode("utf-8", errors="ignore") if tail_limit else ""
    return head + marker.decode("utf-8") + tail, True
