#!/usr/bin/env python3
from __future__ import print_function

import base64
import contextlib
import fcntl
import hashlib
import hmac
import json
import os
import shutil
import signal
import stat
import subprocess
import sys
import time
import traceback
import uuid

sys.dont_write_bytecode = True

import runtime_common as common

CONTRACT = "openmle_fast_linux_cgroup_namespace_runner_v1"
METADATA_SCHEMA = "openmle_fast_runner_metadata_v2"
REQUEST_SCHEMA = "openmle_fast_runner_request_v1"
RECEIPT_SCHEMA = "openmle_fast_runner_receipt_v1"
LIFECYCLE_REQUEST_SCHEMA = "openmle_fast_runner_lifecycle_request_v1"
LIFECYCLE_RECEIPT_SCHEMA = "openmle_fast_backend_lifecycle_v1"
STATE_SCHEMA = "openmle_fast_public_workspace_state_v1"
FIT_HOOK_CONTRACT = "openmle_fast_fit_hook_v1"
FIT_IMPLEMENTATION_CONTRACT = "openmle_fast_python_profile_fit_hook_v1"
ARTIFACT_LOCK_SHA256 = common._safe_hash(common.ARTIFACT_LOCK) or ("0" * 64)
LIFECYCLE_COMPLETION_GRACE_MS = 500

ACTION_PREPARATION_GRACE_MS = 12_000
ACTION_COMPLETION_GRACE_MS = 20_000
PUBLIC_FAULT_ROOT = os.path.join(common.SCRATCH, "public-faults")
PUBLIC_FAULT_MAX_RECORDS = 128

def _safe_exception_detail(exception, command):
    cause = getattr(exception, "original_cause", exception)
    if isinstance(cause, subprocess.CalledProcessError):
        detail = "subprocess returned %s" % cause.returncode
    elif isinstance(cause, subprocess.TimeoutExpired):
        detail = "subprocess timed out"
    else:
        detail = str(cause)
    if isinstance(command, str) and command:
        detail = detail.replace(command, "<policy-command>")
    return detail[:512]

def _write_public_fault(request, exception):

    directory_fd = None
    try:
        if not os.path.lexists(PUBLIC_FAULT_ROOT):
            try:
                os.makedirs(PUBLIC_FAULT_ROOT, 0o700)
            except OSError as exc:
                if exc.errno != getattr(os, "EEXIST", 17):
                    return
        flags = os.O_RDONLY
        flags |= getattr(os, "O_DIRECTORY", 0)
        flags |= getattr(os, "O_NOFOLLOW", 0)
        directory_fd = os.open(PUBLIC_FAULT_ROOT, flags)
        info = os.fstat(directory_fd)
        if not stat.S_ISDIR(info.st_mode) or info.st_uid != os.geteuid():
            return
        os.fchmod(directory_fd, 0o700)

        fcntl.flock(directory_fd, fcntl.LOCK_EX)

        command = request.get("command") if isinstance(request, dict) else None
        command_bytes = b""
        if isinstance(command, str):
            command_bytes = command.encode("utf-8", "replace")
        cause = getattr(exception, "original_cause", exception)
        extracted = traceback.extract_tb(getattr(cause, "__traceback__", None))
        frames = [
            {
                "file": os.path.basename(frame.filename)[:128],
                "function": frame.name[:128],
                "line": int(frame.lineno),
            }
            for frame in extracted[-6:]
        ]
        phase = getattr(exception, "phase", None)
        if not isinstance(phase, str) or not phase:
            phase = frames[-1]["function"] if frames else "public_runner_main"
        value = {
            "schema": "openmle_fast_public_runner_fault_v1",
            "pid": os.getpid(),
            "monotonic_ns": common.monotonic_ns(),
            "request_sha256": (
                common.canonical_sha256(request) if isinstance(request, dict) else None
            ),
            "timeout_ms": (
                request.get("timeout_ms") if isinstance(request, dict) else None
            ),
            "command_bytes": len(command_bytes),
            "command_sha256": common.bytes_sha256(command_bytes),
            "phase": phase[:96],
            "prior_phase": getattr(exception, "prior_phase", None),
            "exception_type": type(cause).__name__[:96],
            "exception_detail": _safe_exception_detail(exception, command),
            "traceback_frames": frames,
        }

        regular = []
        for name in os.listdir(directory_fd):
            try:
                info = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
            except OSError:
                continue
            if name.endswith(".json") and stat.S_ISREG(info.st_mode):
                regular.append((info.st_mtime, name))
        remove_count = max(0, len(regular) - PUBLIC_FAULT_MAX_RECORDS + 1)
        for _mtime, name in sorted(regular)[:remove_count]:
            try:
                os.unlink(name, dir_fd=directory_fd)
            except OSError:
                return

        payload = (common.canonical_json(value) + "\n").encode("utf-8")
        if len(payload) > 4096:
            return
        name = "%020d-%d-%s.json" % (
            value["monotonic_ns"],
            os.getpid(),
            uuid.uuid4().hex,
        )
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        flags |= getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(name, flags, 0o600, dir_fd=directory_fd)
        try:
            offset = 0
            while offset < len(payload):
                offset += os.write(descriptor, payload[offset:])
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
        os.fsync(directory_fd)
    except BaseException:
        
        return
    finally:
        if directory_fd is not None:
            try:
                fcntl.flock(directory_fd, fcntl.LOCK_UN)
            except OSError:
                pass
            os.close(directory_fd)

