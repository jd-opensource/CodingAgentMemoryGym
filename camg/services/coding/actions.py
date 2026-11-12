from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any, Literal, Mapping

ActionKind = Literal["bash", "parser_error"]

_SHELL_PREFIX = "bash "
_PATCH_PREFIX = "apply_patch\n"
UPSTREAM_SUBMISSION_SENTINEL = "COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT"
_NATIVE_TOOL_START = "<tool_call>"
_NATIVE_TOOL_END = "</tool_call>"
_NATIVE_FUNCTION_END = "</function>"
_NATIVE_PARAMETER_END = "</parameter>"
_NATIVE_FUNCTION_RE = re.compile(r"\A<function=([A-Za-z0-9_]+)>\Z")
_NATIVE_PARAMETER_RE = re.compile(r"\A<parameter=([A-Za-z][A-Za-z0-9_]*)>\Z")
MAX_PRE_ACTION_REASONING_BYTES = 512
_ACTION_LINE_START_RES = (
    re.compile(r"(?m)^bash (?=\{)"),
    re.compile(r"(?m)^apply_patch\r?\n(?=\*\*\* Begin Patch)"),
    re.compile(r"(?m)^<tool_call>\r?$"),
)
_THINK_START_RE = re.compile(r"\A<think\s*>", re.IGNORECASE)
_THINK_END_RE = re.compile(r"</think\s*>", re.IGNORECASE)
_TOOLISH_PREFIX_RE = re.compile(
    r"\A(?:Action\s*:\s*)?(?:shell[\s_-]*command|apply[\s_-]*patch)\b",
    re.IGNORECASE,
)
_FENCED_TOOLISH_RE = re.compile(
    r"\A```(?:json|python|bash|shell)?\s*\n?"
    r"(?:shell[\s_-]*command|apply[\s_-]*patch)\b",
    re.IGNORECASE,
)
_EMBEDDED_SHELL_ATTEMPT_RE = re.compile(
    r"\bbash\s+\{",
    re.IGNORECASE,
)
_EMBEDDED_PATCH_ATTEMPT_RE = re.compile(
    r"(?:<tool_call>\s*)?apply_patch\s*\r?\n\s*\*\*\* Begin Patch",
    re.IGNORECASE,
)

@dataclass(frozen=True)
class ParsedPolicyAction:
    kind: ActionKind
    raw_output: str
    action_text: str
    thought: str = ""
    arguments: Mapping[str, Any] | None = None
    patch: str | None = None
    final_response: str | None = None
    error: str | None = None
    tool_hint: str | None = None
    calls: tuple[ParsedPolicyAction, ...] = ()

    @property
    def is_tool(self) -> bool:
        return self.kind == "bash"

    def as_evidence(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "raw_output": self.raw_output,
            "action_text": self.action_text,
            "thought": self.thought,
            "arguments": None if self.arguments is None else dict(self.arguments),
            "patch": self.patch,
            "final_response": self.final_response,
            "error": self.error,
            "tool_hint": self.tool_hint,
            "calls": [
                {"kind": sub.kind, "arguments": dict(sub.arguments or {})}
                for sub in self.calls
            ],
        }

class _DuplicateJsonKey(ValueError):
    pass

