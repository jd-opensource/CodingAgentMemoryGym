from __future__ import annotations

import base64
import json
import logging
import os
import re
import time
import urllib.request
import uuid
from pathlib import Path
from typing import Any

logger = logging.getLogger("camg.services.visual.bridge")

_KIND_OK = "ok"
_KIND_TOOL_EXCEPTION = "tool_exception"
_KIND_LIMITS = "limits_exceeded"
_KIND_TRANSPORT = "transport_error"
_KIND_UNEXPECTED = "unexpected"

_PREVIEW_TOOL_NAME = "render_preview"
_PREVIEW_MAX_IMAGES = 4
_PREVIEW_CLIP_HEIGHT = 1400
_PREVIEW_MARKER_BEGIN = "[[WDIMG:"
_PREVIEW_MARKER_END = "]]"
_PREVIEW_TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": _PREVIEW_TOOL_NAME,
        "description": (
            "Render the current delivery (dist/index.html or a root-level "
            "index.html) and return one screenshot image of the page so you "
            "can see how it looks; call it before finish to check the "
            "result against the design brief. At most 4 screenshots per "
            "episode."
        ),
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
}

_TASK_DIR_ROOT = os.environ.get("WEBDEV_TASK_DIR_ROOT", "/tmp/camg-visual-tasks")

_RENDER_SCRIPT = "\n".join(
    [
        "import functools, http.server, sys, threading",
        "from playwright.sync_api import sync_playwright",
        "deliver_dir, out_path = sys.argv[1], sys.argv[2]",
        "handler = functools.partial(",
        "    http.server.SimpleHTTPRequestHandler, directory=deliver_dir",
        ")",
        "srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)",
        "port = srv.server_address[1]",
        "threading.Thread(target=srv.serve_forever, daemon=True).start()",
        "with sync_playwright() as p:",
        "    b = p.chromium.launch()",
        "    pg = b.new_page(viewport={'width': 1440, 'height': 900})",
        "    pg.goto('http://127.0.0.1:%d/index.html' % port,",
        "            wait_until='domcontentloaded', timeout=30000)",
        "    try:",
        "        pg.wait_for_load_state('networkidle', timeout=8000)",
        "    except Exception:",
        "        pass",
        "    pg.wait_for_timeout(1500)",
        "    height = pg.evaluate(",
        "        'Math.max(document.body ? document.body.scrollHeight : 0,"
        " document.documentElement ? document.documentElement.scrollHeight : 0)'",
        "    )",
        "    cap = int(sys.argv[3]) if len(sys.argv) > 3 else 12000",
        "    clip = {'x': 0, 'y': 0, 'width': 1440,",
        "            'height': max(1, min(int(height), cap))}",
        "    pg.screenshot(path=out_path, type='jpeg', quality=75, clip=clip)",
        "    b.close()",
        "srv.shutdown()",
        "print('RENDER_OK')",
    ]
)

def load_mimoagent_config(path: str | Path) -> dict[str, Any]:

    import yaml

    with open(path, "r", encoding="utf-8") as fh:
        config = yaml.safe_load(fh) or {}
    tools = (config.get("agent") or {}).get("tools") or []
    tool_names = [t.get("tool") for t in tools if isinstance(t, dict)]
    if "agent" in tool_names:
        raise ValueError(
            f"{path}: the 'agent' (subagent) tool is not supported here; "
            "use a config without it."
        )
    if not tool_names and not config.get("use_dataset_env"):
        raise ValueError(f"{path}: agent.tools is empty.")
    return config

