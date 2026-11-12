#!/usr/bin/env python3
from __future__ import print_function

import base64
import fcntl
import math
import os
import shlex
import shutil
import stat
import subprocess
import sys
import time
import uuid

sys.dont_write_bytecode = True

import runtime_common as common

CONTRACT = "openmle_fast_private_grader_runner_v1"
METADATA_SCHEMA = "openmle_fast_private_runner_metadata_v2"
REQUEST_SCHEMA = "openmle_fast_private_runner_request_v1"
RESULT_SCHEMA = "openmle_fast_private_worker_result_v1"
ARTIFACT_LOCK_SHA256 = common._safe_hash(common.ARTIFACT_LOCK) or ("0" * 64)
COMPLETION_GRACE_MS = 750
STAGE_CLEANUP_TIMEOUT_MS = 2000
PROBE_FAULT_ROOT = os.path.join(common.SCRATCH, "probe-private-faults")
FORMAL_FAULT_ROOT_ENV = "OPENMLE_FAST_PRIVATE_FAULT_AUDIT_ROOT"
PROCESS_OWNER_ENV = "OPENMLE_FAST_PROCESS_OWNER"
RUN_ID_ENV = "OPENMLE_FAST_RUN_ID"
REQUEST_ID_SHA256_ENV = "OPENMLE_FAST_PRIVATE_REQUEST_ID_SHA256"
EPISODE_ID_SHA256_ENV = "OPENMLE_FAST_PRIVATE_EPISODE_ID_SHA256"
PRIVATE_FAULT_MAX_RECORDS = 512

def _bounded_context_text(name):
    value = os.environ.get(name)
    if (
        not isinstance(value, str)
        or not value
        or len(value) > 256
        or any(ord(character) < 32 or ord(character) > 126 for character in value)
    ):
        return None
    return value

def _diagnostic_digest(name):
    value = os.environ.get(name)
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(character not in "0123456789abcdef" for character in value)
    ):
        return None
    return value

def _formal_fault_context():
    root = os.environ.get(FORMAL_FAULT_ROOT_ENV)
    owner = _bounded_context_text(PROCESS_OWNER_ENV)
    run_id = _bounded_context_text(RUN_ID_ENV)
    request_id_sha256 = _diagnostic_digest(REQUEST_ID_SHA256_ENV)
    episode_id_sha256 = _diagnostic_digest(EPISODE_ID_SHA256_ENV)
    if (
        not isinstance(root, str)
        or not root
        or not os.path.isabs(root)
        or os.path.normpath(root) != root
        or owner is None
        or run_id is None
        or request_id_sha256 is None
        or episode_id_sha256 is None
    ):
        return None
    return {
        "root": root,
        "schema": "openmle_fast_private_runtime_fault_v1",
        "prefix": "runtime-fault-",
        "process_owner": owner,
        "run_id": run_id,
        "request_id_sha256": request_id_sha256,
        "episode_id_sha256": episode_id_sha256,
    }

def _safe_exception_identity(exception):
    if exception is None:
        return None, None, None
    cause = getattr(exception, "original_cause", exception)
    detail = str(cause).encode("utf-8", "replace")
    return type(cause).__name__[:96], len(detail), common.bytes_sha256(detail)

