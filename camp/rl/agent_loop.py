"""Sample multi-step trajectories while preserving token probabilities across context changes."""
from __future__ import annotations

import fcntl
import hashlib
import json
import os
import re
import time
from collections.abc import Mapping, Sequence
from copy import deepcopy
from typing import Any
from uuid import uuid4

import numpy as np
from camg.controller import (
    PolicyContextCapacityExceeded,
    bind_initial_policy_context,
    complete_policy_turn,
    prepare_policy_turn,
)
from verl.experimental.agent_loop.agent_loop import (
    AgentLoopBase,
    AgentLoopMetrics,
    AgentLoopOutput,
    register,
)
from verl.experimental.agent_loop.tool_parser import FunctionCall, ToolParser
from verl.tools.schemas import OpenAIFunctionToolSchema
from verl.utils.tokenizer import normalize_token_ids
from verl.workers.rollout.replica import TokenOutput

from camp.env_client import create_env_client
from camp.routes import RouteSpec, route_registry_from_agentgym_config

def _get(config: Any, key: str, default: Any = None) -> Any:
    if isinstance(config, Mapping):
        return config.get(key, default)
    getter = getattr(config, "get", None)
    if callable(getter):
        return getter(key, default)
    return getattr(config, key, default)

def _scalar(value: Any) -> Any:
    if isinstance(value, np.ndarray) and value.ndim == 0:
        return value.item()
    return (
        value.item()
        if hasattr(value, "item") and not isinstance(value, (str, bytes))
        else value
    )

_WDIMG_MARKER_RE = re.compile(
    r"\[\[WDIMG:(data:image/jpeg;base64,[A-Za-z0-9+/=]+)\]\]"
)

def _split_preview_markers(text: str) -> tuple[str, list[str]]:

    images: list[str] = []
    parts: list[str] = []
    last = 0
    for match in _WDIMG_MARKER_RE.finditer(text):
        parts.append(text[last : match.start()])
        images.append(match.group(1))
        last = match.end()
    parts.append(text[last:])
    return "".join(parts), images

def _observation_content(text: str) -> Any:

    if _WDIMG_MARKER_RE.search(text) is None:
        return text
    body, images = _split_preview_markers(text)
    blocks: list[dict[str, Any]] = [
        {"type": "text", "text": body if body else "(image observation)"}
    ]
    for uri in images:
        blocks.append({"type": "image_url", "image_url": {"url": uri}})
    return blocks

