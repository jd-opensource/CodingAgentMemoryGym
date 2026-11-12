from __future__ import annotations

import json
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any


QWEN_SINGLE_TOOL_CALL_CONTRACT = (
    "Every policy response must contain at least one Qwen XML envelope. "
    "When several independent calls are useful together, emit them as "
    "consecutive envelopes in the same response; the environment "
    "executes them in order. Reason inside think tags before the "
    "envelopes, and output nothing after the last envelope closes. Do "
    "not use Markdown fences, bare JSON, or bare tool syntax, and never "
    "write envelope syntax inside your reasoning or your think blocks."
)


WORKSPACE_SHELL_CONTRACT = (
    "Workspace bash takes exactly one parameter: command. Never add "
    "workdir or timeout_ms parameters; every command already runs from the "
    "workspace root, so use workspace-relative paths and no cd.\n"
    "Put multi-line file content in one quoted here-document: append with "
    "`cat >> path <<'EOF'` and overwrite with `cat > path <<'EOF'`, placing "
    "every pending line in the same block instead of one line per call. Do "
    "not assemble multi-line text with inline printf or echo arguments.\n"
    "Chaining with `&&` or `||` inside one command is allowed; prefer "
    "write-then-read-back verification, for example "
    "`echo '+Confirmed field: value' >> notes.md && cat notes.md`."
)


QWEN_INVALID_ACTION_SENTINEL = "__AMG_INVALID_QWEN_TOOL_CALL__"


QWEN_TOOL_CALL_FENCE_OPEN = '<tool_call>'
QWEN_TOOL_CALL_FENCE_CLOSE = '</tool_call>'
QWEN_THINK_TAG_MARKER_1 = '<think>'
QWEN_THINK_TAG_MARKER_2 = '</think>'

_LEGACY_MARKER_IN_JSON_STRING_RE = re.compile(
    r"(?i)(?:"
    r"(?<![A-Za-z0-9_])(?P<bracket>search|click)\["
    r"|(?<![A-Za-z0-9_])(?P<object>bash|ask|submit)\s+\{"
    r"|(?P<patch>`apply_patch`|(?<![A-Za-z0-9_`])apply_patch(?!`))"
    r"(?=(?:\s+followed|\s*\\n\*\*\* Begin Patch))"
    r")"
)


def _inert_exact_value(value: Any) -> tuple[str, str]:


    if isinstance(value, str):
        kind = "string"
        payload = value
    else:
        kind = "canonical JSON"
        payload = json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        )
    encoded = json.dumps(payload, ensure_ascii=False)

    def escape_marker(match: re.Match[str]) -> str:
        matched = match.group(0)
        if match.group("bracket") is not None:
            return matched[:-1] + "\\u005b"
        if match.group("object") is not None:
            return matched[:-1] + "\\u007b"
        underscore = matched.find("_")
        if underscore < 0:
            raise AssertionError("apply_patch marker lost its underscore")
        return matched[:underscore] + "\\u005f" + matched[underscore + 1 :]

    encoded = _LEGACY_MARKER_IN_JSON_STRING_RE.sub(escape_marker, encoded)


    encoded = encoded.replace("<", "\\u003c").replace(">", "\\u003e")
    return kind, encoded


def describe_inert_qwen_function_record(
    name: str, arguments: Mapping[str, Any]
) -> str:


    if not arguments:
        return f"an inert record of the Qwen XML `{name}` function with no parameters"
    rendered_arguments = []
    for key, value in arguments.items():
        kind, encoded = _inert_exact_value(value)
        rendered_arguments.append(
            f"`{key}` exact {kind} value encoded as a JSON string: {encoded}"
        )
    return (
        f"an inert record of the Qwen XML `{name}` function; "
        + "; ".join(rendered_arguments)
    )


@dataclass(frozen=True)
class ParsedQwenToolCall:
    name: str
    arguments: Mapping[str, Any]
    parser_name: str = "qwen3_coder"