def _write_probe_fault(kind, request=None, exception=None, sandbox=None):

    directory_fd = None
    try:
        if common._parent_is_exact_remote_probe(os.getppid()):
            session = common.load_probe_session()
            if not isinstance(session, dict):
                return
            context = {
                "root": PROBE_FAULT_ROOT,
                "schema": "openmle_fast_private_probe_fault_v1",
                "prefix": "",
                "probe_session_id": session.get("probe_session_id"),
            }
            if not os.path.lexists(PROBE_FAULT_ROOT):
                os.makedirs(PROBE_FAULT_ROOT, 0o700)
        else:
            context = _formal_fault_context()
            if context is None:
                return

        root = context.pop("root")
        prefix = context.pop("prefix")
        flags = os.O_RDONLY
        flags |= getattr(os, "O_DIRECTORY", 0)
        flags |= getattr(os, "O_NOFOLLOW", 0)
        directory_fd = os.open(root, flags)
        info = os.fstat(directory_fd)
        if not stat.S_ISDIR(info.st_mode) or info.st_uid != os.geteuid():
            return
        os.fchmod(directory_fd, 0o700)
        fcntl.flock(directory_fd, fcntl.LOCK_EX)

        exception_type, exception_bytes, exception_sha256 = _safe_exception_identity(
            exception
        )
        request_identity = {}
        if isinstance(request, dict):
            for name in (
                "task_id",
                "grader_binding_sha256",
                "package_identity_sha256",
                "metric_sha256",
                "answer_sha256",
                "submission_sha256",
                "higher_is_better",
            ):
                request_identity[name] = request.get(name)
        value = {
            "schema": context.pop("schema"),
            "kind": str(kind)[:96],
            "pid": os.getpid(),
            "monotonic_ns": common.monotonic_ns(),
            "request_identity_sha256": (
                common.canonical_sha256(request_identity) if request_identity else None
            ),
            "task_id": request_identity.get("task_id"),
            "grader_binding_sha256": request_identity.get("grader_binding_sha256"),
            "package_identity_sha256": request_identity.get("package_identity_sha256"),
            "submission_sha256": request_identity.get("submission_sha256"),
            "exception_type": exception_type,
            "exception_detail_bytes": exception_bytes,
            "exception_detail_sha256": exception_sha256,
            "sandbox": None,
        }
        value.update(context)
        if isinstance(sandbox, dict):
            allow = (
                "infrastructure_fault",
                "failure_class",
                "exit_code",
                "timed_out",
                "wall_seconds",
                "managed_runtime_wall_seconds",
                "cpu_seconds",
                "peak_rss_bytes",
                "process_peak",
                "execution_attempt_delta",
                "execution_completed_delta",
                "nested_subprocess_delta",
                "fit_delta",
            )
            value["sandbox"] = {name: sandbox.get(name) for name in allow}

        regular = []
        for name in os.listdir(directory_fd):
            if not name.startswith(prefix) or not name.endswith(".json"):
                continue
            try:
                child = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
            except OSError:
                continue
            if stat.S_ISREG(child.st_mode):
                regular.append((child.st_mtime, name))
        remove_count = max(0, len(regular) - PRIVATE_FAULT_MAX_RECORDS + 1)
        for _mtime, name in sorted(regular)[:remove_count]:
            try:
                os.unlink(name, dir_fd=directory_fd)
            except OSError:
                return

        payload = (common.canonical_json(value) + "\n").encode("utf-8")
        if len(payload) > 4096:
            return
        name = "%s%020d-%d-%s.json" % (
            prefix,
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
    except BaseException:
        
        return
    finally:
        if directory_fd is not None:
            try:
                os.close(directory_fd)
            except OSError:
                pass

def metadata():
    preflight = common.active_preflight(ARTIFACT_LOCK_SHA256)
    controller = common.controller_attestation()
    coverage = preflight["all_checks_pass"]
    cgroup_v1 = controller["version"] in ("v1", "hybrid")
    controllers = controller["controllers"]
    formal = coverage and preflight["admission_stamp_valid"]
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
        "fresh_worker_per_grade": coverage,
        "selected_task_only_mounts": coverage,
        "staged_task_files": ["metric.py", "answer.csv", "submission.csv"],
        "submission_passed_by_fd": coverage,
        "all_task_inputs_passed_by_fd": coverage,
        "result_sanitized_ipc": coverage,
        "service_environment_hidden": coverage,
        "network_namespace": coverage,
        "network_no_egress": coverage,
        "dns_disabled": coverage,
        "metadata_service_blocked": coverage,
        "external_unix_sockets_blocked": coverage,
        "pid_namespace": coverage,
        "ipc_namespace": coverage,
        "mount_namespace": coverage,
        "fresh_unprivileged_uid_gid": coverage,
        "capabilities_dropped": coverage,
        "no_new_privs": coverage,
        "seccomp": coverage,
        "read_only_rootfs": coverage,
        "isolated_proc": coverage,
        "minimal_devices": coverage,
        "gpu_devices_absent": coverage,
        "core_dumps_disabled": coverage,
        "hard_wall_supervision": coverage,
        "runner_completion_grace_ms": COMPLETION_GRACE_MS,
        "descendant_kill_reap": coverage,
        "parent_death_cleanup_watchdog": coverage,
        "worker_teardown_verified": coverage,
        "validate_submission_once": coverage,
        "evaluate_once_after_validation": coverage,
        "worker_result_schema": RESULT_SCHEMA,
        "worker_source_sha256": common._safe_hash(common.PRIVATE_WORKER),
        "active_verification": preflight,
        "artifact_identity": common.artifact_identity(ARTIFACT_LOCK_SHA256),
        "resource_limits": dict(common.PRIVATE_LIMITS),
    }

