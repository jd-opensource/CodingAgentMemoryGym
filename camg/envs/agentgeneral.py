from __future__ import annotations

import math
from copy import deepcopy
from typing import Any, Mapping, Sequence

from camg.controller.types import (
    CONTEXT_OPERATION_REPLACE,
    StepOutput,
    build_task_neutral_context_transition,
    build_task_neutral_transition_info,
)
from .filesystem_checkpoint import (
    FILESYSTEM_CHECKPOINT_PATH,
    FILESYSTEM_CHECKPOINT_REQUEST,
    build_post_checkpoint_context,
    build_post_checkpoint_read_retry_context,
    build_filesystem_checkpoint_retry_observation,
    build_filesystem_checkpoint_write_retry_context,
    bind_filesystem_checkpoint_receipt_to_submitted_action,
    filesystem_checkpoint_failure_reason,
    filesystem_checkpoint_read_failure_reason,
    filesystem_checkpoint_read_observed,
    filesystem_checkpoint_write_succeeded,
)
from .literesearcher import LiteResearcherEnvClient
from .verl_qwen_tool_parser import (
    QWEN_INVALID_ACTION_SENTINEL,
    QWEN_SINGLE_TOOL_CALL_CONTRACT,
    classify_qwen_tool_call_rejection,
    collect_clean_multi_qwen_tool_calls,
    parse_single_qwen3_tool_call,
)

AGENTGENERAL_COMPACTION_CONTRACT = "policy_filesystem_checkpoint_then_client_replace_v2"
AGENTGENERAL_MEMORY_CONTRACT = AGENTGENERAL_COMPACTION_CONTRACT

AGENTGENERAL_TOOLS_CONTRACT = (
    "Workspace bash takes exactly one parameter: command. Every command "
    "already runs from the workspace root, so use workspace-relative paths "
    "and no cd.\n"
    "Put multi-line file content in one quoted here-document: append with "
    "`cat >> path <<'EOF'` and overwrite with `cat > path <<'EOF'`, placing "
    "every pending line in the same block instead of one line per call. Do "
    "not assemble multi-line text with inline printf or echo arguments.\n"
    "Chaining with `&&` or `||` inside one command is allowed; prefer "
    "write-then-read-back verification."
)


_TC_OPEN = "<tool" + "_call>"
_TC_CLOSE = "</tool" + "_call>"

_BASH_EXAMPLE = (
    _TC_OPEN + "\n<function=bash>\n<parameter=command>\n"
    "ls -la\n"
    "</parameter>\n</function>\n" + _TC_CLOSE
)
_BASH_WRITE_EXAMPLE = (
    _TC_OPEN + "\n<function=bash>\n<parameter=command>\n"
    "cat >> notes.md <<'EOF'\nConfirmed finding: example value\nEOF\n"
    "</parameter>\n</function>\n" + _TC_CLOSE
)
_FINISH_EXAMPLE = (
    _TC_OPEN + "\n<function=finish>\n<parameter=answer>\n"
    "Final answer with the requested fields.\n"
    "</parameter>\n</function>\n" + _TC_CLOSE
)

_MCP_EXAMPLE = (
    _TC_OPEN + "\n<function=mcp__service__tool>\n<parameter=argument>\n"
    "value-from-the-task\n"
    "</parameter>\n</function>\n" + _TC_CLOSE
)
_MCP_NOARG_EXAMPLE = (
    _TC_OPEN + "\n<function=mcp__service__tool>\n</function>\n" + _TC_CLOSE
)

_AGENTGENERAL_DUAL_EXAMPLE = (
    _TC_OPEN + "\n<function=bash>\n<parameter=command>\n"
    "find . -maxdepth 1 -type f | head -20\n"
    "</parameter>\n</function>\n" + _TC_CLOSE + "\n"
    + _TC_OPEN + "\n<function=bash>\n<parameter=command>\n"
    "cat " + FILESYSTEM_CHECKPOINT_PATH + "\n"
    "</parameter>\n</function>\n" + _TC_CLOSE
)