def metadata():
    preflight = common.active_preflight(ARTIFACT_LOCK_SHA256)
    controller = common.controller_attestation()
    coverage = preflight["all_checks_pass"]
    cgroup_v1 = controller["version"] in ("v1", "hybrid")
    controllers = controller["controllers"]
    formal = coverage and preflight["admission_stamp_valid"]
    true_if_covered = bool(coverage)
    failed_checks = sorted(
        name for name, passed in preflight["checks"].items() if not passed
    )
    ineligibility = []
    if failed_checks:
        ineligibility.append("active_preflight_failed:" + ",".join(failed_checks))
    if not preflight["admission_stamp_valid"]:
        ineligibility.append("live_admission_stamp_missing_or_invalid")
    return {
        "schema": METADATA_SCHEMA,
        "contract": CONTRACT,
        "runtime_digest": common.RUNTIME_DIGEST,
        "formal_eligible": formal,
        "formal_ineligibility": ineligibility,
        "kernel_release": os.uname()[2],
        "cgroup_version": controller["version"],
        "cgroup_mode": controller["version"],
        "cgroup_controller_attestation": controller,
        "cgroup_v1_cpu": cgroup_v1 and controllers["cpu"]["available"],
        "cgroup_v1_memory": cgroup_v1 and controllers["memory"]["available"],
        "cgroup_v1_pids": cgroup_v1 and controllers["pids"]["available"],
        "cgroup_v2_cpu": False,
        "cgroup_v2_memory": False,
        "cgroup_v2_pids": False,
        "cgroup_mounts_exposed_read_only": bool(cgroup_v1),
        "cgroup_v1_private_bind_remount": true_if_covered,
        "network_namespace": true_if_covered,
        "network_no_egress": true_if_covered,
        "dns_disabled": true_if_covered,
        "metadata_service_blocked": true_if_covered,
        "external_unix_sockets_blocked": true_if_covered,
        "pid_namespace": true_if_covered,
        "ipc_namespace": true_if_covered,
        "mount_namespace": true_if_covered,
        "user_namespace": true_if_covered,
        "workspace_quota": true_if_covered,
        "tmpfs_limit": true_if_covered,
        "file_size_limit": true_if_covered,
        "open_files_limit": true_if_covered,
        "fresh_unprivileged_uid_gid": true_if_covered,
        "capabilities_dropped": true_if_covered,
        "no_new_privs": true_if_covered,
        "seccomp": true_if_covered,
        "seccomp_contract": "openmle_fast_seccomp_deny_sensitive_v1",
        "read_only_rootfs": true_if_covered,
        "rootfs_kind": "read_only_overlay_over_pinned_oci_lower",
        "workspace_noexec": true_if_covered,
        "workspace_storage_contract": "owned_dedicated_tmpfs_at_most_2g_v1",
        "workspace_parent": common.PUBLIC_WORKSPACE_ROOT,
        "instrumented_python_only": true_if_covered,
        "isolated_proc": true_if_covered,
        "minimal_devices": true_if_covered,
        "gpu_devices_absent": true_if_covered,
        "core_dumps_disabled": true_if_covered,
        "mount_denied": true_if_covered,
        "ptrace_denied": true_if_covered,
        "setuid_denied": true_if_covered,
        "user_namespace_creation_denied": true_if_covered,
        "ebpf_denied": true_if_covered,
        "raw_sockets_denied": true_if_covered,
        "kernel_module_denied": true_if_covered,
        "container_engine_absent": true_if_covered,
        "background_process_detection": true_if_covered,
        "descendant_kill_reap": true_if_covered,
        "parent_death_cleanup_watchdog": true_if_covered,
        "freeze_reap": true_if_covered,
        "read_only_workspace_freeze": true_if_covered,
        "teardown_cgroup_empty": true_if_covered,
        "teardown_mount_empty": true_if_covered,
        "idempotent_teardown": true_if_covered,
        "lifecycle_completion_grace_ms": LIFECYCLE_COMPLETION_GRACE_MS,
        "execution_counter_coverage": "complete",
        "execution_counter_mechanism": "ptrace_exec_lineage_v1",
        "fit_counter_coverage": "partial",
        "cumulative_managed_runtime_budget": true_if_covered,
        "fit_hook_contract": FIT_HOOK_CONTRACT,
        "fit_hook_implementation_contract": FIT_IMPLEMENTATION_CONTRACT,
        "fit_hook_digest": hashlib.sha256(FIT_HOOK_CONTRACT.encode("utf-8")).hexdigest(),
        "cleanup_contract": "openmle_fast_owned_workspace_cgroup_mount_cleanup_v2",
        "ownership_contract": "openmle_fast_hmac_workspace_identity_state_v1",
        "active_verification": preflight,
        "artifact_identity": common.artifact_identity(ARTIFACT_LOCK_SHA256),
        "resource_limits": dict(common.PUBLIC_LIMITS),
    }

