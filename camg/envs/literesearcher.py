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
    FILESYSTEM_CHECKPOINT_FAILURE_DETAIL_MAX_BYTES,
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
    extract_filesystem_checkpoint_failure_detail,
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
    classify_qwen_tool_call_rejection,
    parse_single_qwen3_tool_call,
)


LITERESEARCHER_MIN_OBSERVATION_TOKEN_ENVELOPE = 12_288

LITERESEARCHER_MIN_ACTIONS_FOR_CHECKPOINT_WRITE_READ_ANSWER = 3


_LITERESEARCHER_QWEN_TOOL_SCHEMAS = (
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": "Search the released web corpus.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["query"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "visit",
            "description": "Visit one URL returned by search.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string"},
                    "goal": {"type": "string"},
                    "page": {"type": "integer", "minimum": 1},
                },
                "required": ["url", "goal"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "bash",
            "description": "Run one networkless workspace command.",
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
    {
        "type": "function",
        "function": {
            "name": "answer",
            "description": "Return the final evidence-backed answer and terminate.",
            "parameters": {
                "type": "object",
                "properties": {"answer": {"type": "string"}},
                "required": ["answer"],
                "additionalProperties": False,
            },
        },
    },
)


LITERESEARCHER_QWEN_XML_CHECKPOINT_GUIDANCE = """

For this context-boundary write, use bash.
Output exactly the command-only Qwen XML call below, replacing the placeholder
lines with the current research state. Add no optional parameters or extra XML
tags.

<tool_call>
<function=bash>
<parameter=command>
mkdir -p .agent_memory && cat > .agent_memory/CONTINUATION.md <<'EOF'
Objective: ...
Evidence and source URLs: ...
Uncertainty: ...
Next action: ...
EOF
</parameter>
</function>
</tool_call>
"""

LITERESEARCHER_EXACT_CHECKPOINT_READ_ACTION = """<tool_call>
<function=bash>
<parameter=command>
cat .agent_memory/CONTINUATION.md
</parameter>
</function>
</tool_call>"""

LITERESEARCHER_CONTEXT_COMPACTION_REQUEST = (
    FILESYSTEM_CHECKPOINT_REQUEST
    + LITERESEARCHER_QWEN_XML_CHECKPOINT_GUIDANCE
    + " For this research task, preserve the unresolved question, decisive "
    "evidence with source URLs, conflicts or uncertainty, and the next search "
    "or visit action."
)

LITERESEARCHER_POLICY_CONTINUATION_MARKER = (
    FILESYSTEM_CHECKPOINT_CONTINUATION_MARKER
    + "\nOutput exactly this command-only Qwen XML action and no other text:\n\n"
    + LITERESEARCHER_EXACT_CHECKPOINT_READ_ACTION
)


LITERESEARCHER_POLICY_WRITE_RETRY_MARKER = (
    "The continuation checkpoint write has not been accepted yet, so no "
    "earlier conversation was removed and the current context is still "
    "present. Retry the checkpoint write exactly as described above; "
    "reading the checkpoint file cannot replace the required write."
)


LITERESEARCHER_SYSTEM_PROMPT = (
    QWEN_SINGLE_TOOL_CALL_CONTRACT
    + "\n"
    + WORKSPACE_SHELL_CONTRACT
    + " Plain-prose narration before the tool call is allowed.\n\n"
) + """
Use only functions from the native Tools section above. Never mix the native Qwen XML envelope with a bare Codex-style action.

For a search, use this complete form. The query value MUST be a JSON array
containing exactly one non-empty string, never a bare string and never
multiple entries - the backend joins multiple entries with spaces into one
query, so they do not produce separate searches:

<tool_call>
<function=search>
<parameter=query>
["single focused search query"]
</parameter>
</function>
</tool_call>

When several independent searches would each add evidence, emit them as
consecutive envelopes in the same response, for example:

<tool_call>
<function=search>
<parameter=query>
["first focused search query"]
</parameter>
</function>
</tool_call>
<tool_call>
<function=search>
<parameter=query>
["second focused search query"]
</parameter>
</function>
</tool_call>

For a visit, use this complete form. Replace the URL with one copied verbatim
from a search result; never invent, reconstruct, shorten, or edit a URL:

<tool_call>
<function=visit>
<parameter=url>
URL_COPIED_VERBATIM_FROM_A_SEARCH_RESULT
</parameter>
<parameter=goal>
specific evidence to find on that page
</parameter>
<parameter=page>
1
</parameter>
</function>
</tool_call>

For a workspace shell action, use this complete form:

<tool_call>
<function=bash>
<parameter=command>
cat .agent_memory/research.md
</parameter>
</function>
</tool_call>

For a workspace file edit, use one bash with a quoted here-document:
<tool_call>
<function=bash>
<parameter=command>
cat >> .agent_memory/research.md <<'EOF'
Question, evidence, source URLs, and next steps.
EOF</parameter>
</function>
</tool_call>
Your available action kinds are limited to search, visit, bash, and answer.
Required parameters must be present. Emit no text after a function call. Do not
put quotation marks around parameter names. Do not emit bare bash
syntax outside the XML envelope.

You are a research agent working on one continuous question. Your response channel is an action parser, not a chat channel. Reason in plain prose before each tool call. Answer as soon as the evidence is sufficient instead of searching further. Copy each visit URL exactly from a search result. A visit returns one bounded page; follow next_page with the same URL and goal when needed. A visit returns one bounded page in stable document order; page numbers are stable coordinates, so next_page with the same URL reads further into the same document. Every observation footer carries a line of the form [LR policy budget: turn N of 40; R turns remain.]. Turn 40 reached without an answer is a hard terminal that scores zero: when the remaining turns get low and the evidence is sufficient, submit the answer instead of running one more search. On the final turn, always submit your best answer — an unanswered terminal scores zero, a guessed answer can score.

An empty episode-private workspace persists across context compaction. Use files when evidence or a continuation plan should survive a long interaction.
At an explicit context-boundary request, use one normal bash tool call to overwrite `.agent_memory/CONTINUATION.md`; only a verified non-empty write allows old messages to be removed. After replacement, read that file through a normal bash tool call before continuing. Other workspace files remain available for voluntary notes at any time. """ + FILESYSTEM_CHECKPOINT_LONG_LIVED_MEMORY_NOTICE + """

When evidence is sufficient, use this complete final form and replace the text
with the evidence-backed answer:
<tool_call>
<function=answer>
<parameter=answer>your evidence-backed answer</parameter>
</function>
</tool_call>

Independent calls may share one response as consecutive envelopes; a call that depends on an earlier result must wait for that result's observation."""