def parse_single_qwen3_tool_call(
    raw_output: str,
    *,
    tool_schemas: Sequence[Mapping[str, Any]],
) -> ParsedQwenToolCall | None:


    if not isinstance(raw_output, str):
        raise TypeError("Qwen policy output must be text")
    text = raw_output.strip()
    if text.endswith("</s>"):
        text = text[:-4].rstrip()
    if (
        text.count(QWEN_TOOL_CALL_FENCE_OPEN) != 1
        or text.count(QWEN_TOOL_CALL_FENCE_CLOSE) != 1
    ):
        return None
    if (
        QWEN_THINK_TAG_MARKER_1 in text
        or QWEN_THINK_TAG_MARKER_2 in text
    ):
        return None


    from verl.experimental.agent_loop.tool_parser import ToolParser
    from verl.tools.schemas import OpenAIFunctionToolSchema

    parser = ToolParser.get_tool_parser("qwen3_coder", tokenizer=None)
    schemas = [
        OpenAIFunctionToolSchema.model_validate(dict(item)) for item in tool_schemas
    ]


    try:
        envelope = parser.tool_call_complete_regex.search(text)
        if envelope is None:
            return None
        envelope_body = envelope.group(1).strip()
        function_match = parser.tool_call_function_regex.fullmatch(envelope_body)
        if function_match is None or function_match.group(1) is None:
            return None
        raw_function_call = function_match.group(1)
        separator = raw_function_call.find(">")
        if separator < 0:
            return None
        parameter_body = raw_function_call[separator + 1 :]
        parameter_matches = list(
            parser.tool_call_parameter_regex.finditer(parameter_body)
        )
        cursor = 0
        parameter_names: set[str] = set()
        truncated_parameter_count = 0
        for parameter_index, parameter_match in enumerate(parameter_matches):
            if parameter_body[cursor : parameter_match.start()].strip():
                return None
            match_text = parameter_match.group(1)
            if match_text is None:


                match_text = parameter_match.group(2)
                truncated_parameter_count += 1
                if (
                    match_text is None
                    or parameter_index != len(parameter_matches) - 1
                    or parameter_body[parameter_match.end() :].strip()
                ):
                    return None
            name_separator = match_text.find(">")
            if name_separator < 0:
                return None
            parameter_name = match_text[:name_separator]
            parameter_value = match_text[name_separator + 1 :]


            if (
                "<parameter=" in parameter_value
                or "</parameter>" in parameter_value
            ):
                return None
            if not parameter_name or parameter_name in parameter_names:
                return None
            parameter_names.add(parameter_name)
            cursor = parameter_match.end()
        if parameter_body[cursor:].strip() or truncated_parameter_count > 1:
            return None
        function_call = parser._parse_xml_function_call(raw_function_call, schemas)
    except (AttributeError, IndexError, KeyError, TypeError, ValueError):
        return None
    if function_call is None:
        return None
    allowed_names = {schema.function.name for schema in schemas}
    if function_call.name not in allowed_names:
        return None
    try:
        arguments = json.loads(function_call.arguments)
    except (TypeError, json.JSONDecodeError):
        return None
    if not isinstance(arguments, dict):
        return None
    return ParsedQwenToolCall(
        name=function_call.name,
        arguments=arguments,
    )


_MULTI_FUNCTION_LINE_RE = re.compile(r"<function=([A-Za-z0-9_.-]+)>")


def collect_clean_multi_qwen_tool_calls(raw_output: str) -> list[str] | None:

    function_close = "</" + "function>"
    parameter_close = "</" + "parameter>"
    lines = raw_output.strip().splitlines()
    blocks: list[list[str]] = []
    current: list[str] | None = None
    for line in lines:
        if current is None:
            if line == QWEN_TOOL_CALL_FENCE_OPEN:
                current = [line]
            elif line.strip():
                return None
        else:
            current.append(line)
            if line == QWEN_TOOL_CALL_FENCE_CLOSE:
                blocks.append(current)
                current = None
    if current is not None or len(blocks) < 2:
        return None
    names: list[str] = []
    for block in blocks:
        if len(block) < 4 or block[-2] != function_close:
            return None
        match = _MULTI_FUNCTION_LINE_RE.fullmatch(block[1])
        if match is None or parameter_close not in block:
            return None
        names.append(match.group(1))
    return names


def classify_qwen_tool_call_rejection(raw_output: str) -> str | None:


    if not isinstance(raw_output, str):
        return None
    text = raw_output.strip()
    if text.endswith("</s>"):
        text = text[:-4].rstrip()
    if QWEN_THINK_TAG_MARKER_1 in text or QWEN_THINK_TAG_MARKER_2 in text:
        return "qwen_xml_think_tag_in_response"
    if "<answer>" in text or "</answer>" in text:
        return "qwen_xml_reserved_tag_in_response"
    open_fences = text.count(QWEN_TOOL_CALL_FENCE_OPEN)
    close_fences = text.count(QWEN_TOOL_CALL_FENCE_CLOSE)
    if open_fences or close_fences:


        if open_fences != 1 or close_fences != 1:
            return "qwen_xml_tool_call_fence_miscounted"
    return None
