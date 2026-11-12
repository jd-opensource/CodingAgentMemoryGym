# Docker-substrate equivalent of k8s_sidecar: same interface, plain docker containers.
#
# Semantics preserved from the kubernetes recipe: per-task image, main + sidecar
# containers, shared emptyDir-style volumes, main-container default exec routing,
# per-call container= routing for uploads/verifier/probes, copy_to(dereference=)
# symlink guard, and every config field the dataset rows / yaml blocks carry
# (scheduling-only fields are accepted and ignored). Differences: no namespace /
# labels / node scheduling (single dedicated pod), cpu_request/memory_request not
# enforced (only *_limit maps to --cpus/--memory), pods are docker containers.
from __future__ import annotations

import os
import shlex
import subprocess
import uuid
from dataclasses import dataclass, field
from typing import Any

from mimoagent.environments.docker import DockerEnvironment, DockerEnvironmentConfig

_VOL_ROOT = os.environ.get("MIMOAGENT_DOCKER_VOL_ROOT", "/dev/shm/mimo-envs")

# Host-side venv bound into every container at /opt/openai-agents-venv (the
# VENV_PYTHON the general-agent task scripts expect). Provisioned once on the
# pod because the env images carry no such venv and have no pip network.
_AGENT_VENV_HOST_DIR = os.environ.get(
    "MIMOAGENT_AGENT_VENV_HOST_DIR", "/root/openai-agents-venv"
)


@dataclass
class SidecarDockerEnvironmentConfig(DockerEnvironmentConfig):
    """DockerEnvironmentConfig plus the k8s-shaped fields that dataset rows and
    yaml environment blocks carry, so filter_env_kwargs keeps the set intact."""

    # scheduling-shaped, accepted and ignored on a dedicated pod
    cpu_request: str = "0.5"
    memory_request: str = "1Gi"
    cpu_limit: str | None = None
    memory_limit: str | None = None
    pod_timeout: str = "2h"
    namespace: str = "default"
    labels: dict[str, str] = field(default_factory=dict)
    annotations: dict[str, str] = field(default_factory=dict)
    node_selector: dict[str, str] | None = None
    tolerations: list[dict[str, Any]] | None = None
    kubeconfig: str | None = None
    image_pull_secrets: list[str] | None = None
    dnat_proxy_ip: str = ""

    # behavioural fields consumed by DatasetEnvironment / the agent framework
    raise_on_transport_error: bool = False
    exec_user: str | None = None
    max_exec_budget: float = 0
    no_binary: bool = False
    max_submits: int = 0
    capabilities: list[str] = field(default_factory=list)
    skip_precheck: bool = False
    answer_leak_blocklist: list[str] | None = None
    host_network: bool = False

    # multi-container keys, same shapes as k8s_sidecar
    shared_volumes: list[str] = field(default_factory=list)
    main_volume_mounts: list[dict[str, Any]] = field(default_factory=list)
    sidecars: list[dict[str, Any]] = field(default_factory=list)