def _literesearcher_invalid_qwen_action(reason: str) -> tuple[str, dict[str, Any]]:
    return QWEN_INVALID_ACTION_SENTINEL, {
        "tool_contract": "qwen3_xml_single_call_v1",
        "tool_parser": "qwen3_coder",
        "tool_parser_normalized": False,
        "tool_parser_error": reason,
        "submitted_action": QWEN_INVALID_ACTION_SENTINEL,
    }


def _qwen_xml_parameter(name: str, value: str) -> str:
    return f"<parameter={name}>\n{value}\n</parameter>"


def _canonical_literesearcher_domain_xml(
    name: str,
    arguments: Mapping[str, Any],
) -> str:
    parameters: list[str] = []
    if name == "search":
        parameters.append(
            _qwen_xml_parameter(
                "query",
                json.dumps(arguments["query"], ensure_ascii=False),
            )
        )
    elif name == "visit":


        parameters.extend(
            [
                _qwen_xml_parameter(
                    "url", json.dumps(arguments["url"], ensure_ascii=False)
                ),
                _qwen_xml_parameter(
                    "goal", json.dumps(arguments["goal"], ensure_ascii=False)
                ),
            ]
        )
        if "page" in arguments:
            parameters.append(_qwen_xml_parameter("page", str(arguments["page"])))
    else:
        raise ValueError(f"unsupported LiteResearcher domain function: {name}")
    return (
        "<tool_call>\n"
        f"<function={name}>\n"
        + "\n".join(parameters)
        + "\n</function>\n</tool_call>"
    )


_INVALID_ACTION_REASON_GUIDANCE = {
    "search query must be a non-empty string array": (
        "For the search tool the query parameter must be a JSON array of one "
        "or more quoted strings, for example a query parameter value of: "
        '["first search query", "second search query"]. Plain-text queries '
        "are rejected."
    ),
    "search requires exactly query": (
        "For the search tool provide exactly one parameter named query, "
        "whose value is a JSON array of quoted strings, for example: "
        '["first search query", "second search query"].'
    ),
    "visit requires url and goal, with optional page": (
        "For the visit tool provide url and goal parameters, with the url "
        "copied exactly from a search result; page is optional."
    ),
    "expected_complete_qwen_xml_tool_call": (
        "Emit each tool call as one complete envelope with no extra text "
        "around it, and make every parameter value valid JSON; the search "
        "query must be a JSON array of quoted strings such as: "
        '["first search query", "second search query"].'
    ),


    "qwen_xml_think_tag_in_response": (
        "The response contained think-tag markers. Do the reasoning in "
        "plain prose before the tool call instead: the action channel "
        "accepts plain text plus one or more complete Qwen XML tool calls, never "
        "think tags."
    ),
    "qwen_xml_reserved_tag_in_response": (
        "The response used the reserved <answer> envelope outside the tool "
        "call. Submit answers only through the answer function's Qwen XML "
        "form with the answer text inside its parameter, and never place "
        "</answer> or other envelope tags inside parameter values."
    ),
    "qwen_xml_tool_call_fence_miscounted": (
        "The response opened or closed a tool-call fence without a "
        "complete function call inside. Emit every call as a complete "
        "envelope: one opening fence, one complete function call, one "
        "closing fence, and nothing after the last one."
    ),
    "answer contains a reserved closing tag": (
        "The answer parameter must not contain the reserved closing tag "
        "</answer>: write the answer text itself inside the parameter and "
        "let the client add the envelope around it."
    ),
}


def _invalid_action_feedback(generic_observation, reason):

    if not reason:
        return generic_observation
    guidance = _INVALID_ACTION_REASON_GUIDANCE.get(str(reason))
    parts = [str(generic_observation).rstrip(), " Rejected because: ", str(reason), "."]
    if guidance:
        parts.extend((" ", guidance))
    return "".join(parts)


def _append_rejected_reason_to_messages(messages, reason):

    rewritten = [dict(message) for message in messages]
    if not reason:
        return rewritten
    for message in reversed(rewritten):
        if message.get("role") == "user":
            guidance = _INVALID_ACTION_REASON_GUIDANCE.get(str(reason))
            parts = [
                str(message.get("content", "")).rstrip(),
                " Rejected because: ",
                str(reason),
                ".",
            ]
            if guidance:
                parts.extend((" ", guidance))
            message["content"] = "".join(parts)
            break
    return rewritten


_SEARCH_ENVELOPE_RE = re.compile(
    r"<function=search>(?P<body>.*?)</function>", re.DOTALL
)
_SEARCH_QUERY_PARAMETER_CLOSED_RE = re.compile(
    r"<parameter=query>(?P<value>.*?)</parameter>", re.DOTALL
)


def _literesearcher_raw_search_query_text(action: Any) -> str | None:


    if not isinstance(action, str):
        return None
    text = action.strip()
    if not text:
        return None
    if (
        text.count("<function=") != 1
        or text.count("</function>") != 1
        or "<function=search>" not in text
        or text.count("<parameter=") != 1
        or text.count("<parameter=query>") != 1
    ):
        return None
    envelope = _SEARCH_ENVELOPE_RE.search(text)
    if envelope is None:
        return None
    body = envelope.group("body")
    closed = _SEARCH_QUERY_PARAMETER_CLOSED_RE.search(body)
    if closed is not None:
        return closed.group("value").strip()
    if "</parameter>" in body:
        return None


    _, separator, value = body.partition("<parameter=query>")
    if not separator:
        return None
    return value.strip()