def _convert_messages_mm(
    messages: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:

    converted: list[dict[str, Any]] = []
    for message in messages:
        content = message.get("content")
        if isinstance(content, str) and _WDIMG_MARKER_RE.search(content) is not None:
            converted.append(
                {
                    "role": message.get("role"),
                    "content": _observation_content(content),
                }
            )
        else:
            converted.append(dict(message))
    return converted

def _extract_image_data(
    messages: Sequence[Mapping[str, Any]],
) -> list[str] | None:

    images: list[str] = []
    for message in messages:
        content = message.get("content")
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "image_url":
                    url = (block.get("image_url") or {}).get("url")
                    if isinstance(url, str):
                        images.append(url)
    return images or None

def _strip_preview_markers_text(value: Any) -> Any:

    if isinstance(value, str) and _WDIMG_MARKER_RE.search(value) is not None:
        return _split_preview_markers(value)[0]
    return value

def _messages(value: Sequence[Mapping[str, Any]]) -> list[dict[str, str]]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise TypeError("AMG raw_prompt must be a sequence of policy messages")
    normalized: list[dict[str, str]] = []
    for index, message in enumerate(value):
        if not isinstance(message, Mapping):
            raise TypeError(f"AMG policy message {index} is not a mapping")
        role = message.get("role")
        content = message.get("content")
        if role not in {"system", "user", "assistant"} or not isinstance(content, str):
            raise ValueError(
                f"invalid AMG policy message at index {index}: {message!r}"
            )
        normalized.append({"role": str(role), "content": content})
    if not normalized:
        raise ValueError("AMG raw_prompt must not be empty")
    return normalized

def _policy_tool_schemas(client: Any) -> list[dict[str, Any]] | None:
    provider = getattr(client, "policy_tool_schemas", None)
    if not callable(provider):
        return None
    raw_schemas = provider()
    if raw_schemas is None:
        return None
    if isinstance(raw_schemas, (str, bytes)) or not isinstance(
        raw_schemas, Sequence
    ):
        raise TypeError("AMG policy tool schemas must be a sequence of mappings")

    schemas: list[dict[str, Any]] = []
    names: set[str] = set()
    for index, raw_schema in enumerate(raw_schemas):
        if not isinstance(raw_schema, Mapping):
            raise TypeError(f"AMG policy tool schema {index} is not a mapping")
        schema = deepcopy(dict(raw_schema))
        function = schema.get("function")
        if schema.get("type") != "function" or not isinstance(function, Mapping):
            raise ValueError(
                f"AMG policy tool schema {index} is not an OpenAI function schema"
            )
        name = function.get("name")
        if not isinstance(name, str) or not name:
            raise ValueError(f"AMG policy tool schema {index} has no function name")
        if name in names:
            raise ValueError(f"AMG policy tool schema repeats function {name!r}")
        names.add(name)
        schemas.append(schema)
    if not schemas:
        raise ValueError("AMG policy tool schemas must not be empty")
    return schemas

def _tool_schema_digest(tools: Sequence[Mapping[str, Any]] | None) -> str:
    payload = json.dumps(
        list(tools or []),
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()

def _is_prefix(
    prefix: Sequence[Mapping[str, str]], values: Sequence[Mapping[str, str]]
) -> bool:
    return len(prefix) <= len(values) and all(
        dict(left) == dict(right) for left, right in zip(prefix, values)
    )

def _json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, Mapping):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    return repr(value)

def _digest_token_ids(token_ids: Sequence[int]) -> str:
    payload = ",".join(str(int(token_id)) for token_id in token_ids).encode("ascii")
    return hashlib.sha256(payload).hexdigest()

_THINK_OPEN = "<" + "think" + ">"
_THINK_CLOSE = "</" + "think" + ">"
_THINK_HEAD_CALL_MARKERS = (
    "<" + "function",  
    "<" + "tool_call",  
)

_THINK_STRIP_LOG = os.path.join(os.environ.get("CAMP_STATE_DIR", "/tmp/camp"), "think_strip_events.log")

def _record_think_strip(removed_chars: int) -> None:

    try:
        with open(_THINK_STRIP_LOG, "a", encoding="utf-8") as fh:
            fh.write(f"{removed_chars}\n")
    except OSError:
        pass

_QWEN_NATIVE_TOOL_TEMPLATE_REPLACEMENTS = (
    (
        "If you choose to call a function ONLY reply in the following format "
        "with NO suffix:",
        "For every response, call at least one function and reply with each call in the following format; plain-prose reasoning may precede the calls, and nothing may follow them; independent calls may be issued together in one response, one block after another, and the environment executes them in order:",
    ),
    (
        "- If there is no function call available, answer the question like "
        "normal with your current knowledge and do not tell the user about "
        "function calls",
        "- Always select at least one available function; never answer in prose; several functions may be called in one response",
    ),
)

def _strip_leading_think(text: str) -> str:

    stripped = text.lstrip()
    if stripped.startswith(_THINK_OPEN):
        cut = stripped.rfind(_THINK_CLOSE)
        if cut == -1:
            return text
        _record_think_strip(len(stripped[: cut + len(_THINK_CLOSE)]))
        return stripped[cut + len(_THINK_CLOSE) :].lstrip()
    cut = stripped.find(_THINK_CLOSE)
    if cut == -1:
        return text
    head = stripped[:cut]
    if any(marker in head for marker in _THINK_HEAD_CALL_MARKERS):
        return text
    _record_think_strip(cut + len(_THINK_CLOSE))
    return stripped[cut + len(_THINK_CLOSE) :].lstrip()

def _strict_qwen_tool_chat_template(template: Any) -> str:

    if not isinstance(template, str) or not template:
        raise RuntimeError("AMG native tools require a nonempty Qwen chat template")
    patched = template
    for old, new in _QWEN_NATIVE_TOOL_TEMPLATE_REPLACEMENTS:
        count = patched.count(old)
        if count != 1:
            raise RuntimeError(
                "AMG pinned Qwen tool-template clause drifted: "
                f"expected one occurrence, found {count}: {old!r}"
            )
        patched = patched.replace(old, new, 1)
    return patched

def _native_tool_observation_messages(
    messages: Sequence[Mapping[str, Any]],
    *,
    expected_assistant_messages: Sequence[Mapping[str, Any]],
    tool_name: str,
    observation: str,
) -> list[dict[str, Any]]:

    normalized = [dict(message) for message in messages]
    assistant_prefix = [dict(message) for message in expected_assistant_messages]
    if (
        len(normalized) != len(assistant_prefix) + 1
        or normalized[:-1] != assistant_prefix
        or normalized[-1].get("role") != "user"
        or normalized[-1].get("content") != observation
    ):
        raise RuntimeError(
            "AMG native tool lifecycle must append exactly one observation after "
            "the sampled assistant call"
        )
    if not isinstance(tool_name, str) or not tool_name:
        raise ValueError("AMG native tool observation requires a tool name")
    normalized[-1] = {
        "role": "tool",
        "name": tool_name,
        "content": observation,
    }
    return normalized

def _parallel_call_slices(
    response_ids_count: int,
    blocks: Sequence[tuple[int, int]],
    dispatched_count: int,
) -> list[tuple[int, int]]:

    if dispatched_count < 1 or dispatched_count > len(blocks):
        raise ValueError(
            "AMG parallel-call slicing requires 1..len(blocks) dispatched "
            f"calls: dispatched={dispatched_count} blocks={len(blocks)}"
        )
    previous_end = -1
    slices: list[tuple[int, int]] = []
    for start, end in blocks[:dispatched_count]:
        if start <= previous_end or end < start or end >= response_ids_count:
            raise ValueError(
                "AMG parallel-call slice bounds overlap or exceed the "
                "response: "
                f"start={start} end={end} previous_end={previous_end} "
                f"response_tokens={response_ids_count}"
            )
        slices.append((previous_end + 1, end))
        previous_end = end
    last_start, _ = slices[-1]
    slices[-1] = (last_start, response_ids_count - 1)
    return slices

def _slice_routed_experts(routed_experts: Any, start: int, end: int) -> Any:
    if routed_experts is None:
        return None
    if isinstance(routed_experts, (list, tuple)):
        return type(routed_experts)(routed_experts[start:end])
    return routed_experts[start:end]

_OUTPUT_CAP_NOTICE_TEMPLATE = (
    "[AMG output-cap notice] Your previous response was cut off at the "
    "per-turn output-token limit: sampling stopped mid-stream after "
    "{tokens} tokens (limit {budget}), so anything you intended after the "
    "cut was never generated or executed. Only the complete text above "
    "was dispatched, and the observation above is its full result. "
    "Continue with smaller steps: split long content across turns rather "
    "than resending the same long output."
)

def _annotate_output_cap_truncation(
    messages: Sequence[Mapping[str, Any]],
    *,
    stop_reason: Any,
    response_tokens: int,
    response_budget: int,
) -> list[dict[str, Any]]:

    annotated = [dict(message) for message in messages]
    if stop_reason != "length" or not annotated:
        return annotated
    if annotated[-1].get("role") not in {"user", "tool"}:
        return annotated
    content = str(annotated[-1].get("content") or "")
    notice = _OUTPUT_CAP_NOTICE_TEMPLATE.format(
        tokens=int(response_tokens), budget=int(response_budget)
    )
    annotated[-1]["content"] = content + "\n\n" + notice if content else notice
    return annotated

def _merged_parallel_turn_messages(
    prepared_messages: Sequence[Mapping[str, Any]],
    action: str,
    call_states: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[bool]]:

    merged = [dict(message) for message in prepared_messages]
    merged.append({"role": "assistant", "content": action})
    native_flags: list[bool] = []
    for call_state in call_states:
        call_done = bool(call_state.get("done") or call_state.get("contained"))
        native = False
        transition = call_state.get("context_transition") or {}
        if transition.get("operation") == "append_observation":
            observation = str(call_state["step_output"].state)
            merged.append({"role": "user", "content": observation})
            if call_state.get("name") is not None and not call_done:
                merged[-1] = {
                    "role": "tool",
                    "name": call_state["name"],
                    "content": observation,
                }
                native = True
        elif transition.get("operation") == "replace_messages":
            merged = [
                dict(message) for message in call_state["next_messages"]
            ]
        native_flags.append(native)
    return merged, native_flags

_EXCLUSION_CONTAINMENT_CAP = 32

_EXCLUSION_RATE_MIN_SAMPLES = 8
_EXCLUSION_RATE_MAX_EXCLUDED_FRACTION = 0.5

_STRAGGLER_STEP_SLACK = 8

_ANSWER_INJECTION_REDLINE_COUNT = 2

try:  
    import requests as _requests

    _ROUTE_TRANSPORT_EXCEPTIONS: tuple[type[BaseException], ...] = (
        _requests.RequestException,
    )
except ImportError:  
    _ROUTE_TRANSPORT_EXCEPTIONS = ()

def _route_client_interaction(description: str, call: Any, /, *args: Any, **kwargs: Any) -> Any:

    try:
        return call(*args, **kwargs)
    except _ROUTE_TRANSPORT_EXCEPTIONS as exc:
        raise _SampleExcluded(
            f"route transport failure during {description}: {exc}"
        ) from exc

def _exclusion_rate_state_path() -> str:
    return os.environ.get(
        "AMG_EXCLUSION_RATE_FILE",
        os.path.join(os.environ.get("CAMP_STATE_DIR", "/tmp/camp"), "exclusion_rate.json"),
    )

def _exclusion_bucket_breached(bucket: Mapping[str, int]) -> bool:

    attempts = int(bucket.get("attempts", 0))
    excluded = int(bucket.get("excluded", 0))
    return (
        attempts >= _EXCLUSION_RATE_MIN_SAMPLES
        and excluded > _EXCLUSION_RATE_MAX_EXCLUDED_FRACTION * attempts
    )

def _record_sample_outcome(global_step: int, *, excluded: bool) -> bool:

    live_bucket = {"excluded": 0, "attempts": 0}
    try:
        with open(_exclusion_rate_state_path(), "a+") as state_file:
            fcntl.flock(state_file, fcntl.LOCK_EX)
            try:
                state_file.seek(0)
                raw = state_file.read().strip()
                try:
                    loaded = json.loads(raw) if raw else {}
                except json.JSONDecodeError:
                    loaded = {}
                steps: dict[str, dict[str, int]] = {}
                if isinstance(loaded, dict) and isinstance(
                    loaded.get("steps"), dict
                ):
                    for step_key, bucket in loaded["steps"].items():
                        try:
                            step_number = int(step_key)
                        except (TypeError, ValueError):
                            continue
                        if isinstance(bucket, dict):
                            try:
                                steps[str(step_number)] = {
                                    "excluded": int(bucket.get("excluded", 0)),
                                    "attempts": int(bucket.get("attempts", 0)),
                                }
                            except (TypeError, ValueError):

                                continue
                max_step_written = 0
                if isinstance(loaded, dict):
                    raw_max = loaded.get("max_step_written")
                    try:
                        max_step_written = int(raw_max)
                    except (TypeError, ValueError):
                        max_step_written = 0
                if global_step > max_step_written:
                    max_step_written = global_step

                effective_watermark = max_step_written
                if steps:
                    effective_watermark = max(
                        effective_watermark, max(int(k) for k in steps)
                    )
                if effective_watermark - global_step > _STRAGGLER_STEP_SLACK:

                    print(
                        "[AMG exclusion-rate reset] step=%s watermark=%s "
                        "(previous-run residue detected); tally reset"
                        % (global_step, effective_watermark),
                        flush=True,
                    )
                    steps = {}
                    max_step_written = global_step
                live_bucket = steps.setdefault(
                    str(global_step), {"excluded": 0, "attempts": 0}
                )
                live_bucket["excluded"] += int(excluded)
                live_bucket["attempts"] += 1

                for stale_step in sorted(steps, key=int)[:-2]:
                    if stale_step in steps and stale_step != str(global_step):
                        del steps[stale_step]
                state_file.seek(0)
                state_file.truncate()
                state_file.write(
                    json.dumps(
                        {"steps": steps, "max_step_written": max_step_written}
                    )
                )
                state_file.flush()
                os.fsync(state_file.fileno())
            finally:
                fcntl.flock(state_file, fcntl.LOCK_UN)
    except OSError:
        
        return False
    excluded_count = live_bucket["excluded"]
    attempts = live_bucket["attempts"]
    breached = _exclusion_bucket_breached(live_bucket)
    if breached and excluded:
        print(
            "[AMG exclusion-rate breach] step=%s excluded=%d/%d "
            "(>%.0f%% after >=%d samples); environment endpoints are "
            "systemically broken — escalating to fast-fail"
            % (
                global_step,
                excluded_count,
                attempts,
                _EXCLUSION_RATE_MAX_EXCLUDED_FRACTION * 100,
                _EXCLUSION_RATE_MIN_SAMPLES,
            ),
            flush=True,
        )
    return breached

def _answer_injection_state_path() -> str:
    return os.environ.get(
        "AMG_ANSWER_INJECTION_FILE",
        os.path.join(os.environ.get("CAMP_STATE_DIR", "/tmp/camp"), "answer_injection.json"),
    )

def check_exclusion_fast_fail(global_step: int | None) -> None:

    if global_step is None:
        return
    try:
        with open(_exclusion_rate_state_path(), "r") as state_file:
            fcntl.flock(state_file, fcntl.LOCK_SH)
            try:
                state_file.seek(0)
                raw = state_file.read().strip()
            finally:
                fcntl.flock(state_file, fcntl.LOCK_UN)
    except OSError:

        return
    try:
        loaded = json.loads(raw) if raw else {}
    except json.JSONDecodeError:
        return
    if not isinstance(loaded, dict):
        return
    steps: dict[str, dict[str, int]] = {}
    raw_steps = loaded.get("steps")
    if isinstance(raw_steps, dict):
        for step_key, bucket in raw_steps.items():
            try:
                step_number = int(step_key)
            except (TypeError, ValueError):
                continue
            if isinstance(bucket, dict):
                try:
                    steps[str(step_number)] = {
                        "excluded": int(bucket.get("excluded", 0)),
                        "attempts": int(bucket.get("attempts", 0)),
                    }
                except (TypeError, ValueError):
                    continue
    if not steps:
        return
    watermark = 0
    try:
        watermark = int(loaded.get("max_step_written"))
    except (TypeError, ValueError):
        watermark = 0
    watermark = max(watermark, max(int(key) for key in steps))
    if watermark - global_step > _STRAGGLER_STEP_SLACK:

        return
    for step_key in sorted(steps, key=int):
        bucket = steps[step_key]
        if _exclusion_bucket_breached(bucket):
            raise RuntimeError(
                "AMG X-1a exclusion fast-fail escalated to run level (D1): "
                f"step {step_key} tally is {bucket['excluded']} excluded of "
                f"{bucket['attempts']} settled samples (> "
                f"{_EXCLUSION_RATE_MAX_EXCLUDED_FRACTION:.0%} threshold after "
                f">= {_EXCLUSION_RATE_MIN_SAMPLES} samples); under the TQ "
                "architecture the per-sample fast-fail is swallowed as a "
                "per-uid failure and the replay buffer would evict-and-refill "
                "forever — stopping the run instead"
            )

def _record_answer_injection(global_step: int, *, flagged: bool) -> bool:

    live_bucket = {"flagged": 0, "answers": 0}
    previous_bucket_flagged = 0
    try:
        with open(_answer_injection_state_path(), "a+") as state_file:
            fcntl.flock(state_file, fcntl.LOCK_EX)
            try:
                state_file.seek(0)
                raw = state_file.read().strip()
                try:
                    loaded = json.loads(raw) if raw else {}
                except json.JSONDecodeError:
                    loaded = {}
                steps: dict[str, dict[str, int]] = {}
                if isinstance(loaded, dict) and isinstance(
                    loaded.get("steps"), dict
                ):
                    for step_key, bucket in loaded["steps"].items():
                        try:
                            step_number = int(step_key)
                        except (TypeError, ValueError):
                            continue
                        if isinstance(bucket, dict):
                            try:
                                steps[str(step_number)] = {
                                    "flagged": int(bucket.get("flagged", 0)),
                                    "answers": int(bucket.get("answers", 0)),
                                }
                            except (TypeError, ValueError):
                                continue
                max_step_written = 0
                if isinstance(loaded, dict):
                    raw_max = loaded.get("max_step_written")
                    try:
                        max_step_written = int(raw_max)
                    except (TypeError, ValueError):
                        max_step_written = 0
                if global_step > max_step_written:
                    max_step_written = global_step
                effective_watermark = max_step_written
                if steps:
                    effective_watermark = max(
                        effective_watermark, max(int(k) for k in steps)
                    )
                if effective_watermark - global_step > _STRAGGLER_STEP_SLACK:

                    print(
                        "[AMG answer-injection reset] step=%s watermark=%s "
                        "(previous-run residue detected); tally reset"
                        % (global_step, effective_watermark),
                        flush=True,
                    )
                    steps = {}
                    max_step_written = global_step
                live_bucket = steps.setdefault(
                    str(global_step), {"flagged": 0, "answers": 0}
                )
                live_bucket["flagged"] += int(bool(flagged))
                live_bucket["answers"] += 1

                for stale_step in sorted(steps, key=int)[:-2]:
                    if stale_step in steps and stale_step != str(global_step):
                        del steps[stale_step]
                retained = sorted(steps, key=int)

                other_updates = [
                    key for key in retained if key != str(global_step)
                ]
                if other_updates:
                    previous_bucket_flagged = int(
                        steps[other_updates[-1]].get("flagged", 0)
                    )
                state_file.seek(0)
                state_file.truncate()
                state_file.write(
                    json.dumps(
                        {"steps": steps, "max_step_written": max_step_written}
                    )
                )
                state_file.flush()
                os.fsync(state_file.fileno())
            finally:
                fcntl.flock(state_file, fcntl.LOCK_UN)
    except OSError:
        
        return False
    flagged_count = live_bucket["flagged"]
    answers = live_bucket["answers"]
    if flagged:
        print(
            "[AMG answer-injection marker] step=%s flagged=%d/%d answers "
            "(LR judge prompt injection monitor, P2-10)"
            % (global_step, flagged_count, answers),
            flush=True,
        )
    redline = (
        flagged_count >= _ANSWER_INJECTION_REDLINE_COUNT
        or (flagged_count >= 1 and previous_bucket_flagged >= 1)
    )
    if redline:
        print(
            "[AMG LR JUDGE-INJECTION REDLINE] step=%s flagged=%d/%d answers "
            "this update, previous-update flagged=%d — the policy may be "
            "learning to address the judge; inspect this update's answers "
            "before continuing the run"
            % (global_step, flagged_count, answers, previous_bucket_flagged),
            flush=True,
        )
    return redline

def _record_answer_injection_outcome(global_step: int, outputs: Any) -> None:

    try:
        for output in outputs:
            extra = getattr(output, "extra_fields", None)
            if not isinstance(extra, Mapping):
                continue
            wrapper_evidence = extra.get("wrapper_evidence")
            if not isinstance(wrapper_evidence, Mapping):
                continue
            scan = wrapper_evidence.get("answer_injection_scan")
            if isinstance(scan, Mapping):
                _record_answer_injection(
                    global_step, flagged=bool(scan.get("flagged"))
                )
                return
    except Exception:
        
        return

def _exclusion_budget_path() -> str:
    return os.environ.get(
        "AMG_EXCLUSION_BUDGET_FILE",
        os.path.join(os.environ.get("CAMP_STATE_DIR", "/tmp/camp"), "exclusion_budget.json"),
    )

_NATIVE_SHAPE_FALLBACK_COUNT = os.path.join(os.environ.get("CAMP_STATE_DIR", "/tmp/camp"), "tool_shape_fallback.count")
_NATIVE_SHAPE_FALLBACK_FIRST = os.path.join(os.environ.get("CAMP_STATE_DIR", "/tmp/camp"), "tool_shape_fallback_first.txt")

def _record_native_shape_fallback(action: str) -> None:

    stamp = time.strftime("%Y-%m-%dT%H:%M:%S")
    try:
        with open(_NATIVE_SHAPE_FALLBACK_COUNT, "a") as fh:
            fh.write("%s pid=%d len=%d\n" % (stamp, os.getpid(), len(action)))
        if not os.path.exists(_NATIVE_SHAPE_FALLBACK_FIRST):
            with open(_NATIVE_SHAPE_FALLBACK_FIRST, "x") as fh:
                fh.write("%s pid=%d\n" % (stamp, os.getpid()))
                fh.write(action[:20000])
                fh.write("\n")
    except OSError:
        pass

def _finalize_amg_trajectory(
    rows: list[dict[str, Any]], outputs: list["AgentLoopOutput"]
) -> list["AgentLoopOutput"]:

    trajectory_return = sum(float(row["immediate_reward"]) for row in rows)
    for index, (row, output) in enumerate(zip(rows, outputs, strict=True)):
        terminal = index == len(rows) - 1
        row["trajectory_terminal"] = terminal
        row["trajectory_return"] = trajectory_return
        output.extra_fields["trajectory_terminal"] = terminal
        output.extra_fields["trajectory_return"] = trajectory_return
        step_record_json = json.dumps(
            _json_safe(row),
            ensure_ascii=True,
            sort_keys=True,
            separators=(",", ":"),
        )
        output.extra_fields["step_record_json"] = step_record_json

        output.extra_fields["reward_extra_info"] = {
            "step_record_json": step_record_json,
            "is_padding": False,
        }
    return outputs

def _contain_excluded_sample(
    loop: Any, sample_reschedule_attempt: int, item_id: str, data_idx: int
) -> int | None:

    max_retries = int(_get(loop.agentgym_config, "max_retries", 2))
    if sample_reschedule_attempt < max_retries:
        return None
    try:
        with open(_exclusion_budget_path(), "a+") as budget:
            fcntl.flock(budget, fcntl.LOCK_EX)
            try:
                budget.seek(0)
                raw = budget.read().strip()
                used = int(raw) if raw.isdigit() else 0
                if used >= _EXCLUSION_CONTAINMENT_CAP:
                    return None
                budget.seek(0)
                budget.truncate()
                budget.write(str(used + 1))
                budget.flush()
                os.fsync(budget.fileno())
            finally:
                fcntl.flock(budget, fcntl.LOCK_UN)
    except OSError:
        return None
    print(
        "[AMG exclusion containment] item_id=%r data_idx=%s attempt=%d "
        "contained as neutral terminal trajectory (budget %d/%d)"
        % (
            item_id,
            data_idx,
            sample_reschedule_attempt,
            used + 1,
            _EXCLUSION_CONTAINMENT_CAP,
        ),
        flush=True,
    )
    return used + 1

class _SampleExcluded(Exception):

    def __init__(self, summary: str) -> None:
        super().__init__(summary)
        self.summary = summary

def _sample_exclusion_summary(step_output: Any) -> str:
    payload = {
        "state": _json_safe(
            _strip_preview_markers_text(getattr(step_output, "state", None))
        ),
        "info": _json_safe(getattr(step_output, "info", {})),
    }
    encoded = json.dumps(
        payload,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    )
    return encoded[:2048]

_S15_CLIENT_CONTRACT_ERRORS = frozenset(
    {
        "LiteResearcher invalid action cannot also be sample_excluded",
        "LiteResearcher invalid-action overlay requires zero native reward",
    }
)

_S15_EXCLUSION_REASON = "s1_5_invalid_action_contract"

def _contain_s15_client_contract_error(
    loop: Any,
    exc: RuntimeError,
    *,
    route_id: str,
    item_id: str,
    data_idx: int,
    sample_reschedule_attempt: int,
    rows: list[dict[str, Any]],
    outputs: list["AgentLoopOutput"],
) -> list["AgentLoopOutput"]:

    print(
        "[AMG S1-5 controlled exclusion] route=%s item_id=%r data_idx=%s "
        "attempt=%d emitted_rows=%d error=%s"
        % (
            route_id,
            item_id,
            data_idx,
            sample_reschedule_attempt,
            len(rows),
            exc,
        ),
        flush=True,
    )
    summary = (
        "S1-5 controlled exclusion (invalid-action contract violation): "
        f"{exc}"
    )
    max_retries = int(_get(loop.agentgym_config, "max_retries", 2))
    unrecoverable = (
        summary
        + " — reschedule budget exhausted and the exclusion containment "
        "budget cannot absorb this sample: unrecoverable exclusion path"
    )
    if not rows or not outputs:
        raise _SampleExcluded(
            summary if sample_reschedule_attempt < max_retries else unrecoverable
        ) from exc
    if not _contain_excluded_sample(
        loop, sample_reschedule_attempt, item_id, data_idx
    ):
        raise _SampleExcluded(
            summary if sample_reschedule_attempt < max_retries else unrecoverable
        ) from exc
    rows[-1]["outcome"] = "environment_infrastructure_failure"
    rows[-1]["exclusion_contained"] = True
    rows[-1]["rollout_done_flag"] = True
    rows[-1]["exclusion_reason"] = _S15_EXCLUSION_REASON
    outputs[-1].extra_fields.update(
        {
            "outcome": "environment_infrastructure_failure",
            "rollout_done_flag": True,
            "exclusion_contained": True,
            "exclusion_reason": _S15_EXCLUSION_REASON,
        }
    )
    return _finalize_amg_trajectory(rows, outputs)

def _receipt_parts(
    step_output: Any, action: str
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    info = getattr(step_output, "info", {})
    info = dict(info) if isinstance(info, Mapping) else {}
    env_info = info.get("env_info", info.get("info", {}))
    action_submission = info.get("action_submission", {"raw_policy_output": action})
    context_transition = info.get("context_transition", {})
    wrapper_evidence = info.get("wrapper_evidence", {})
    return (
        deepcopy(dict(env_info)) if isinstance(env_info, Mapping) else {},
        deepcopy(dict(action_submission))
        if isinstance(action_submission, Mapping)
        else {},
        {
            "context_transition": deepcopy(dict(context_transition))
            if isinstance(context_transition, Mapping)
            else {},
            "wrapper_evidence": deepcopy(dict(wrapper_evidence))
            if isinstance(wrapper_evidence, Mapping)
            else {},
        },
    )

def _outcome(
    *,
    done: bool,
    reward: float,
    env_info: Mapping[str, Any],
    wrapper_evidence: Mapping[str, Any],
) -> str:

    if not done:
        return "continue"
    if wrapper_evidence.get("outcome") == "environment_error":
        return "environment_error"
    if env_info.get("episode_success") is True or env_info.get("resolved") is True:
        return "success"
    if env_info.get("episode_success") is False or env_info.get("resolved") is False:
        return "terminal_failure"
    return "terminal_failure"

@register("amg_task_neutral_async")
class AMGTaskNeutralAgentLoop(AgentLoopBase):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.agentgym_config = self.config.actor_rollout_ref.get("agentgym")
        if self.agentgym_config is None:
            raise ValueError(
                "AMGTaskNeutralAgentLoop requires actor_rollout_ref.agentgym"
            )
        self._route_registry = route_registry_from_agentgym_config(
            self.agentgym_config
        )
        self._envelope_tokens_by_tool_schema: dict[str, int] = {}
        self._typed_tool_schemas_by_digest: dict[
            str, tuple[OpenAIFunctionToolSchema, ...]
        ] = {}
        self._native_tool_parser = ToolParser.get_tool_parser(
            "qwen3_coder", self.tokenizer
        )
        self._native_tool_template_sha256: str | None = None
        multi_turn_config = getattr(self.rollout_config, "multi_turn", None)
        self._max_parallel_calls = 4
        if multi_turn_config is not None:
            raw_parallel = getattr(multi_turn_config, "max_parallel_calls", None)
            if raw_parallel is not None:
                self._max_parallel_calls = int(raw_parallel)
        if self._max_parallel_calls < 1:
            raise ValueError(
                "AMG multi_turn.max_parallel_calls must be >= 1, got "
                f"{self._max_parallel_calls}"
            )
        self._native_tool_start_id: int | None = None
        self._native_tool_end_id: int | None = None
        if self._max_parallel_calls > 1:
            self._native_tool_start_id = self._atomic_special_token_id(
                self._native_tool_parser.tool_call_start_token
            )
            self._native_tool_end_id = self._atomic_special_token_id(
                self._native_tool_parser.tool_call_end_token
            )

            print(
                "AMG parallel tool calls enabled: max_parallel_calls="
                f"{self._max_parallel_calls}",
                flush=True,
            )

        print(
            "AMG shared turn budget: counting=turns "
            f"parallel_calls_cap={self._max_parallel_calls}",
            flush=True,
        )

    def _activate_native_tool_template(
        self, tools: Sequence[Mapping[str, Any]] | None
    ) -> None:
        if not tools or self._native_tool_template_sha256 is not None:
            return
        builder_kwargs = dict(self.continuous_token_builder.chat_template_kwargs)
        source_template = builder_kwargs.get(
            "chat_template", getattr(self.tokenizer, "chat_template", None)
        )
        strict_template = _strict_qwen_tool_chat_template(source_template)
        builder_kwargs["chat_template"] = strict_template
        self.continuous_token_builder.chat_template_kwargs = builder_kwargs
        self._native_tool_template_sha256 = hashlib.sha256(
            strict_template.encode("utf-8")
        ).hexdigest()

    def _typed_tool_schemas(
        self, tools: Sequence[Mapping[str, Any]]
    ) -> tuple[OpenAIFunctionToolSchema, ...]:
        digest = _tool_schema_digest(tools)
        typed = self._typed_tool_schemas_by_digest.get(digest)
        if typed is None:
            typed = tuple(
                OpenAIFunctionToolSchema.model_validate(dict(schema))
                for schema in tools
            )
            self._typed_tool_schemas_by_digest[digest] = typed
        return typed

    async def _validated_native_tool_call(
        self,
        *,
        response_ids: list[int],
        action: str,
        tools: Sequence[Mapping[str, Any]] | None,
        action_submission: Mapping[str, Any],
    ) -> FunctionCall | None:

        if action_submission.get("tool_parser_normalized") is not True:
            return None
        if not tools:
            raise RuntimeError(
                "AMG wrapper accepted a native tool call without tool schemas"
            )
        opening = "<tool_call>"
        closing = "</tool_call>"
        lowered = action.lower()
        if (
            action.count(opening) != 1
            or action.count(closing) != 1
            or action.find(opening) > action.find(closing)
            or "<think" in lowered
            or "</think" in lowered
        ):

            _record_native_shape_fallback(action)
            print(
                "[AMG native shape fallback] accepted action len=%d failed the "
                "naive tag-shape check; continuing via observation path"
                % len(action)
            )
            return None
        _content, calls = await self._native_tool_parser.extract_tool_calls(
            response_ids, list(self._typed_tool_schemas(tools))
        )
        if len(calls) != 1:
            raise RuntimeError(
                "AMG wrapper/native veRL parser disagreement for an accepted action"
            )
        allowed_names = {
            str(schema["function"]["name"])
            for schema in tools
        }
        if calls[0].name not in allowed_names:
            raise RuntimeError(
                "AMG wrapper accepted an action outside the native tool schema: "
                f"{calls[0].name!r}"
            )
        return calls[0]

    def _atomic_special_token_id(self, token_text: str) -> int:
        encoded = self.tokenizer.encode(token_text, add_special_tokens=False)
        if len(encoded) != 1:
            raise ValueError(
                "AMG parallel tool calls require single-token call delimiters: "
                f"{token_text!r} encoded to {len(encoded)} tokens"
            )
        return int(encoded[0])

    def _scan_tool_call_blocks(
        self, response_ids: list[int]
    ) -> list[tuple[int, int]]:

        if self._native_tool_start_id is None or self._native_tool_end_id is None:
            return []
        blocks: list[tuple[int, int]] = []
        index = 0
        total = len(response_ids)
        while index < total:
            if response_ids[index] != self._native_tool_start_id:
                index += 1
                continue
            end = index + 1
            while end < total and response_ids[end] != self._native_tool_end_id:
                end += 1
            if end >= total:
                break
            blocks.append((index, end))
            index = end + 1
        return blocks

    def _prompt_mm_data(
        self, messages: Sequence[Mapping[str, Any]]
    ) -> dict[str, Any] | None:

        images = _extract_image_data(_convert_messages_mm(messages))
        if not images:
            return None
        return {"images": list(images)}

    def _builder_mm_kwargs(self) -> dict[str, Any] | None:

        kwargs = getattr(self.continuous_token_builder, "mm_processor_kwargs", None)
        return dict(kwargs) if kwargs else None

    def _render_prompt_sync(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> list[int]:

        converted = _convert_messages_mm(messages)
        return normalize_token_ids(
            self.continuous_token_builder.build_initial_tokens(
                converted,
                tools=tools,
                images=_extract_image_data(converted),
            )
        )

    def _prompt_for_candidate(
        self,
        current_messages: list[dict[str, Any]],
        current_prompt_ids: list[int],
        candidate_messages: Sequence[Mapping[str, str]],
        tools: list[dict[str, Any]] | None = None,
    ) -> list[int]:
        candidate = [dict(message) for message in candidate_messages]
        if candidate == current_messages:
            return list(current_prompt_ids)

        return self._render_prompt_sync(candidate, tools=tools)

    def _next_prompt_ids(
        self,
        *,
        prepared_messages: list[dict[str, Any]],
        prepared_prompt_ids: list[int],
        action: str,
        action_token_ids: list[int],
        next_messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> list[int]:
        assistant_messages = prepared_messages + [
            {"role": "assistant", "content": action}
        ]
        if _is_prefix(assistant_messages, next_messages) and len(next_messages) > len(
            assistant_messages
        ):
            appended = next_messages[len(assistant_messages) :]
            if all(message.get("role") != "assistant" for message in appended):
                assistant_runtime = (
                    self.continuous_token_builder.merge_assistant_tokens(
                        prepared_prompt_ids, action_token_ids
                    ).token_ids
                )
                next_prompt = normalize_token_ids(
                    self.continuous_token_builder.merge_context_tokens(
                        _convert_messages_mm(assistant_messages),
                        _convert_messages_mm(next_messages),
                        assistant_runtime,
                        tools=tools,
                    ).token_ids
                )
                return next_prompt

        return self._render_prompt_sync(next_messages, tools=tools)

    def _action_observation_envelope_tokens(
        self,
        messages: list[dict[str, Any]],
        prompt_ids: list[int],
        tools: list[dict[str, Any]] | None = None,
    ) -> int:
        schema_digest = _tool_schema_digest(tools)
        envelope_tokens = self._envelope_tokens_by_tool_schema.get(schema_digest)
        if envelope_tokens is None:
            observation_message: dict[str, Any] = {
                "role": "user",
                "content": "",
            }
            if tools:
                observation_message = {
                    "role": "tool",
                    "name": str(tools[0]["function"]["name"]),
                    "content": "",
                }
            empty_transition = messages + [
                {"role": "assistant", "content": ""},
                observation_message,
            ]
            envelope_tokens = len(
                self._render_prompt_sync(empty_transition, tools=tools)
            ) - len(prompt_ids)
            if envelope_tokens < 0:
                raise RuntimeError(
                    "AMG chat template shortened across an empty action/observation turn"
                )
            self._envelope_tokens_by_tool_schema[schema_digest] = envelope_tokens
        return envelope_tokens

    @staticmethod
    def _resolve_data_idx(kwargs: Mapping[str, Any]) -> int:
        value = kwargs.get("data_idx")
        if value is None:
            extra_info = kwargs.get("extra_info")
            if isinstance(extra_info, Mapping):
                value = extra_info.get("index")
        if value is None:
            value = kwargs.get("index")
        value = _scalar(value)
        if isinstance(value, (bool, np.bool_)):
            raise TypeError("AMG data_idx must be an integer, not bool")
        try:
            data_idx = int(value)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError(f"AMG data_idx is not an integer: {value!r}") from exc
        if data_idx < 0:
            raise ValueError(f"AMG data_idx must be non-negative, got {data_idx}")
        return data_idx

    @staticmethod
    def _resolve_trajectory_uid(kwargs: Mapping[str, Any]) -> str:
        raw_uid = _scalar(kwargs.get("uid"))
        if raw_uid is not None and str(raw_uid):
            return str(raw_uid)
        item_id = _scalar(kwargs.get("item_id"))
        return f"amg-{item_id}-{uuid4().hex}"

    async def run(
        self,
        sampling_params: dict[str, Any],
        priority: int = 0,
        **kwargs: Any,
    ) -> list[AgentLoopOutput]:
        max_retries = int(_get(self.agentgym_config, "max_retries", 2))
        if max_retries < 0:
            raise ValueError("AMG max_retries must be non-negative")

        route = self._route_registry.resolve_row(kwargs)
        attempt_kwargs = dict(kwargs)
        attempt_kwargs["uid"] = self._resolve_trajectory_uid(kwargs)
        data_idx = self._resolve_data_idx(kwargs)
        item_id = str(_scalar(kwargs.get("item_id", data_idx)))
        global_step = int(_scalar(kwargs.get("global_steps", -1)))
        last_exclusion: _SampleExcluded | None = None
        for sample_reschedule_attempt in range(max_retries + 1):
            try:
                outputs = await self._run_single_attempt(
                    sampling_params,
                    priority,
                    route=route,
                    sample_reschedule_attempt=sample_reschedule_attempt,
                    **attempt_kwargs,
                )
            except _SampleExcluded as exc:
                last_exclusion = exc
            else:

                _record_sample_outcome(global_step, excluded=False)

                _record_answer_injection_outcome(global_step, outputs)
                return outputs

        assert last_exclusion is not None
        if _record_sample_outcome(global_step, excluded=True):

            raise RuntimeError(
                f"AMG exclusion-rate fast-fail at step {global_step}: more "
                "than half of this step's samples ended in exclusion "
                f"(item_id={item_id!r} data_idx={data_idx} last exclusion: "
                f"{last_exclusion.summary}); the environment endpoints are "
                "systemically broken, not per-sample faulty."
            ) from last_exclusion
        raise RuntimeError(
            f"AMG sample item_id={item_id!r} data_idx={data_idx} was excluded after "
            f"{max_retries + 1} complete trajectory attempts: "
            f"{last_exclusion.summary}"
        ) from last_exclusion

    async def _run_single_attempt(
        self,
        sampling_params: dict[str, Any],
        priority: int = 0,
        *,
        route: RouteSpec,
        sample_reschedule_attempt: int,
        **kwargs: Any,
    ) -> list[AgentLoopOutput]:
        priority = int(_scalar(priority))
        data_idx = self._resolve_data_idx(kwargs)
        item_id = str(_scalar(kwargs.get("item_id", data_idx)))
        trajectory_uid = self._resolve_trajectory_uid(kwargs)
        raw_prompt = _messages(kwargs["raw_prompt"])

        response_budget = int(
            sampling_params.get("max_tokens", self.rollout_config.response_length)
        )
        if response_budget <= 0 or response_budget > int(
            self.rollout_config.response_length
        ):
            raise ValueError(
                "AMG sampling max_tokens must fit rollout.response_length: "
                f"sampling={response_budget} width={self.rollout_config.response_length}"
            )
        max_prompt_tokens = int(self.rollout_config.prompt_length)
        max_model_tokens = int(
            getattr(
                self.rollout_config,
                "max_model_len",
                max_prompt_tokens + int(self.rollout_config.response_length),
            )
        )
        sampling_params = dict(sampling_params)
        sampling_params["max_tokens"] = response_budget
        eos_token_id = getattr(self.tokenizer, "eos_token_id", None)
        if eos_token_id is None:
            raise ValueError("AMG AgentLoop tokenizer must define eos_token_id")
        existing_stop_ids = sampling_params.get("stop_token_ids") or []
        if not isinstance(existing_stop_ids, (list, tuple)):
            raise TypeError("sampling_params.stop_token_ids must be a list or tuple")
        eos_stop_ids = (
            eos_token_id if isinstance(eos_token_id, (list, tuple)) else [eos_token_id]
        )
        merged_stop_ids: list[int] = []
        seen_stop_ids: set[int] = set()
        for token_id in [*existing_stop_ids, *eos_stop_ids]:
            normalized_token_id = int(token_id)
            if normalized_token_id not in seen_stop_ids:
                seen_stop_ids.add(normalized_token_id)
                merged_stop_ids.append(normalized_token_id)
        sampling_params["stop_token_ids"] = merged_stop_ids
        if not bool(self.rollout_config.calculate_log_probs):
            raise ValueError(
                "AMG fully-async PPO requires rollout.calculate_log_probs=true"
            )

        client = _route_client_interaction(
            "client construction", create_env_client, route.client_config
        )
        outputs: list[AgentLoopOutput] = []
        rows: list[dict[str, Any]] = []
        try:
            _route_client_interaction("client.reset", client.reset, data_idx)
            policy_tools = _policy_tool_schemas(client)
            self._activate_native_tool_template(policy_tools)
            initial_messages = raw_prompt + [
                {
                    "role": "user",
                    "content": str(
                        _route_client_interaction("client.observe", client.observe)
                    ),
                }
            ]
            current_messages = bind_initial_policy_context(client, initial_messages)
            current_prompt_ids = self._render_prompt_sync(
                current_messages, tools=policy_tools
            )

            emitted_row_order = 0

            for row_order in range(route.max_rounds):
                if len(current_prompt_ids) > max_prompt_tokens:
                    raise PolicyContextCapacityExceeded(
                        "AMG prompt exceeded PPO width before a trainable compaction action: "
                        f"item_id={item_id!r} data_idx={data_idx} row_order={row_order} "
                        f"tokens={len(current_prompt_ids)} width={max_prompt_tokens}"
                    )

                begin_policy_turn_hook = getattr(client, "begin_policy_turn", None)
                if begin_policy_turn_hook is not None:
                    begin_policy_turn_hook(row_order, route.max_rounds)
                prepared = prepare_policy_turn(
                    client,
                    current_messages,
                    count_prompt_tokens=lambda candidate, messages=current_messages, prompt_ids=current_prompt_ids: (
                        len(
                            self._prompt_for_candidate(
                                messages,
                                prompt_ids,
                                candidate,
                                tools=policy_tools,
                            )
                        )
                    ),
                    max_prompt_tokens=max_prompt_tokens,
                    max_model_tokens=max_model_tokens,
                    max_response_tokens=response_budget,
                    max_observation_tokens=route.max_observation_tokens,

                    action_observation_envelope_tokens=(
                        self._action_observation_envelope_tokens(
                            current_messages,
                            current_prompt_ids,
                            tools=policy_tools,
                        )
                        * self._max_parallel_calls
                    ),
                )
                prepared_messages = [dict(message) for message in prepared.messages]
                prompt_ids = self._prompt_for_candidate(
                    current_messages,
                    current_prompt_ids,
                    prepared_messages,
                    tools=policy_tools,
                )
                if len(prompt_ids) != prepared.prompt_token_count:
                    raise RuntimeError(
                        "AMG wrapper prompt-token count differs from sampled prompt: "
                        f"wrapper={prepared.prompt_token_count} sampled={len(prompt_ids)}"
                    )
                if len(prompt_ids) > max_prompt_tokens:
                    raise PolicyContextCapacityExceeded(
                        "AMG wrapper control prompt exceeds PPO prompt width: "
                        f"item_id={item_id!r} data_idx={data_idx} row_order={row_order} "
                        f"tokens={len(prompt_ids)} width={max_prompt_tokens}"
                    )

                request_id = f"{trajectory_uid}-row-{row_order}-{uuid4().hex[:8]}"
                started = time.perf_counter()
                token_output: TokenOutput = await self.server_manager.generate(
                    request_id=request_id,
                    prompt_ids=prompt_ids,
                    sampling_params=sampling_params,
                    priority=priority,
                    image_data=_extract_image_data(
                        _convert_messages_mm(prepared_messages)
                    ),
                )
                elapsed = time.perf_counter() - started
                response_ids = [int(token_id) for token_id in token_output.token_ids]
                if not response_ids:
                    raise RuntimeError(
                        "AMG policy generation returned no response tokens"
                    )
                if len(response_ids) > response_budget:
                    raise RuntimeError(
                        "AMG policy generation exceeded the configured response budget: "
                        f"tokens={len(response_ids)} budget={response_budget}"
                    )
                if token_output.log_probs is None or len(token_output.log_probs) != len(
                    response_ids
                ):
                    raise RuntimeError(
                        "AMG PPO requires one rollout behavior logprob per sampled response token"
                    )
                response_logprobs = [float(value) for value in token_output.log_probs]
                action = _strip_leading_think(
                    self.tokenizer.decode(response_ids, skip_special_tokens=True)
                )

                if self._max_parallel_calls > 1:
                    multi_call_blocks = self._scan_tool_call_blocks(response_ids)
                else:
                    multi_call_blocks = []
                if len(multi_call_blocks) >= 2:
                    _content, parser_calls = (
                        await self._native_tool_parser.extract_tool_calls(
                            response_ids,
                            list(self._typed_tool_schemas(policy_tools)),
                        )
                    )
                    if len(parser_calls) != len(multi_call_blocks):

                        print(
                            "[AMG parallel-call shape fallback] blocks=%d "
                            "parsed=%d; continuing via single-action path"
                            % (len(multi_call_blocks), len(parser_calls)),
                            flush=True,
                        )
                        multi_call_blocks = []
                if len(multi_call_blocks) >= 2:

                    if not policy_tools:
                        raise RuntimeError(
                            "AMG wrapper accepted parallel tool calls "
                            "without tool schemas"
                        )
                    dispatched_blocks = multi_call_blocks[: self._max_parallel_calls]
                    call_slices = _parallel_call_slices(
                        len(response_ids),
                        multi_call_blocks,
                        len(dispatched_blocks),
                    )
                    allowed_names = {
                        str(schema["function"]["name"]) for schema in policy_tools
                    }
                    call_states: list[dict[str, Any]] = []
                    terminal_call: int | None = None
                    for call_index, (block_start, block_end) in enumerate(
                        dispatched_blocks
                    ):
                        call_text = self.tokenizer.decode(
                            response_ids[block_start : block_end + 1],
                            skip_special_tokens=True,
                        )
                        (
                            call_step_output,
                            call_next_messages,
                        ) = _route_client_interaction(
                            "policy turn dispatch",
                            complete_policy_turn,
                            client,
                            prepared,
                            call_text,
                        )
                        (
                            call_env_info,
                            call_submission,
                            call_receipt,
                        ) = _receipt_parts(call_step_output, call_text)
                        call_name = None
                        if call_submission.get("tool_parser_normalized") is True:
                            call_name = str(parser_calls[call_index].name)
                            if call_name not in allowed_names:
                                raise RuntimeError(
                                    "AMG wrapper accepted an action outside "
                                    f"the native tool schema: {call_name!r}"
                                )
                        call_done = bool(call_step_output.done)
                        call_contained = False
                        if getattr(client, "sample_excluded", False):
                            if not call_done:
                                print(
                                    "[AMG non-terminal sample exclusion] "
                                    "route=%s item_id=%r data_idx=%s "
                                    "attempt=%d row_order=%d "
                                    "multi_call_index=%d"
                                    % (
                                        route.route_id,
                                        item_id,
                                        data_idx,
                                        sample_reschedule_attempt,
                                        row_order,
                                        call_index,
                                    ),
                                    flush=True,
                                )
                            if _contain_excluded_sample(
                                self, sample_reschedule_attempt, item_id, data_idx
                            ):
                                call_contained = True
                            else:
                                raise _SampleExcluded(
                                    _sample_exclusion_summary(call_step_output)
                                )
                        call_states.append(
                            {
                                "text": call_text,
                                "step_output": call_step_output,
                                "next_messages": call_next_messages,
                                "env_info": call_env_info,
                                "action_submission": call_submission,
                                "context_transition": call_receipt[
                                    "context_transition"
                                ],
                                "wrapper_evidence": call_receipt[
                                    "wrapper_evidence"
                                ],
                                "name": call_name,
                                "done": call_done,
                                "contained": call_contained,
                            }
                        )
                        if call_done or call_contained:
                            terminal_call = call_index
                            break
                    if (
                        terminal_call is not None
                        and terminal_call < len(dispatched_blocks) - 1
                    ):

                        terminal_slice_start, _ = call_slices[terminal_call]
                        call_slices[terminal_call] = (
                            terminal_slice_start,
                            len(response_ids) - 1,
                        )
                    token_extra_multi = dict(token_output.extra_fields or {})
                    if (
                        token_extra_multi.get("min_global_steps") is None
                        or token_extra_multi.get("max_global_steps") is None
                    ):
                        raise RuntimeError(
                            "AMG fully-async generation is missing upstream "
                            "policy-version metadata"
                        )
                    merged_messages, native_flags = (
                        _merged_parallel_turn_messages(
                            prepared_messages, action, call_states
                        )
                    )
                    for call_index, call_state in enumerate(call_states):
                        call_step_output = call_state["step_output"]
                        call_transition = call_state["context_transition"]
                        call_contained = call_state["contained"]
                        reward_k = (
                            0.0 if call_contained else float(call_step_output.reward)
                        )
                        done_k = bool(call_state["done"] or call_contained)
                        outcome_k = (
                            "environment_infrastructure_failure"
                            if call_contained
                            else _outcome(
                                done=done_k,
                                reward=reward_k,
                                env_info=call_state["env_info"],
                                wrapper_evidence=call_state["wrapper_evidence"],
                            )
                        )
                        native_observation = native_flags[call_index]
                        slice_start, slice_end = call_slices[call_index]
                        row_prompt_ids = prompt_ids + response_ids[:slice_start]
                        row_response_ids = response_ids[slice_start : slice_end + 1]
                        row_response_logprobs = response_logprobs[
                            slice_start : slice_end + 1
                        ]
                        row_uid = (
                            f"{trajectory_uid}-row-"
                            f"{emitted_row_order + call_index}"
                        )
                        row = {
                            "schema": "amg_task_neutral_action_row_v1",
                            "route_id": route.route_id,
                            "data_source": route.route_id,
                            "item_id": item_id,
                            "data_idx": data_idx,
                            "trajectory_uid": trajectory_uid,
                            "trajectory_row_uid": row_uid,
                            "trajectory_row_order": emitted_row_order + call_index,
                            "sample_reschedule_attempt": sample_reschedule_attempt,
                            "trajectory_terminal": False,
                            "rollout_done_flag": done_k,
                            "immediate_reward": reward_k,
                            "trajectory_return": 0.0,
                            "task_round": row_order + 1,
                            "action": call_state["text"],
                            "action_submission": call_state["action_submission"],
                            "env_info_after": call_state["env_info"],
                            "context_transition": call_transition,
                            "wrapper_evidence": call_state["wrapper_evidence"],
                            "control_request": prepared.control_request,
                            "outcome": outcome_k,
                            "prompt_token_count": len(row_prompt_ids),
                            "prompt_token_sha256": _digest_token_ids(row_prompt_ids),
                            "response_token_count": len(row_response_ids),
                            "response_token_sha256": _digest_token_ids(
                                row_response_ids
                            ),
                            "generation_stop_reason": _json_safe(
                                token_output.stop_reason
                            ),
                            "native_tool_call_name": call_state["name"],
                            "native_tool_observation": native_observation,
                            "native_tool_template_sha256": (
                                self._native_tool_template_sha256
                            ),
                            "min_global_steps": int(
                                token_extra_multi["min_global_steps"]
                            ),
                            "max_global_steps": int(
                                token_extra_multi["max_global_steps"]
                            ),
                            "multi_call_index": call_index,
                            "multi_call_total": len(call_states),
                            "multi_call_blocks": len(multi_call_blocks),
                        }
                        if call_contained:
                            row["exclusion_contained"] = True
                        rows.append(row)
                        row_extra = dict(token_extra_multi)
                        row_extra.update(
                            {
                                "route_id": route.route_id,
                                "data_source": route.route_id,
                                "trajectory_uid": trajectory_uid,
                                "trajectory_row_uid": row_uid,
                                "trajectory_row_order": (
                                    emitted_row_order + call_index
                                ),
                                "sample_reschedule_attempt": (
                                    sample_reschedule_attempt
                                ),
                                "trajectory_terminal": False,
                                "rollout_done_flag": done_k,
                                "immediate_reward": reward_k,
                                "trajectory_return": 0.0,
                                "item_id": item_id,
                                "data_idx": data_idx,
                                "task_round": row_order + 1,
                                "action_text": call_state["text"],
                                "generation_stop_reason": _json_safe(
                                    token_output.stop_reason
                                ),
                                "native_tool_call_name": call_state["name"],
                                "native_tool_observation": native_observation,
                                "native_tool_template_sha256": (
                                    self._native_tool_template_sha256
                                ),
                                "context_transition": call_transition,
                                "wrapper_evidence": call_state["wrapper_evidence"],
                                "env_info_after": call_state["env_info"],
                                "control_request": prepared.control_request,
                                "outcome": outcome_k,
                                "horizon_finalization": None,
                                "turn_scores": [reward_k],
                                "tool_rewards": [],
                                "multi_call_index": call_index,
                                "multi_call_total": len(call_states),
                                "multi_call_blocks": len(multi_call_blocks),
                            }
                        )
                        outputs.append(
                            AgentLoopOutput(
                                prompt_ids=row_prompt_ids,
                                response_ids=row_response_ids,
                                response_mask=[1] * len(row_response_ids),
                                response_logprobs=row_response_logprobs,
                                multi_modal_data=self._prompt_mm_data(
                                    prepared_messages
                                ),
                                mm_processor_kwargs=self._builder_mm_kwargs(),
                                routed_experts=_slice_routed_experts(
                                    token_output.routed_experts,
                                    slice_start,
                                    slice_end + 1,
                                ),
                                reward_score=reward_k,
                                num_turns=row_order + 1,
                                metrics=AgentLoopMetrics(
                                    generate_sequences=elapsed,
                                    num_preempted=(
                                        int(token_output.num_preempted)
                                        if token_output.num_preempted is not None
                                        else -1
                                    ),
                                ),
                                extra_fields=row_extra,
                            )
                        )
                    emitted_row_order += len(call_states)
                    if terminal_call is not None:
                        break
                    merged_messages = _annotate_output_cap_truncation(
                        merged_messages,
                        stop_reason=token_output.stop_reason,
                        response_tokens=len(response_ids),
                        response_budget=response_budget,
                    )
                    current_prompt_ids = self._next_prompt_ids(
                        prepared_messages=prepared_messages,
                        prepared_prompt_ids=prompt_ids,
                        action=action,
                        action_token_ids=response_ids,
                        next_messages=merged_messages,
                        tools=policy_tools,
                    )
                    current_messages = merged_messages
                    continue

                step_output, next_messages = _route_client_interaction(
                    "policy turn dispatch", complete_policy_turn, client, prepared, action
                )
                contained_terminal = False
                if getattr(client, "sample_excluded", False):
                    if not bool(step_output.done):

                        print(
                            "[AMG non-terminal sample exclusion] route=%s "
                            "item_id=%r data_idx=%s attempt=%d row_order=%d"
                            % (
                                route.route_id,
                                item_id,
                                data_idx,
                                sample_reschedule_attempt,
                                row_order,
                            ),
                            flush=True,
                        )
                    if _contain_excluded_sample(
                        self, sample_reschedule_attempt, item_id, data_idx
                    ):
                        contained_terminal = True
                    else:
                        raise _SampleExcluded(
                            _sample_exclusion_summary(step_output)
                        )
                next_messages = [dict(message) for message in next_messages]
                reward = 0.0 if contained_terminal else float(step_output.reward)
                done = True if contained_terminal else bool(step_output.done)
                env_info, action_submission, receipt = _receipt_parts(
                    step_output, action
                )
                context_transition = receipt["context_transition"]
                wrapper_evidence = receipt["wrapper_evidence"]
                native_tool_call = await self._validated_native_tool_call(
                    response_ids=response_ids,
                    action=action,
                    tools=policy_tools,
                    action_submission=action_submission,
                )
                native_tool_name = (
                    native_tool_call.name if native_tool_call is not None else None
                )
                native_tool_observation = False
                if (
                    native_tool_name is not None
                    and context_transition.get("operation") == "append_observation"
                    and not done
                ):
                    next_messages = _native_tool_observation_messages(
                        next_messages,
                        expected_assistant_messages=prepared_messages
                        + [{"role": "assistant", "content": action}],
                        tool_name=native_tool_name,
                        observation=str(step_output.state),
                    )
                    native_tool_observation = True

                token_extra = dict(token_output.extra_fields or {})
                if (
                    token_extra.get("min_global_steps") is None
                    or token_extra.get("max_global_steps") is None
                ):
                    raise RuntimeError(
                        "AMG fully-async generation is missing upstream policy-version metadata"
                    )
                metrics = AgentLoopMetrics(
                    generate_sequences=elapsed,
                    num_preempted=(
                        int(token_output.num_preempted)
                        if token_output.num_preempted is not None
                        else -1
                    ),
                )
                row_uid = f"{trajectory_uid}-row-{emitted_row_order}"
                row = {
                    "schema": "amg_task_neutral_action_row_v1",
                    "route_id": route.route_id,
                    "data_source": route.route_id,
                    "item_id": item_id,
                    "data_idx": data_idx,
                    "trajectory_uid": trajectory_uid,
                    "trajectory_row_uid": row_uid,
                    "trajectory_row_order": emitted_row_order,
                    "sample_reschedule_attempt": sample_reschedule_attempt,
                    "trajectory_terminal": False,
                    "rollout_done_flag": done,
                    "immediate_reward": reward,
                    "trajectory_return": 0.0,
                    "task_round": row_order + 1,
                    "action": action,
                    "action_submission": action_submission,
                    "env_info_after": env_info,
                    "context_transition": context_transition,
                    "wrapper_evidence": wrapper_evidence,
                    "control_request": prepared.control_request,
                    "outcome": (
                        "environment_infrastructure_failure"
                        if contained_terminal
                        else _outcome(
                            done=done,
                            reward=reward,
                            env_info=env_info,
                            wrapper_evidence=wrapper_evidence,
                        )
                    ),
                    "prompt_token_count": len(prompt_ids),
                    "prompt_token_sha256": _digest_token_ids(prompt_ids),
                    "response_token_count": len(response_ids),
                    "response_token_sha256": _digest_token_ids(response_ids),
                    "generation_stop_reason": _json_safe(token_output.stop_reason),
                    "native_tool_call_name": native_tool_name,
                    "native_tool_observation": native_tool_observation,
                    "native_tool_template_sha256": self._native_tool_template_sha256,
                    "min_global_steps": int(token_extra["min_global_steps"]),
                    "max_global_steps": int(token_extra["max_global_steps"]),
                }
                if contained_terminal:
                    row["exclusion_contained"] = True
                rows.append(row)
                token_extra.update(
                    {
                        "route_id": route.route_id,
                        "data_source": route.route_id,
                        "trajectory_uid": trajectory_uid,
                        "trajectory_row_uid": row_uid,
                        "trajectory_row_order": emitted_row_order,
                        "sample_reschedule_attempt": sample_reschedule_attempt,
                        "trajectory_terminal": False,
                        "rollout_done_flag": done,
                        "immediate_reward": reward,
                        "trajectory_return": 0.0,
                        "item_id": item_id,
                        "data_idx": data_idx,
                        "task_round": row_order + 1,
                        "action_text": action,
                        "generation_stop_reason": _json_safe(token_output.stop_reason),
                        "native_tool_call_name": native_tool_name,
                        "native_tool_observation": native_tool_observation,
                        "native_tool_template_sha256": self._native_tool_template_sha256,
                        "context_transition": context_transition,
                        "wrapper_evidence": wrapper_evidence,
                        "env_info_after": env_info,
                        "control_request": prepared.control_request,
                        "outcome": row["outcome"],
                        "horizon_finalization": None,
                        "turn_scores": [reward],
                        "tool_rewards": [],
                    }
                )
                outputs.append(
                    AgentLoopOutput(
                        prompt_ids=prompt_ids,
                        response_ids=response_ids,
                        response_mask=[1] * len(response_ids),
                        response_logprobs=response_logprobs,
                        multi_modal_data=self._prompt_mm_data(
                            prepared_messages
                        ),
                        mm_processor_kwargs=self._builder_mm_kwargs(),
                        routed_experts=token_output.routed_experts,
                        reward_score=reward,
                        num_turns=row_order + 1,
                        metrics=metrics,
                        extra_fields=token_extra,
                    )
                )
                emitted_row_order += 1

                if done:
                    break
                next_messages = _annotate_output_cap_truncation(
                    next_messages,
                    stop_reason=token_output.stop_reason,
                    response_tokens=len(response_ids),
                    response_budget=response_budget,
                )
                current_prompt_ids = self._next_prompt_ids(
                    prepared_messages=prepared_messages,
                    prepared_prompt_ids=prompt_ids,
                    action=action,
                    action_token_ids=response_ids,
                    next_messages=next_messages,
                    tools=policy_tools,
                )
                current_messages = next_messages

            if not outputs:
                raise RuntimeError("AMG AgentLoop produced no trainable policy action")

            if not rows[-1]["rollout_done_flag"]:
                finalizer = getattr(client, "finalize_policy_horizon", None)
                horizon_output = finalizer() if callable(finalizer) else None
                horizon_contained = False
                if horizon_output is not None:
                    if getattr(client, "sample_excluded", False):
                        if not bool(horizon_output.done):

                            print(
                                "[AMG non-terminal horizon exclusion] route=%s "
                                "item_id=%r data_idx=%s attempt=%d"
                                % (
                                    route.route_id,
                                    item_id,
                                    data_idx,
                                    sample_reschedule_attempt,
                                ),
                                flush=True,
                            )
                        if _contain_excluded_sample(
                            self, sample_reschedule_attempt, item_id, data_idx
                        ):
                            horizon_contained = True
                            rows[-1]["outcome"] = "environment_infrastructure_failure"
                            rows[-1]["exclusion_contained"] = True
                            rows[-1]["rollout_done_flag"] = True
                            outputs[-1].extra_fields.update(
                                {
                                    "outcome": rows[-1]["outcome"],
                                    "rollout_done_flag": True,
                                    "exclusion_contained": True,
                                }
                            )
                        else:
                            raise _SampleExcluded(
                                _sample_exclusion_summary(horizon_output)
                            )
                    if not horizon_contained and not bool(horizon_output.done):
                        raise RuntimeError(
                            "AMG horizon finalization must terminate the episode"
                        )
                    if not horizon_contained:
                        horizon_reward = float(horizon_output.reward)
                        horizon_env_info, horizon_action_submission, horizon_receipt = (
                            _receipt_parts(horizon_output, "")
                        )
                        horizon_context_transition = horizon_receipt["context_transition"]
                        horizon_wrapper_evidence = horizon_receipt["wrapper_evidence"]
                        rows[-1]["immediate_reward"] += horizon_reward
                        rows[-1]["rollout_done_flag"] = True
                        rows[-1]["outcome"] = _outcome(
                            done=True,
                            reward=float(rows[-1]["immediate_reward"]),
                            env_info=horizon_env_info,
                            wrapper_evidence=horizon_wrapper_evidence,
                        )
                        horizon_finalization = _json_safe(
                            {
                                "state": horizon_output.state,
                                "reward": horizon_reward,
                                "done": True,
                                "info": horizon_output.info,
                                "env_info": horizon_env_info,
                                "action_submission": horizon_action_submission,
                                "context_transition": horizon_context_transition,
                                "wrapper_evidence": horizon_wrapper_evidence,
                            }
                        )
                        rows[-1]["horizon_finalization"] = horizon_finalization
                        outputs[-1].reward_score = float(rows[-1]["immediate_reward"])
                        outputs[-1].extra_fields.update(
                            {
                                "immediate_reward": float(rows[-1]["immediate_reward"]),
                                "rollout_done_flag": True,
                                "outcome": rows[-1]["outcome"],
                                "horizon_finalization": horizon_finalization,
                            }
                        )
                else:
                    rows[-1]["outcome"] = "max_rounds"
                    outputs[-1].extra_fields["outcome"] = "max_rounds"

            return _finalize_amg_trajectory(rows, outputs)
        except PolicyContextCapacityExceeded as exc:

            if not rows or not outputs:
                raise _SampleExcluded(
                    "policy context capacity exceeded before any trainable "
                    f"action: {exc}"
                ) from exc
            if not _contain_excluded_sample(
                self, sample_reschedule_attempt, item_id, data_idx
            ):
                raise _SampleExcluded(
                    f"policy context capacity exceeded: {exc}"
                ) from exc
            rows[-1]["outcome"] = "environment_infrastructure_failure"
            rows[-1]["exclusion_contained"] = True
            rows[-1]["rollout_done_flag"] = True

            earned_reward = rows[-1].get("immediate_reward")
            if not isinstance(earned_reward, (int, float)):
                earned_reward = 0.0
            earned_reward = float(earned_reward)
            rows[-1]["immediate_reward"] = earned_reward
            outputs[-1].reward_score = earned_reward
            outputs[-1].extra_fields.update(
                {
                    "outcome": rows[-1]["outcome"],
                    "rollout_done_flag": True,
                    "exclusion_contained": True,
                    "immediate_reward": earned_reward,
                }
            )
            return _finalize_amg_trajectory(rows, outputs)
        except RuntimeError as exc:

            if str(exc) not in _S15_CLIENT_CONTRACT_ERRORS:
                raise
            return _contain_s15_client_contract_error(
                self,
                exc,
                route_id=route.route_id,
                item_id=item_id,
                data_idx=data_idx,
                sample_reschedule_attempt=sample_reschedule_attempt,
                rows=rows,
                outputs=outputs,
            )
        finally:
            try:
                client.close()
            except Exception as exc:  

                print(
                    "AMG episode close degraded: route=%s item=%s uid=%s error=%r"
                    % (route.route_id, item_id, trajectory_uid, exc),
                    flush=True,
                )