def parse_policy_action(raw_output: str) -> ParsedPolicyAction:

    if not isinstance(raw_output, str):
        raise TypeError(
            f"SWE-smith policy output must be text, got {type(raw_output).__name__}"
        )
    thought, action_text, framing_error = _split_thinking(raw_output)
    if framing_error is not None:
        return _parser_error(
            raw_output,
            action_text,
            thought,
            framing_error,
        )
    action_text = _strip_single_eos(action_text).strip()
    if not action_text:
        return _parser_error(
            raw_output,
            action_text,
            thought,
            "policy output is empty after removing optional thinking text",
        )
    visible_reasoning, action_text, prefix_error = _split_bounded_action_prefix(
        action_text
    )
    if prefix_error is not None:
        return _parser_error(
            raw_output,
            action_text,
            thought,
            prefix_error,
            tool_hint=_infer_toolish_attempt(action_text),
        )
    if visible_reasoning:
        thought = "\n\n".join(part for part in (thought, visible_reasoning) if part)

    if action_text.startswith(_SHELL_PREFIX):
        return _parse_bash(raw_output, action_text, thought)
    if action_text.startswith(_NATIVE_TOOL_START):
        return _parse_native_tool_call(raw_output, action_text, thought)
    tool_hint = _infer_toolish_attempt(action_text)
    if tool_hint is not None:
        return _parser_error(
            raw_output,
            action_text,
            thought,
            "attempted tool call does not use the canonical SWE-smith grammar",
            tool_hint=tool_hint,
        )
    return _parser_error(
        raw_output,
        action_text,
        thought,
        "plain text is not a submission; run the upstream submission sentinel "
        "after editing and testing",
    )

def _parse_bash(
    raw_output: str,
    action_text: str,
    thought: str,
) -> ParsedPolicyAction:
    payload_text = action_text[len(_SHELL_PREFIX) :]
    try:
        payload = json.loads(payload_text, object_pairs_hook=_unique_json_object)
    except (_DuplicateJsonKey, json.JSONDecodeError) as exc:
        return _parser_error(
            raw_output,
            action_text,
            thought,
            f"bash payload must be one valid JSON object: {exc}",
            tool_hint="bash",
        )
    if not isinstance(payload, dict):
        return _parser_error(
            raw_output,
            action_text,
            thought,
            "bash payload must be a JSON object",
            tool_hint="bash",
        )
    return _build_bash(raw_output, action_text, thought, payload)

def _build_bash(
    raw_output: str,
    action_text: str,
    thought: str,
    payload: Mapping[str, Any],
) -> ParsedPolicyAction:
    allowed = {"command"}
    unexpected = sorted(set(payload) - allowed)
    missing = sorted({"command"} - set(payload))
    if unexpected or missing:
        detail = []
        if missing:
            detail.append("missing " + ", ".join(missing))
        if unexpected:
            detail.append("unexpected " + ", ".join(unexpected))
        return _parser_error(
            raw_output,
            action_text,
            thought,
            "bash arguments are invalid: " + "; ".join(detail),
            tool_hint="bash",
        )
    command = payload["command"]
    if not isinstance(command, str) or not command or "\x00" in command:
        return _parser_error(
            raw_output,
            action_text,
            thought,
            "bash command must be a non-empty string without NUL bytes",
            tool_hint="bash",
        )
    workdir = payload.get("workdir", ".")
    if not isinstance(workdir, str) or not workdir or "\x00" in workdir:
        return _parser_error(
            raw_output,
            action_text,
            thought,
            "bash workdir must be a non-empty string without NUL bytes",
            tool_hint="bash",
        )
    timeout_ms = payload.get("timeout_ms")
    if timeout_ms is not None and (
        isinstance(timeout_ms, bool)
        or not isinstance(timeout_ms, int)
        or timeout_ms <= 0
    ):
        return _parser_error(
            raw_output,
            action_text,
            thought,
            "bash timeout_ms must be a positive integer",
            tool_hint="bash",
        )
    normalized: dict[str, Any] = {"command": command, "workdir": workdir}
    if timeout_ms is not None:
        normalized["timeout_ms"] = timeout_ms
    return ParsedPolicyAction(
        kind="bash",
        raw_output=raw_output,
        action_text=action_text,
        thought=thought,
        arguments=normalized,
        tool_hint="bash",
    )