AGENTGENERAL_SYSTEM_PROMPT = (
    QWEN_SINGLE_TOOL_CALL_CONTRACT
    + "\n"
    + AGENTGENERAL_TOOLS_CONTRACT
    + " Reasoning belongs inside think tags before the tool call.\n\n"
) + f"""
You are working on an open-ended task inside a persistent workspace. The task
message lists every tool available for the current task: the fixed workspace
tool (bash), possibly task-specific MCP tools, and the finish tool. Call
any listed tool by its exact name. The workspace persists for the whole
episode, so files you write survive every context compaction.

For a workspace command, use this complete form:

{_BASH_EXAMPLE}

For a multi-line file write, use one bash call with a quoted here-document:

{_BASH_WRITE_EXAMPLE}

For a task-specific MCP tool listed in the task message (signatures look
like mcp__service__tool(argument: type), where a trailing * marks a
required argument), call it with the same envelope grammar as bash, with
one parameter block per argument you supply and every required argument
included, using the exact tool name and argument names from the listing:

{_MCP_EXAMPLE}

An MCP tool listed with no arguments takes no parameter blocks:

{_MCP_NOARG_EXAMPLE}

When the task is fully completed, call finish with your final answer so it is
submitted for grading:

{_FINISH_EXAMPLE}

Your continuing memory lives in {FILESYSTEM_CHECKPOINT_PATH}: when the
conversation is compacted, write the checkpoint exactly as requested, then
read it back with one bash call when instructed.

The episode's turn budget is measured in policy responses: every response
spends exactly one turn, however many tool calls it carries, and the task's
opening message states how many turns the episode has. When several
independent commands are useful together, emit them as consecutive
envelopes in the same response, for example:

{_AGENTGENERAL_DUAL_EXAMPLE}
"""

AGENTGENERAL_CONTEXT_COMPACTION_REQUEST = (
    FILESYSTEM_CHECKPOINT_REQUEST
    + " For this task, preserve the objective, verified findings with their "
    "sources or file paths, open uncertainties, and the next concrete action."
)

AGENTGENERAL_POLICY_CONTINUATION_MARKER = (
    "The earlier conversation was compacted into the workspace checkpoint.\n"
    "Output exactly this command-only Qwen XML action and no other text:\n\n"
    + _TC_OPEN + "\n<function=bash>\n<parameter=command>\n"
    "cat " + FILESYSTEM_CHECKPOINT_PATH + "\n"
    "</parameter>\n</function>\n" + _TC_CLOSE
)

AGENTGENERAL_POLICY_WRITE_RETRY_MARKER = (
    "The continuation checkpoint write has not been accepted yet, so no "
    "earlier conversation was removed and the current context is still "
    "present. Retry the checkpoint write exactly as described above; "
    "reading the checkpoint file cannot replace the required write."
)

_AGENTGENERAL_QWEN_TOOL_SCHEMAS = (
    {
        "type": "function",
        "function": {
            "name": "bash",
            "description": "Executes a given bash command in the workspace and returns its output.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "The bash command to run."}
                },
                "required": ["command"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "Read",
            "description": "Reads a file from the workspace filesystem.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "The file to read."}
                },
                "required": ["file_path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "Write",
            "description": "Writes a file to the workspace filesystem.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "The target path."},
                    "content": {"type": "string", "description": "The full file content."},
                },
                "required": ["file_path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "Edit",
            "description": "Performs an exact string replacement in a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "The file to edit."},
                    "old_string": {"type": "string", "description": "Text to replace."},
                    "new_string": {"type": "string", "description": "Replacement text."},
                },
                "required": ["file_path", "old_string", "new_string"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "Grep",
            "description": "Searches file contents with a ripgrep pattern.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "The regex to search for."}
                },
                "required": ["pattern"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "Glob",
            "description": "Finds files by glob pattern.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "The glob pattern."}
                },
                "required": ["pattern"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "finish",
            "description": (
                "Submit the final answer for grading and end the episode."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "answer": {
                        "type": "string",
                        "description": "The final answer text.",
                    }
                },
            },
        },
    },
)


_AGENTGENERAL_DECLARED_TOOL_NAMES = frozenset({"bash", "finish"})