def validate_metadata(value):
    if not isinstance(value, dict) or value.get("schema") != METADATA_SCHEMA:
        raise common.RuntimeErrorClosed("metadata schema mismatch")
    if value.get("contract") != CONTRACT or value.get("runtime_digest") != common.RUNTIME_DIGEST:
        raise common.RuntimeErrorClosed("metadata identity mismatch")
    if value.get("resource_limits") != common.PUBLIC_LIMITS:
        raise common.RuntimeErrorClosed("resource limit drift")
    if value.get("cgroup_version") in ("v1", "hybrid"):
        for name in ("cgroup_v1_cpu", "cgroup_v1_memory", "cgroup_v1_pids"):
            if value.get(name) is not True:
                raise common.RuntimeErrorClosed("cgroup-v1 controller incomplete")
        for name in ("cgroup_v2_cpu", "cgroup_v2_memory", "cgroup_v2_pids"):
            if value.get(name) is not False:
                raise common.RuntimeErrorClosed("fabricated cgroup-v2 field")
    if value.get("formal_eligible") is True and not value["active_verification"].get(
        "admission_stamp_valid"
    ):
        raise common.RuntimeErrorClosed("formal admission lacks live stamp")
    return True

def _validate_execute_request(value):
    required = {
        "schema",
        "workspace",
        "command",
        "timeout_ms",
        "managed_runtime_budget_ms",
    }
    if not isinstance(value, dict) or set(value) != required:
        raise common.RuntimeErrorClosed("execute request fields mismatch")
    if value.get("schema") != REQUEST_SCHEMA:
        raise common.RuntimeErrorClosed("execute request schema mismatch")
    command = value.get("command")
    if not isinstance(command, str) or "\x00" in command:
        raise common.RuntimeErrorClosed("command must be NUL-free text")
    if len(command.encode("utf-8")) > 32 * common.KIB:
        raise common.RuntimeErrorClosed("command exceeds 32 KiB")
    timeout_ms = value.get("timeout_ms")
    if isinstance(timeout_ms, bool) or not isinstance(timeout_ms, int):
        raise common.RuntimeErrorClosed("timeout must be integer")
    if timeout_ms <= 0 or timeout_ms > common.PUBLIC_LIMITS["shell_wall_ms"]:
        raise common.RuntimeErrorClosed("timeout exceeds frozen one-action cap")
    managed_runtime_budget_ms = value.get("managed_runtime_budget_ms")
    if (
        isinstance(managed_runtime_budget_ms, bool)
        or not isinstance(managed_runtime_budget_ms, int)
    ):
        raise common.RuntimeErrorClosed("managed runtime budget must be integer")
    if (
        managed_runtime_budget_ms <= 0
        or managed_runtime_budget_ms
        > common.PUBLIC_LIMITS["managed_runtime_per_action_ms"]
    ):
        raise common.RuntimeErrorClosed(
            "managed runtime budget exceeds frozen one-action cap"
        )
    return value["workspace"], command, timeout_ms, managed_runtime_budget_ms

def _validate_lifecycle_request(value, operation):
    required = {"schema", "workspace", "operation", "timeout_ms"}
    if not isinstance(value, dict) or set(value) != required:
        raise common.RuntimeErrorClosed("lifecycle request fields mismatch")
    if value.get("schema") != LIFECYCLE_REQUEST_SCHEMA or value.get("operation") != operation:
        raise common.RuntimeErrorClosed("lifecycle request identity mismatch")
    timeout_ms = value.get("timeout_ms")
    if isinstance(timeout_ms, bool) or not isinstance(timeout_ms, int):
        raise common.RuntimeErrorClosed("lifecycle timeout must be integer")
    if timeout_ms <= 0 or timeout_ms > common.PUBLIC_LIMITS["shell_wall_ms"]:
        raise common.RuntimeErrorClosed("lifecycle timeout exceeds cap")
    return value["workspace"], timeout_ms

