"""Run one configured task service in the foreground, bound to loopback."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import secrets
import signal
import subprocess
import sys
import time
import ctypes
import threading

from .configure import ENVIRONMENTS, PORTS, ROOT


def validate_settings(name: str, settings: dict) -> None:
    if name not in ENVIRONMENTS or not isinstance(settings, dict):
        raise ValueError("Unknown environment configuration")
    for key, value in settings.items():
        if not isinstance(key, str) or not key.replace("_", "").isalnum() or not isinstance(value, str) or "\0" in value:
            raise ValueError("Service settings must contain plain environment-variable strings")
        if key.endswith("_HOST") and value != "127.0.0.1":
            raise ValueError("Task services must bind to 127.0.0.1")
        if key.endswith("_PORT") and int(value) != PORTS[name]:
            raise ValueError("Service port differs from the prepared routes")
    if name in {"general", "visual"}:
        prefix = "GA" if name == "general" else "WD"
        for suffix in ("URL", "KEY", "MODEL"):
            key = prefix + "_JUDGE_" + suffix
            if not os.environ.get(key):
                raise ValueError(f"Set {key} explicitly in the service environment; judge credentials are not saved in configuration")


def launch_public(name: str) -> None:
    if name == "shop":
        import uvicorn
        uvicorn.run("camg.services.shop.server:app", host="127.0.0.1", port=PORTS[name], workers=1)
    elif name in {"coding", "autoresearch"}:
        from importlib import import_module
        import_module(f"camg.services.{name}.launch").launch()
    else:
        from importlib import import_module
        import_module(f"camg.services.{name}.launch").main()


def run_autoresearch() -> None:
    credential = Path(os.environ["OPENMLE_FAST_GRADER_CREDENTIAL"])
    credential.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    # Never reuse a credential/socket from a different service invocation.
    socket = Path(os.environ["OPENMLE_FAST_GRADER_ENDPOINT"])
    if credential.exists() or socket.exists():
        raise FileExistsError("AutoResearch service state already exists; use a new state_root after checking the prior service has stopped")
    fd = os.open(credential, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write(secrets.token_bytes(64))
    parent = os.getpid()
    def parent_death_signal():
        # This runs before exec, before starting threads in the child.
        libc = ctypes.CDLL(None, use_errno=True)
        if libc.prctl(1, signal.SIGTERM, 0, 0, 0) != 0 or os.getppid() != parent:
            os._exit(125)
    child = None
    monitor_stop = threading.Event()
    monitor = None
    previous = {}
    def stop(signum, _frame):
        raise KeyboardInterrupt(f"Service received signal {signum}")
    for sig in (signal.SIGTERM, signal.SIGINT):
        previous[sig] = signal.signal(sig, stop)
    try:
        child = subprocess.Popen([sys.executable, "-m", "camg.serve", "--private-grader"],
            start_new_session=True, preexec_fn=parent_death_signal)
        deadline = time.monotonic() + 120
        while not socket.exists():
            if child.poll() is not None:
                raise RuntimeError(f"Private grader stopped during startup (exit {child.returncode})")
            if time.monotonic() >= deadline:
                raise TimeoutError("Private grader did not create its local socket")
            time.sleep(0.2)
        def watch_grader():
            while not monitor_stop.wait(0.5):
                if child.poll() is not None:
                    print("Private grader stopped; shutting down the task service.", file=sys.stderr)
                    os.kill(parent, signal.SIGTERM)
                    return
        monitor = threading.Thread(target=watch_grader, daemon=True, name="camg-grader-watch")
        monitor.start()
        launch_public("autoresearch")
    finally:
        monitor_stop.set()
        if monitor is not None:
            monitor.join(timeout=2)
        if child is not None and child.poll() is None:
            child.terminate()
            try:
                child.wait(timeout=120)
            except subprocess.TimeoutExpired:
                child.kill()
                child.wait()
        for sig, handler in previous.items():
            signal.signal(sig, handler)
        credential.unlink(missing_ok=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--check-config", action="store_true", help="Validate configuration only; do not start services")
    parser.add_argument("--private-grader", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if args.private_grader:
        if sys.platform != "linux":
            raise RuntimeError("The isolated grader requires Linux")
        from .services.autoresearch.launch import launch_private_grader
        def stop_private(_signum, _frame):
            raise KeyboardInterrupt("Private grader shutdown requested")
        signal.signal(signal.SIGTERM, stop_private)
        launch_private_grader()
        return
    if args.config is None:
        parser.error("--config is required")
    config = json.loads(args.config.read_text())
    name, settings = config["environment"], config["settings"]
    validate_settings(name, settings)
    if args.check_config:
        print(f"{name}: settings checked. Assets, containers and runtime have not been executed.")
        return
    if sys.platform != "linux":
        raise RuntimeError("Task execution services require Linux; configuration checks can run elsewhere")
    os.environ.update(settings)
    extra = [ROOT / "third_party/mimo_runtime", ROOT / "third_party/mimo_runtime/mimoagent/src", ROOT / "third_party/swebench_shim"]
    for path in reversed(extra):
        sys.path.insert(0, str(path))
    os.environ["PYTHONPATH"] = os.pathsep.join([str(ROOT), *(str(p) for p in extra), os.environ.get("PYTHONPATH", "")])
    for prefix in ("AGENTGENERAL", "WEBDEV"):
        os.environ.setdefault(prefix + "_DETAIL_TOKEN", secrets.token_urlsafe(32))
    if name == "autoresearch":
        run_autoresearch()
    else:
        launch_public(name)


if __name__ == "__main__":
    main()
