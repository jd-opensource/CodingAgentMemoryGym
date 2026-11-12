from __future__ import annotations

import json
import logging
import os
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

logger = logging.getLogger("camg.services.general.bridge")

def dataset_env_uid(bridge: "MimoBridge") -> str | None:

    env = getattr(bridge, "dataset_env", None)
    return getattr(getattr(env, "env", None), "_env_uid", None)

def reclaim_env_uid(uid: str, *, reason: str = "") -> dict[str, Any]:

    executable = os.environ.get("MIMOAGENT_DOCKER_EXECUTABLE", "docker")
    residual: list[str] = []
    for _ in range(3):
        res = subprocess.run(
            [executable, "ps", "-a", "--filter", f"name=mimoagent-{uid}-", "-q"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        residual = [x for x in res.stdout.split() if x]
        if not residual:
            break
        subprocess.run(
            [executable, "rm", "-f", *residual],
            capture_output=True,
            text=True,
            timeout=120,
        )
    vol_dir = os.path.join(
        os.environ.get("MIMOAGENT_DOCKER_VOL_ROOT", "/dev/shm/mimo-envs"), uid
    )
    if os.path.isdir(vol_dir) and not residual:
        shutil.rmtree(vol_dir, ignore_errors=True)
    if residual:
        logger.warning(
            "reclaim_env_uid(%s): residual containers %s (%s)",
            uid,
            residual,
            reason,
        )
    return {"env_uid": uid, "reason": reason, "residual": residual}

_KIND_OK = "ok"
_KIND_TOOL_EXCEPTION = "tool_exception"
_KIND_LIMITS = "limits_exceeded"
_KIND_TRANSPORT = "transport_error"
_KIND_UNEXPECTED = "unexpected"

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

def _register_cc_tools_if_needed(config: dict[str, Any]) -> None:

    from mimoagent.tools.registry import _TOOL_CLASSES

    tool_names = [
        t.get("tool")
        for t in (config.get("agent") or {}).get("tools") or []
        if isinstance(t, dict)
    ]
    if any(name not in _TOOL_CLASSES for name in tool_names):
        from recipes.general.tools import register_cc_tools

        register_cc_tools()

class MimoBridge:

    def __init__(
        self,
        *,
        instance: dict[str, Any],
        config: dict[str, Any],
        instance_id: str,
        exp_label: str = "amg_agentgeneral",
    ):
        from mimoagent.tools import ToolRegistry

        self.instance = instance
        self.instance_id = instance_id
        self.config = config
        self.dataset_env: Any = None
        _register_cc_tools_if_needed(config)
        self.tool_registry = ToolRegistry.from_config(
            (config.get("agent") or {}).get("tools") or []
        )
        self._exp_label = exp_label
        self.infra_error: str | None = None
        self.close_report: dict[str, Any] | None = None
        self._final_answer: str = ""

    def setup(self) -> None:

        from mimoagent.environments.utils import make_dataset_env

        self._register_general_agent_env()

        env_block = dict(self.config.get("environment") or {})
        env_kwargs = dict(env_block)
        env_kwargs["labels"] = {
            "exp": os.getenv("EXP_NAME", self._exp_label),
            **(env_kwargs.get("labels") or {}),
        }
        if os.environ.get("KUBECONFIG") and "kubeconfig" not in env_kwargs:
            env_kwargs["kubeconfig"] = os.environ["KUBECONFIG"]
        registry = os.environ.get("DOCKER_REGISTRY")
        if registry and "image_prefix" not in env_kwargs:
            env_kwargs["image_prefix"] = registry

        self.dataset_env = make_dataset_env(self.instance, **env_kwargs)
        self.dataset_env.setup_environment()

        env_obj = self.dataset_env.env
        mcp_servers = getattr(env_obj, "mcp_servers", None)
        bridge_script = getattr(env_obj, "mcp_bridge_script", None)
        bridge_python = getattr(env_obj, "mcp_bridge_python", "python3")
        if mcp_servers and bridge_script:
            from recipes.general.mcp_proxy import discover_mcp_tools

            mcp_tools = discover_mcp_tools(
                env_obj, mcp_servers, bridge_python, bridge_script
            )
            for tool in mcp_tools:
                self.tool_registry.register(tool)
            self._ensure_bridge_in_sidecar(bridge_script)
            logger.info(
                "%s: registered %d MCP tool(s) from %d server(s)",
                self.instance_id,
                len(mcp_tools),
                len(mcp_servers),
            )
        elif mcp_servers:
            logger.warning(
                "%s: env has %d mcp_servers but no bridge script; MCP tools unregistered",
                self.instance_id,
                len(mcp_servers),
            )

    def _register_general_agent_env(self) -> None:
        from recipes.general.general_agent import register_general_agent_env

        register_general_agent_env()

    def _ensure_bridge_in_sidecar(self, bridge_path: str) -> None:
        src = os.path.join(self.instance.get("env_task_dir") or "", "mcp_bridge.py")
        if not os.path.isfile(src):
            return
        try:
            env_obj = self.dataset_env.env
            env_obj.execute(
                f"mkdir -p {os.path.dirname(bridge_path)}", container="sidecar"
            )
            env_obj.copy_to(src, bridge_path, container="sidecar", dereference=True)
            check = env_obj.execute(
                f"test -s {bridge_path} && echo OK", container="sidecar"
            )
            if check.get("returncode") != 0:
                logger.warning(
                    "%s: sidecar bridge verification failed", self.instance_id
                )
        except Exception as exc:  
            logger.warning(
                "%s: ensuring bridge in sidecar failed (%r)", self.instance_id, exc
            )

    def close(self) -> None:
        if self.dataset_env is not None:

            uid = dataset_env_uid(self)
            try:
                self.dataset_env.cleanup()
            except Exception as exc:
                logger.warning("%s: env cleanup failed (%r)", self.instance_id, exc)
            self.dataset_env = None
            if uid and os.environ.get("AG_CLOSE_VERIFY", "1") != "0":
                self.close_report = reclaim_env_uid(uid, reason="bridge_close")
            elif uid:
                self.close_report = {
                    "env_uid": uid,
                    "reason": "bridge_close",
                    "verified": False,
                }

    _POLICY_TOOL_NAMES = {"Bash": "bash"}

    def _policy_tool_name(self, name: str) -> str:
        return self._POLICY_TOOL_NAMES.get(name, name)

    def _canonical_tool_name(self, name: str) -> str:
        for canonical, policy in self._POLICY_TOOL_NAMES.items():
            if name == policy:
                return canonical
        return name

    def tool_names(self) -> list[str]:
        return [self._policy_tool_name(n) for n in self.tool_registry.list_tools()]

    def tool_definitions(self) -> list[dict[str, Any]]:
        import copy

        rewritten = []
        for definition in self.tool_registry.get_function_definitions():
            if not isinstance(definition, dict):
                rewritten.append(definition)
                continue
            fn = definition.get("function")
            target = fn if isinstance(fn, dict) else definition
            if target.get("name") in self._POLICY_TOOL_NAMES:
                definition = copy.deepcopy(definition)
                target = (
                    definition.get("function")
                    if isinstance(fn, dict)
                    else definition
                )
                target["name"] = self._policy_tool_name(target["name"])
            rewritten.append(definition)
        return rewritten

    def render_tool_surface(self) -> str:

        lines: list[str] = ["Available tools:"]
        for definition in self.tool_definitions():
            fn = definition.get("function") or definition
            name = fn.get("name", "?")
            desc = (fn.get("description") or "").strip().splitlines()
            summary = desc[0][:160] if desc else ""
            params = fn.get("parameters") or {}
            required = set(params.get("required") or [])
            props = params.get("properties") or {}
            if props:

                sig = ", ".join(
                    f"{p}: {props.get(p, {}).get('type', 'string')}"
                    + ("*" if p in required else "")
                    for p in props
                )
                lines.append(f"- {name}({sig}) — {summary}")
            else:
                lines.append(f"- {name}() — {summary}")
        return "\n".join(lines)

    def execute(self, name: str, params: dict[str, Any]) -> dict[str, Any]:

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

    CHECKPOINT_PATH = ".agent_memory/CONTINUATION.md"
    _STEP_MARKER = "/tmp/.ag_step_marker"

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

    def _write_answer_md(self) -> None:

        if not self._final_answer:
            return
        repo_path = getattr(self.dataset_env, "REPO_PATH", "")
        target = f"{repo_path}/answer.md" if repo_path else "answer.md"
        env_obj = self.dataset_env.env
        check = env_obj.execute(f"test -s {target}")
        if check.get("returncode") == 0:
            return
        try:
            self.dataset_env.copy_text_to(self._final_answer, target)
        except Exception as exc:
            logger.warning(
                "%s: writing answer.md failed (%r)", self.instance_id, exc
            )

    def calculate_reward(self, timeout: float | None = None) -> tuple[float, str, dict]:

        if self.infra_error is not None:
            return 0.0, self.infra_error, {"error_category": "infra_error"}
        self._write_answer_md()
        try:
            reward, output, extra = self.dataset_env.calculate_reward(timeout=timeout)
            return float(reward), str(output), dict(extra or {})
        except Exception as exc:
            logger.warning("%s: calculate_reward raised (%r)", self.instance_id, exc)
            return 0.0, str(exc), {"error_category": "reward/exception"}