def _path_key(workspace):
    if not isinstance(workspace, str) or not workspace.startswith("/"):
        raise common.RuntimeErrorClosed("workspace path must be absolute")
    if os.path.normpath(workspace) != workspace:
        raise common.RuntimeErrorClosed("workspace path is not canonical")
    root = os.path.normpath(common.PUBLIC_WORKSPACE_ROOT)
    try:
        inside = os.path.commonpath((workspace, root)) == root
    except ValueError:
        inside = False
    if not inside or workspace == root:
        raise common.RuntimeErrorClosed("workspace is outside owned root")
    return hashlib.sha256(workspace.encode("utf-8")).hexdigest()

def _owner_key(deadline=None):
    common.ensure_runtime_directories(deadline=deadline)
    common.check_deadline(deadline, "state key access")
    path = os.path.join(common.STATE_ROOT, "owner.key")
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        descriptor = None
    if descriptor is not None:
        try:
            os.write(descriptor, os.urandom(32))
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
    info = os.lstat(path)
    if not stat.S_ISREG(info.st_mode) or stat.S_IMODE(info.st_mode) != 0o600 or info.st_nlink != 1:
        raise common.RuntimeErrorClosed("owner key is unsafe")
    with open(path, "rb") as handle:
        key = handle.read(33)
    if len(key) != 32:
        raise common.RuntimeErrorClosed("owner key length mismatch")
    common.check_deadline(deadline, "state key access")
    return key

def _state_paths(workspace):
    key = _path_key(workspace)
    return (
        os.path.join(common.STATE_ROOT, key + ".json"),
        os.path.join(common.STATE_ROOT, key + ".lock"),
    )

@contextlib.contextmanager
def _workspace_lock(workspace, deadline=None):
    common.ensure_runtime_directories(deadline=deadline)
    common.check_deadline(deadline, "workspace lock")
    state_path, lock_path = _state_paths(workspace)
    descriptor = os.open(lock_path, os.O_RDWR | os.O_CREAT, 0o600)
    try:
        while True:
            try:
                fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                common.check_deadline(deadline, "workspace lock")
                time.sleep(0.01)
        yield state_path
    finally:
        fcntl.flock(descriptor, fcntl.LOCK_UN)
        os.close(descriptor)

def _seal_state(body, deadline=None):
    payload = common.canonical_json(body).encode("utf-8")
    return hmac.new(_owner_key(deadline), payload, hashlib.sha256).hexdigest()

def _write_state(path, body, deadline=None):
    common.check_deadline(deadline, "state write")
    value = dict(body)
    value["state_hmac_sha256"] = _seal_state(body, deadline)
    temporary = path + ".tmp-%d" % os.getpid()
    descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        try:
            payload = (common.canonical_json(value) + "\n").encode("utf-8")
            os.write(descriptor, payload)
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
        common.check_deadline(deadline, "state write")
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except OSError:
            pass
        raise

def _read_state(path, deadline=None):
    common.check_deadline(deadline, "state read")
    try:
        info = os.lstat(path)
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise common.RuntimeErrorClosed("workspace state is unsafe")
        with open(path, "r") as handle:
            value = common.strict_json_loads(handle.read())
    except FileNotFoundError:
        return None
    except (OSError, ValueError):
        raise common.RuntimeErrorClosed("workspace state is unreadable")
    if not isinstance(value, dict) or "state_hmac_sha256" not in value:
        raise common.RuntimeErrorClosed("workspace state shape mismatch")
    seal = value.pop("state_hmac_sha256")
    if not isinstance(seal, str) or not hmac.compare_digest(
        seal, _seal_state(value, deadline)
    ):
        raise common.RuntimeErrorClosed("workspace state authentication failed")
    if value.get("schema") != STATE_SCHEMA or value.get("lifecycle") not in (
        "active",
        "freezing",
        "frozen",
        "tearing_down",
        "torn_down",
    ):
        raise common.RuntimeErrorClosed("workspace state contract mismatch")
    return value

def _new_state(identity):
    return {
        "schema": STATE_SCHEMA,
        "state_id": os.urandom(8).hex(),
        "workspace": identity["path"],
        "device": identity["device"],
        "inode": identity["inode"],
        "mount_id": identity["mount"]["mount_id"],
        "boot_id": common.boot_id(),
        "owner_uid": os.getuid(),
        "owner_gid": os.getgid(),
        "lifecycle": "active",
        "shell_actions": 0,
        "managed_runtime_ms": 0,
        "started_monotonic": time.monotonic(),
        "updated_monotonic": time.monotonic(),
    }

