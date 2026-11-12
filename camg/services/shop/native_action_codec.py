from __future__ import annotations

import re
from typing import Any

_NATIVE_ACTION_PREFIX_RE = re.compile(r"\A(search|click)\[")

def parse_native_bracket_action(text: str) -> tuple[str, str] | None:

    if not isinstance(text, str) or "\n" in text or "\r" in text:
        return None
    prefix = _NATIVE_ACTION_PREFIX_RE.match(text)
    if prefix is None:
        return None

    depth = 1
    argument_start = prefix.end()
    for index in range(argument_start, len(text)):
        char = text[index]
        if char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
            if depth == 0:
                if index != len(text) - 1:
                    return None
                return prefix.group(1), text[argument_start:index]
            if depth < 0:
                return None
    return None

def parse_memoryarena_native_action(action: Any) -> tuple[Any, str | None]:

    if not isinstance(action, str):
        return action, None
    parsed = parse_native_bracket_action(action)
    if parsed is None:
        return action, None
    return parsed
