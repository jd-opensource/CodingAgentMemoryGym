from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Mapping

NATIVE_TOOL_START = "<tool" + "_call>"
NATIVE_TOOL_END = "</tool" + "_call>"
NATIVE_FUNCTION_END = "</function>"
NATIVE_PARAMETER_END = "</parameter>"

_NATIVE_FUNCTION_RE = re.compile(r"\A<function=([A-Za-z0-9_]+)>\Z")
_NATIVE_PARAMETER_RE = re.compile(r"\A<parameter=([A-Za-z][A-Za-z0-9_]*)>\Z")

_NATIVE_PARAMETER_INLINE_RE = re.compile(
    r"\A<parameter=([A-Za-z][A-Za-z0-9_]*)>(.*)</parameter>\Z", re.DOTALL
)
MAX_PRE_ACTION_REASONING_BYTES = 512
_ACTION_LINE_START_RES = (
    re.compile(r"(?m)^" + re.escape(NATIVE_TOOL_START) + r"\r?$"),
)
_THINK_START_RE = re.compile(r"\A<think\s*>", re.IGNORECASE)
_THINK_END_RE = re.compile(r"</think\s*>", re.IGNORECASE)

@dataclass(frozen=True)
class ParsedPolicyAction:
    kind: str
    raw_output: str
    action_text: str
    thought: str = ""
    function_name: str | None = None
    parameters: Mapping[str, str] | None = None
    calls: tuple[tuple[str, dict[str, str]], ...] = ()
    error: str | None = None

    @property
    def is_tool(self) -> bool:
        return self.kind == "tool_call"

    def as_evidence(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "raw_output": self.raw_output,
            "action_text": self.action_text,
            "thought": self.thought,
            "function_name": self.function_name,
            "parameters": None if self.parameters is None else dict(self.parameters),
            "calls": [
                {"function_name": name, "parameters": dict(params)}
                for name, params in self.calls
            ],
            "error": self.error,
        }

def parse_policy_action(raw_output: str) -> ParsedPolicyAction:
    if not isinstance(raw_output, str):
        raise TypeError(
            f"agentgeneral policy output must be text, got {type(raw_output).__name__}"
        )
    thought, action_text, framing_error = _split_thinking(raw_output)
    if framing_error is not None:
        return _parser_error(raw_output, action_text, thought, framing_error)
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
        return _parser_error(raw_output, action_text, thought, prefix_error)
    if visible_reasoning:
        thought = "\n\n".join(
            part for part in (thought, visible_reasoning) if part
        )

    if action_text.startswith(NATIVE_TOOL_START):
        return _parse_native_tool_call(raw_output, action_text, thought)
    if "<function=" in action_text or NATIVE_TOOL_START in action_text:
        return _parser_error(
            raw_output,
            action_text,
            thought,
            "attempted tool call does not use the canonical envelope grammar",
        )
    return _parser_error(
        raw_output,
        action_text,
        thought,
        "plain text is not an action; emit one Qwen XML envelope with a tool call",
    )

def _parse_native_tool_call(
    raw_output: str,
    action_text: str,
    thought: str,
) -> ParsedPolicyAction:
    lines = action_text.splitlines()
    if (
        len(lines) < 4
        or lines[0] != NATIVE_TOOL_START
        or lines[-1] != NATIVE_TOOL_END
        or lines[-2] != NATIVE_FUNCTION_END
    ):
        return _parser_error(
            raw_output,
            action_text,
            thought,
            "tool call must contain exactly one complete envelope",
        )
    blocks: list[list[str]] = []
    current: list[str] | None = None
    for line in lines:
        if current is None:
            if line == NATIVE_TOOL_START:
                current = [line]
            elif line.strip():
                return _parser_error(
                    raw_output,
                    action_text,
                    thought,
                    "tool call has content outside a parameter block",
                )
        else:
            current.append(line)
            if line == NATIVE_TOOL_END:
                blocks.append(current)
                current = None
    if current is not None or not blocks:
        return _parser_error(
            raw_output,
            action_text,
            thought,
            "tool call envelope is not closed",
        )
    calls: list[tuple[str, dict[str, str]]] = []
    for block in blocks:
        parsed = _parse_envelope_block(block, raw_output, action_text, thought)
        if isinstance(parsed, ParsedPolicyAction):
            return parsed
        calls.append(parsed)
    function_name, parameters = calls[0]
    return ParsedPolicyAction(
        kind="tool_call",
        raw_output=raw_output,
        action_text=action_text,
        thought=thought,
        function_name=function_name,
        parameters=parameters,
        calls=tuple(calls),
    )

def _parse_envelope_block(
    block: list[str],
    raw_output: str,
    action_text: str,
    thought: str,
) -> tuple[str, dict[str, str]] | ParsedPolicyAction:

    if len(block) < 4 or block[-2] != NATIVE_FUNCTION_END:
        return _parser_error(
            raw_output,
            action_text,
            thought,
            "tool call must contain exactly one complete envelope",
        )
    function_match = _NATIVE_FUNCTION_RE.fullmatch(block[1])
    if function_match is None:
        return _parser_error(
            raw_output,
            action_text,
            thought,
            "tool call has an invalid function opening tag",
        )
    function_name = function_match.group(1)

    parameters: dict[str, str] = {}
    cursor = 2
    while cursor < len(block) - 2:
        line = block[cursor]
        inline_match = _NATIVE_PARAMETER_INLINE_RE.fullmatch(line)
        if inline_match is not None:
            name = inline_match.group(1)
            if name in parameters:
                return _parser_error(
                    raw_output,
                    action_text,
                    thought,
                    f"tool call repeats parameter {name!r}",
                )
            parameters[name] = inline_match.group(2)
            cursor += 1
            continue
        parameter_match = _NATIVE_PARAMETER_RE.fullmatch(line)
        if parameter_match is None:
            return _parser_error(
                raw_output,
                action_text,
                thought,
                "tool call has content outside a parameter block",
            )
        name = parameter_match.group(1)
        if name in parameters:
            return _parser_error(
                raw_output,
                action_text,
                thought,
                f"tool call repeats parameter {name!r}",
            )
        cursor += 1
        value_start = cursor
        while cursor < len(block) - 2 and block[cursor] != NATIVE_PARAMETER_END:
            if _NATIVE_PARAMETER_RE.fullmatch(block[cursor]):
                return _parser_error(
                    raw_output,
                    action_text,
                    thought,
                    "tool call contains a nested parameter block",
                )
            cursor += 1
        if cursor >= len(block) - 2:
            return _parser_error(
                raw_output,
                action_text,
                thought,
                f"tool call parameter {name!r} is not closed",
            )
        parameters[name] = "\n".join(block[value_start:cursor])
        cursor += 1
    return function_name, parameters

def _split_bounded_action_prefix(
    text: str,
) -> tuple[str, str, str | None]:
    if text.startswith(NATIVE_TOOL_START):
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
            return "", text, "policy output contains an unmatched thinking tag"
        return "", text, None
    end = _THINK_END_RE.search(text, start.end())
    if end is None:
        return (
            text[start.end() :].strip(),
            "",
            "policy output contains an unclosed thinking block",
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

def _parser_error(
    raw_output: str,
    action_text: str,
    thought: str,
    error: str,
) -> ParsedPolicyAction:
    return ParsedPolicyAction(
        kind="parser_error",
        raw_output=raw_output,
        action_text=action_text,
        thought=thought,
        error=error,
    )