def _state_identity_matches(state, identity):
    return (
        state.get("workspace") == identity["path"]
        and state.get("device") == identity["device"]
        and state.get("inode") == identity["inode"]
        and state.get("mount_id") == identity["mount"]["mount_id"]
        and state.get("boot_id") == common.boot_id()
        and state.get("owner_uid") == os.getuid()
        and state.get("owner_gid") == os.getgid()
    )

def _adopt_or_validate_active(state_path, workspace, deadline=None):
    identity = common.validate_public_workspace(
        workspace, require_writable=True, deadline=deadline
    )
    state = _read_state(state_path, deadline=deadline)
    if state is None:
        state = _new_state(identity)
        _write_state(state_path, state, deadline=deadline)
        return state
    if state["lifecycle"] == "torn_down":
        if (
            state.get("device") == identity["device"]
            and state.get("inode") == identity["inode"]
            and state.get("mount_id") == identity["mount"]["mount_id"]
        ):
            raise common.RuntimeErrorClosed("torn-down workspace mount was reused unsafely")
        state = _new_state(identity)
        _write_state(state_path, state, deadline=deadline)
        return state
    if state["lifecycle"] != "active" or not _state_identity_matches(state, identity):
        raise common.RuntimeErrorClosed("workspace is frozen, foreign, or identity-drifted")
    return state

def _owned_state_or_adopt(state_path, workspace, deadline=None):

    state = _read_state(state_path, deadline=deadline)
    if state is None:
        state = _adopt_or_validate_active(
            state_path, workspace, deadline=deadline
        )
    return state

def _execution_receipt(result, failure_override=None):
    failure = failure_override if failure_override is not None else result["failure_class"]
    return {
        "schema": RECEIPT_SCHEMA,
        "stdout_b64": base64.b64encode(result["stdout"]).decode("ascii"),
        "stderr_b64": base64.b64encode(result["stderr"]).decode("ascii"),
        "exit_code": result["exit_code"],
        "timed_out": bool(result["timed_out"]),
        "wall_seconds": max(0.0, float(result["wall_seconds"])),
        "managed_runtime_wall_seconds": max(
            0.0, float(result["managed_runtime_wall_seconds"])
        ),
        "cpu_seconds": max(0.0, float(result["cpu_seconds"])),
        "peak_rss_bytes": max(0, int(result["peak_rss_bytes"])),
        "bytes_read": max(0, int(result["bytes_read"])),
        "bytes_written": max(0, int(result["bytes_written"])),
        "process_peak": max(0, int(result["process_peak"])),
        "execution_attempt_delta": max(0, int(result["execution_attempt_delta"])),
        "execution_completed_delta": max(0, int(result["execution_completed_delta"])),
        "nested_subprocess_delta": max(0, int(result["nested_subprocess_delta"])),
        "fit_delta": max(0, int(result["fit_delta"])),
        "fit_counter_coverage": "partial",
        "failure_class": failure,
        "infrastructure_fault": bool(result["infrastructure_fault"]),
    }

def infrastructure_receipt():
    return {
        "schema": RECEIPT_SCHEMA,
        "stdout_b64": "",
        "stderr_b64": "",
        "exit_code": None,
        "timed_out": False,
        "wall_seconds": 0.0,
        "managed_runtime_wall_seconds": 0.0,
        "cpu_seconds": 0.0,
        "peak_rss_bytes": 0,
        "bytes_read": 0,
        "bytes_written": 0,
        "process_peak": 0,
        "execution_attempt_delta": 0,
        "execution_completed_delta": 0,
        "nested_subprocess_delta": 0,
        "fit_delta": 0,
        "fit_counter_coverage": "partial",
        "failure_class": "runner_infrastructure_fault",
        "infrastructure_fault": True,
    }

class BudgetLedgerExhausted(common.RuntimeErrorClosed):

    def __init__(self, message, failure_class):
        super().__init__(message)
        if failure_class not in (
            "wall_timeout",
            "managed_runtime_limit",
            "action_budget_exhausted",
        ):
            raise ValueError("unsupported budget failure class")
        self.failure_class = failure_class