def _is_sha256(value):
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )

def _validate_request(value):
    required = {
        "schema",
        "task_id",
        "grader_binding_sha256",
        "package_identity_sha256",
        "metric_sha256",
        "answer_sha256",
        "submission_sha256",
        "higher_is_better",
        "validator_success_forms",
        "metric_fd",
        "answer_fd",
        "submission_fd",
        "timeout_ms",
    }
    if not isinstance(value, dict) or set(value) != required:
        raise common.RuntimeErrorClosed("private request fields mismatch")
    if value.get("schema") != REQUEST_SCHEMA:
        raise common.RuntimeErrorClosed("private request schema mismatch")
    task_id = value.get("task_id")
    if (
        not isinstance(task_id, str)
        or not task_id
        or len(task_id.encode("utf-8")) > 512
        or any(ord(character) < 32 for character in task_id)
    ):
        raise common.RuntimeErrorClosed("task identity is invalid")
    for name in (
        "grader_binding_sha256",
        "package_identity_sha256",
        "metric_sha256",
        "answer_sha256",
        "submission_sha256",
    ):
        if not _is_sha256(value.get(name)):
            raise common.RuntimeErrorClosed("private digest is invalid")
    if type(value.get("higher_is_better")) is not bool:
        raise common.RuntimeErrorClosed("private direction is invalid")
    forms = value.get("validator_success_forms")
    if (
        not isinstance(forms, list)
        or len(forms) > 64
        or any(not isinstance(item, str) or len(item.encode("utf-8")) > 256 for item in forms)
    ):
        raise common.RuntimeErrorClosed("validation convention list is invalid")
    descriptors = tuple(value.get(name) for name in ("metric_fd", "answer_fd", "submission_fd"))
    if (
        any(isinstance(item, bool) or not isinstance(item, int) or item < 3 for item in descriptors)
        or len(set(descriptors)) != 3
    ):
        raise common.RuntimeErrorClosed("private descriptors are invalid")
    timeout_ms = value.get("timeout_ms")
    if (
        isinstance(timeout_ms, bool)
        or not isinstance(timeout_ms, int)
        or timeout_ms <= 0
        or timeout_ms > common.PRIVATE_LIMITS["wall_ms"]
    ):
        raise common.RuntimeErrorClosed("private timeout exceeds frozen cap")
    return descriptors