def _valid_literesearcher_search_query(value: Any) -> bool:
    return bool(
        isinstance(value, list)
        and value
        and all(
            isinstance(item, str) and item.strip()
            for item in value
        )
    )


def _recover_literesearcher_search_query(
    raw_text: str | None,
) -> tuple[list[str], str] | None:


    if not isinstance(raw_text, str):
        return None
    text = raw_text.strip()
    if not text:
        return None


    for layer, candidate in (
        ("json_array", text),
        ("trailing_comma_stripped", text.rstrip().rstrip(",")),
    ):
        try:
            value = json.loads(candidate)
        except (TypeError, ValueError):
            continue
        if _valid_literesearcher_search_query(value):
            return [item.strip() for item in value], layer
        if isinstance(value, str) and value.strip():
            return [value.strip()], layer

    return [text], "raw_text_single_query"


def normalize_literesearcher_policy_action(
    action: str,
) -> tuple[str, dict[str, Any]]:


    parsed = parse_single_qwen3_tool_call(
        action,
        tool_schemas=_LITERESEARCHER_QWEN_TOOL_SCHEMAS,
    )
    if parsed is None:


        return _literesearcher_invalid_qwen_action(
            classify_qwen_tool_call_rejection(action)
            or "expected_complete_qwen_xml_tool_call"
        )
    name = parsed.name
    arguments = dict(parsed.arguments)
    recovery_evidence: dict[str, Any] = {}
    try:
        if name == "search":
            if set(arguments) != {"query"}:
                raise ValueError("search requires exactly query")
            query = arguments["query"]
            if not _valid_literesearcher_search_query(query):


                recovered = _recover_literesearcher_search_query(
                    _literesearcher_raw_search_query_text(action)
                )
                if recovered is None:
                    raise ValueError(
                        "search query must be a non-empty string array"
                    )
                query, layer = recovered
                recovery_evidence["search_query_recovery"] = layer
            arguments = {"query": [item.strip() for item in query]}
            submitted = _canonical_literesearcher_domain_xml(name, arguments)
        elif name == "visit":
            required = {"url", "goal"}
            if not required <= set(arguments) or not set(arguments) <= required | {"page"}:
                raise ValueError("visit requires url and goal, with optional page")
            normalized_visit: dict[str, Any] = {}
            for key in ("url", "goal"):
                value = arguments[key]
                if not isinstance(value, str) or not value.strip():
                    raise ValueError(f"visit {key} must be a non-empty string")
                if value != value.strip():
                    raise ValueError(
                        f"visit {key} must not have leading or trailing whitespace"
                    )
                if (
                    len(value) >= 2
                    and value[0] == value[-1]
                    and value[0] in "\"'"
                ):


                    value = value[1:-1].strip()
                    if not value:
                        raise ValueError(
                            f"visit {key} must be a non-empty string"
                        )
                normalized_visit[key] = value
            if "page" in arguments:
                page = arguments["page"]
                if isinstance(page, bool) or not isinstance(page, int) or page < 1:
                    raise ValueError("visit page must be a positive integer")
                normalized_visit["page"] = page
            arguments = normalized_visit
            submitted = _canonical_literesearcher_domain_xml(name, arguments)
        elif name == "bash":
            allowed = {"command"}
            if "command" not in arguments or not set(arguments) <= allowed:
                raise ValueError(
                    "bash accepts only the command parameter; "
                    "remove workdir and timeout_ms"
                )
            command = arguments["command"]
            if not isinstance(command, str) or not command.strip():
                raise ValueError("bash command must be a non-empty string")
            normalized_shell: dict[str, Any] = {"command": command, "workdir": "."}
            if "workdir" in arguments:
                workdir = arguments["workdir"]
                if not isinstance(workdir, str) or not workdir.strip() or "\x00" in workdir:
                    raise ValueError("bash workdir must be a safe non-empty string")
                normalized_shell["workdir"] = workdir.strip()
            if "timeout_ms" in arguments:
                timeout_ms = arguments["timeout_ms"]
                if (
                    isinstance(timeout_ms, bool)
                    or not isinstance(timeout_ms, int)
                    or timeout_ms < 1
                ):
                    raise ValueError("bash timeout_ms must be a positive integer")
                normalized_shell["timeout_ms"] = timeout_ms
            submitted = "bash " + json.dumps(
                normalized_shell,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )
        elif name == "answer":
            if set(arguments) != {"answer"}:
                raise ValueError("answer requires exactly answer")
            answer = arguments["answer"]
            if not isinstance(answer, str) or not answer.strip():
                raise ValueError("answer must be a non-empty string")
            if (
                len(answer) >= 2
                and answer[0] == answer[-1]
                and answer[0] in "\"'"
            ):


                answer = answer[1:-1].strip()
                if not answer:
                    raise ValueError("answer must be a non-empty string")
            if "</answer>" in answer.lower():
                raise ValueError("answer contains a reserved closing tag")
            submitted = f"<answer>{answer.strip()}</answer>"
        else:
            raise ValueError(f"unsupported LiteResearcher function: {name}")
    except (TypeError, ValueError) as exc:
        return _literesearcher_invalid_qwen_action(str(exc))
    return submitted, {
        "tool_contract": "qwen3_xml_single_call_v1",
        "tool_parser": parsed.parser_name,
        "tool_parser_normalized": True,
        "submitted_action": submitted,
        **recovery_evidence,
    }


_EXPLORATION_MILESTONE_EVENTS = frozenset({"first_search", "first_visit"})


_ANSWER_INJECTION_MARKERS = (
    "judgment",
    "correct",
    "incorrect",
    "ignore previous",
    "ignore all",
    "as an ai",
    "evaluation assistant",
    "you must return",
    "json object",
    "labeled answer",
    "semantically equivalent",
)
_ANSWER_ENVELOPE_PREFIX = "<answer>"
_ANSWER_ENVELOPE_SUFFIX = "</answer>"


def _scan_answer_injection(answer_text: str) -> dict[str, Any]:
    lowered = answer_text.lower()
    markers_hit = sorted(
        marker for marker in _ANSWER_INJECTION_MARKERS if marker in lowered
    )
    return {
        "schema": "literesearcher_answer_injection_monitor_v1",
        "answer_length_chars": len(answer_text),
        "markers_hit": markers_hit,
        "flagged": bool(markers_hit),
    }