def _parse_native_tool_call(
    raw_output: str,
    action_text: str,
    thought: str,
) -> ParsedPolicyAction:
    lines = action_text.splitlines()
    if (
        len(lines) < 6
        or lines[0] != _NATIVE_TOOL_START
        or lines[-1] != _NATIVE_TOOL_END
        or lines[-2] != _NATIVE_FUNCTION_END
    ):
        return _parser_error(
            raw_output,
            action_text,
            thought,
            "native tool call must contain one complete tool_call/function block",
            tool_hint=_native_tool_hint(action_text),
        )
    blocks: list[list[str]] = []
    current: list[str] | None = None
    for line in lines:
        if current is None:
            if line == _NATIVE_TOOL_START:
                current = [line]
            elif line.strip():
                return _parser_error(
                    raw_output,
                    action_text,
                    thought,
                    "native tool call has content outside a parameter block",
                    tool_hint=_native_tool_hint(action_text),
                )
        else:
            current.append(line)
            if line == _NATIVE_TOOL_END:
                blocks.append(current)
                current = None
    if current is not None or not blocks:
        return _parser_error(
            raw_output,
            action_text,
            thought,
            "native tool call envelope is not closed",
            tool_hint=_native_tool_hint(action_text),
        )
    calls: list[ParsedPolicyAction] = []
    for block in blocks:
        parsed = _parse_envelope_block(block, raw_output, action_text, thought)
        if parsed.kind == "parser_error":
            return parsed
        calls.append(parsed)
    first = calls[0]
    return ParsedPolicyAction(
        kind="bash",
        raw_output=raw_output,
        action_text=action_text,
        thought=thought,
        arguments=first.arguments,
        calls=tuple(calls),
        tool_hint="bash",
    )

def _parse_envelope_block(
    block: list[str],
    raw_output: str,
    action_text: str,
    thought: str,
) -> ParsedPolicyAction:

    if len(block) < 6 or block[-2] != _NATIVE_FUNCTION_END:
        return _parser_error(
            raw_output,
            action_text,
            thought,
            "native tool call must contain one complete tool_call/function block",
            tool_hint=_native_tool_hint(action_text),
        )
    function_match = _NATIVE_FUNCTION_RE.fullmatch(block[1])
    if function_match is None:
        return _parser_error(
            raw_output,
            action_text,
            thought,
            "native tool call has an invalid function opening tag",
            tool_hint=_native_tool_hint(action_text),
        )
    function_name = function_match.group(1)
    if function_name != "bash":
        return _parser_error(
            raw_output,
            action_text,
            thought,
            f"unsupported native tool function: {function_name}",
            tool_hint=function_name,
        )

    parameters: dict[str, str] = {}
    cursor = 2
    while cursor < len(block) - 2:
        parameter_match = _NATIVE_PARAMETER_RE.fullmatch(block[cursor])
        if parameter_match is None:
            return _parser_error(
                raw_output,
                action_text,
                thought,
                "native tool call has content outside a parameter block",
                tool_hint=function_name,
            )
        name = parameter_match.group(1)
        if name in parameters:
            return _parser_error(
                raw_output,
                action_text,
                thought,
                f"native tool call repeats parameter {name!r}",
                tool_hint=function_name,
            )
        cursor += 1
        value_start = cursor
        while cursor < len(block) - 2 and block[cursor] != _NATIVE_PARAMETER_END:
            if _NATIVE_PARAMETER_RE.fullmatch(block[cursor]):
                return _parser_error(
                    raw_output,
                    action_text,
                    thought,
                    "native tool call contains a nested parameter block",
                    tool_hint=function_name,
                )
            cursor += 1
        if cursor >= len(block) - 2:
            return _parser_error(
                raw_output,
                action_text,
                thought,
                f"native tool parameter {name!r} is not closed",
                tool_hint=function_name,
            )
        parameters[name] = "\n".join(block[value_start:cursor])
        cursor += 1

    payload: dict[str, Any] = dict(parameters)
    if "timeout_ms" in payload:
        raw_timeout = str(payload["timeout_ms"]).strip()
        if not raw_timeout.isdecimal():
            return _parser_error(
                raw_output,
                action_text,
                thought,
                "bash timeout_ms must be a positive integer",
                tool_hint=function_name,
            )
        payload["timeout_ms"] = int(raw_timeout)
    return _build_bash(raw_output, action_text, thought, payload)

