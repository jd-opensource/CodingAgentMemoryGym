from __future__ import annotations

from copy import deepcopy
import json
import math
import re
from typing import Any, Mapping, Sequence

import requests

from camg.controller import (BaseEnvClient)
from camg.controller.types import (
    PolicyContextCapacityExceeded,
    CONTEXT_OPERATION_REPLACE,
    ConversationMessage,
    PolicyContextPressure,
    StepOutput,
    build_task_neutral_context_transition,
    build_task_neutral_transition_info,
)
from .filesystem_checkpoint import (
    FILESYSTEM_CHECKPOINT_CONTINUATION_MARKER,
    FILESYSTEM_CHECKPOINT_LONG_LIVED_MEMORY_NOTICE,
    FILESYSTEM_CHECKPOINT_MAX_BYTES,
    FILESYSTEM_CHECKPOINT_PATH,
    FILESYSTEM_CHECKPOINT_REQUEST,
    checkpoint_retry_trigger_tokens,
    build_filesystem_checkpoint_read_retry_observation,
    build_filesystem_checkpoint_retry_observation,
    build_filesystem_checkpoint_write_retry_context,
    build_post_checkpoint_context,
    build_post_checkpoint_read_retry_context,
    bind_filesystem_checkpoint_receipt_to_submitted_action,
    filesystem_checkpoint_failure_reason,
    filesystem_checkpoint_framing_sha256,
    filesystem_checkpoint_read_failure_reason,
    filesystem_checkpoint_read_observed,
    filesystem_checkpoint_write_succeeded,
)
from .verl_qwen_tool_parser import (
    QWEN_INVALID_ACTION_SENTINEL,
    QWEN_SINGLE_TOOL_CALL_CONTRACT,
    WORKSPACE_SHELL_CONTRACT,
    collect_clean_multi_qwen_tool_calls,
    parse_single_qwen3_tool_call,
)


SWE_CHECKPOINT_SHELL_SAFE_EXAMPLE = (
    "<tool_call>\n"
    "<function=bash>\n"
    "<parameter=command>\n"
    "cat > .agent_memory/CONTINUATION.md <<'AGENT_MEMORY_EOF'\n"
    "objective: <user's task>\n"
    "evidence: <verified state>\n"
    "paths: <relevant files>\n"
    "next: <concrete action>\n"
    "AGENT_MEMORY_EOF\n"
    "</parameter>\n"
    "</function>\n"
    "</tool_call>"
)
SWE_CHECKPOINT_READ_ACTION = (
    "<tool_call>\n"
    "<function=bash>\n"
    "<parameter=command>\n"
    "cat .agent_memory/CONTINUATION.md\n"
    "</parameter>\n"
    "</function>\n"
    "</tool_call>"
)

SWE_CONTEXT_COMPACTION_REQUEST = (
    FILESYSTEM_CHECKPOINT_REQUEST
    + " The reserved `.agent_memory` directory already exists. If the repair is "
    "already complete, submit with the normal terminal sentinel. Otherwise, on "
    "this turn only, overwrite the checkpoint; do not inspect, read, test, edit "
    "source, or write another path. Use exactly the Qwen XML shell action below, "
    "replacing its placeholders. Keep the quoted heredoc and literal multiline "
    "command inside the command parameter; do not use printf/echo for "
    "checkpoint text:\n"
    + SWE_CHECKPOINT_SHELL_SAFE_EXAMPLE
    + " For this coding task, preserve the issue objective, decisive inspection "
    "and test evidence, changed source paths, unresolved failure, and the next "
    "concrete edit or test."
)
SWE_POLICY_CONTINUATION_MARKER = (
    FILESYSTEM_CHECKPOINT_CONTINUATION_MARKER
    + " Do not inspect, edit, test, or submit task source until the required "
    "checkpoint read succeeds. Output exactly this Qwen XML action and no other "
    "text:\n\n"
    + SWE_CHECKPOINT_READ_ACTION
)

SWE_MIN_ACTIONS_FOR_CHECKPOINT_WRITE_READ_ANSWER = 3


_SWE_TURN_BUDGET_FOOTNOTE_RE = re.compile(
    r"\[SWE turn budget: turn \d+ of \d+; \d+ turns remain\.\]"
)


ACTOR_CREDIT_SCHEMA = "task_neutral_actor_credit_v1"
ACTION_PROGRESS_SCHEMA = "swesmith_action_progress_v1"
SWE_MEMORY_CONTRACT = "policy_filesystem_checkpoint_then_client_replace_v3"
_POSITIVE_ACTOR_CREDIT_BASES = {
    "shell_executed",
    "workspace_changed",
    "terminal_submission",
    "policy_context_compaction",
}
_INELIGIBLE_ACTOR_CREDIT_BASES = {
    "parser_rejected",
    "executor_rejected",
    "no_workspace_change",
    "zero_progress_repeat",


    "environment_excluded",


    "workspace_integrity_violation",
}