_FUNCTION_LINE_RE = None


def _agentgeneral_raw_function_name(action: str) -> str | None:

    global _FUNCTION_LINE_RE
    import re

    text = action.strip()
    if text.count(_TC_OPEN) != 1 or text.count(_TC_CLOSE) != 1:
        return None
    if _FUNCTION_LINE_RE is None:
        _FUNCTION_LINE_RE = re.compile(r"<function=([A-Za-z0-9_.-]+)>")
    match = _FUNCTION_LINE_RE.search(text)
    return match.group(1) if match is not None else None


def normalize_agentgeneral_policy_action(
    action: str,
) -> tuple[str, dict[str, Any]]:

    parsed = parse_single_qwen3_tool_call(
        action, tool_schemas=_AGENTGENERAL_QWEN_TOOL_SCHEMAS
    )
    if parsed is not None:
        submitted = _render_canonical_agentgeneral_call(parsed.name, parsed.arguments)
        evidence = {
            "normalizer": "agentgeneral_schema_v1",
            "function_name": parsed.name,
        }
        return submitted, evidence
    multi_names = collect_clean_multi_qwen_tool_calls(action)
    if multi_names is not None:
        return action.strip(), {
            "normalizer": "agentgeneral_multi_v1",
            "function_names": multi_names,
        }
    raw_name = _agentgeneral_raw_function_name(action)
    if raw_name is not None and raw_name not in {"bash", "Read", "Write", "Edit", "Grep", "Glob", "finish"}:
        return action.strip(), {
            "normalizer": "agentgeneral_mcp_passthrough_v1",
            "function_name": raw_name,
        }
    reason = classify_qwen_tool_call_rejection(action) or (
        "expected_exactly_one_qwen_xml_tool_call"
    )
    return QWEN_INVALID_ACTION_SENTINEL, {
        "normalizer": "agentgeneral_invalid_v1",
        "tool_parser_error": reason,
    }


def _render_canonical_agentgeneral_call(
    name: str, arguments: Mapping[str, Any]
) -> str:
    import json as _json

    lines = [_TC_OPEN, f"<function={name}>"]
    for key, value in arguments.items():
        if isinstance(value, str):
            text = value
        else:
            text = _json.dumps(value, ensure_ascii=False)
        lines.append(f"<parameter={key}>")
        lines.append(text)
        lines.append("</parameter>")
    lines.append("</function>")
    lines.append(_TC_CLOSE)
    return "\n".join(lines)