_CANONICAL_HEADER_TO_MILESTONE = {
    "<function=search>": "first_search",
    "<function=visit>": "first_visit",
}


_CANONICAL_DOMAIN_ACTION_FENCE = _canonical_literesearcher_domain_xml(
    "visit", {"url": "u", "goal": "g"}
).split("\n", 1)[0]


def _validate_exploration_milestones(
    value: Mapping[str, float] | None,
) -> dict[str, float]:
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise TypeError(
            "LiteResearcher exploration_milestones must be a mapping"
        )
    milestones: dict[str, float] = {}
    for key, reward in value.items():
        if key not in _EXPLORATION_MILESTONE_EVENTS:
            raise ValueError(
                "LiteResearcher exploration_milestones keys must be one of "
                f"{sorted(_EXPLORATION_MILESTONE_EVENTS)}, got {key!r}"
            )
        if (
            isinstance(reward, bool)
            or not isinstance(reward, (int, float))
            or not math.isfinite(float(reward))
            or float(reward) < 0.0
        ):
            raise ValueError(
                "LiteResearcher exploration milestone rewards must be "
                "finite and non-negative"
            )
        milestones[str(key)] = float(reward)
    return milestones


def _canonical_action_function_line(submitted_action: str) -> str | None:

    parts = submitted_action.split("\n", 2)
    if len(parts) < 3 or parts[0] != _CANONICAL_DOMAIN_ACTION_FENCE:
        return None
    header = parts[1]
    if header.startswith("<function=") and header.endswith(">"):
        return header
    return None


def _is_pure_checkpoint_read_submission(submitted_action: Any) -> bool:


    if not isinstance(submitted_action, str):
        return False
    text = submitted_action.strip()
    if not text.startswith("bash "):
        return False
    try:
        payload = json.loads(text[len("bash ") :])
    except (TypeError, ValueError):
        return False
    if not isinstance(payload, dict):
        return False
    if not set(payload) <= {"command", "workdir", "timeout_ms"}:
        return False
    command = payload.get("command")
    if not isinstance(command, str):
        return False
    return command.split() == ["cat", FILESYSTEM_CHECKPOINT_PATH]


def _literesearcher_checkpoint_failure_detail(
    execution: Any,
    native_observation: str,
) -> str:


    detail = extract_filesystem_checkpoint_failure_detail(execution)
    if detail:
        return detail
    if not isinstance(native_observation, str):
        return ""
    marker = native_observation.rfind("[stderr]")
    if marker < 0:
        return ""
    tail = native_observation[marker + len("[stderr]") :].strip()
    if not tail:
        return ""
    bounded = tail[-FILESYSTEM_CHECKPOINT_FAILURE_DETAIL_MAX_BYTES:]
    newline = bounded.find("\n")
    if 0 <= newline < len(bounded) // 2:
        bounded = bounded[newline + 1 :]
    return bounded.strip()


_LITERESEARCHER_MAX_REPLACEMENT_CHAR_RATIO = 0.001
_LITERESEARCHER_MAX_CONTROL_CHAR_RATIO = 0.01
_LITERESEARCHER_CORRUPT_PAGE_OBSERVATION = (
    "The page content for this request was rejected because too many of its "
    "characters were corrupted or non-printable, so its text is not usable. "
    "Continue with a different search result, page, or URL."
)
_CANONICAL_PAGE_FETCH_HEADERS = frozenset(
    {"<function=search>", "<function=visit>"}
)


def _literesearcher_observation_rejectably_corrupt(observation: str) -> bool:
    if not observation:
        return False
    length = len(observation)
    replacement_ratio = observation.count("\ufffd") / length
    if replacement_ratio > _LITERESEARCHER_MAX_REPLACEMENT_CHAR_RATIO:
        return True
    control_count = sum(
        1
        for char in observation
        if (ord(char) < 0x20 or ord(char) == 0x7F)
        and char not in "\t\n\r"
    )
    return control_count / length > _LITERESEARCHER_MAX_CONTROL_CHAR_RATIO