def _validate_actor_credit_receipt(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise RuntimeError("SWE-smith response is missing its actor-credit receipt")
    expected_keys = {"schema", "positive_eligible", "basis"}
    if set(value) != expected_keys:
        raise RuntimeError(
            "SWE-smith actor-credit receipt has unexpected fields: "
            f"{sorted(set(value) - expected_keys)}"
        )
    if value.get("schema") != ACTOR_CREDIT_SCHEMA:
        raise RuntimeError("SWE-smith actor-credit receipt schema drifted")
    positive_eligible = value.get("positive_eligible")
    if type(positive_eligible) is not bool:
        raise RuntimeError(
            "SWE-smith actor-credit positive_eligible must be boolean"
        )
    basis = value.get("basis")
    allowed_bases = (
        _POSITIVE_ACTOR_CREDIT_BASES
        if positive_eligible
        else _INELIGIBLE_ACTOR_CREDIT_BASES
    )
    if basis not in allowed_bases:
        raise RuntimeError(
            "SWE-smith actor-credit basis disagrees with positive_eligible: "
            f"{basis!r}"
        )
    return {
        "schema": ACTOR_CREDIT_SCHEMA,
        "positive_eligible": positive_eligible,
        "basis": str(basis),
    }


def _validate_action_progress_receipt(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise RuntimeError("SWE-smith shell response is missing action progress")
    expected_keys = {
        "schema",
        "action_fingerprint",
        "result_fingerprint",
        "workspace_changed",
    }
    if set(value) != expected_keys:
        raise RuntimeError(
            "SWE-smith action-progress receipt has unexpected fields: "
            f"{sorted(set(value) - expected_keys)}"
        )
    if value.get("schema") != ACTION_PROGRESS_SCHEMA:
        raise RuntimeError("SWE-smith action-progress receipt schema drifted")
    normalized: dict[str, Any] = {"schema": ACTION_PROGRESS_SCHEMA}
    for key in ("action_fingerprint", "result_fingerprint"):
        fingerprint = value.get(key)
        if (
            not isinstance(fingerprint, str)
            or len(fingerprint) != 64
            or any(character not in "0123456789abcdef" for character in fingerprint)
        ):
            raise RuntimeError(
                f"SWE-smith action-progress {key} must be lowercase SHA256"
            )
        normalized[key] = fingerprint
    workspace_changed = value.get("workspace_changed")
    if type(workspace_changed) is not bool:
        raise RuntimeError(
            "SWE-smith action-progress workspace_changed must be boolean"
        )
    normalized["workspace_changed"] = workspace_changed
    return normalized

_SWE_QWEN_TOOL_SCHEMAS = (
    {
        "type": "function",
        "function": {
            "name": "bash",
            "description": "Run one command in the persistent /testbed workspace.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string"},
                },
                "required": ["command"],
                "additionalProperties": False,
            },
        },
    },
)


SWE_POLICY_SYSTEM_PROMPT = (
    "You are a coding agent in one persistent /testbed repository. Inspect, edit, "
    "and test until the issue is fixed. Your response channel is an action parser, "
    "not a chat channel. Reason inside think tags before each tool call. "
    + QWEN_SINGLE_TOOL_CALL_CONTRACT
    + "\n"
    + WORKSPACE_SHELL_CONTRACT
    + " Reasoning belongs inside think tags before the tool call.\n\n"
    "# Exact tool syntax\n\n"
    "For inspection, editing, or tests, output Qwen XML tool calls. "
    "For a shell command, use exactly this shape:\n"
    "<tool_call>\n"
    "<function=bash>\n"
    "<parameter=command>\n"
    "find . -maxdepth 2 -type f | head -80\n"
    "</parameter>\n"
    "</function>\n"
    "</tool_call>\n"
    "Replace the command text with the command you need. The command parameter is "
    "the only parameter; never add workdir or timeout_ms. Command text is literal "
    "and does not use JSON string escaping. Commands already run from the /testbed "
    "repository root; use paths such as src/module.py, never /testbed/src/module.py.\n"
    "When several independent commands are useful together, for example "
    "inspecting two different regions, emit them as consecutive envelopes "
    "in the same response:\n"
    "<tool_call>\n<function=bash>\n<parameter=command>\n"
    "sed -n '1,40p' src/module.py\n</parameter>\n</function>\n</tool_call>\n"
    "<tool_call>\n<function=bash>\n<parameter=command>\n"
    "grep -rn 'def parse' src/ | head -20\n</parameter>\n</function>\n</tool_call>\n"
    "For file edits, use bounded shell edits after inspecting the exact target "
    "lines. A few reliable shapes:\n"
    "sed -i 's/old_string/new_string/' path.py   (replace first occurrence)\n"
    "sed -i 's/old_string/new_string/g' path.py   (replace all occurrences)\n"
    "sed -i '12,40s/old/new/' path.py             (replace within a line range)\n"
    "cat > new_path.py <<'EOF' ... EOF            (write a new file with the exact "
    "final text)\n"
    "Quote sed patterns carefully and prefer simple literal strings over regex. "
    "Paths are relative to /testbed, for example src/module.py, never "
    "/testbed/src/module.py. Prefer a bounded edit over rewriting an entire "
    "existing source file; re-inspect the small target region before and after "
    "an edit. If an edit fails or matches nothing, re-read the exact lines and "
    "retry; do not replace the whole file when a bounded edit works.\n\n"
    "# Durable debugging notes\n"
    "This is a long-running debugging task. The persistent workspace can hold ordinary "
    "files that you create and maintain with the same bash "
    "actions. For a debugging path that may span context compactions, maintain a "
    "concise evidence ledger incrementally instead of waiting for the compaction "
    "request. Update it at meaningful state changes: a hypothesis is introduced or "
    "ruled out, a command or test changes the evidence, a root cause or partial fix is "
    "verified, a regression is found, or the next branch is chosen. Record high-volume "
    "state that may outlive the visible "
    "conversation: hypotheses, commands or tests already tried, exact observations, "
    "failed approaches and why they failed, successful partial results, and unresolved "
    "next checks. Choose a safe relative path and organization; no filename or note "
    "format is prescribed, and a short task may not need notes at all. Keep notes "
    "separate from source code when practical.\n"
    "Before context compaction, keep detailed evidence that may be needed later in "
    "ordinary task files. At an explicit context-boundary request, use one normal "
    "bash action to overwrite "
    "`.agent_memory/CONTINUATION.md` with a short working-state snapshot and locators "
    "for those longer-lived files. That action is executed normally and consumes the "
    "same policy-action budget. Old messages are removed only after the exact write is "
    "verified. After replacement, read the checkpoint with a normal command, then read "
    "any detailed notes it points to before acting on them. The checkpoint does not "
    "replace source files, test artifacts, or voluntary debugging notes. "
    + FILESYSTEM_CHECKPOINT_LONG_LIVED_MEMORY_NOTICE
    + "\n"
    "Illustrative pattern only (do not copy its content as a task answer): for "
    "arbitrary note text, put a quoted heredoc inside one bash command "
    "parameter. A later bash can run `rg -n "
    "'hypothesis|evidence|next check' .agent_memory`. Do not use inline single-quoted "
    "printf/echo for arbitrary note text. This is only a syntax illustration: do not "
    "assume a filename, content, or timing is useful for the current issue. Writing or "
    "reading a note has no separate reward; the native task result is the objective.\n\n"
    "# Turn budget\n"
    "Each observation footer carries a line of the form [SWE turn budget: turn N of 64; R turns remain.]. An episode that reaches turn 64 without the submit sentinel ends as a policy-step terminal failure with no grading: keep an eye on the remaining turns, verify incrementally instead of leaving all tests to the end, and submit once the fix is verified rather than continuing to explore.\n\n"
    "# Output contract\n"
    "Start at byte zero with <tool_call>. Do not use the bare "
    "bash JSON form. After an observation, reason inside think tags, then emit the "
    "next action. A shell command can "
    "edit the persistent workspace. Do not repeat a successful inspection or edit. "
    "Never submit a plain-text final response. After at least one non-generated source "
    "path has changed and the relevant tests have run, submit with one bash "
    "Qwen XML tool call whose command parameter is exactly `echo "
    "COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT`. Text after the tool call is a parser error and nothing runs; a leading think block is separated before the action is parsed. This "
    "workspace intentionally has no .git directory."
)