class SidecarDockerEnvironment(DockerEnvironment):
    """DockerEnvironment that also starts sidecar containers, mirroring
    recipes.general.general_agent.k8s_sidecar.SidecarKubernetesEnvironment."""

    def __init__(self, *, config_class: type = SidecarDockerEnvironmentConfig, **kwargs):
        super().__init__(config_class=config_class, **kwargs)
        self._validate_multi_container_config()
        self._env_uid = uuid.uuid4().hex[:12]
        self._vol_root = os.path.join(_VOL_ROOT, self._env_uid)
        self._sidecar_ids: dict[str, str] = {}
        self._started = False

    # ---- helpers ---------------------------------------------------------

    @property
    def _main_id(self) -> str:
        assert self.container_id, "environment not started"
        return self.container_id

    def _validate_multi_container_config(self) -> None:
        declared = set(self.config.shared_volumes)
        names: list[str] = []
        for sidecar in self.config.sidecars:
            name = sidecar.get("name")
            if not name or name == "main":
                raise ValueError(f"sidecar needs a name other than 'main': {sidecar!r}")
            names.append(name)
            for mount in sidecar.get("volume_mounts") or []:
                if mount.get("name") not in declared:
                    raise ValueError(
                        f"sidecar {name!r} mounts undeclared volume {mount.get('name')!r} "
                        f"(declared shared_volumes: {sorted(declared)})"
                    )
        if len(set(names)) != len(names):
            raise ValueError(f"duplicate sidecar names: {names}")
        for mount in self.config.main_volume_mounts:
            if mount.get("name") not in declared:
                raise ValueError(
                    f"main mounts undeclared volume {mount.get('name')!r} "
                    f"(declared shared_volumes: {sorted(declared)})"
                )

    def _volume_dir(self, volume_name: str) -> str:
        path = os.path.join(self._vol_root, volume_name)
        os.makedirs(path, exist_ok=True)
        return path

    def _mount_args(self, mounts: list[dict[str, Any]]) -> list[str]:
        args: list[str] = []
        for mount in mounts or []:
            host_dir = self._volume_dir(mount["name"])
            spec = f"{host_dir}:{mount['mount_path']}"
            if mount.get("read_only"):
                spec += ":ro"
            args.extend(["-v", spec])
        return args

    def _agent_venv_args(self) -> list[str]:
        # Task scripts run MCP servers (sidecar) and the MCP bridge (main)
        # under /opt/openai-agents-venv/bin/python, matching VENV_PYTHON in
        # sidecar_entrypoint.py / environment.py. The env images ship mcp 2.x
        # in the system python while those scripts use the mcp<2 FastMCP API
        # and carry no venv of their own, so bind the host-provided one in.
        # A missing host dir means no mount; environments that need it then
        # fail loudly at their own spawn, same as before this patch.
        if os.path.isdir(_AGENT_VENV_HOST_DIR):
            return ["-v", f"{_AGENT_VENV_HOST_DIR}:/opt/openai-agents-venv:ro"]
        return []

    def _resource_args(self, *, networked: bool = True) -> list[str]:
        # networked=False is for containers that join another container's netns
        # (--network=container:...), where a --network flag is not allowed.
        args: list[str] = []
        if self.config.cpu_limit:
            args.extend(["--cpus", str(self.config.cpu_limit)])
        if self.config.memory_limit:
            args.extend(["--memory", str(self.config.memory_limit)])
        for cap in self.config.capabilities or []:
            args.extend(["--cap-add", cap])
        if networked and self.config.host_network:
            args.append("--network=host")
        return args

    # ---- lifecycle -------------------------------------------------------

    def start(self):
        if self._started:
            return
        os.makedirs(self._vol_root, exist_ok=True)
        self._start_container()
        for sidecar in self.config.sidecars:
            self._start_sidecar(sidecar)
        self._started = True

    def _start_container(self):
        """docker run of the main container, parent's shape plus volume binds."""
        name = f"mimoagent-{self._env_uid}-main"
        cmd = [
            self.config.executable,
            "run",
            "-d",
            "--name",
            name,
            "-w",
            self.config.cwd,
            *self._mount_args(self.config.main_volume_mounts),
            *self._agent_venv_args(),
            *self._resource_args(),
            *self.config.run_args,
            self.config.image,
            "sleep",
            "infinity",
        ]
        self.logger.debug(f"Starting main container: {shlex.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            raise RuntimeError(
                f"docker run main failed rc={result.returncode}: "
                f"{(result.stderr or result.stdout).strip()[:500]}"
            )
        self.container_id = result.stdout.strip()

    def _start_sidecar(self, sidecar: dict[str, Any]):
        name = sidecar["name"]
        command = list(sidecar.get("command") or ["sleep", "infinity"])
        container_name = f"mimoagent-{self._env_uid}-{name}"
        # k8s pods share one netns: sidecar MCP servers bind 127.0.0.1 and main
        # dials them there. The docker equivalent is joining the main container's
        # netns, so --network=container:<main> (and no --network flag of its own).
        cmd = [
            self.config.executable,
            "run",
            "-d",
            "--name",
            container_name,
            "--network",
            f"container:{self._main_id}",
            *self._mount_args(sidecar.get("volume_mounts")),
            *self._agent_venv_args(),
            *self._resource_args(networked=False),
        ]
        for key, value in (sidecar.get("env") or {}).items():
            cmd.extend(["-e", f"{key}={value}"])
        for key in sidecar.get("forward_env") or []:
            if (value := os.getenv(key)) is not None:
                cmd.extend(["-e", f"{key}={value}"])
        if len(command) > 1:
            cmd.extend(["--entrypoint", command[0], self.config.image, *command[1:]])
        else:
            cmd.extend(["--entrypoint", command[0], self.config.image])
        self.logger.debug(f"Starting sidecar {name}: {shlex.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            raise RuntimeError(
                f"docker run sidecar {name!r} failed rc={result.returncode}: "
                f"{(result.stderr or result.stdout).strip()[:500]}"
            )
        self._sidecar_ids[name] = result.stdout.strip()

    def _resolve_container(self, container: str | None) -> str:
        if container is None or container == "main":
            return self._main_id
        try:
            return self._sidecar_ids[container]
        except KeyError:
            raise ValueError(
                f"unknown container {container!r} (main + {sorted(self._sidecar_ids)})"
            ) from None

    # ---- exec / copy -----------------------------------------------------

    def execute(
        self, command: str, cwd: str = "", timeout: int = None, container: str | None = None
    ) -> dict[str, Any]:
        cid = self._resolve_container(container)
        cwd = cwd or self.config.cwd
        cmd = [self.config.executable, "exec", "-w", cwd]
        if self.config.exec_user:
            cmd.extend(["-u", self.config.exec_user])
        for key in self.config.forward_env:
            if (value := os.getenv(key)) is not None:
                cmd.extend(["-e", f"{key}={value}"])
        for key, value in self.config.env.items():
            cmd.extend(["-e", f"{key}={value}"])
        cmd.extend([cid, "bash", "-c", command])
        result = subprocess.run(
            cmd,
            text=True,
            timeout=timeout or self.config.timeout,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        return {"output": result.stdout, "returncode": result.returncode}

    def execute_detached(self, command: str, cwd: str = "", timeout: int = None, **ignored) -> dict[str, Any]:
        return self.execute(command, cwd=cwd, timeout=timeout)

    @staticmethod
    def _dereferenced(src_path: str) -> str:
        """Same guard as k8s_sidecar: resolve the top level, refuse nested links."""
        resolved = os.path.realpath(src_path)
        if os.path.isdir(resolved):
            for root, dirs, files in os.walk(resolved, followlinks=False):
                for name in dirs + files:
                    if os.path.islink(os.path.join(root, name)):
                        raise ValueError(
                            f"copy_to(dereference=True) cannot resolve nested symlinks: "
                            f"{os.path.join(root, name)!r} inside {src_path!r}. Materialise "
                            f"the link in the task directory before uploading."
                        )
        return resolved

    def copy_to(
        self,
        src_path: str,
        dest_path: str,
        *,
        timeout: int = 300,
        max_retries: int = 3,
        container: str | None = None,
        dereference: bool = False,
    ) -> None:
        if dereference:
            src_path = self._dereferenced(src_path)
        cid = self._resolve_container(container)
        if not os.path.exists(src_path):
            raise FileNotFoundError(f"Source path not found: {src_path}")
        if os.path.isdir(src_path):
            # docker cp nests a directory INSIDE the destination, while kubectl
            # cp — for which these manifests were authored — streams the
            # directory's contents. Create the destination and use the src/.
            # idiom so the contents land at dest_path itself.
            dest_dir = dest_path.rstrip("/") or "/"
            mkdir_res = self.execute(f"mkdir -p '{dest_dir}'", container=container)
            if mkdir_res.get("returncode", 1) != 0:
                raise RuntimeError(mkdir_res.get("output", ""))
            target = f"{cid}:{dest_dir}/"
            cp_src = os.path.abspath(src_path) + "/."
            last_err = None
            for _ in range(max_retries):
                result = subprocess.run(
                    [self.config.executable, "cp", "-a", cp_src, target],
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                )
                if result.returncode == 0:
                    return
                last_err = (result.stderr or result.stdout).strip()
            raise RuntimeError(f"docker cp (dir contents) failed after {max_retries} tries: {last_err}")
        target = f"{cid}:{dest_path}"
        # docker cp requires the destination parent to exist (kubectl cp tolerated it);
        # same guard as mimoagent.environments.docker.DockerEnvironment.copy_to
        target_dir = dest_path if dest_path.endswith("/") else os.path.dirname(dest_path)
        if target_dir and target_dir not in ("", "."):
            mkdir_res = self.execute(f"mkdir -p '{target_dir}'", container=container)
            if mkdir_res.get("returncode", 1) != 0:
                raise RuntimeError(mkdir_res.get("output", ""))
        last_err = None
        for _ in range(max_retries):
            result = subprocess.run(
                [self.config.executable, "cp", "-a", os.path.abspath(src_path), target],
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            if result.returncode == 0:
                return
            last_err = result.stderr.strip()
        raise RuntimeError(f"docker cp to {target} failed after {max_retries} tries: {last_err}")

    def copy_out(
        self,
        src_path: str,
        dest_path: str,
        *,
        timeout: int = 300,
        max_retries: int = 3,
        container: str | None = None,
    ) -> None:
        cid = self._resolve_container(container)
        target = f"{cid}:{src_path}"
        os.makedirs(os.path.dirname(os.path.abspath(dest_path)), exist_ok=True)
        last_err = None
        for _ in range(max_retries):
            result = subprocess.run(
                [self.config.executable, "cp", "-a", target, dest_path],
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            if result.returncode == 0:
                return
            last_err = result.stderr.strip()
        raise RuntimeError(f"docker cp from {target} failed after {max_retries} tries: {last_err}")

    def cleanup(self):
        """Remove every container of this environment and its volume dirs."""
        ids = [self.container_id] + list(self._sidecar_ids.values())
        ids = [i for i in ids if i]
        if ids:
            subprocess.run(
                [self.config.executable, "rm", "-f", *ids],
                capture_output=True,
                text=True,
                timeout=60,
            )
        subprocess.run(["rm", "-rf", self._vol_root], capture_output=True, timeout=60)
        self.container_id = None
        self._sidecar_ids = {}
        self._started = False