def _split_bounded_action_prefix(
    text: str,
) -> tuple[str, str, str | None]:

    if text.startswith((_SHELL_PREFIX, _PATCH_PREFIX, _NATIVE_TOOL_START)):
        return "", text, None
    starts = [
        match.start()
        for pattern in _ACTION_LINE_START_RES
        for match in pattern.finditer(text)
    ]
    if not starts:
        return "", text, None
    action_start = min(starts)
    visible_reasoning = text[:action_start].rstrip()
    if len(visible_reasoning.encode("utf-8")) > MAX_PRE_ACTION_REASONING_BYTES:
        return (
            visible_reasoning,
            text[action_start:],
            "pre-action reasoning exceeds the 512-byte safety bound",
        )
    return visible_reasoning, text[action_start:], None

def _split_thinking(raw_output: str) -> tuple[str, str, str | None]:
    text = raw_output.strip()
    start = _THINK_START_RE.match(text)
    if start is None:
        if _THINK_END_RE.search(text):
            return "", text, "policy output contains an unmatched </think> tag"
        return "", text, None
    end = _THINK_END_RE.search(text, start.end())
    if end is None:
        return (
            text[start.end() :].strip(),
            "",
            "policy output contains an unclosed <think> block",
        )
    thought = text[start.end() : end.start()].strip()
    action_text = text[end.end() :].strip()
    if _THINK_START_RE.search(action_text) or _THINK_END_RE.search(action_text):
        return thought, action_text, "policy output contains multiple thinking blocks"
    return thought, action_text, None

def _strip_single_eos(text: str) -> str:
    stripped = text.rstrip()
    if stripped.endswith("</s>"):
        return stripped[:-4].rstrip()
    return text

def _infer_toolish_attempt(text: str) -> str | None:
    if _NATIVE_TOOL_START in text or "<function=" in text:
        return _native_tool_hint(text)
    if _TOOLISH_PREFIX_RE.match(text) or _FENCED_TOOLISH_RE.match(text):
        lowered = text.lower()
        return "apply_patch" if "apply" in lowered[:80] else "bash"
    embedded_patch = _EMBEDDED_PATCH_ATTEMPT_RE.search(text)
    embedded_shell = _EMBEDDED_SHELL_ATTEMPT_RE.search(text)
    if embedded_patch is not None and (
        embedded_shell is None or embedded_patch.start() < embedded_shell.start()
    ):
        return "apply_patch"
    if embedded_shell is not None:
        return "bash"
    if text.startswith("{"):
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            return None
        if isinstance(payload, dict):
            candidate = payload.get("function_name", payload.get("name"))
            if isinstance(candidate, str):
                normalized = candidate.lower().replace("-", "_").replace(" ", "_")
                if normalized in {"bash", "apply_patch"}:
                    return normalized
    return None

def _native_tool_hint(text: str) -> str:
    match = re.search(r"<function=([A-Za-z0-9_]+)>", text)
    if match is not None:
        return match.group(1)
    native_prefix = text[text.find(_NATIVE_TOOL_START) :][:160].lower()
    if "apply_patch" in native_prefix:
        return "apply_patch"
    if "bash" in native_prefix:
        return "bash"
    return "native_tool"

def _unique_json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise _DuplicateJsonKey(f"duplicate key {key!r}")
        value[key] = item
    return value

def _parser_error(
    raw_output: str,
    action_text: str,
    thought: str,
    error: str,
    *,
    tool_hint: str | None = None,
) -> ParsedPolicyAction:
    return ParsedPolicyAction(
        kind="parser_error",
        raw_output=raw_output,
        action_text=action_text,
        thought=thought,
        error=error,
        tool_hint=tool_hint,
    )