def _swe_invalid_qwen_action(reason: str) -> tuple[str, dict[str, Any]]:
    return QWEN_INVALID_ACTION_SENTINEL, {
        "tool_contract": "qwen3_xml_single_call_v1",
        "tool_parser": "qwen3_coder",
        "tool_parser_normalized": False,
        "tool_parser_error": reason,
        "submitted_action": QWEN_INVALID_ACTION_SENTINEL,
    }


def normalize_swesmith_policy_action(
    action: str,
) -> tuple[str, dict[str, Any]]:


    parsed = parse_single_qwen3_tool_call(
        action,
        tool_schemas=_SWE_QWEN_TOOL_SCHEMAS,
    )
    if parsed is None:
        multi_names = collect_clean_multi_qwen_tool_calls(action)
        if multi_names is not None:
            submitted = action.strip()
            return submitted, {
                "tool_contract": "qwen3_xml_multi_call_v1",
                "tool_parser": "qwen3_coder",
                "tool_parser_normalized": False,
                "function_names": multi_names,
                "submitted_action": submitted,
            }
        return _swe_invalid_qwen_action(
            "expected_complete_qwen_xml_tool_call"
        )
    name = parsed.name
    arguments = dict(parsed.arguments)
    try:
        if name == "bash":
            allowed = {"command"}
            if "command" not in arguments or not set(arguments) <= allowed:
                raise ValueError(
                    "bash accepts only the command parameter; "
                    "remove workdir and timeout_ms"
                )
            command = arguments["command"]
            if not isinstance(command, str) or not command.strip():
                raise ValueError("bash command must be a non-empty string")
            normalized: dict[str, Any] = {"command": command}
            submitted = "bash " + json.dumps(
                normalized, ensure_ascii=False, separators=(",", ":")
            )
        else:
            raise ValueError(f"unsupported SWE-smith function: {name}")
    except (TypeError, ValueError) as exc:
        return _swe_invalid_qwen_action(str(exc))
    return submitted, {
        "tool_contract": "qwen3_xml_single_call_v1",
        "tool_parser": parsed.parser_name,
        "tool_parser_normalized": True,
        "submitted_action": submitted,
    }