class WebdevBridge:

    CHECKPOINT_PATH = ".agent_memory/CONTINUATION.md"
    _STEP_MARKER = "/tmp/.wd_step_marker"

    def __init__(
        self,
        *,
        instance: dict[str, Any],
        config: dict[str, Any],
        instance_id: str,
        exp_label: str = "amg_webdev",
    ):
        from mimoagent.tools import ToolRegistry

        self.instance = instance
        self.instance_id = instance_id
        self.config = config
        self.dataset_env: Any = None
        self._register_cc_tools(config)
        self.tool_registry = ToolRegistry.from_config(
            (config.get("agent") or {}).get("tools") or []
        )
        self._exp_label = exp_label
        self.infra_error: str | None = None
        self._final_answer: str = ""
        self._preview_renders: int = 0

    @staticmethod
    def _register_cc_tools(config: dict[str, Any]) -> None:

        from mimoagent.tools.registry import _TOOL_CLASSES

        tool_names = [
            t.get("tool")
            for t in (config.get("agent") or {}).get("tools") or []
            if isinstance(t, dict)
        ]
        if any(name not in _TOOL_CLASSES for name in tool_names):
            from recipes.general.tools import register_cc_tools

            register_cc_tools()

    def setup(self) -> None:

        from mimoagent.environments.utils import make_dataset_env
        from recipes.general.general_agent import register_general_agent_env

        register_general_agent_env()

        env_block = dict(self.config.get("environment") or {})
        env_kwargs = dict(env_block)
        env_kwargs["labels"] = {
            "exp": os.getenv("EXP_NAME", self._exp_label),
            **(env_kwargs.get("labels") or {}),
        }

        env_instance = dict(self.instance)
        self._synth_task_dir: str | None = None
        if env_instance.get("dataset_type") == "webdev":
            env_instance["dataset_type"] = "general_agent"
            os.makedirs(_TASK_DIR_ROOT, exist_ok=True)
            task_dir = os.path.join(
                _TASK_DIR_ROOT, f"{self.instance_id}-{uuid.uuid4().hex[:8]}"
            )
            os.makedirs(os.path.join(task_dir, "workspace"), exist_ok=True)
            env_instance["env_task_dir"] = task_dir
            self._synth_task_dir = task_dir

        self.dataset_env = make_dataset_env(env_instance, **env_kwargs)
        self.dataset_env.setup_environment()

    def close(self) -> None:
        if self.dataset_env is not None:
            try:
                self.dataset_env.cleanup()
            except Exception as exc:
                logger.warning("%s: env cleanup failed (%r)", self.instance_id, exc)
            self.dataset_env = None
        if self._synth_task_dir is not None:
            import shutil

            shutil.rmtree(self._synth_task_dir, ignore_errors=True)
            self._synth_task_dir = None

    _POLICY_TOOL_NAMES = {"Bash": "bash"}

    def _policy_tool_name(self, name: str) -> str:
        return self._POLICY_TOOL_NAMES.get(name, name)

    def _canonical_tool_name(self, name: str) -> str:
        for canonical, policy in self._POLICY_TOOL_NAMES.items():
            if name == policy:
                return canonical
        return name

    def tool_names(self) -> list[str]:
        return [self._policy_tool_name(n) for n in self.tool_registry.list_tools()] + [
            _PREVIEW_TOOL_NAME
        ]

    def tool_definitions(self) -> list[dict[str, Any]]:
        definitions = []
        for definition in self.tool_registry.get_function_definitions():
            if isinstance(definition, dict):
                fn = definition.get("function")
                target = fn if isinstance(fn, dict) else definition
                if target.get("name") in self._POLICY_TOOL_NAMES:
                    definition = json.loads(json.dumps(definition))
                    target = (
                        definition.get("function")
                        if isinstance(fn, dict)
                        else definition
                    )
                    target["name"] = self._policy_tool_name(target["name"])
            definitions.append(definition)
        definitions.append(json.loads(json.dumps(_PREVIEW_TOOL_DEFINITION)))
        return definitions

    def render_tool_surface(self) -> str:

        lines: list[str] = ["Available tools:"]
        for definition in self.tool_definitions():
            fn = definition.get("function") or definition
            name = fn.get("name", "?")
            desc = (fn.get("description") or "").strip().splitlines()
            summary = desc[0][:160] if desc else ""
            params = fn.get("parameters") or {}
            required = list(params.get("required") or [])
            props = params.get("properties") or {}
            if required:
                sig = ", ".join(
                    f"{p}:{props.get(p, {}).get('type', 'string')}" for p in required
                )
                lines.append(f"- {name}({sig}) — {summary}")
            else:
                lines.append(f"- {name}() — {summary}")
        return "\n".join(lines)

    def execute(self, name: str, params: dict[str, Any]) -> dict[str, Any]:

        if name == _PREVIEW_TOOL_NAME:
            return self._execute_render_preview(params)
        from mimoagent.agents.base import LimitsExceeded
        from mimoagent.environments import TransportError
        from mimoagent.tools import ToolException

        max_attempts = 3
        for attempt in range(1, max_attempts + 1):
            try:
                tool = self.tool_registry.get(self._canonical_tool_name(name))
                result = tool.execute(params, {"env": self.dataset_env.env})
            except LimitsExceeded as exc:
                return {"kind": _KIND_LIMITS, "message": str(exc)}
            except TransportError as exc:
                if "opening exec stream" in str(exc) and attempt < max_attempts:
                    time.sleep(2 * attempt)
                    continue
                self.infra_error = f"rollout/pod_conn_timeout: {exc}"
                return {"kind": _KIND_TRANSPORT, "message": str(exc)}
            except ToolException as exc:
                return {"kind": _KIND_TOOL_EXCEPTION, "message": str(exc)}
            except Exception as exc:
                return {
                    "kind": _KIND_UNEXPECTED,
                    "message": f"Unexpected error executing tool '{name}': {exc}",
                }
            return {"kind": _KIND_OK, "result": result.to_dict()}
        return {
            "kind": _KIND_TRANSPORT,
            "message": f"tool '{name}' failed after {max_attempts} exec-stream attempts",
        }

    def _execute_render_preview(self, params: dict[str, Any]) -> dict[str, Any]:

        if self._preview_renders >= _PREVIEW_MAX_IMAGES:
            return {
                "kind": _KIND_TOOL_EXCEPTION,
                "message": (
                    "render_preview budget exhausted: at most "
                    f"{_PREVIEW_MAX_IMAGES} screenshots per episode."
                ),
            }
        delivery_dir = self._locate_delivery()
        if delivery_dir is None:
            return {
                "kind": _KIND_TOOL_EXCEPTION,
                "message": (
                    "nothing to preview yet: neither dist/index.html nor "
                    "index.html exists in the workspace"
                ),
            }
        shot_b64 = self._render_delivery(
            delivery_dir, max_height=_PREVIEW_CLIP_HEIGHT
        )
        if shot_b64 is None:
            return {"kind": _KIND_TOOL_EXCEPTION, "message": "preview render failed"}
        self._preview_renders += 1
        data_uri = "data:image/jpeg;base64," + shot_b64
        output = (
            f"render_preview: screenshot {self._preview_renders}/"
            f"{_PREVIEW_MAX_IMAGES} of {delivery_dir}/index.html follows as "
            "one image."
            f"\n{_PREVIEW_MARKER_BEGIN}{data_uri}{_PREVIEW_MARKER_END}"
        )
        return {"kind": _KIND_OK, "result": {"output": output, "success": True}}

    def coerce_params(
        self, name: str, raw_params: dict[str, str]
    ) -> dict[str, Any]:

        definitions = self.tool_definitions()
        schema: dict[str, Any] = {}
        for definition in definitions:
            fn = definition.get("function") or definition
            if fn.get("name") == name:
                schema = (fn.get("parameters") or {}).get("properties") or {}
                break
        coerced: dict[str, Any] = {}
        for key, value in raw_params.items():
            expected = schema.get(key, {}).get("type")
            if expected in ("integer", "number", "boolean", "array", "object", "null"):
                try:
                    coerced[key] = json.loads(value)
                    continue
                except (json.JSONDecodeError, ValueError):
                    pass
            coerced[key] = value
        return coerced

    def checkpoint_state(self) -> dict[str, Any] | None:

        try:
            env_obj = self.dataset_env.env
            probe = env_obj.execute(
                "if [ -f '" + self.CHECKPOINT_PATH + "' ] && [ ! -d '"
                + self.CHECKPOINT_PATH + "' ]; then stat -c '%s' '"
                + self.CHECKPOINT_PATH + "'; sha256sum '" + self.CHECKPOINT_PATH
                + "' | cut -d' ' -f1; else echo __MISSING__; fi"
            )
        except Exception:
            return None
        if probe.get("returncode") != 0:
            return None
        output = str(probe.get("output", "")).strip()
        if output == "__MISSING__":
            return None
        lines = output.splitlines()
        if len(lines) < 2:
            return None
        try:
            size = int(lines[0].strip())
        except ValueError:
            return None
        return {"size_bytes": size, "sha256": lines[1].strip()}

    def checkpoint_content(self) -> str | None:
        try:
            env_obj = self.dataset_env.env
            probe = env_obj.execute("cat '" + self.CHECKPOINT_PATH + "'")
        except Exception:
            return None
        if probe.get("returncode") != 0:
            return None
        return str(probe.get("output", ""))

    def workspace_changes_since_marker(self) -> list[str]:

        try:
            env_obj = self.dataset_env.env
            probe = env_obj.execute(
                "find . -type f -newer '" + self._STEP_MARKER
                + "' -not -path './.agent_memory/*' -not -name '"
                + self._STEP_MARKER + "' 2>/dev/null | head -64"
            )
        except Exception:
            return []
        if probe.get("returncode") != 0:
            return []
        return [
            line.strip().lstrip("./")
            for line in str(probe.get("output", "")).splitlines()
            if line.strip()
        ]

    def touch_step_marker(self) -> None:
        try:
            env_obj = self.dataset_env.env
            env_obj.execute("touch '" + self._STEP_MARKER + "'")
        except Exception:
            pass

    def set_final_answer(self, text: str) -> None:
        self._final_answer = text or ""

    def calculate_reward(self, timeout: float | None = None) -> tuple[float, str, dict]:

        if self.infra_error is not None:
            return 0.0, self.infra_error, {"error_category": "infra_error"}
        delivery_dir = self._locate_delivery()
        if delivery_dir is None:
            return (
                0.0,
                "no delivery: neither dist/index.html nor index.html exists "
                "in the workspace",
                {"error_category": "no_delivery"},
            )
        shot_b64 = self._render_delivery(delivery_dir)
        if shot_b64 is None:
            return 0.0, "render failed", {"error_category": "render_failed"}
        return self._judge_shot(shot_b64)

    def _locate_delivery(self) -> str | None:

        env_obj = self.dataset_env.env
        for candidate in ("dist/index.html", "index.html"):
            try:
                probe = env_obj.execute(
                    "test -s '" + candidate + "' && echo __DELIVERED__"
                )
            except Exception:
                return None
            if (
                probe.get("returncode") == 0
                and "__DELIVERED__" in str(probe.get("output", ""))
            ):
                return candidate.rsplit("/", 1)[0] or "."
        return None

    def _render_delivery(
        self, deliver_dir: str, max_height: int | None = None
    ) -> str | None:

        env_obj = self.dataset_env.env
        script_b64 = base64.b64encode(_RENDER_SCRIPT.encode("utf-8")).decode("ascii")
        command = (
            "echo " + script_b64 + " | base64 -d > /tmp/_wd_render.py"
            " && python3 /tmp/_wd_render.py '" + deliver_dir
            + "' /tmp/_wd_shot.jpg"
            + (f" {int(max_height)}" if max_height is not None else "")
            + " >/tmp/_wd_render.out 2>&1"
            " && base64 -w0 /tmp/_wd_shot.jpg"
        )
        try:
            probe = env_obj.execute(command)
        except Exception as exc:
            logger.warning("%s: render exec failed (%r)", self.instance_id, exc)
            return None
        if probe.get("returncode") != 0:
            logger.warning(
                "%s: render script rc=%s head=%s",
                self.instance_id,
                probe.get("returncode"),
                str(probe.get("output", ""))[:400],
            )
            return None
        b64 = str(probe.get("output", "")).strip()
        if len(b64) < 1000:
            logger.warning(
                "%s: render output too short (%d bytes)", self.instance_id, len(b64)
            )
            return None
        try:
            base64.b64decode(b64, validate=True)
        except Exception:
            logger.warning("%s: render output is not clean base64", self.instance_id)
            return None
        return b64

    def _judge_shot(self, shot_b64: str) -> tuple[float, str, dict]:

        from recipes.design.webdev.eval_rubric import (
            ALL_KEYS,
            RUBRIC_ID,
            VISUAL_KEYS,
            build_prompt,
        )

        query = str(self.instance.get("problem_statement") or "").strip()
        prompt = build_prompt().format(query=query)
        judge_url = os.environ["WD_JUDGE_URL"]
        judge_key = os.environ["WD_JUDGE_KEY"]
        judge_model = os.environ["WD_JUDGE_MODEL"]
        judge_timeout = float(os.environ.get("WD_JUDGE_TIMEOUT_S", "180"))
        judge_retries = int(os.environ.get("WD_JUDGE_RETRIES", "3"))

        last_error = ""
        for attempt in range(1, judge_retries + 1):
            try:
                content = _chat_vision(
                    judge_url,
                    judge_key,
                    judge_model,
                    shot_b64,
                    prompt,
                    timeout=judge_timeout,
                )
                verdict = _parse_verdict(content, ALL_KEYS)
            except Exception as exc:
                last_error = f"attempt {attempt}: {type(exc).__name__}: {exc}"[:400]
                logger.warning("%s: judge %s", self.instance_id, last_error)
                time.sleep(2 * attempt)
                continue
            visual = sum(verdict[k] for k in VISUAL_KEYS) / len(VISUAL_KEYS)
            score = (
                visual + verdict["query_fulfillment"] + verdict["premium_assets"]
            ) / 3
            score = float(min(1.0, max(0.0, score)))
            extra = {
                "rubric_id": RUBRIC_ID,
                "judge_model": judge_model,
                "dims": {k: verdict[k] for k in ALL_KEYS},
            }
            return score, content[:1500], extra
        return (
            0.0,
            "judge failed after retries: " + last_error,
            {"error_category": "reward/exception", "rubric_id": RUBRIC_ID},
        )

def _chat_vision(
    base_url: str,
    api_key: str,
    model: str,
    image_b64: str,
    prompt: str,
    *,
    timeout: float,
) -> str:
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": "data:image/jpeg;base64," + image_b64},
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ],
        "temperature": 1.0,
        "max_tokens": 6000,
    }
    req = urllib.request.Request(
        base_url.rstrip("/") + "/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + api_key,
        },
    )
    resp = json.load(urllib.request.urlopen(req, timeout=timeout))
    content = resp["choices"][0]["message"].get("content") or ""
    if not content:
        raise ValueError("judge returned empty content")
    return content

def _parse_verdict(content: str, all_keys: tuple[str, ...]) -> dict[str, float]:

    match = re.search(r"\{.*\}", content, re.S)
    if match is None:
        raise ValueError("no JSON object in judge content")
    verdict = json.loads(match.group(0))
    missing = [k for k in all_keys if not isinstance(verdict.get(k), (int, float))]
    if missing:
        raise ValueError("missing dimensions: " + ",".join(missing))
    return {k: float(min(1.0, max(0.0, float(verdict[k])))) for k in all_keys}