def budget_exhausted_receipt(failure_class):
    return {
        "schema": RECEIPT_SCHEMA,
        "stdout_b64": "",
        "stderr_b64": "",
        "exit_code": None,
        "timed_out": False,
        "wall_seconds": 0.0,
        "managed_runtime_wall_seconds": 0.0,
        "cpu_seconds": 0.0,
        "peak_rss_bytes": 0,
        "bytes_read": 0,
        "bytes_written": 0,
        "process_peak": 0,
        "execution_attempt_delta": 0,
        "execution_completed_delta": 0,
        "nested_subprocess_delta": 0,
        "fit_delta": 0,
        "fit_counter_coverage": "partial",
        "failure_class": failure_class,
        "infrastructure_fault": False,
    }

def execute(value):
    request_started = time.monotonic()
    common.require_runtime_admission(
        ARTIFACT_LOCK_SHA256, operation="public.execute", request=value
    )
    (
        workspace,
        command,
        timeout_ms,
        adapter_managed_runtime_budget_ms,
    ) = _validate_execute_request(value)
    action_deadline = request_started + (
        ACTION_PREPARATION_GRACE_MS + timeout_ms + ACTION_COMPLETION_GRACE_MS
    ) / 1000.0
    with _workspace_lock(workspace, deadline=action_deadline) as state_path:
        state = _adopt_or_validate_active(
            state_path, workspace, deadline=action_deadline
        )
        now = time.monotonic()
        if state["boot_id"] != common.boot_id():
            raise common.RuntimeErrorClosed("workspace state crossed a boot boundary")
        if state["shell_actions"] >= common.PUBLIC_LIMITS["max_policy_actions"]:
            raise BudgetLedgerExhausted(
                "shell action ledger exhausted",
                failure_class="action_budget_exhausted",
            )
        if (
            (now - state["started_monotonic"]) * 1000.0
            >= common.PUBLIC_LIMITS["episode_wall_ms"]
        ):
            raise BudgetLedgerExhausted(
                "episode wall ledger exhausted",
                failure_class="wall_timeout",
            )
        if state["managed_runtime_ms"] >= common.PUBLIC_LIMITS[
            "managed_runtime_per_episode_ms"
        ]:
            raise BudgetLedgerExhausted(
                "episode managed-runtime ledger exhausted",
                failure_class="managed_runtime_limit",
            )
        before = common.scan_workspace(
            workspace, common.PUBLIC_LIMITS, deadline=action_deadline
        )
        now = time.monotonic()
        remaining_wall_ms = int(
            common.PUBLIC_LIMITS["episode_wall_ms"]
            - (now - state["started_monotonic"]) * 1000.0
        )
        remaining_managed_ms = (
            common.PUBLIC_LIMITS["managed_runtime_per_episode_ms"]
            - state["managed_runtime_ms"]
        )
        action_timeout_ms = min(
            timeout_ms,
            remaining_wall_ms - ACTION_COMPLETION_GRACE_MS,
        )
        remaining_request_ms = int((action_deadline - now) * 1000.0)

        if (
            action_timeout_ms > 0
            and remaining_request_ms
            <= action_timeout_ms + ACTION_COMPLETION_GRACE_MS
        ):
            raise common.RuntimeErrorClosed(
                "request exhausted the host preparation grace"
            )
        action_managed_ms = min(
            common.PUBLIC_LIMITS["managed_runtime_per_action_ms"],
            remaining_managed_ms,
            adapter_managed_runtime_budget_ms,
        )
        if action_timeout_ms <= 0:
            raise BudgetLedgerExhausted(
                "episode wall ledger leaves no action budget",
                failure_class="wall_timeout",
            )
        if action_managed_ms <= 0:
            raise BudgetLedgerExhausted(
                "episode managed-runtime ledger leaves no action budget",
                failure_class="managed_runtime_limit",
            )
        state["shell_actions"] += 1
        state["updated_monotonic"] = now
        _write_state(state_path, state, deadline=action_deadline)
        try:
            result = common.run_sandbox(
                workspace=workspace,
                command=command,
                timeout_ms=action_timeout_ms,
                cpu_vcpus=common.PUBLIC_LIMITS["cpu_vcpus"],
                memory_bytes=common.PUBLIC_LIMITS["memory_bytes"],
                max_processes=common.PUBLIC_LIMITS["max_processes"],
                managed_ms=action_managed_ms,
                max_open_files=common.PUBLIC_LIMITS["max_open_files"],
                max_file_bytes=common.PUBLIC_LIMITS["max_file_bytes"],
                output_cap=common.PUBLIC_LIMITS["raw_output_bytes"],
                run_name="public-" + state["state_id"],
                deadline=action_deadline,
            )
        except BaseException:
            state["updated_monotonic"] = time.monotonic()
            _write_state(state_path, state, deadline=action_deadline)
            raise
        state["managed_runtime_ms"] += int(
            round(result["managed_runtime_wall_seconds"] * 1000.0)
        )
        state["updated_monotonic"] = time.monotonic()
        _write_state(state_path, state, deadline=action_deadline)
        after = common.scan_workspace(
            workspace, common.PUBLIC_LIMITS, deadline=action_deadline
        )
        failure_override = None
        if (
            result["failure_class"] is None
            and after["free_bytes"] <= max(4096, after["capacity_bytes"] // 1000)
            and result["exit_code"] != 0
        ):
            failure_override = "disk_limit"
        if (
            state["managed_runtime_ms"]
            > common.PUBLIC_LIMITS["managed_runtime_per_episode_ms"]
        ):
            failure_override = "managed_runtime_limit"
        del before
        return _execution_receipt(result, failure_override=failure_override)

def _make_tree_read_only(workspace, deadline):
    for root, directories, files in os.walk(workspace, topdown=False, followlinks=False):
        if time.monotonic() >= deadline:
            raise common.RuntimeErrorClosed("freeze deadline expired")
        for name in files:
            common.check_deadline(deadline, "freeze")
            path = os.path.join(root, name)
            info = os.lstat(path)
            if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
                raise common.RuntimeErrorClosed("unsafe file appeared during freeze")
            os.chmod(path, 0o444)
        for name in directories:
            common.check_deadline(deadline, "freeze")
            path = os.path.join(root, name)
            info = os.lstat(path)
            if not stat.S_ISDIR(info.st_mode) or stat.S_ISLNK(info.st_mode):
                raise common.RuntimeErrorClosed("unsafe directory appeared during freeze")
            os.chmod(path, 0o555)
    os.chmod(workspace, 0o555)
    common.run_checked(
        ["/usr/bin/mount", "-o", "remount,ro,noexec,nosuid,nodev", workspace],
        deadline=deadline,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

def _lifecycle_receipt(operation, success, reaped, read_only, empty, failure=None):
    return {
        "schema": LIFECYCLE_RECEIPT_SCHEMA,
        "operation": operation,
        "success": bool(success),
        "processes_reaped": bool(reaped),
        "workspace_read_only": bool(read_only),
        "cgroup_empty": bool(empty),
        "failure_class": failure,
    }

def lifecycle_failure(operation, failure="runner_lifecycle_fault"):
    return _lifecycle_receipt(operation, False, False, False, False, failure)

def _lifecycle_cleanup(state, deadline):
    common.check_deadline(deadline, "lifecycle cleanup")
    cleanup = common.reap_named_cgroups(state["state_id"], deadline=deadline)
    runs_clean = common.cleanup_named_run_directories(
        state["state_id"], deadline=deadline
    )
    residue = common.residue_snapshot(state["state_id"], deadline=deadline)
    reaped = (
        cleanup.get("child_exit_zero") is True
        and not cleanup.get("failures")
        and not residue["errors"]
        and not residue["processes"]
    )
    empty = (
        runs_clean
        and not residue["cgroups"]
        and not residue["mounts"]
        and not residue["run_entries"]
    )
    return reaped, empty

def _set_lifecycle(state_path, state, lifecycle, deadline=None):
    state["lifecycle"] = lifecycle
    state["updated_monotonic"] = time.monotonic()
    _write_state(state_path, state, deadline=deadline)

def _workspace_mount_if_any(workspace, deadline=None):
    mount = common.exact_mount(workspace, required=False, deadline=deadline)
    if mount is None:
        return None
    return common.validate_public_workspace(
        workspace, require_writable=False, deadline=deadline
    )

def freeze(value):
    started = time.monotonic()
    common.require_runtime_admission(
        ARTIFACT_LOCK_SHA256, operation="public.freeze", request=value
    )
    workspace, timeout_ms = _validate_lifecycle_request(value, "freeze")
    if timeout_ms <= LIFECYCLE_COMPLETION_GRACE_MS:
        raise common.RuntimeErrorClosed("freeze timeout leaves no cleanup grace")
    deadline = started + (
        timeout_ms - LIFECYCLE_COMPLETION_GRACE_MS
    ) / 1000.0
    with _workspace_lock(workspace, deadline=deadline) as state_path:
        state = _owned_state_or_adopt(state_path, workspace, deadline=deadline)
        if state["lifecycle"] in ("tearing_down", "torn_down"):
            raise common.RuntimeErrorClosed("cannot freeze non-owned workspace")
        identity = common.validate_public_workspace(
            workspace, require_writable=False, deadline=deadline
        )
        if not _state_identity_matches(state, identity):
            raise common.RuntimeErrorClosed("workspace identity drifted")
        if state["lifecycle"] == "active":
            _set_lifecycle(state_path, state, "freezing", deadline=deadline)
        reaped, empty = _lifecycle_cleanup(state, deadline)
        if not reaped or not empty:
            return _lifecycle_receipt(
                "freeze", False, reaped, False, empty, "owned_residue_remains"
            )
        mount = common.exact_mount(workspace, deadline=deadline)
        options = set(mount["mount_options"]) | set(mount["super_options"])
        if state["lifecycle"] == "frozen" and "ro" not in options:
            raise common.RuntimeErrorClosed("frozen workspace became writable")
        if "ro" not in options:
            _make_tree_read_only(workspace, deadline)
        common.check_deadline(deadline, "freeze")
        mount = common.exact_mount(workspace, deadline=deadline)
        options = set(mount["mount_options"]) | set(mount["super_options"])
        read_only = "ro" in options
        if read_only:
            _set_lifecycle(state_path, state, "frozen", deadline=deadline)
        success = reaped and empty and read_only
        return _lifecycle_receipt(
            "freeze",
            success,
            reaped,
            read_only,
            empty,
            None if success else "workspace_freeze_failure",
        )

def teardown(value):
    started = time.monotonic()
    common.require_runtime_admission(
        ARTIFACT_LOCK_SHA256, operation="public.teardown", request=value
    )
    workspace, timeout_ms = _validate_lifecycle_request(value, "teardown")
    if timeout_ms <= LIFECYCLE_COMPLETION_GRACE_MS:
        raise common.RuntimeErrorClosed("teardown timeout leaves no cleanup grace")
    deadline = started + (
        timeout_ms - LIFECYCLE_COMPLETION_GRACE_MS
    ) / 1000.0
    with _workspace_lock(workspace, deadline=deadline) as state_path:
        state = _owned_state_or_adopt(state_path, workspace, deadline=deadline)
        if state["lifecycle"] == "torn_down":
            if common.exact_mount(
                workspace, required=False, deadline=deadline
            ) is not None:
                raise common.RuntimeErrorClosed("torn-down workspace was remounted")
            reaped, empty = _lifecycle_cleanup(state, deadline)
            success = reaped and empty
            return _lifecycle_receipt(
                "teardown",
                success,
                reaped,
                False,
                empty,
                None if success else "owned_residue_remains",
            )
        identity = _workspace_mount_if_any(workspace, deadline=deadline)
        if identity is not None and not _state_identity_matches(state, identity):
            raise common.RuntimeErrorClosed("workspace identity drifted")
        if state["lifecycle"] != "tearing_down":
            if identity is None:
                raise common.RuntimeErrorClosed("owned workspace mount disappeared")
            _set_lifecycle(state_path, state, "tearing_down", deadline=deadline)
        reaped, empty = _lifecycle_cleanup(state, deadline)
        if not reaped or not empty:
            return _lifecycle_receipt(
                "teardown", False, reaped, False, empty, "owned_residue_remains"
            )
        if common.exact_mount(
            workspace, required=False, deadline=deadline
        ) is not None:
            common.run_checked(
                ["/usr/bin/umount", workspace],
                deadline=deadline,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        if common.exact_mount(
            workspace, required=False, deadline=deadline
        ) is not None:
            return _lifecycle_receipt(
                "teardown", False, True, False, True, "workspace_unmount_failure"
            )
        common.check_deadline(deadline, "teardown")
        _set_lifecycle(state_path, state, "torn_down", deadline=deadline)
        residue = common.residue_snapshot(state["state_id"], deadline=deadline)
        empty = common.residue_is_zero(residue)
        return _lifecycle_receipt(
            "teardown",
            empty,
            True,
            False,
            empty,
            None if empty else "owned_residue_remains",
        )

def main(argv):
    if len(argv) != 2 or argv[1] not in (
        "metadata",
        "execute",
        "freeze",
        "teardown",
    ):
        print("usage: public_runner.py {metadata|execute|freeze|teardown}", file=sys.stderr)
        return 2
    operation = argv[1]
    if operation == "metadata":
        value = metadata()
        
        if value["cgroup_version"] in ("v1", "hybrid") and value["active_verification"][
            "all_checks_pass"
        ]:
            validate_metadata(value)
        print(common.canonical_json(value))
        return 0
    request = None
    try:
        request = common.read_stdin_json()
        if operation == "execute":
            result = execute(request)
        elif operation == "freeze":
            result = freeze(request)
        else:
            result = teardown(request)
    except BudgetLedgerExhausted as exc:
        result = budget_exhausted_receipt(exc.failure_class)
    except BaseException as exc:
        if operation == "execute":
            _write_public_fault(
                request if isinstance(request, dict) else None,
                exc,
            )
            result = infrastructure_receipt()
        else:
            result = lifecycle_failure(operation)
    print(common.canonical_json(result))
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