class AgentGeneralEnvClient(LiteResearcherEnvClient):


    _system_prompt = AGENTGENERAL_SYSTEM_PROMPT


    _POLICY_BUDGET_FOOTER_LABEL = "AgentGeneral"

    @property
    def conversation_start(self):
        from camg.controller.types import ConversationMessage

        return (
            ConversationMessage(
                {"from": "human", "loss": None, "value": self._system_prompt}
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
        **kwargs,
    ) -> None:


        from camg.controller import BaseEnvClient

        BaseEnvClient.__init__(self, *args, **kwargs)
        self.env_server_base = env_server_base.rstrip("/")
        self.timeout = timeout
        self.invalid_action_reward = 0.0
        self.invalid_action_budget = None
        self._exploration_milestones = {}
        metadata = self._request("GET", "metadata")
        if metadata.get("domain_id") != "agentgeneral":
            raise RuntimeError(
                "AgentGeneral endpoint reports the wrong domain"
            )
        if metadata.get("compaction_contract") != AGENTGENERAL_COMPACTION_CONTRACT:
            raise RuntimeError(
                "AgentGeneral endpoint reports the wrong compaction contract"
            )
        max_policy_steps = metadata.get("max_policy_steps")
        if type(max_policy_steps) is not int or max_policy_steps <= 0:
            raise RuntimeError("AgentGeneral endpoint reports invalid max_policy_steps")
        if metadata.get("max_policy_steps_enforced_by") != "shared_policy_runner":
            raise RuntimeError(
                "AgentGeneral endpoint reports the wrong policy-step owner"
            )
        prompt_policy_turns = metadata.get("prompt_policy_turns", max_policy_steps)
        if type(prompt_policy_turns) is not int or prompt_policy_turns <= 0:
            raise RuntimeError("AgentGeneral endpoint reports invalid prompt_policy_turns")
        if prompt_policy_turns > max_policy_steps:
            raise RuntimeError("AgentGeneral endpoint reports prompt turns above the action cap")
        self.max_policy_steps = prompt_policy_turns
        self._policy_action_headroom = max_policy_steps
        task_count = int(metadata["task_count"])
        if data_len is not None and int(data_len) > task_count:
            raise ValueError(
                f"AgentGeneral data_len {data_len} exceeds task_count {task_count}"
            )
        self.data_len = task_count if data_len is None else int(data_len)
        created = self._request("POST", "create", json={})
        self.env_id = int(created["id"])
        self.info = created
        self.metadata = metadata
        self._reset_policy_transition_state()


    def policy_framing(self) -> list[dict[str, str]]:
        return [{"role": "system", "content": self._system_prompt}]

    def policy_tool_schemas(self) -> list[dict[str, Any]]:


        return deepcopy(
            [
                schema
                for schema in _AGENTGENERAL_QWEN_TOOL_SCHEMAS
                if schema["function"]["name"]
                in _AGENTGENERAL_DECLARED_TOOL_NAMES
            ]
        )

    def normalize_initial_policy_context(
        self,
        messages: Sequence[Mapping[str, str]],
    ) -> list[dict[str, str]]:
        normalized = self._copy_policy_messages_public(messages)
        if not normalized or normalized[-1]["role"] != "user":
            raise ValueError(
                "AgentGeneral initial policy context must end with the task"
            )
        observation = str(self.observe())
        if normalized[-1]["content"] != observation:
            raise ValueError(
                "AgentGeneral initial policy context does not end with the current task"
            )
        return self.policy_framing() + [{"role": "user", "content": observation}]

    @staticmethod
    def _copy_policy_messages_public(
        messages: Sequence[Mapping[str, str]],
    ) -> list[dict[str, str]]:
        from .swesmith import _copy_policy_messages

        return _copy_policy_messages(messages)


    def begin_policy_turn(self, turn_index: int, turn_budget: int) -> None:


        self._policy_turn_index = int(turn_index)
        self._policy_turn_budget = int(turn_budget)

    def policy_turn_candidate(self) -> str | None:
        if not self._policy_context_bound or self._pending_checkpoint_read is not None:
            return None
        return AGENTGENERAL_CONTEXT_COMPACTION_REQUEST

    def prepare_policy_turn(self, pressure) -> str | None:


        from .literesearcher import LITERESEARCHER_CONTEXT_COMPACTION_REQUEST

        selected = super().prepare_policy_turn(pressure)
        if selected is None:
            return None
        if selected == LITERESEARCHER_CONTEXT_COMPACTION_REQUEST:
            return AGENTGENERAL_CONTEXT_COMPACTION_REQUEST
        return selected

    def _policy_continuation_marker(self) -> str:
        return AGENTGENERAL_POLICY_CONTINUATION_MARKER + self._policy_budget_footer()

    def _policy_write_retry_marker(self) -> str:
        return AGENTGENERAL_POLICY_WRITE_RETRY_MARKER + self._policy_budget_footer()

    def _policy_budget_footer(self) -> str:


        line = self._policy_budget_footer_line()
        return f" {line}" if line else ""

    def _policy_budget_footer_line(self) -> str:


        if self._policy_turn_budget is not None:
            used = self._policy_turn_index + 1
            remaining = max(0, self._policy_turn_budget - used)
            if remaining <= 1:


                return (
                    f"[{self._POLICY_BUDGET_FOOTER_LABEL} "
                    "FINAL TURN: your next response is the last action of "
                    "this episode; there is no next turn. Anything not "
                    "submitted in this response earns no credit, so do "
                    "not verify, do not edit, and do not call any other "
                    "tool. Call the finish tool now with your best "
                    "current answer: an imperfect answer submitted now "
                    "scores higher than a better answer that is never "
                    "submitted.]"
                )
            return (
                f"[{self._POLICY_BUDGET_FOOTER_LABEL} turn budget: "
                f"turn {used} of {self._policy_turn_budget}; "
                f"{remaining} turns remain.]"
            )
        used = self._policy_step_count
        remaining = max(0, self.max_policy_steps - used)
        return (
            f"[{self._POLICY_BUDGET_FOOTER_LABEL} policy budget: "
            f"step {used} of {self.max_policy_steps}; "
            f"{remaining} steps remain.]"
        )

    def _policy_budget_observation_footer(self) -> str:


        if self._policy_turn_budget is None:
            return ""
        return f"\n\n{self._policy_budget_footer_line()}"


    def _step_native_policy_action(self, action: str) -> StepOutput:
        native_before = self._native_call_count
        policy_before = self._policy_step_count
        context_before = self._context_epoch
        checkpoint_read_pending_before = self._pending_checkpoint_read
        checkpoint_read_framing_before = self._pending_checkpoint_read_framing
        submitted_action, parser_evidence = (
            normalize_agentgeneral_policy_action(action)
        )
        response = self._request(
            "POST",
            "step",
            json={"id": self.env_id, "action": submitted_action},
        )
        self._native_call_count += 1
        self._policy_step_count += 1
        self.info = response
        response_info = response.get("info", {})
        action_submission: dict[str, Any] = {
            "raw_policy_output": action,
            "submitted_action": submitted_action,
            **parser_evidence,
        }
        server_wrapper = (
            response_info.get("wrapper_evidence", {})
            if isinstance(response_info, Mapping)
            else {}
        )
        native_reward = float(response["reward"])
        if not math.isfinite(native_reward):
            raise RuntimeError("AgentGeneral endpoint returned a non-finite reward")
        reward = native_reward
        wrapper_evidence: dict[str, Any] = {
            "event": "native_action",
            "server_wrapper_evidence": (
                dict(server_wrapper) if isinstance(server_wrapper, Mapping) else {}
            ),
        }
        if submitted_action == QWEN_INVALID_ACTION_SENTINEL:
            wrapper_evidence["invalid_action"] = True
            wrapper_evidence["tool_parser_error"] = parser_evidence.get(
                "tool_parser_error"
            )
        read_receipt = None
        if isinstance(server_wrapper, Mapping):
            read_receipt = server_wrapper.get("filesystem_checkpoint_read")
            if filesystem_checkpoint_read_observed(read_receipt):
                wrapper_evidence.update(
                    {
                        "memory_event": "read",
                        "document_read_observed": True,
                        "filesystem_checkpoint_read": dict(read_receipt),
                    }
                )
            else:
                changed_paths = server_wrapper.get("workspace_changed_paths")
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
                if (
                    server_wrapper.get("workspace_action_completed") is True
                    and noncheckpoint_paths
                ):
                    wrapper_evidence.update(
                        {
                            "memory_event": "modify",
                            "workspace_change_observed": True,
                            "workspace_changed_paths": noncheckpoint_paths,
                        }
                    )
                elif (
                    server_wrapper.get("workspace_action_completed") is True
                    and str(server_wrapper.get("workspace_op", "")).upper()
                    == "BASH"
                ):
                    wrapper_evidence.update(
                        {
                            "memory_event": "execute",
                            "outcome": "success",
                            "execution_completed_observed": True,
                        }
                    )
        read_satisfied = False
        read_failure_reason = None
        read_retry_budget_exhausted = False
        if getattr(self, "_policy_turn_budget", None) is not None:
            remaining_actions = self._policy_turn_budget - self._policy_turn_index - 1
        else:
            remaining_actions = self.max_policy_steps - self._policy_step_count
        if checkpoint_read_pending_before is not None:
            read_failure_reason = filesystem_checkpoint_read_failure_reason(
                read_receipt,
                checkpoint_read_pending_before,
            )
            read_satisfied = read_failure_reason is None
            read_retry_budget_exhausted = bool(
                not read_satisfied
                and not bool(response["done"])
                and remaining_actions < 2
            )
            wrapper_evidence.update(
                {
                    "checkpoint_read_required": True,
                    "checkpoint_read_satisfied": read_satisfied,
                    "checkpoint_read_retry_pending": bool(
                        not read_satisfied
                        and not bool(response["done"])
                        and not read_retry_budget_exhausted
                    ),
                    "checkpoint_read_failure_reason": read_failure_reason,
                    "checkpoint_read_expected_size_bytes": (
                        checkpoint_read_pending_before.get("size_bytes")
                    ),
                    "checkpoint_read_expected_sha256": (
                        checkpoint_read_pending_before.get("sha256")
                    ),
                    "checkpoint_read_retry_budget_exhausted": (
                        read_retry_budget_exhausted
                    ),
                    "checkpoint_read_retry_remaining_actions": remaining_actions,
                }
            )
            if (
                read_satisfied
                or bool(response["done"])
                or read_retry_budget_exhausted
            ):
                self._pending_checkpoint_read = None
                self._pending_checkpoint_read_framing = None
        context_transition = None
        if (
            checkpoint_read_pending_before is not None
            and not read_satisfied
            and not bool(response["done"])
            and not read_retry_budget_exhausted
        ):
            if checkpoint_read_framing_before is None:
                raise RuntimeError(
                    "AgentGeneral pending checkpoint read lost its trusted framing"
                )
            read_retry_messages = build_post_checkpoint_read_retry_context(
                checkpoint_read_framing_before,
                checkpoint_read_pending_before,
                read_failure_reason or "checkpoint_read_not_observed",
                continuation_marker=self._policy_continuation_marker(),
            )
            if submitted_action == QWEN_INVALID_ACTION_SENTINEL:
                read_retry_messages = _append_rejected_reason_public(
                    read_retry_messages,
                    parser_evidence.get("tool_parser_error"),
                )
            context_transition = build_task_neutral_context_transition(
                CONTEXT_OPERATION_REPLACE,
                messages=read_retry_messages,
            )
        returned_env_info = dict(response_info)
        policy_state = str(response["observation"])
        policy_state += self._policy_budget_observation_footer()
        terminal = bool(response["done"])
        return StepOutput(
            state=policy_state,
            reward=reward,
            done=terminal,
            info=build_task_neutral_transition_info(
                env_info=returned_env_info,
                action_submission=action_submission,
                native_step_before=native_before,
                native_step_after=self._native_call_count,
                native_call_count_before=native_before,
                native_call_count_after=self._native_call_count,
                context_epoch_before=context_before,
                context_epoch_after=self._context_epoch,
                session_epoch_before=0,
                session_epoch_after=0,
                policy_step_before=policy_before,
                policy_step_after=self._policy_step_count,
                context_transition=context_transition,
                wrapper_evidence=wrapper_evidence,
            ),
        )


    def finalize_policy_horizon(self) -> StepOutput:

        response = self._request(
            "POST", "horizon", json={"id": self.env_id}
        )
        self.info = response
        env_info = dict(response.get("info", {}))
        env_info.setdefault("status", "max_policy_steps_exhausted")
        return StepOutput(
            state=str(response.get("observation", "")),
            reward=float(response.get("reward", 0.0)),
            done=True,
            info=build_task_neutral_transition_info(
                env_info=env_info,
                action_submission={"control_action": "horizon"},
                native_step_before=self._native_call_count,
                native_step_after=self._native_call_count,
                native_call_count_before=self._native_call_count,
                native_call_count_after=self._native_call_count,
                context_epoch_before=self._context_epoch,
                context_epoch_after=self._context_epoch,
                session_epoch_before=0,
                session_epoch_after=0,
                policy_step_before=self._policy_step_count,
                policy_step_after=self._policy_step_count,
                wrapper_evidence={
                    "event": "horizon_finalization",
                    "outcome": "max_rounds",
                },
            ),
        )

    def close(self) -> dict[str, Any]:
        return self._request("POST", "close", json={"id": self.env_id})


def _append_rejected_reason_public(messages, reason):
    from .literesearcher import _append_rejected_reason_to_messages

    return _append_rejected_reason_to_messages(messages, reason)