def _read_regular_fd(descriptor, maximum, deadline=None):
    common.check_deadline(deadline, "private FD read")
    flags = fcntl.fcntl(descriptor, fcntl.F_GETFL)
    if flags & os.O_ACCMODE != os.O_RDONLY:
        raise common.RuntimeErrorClosed("private descriptor is not read-only")
    info = os.fstat(descriptor)
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_size > maximum:
        raise common.RuntimeErrorClosed("private descriptor is not independent bounded file")
    chunks = []
    offset = 0
    while offset <= maximum:
        common.check_deadline(deadline, "private FD read")
        chunk = os.pread(descriptor, min(1024 * 1024, maximum + 1 - offset), offset)
        if not chunk:
            break
        chunks.append(chunk)
        offset += len(chunk)
    payload = b"".join(chunks)
    common.check_deadline(deadline, "private FD read")
    if len(payload) > maximum or len(payload) != info.st_size:
        raise common.RuntimeErrorClosed("private descriptor changed or exceeded cap")
    after = os.fstat(descriptor)
    if (
        after.st_dev != info.st_dev
        or after.st_ino != info.st_ino
        or after.st_size != info.st_size
        or after.st_mtime_ns != info.st_mtime_ns
    ):
        raise common.RuntimeErrorClosed("private descriptor changed during read")
    return payload

def _write_staged(path, payload, deadline=None):
    common.check_deadline(deadline, "private staging")
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
    try:
        view = memoryview(payload)
        written = 0
        while written < len(view):
            common.check_deadline(deadline, "private staging")
            written += os.write(descriptor, view[written:])
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    os.chmod(path, 0o444)
    common.check_deadline(deadline, "private staging")

def _worker_command(direction, forms, deadline=None):
    common.check_deadline(deadline, "private worker preparation")
    with open(common.PRIVATE_WORKER, "rb") as handle:
        source = handle.read(256 * common.KIB + 1)
    common.check_deadline(deadline, "private worker preparation")
    if len(source) > 256 * common.KIB:
        raise common.RuntimeErrorClosed("trusted private worker source is oversized")
    source_text = source.decode("utf-8")
    forms_json = common.canonical_json(forms).encode("utf-8")
    forms_b64 = base64.b64encode(forms_json).decode("ascii")
    return "python -c %s %s %s" % (
        shlex.quote(source_text),
        "true" if direction else "false",
        shlex.quote(forms_b64),
    )

def _decode_and_sanitize(raw, expected_direction):
    try:
        value = common.strict_json_loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        raise common.RuntimeErrorClosed("private worker returned invalid JSON")
    required = {"schema", "classification", "native_score", "higher_is_better"}
    if not isinstance(value, dict) or set(value) != required:
        raise common.RuntimeErrorClosed("private result fields mismatch")
    if value.get("schema") != RESULT_SCHEMA:
        raise common.RuntimeErrorClosed("private result schema mismatch")
    classification = value.get("classification")
    if classification not in ("graded", "invalid_submission", "infrastructure_fault"):
        raise common.RuntimeErrorClosed("private classification invalid")
    direction = value.get("higher_is_better")
    if type(direction) is not bool or direction != expected_direction:
        raise common.RuntimeErrorClosed("private direction drift")
    score_value = value.get("native_score")
    score = None
    if classification == "graded":
        if isinstance(score_value, bool) or not isinstance(score_value, (int, float)):
            raise common.RuntimeErrorClosed("private score type invalid")
        score = float(score_value)
        if not math.isfinite(score):
            raise common.RuntimeErrorClosed("private score non-finite")
    elif score_value is not None:
        raise common.RuntimeErrorClosed("ungraded result carried score")
    return {
        "schema": RESULT_SCHEMA,
        "classification": classification,
        "native_score": score,
        "higher_is_better": direction,
    }

def infrastructure_result(direction=False):
    return {
        "schema": RESULT_SCHEMA,
        "classification": "infrastructure_fault",
        "native_score": None,
        "higher_is_better": bool(direction),
    }