class LiteResearcherEnvClient(BaseEnvClient):


    conversation_start = (
        ConversationMessage(
            {
                "from": "human",
                "loss": None,
                "value": LITERESEARCHER_SYSTEM_PROMPT,
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
        invalid_action_budget: int | None = None,
        exploration_milestones: Mapping[str, float] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        if (
            isinstance(invalid_action_reward, bool)
            or not isinstance(invalid_action_reward, (int, float))
            or not math.isfinite(float(invalid_action_reward))
            or float(invalid_action_reward) > 0.0
        ):
            raise ValueError(
                "LiteResearcher invalid_action_reward must be finite and non-positive"
            )
        self.env_server_base = env_server_base.rstrip("/")
        self.timeout = timeout
        self.invalid_action_reward = float(invalid_action_reward)
        if invalid_action_budget is not None and (
            isinstance(invalid_action_budget, bool)
            or not isinstance(invalid_action_budget, int)
            or invalid_action_budget < 1
        ):
            raise ValueError(
                "LiteResearcher invalid_action_budget must be a positive "
                "integer or null"
            )
        self.invalid_action_budget = invalid_action_budget
        self._exploration_milestones = _validate_exploration_milestones(
            exploration_milestones
        )
        metadata = self._request("GET", "metadata")
        if metadata.get("domain_id") != "literesearcher":
            raise RuntimeError("LiteResearcher endpoint reports the wrong domain")
        if (
            metadata.get("compaction_contract")
            != "policy_filesystem_checkpoint_then_client_replace_v2"
        ):
            raise RuntimeError("LiteResearcher endpoint reports the wrong compaction contract")
        max_policy_steps = metadata.get("max_policy_steps")
        if type(max_policy_steps) is not int or max_policy_steps <= 0:
            raise RuntimeError("LiteResearcher endpoint reports invalid max_policy_steps")
        if metadata.get("max_policy_steps_enforced_by") != "shared_policy_runner":
            raise RuntimeError(
                "LiteResearcher endpoint reports the wrong policy-step owner"
            )
        self.max_policy_steps = max_policy_steps
        task_count = int(metadata["task_count"])
        if data_len is not None and int(data_len) > task_count:
            raise ValueError(
                f"LiteResearcher data_len {data_len} exceeds task_count {task_count}"
            )
        self.data_len = task_count if data_len is None else int(data_len)
        created = self._request("POST", "create", json={})
        self.env_id = int(created["id"])
        self.info = created
        self.metadata = metadata
        self._reset_policy_transition_state()

    def _reset_policy_transition_state(self) -> None:
        self._policy_step_count = 0
        self._policy_turn_index = 0
        self._policy_turn_budget: int | None = None
        self._invalid_action_total = 0
        self._checkpoint_write_failure_total = 0
        self._native_call_count = 0
        self._context_epoch = 0
        self._exploration_milestones_paid: set[str] = set()
        self._immutable_policy_context: list[dict[str, str]] | None = None
        self._current_policy_context: list[dict[str, str]] | None = None
        self._policy_context_bound = False
        self._selected_policy_control: str | None = None
        self._checkpoint_retry_pending = False
        self._checkpoint_write_retry_framing: list[dict[str, str]] | None = None
        self._pending_checkpoint_read: dict[str, Any] | None = None
        self._pending_checkpoint_read_framing: list[dict[str, str]] | None = None

    def __len__(self) -> int:
        return self.data_len

    def observe(self) -> str:
        return str(self.info["observation"])

    @property
    def sample_excluded(self) -> bool:
        return bool(self.info.get("info", {}).get("sample_excluded", False))

    def policy_framing(self) -> list[dict[str, str]]:


        return [{"role": "system", "content": LITERESEARCHER_SYSTEM_PROMPT}]

    def policy_tool_schemas(self) -> list[dict[str, Any]]:
        return deepcopy(list(_LITERESEARCHER_QWEN_TOOL_SCHEMAS))

    def normalize_initial_policy_context(
        self,
        messages: Sequence[Mapping[str, str]],
    ) -> list[dict[str, str]]:
        normalized = _copy_policy_messages(messages)
        if not normalized or normalized[-1]["role"] != "user":
            raise ValueError(
                "LiteResearcher initial policy context must end with the question"
            )
        observation = str(self.observe())
        if normalized[-1]["content"] != observation:
            raise ValueError(
                "LiteResearcher initial policy context does not end with the current question"
            )
        return self.policy_framing() + [{"role": "user", "content": observation}]

    def bind_policy_context(
        self,
        messages: Sequence[Mapping[str, str]],
        *,
        initial: bool = False,
    ) -> None:
        normalized = _copy_policy_messages(messages)
        if initial:
            self._immutable_policy_context = deepcopy(normalized)
            self._policy_context_bound = True
        self._current_policy_context = normalized

    def policy_turn_candidate(self) -> str | None:
        if not self._policy_context_bound or self._pending_checkpoint_read is not None:
            return None
        return LITERESEARCHER_CONTEXT_COMPACTION_REQUEST

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
                "LiteResearcher compaction requires task-neutral token pressure"
            )
        if (
            pressure.max_observation_tokens
            < LITERESEARCHER_MIN_OBSERVATION_TOKEN_ENVELOPE
        ):
            raise RuntimeError(
                "LiteResearcher route observation-token envelope is too small: "
                f"configured={pressure.max_observation_tokens} "
                f"minimum={LITERESEARCHER_MIN_OBSERVATION_TOKEN_ENVELOPE}"
            )
        capacity = pressure.effective_prompt_capacity
        if (
            pressure.action_prompt_tokens > capacity
            or pressure.candidate_prompt_tokens > capacity
        ):
            raise PolicyContextCapacityExceeded(
                "LiteResearcher context reached the prompt cap before a trainable "
                "compaction could be sampled"
            )


        if (
            not self._checkpoint_retry_pending
            and checkpoint_retry_trigger_tokens(
                pressure, control_request=LITERESEARCHER_CONTEXT_COMPACTION_REQUEST
            )
            < capacity
        ):
            return None
        remaining_actions = self._lr_remaining_budget()
        if (
            remaining_actions
            < LITERESEARCHER_MIN_ACTIONS_FOR_CHECKPOINT_WRITE_READ_ANSWER
        ):


            return None
        if not self._checkpoint_retry_pending:
            if self._current_policy_context is None:
                raise RuntimeError(
                    "LiteResearcher checkpoint request lost its pre-boundary context"
                )
            self._checkpoint_write_retry_framing = deepcopy(
                self._current_policy_context
            )
        elif self._checkpoint_write_retry_framing is None:
            raise RuntimeError(
                "LiteResearcher checkpoint retry lost its pre-boundary context"
            )
        self._selected_policy_control = "context_compaction"
        return LITERESEARCHER_CONTEXT_COMPACTION_REQUEST

    def step(self, action: str) -> StepOutput:
        if self._selected_policy_control == "context_compaction":
            return self._complete_context_compaction(action)
        return self._step_native_policy_action(action)

    def _step_native_policy_action(self, action: str) -> StepOutput:
        native_before = self._native_call_count
        policy_before = self._policy_step_count
        context_before = self._context_epoch
        checkpoint_read_pending_before = self._pending_checkpoint_read
        checkpoint_read_framing_before = self._pending_checkpoint_read_framing
        submitted_action, parser_evidence = (
            normalize_literesearcher_policy_action(action)
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
        endpoint_action_submission = response_info.get("action_submission")
        action_submission: dict[str, Any] = {
            "raw_policy_output": action,
            "submitted_action": submitted_action,
            **parser_evidence,
        }
        if isinstance(endpoint_action_submission, Mapping):
            action_submission["endpoint_action_submission"] = dict(
                endpoint_action_submission
            )
        server_wrapper = (
            response_info.get("wrapper_evidence", {})
            if isinstance(response_info, Mapping)
            else {}
        )
        native_reward = float(response["reward"])
        if not math.isfinite(native_reward):
            raise RuntimeError(
                "LiteResearcher endpoint returned a non-finite reward"
            )
        reward = native_reward
        reward_overlay = None
        invalid_action = (
            response_info.get("status") == "invalid_action"
            or (
                isinstance(server_wrapper, Mapping)
                and server_wrapper.get("invalid_action") is True
            )
        )
        if invalid_action:
            reward, reward_overlay = self._invalid_action_reward_overlay(
                native_reward=native_reward,
                done=bool(response["done"]),
                sample_excluded=bool(response_info.get("sample_excluded", False)),
            )
        wrapper_evidence: dict[str, Any] = {
            "event": "native_action",
            "server_wrapper_evidence": (
                dict(server_wrapper) if isinstance(server_wrapper, Mapping) else {}
            ),
        }
        if (
            submitted_action.startswith(_ANSWER_ENVELOPE_PREFIX)
            and submitted_action.endswith(_ANSWER_ENVELOPE_SUFFIX)
        ):


            wrapper_evidence["answer_injection_scan"] = _scan_answer_injection(
                submitted_action[
                    len(_ANSWER_ENVELOPE_PREFIX) : -len(_ANSWER_ENVELOPE_SUFFIX)
                ]
            )
        if reward_overlay is not None:
            wrapper_evidence["reward_overlay"] = reward_overlay
        milestone_overlay = self._exploration_milestone_overlay(
            submitted_action=submitted_action,
            reward=reward,
            done=bool(response["done"]),
            invalid_action=invalid_action,
            sample_excluded=bool(response_info.get("sample_excluded", False)),
        )
        if milestone_overlay is not None:
            reward = milestone_overlay["total_reward"]
            wrapper_evidence["exploration_milestone_overlay"] = milestone_overlay
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
        remaining_actions = self._lr_remaining_budget()
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
        invalid_budget_exhausted = (
            self.invalid_action_budget is not None
            and self._invalid_action_total >= self.invalid_action_budget
        )
        terminal = (
            bool(response["done"])
            or read_retry_budget_exhausted
            or invalid_budget_exhausted
        )
        wrapper_evidence["invalid_action_budget_exhausted"] = (
            invalid_budget_exhausted
        )
        wrapper_evidence["invalid_action_total"] = self._invalid_action_total
        if invalid_budget_exhausted:
            policy_state = (
                "Too many invalid actions were submitted in this episode; the "
                "episode ended without an answer."
            )
        elif read_retry_budget_exhausted:
            policy_state = (
                "Checkpoint read failed with too few policy actions remaining for "
                "a retry and final answer; the episode ended without an answer."
            )
        elif (
            checkpoint_read_pending_before is not None
            and not read_satisfied
            and not bool(response["done"])
        ):
            policy_state = build_filesystem_checkpoint_read_retry_observation(
                read_failure_reason or "checkpoint_read_not_observed"
            )
            if submitted_action == QWEN_INVALID_ACTION_SENTINEL:
                policy_state = _invalid_action_feedback(
                    policy_state,
                    parser_evidence.get("tool_parser_error"),
                )
        else:
            observation_text = str(response["observation"])
            if (
                _canonical_action_function_line(submitted_action)
                in _CANONICAL_PAGE_FETCH_HEADERS
                and _literesearcher_observation_rejectably_corrupt(
                    observation_text
                )
            ):


                observation_text = _LITERESEARCHER_CORRUPT_PAGE_OBSERVATION
                wrapper_evidence["page_content_rejected"] = True
            policy_state = observation_text
            if submitted_action == QWEN_INVALID_ACTION_SENTINEL:
                policy_state = _invalid_action_feedback(
                    policy_state,
                    parser_evidence.get("tool_parser_error"),
                )
        context_transition = None
        if (
            checkpoint_read_pending_before is not None
            and not read_satisfied
            and not bool(response["done"])
            and not read_retry_budget_exhausted
        ):
            if checkpoint_read_framing_before is None:
                raise RuntimeError(
                    "LiteResearcher pending checkpoint read lost its trusted framing"
                )
            read_retry_messages = build_post_checkpoint_read_retry_context(
                checkpoint_read_framing_before,
                checkpoint_read_pending_before,
                read_failure_reason or "checkpoint_read_not_observed",
                continuation_marker=self._policy_continuation_marker(),
            )
            if submitted_action == QWEN_INVALID_ACTION_SENTINEL:
                read_retry_messages = _append_rejected_reason_to_messages(
                    read_retry_messages,
                    parser_evidence.get("tool_parser_error"),
                )
            context_transition = build_task_neutral_context_transition(
                CONTEXT_OPERATION_REPLACE,
                messages=read_retry_messages,
            )
        returned_env_info = dict(response_info)


        server_excluded = bool(response_info.get("sample_excluded", False))
        if invalid_budget_exhausted and not server_excluded:
            returned_env_info.update(
                {
                    "status": "invalid_action_budget_exhausted",
                    "episode_success": False,
                    "sample_excluded": False,
                }
            )
        if read_retry_budget_exhausted and not server_excluded:
            returned_env_info.update(
                {
                    "status": "checkpoint_read_retry_budget_exhausted",
                    "episode_success": False,
                    "sample_excluded": False,
                }
            )
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

    def _invalid_action_reward_overlay(
        self,
        *,
        native_reward: float,
        done: bool,
        sample_excluded: bool,
    ) -> tuple[float, dict[str, Any] | None]:
        self._invalid_action_total += 1
        invalid_action_reward = float(getattr(self, "invalid_action_reward", 0.0))
        if invalid_action_reward == 0.0:
            return native_reward, None
        if sample_excluded:
            raise RuntimeError(
                "LiteResearcher invalid action cannot also be sample_excluded"
            )
        if native_reward != 0.0:
            raise RuntimeError(
                "LiteResearcher invalid-action overlay requires zero native reward"
            )
        reward = native_reward + invalid_action_reward
        return reward, {
            "schema": "literesearcher_invalid_action_reward_v1",
            "native_reward": native_reward,
            "penalty": invalid_action_reward,
            "total_reward": reward,
            "terminal": done,
        }

    def _exploration_milestone_overlay(
        self,
        *,
        submitted_action: str,
        reward: float,
        done: bool,
        invalid_action: bool,
        sample_excluded: bool,
    ) -> dict[str, Any] | None:

        if not self._exploration_milestones or done or sample_excluded:
            return None
        if invalid_action or submitted_action == QWEN_INVALID_ACTION_SENTINEL:
            return None
        header = _canonical_action_function_line(submitted_action)
        event = _CANONICAL_HEADER_TO_MILESTONE.get(header)
        if event is None or event in self._exploration_milestones_paid:
            return None
        milestone_reward = self._exploration_milestones[event]
        self._exploration_milestones_paid.add(event)
        return {
            "schema": "literesearcher_exploration_milestone_reward_v1",
            "event": event,
            "reward_before_overlay": reward,
            "milestone_reward": milestone_reward,
            "total_reward": reward + milestone_reward,
        }

    def begin_policy_turn(self, turn_index: int, turn_budget: int) -> None:


        self._policy_turn_index = int(turn_index)
        self._policy_turn_budget = int(turn_budget)

    def _lr_remaining_budget(self) -> int:


        if self._policy_turn_budget is not None:
            return self._policy_turn_budget - (self._policy_turn_index + 1)
        return self.max_policy_steps - self._policy_step_count

    def _policy_budget_footer(self) -> str:


        if self._policy_turn_budget is not None:

            used = self._policy_turn_index + 1
            remaining = max(0, self._policy_turn_budget - used)
            return (
                f" [LR policy budget: turn {used} of "
                f"{self._policy_turn_budget}; "
                f"{remaining} turns remain.]"
            )
        used = self._policy_step_count
        remaining = max(0, self.max_policy_steps - used)
        return (
            f" [LR policy budget: step {used} of {self.max_policy_steps}; "
            f"{remaining} steps remain.]"
        )

    def _policy_continuation_marker(self) -> str:

        return (
            LITERESEARCHER_POLICY_CONTINUATION_MARKER
            + self._policy_budget_footer()
        )

    def _policy_write_retry_marker(self) -> str:

        return (
            LITERESEARCHER_POLICY_WRITE_RETRY_MARKER
            + self._policy_budget_footer()
        )

    def _complete_context_compaction(self, action: str) -> StepOutput:
        write_retry_framing_before = self._checkpoint_write_retry_framing
        native_output = self._step_native_policy_action(action)
        self._selected_policy_control = None
        info = dict(native_output.info)
        env_info = info.get("env_info", {})
        server_wrapper = (
            env_info.get("wrapper_evidence", {})
            if isinstance(env_info, Mapping)
            else {}
        )
        receipt_value = (
            server_wrapper.get("filesystem_checkpoint")
            if isinstance(server_wrapper, Mapping)
            else None
        )
        action_submission = info.get("action_submission")
        submitted_checkpoint_action = (
            action_submission.get("submitted_action")
            if isinstance(action_submission, Mapping)
            else None
        )
        checkpoint_receipt = bind_filesystem_checkpoint_receipt_to_submitted_action(
            receipt_value,
            submitted_action=submitted_checkpoint_action,
        )
        persisted = filesystem_checkpoint_write_succeeded(checkpoint_receipt)
        checkpoint_failure_reason = filesystem_checkpoint_failure_reason(
            checkpoint_receipt
        )


        checkpoint_read_attempt = _is_pure_checkpoint_read_submission(
            submitted_checkpoint_action
        )
        remaining_actions = self._lr_remaining_budget()


        checkpoint_write_abandoned_low_budget = bool(
            not persisted
            and not native_output.done
            and remaining_actions
            < LITERESEARCHER_MIN_ACTIONS_FOR_CHECKPOINT_WRITE_READ_ANSWER
        )
        self._checkpoint_retry_pending = bool(
            not persisted
            and not native_output.done
            and not checkpoint_write_abandoned_low_budget
        )


        failure_detail = _literesearcher_checkpoint_failure_detail(
            server_wrapper.get("execution")
            if isinstance(server_wrapper, Mapping)
            else None,
            native_output.state,
        )
        model_facing_failure_reason = (
            "checkpoint_read_instead_of_write"
            if checkpoint_read_attempt
            else checkpoint_failure_reason or "unknown_checkpoint_failure"
        )
        if checkpoint_write_abandoned_low_budget:
            policy_observation = (
                "Filesystem checkpoint was not accepted and too few policy "
                "actions remain for a rewrite, a verified read, and a final "
                "answer. Compaction is abandoned and the current context is "
                "kept; do not retry the checkpoint write. Submit your best "
                "evidence-backed answer with the answer tool now."
            )
        elif self._checkpoint_retry_pending:
            policy_observation = build_filesystem_checkpoint_retry_observation(
                model_facing_failure_reason,
                failure_detail=failure_detail,
            )
        else:
            policy_observation = native_output.state

        context_transition = None
        checkpoint_framing_sha256 = None
        if persisted and not native_output.done:
            framing = self._immutable_policy_context
            if framing is None:
                raise RuntimeError("LiteResearcher compaction lost its task framing")
            checkpoint_framing_sha256 = filesystem_checkpoint_framing_sha256(
                framing
            )
            replacement = build_post_checkpoint_context(
                framing,
                checkpoint_receipt,
                continuation_marker=self._policy_continuation_marker(),
            )
            self._context_epoch += 1
            self._pending_checkpoint_read = dict(checkpoint_receipt)
            self._pending_checkpoint_read_framing = deepcopy(framing)
            self._checkpoint_write_retry_framing = None
            context_transition = build_task_neutral_context_transition(
                CONTEXT_OPERATION_REPLACE,
                messages=replacement,
            )
        elif native_output.done or checkpoint_write_abandoned_low_budget:


            self._checkpoint_write_retry_framing = None
            self._pending_checkpoint_read = None
            self._pending_checkpoint_read_framing = None
        else:
            if write_retry_framing_before is None:
                raise RuntimeError(
                    "LiteResearcher failed checkpoint write lost its retry context"
                )
            write_retry_messages = build_filesystem_checkpoint_write_retry_context(
                write_retry_framing_before,
                model_facing_failure_reason,
                failure_detail=failure_detail,
                continuation_marker=self._policy_write_retry_marker(),
            )
            write_retry_submission = info.get("action_submission")
            write_retry_reason = (
                write_retry_submission.get("tool_parser_error")
                if isinstance(write_retry_submission, Mapping)
                and write_retry_submission.get("submitted_action")
                == QWEN_INVALID_ACTION_SENTINEL
                else None
            )
            write_retry_messages = _append_rejected_reason_to_messages(
                write_retry_messages, write_retry_reason
            )
            context_transition = build_task_neutral_context_transition(
                CONTEXT_OPERATION_REPLACE,
                messages=write_retry_messages,
            )

        reward = float(native_output.reward)
        terminal = bool(native_output.done)
        wrapper_evidence = {
            "event": "context_compaction",
            "workspace_continuity_id": self.env_id,
            "native_environment_call_count": 1,
            "continuation_path": FILESYSTEM_CHECKPOINT_PATH,
            "continuation_max_bytes": FILESYSTEM_CHECKPOINT_MAX_BYTES,
            "continuation_persisted": persisted,
            "checkpoint_receipt": checkpoint_receipt,
            "checkpoint_failure_reason": checkpoint_failure_reason,
            "checkpoint_failure_detail": failure_detail or None,
            "context_replaced": bool(persisted and not terminal),
            "retry_pending": self._checkpoint_retry_pending,
            "checkpoint_retry_observation_bounded": self._checkpoint_retry_pending,
            "checkpoint_retry_context_rebuilt": self._checkpoint_retry_pending,
            "preserved_policy_output": persisted,
            "preserved_native_observation": persisted,
            "checkpoint_action_in_successor_context": False,
            "checkpoint_observation_in_successor_context": False,
            "checkpoint_content_in_successor_context": False,
            "checkpoint_framing_sha256": checkpoint_framing_sha256,
            "checkpoint_read_required_after": bool(persisted and not terminal),
            "checkpoint_write_abandoned_low_budget": (
                checkpoint_write_abandoned_low_budget
            ),
            "checkpoint_write_abandon_remaining_actions": remaining_actions,
            "server_wrapper_evidence": (
                dict(server_wrapper) if isinstance(server_wrapper, Mapping) else {}
            ),
        }
        if checkpoint_read_attempt:
            wrapper_evidence["checkpoint_write_turn_action"] = "checkpoint_read"
        existing_overlay = info.get("wrapper_evidence", {}).get("reward_overlay")
        if not persisted and not native_output.done and existing_overlay is None:


            if not checkpoint_read_attempt:


                self._checkpoint_write_failure_total += 1
                write_failure_penalty = float(
                    getattr(self, "invalid_action_reward", 0.0)
                )
                checkpoint_overlay = None
                if write_failure_penalty != 0.0:


                    reward_before = reward
                    reward = min(reward_before, write_failure_penalty)
                    checkpoint_overlay = {
                        "schema": (
                            "literesearcher_checkpoint_write_failure_reward_v1"
                        ),
                        "native_reward": reward_before,
                        "penalty": write_failure_penalty,
                        "total_reward": reward,
                        "terminal": terminal,
                    }
                if checkpoint_overlay is not None:
                    checkpoint_overlay = dict(checkpoint_overlay)
                    checkpoint_overlay["basis"] = "checkpoint_contract_unsatisfied"
                    wrapper_evidence["reward_overlay"] = checkpoint_overlay
        elif existing_overlay is not None:
            wrapper_evidence["reward_overlay"] = dict(existing_overlay)

        wrapper_evidence["checkpoint_write_failure_total"] = (
            self._checkpoint_write_failure_total
        )
        returned_env_info = dict(env_info) if isinstance(env_info, Mapping) else {}
        return StepOutput(
            state=policy_observation,
            reward=reward,
            done=terminal,
            info=build_task_neutral_transition_info(
                env_info=returned_env_info,
                action_submission=info.get(
                    "action_submission", {"raw_policy_output": action}
                ),
                native_step_before=info.get("native_step_before"),
                native_step_after=info.get("native_step_after"),
                native_call_count_before=info.get("native_call_count_before"),
                native_call_count_after=info.get("native_call_count_after"),
                context_epoch_before=info.get("context_epoch_before"),
                context_epoch_after=self._context_epoch,
                session_epoch_before=0,
                session_epoch_after=0,
                policy_step_before=info.get("policy_step_before"),
                policy_step_after=info.get("policy_step_after"),
                context_transition=context_transition,
                wrapper_evidence=wrapper_evidence,
            ),
        )

    def reset(self, idx: int = 0) -> dict[str, Any]:
        response = self._request(
            "POST", "reset", json={"id": self.env_id, "data_idx": idx}
        )
        self.info = response
        self._reset_policy_transition_state()
        return response

    def finalize_policy_horizon(self) -> StepOutput:
        return StepOutput(
            state="LiteResearcher policy-turn budget exhausted without an accepted answer.",
            reward=0.0,
            done=True,
            info=build_task_neutral_transition_info(
                env_info={
                    **dict(self.info.get("info", {})),
                    "status": "max_policy_steps_exhausted",
                    "episode_success": False,
                    "sample_excluded": False,
                },
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

    def close(self) -> bool:
        value = self._request_json("POST", "close", json={"id": self.env_id})
        if value is not True:
            raise requests.RequestException(
                "LiteResearcher POST /close did not return true"
            )
        return True

    def _request(self, method: str, path: str, **kwargs) -> dict[str, Any]:
        value = self._request_json(method, path, **kwargs)
        if not isinstance(value, dict):
            raise requests.RequestException(
                f"LiteResearcher {method} /{path} returned a non-object response"
            )
        return value

    def _request_json(self, method: str, path: str, **kwargs) -> Any:
        response = requests.request(
            method,
            f"{self.env_server_base}/{path}",
            timeout=self.timeout,
            **kwargs,
        )
        if response.status_code != 200:
            raise requests.RequestException(
                f"LiteResearcher {method} /{path} failed: "
                f"status={response.status_code} body={response.text[-1000:]}"
            )
        return response.json()


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