class SwesmithEnvClient(BaseEnvClient):
    conversation_start = (
        ConversationMessage(
            {
                "from": "human",
                "loss": None,
                "value": SWE_POLICY_SYSTEM_PROMPT,
            }
        ),
        ConversationMessage(
            {"from": "gpt", "loss": False, "value": "Understood."}
        ),
    )

    def __init__(
        self,
        env_server_base: str,
        data_len: int | None = None,
        *args,
        timeout: int = 900,
        invalid_action_reward: float = 0.0,
        checkpoint_contract_penalty: float = 0.0,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        if (
            isinstance(invalid_action_reward, bool)
            or not isinstance(invalid_action_reward, (int, float))
            or not math.isfinite(float(invalid_action_reward))
            or float(invalid_action_reward) != 0.0
        ):
            raise ValueError(
                "SWE-smith invalid_action_reward must be zero because the endpoint "
                "owns parser/executor/horizon penalties"
            )
        if (
            isinstance(checkpoint_contract_penalty, bool)
            or not isinstance(checkpoint_contract_penalty, (int, float))
            or not math.isfinite(float(checkpoint_contract_penalty))
            or float(checkpoint_contract_penalty) > 0.0
        ):
            raise ValueError(
                "SWE-smith checkpoint_contract_penalty must be finite and "
                "non-positive"
            )
        self.env_server_base = env_server_base.rstrip("/")
        self.timeout = timeout
        self.invalid_action_reward = float(invalid_action_reward)
        self.checkpoint_contract_penalty = float(checkpoint_contract_penalty)
        metadata = self._request("GET", "metadata")
        memory_contract = metadata.get("memory_contract")
        if memory_contract != SWE_MEMORY_CONTRACT:
            raise RuntimeError(
                "SWE-smith endpoint memory contract mismatch: "
                f"expected {SWE_MEMORY_CONTRACT!r}, got {memory_contract!r}"
            )
        task_count = int(metadata["task_count"])
        if data_len is not None and int(data_len) > task_count:
            raise ValueError(
                f"SWE-smith data_len {data_len} exceeds server task_count {task_count}"
            )


        turn_ceiling = self._swe_configured_max_turns_from(metadata)
        if turn_ceiling is None:
            raise RuntimeError(
                "SWE-smith endpoint metadata lacks a usable turn ceiling "
                "(configured_max_policy_turns/max_steps must be a positive int)"
            )
        self.data_len = task_count if data_len is None else int(data_len)
        created = self._request("POST", "create", json={})
        self.env_id = int(created["id"])
        self.info = created
        self.metadata = metadata
        self._reset_policy_transition_state()

    def _reset_policy_transition_state(self) -> None:
        self._policy_step_count = 0
        self._native_call_count = 0
        self._policy_turn_index = 0
        self._policy_turn_budget: int | None = None
        self._context_epoch = 0
        self._session_epoch = 0
        self._immutable_policy_context: list[dict[str, str]] | None = None
        self._current_policy_context: list[dict[str, str]] | None = None
        self._policy_context_bound = False
        self._selected_policy_control: str | None = None
        self._checkpoint_retry_pending = False
        self._checkpoint_write_retry_framing: list[dict[str, str]] | None = None
        self._pending_checkpoint_read: dict[str, Any] | None = None
        self._pending_checkpoint_read_framing: list[dict[str, str]] | None = None
        self._zero_progress_shell_receipts: set[tuple[str, str]] = set()

    def begin_policy_turn(self, turn_index: int, turn_budget: int) -> None:


        self._policy_turn_index = int(turn_index)
        self._policy_turn_budget = int(turn_budget)

    def _swe_rewrite_turn_budget_footnote(self, text: str) -> str:


        if self._policy_turn_budget is None:
            return text
        used = self._policy_turn_index + 1
        remaining = max(0, self._policy_turn_budget - used)
        if remaining <= 1:


            replacement = (
                "[SWE FINAL TURN: your next response is the last action of "
                "this episode; there is no next turn. Work that is not "
                "submitted is never graded and scores zero, so do not "
                "verify, do not edit, and do not run any other command. "
                "Submit right now by running the command whose first "
                "stdout line is COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT. "
                "A partial fix submitted now can still pass; a perfect "
                "fix that is never submitted cannot.]"
            )
        else:
            replacement = (
                f"[SWE turn budget: turn {used} of "
                f"{self._policy_turn_budget}; {remaining} turns remain.]"
            )
        return _SWE_TURN_BUDGET_FOOTNOTE_RE.sub(replacement, text)

    def _classify_shell_actor_credit(
        self,
        actor_credit: Mapping[str, Any],
        action_progress: Mapping[str, Any],
    ) -> dict[str, Any]:
        if action_progress["workspace_changed"]:
            self._zero_progress_shell_receipts.clear()
            return dict(actor_credit)
        key = (
            str(action_progress["action_fingerprint"]),
            str(action_progress["result_fingerprint"]),
        )
        if key in self._zero_progress_shell_receipts:
            return {
                "schema": ACTOR_CREDIT_SCHEMA,
                "positive_eligible": False,
                "basis": "zero_progress_repeat",
            }
        self._zero_progress_shell_receipts.add(key)
        return dict(actor_credit)

    def policy_framing(self) -> list[dict[str, str]]:
        return [{"role": "system", "content": SWE_POLICY_SYSTEM_PROMPT}]

    def policy_tool_schemas(self) -> list[dict[str, Any]]:
        return deepcopy(list(_SWE_QWEN_TOOL_SCHEMAS))

    def normalize_initial_policy_context(
        self,
        messages: Sequence[Mapping[str, str]],
    ) -> list[dict[str, str]]:
        normalized = _copy_policy_messages(messages)
        observation = str(self.observe())
        if (
            not normalized
            or normalized[-1]["role"] != "user"
            or normalized[-1]["content"] != observation
        ):
            raise ValueError(
                "SWE-smith initial policy context must end with the current observation"
            )
        return self.policy_framing() + [
            {"role": "user", "content": observation}
        ]

    def bind_policy_context(
        self,
        messages: Sequence[Mapping[str, str]],
        *,
        initial: bool = False,
    ) -> None:
        normalized = _copy_policy_messages(messages)
        if initial:
            expected = self.policy_framing() + [
                {"role": "user", "content": str(self.observe())}
            ]
            if normalized != expected:
                raise ValueError(
                    "SWE-smith initial policy context differs from its system framing"
                )
            self._immutable_policy_context = deepcopy(normalized)
            self._policy_context_bound = True
        self._current_policy_context = normalized

    def policy_turn_candidate(self) -> str | None:
        if not self._policy_context_bound or self._pending_checkpoint_read is not None:
            return None
        return SWE_CONTEXT_COMPACTION_REQUEST

    def prepare_policy_turn(
        self, pressure: PolicyContextPressure | None
    ) -> str | None:
        self._selected_policy_control = None
        if not self._policy_context_bound:
            return None
        if self._pending_checkpoint_read is not None:
            return None
        if pressure is None:
            raise RuntimeError(
                "SWE-smith context compaction requires task-neutral token pressure"
            )
        capacity = pressure.effective_prompt_capacity
        if (
            pressure.action_prompt_tokens > capacity
            or pressure.candidate_prompt_tokens > capacity
        ):
            raise PolicyContextCapacityExceeded(
                "SWE-smith context reached the prompt cap before a trainable "
                "compaction could be sampled"
            )


        if self._policy_turn_budget is not None:


            remaining_turns = self._policy_turn_budget - (
                self._policy_turn_index + 1
            )
            if remaining_turns < SWE_MIN_ACTIONS_FOR_CHECKPOINT_WRITE_READ_ANSWER:
                return None
        else:
            max_turns = self._swe_configured_max_turns()
            if (
                max_turns is not None
                and (max_turns - self._native_call_count)
                < SWE_MIN_ACTIONS_FOR_CHECKPOINT_WRITE_READ_ANSWER
            ):
                return None


        if (
            not self._checkpoint_retry_pending
            and checkpoint_retry_trigger_tokens(
                pressure, control_request=SWE_CONTEXT_COMPACTION_REQUEST
            )
            < capacity
        ):
            return None
        if not self._checkpoint_retry_pending:
            if self._current_policy_context is None:
                raise RuntimeError(
                    "SWE-smith checkpoint request lost its pre-boundary context"
                )
            self._checkpoint_write_retry_framing = deepcopy(
                self._current_policy_context
            )
        elif self._checkpoint_write_retry_framing is None:
            raise RuntimeError(
                "SWE-smith checkpoint retry lost its pre-boundary context"
            )
        self._selected_policy_control = "context_compaction"
        return SWE_CONTEXT_COMPACTION_REQUEST

    def __len__(self) -> int:
        return self.data_len

    def observe(self) -> str:
        return str(self.info["observation"])

    @property
    def sample_excluded(self) -> bool:
        info = self.info.get("info", {})
        if not isinstance(info, Mapping):
            return False
        value = info.get("sample_excluded", False)
        if type(value) is not bool:
            raise RuntimeError("SWE-smith sample_excluded must be boolean")
        return value

    def step(self, action: str) -> StepOutput:
        if self._selected_policy_control == "context_compaction":
            return self._complete_context_compaction(action)
        return self._step_native_policy_action(action)

    def _step_native_policy_action(self, action: str) -> StepOutput:
        native_before = self._native_call_count
        policy_before = self._policy_step_count
        context_before = self._context_epoch
        session_before = self._session_epoch
        checkpoint_read_pending_before = self._pending_checkpoint_read
        checkpoint_read_framing_before = self._pending_checkpoint_read_framing
        submitted_action, parser_evidence = normalize_swesmith_policy_action(action)
        response = self._request(
            "POST",
            "step",
            json={"id": self.env_id, "action": submitted_action},
        )
        self._native_call_count += 1
        self._policy_step_count += 1
        self.info = response
        response_env_info = response.get("info", {})
        actor_credit = _validate_actor_credit_receipt(
            response_env_info.get("actor_credit")
            if isinstance(response_env_info, Mapping)
            else None
        )
        action_progress = None
        if actor_credit["basis"] in {"shell_executed", "terminal_submission"}:
            action_progress = _validate_action_progress_receipt(
                response_env_info.get("action_progress")
            )
            if actor_credit["basis"] == "shell_executed":
                actor_credit = self._classify_shell_actor_credit(
                    actor_credit,
                    action_progress,
                )
        elif response_env_info.get("action_progress") is not None:
            raise RuntimeError(
                "SWE-smith action progress appeared without shell execution"
            )
        if actor_credit["basis"] == "workspace_changed":
            self._zero_progress_shell_receipts.clear()
        native_reward = float(response["reward"])
        if not math.isfinite(native_reward):
            raise RuntimeError(
                "SWE-smith endpoint returned a non-finite reward"
            )
        sample_excluded = response_env_info.get("sample_excluded", False)
        if type(sample_excluded) is not bool:
            raise RuntimeError("SWE-smith sample_excluded must be boolean")
        if sample_excluded and (
            not bool(response.get("done")) or native_reward != 0.0
        ):
            raise RuntimeError(
                "SWE-smith excluded samples must be terminal with zero reward"
            )
        reward = native_reward
        after_step = response_env_info.get("step")
        if after_step is not None and int(after_step) != self._native_call_count:
            raise RuntimeError(
                "SWE-smith native step counter drifted from wrapper dispatches"
            )
        wrapper_evidence: dict[str, Any] = {
            "event": "native_action",
            "workspace_continuity_id": self.env_id,
            "actor_credit": actor_credit,
            "action_progress": action_progress,
        }
        read_receipt = (
            response_env_info.get("filesystem_checkpoint_read")
            if isinstance(response_env_info, Mapping)
            else None
        )
        if filesystem_checkpoint_read_observed(read_receipt):
            wrapper_evidence.update(
                {
                    "memory_event": "read",
                    "document_read_observed": True,
                    "filesystem_checkpoint_read": dict(read_receipt),
                }
            )
        else:
            changed_paths = (
                response_env_info.get("workspace_changed_paths")
                if isinstance(response_env_info, Mapping)
                else None
            )
            noncheckpoint_paths = (
                sorted(
                    {
                        str(path)
                        for path in changed_paths
                        if isinstance(path, str)
                        and path
                        and path != FILESYSTEM_CHECKPOINT_PATH
                    }
                )
                if isinstance(changed_paths, Sequence)
                and not isinstance(changed_paths, (str, bytes))
                else []
            )
            if noncheckpoint_paths:
                wrapper_evidence.update(
                    {
                        "memory_event": "modify",
                        "workspace_change_observed": True,
                        "workspace_changed_paths": noncheckpoint_paths,
                    }
                )
            elif response_env_info.get("shell_action_succeeded") is True:
                wrapper_evidence.update(
                    {
                        "memory_event": "execute",
                        "outcome": "success",
                        "execution_completed_observed": True,
                }
            )
        read_satisfied = False
        read_failure_reason = None
        if checkpoint_read_pending_before is not None:
            read_failure_reason = filesystem_checkpoint_read_failure_reason(
                read_receipt,
                checkpoint_read_pending_before,
            )
            read_satisfied = read_failure_reason is None
            wrapper_evidence.update(
                {
                    "checkpoint_read_required": True,
                    "checkpoint_read_satisfied": read_satisfied,
                    "checkpoint_read_retry_pending": bool(
                        not read_satisfied and not bool(response["done"])
                    ),
                    "checkpoint_read_failure_reason": read_failure_reason,
                    "checkpoint_read_expected_size_bytes": (
                        checkpoint_read_pending_before.get("size_bytes")
                    ),
                    "checkpoint_read_expected_sha256": (
                        checkpoint_read_pending_before.get("sha256")
                    ),
                }
            )
            if read_satisfied or bool(response["done"]):
                self._pending_checkpoint_read = None
                self._pending_checkpoint_read_framing = None
        policy_state = (
            build_filesystem_checkpoint_read_retry_observation(
                read_failure_reason or "checkpoint_read_not_observed"
            )
            if checkpoint_read_pending_before is not None
            and not read_satisfied
            and not bool(response["done"])
            else self._swe_rewrite_turn_budget_footnote(
                str(response["observation"])
            )
        )
        context_transition = None
        if (
            checkpoint_read_pending_before is not None
            and not read_satisfied
            and not bool(response["done"])
        ):
            if checkpoint_read_framing_before is None:
                raise RuntimeError(
                    "SWE-smith pending checkpoint read lost its trusted framing"
                )
            context_transition = build_task_neutral_context_transition(
                CONTEXT_OPERATION_REPLACE,
                messages=build_post_checkpoint_read_retry_context(
                    checkpoint_read_framing_before,
                    checkpoint_read_pending_before,
                    read_failure_reason or "checkpoint_read_not_observed",
                    continuation_marker=self._swe_continuation_marker(),
                ),
            )
        return StepOutput(
            state=policy_state,
            reward=reward,
            done=bool(response["done"]),
            info=build_task_neutral_transition_info(
                env_info=response_env_info,
                action_submission={
                    "raw_policy_output": action,
                    "submitted_action": submitted_action,
                    **parser_evidence,
                    "endpoint_action_submission": (
                        dict(response_env_info.get("action_submission"))
                        if isinstance(response_env_info, Mapping)
                        and isinstance(response_env_info.get("action_submission"), Mapping)
                        else {}
                    ),
                },
                native_step_before=native_before,
                native_step_after=self._native_call_count,
                native_call_count_before=native_before,
                native_call_count_after=self._native_call_count,
                context_epoch_before=context_before,
                context_epoch_after=self._context_epoch,
                session_epoch_before=session_before,
                session_epoch_after=self._session_epoch,
                policy_step_before=policy_before,
                policy_step_after=self._policy_step_count,
                context_transition=context_transition,
                wrapper_evidence=wrapper_evidence,
            ),
        )

    @staticmethod
    def _swe_configured_max_turns_from(metadata: object) -> int | None:

        if isinstance(metadata, Mapping):


            for key in (
                "prompt_policy_turns",
                "configured_max_policy_turns",
                "max_steps",
            ):
                value = metadata.get(key)
                if type(value) is int and value > 0:
                    return value
        return None

    def _swe_configured_max_turns(self) -> int | None:
        return self._swe_configured_max_turns_from(getattr(self, "metadata", None))

    def _swe_continuation_marker(self) -> str:

        if self._policy_turn_budget is not None:

            used = self._policy_turn_index + 1
            budget = (
                f" [SWE turn budget: turn {used} of "
                f"{self._policy_turn_budget}; "
                f"{max(0, self._policy_turn_budget - used)} turns remain.]"
            )
            return SWE_POLICY_CONTINUATION_MARKER + budget
        max_turns = self._swe_configured_max_turns()
        used = self._policy_step_count
        if max_turns is not None:
            budget = (
                f" [SWE turn budget: turn {used} of {max_turns}; "
                f"{max(0, max_turns - used)} turns remain.]"
            )
        else:
            budget = f" [SWE policy turns used so far: {used}.]"
        return SWE_POLICY_CONTINUATION_MARKER + budget

    def _complete_context_compaction(self, action: str) -> StepOutput:
        write_retry_framing_before = self._checkpoint_write_retry_framing
        native_output = self._step_native_policy_action(action)
        self._selected_policy_control = None
        info = dict(native_output.info)
        env_info = info.get("env_info", {})
        receipt_value = (
            env_info.get("filesystem_checkpoint")
            if isinstance(env_info, Mapping)
            else None
        )
        action_submission = info.get("action_submission")
        checkpoint_receipt = bind_filesystem_checkpoint_receipt_to_submitted_action(
            receipt_value,
            submitted_action=(
                action_submission.get("submitted_action")
                if isinstance(action_submission, Mapping)
                else None
            ),
        )
        persisted = filesystem_checkpoint_write_succeeded(checkpoint_receipt)
        checkpoint_failure_reason = filesystem_checkpoint_failure_reason(
            checkpoint_receipt
        )
        self._checkpoint_retry_pending = bool(not persisted and not native_output.done)
        policy_observation = (
            build_filesystem_checkpoint_retry_observation(
                checkpoint_failure_reason or "unknown_checkpoint_failure"
            )
            if self._checkpoint_retry_pending
            else native_output.state
        )

        context_transition = None
        checkpoint_framing_sha256 = None
        if persisted and not native_output.done:
            framing = self._immutable_policy_context
            if framing is None:
                raise RuntimeError("SWE-smith compaction lost its immutable task framing")
            checkpoint_framing_sha256 = filesystem_checkpoint_framing_sha256(
                framing
            )
            replacement = build_post_checkpoint_context(
                framing,
                checkpoint_receipt,
                continuation_marker=self._swe_continuation_marker(),
            )
            self._context_epoch += 1
            self._pending_checkpoint_read = dict(checkpoint_receipt)
            self._pending_checkpoint_read_framing = deepcopy(framing)
            self._checkpoint_write_retry_framing = None
            self._zero_progress_shell_receipts.clear()
            context_transition = build_task_neutral_context_transition(
                CONTEXT_OPERATION_REPLACE,
                messages=replacement,
            )
        elif native_output.done:
            self._checkpoint_write_retry_framing = None
            self._pending_checkpoint_read = None
            self._pending_checkpoint_read_framing = None
        else:
            if write_retry_framing_before is None:
                raise RuntimeError(
                    "SWE-smith failed checkpoint write lost its retry context"
                )
            context_transition = build_task_neutral_context_transition(
                CONTEXT_OPERATION_REPLACE,
                messages=build_filesystem_checkpoint_write_retry_context(
                    write_retry_framing_before,
                    checkpoint_failure_reason or "unknown_checkpoint_failure",
                    continuation_marker=self._swe_continuation_marker(),
                ),
            )

        native_wrapper = info.get("wrapper_evidence", {})
        actor_credit = (
            native_wrapper.get("actor_credit")
            if isinstance(native_wrapper, Mapping)
            else None
        )
        reward = float(native_output.reward)
        checkpoint_reward_overlay = None
        if (
            not persisted
            and not native_output.done
            and self.checkpoint_contract_penalty != 0.0
        ):


            reward_before = reward
            reward = min(reward_before, self.checkpoint_contract_penalty)
            checkpoint_reward_overlay = {
                "schema": "swesmith_checkpoint_contract_reward_v1",
                "basis": "checkpoint_contract_unsatisfied",
                "reward_before": reward_before,
                "configured_penalty": self.checkpoint_contract_penalty,
                "applied_delta": reward - reward_before,
                "final_reward": reward,
                "deduplicated": reward == reward_before,
            }
        wrapper_evidence = {
            "event": "context_compaction",
            "workspace_continuity_id": self.env_id,
            "native_environment_call_count": 1,
            "actor_credit": actor_credit,
            "continuation_path": FILESYSTEM_CHECKPOINT_PATH,
            "continuation_max_bytes": FILESYSTEM_CHECKPOINT_MAX_BYTES,
            "continuation_persisted": persisted,
            "checkpoint_receipt": checkpoint_receipt,
            "checkpoint_failure_reason": checkpoint_failure_reason,
            "context_replaced": bool(persisted and not native_output.done),
            "retry_pending": self._checkpoint_retry_pending,
            "checkpoint_retry_observation_bounded": self._checkpoint_retry_pending,
            "checkpoint_retry_context_rebuilt": self._checkpoint_retry_pending,
            "preserved_policy_output": persisted,
            "preserved_native_observation": persisted,
            "checkpoint_action_in_successor_context": False,
            "checkpoint_observation_in_successor_context": False,
            "checkpoint_content_in_successor_context": False,
            "checkpoint_framing_sha256": checkpoint_framing_sha256,
            "checkpoint_read_required_after": bool(
                persisted and not native_output.done
            ),
            "native_wrapper_evidence": (
                dict(native_wrapper) if isinstance(native_wrapper, Mapping) else {}
            ),
        }
        if checkpoint_reward_overlay is not None:
            wrapper_evidence["reward_overlay"] = checkpoint_reward_overlay
        return StepOutput(
            state=policy_observation,
            reward=reward,
            done=native_output.done,
            info=build_task_neutral_transition_info(
                env_info=env_info if isinstance(env_info, Mapping) else {},
                action_submission=info.get(
                    "action_submission", {"raw_policy_output": action}
                ),
                native_step_before=info.get("native_step_before"),
                native_step_after=info.get("native_step_after"),
                native_call_count_before=info.get("native_call_count_before"),
                native_call_count_after=info.get("native_call_count_after"),
                context_epoch_before=info.get("context_epoch_before"),
                context_epoch_after=self._context_epoch,
                session_epoch_before=info.get("session_epoch_before"),
                session_epoch_after=info.get("session_epoch_after"),
                policy_step_before=info.get("policy_step_before"),
                policy_step_after=info.get("policy_step_after"),
                context_transition=context_transition,
                wrapper_evidence=wrapper_evidence,
            ),
        )

    def reset(self, idx: int = 0) -> dict[str, Any]:
        response = self._request(
            "POST",
            "reset",
            json={"id": self.env_id, "data_idx": idx},
        )
        self.info = response
        self._reset_policy_transition_state()
        return response

    def detail(self, *, private_token: str | None = None) -> dict[str, Any]:
        headers = (
            {} if private_token is None else {"X-SWESMITH-Detail-Token": private_token}
        )
        return self._request(
            "GET", "detail", params={"id": self.env_id}, headers=headers
        )

    def finalize_horizon(self) -> StepOutput:
        response = self._request("POST", "horizon", json={"id": self.env_id})
        self.info = response
        response_env_info = response.get("info", {})
        horizon_reward = float(response["reward"])
        if not math.isfinite(horizon_reward):
            raise RuntimeError(
                "SWE-smith endpoint returned a non-finite reward at horizon finalization"
            )
        return StepOutput(
            state=self._swe_rewrite_turn_budget_footnote(
                str(response["observation"])
            ),
            reward=horizon_reward,
            done=bool(response["done"]),
            info=build_task_neutral_transition_info(
                env_info=response_env_info,
                action_submission={"control_action": "horizon"},
                native_step_before=self._native_call_count,
                native_step_after=self._native_call_count,
                native_call_count_before=self._native_call_count,
                native_call_count_after=self._native_call_count,
                context_epoch_before=self._context_epoch,
                context_epoch_after=self._context_epoch,
                session_epoch_before=self._session_epoch,
                session_epoch_after=self._session_epoch,
                policy_step_before=self._policy_step_count,
                policy_step_after=self._policy_step_count,
                wrapper_evidence={
                    "event": "horizon_finalization",
                    "workspace_continuity_id": self.env_id,
                },
            ),
        )

    def finalize_policy_horizon(self) -> StepOutput:


        return self.finalize_horizon()

    def close(self) -> dict[str, Any]:
        return self._request("POST", "close", json={"id": self.env_id})

    def _request(self, method: str, path: str, **kwargs) -> dict[str, Any]:
        response = requests.request(
            method,
            f"{self.env_server_base}/{path}",
            timeout=self.timeout,
            **kwargs,
        )
        if response.status_code != 200:
            raise requests.RequestException(
                f"SWE-smith {method} /{path} failed: "
                f"status={response.status_code} body={response.text[-1000:]}"
            )
        value = response.json()
        if not isinstance(value, dict):
            raise requests.RequestException(
                f"SWE-smith {method} /{path} returned a non-object response"
            )
        return value


def _copy_policy_messages(
    messages: Sequence[Mapping[str, str]],
) -> list[dict[str, str]]:
    normalized: list[dict[str, str]] = []
    for index, message in enumerate(messages):
        if not isinstance(message, Mapping):
            raise TypeError(f"policy message {index} must be a mapping")
        role = message.get("role")
        content = message.get("content")
        if role not in {"system", "user", "assistant", "tool"}:
            raise ValueError(f"policy message {index} has invalid role: {role!r}")
        if not isinstance(content, str):
            raise TypeError(f"policy message {index} content must be text")
        normalized_message = {"role": role, "content": content}
        if role == "tool":
            name = message.get("name")
            if not isinstance(name, str) or not name:
                raise ValueError(
                    f"policy tool message {index} must carry a nonempty name"
                )
            normalized_message["name"] = name
        normalized.append(normalized_message)
    if not normalized:
        raise ValueError("policy context must not be empty")
    return normalized