def _validate_private_stage(stage_root):
    run_root = os.path.realpath(common.RUN_ROOT)
    real = os.path.realpath(stage_root)
    name = os.path.basename(stage_root)
    prefix = "private-stage-"
    suffix = name[len(prefix):] if name.startswith(prefix) else ""
    if (
        not name.startswith("private-stage-")
        or len(suffix) != 32
        or any(character not in "0123456789abcdef" for character in suffix)
        or os.path.commonpath((real, run_root)) != run_root
        or real == run_root
    ):
        raise common.RuntimeErrorClosed("private stage cleanup target is unsafe")
    return real

def _cleanup_private_stage(stage_root, workspace, deadline=None):
    common.check_deadline(deadline, "private stage cleanup")
    stage_root = _validate_private_stage(stage_root)
    mount = common.exact_mount(workspace, required=False, deadline=deadline)
    if mount is not None:
        common.run_checked(
            ["/usr/bin/umount", workspace],
            deadline=deadline,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    if common.exact_mount(
        workspace, required=False, deadline=deadline
    ) is not None:
        raise common.RuntimeErrorClosed("private stage mount remains")
    common._remove_tree_strict(stage_root, deadline=deadline)
    if os.path.lexists(stage_root):
        raise common.RuntimeErrorClosed("private stage directory remains")

def _start_stage_watchdog(stage_root, workspace, deadline=None):
    common.check_deadline(deadline, "private watchdog setup")
    try:
        read_fd, write_fd = os.pipe()
    except OSError as exc:
        raise common.RuntimeErrorClosed("cannot create private watchdog pipe") from exc
    try:
        pid = os.fork()
    except OSError as exc:
        os.close(read_fd)
        os.close(write_fd)
        raise common.RuntimeErrorClosed("cannot fork private watchdog") from exc
    if pid == 0:
        os.close(write_fd)
        try:
            token = os.read(read_fd, 1)
        except OSError:
            token = b""
        os.close(read_fd)
        if token != b"N":
            for _ in range(3):
                try:
                    _cleanup_private_stage(
                        stage_root,
                        workspace,
                        deadline=time.monotonic() + 2.0,
                    )
                    break
                except BaseException:
                    time.sleep(0.05)
        os._exit(0)
    os.close(read_fd)
    return pid, write_fd

def _finish_stage_watchdog(pid, write_fd, cleanup_complete, deadline=None):
    try:
        if cleanup_complete:
            os.write(write_fd, b"N")
    except OSError:
        pass
    os.close(write_fd)
    try:
        while True:
            waited, _status = os.waitpid(pid, os.WNOHANG)
            if waited == pid:
                break
            common.check_deadline(deadline, "private watchdog cleanup")
            time.sleep(0.01)
    except ChildProcessError:
        pass

def grade(value):
    started = time.monotonic()
    common.require_runtime_admission(
        ARTIFACT_LOCK_SHA256, operation="private.grade", request=value
    )
    descriptors = _validate_request(value)
    deadline = started + value["timeout_ms"] / 1000.0
    maximum = common.PRIVATE_LIMITS["input_bytes"]
    common.check_deadline(deadline, "private runtime setup")
    common.ensure_runtime_directories(deadline=deadline)
    common.check_deadline(deadline, "private runtime setup")
    stage_root = os.path.join(common.RUN_ROOT, "private-stage-" + uuid.uuid4().hex)
    workspace = os.path.join(stage_root, "workspace")
    watchdog_pid, watchdog_write = _start_stage_watchdog(
        stage_root, workspace, deadline=deadline
    )
    mounted = False
    cleanup_complete = False
    cleanup_error = None
    try:
        metric = _read_regular_fd(descriptors[0], maximum, deadline)
        answer = _read_regular_fd(descriptors[1], maximum, deadline)
        submission = _read_regular_fd(descriptors[2], maximum, deadline)
        common.check_deadline(deadline, "private digest verification")
        if common.bytes_sha256(metric) != value["metric_sha256"]:
            raise common.RuntimeErrorClosed("metric digest mismatch")
        if common.bytes_sha256(answer) != value["answer_sha256"]:
            raise common.RuntimeErrorClosed("answer digest mismatch")
        if common.bytes_sha256(submission) != value["submission_sha256"]:
            raise common.RuntimeErrorClosed("submission digest mismatch")
        os.makedirs(workspace, 0o700)
        common.check_deadline(deadline, "private namespace setup")

        common._unshare_mount_namespace(deadline=deadline)
        common.run_checked(
            [
                "/usr/bin/mount",
                "-t",
                "tmpfs",
                "-o",
                "size=%d,nr_inodes=64,noexec,nosuid,nodev,mode=0700"
                % (3 * maximum + 4 * common.MIB),
                "openmle-private-stage",
                workspace,
            ],
            deadline=deadline,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        mounted = True
        _write_staged(os.path.join(workspace, "metric.py"), metric, deadline)
        _write_staged(os.path.join(workspace, "answer.csv"), answer, deadline)
        _write_staged(os.path.join(workspace, "submission.csv"), submission, deadline)
        common.check_deadline(deadline, "private staging")
        os.chmod(workspace, 0o555)
        command = _worker_command(
            value["higher_is_better"], value["validator_success_forms"], deadline
        )
        worker_timeout_ms = int((deadline - time.monotonic()) * 1000.0) - COMPLETION_GRACE_MS
        if worker_timeout_ms <= 0:
            raise common.RuntimeErrorClosed("private request deadline exhausted before worker")
        run_id = uuid.uuid4().hex[:16]
        result = common.run_sandbox(
            workspace=workspace,
            command=command,
            timeout_ms=worker_timeout_ms,
            cpu_vcpus=common.PRIVATE_LIMITS["cpu_vcpus"],
            memory_bytes=common.PRIVATE_LIMITS["memory_bytes"],
            max_processes=common.PRIVATE_LIMITS["max_processes"],
            managed_ms=min(common.PRIVATE_LIMITS["wall_ms"], worker_timeout_ms),
            max_open_files=64,
            max_file_bytes=common.PRIVATE_LIMITS["input_bytes"],
            output_cap=64 * common.KIB,
            run_name="private-" + run_id,
            deadline=deadline,
        )
        if (
            result["infrastructure_fault"]
            or result["failure_class"] is not None
            or result["exit_code"] != 0
            or result["stderr"]
            or len(result["stdout"]) > 64 * common.KIB
        ):
            _write_probe_fault("sandbox_result", request=value, sandbox=result)
            return infrastructure_result(value["higher_is_better"])
        common.check_deadline(deadline, "private result decoding")
        return _decode_and_sanitize(result["stdout"], value["higher_is_better"])
    finally:

        cleanup_deadline = time.monotonic() + STAGE_CLEANUP_TIMEOUT_MS / 1000.0
        try:
            _cleanup_private_stage(
                stage_root, workspace, deadline=cleanup_deadline
            )
            cleanup_complete = True
        except BaseException as exc:
            cleanup_error = exc
        _finish_stage_watchdog(
            watchdog_pid,
            watchdog_write,
            cleanup_complete,
            deadline=cleanup_deadline,
        )
        if cleanup_error is not None:
            raise cleanup_error

def main(argv):
    if len(argv) != 2 or argv[1] not in ("metadata", "grade"):
        print("usage: private_runner.py {metadata|grade}", file=sys.stderr)
        return 2
    if argv[1] == "metadata":
        print(common.canonical_json(metadata()))
        return 0
    direction = False
    request = None
    try:
        request = common.read_stdin_json()
        if isinstance(request, dict) and type(request.get("higher_is_better")) is bool:
            direction = request["higher_is_better"]
        result = grade(request)
    except BaseException as exc:
        _write_probe_fault(
            "runner_exception",
            request=request if isinstance(request, dict) else None,
            exception=exc,
        )
        result = infrastructure_result(direction)
    print(common.canonical_json(result))
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
