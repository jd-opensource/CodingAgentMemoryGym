#!/usr/bin/env python3
from __future__ import print_function

import base64
import concurrent.futures
import errno
import fcntl
import hashlib
import json
import os
import shutil
import shlex
import stat
import subprocess
import sys
import threading
import time
import uuid

sys.dont_write_bytecode = True

import runtime_common as common

SOURCE = os.path.dirname(os.path.realpath(__file__))
PUBLIC_RUNNER = os.path.join(SOURCE, "public_runner.py")
PRIVATE_RUNNER = os.path.join(SOURCE, "private_runner.py")
EVIDENCE = os.path.join(common.SCRATCH, "evidence")
INPUT_ROOT = os.path.join(common.SCRATCH, "probe-inputs")
PROBE_FAULT_ROOT = os.path.join(common.SCRATCH, "probe-private-faults")
PUBLIC_FAULT_ROOT = os.path.join(common.SCRATCH, "public-faults")
PUBLIC_CONCURRENCY_WORKERS = 8
PUBLIC_CONCURRENCY_WAVES = 64
PUBLIC_RUNNER_PROCESS_GRACE_SECONDS = 34.0
G64_ROOT = (
    os.environ.get("CAMG_AUTORESEARCH_PROBE_DATA", "/var/lib/camg/autoresearch/probe")
)
G64_TASK = "air-passengers-forecast-dataset@1"
BASELINE = os.path.join(SOURCE, "tests", "generic_openmle_baseline.py")
BASELINE_SHA256 = "bb5b8773978a71712c3e825a91c45487bcd47f53c4d391074a77574b70b0ac60"

def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()

def write_json(path, value):
    temporary = path + ".tmp-%d" % os.getpid()
    with open(temporary, "w") as handle:
        handle.write(common.canonical_json(value) + "\n")
    os.replace(temporary, path)

def write_evidence(filename, value, session=None):
    bound = common.bind_evidence_context(value, session)
    write_json(os.path.join(EVIDENCE, filename), bound)
    return bound

def _reset_owned_probe_directory(path):
    expected = os.path.abspath(path)
    scratch = os.path.abspath(common.SCRATCH)
    try:
        inside = os.path.commonpath((expected, scratch)) == scratch
    except ValueError:
        inside = False
    if not inside or expected == scratch or os.path.islink(path):
        raise RuntimeError("unsafe probe reset target")
    if os.path.lexists(path):
        if not os.path.isdir(path):
            raise RuntimeError("probe reset target is not a directory")
        shutil.rmtree(path)
    os.makedirs(path, mode=0o700)

def start_probe_session():

    invalidate_admission()
    _reset_owned_probe_directory(EVIDENCE)
    _reset_owned_probe_directory(INPUT_ROOT)
    _reset_owned_probe_directory(PROBE_FAULT_ROOT)
    _reset_owned_probe_directory(PUBLIC_FAULT_ROOT)
    session = {
        "schema": "openmle_fast_probe_session_v1",
        "probe_session_id": uuid.uuid4().hex,
        "boot_id": common.boot_id(),
        "kernel_release": os.uname()[2],
        "artifact_identity": common.probe_artifact_identity(),
    }
    write_json(os.path.join(EVIDENCE, "probe-session.json"), session)
    if common.load_probe_session() != session:
        raise RuntimeError("fresh probe session did not validate")
    return session

def _create_probe_capability(operation, request):
    if operation not in common.PROBE_CAPABILITY_OPERATIONS:
        raise RuntimeError("unsupported probe capability operation")
    session = common.load_probe_session()
    rootfs = common.verified_rootfs_identity()
    if session is None or rootfs.get("valid") is not True:
        raise RuntimeError("probe capability prerequisites are incomplete")
    issued = common.monotonic_ns()
    capability = {
        "schema": common.PROBE_CAPABILITY_SCHEMA,
        "capability_id": uuid.uuid4().hex,
        "probe_session_id": session["probe_session_id"],
        "boot_id": common.boot_id(),
        "kernel_release": os.uname()[2],
        "artifact_identity": common.probe_artifact_identity(),
        "artifact_lock_sha256": common.sha256_file(common.ARTIFACT_LOCK),
        "rootfs_identity_sha256": common.canonical_sha256(rootfs),
        "operation": operation,
        "request_sha256": common.canonical_sha256(request),
        "parent_pid": os.getpid(),
        "parent_start_ticks": common._process_start_ticks(os.getpid()),
        "issued_monotonic_ns": issued,
        "expires_monotonic_ns": issued + common.PROBE_CAPABILITY_MAX_NS,
    }
    if capability["parent_start_ticks"] is None:
        raise RuntimeError("cannot bind probe capability to parent process")
    flags = getattr(os, "MFD_CLOEXEC", 0x0001) | getattr(
        os, "MFD_ALLOW_SEALING", 0x0002
    )
    descriptor = common.create_memfd("openmle-probe-capability", flags)
    try:
        payload = (common.canonical_json(capability) + "\n").encode("utf-8")
        offset = 0
        while offset < len(payload):
            offset += os.write(descriptor, payload[offset:])
        os.fchmod(descriptor, 0o400)
        seals = (
            getattr(fcntl, "F_SEAL_SEAL", 0x0001)
            | getattr(fcntl, "F_SEAL_SHRINK", 0x0002)
            | getattr(fcntl, "F_SEAL_GROW", 0x0004)
            | getattr(fcntl, "F_SEAL_WRITE", 0x0008)
        )
        fcntl.fcntl(descriptor, getattr(fcntl, "F_ADD_SEALS", 1033), seals)
        return descriptor
    except BaseException:
        os.close(descriptor)
        raise

def call_json(
    argv,
    request=None,
    pass_fds=(),
    environment=None,
    timeout=30,
    probe_operation=None,
):
    payload = None if request is None else common.canonical_json(request).encode("utf-8")
    auth_fd = None
    child_environment = environment
    child_fds = tuple(pass_fds)
    if probe_operation is not None:
        if request is None:
            raise RuntimeError("probe operation lacks a bound request")
        child_environment = dict(os.environ if environment is None else environment)
        if common.PROBE_CAPABILITY_ENV in child_environment:
            raise RuntimeError("probe capability environment was prepopulated")
        auth_fd = _create_probe_capability(probe_operation, request)
        child_environment[common.PROBE_CAPABILITY_ENV] = str(auth_fd)
        child_fds += (auth_fd,)
    try:
        result = subprocess.run(
            argv,
            input=payload,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=timeout,
            pass_fds=child_fds,
            env=child_environment,
        )
    finally:
        if auth_fd is not None:
            os.close(auth_fd)
    if result.returncode != 0 or result.stderr or len(result.stdout) > 9 * common.MIB:
        raise RuntimeError("runner process/protocol failure")
    return common.strict_json_loads(result.stdout.decode("utf-8"))

def _popen_probe(argv, request, probe_operation):
    if request is None or probe_operation not in common.PROBE_CAPABILITY_OPERATIONS:
        raise RuntimeError("asynchronous probe lacks an exact operation request")
    environment = dict(os.environ)
    if common.PROBE_CAPABILITY_ENV in environment:
        raise RuntimeError("probe capability environment was prepopulated")
    auth_fd = _create_probe_capability(probe_operation, request)
    environment[common.PROBE_CAPABILITY_ENV] = str(auth_fd)
    try:
        return subprocess.Popen(
            argv,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            pass_fds=(auth_fd,),
            env=environment,
        )
    finally:
        os.close(auth_fd)

def public_metadata():
    return call_json([PUBLIC_RUNNER, "metadata"], timeout=5)

def private_metadata():
    return call_json([PRIVATE_RUNNER, "metadata"], timeout=5)

def mount_workspace(label, size_bytes=64 * common.MIB, inodes=4096):
    common.ensure_runtime_directories()
    path = os.path.join(common.PUBLIC_WORKSPACE_ROOT, label + "-" + uuid.uuid4().hex)
    os.makedirs(path, 0o755)
    subprocess.check_call(
        [
            "/usr/bin/mount",
            "-t",
            "tmpfs",
            "-o",
            "size=%d,nr_inodes=%d,noexec,nosuid,nodev,mode=0777"
            % (size_bytes, inodes),
            "openmle-integration-" + label,
            path,
        ]
    )
    return path

def force_workspace_cleanup(path):
    if path and os.path.isdir(path):
        try:
            if common.exact_mount(path, required=False) is not None:
                subprocess.call(
                    ["/usr/bin/umount", path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
        except (OSError, common.RuntimeErrorClosed):
            pass
        shutil.rmtree(path, ignore_errors=True)

def execute_request(
    workspace,
    command,
    timeout_ms=5000,
    managed_runtime_budget_ms=15000,
    environment=None,
):
    request = {
        "schema": "openmle_fast_runner_request_v1",
        "workspace": workspace,
        "command": command,
        "timeout_ms": timeout_ms,
        "managed_runtime_budget_ms": managed_runtime_budget_ms,
    }
    return call_json(
        [PUBLIC_RUNNER, "execute"],
        request,
        environment=environment,
        timeout=timeout_ms / 1000.0 + PUBLIC_RUNNER_PROCESS_GRACE_SECONDS,
        probe_operation="public.execute",
    )

def lifecycle(workspace, operation, timeout_ms=5000):
    return call_json(
        [PUBLIC_RUNNER, operation],
        {
            "schema": "openmle_fast_runner_lifecycle_request_v1",
            "workspace": workspace,
            "operation": operation,
            "timeout_ms": timeout_ms,
        },
        timeout=timeout_ms / 1000.0 + 5,
        probe_operation="public." + operation,
    )

def complete_lifecycle(workspace):
    frozen = lifecycle(workspace, "freeze")
    after_freeze = execute_request(workspace, "true", 1000)
    torn = lifecycle(workspace, "teardown")
    repeated = lifecycle(workspace, "teardown")
    return {
        "freeze": frozen,
        "execute_after_freeze": after_freeze,
        "teardown": torn,
        "teardown_repeated": repeated,
    }

def public_probe(label, command, timeout_ms=5000, prepare=None):
    workspace = mount_workspace(label)
    try:
        if prepare is not None:
            prepare(workspace)
        receipt = execute_request(workspace, command, timeout_ms)
        lifecycle_receipts = complete_lifecycle(workspace)
        return {
            "label": label,
            "receipt": receipt,
            "lifecycle": lifecycle_receipts,
            "mount_absent": common.exact_mount(workspace, required=False) is None,
            "residue": common.residue_snapshot(),
        }
    finally:
        force_workspace_cleanup(workspace)

def lifecycle_ok(probe):
    lifecycle_receipts = probe["lifecycle"]
    return (
        lifecycle_receipts["freeze"].get("success") is True
        and lifecycle_receipts["freeze"].get("workspace_read_only") is True
        and lifecycle_receipts["teardown"].get("success") is True
        and lifecycle_receipts["teardown_repeated"].get("success") is True
        and lifecycle_receipts["execute_after_freeze"].get("infrastructure_fault") is True
        and probe["mount_absent"]
        and common.residue_is_zero(probe["residue"])
    )

def run_public_concurrency_stress():

    concurrency_waves = []
    concurrency_failed = False
    for wave in range(PUBLIC_CONCURRENCY_WAVES):
        workspaces = []
        wave_started = time.monotonic()
        try:
            for index in range(PUBLIC_CONCURRENCY_WORKERS):
                workspaces.append(
                    mount_workspace("concurrent-%02d-%d" % (wave, index))
                )
            barrier = threading.Barrier(PUBLIC_CONCURRENCY_WORKERS)

            def execute_concurrent(index):
                barrier.wait(timeout=10)
                started = time.monotonic()
                receipt = execute_request(workspaces[index], "true", 2000)
                return {
                    "index": index,
                    "wall_seconds": max(0.0, time.monotonic() - started),
                    "receipt": receipt,
                }

            with concurrent.futures.ThreadPoolExecutor(
                max_workers=PUBLIC_CONCURRENCY_WORKERS
            ) as pool:
                executions = list(
                    pool.map(execute_concurrent, range(PUBLIC_CONCURRENCY_WORKERS))
                )
                lifecycles = list(pool.map(complete_lifecycle, workspaces))

            mount_absent = [
                common.exact_mount(workspace, required=False) is None
                for workspace in workspaces
            ]
            residue = common.residue_snapshot()
            failures = []
            receipt_hashes = []
            lifecycle_hashes = []
            for index, execution in enumerate(executions):
                receipt = execution["receipt"]
                lifecycle_receipts = lifecycles[index]
                item = {
                    "label": "concurrent-%02d-%d" % (wave, index),
                    "receipt": receipt,
                    "lifecycle": lifecycle_receipts,
                    "mount_absent": mount_absent[index],
                    "residue": residue,
                }
                item_ok = (
                    receipt.get("exit_code") == 0
                    and receipt.get("failure_class") is None
                    and receipt.get("infrastructure_fault") is False
                    and lifecycle_ok(item)
                )
                receipt_hashes.append(common.canonical_sha256(receipt))
                lifecycle_hashes.append(common.canonical_sha256(lifecycle_receipts))
                if not item_ok:
                    failures.append(item)
            wave_ok = not failures and common.residue_is_zero(residue)
            wave_summary = {
                "wave": wave,
                "ok": wave_ok,
                "execution_count": len(executions),
                "wall_seconds": max(0.0, time.monotonic() - wave_started),
                "execution_wall_seconds": [
                    item["wall_seconds"] for item in executions
                ],
                "receipt_sha256": receipt_hashes,
                "lifecycle_sha256": lifecycle_hashes,
                "failures": failures,
                "residue": residue,
            }
            concurrency_waves.append(wave_summary)
            if not wave_ok:
                concurrency_failed = True
                break
        finally:
            for workspace in workspaces:
                force_workspace_cleanup(workspace)

    concurrency_evidence = {
        "workers": PUBLIC_CONCURRENCY_WORKERS,
        "requested_waves": PUBLIC_CONCURRENCY_WAVES,
        "completed_waves": len(concurrency_waves),
        "execution_count": sum(
            item["execution_count"] for item in concurrency_waves
        ),
        "ok": (
            not concurrency_failed
            and len(concurrency_waves) == PUBLIC_CONCURRENCY_WAVES
            and all(item["ok"] for item in concurrency_waves)
        ),
        "waves": concurrency_waves,
        "final_residue": common.residue_snapshot(),
    }
    concurrency_evidence["ok"] = (
        concurrency_evidence["ok"]
        and common.residue_is_zero(concurrency_evidence["final_residue"])
    )
    return concurrency_evidence

def run_public_probes():
    probes = []
    basic = public_probe("lifecycle", "python -c 'print(12345)'", 3000)
    probes.append(
        {
            "name": "metadata_execute_freeze_teardown_idempotent",
            "ok": (
                basic["receipt"].get("exit_code") == 0
                and basic["receipt"].get("execution_attempt_delta") == 1
                and lifecycle_ok(basic)
            ),
            "evidence": basic,
        }
    )

    identity_source = (
        "import json,os; "
        "p=[x for x in os.listdir('/proc') if x.isdigit()]; "
        "r=False; "
        "\ntry:\n open('/proc/1/cmdline','rb').read(1); r=True\nexcept OSError: pass\n"
        "blocked=[os.path.exists(x) for x in ['/root/.ssh','/data/private','/grader',"
        "'/tmp/camg-autoresearch/private-canary',"
        "'/tmp/camg-autoresearch/public-faults']]; "
        "print(json.dumps({'pids':len(p),'blocked':blocked,'sys':os.listdir('/sys'),"
        "'proc1_readable':r,'env':sorted(os.environ),'uid':os.getuid(),'gid':os.getgid()}))"
    )
    identity = public_probe(
        "identity", "python -c %s" % shlex.quote(identity_source), 3000
    )
    try:
        visible = json.loads(base64.b64decode(identity["receipt"]["stdout_b64"]))
    except (ValueError, KeyError):
        visible = {}
    probes.append(
        {
            "name": "environment_proc_host_private_isolation",
            "ok": (
                identity["receipt"].get("exit_code") == 0
                and visible.get("uid") == 1000
                and visible.get("gid") == 1000
                and visible.get("pids", 999) <= 4
                and visible.get("proc1_readable") is False
                and not any(visible.get("blocked", [True]))
                and visible.get("sys") == []
                and lifecycle_ok(identity)
            ),
            "evidence": identity,
        }
    )

    listing = public_probe("ls-long", "ls -la", 3000)
    probes.append(
        {
            "name": "basic_long_listing_with_nss_fallback",
            "ok": (
                listing["receipt"].get("exit_code") == 0
                and listing["receipt"].get("failure_class") is None
                and lifecycle_ok(listing)
            ),
            "evidence": listing,
        }
    )

    network_source = (
        "import errno,socket\n"
        "try:\n"
        " socket.socket(socket.AF_INET,socket.SOCK_STREAM)\n"
        "except OSError as exc:\n"
        " print('network_socket_errno=%d' % exc.errno)\n"
        " raise SystemExit(0 if exc.errno in (errno.EPERM,errno.EACCES) else 2)\n"
        "raise SystemExit(3)\n"
    )
    network = public_probe(
        "network", "python -c %s" % shlex.quote(network_source), 3000
    )
    try:
        network_stdout = base64.b64decode(
            network["receipt"]["stdout_b64"]
        ).decode("utf-8").strip()
    except (KeyError, TypeError, ValueError, UnicodeDecodeError):
        network_stdout = ""
    probes.append(
        {
            "name": "network_socket_denied_without_sigsys",
            "ok": (
                network["receipt"].get("exit_code") == 0
                and network["receipt"].get("failure_class") is None
                and network_stdout in (
                    "network_socket_errno=%d" % getattr(errno, "EPERM", 1),
                    "network_socket_errno=%d" % getattr(errno, "EACCES", 13),
                )
                and lifecycle_ok(network)
            ),
            "evidence": network,
        }
    )
    background = public_probe(
        "background", "python -c 'import time; time.sleep(30)' &", 3000
    )
    probes.append(
        {
            "name": "background_descendant_reaped",
            "ok": background["receipt"].get("failure_class") == "background_process"
            and lifecycle_ok(background),
            "evidence": background,
        }
    )
    short_success = public_probe("short-success", "true", 100)
    probes.append(
        {
            "name": "short_timeout_excludes_host_setup",
            "ok": short_success["receipt"].get("infrastructure_fault") is False
            and short_success["receipt"].get("failure_class") in (None, "wall_timeout")
            and (
                short_success["receipt"].get("failure_class") is None
                or short_success["receipt"].get("timed_out") is True
            )
            and lifecycle_ok(short_success),
            "evidence": short_success,
        }
    )
    short_timeout = public_probe(
        "short-timeout", "python -c 'import time; time.sleep(1)'", 100
    )
    probes.append(
        {
            "name": "short_timeout_is_policy_wall_timeout",
            "ok": short_timeout["receipt"].get("failure_class") == "wall_timeout"
            and short_timeout["receipt"].get("timed_out") is True
            and short_timeout["receipt"].get("infrastructure_fault") is False
            and lifecycle_ok(short_timeout),
            "evidence": short_timeout,
        }
    )

    concurrency_evidence = run_public_concurrency_stress()
    probes.append(
        {
            "name": "concurrent_public_setup_and_short_execution",
            "ok": concurrency_evidence["ok"],
            "evidence": concurrency_evidence,
        }
    )

    timeout = public_probe(
        "timeout", "python -c 'import time; time.sleep(30)'", 1500
    )
    probes.append(
        {
            "name": "hard_wall_timeout_reaped",
            "ok": timeout["receipt"].get("failure_class") == "wall_timeout"
            and timeout["receipt"].get("timed_out") is True
            and lifecycle_ok(timeout),
            "evidence": timeout,
        }
    )

    real_python_substitution = public_probe(
        "fd198-substitution",
        "exec 198</bin/true; python -c 'print(12345)'",
        3000,
    )
    probes.append(
        {
            "name": "shell_high_fd198_substitution_attempt_rejected",
            "ok": real_python_substitution["receipt"].get(
                "execution_attempt_delta"
            )
            == 0
            and real_python_substitution["receipt"].get(
                "execution_completed_delta"
            )
            == 0
            and real_python_substitution["receipt"].get("exit_code") != 0
            and lifecycle_ok(real_python_substitution),
            "evidence": real_python_substitution,
        }
    )
    fit_fd_substitution = public_probe(
        "fd199-substitution",
        "exec 199>/dev/null; python -c 'print(12345)'",
        3000,
    )
    probes.append(
        {
            "name": "shell_high_fd199_substitution_attempt_rejected",
            "ok": fit_fd_substitution["receipt"].get("execution_attempt_delta")
            == 0
            and fit_fd_substitution["receipt"].get("execution_completed_delta")
            == 0
            and fit_fd_substitution["receipt"].get("exit_code") != 0
            and lifecycle_ok(fit_fd_substitution),
            "evidence": fit_fd_substitution,
        }
    )

    diagnostic_canary = "OPENMLE_PUBLIC_FAULT_COMMAND_MUST_NOT_APPEAR_7e24"
    diagnostic_command = "printf %s" % diagnostic_canary
    unsafe_request = {
        "schema": "openmle_fast_runner_request_v1",
        "workspace": "/tmp",
        "command": diagnostic_command,
        "timeout_ms": 1000,
        "managed_runtime_budget_ms": 15000,
    }
    unsafe = execute_request("/tmp", diagnostic_command, 1000)
    probes.append(
        {
            "name": "unsafe_nonowned_workspace_rejected",
            "ok": unsafe.get("infrastructure_fault") is True,
            "evidence": unsafe,
        }
    )
    diagnostic = None
    diagnostic_raw = b""
    expected_request_sha256 = common.canonical_sha256(unsafe_request)
    for name in sorted(os.listdir(PUBLIC_FAULT_ROOT), reverse=True):
        path = os.path.join(PUBLIC_FAULT_ROOT, name)
        try:
            info = os.lstat(path)
            if not stat.S_ISREG(info.st_mode):
                continue
            with open(path, "rb") as handle:
                raw = handle.read(4097)
            value = common.strict_json_loads(raw.decode("utf-8"))
        except (OSError, ValueError, UnicodeDecodeError):
            continue
        if value.get("request_sha256") == expected_request_sha256:
            diagnostic = value
            diagnostic_raw = raw
            diagnostic_mode = stat.S_IMODE(info.st_mode)
            break
    root_mode = stat.S_IMODE(os.lstat(PUBLIC_FAULT_ROOT).st_mode)
    probes.append(
        {
            "name": "root_only_bounded_public_fault_diagnostic",
            "ok": diagnostic is not None
            and root_mode == 0o700
            and diagnostic_mode == 0o600
            and len(diagnostic_raw) <= 4096
            and diagnostic_canary.encode("utf-8") not in diagnostic_raw
            and diagnostic.get("command_bytes") == len(diagnostic_command.encode("utf-8"))
            and diagnostic.get("command_sha256")
            == common.bytes_sha256(diagnostic_command.encode("utf-8"))
            and isinstance(diagnostic.get("phase"), str)
            and bool(diagnostic.get("phase"))
            and isinstance(diagnostic.get("exception_type"), str)
            and isinstance(diagnostic.get("exception_detail"), str)
            and isinstance(diagnostic.get("traceback_frames"), list)
            and bool(diagnostic.get("traceback_frames")),
            "evidence": {
                "directory_mode": root_mode,
                "record_mode": diagnostic_mode if diagnostic is not None else None,
                "record": diagnostic,
                "command_content_absent": diagnostic_canary.encode("utf-8")
                not in diagnostic_raw,
            },
        }
    )
    unsafe_freeze = lifecycle("/tmp", "freeze")
    probes.append(
        {
            "name": "unsafe_nonowned_freeze_rejected",
            "ok": unsafe_freeze.get("success") is False,
            "evidence": unsafe_freeze,
        }
    )

    patch_only_workspace = mount_workspace("patch-only")
    try:
        with open(os.path.join(patch_only_workspace, "solution.py"), "w") as handle:
            handle.write("print('patch-only workspace')\n")
        patch_only_freeze = lifecycle(patch_only_workspace, "freeze")
        patch_only_teardown = lifecycle(patch_only_workspace, "teardown")
        patch_only_teardown_repeated = lifecycle(patch_only_workspace, "teardown")
        patch_only_evidence = {
            "freeze": patch_only_freeze,
            "teardown": patch_only_teardown,
            "teardown_repeated": patch_only_teardown_repeated,
            "mount_absent": common.exact_mount(
                patch_only_workspace, required=False
            )
            is None,
            "residue": common.residue_snapshot(),
        }
        probes.append(
            {
                "name": "patch_only_freeze_adopted_and_torn_down",
                "ok": patch_only_freeze.get("success") is True
                and patch_only_freeze.get("workspace_read_only") is True
                and patch_only_teardown.get("success") is True
                and patch_only_teardown_repeated.get("success") is True
                and patch_only_evidence["mount_absent"]
                and common.residue_is_zero(patch_only_evidence["residue"]),
                "evidence": patch_only_evidence,
            }
        )
    finally:
        force_workspace_cleanup(patch_only_workspace)

    def symlink_prepare(workspace):
        os.symlink("/etc/passwd", os.path.join(workspace, "escape"))

    unsafe_workspace = mount_workspace("symlink")
    try:
        symlink_prepare(unsafe_workspace)
        symlink = execute_request(unsafe_workspace, "true", 1000)
        probes.append(
            {
                "name": "symlink_workspace_rejected",
                "ok": symlink.get("infrastructure_fault") is True,
                "evidence": symlink,
            }
        )
    finally:
        force_workspace_cleanup(unsafe_workspace)

    failures = [item["name"] for item in probes if not item["ok"]]
    summary = {
        "schema": "openmle_fast_public_integration_probe_summary_v1",
        "ok": not failures,
        "failures": failures,
        "probe_count": len(probes),
        "pass_count": len(probes) - len(failures),
        "probes": probes,
        "final_residue": common.residue_snapshot(),
    }
    summary["ok"] = summary["ok"] and common.residue_is_zero(summary["final_residue"])
    return write_evidence("public-probe-summary.json", summary)

def load_g64_records():
    public_path = os.path.join(G64_ROOT, "train.json")
    private_path = os.path.join(G64_ROOT, "grader.json")
    with open(public_path, "r") as handle:
        public = json.load(handle)
    with open(private_path, "r") as handle:
        private = json.load(handle)
    public_record = next(item for item in public["records"] if item["task_id"] == G64_TASK)
    private_record = next(item for item in private["records"] if item["task_id"] == G64_TASK)
    return public_path, private_path, public, private, public_record, private_record

def run_g64_public():
    public_path, _private_path, public, _private, record, private_record = load_g64_records()
    if sha256_file(BASELINE) != BASELINE_SHA256:
        raise RuntimeError("baseline digest drift")
    source_root = os.path.join(G64_ROOT, record["public_task_relpath"])
    workspace = mount_workspace("g64", size_bytes=64 * common.MIB)
    try:
        for expected in record["public_files"]:
            source = os.path.join(source_root, expected["path"])
            if sha256_file(source) != expected["sha256"]:
                raise RuntimeError("G64 public source hash drift")
            target = os.path.join(workspace, expected["path"])
            parent = os.path.dirname(target)
            if not os.path.isdir(parent):
                os.makedirs(parent, 0o755)
            shutil.copyfile(source, target)
            os.chmod(target, expected["mode"])
        solution = os.path.join(workspace, "solution.py")
        shutil.copyfile(BASELINE, solution)
        os.chmod(solution, 0o444)
        receipt = execute_request(workspace, "python solution.py", 15000)
        submission_path = os.path.join(workspace, "submission.csv")
        if not os.path.isfile(submission_path):
            lifecycle_receipts = complete_lifecycle(workspace)
            failure = {
                "schema": "openmle_fast_g64_public_execution_failure_v1",
                "task_id": G64_TASK,
                "receipt": receipt,
                "lifecycle": lifecycle_receipts,
                "residue": common.residue_snapshot(),
            }
            write_evidence("g64-public-execution-failure.json", failure)
            raise RuntimeError(
                "G64 baseline produced no submission; see bounded failure evidence"
            )
        with open(submission_path, "rb") as handle:
            submission = handle.read(common.PRIVATE_LIMITS["input_bytes"] + 1)
        lifecycle_receipts = complete_lifecycle(workspace)
        evidence = {
            "schema": "openmle_fast_g64_public_execution_probe_v2",
            "task_id": G64_TASK,
            "data_idx": record["data_idx"],
            "source_role": public["role"],
            "public_manifest_sha256": sha256_file(public_path),
            "public_tree_sha256": record["public_tree_sha256"],
            "baseline_sha256": BASELINE_SHA256,
            "submission_sha256": hashlib.sha256(submission).hexdigest(),
            "submission_bytes": len(submission),
            "receipt": receipt,
            "lifecycle": lifecycle_receipts,
            "ok": (
                receipt.get("exit_code") == 0
                and receipt.get("failure_class") is None
                and receipt.get("execution_attempt_delta") == 1
                and receipt.get("execution_completed_delta") == 1
                and lifecycle_receipts["freeze"].get("success") is True
                and lifecycle_receipts["teardown"].get("success") is True
                and lifecycle_receipts["teardown_repeated"].get("success") is True
            ),
        }
        evidence = write_evidence("g64-public-execution.json", evidence)
        return evidence, submission, record, private_record
    finally:
        force_workspace_cleanup(workspace)

def _controller_directories(controller):
    root = os.path.join("/sys/fs/cgroup", controller)
    return {
        name
        for name in os.listdir(root)
        if name.startswith("openmle-public-") and os.path.isdir(os.path.join(root, name))
    }

def run_live_cgroup_probe():
    controllers = {
        "cpu,cpuacct": ("cpu.cfs_period_us", "cpu.cfs_quota_us", "tasks"),
        "memory": (
            "memory.limit_in_bytes",
            "memory.memsw.limit_in_bytes",
            "memory.swappiness",
            "tasks",
        ),
        "pids": ("pids.max", "tasks"),
    }
    before = {name: _controller_directories(name) for name in controllers}
    workspace = mount_workspace("live-cgroup")
    process = None
    try:
        request = {
            "schema": "openmle_fast_runner_request_v1",
            "workspace": workspace,
            "command": "python -c 'import time; print(1,flush=True); time.sleep(3)'",
            "timeout_ms": 5000,
            "managed_runtime_budget_ms": 5000,
        }
        process = _popen_probe(
            [PUBLIC_RUNNER, "execute"],
            request,
            "public.execute",
        )
        process.stdin.write(common.canonical_json(request).encode("utf-8"))
        process.stdin.close()
        process.stdin = None
        sample = None
        deadline = time.monotonic() + 4
        while time.monotonic() < deadline:
            created = {
                name: sorted(_controller_directories(name) - before[name])
                for name in controllers
            }
            if all(len(items) == 1 for items in created.values()):
                sample = {}
                for name, files in controllers.items():
                    root = os.path.join("/sys/fs/cgroup", name, created[name][0])
                    sample[name] = {
                        filename: open(os.path.join(root, filename), "r").read().strip()
                        for filename in files
                    }
                if all(sample[name]["tasks"] for name in controllers):
                    break
            time.sleep(0.02)
        stdout, stderr = process.communicate(timeout=8)
        receipt = common.strict_json_loads(stdout.decode("utf-8"))
        lifecycle_receipts = complete_lifecycle(workspace)
        expected = sample is not None and (
            sample["cpu,cpuacct"]["cpu.cfs_period_us"] == "100000"
            and sample["cpu,cpuacct"]["cpu.cfs_quota_us"] == "200000"
            and sample["memory"]["memory.limit_in_bytes"] == str(4 * common.GIB)
            and sample["memory"]["memory.memsw.limit_in_bytes"] == str(4 * common.GIB)
            and sample["memory"]["memory.swappiness"] == "0"
            and sample["pids"]["pids.max"] == "64"
        )
        value = {
            "schema": "openmle_fast_cgroup_v1_live_integration_probe_v1",
            "ok": bool(
                expected
                and not stderr
                and receipt.get("exit_code") == 0
                and lifecycle_receipts["teardown"].get("success") is True
            ),
            "live_cgroups": sample,
            "receipt": receipt,
            "lifecycle": lifecycle_receipts,
        }
        return write_evidence("cgroup-v1-live.json", value)
    finally:
        if process is not None and process.poll() is None:
            process.kill()
            process.wait()
        force_workspace_cleanup(workspace)

def private_grade(metric, answer, submission, direction, forms, identities=None, env=None):
    common.ensure_runtime_directories()
    if not os.path.isdir(INPUT_ROOT):
        os.makedirs(INPUT_ROOT, 0o700)
    root = os.path.join(INPUT_ROOT, uuid.uuid4().hex)
    os.makedirs(root, 0o700)
    paths = []
    try:
        for name, payload in (
            ("metric.py", metric),
            ("answer.csv", answer),
            ("submission.csv", submission),
        ):
            path = os.path.join(root, name)
            descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o400)
            try:
                os.write(descriptor, payload)
                os.fsync(descriptor)
            finally:
                os.close(descriptor)
            paths.append(path)
        descriptors = tuple(os.open(path, os.O_RDONLY) for path in paths)
        identity = identities or {}
        request = {
            "schema": "openmle_fast_private_runner_request_v1",
            "task_id": identity.get("task_id", "synthetic-probe@1"),
            "grader_binding_sha256": identity.get("grader_binding_sha256", "1" * 64),
            "package_identity_sha256": identity.get("package_identity_sha256", "2" * 64),
            "metric_sha256": hashlib.sha256(metric).hexdigest(),
            "answer_sha256": hashlib.sha256(answer).hexdigest(),
            "submission_sha256": hashlib.sha256(submission).hexdigest(),
            "higher_is_better": direction,
            "validator_success_forms": list(forms),
            "metric_fd": descriptors[0],
            "answer_fd": descriptors[1],
            "submission_fd": descriptors[2],
            "timeout_ms": common.PRIVATE_LIMITS["wall_ms"],
        }
        try:
            return call_json(
                [PRIVATE_RUNNER, "grade"],
                request,
                pass_fds=descriptors,
                environment=env,
                timeout=8,
                probe_operation="private.grade",
            )
        finally:
            for descriptor in descriptors:
                os.close(descriptor)
    finally:
        common._remove_tree_strict(root)

def run_private_probes(g64_submission, public_record, private_record):
    private_root = os.path.join(G64_ROOT, "private-grader")
    metric = open(os.path.join(private_root, private_record["metric_relpath"]), "rb").read()
    answer = open(os.path.join(private_root, private_record["answer_relpath"]), "rb").read()
    if hashlib.sha256(metric).hexdigest() != private_record["metric_sha256"]:
        raise RuntimeError("native metric hash drift")
    if hashlib.sha256(answer).hexdigest() != private_record["answer_sha256"]:
        raise RuntimeError("native answer hash drift")
    validator = private_record["validator_contract"]
    forms = [validator["success_value"]] if validator["kind"] == "string" else []
    identities = {
        "task_id": G64_TASK,
        "grader_binding_sha256": private_record["grader_binding_sha256"],
        "package_identity_sha256": public_record["archive_sha256"],
    }
    probes = []
    valid = private_grade(
        metric,
        answer,
        g64_submission,
        private_record["higher_is_better"],
        forms,
        identities,
    )
    probes.append({"name": "native_metric_valid", "ok": valid["classification"] == "graded", "result": valid})
    invalid = private_grade(
        metric,
        answer,
        b"invalid_column\ninvalid\n",
        private_record["higher_is_better"],
        forms,
        identities,
    )
    probes.append(
        {
            "name": "native_metric_invalid_submission",
            "ok": invalid["classification"] == "invalid_submission",
            "result": invalid,
        }
    )

    timeout_metric = b'''\
import time
class Metric:
    higher_is_better=True
    def validate_submission(self,prediction,truth): time.sleep(10); return True
    def evaluate(self,y_true,y_pred): return 1.0
'''
    timed = private_grade(timeout_metric, b"y\n1\n", b"y\n1\n", True, [])
    probes.append(
        {
            "name": "timeout",
            "ok": timed["classification"] == "infrastructure_fault",
            "result": timed,
        }
    )

    network_metric = b'''\
class Metric:
    higher_is_better=True
    def validate_submission(self,prediction,truth):
        import socket; socket.socket(socket.AF_INET,socket.SOCK_STREAM); return True
    def evaluate(self,y_true,y_pred): return 1.0
'''
    network = private_grade(network_metric, b"y\n1\n", b"y\n1\n", True, [])
    probes.append(
        {
            "name": "malicious_metric_network_denied_without_sigsys",
            "ok": (
                network["classification"] == "invalid_submission"
                and network["native_score"] is None
            ),
            "result": network,
        }
    )

    isolation_metric = b'''\
class Metric:
    higher_is_better=True
    def validate_submission(self,prediction,truth):
        import os
        assert not os.path.exists('/tmp/camg-autoresearch/private-canary')
        assert not os.path.exists('/root/.ssh')
        assert os.listdir('/sys') == []
        assert len([x for x in os.listdir('/proc') if x.isdigit()]) <= 4
        try:
            open('/proc/1/cmdline','rb').read(1)
            raise AssertionError('proc pid 1 was readable')
        except OSError:
            pass
        assert 'OPENMLE_SERVICE_SECRET' not in os.environ
        return True
    def evaluate(self,y_true,y_pred): return 1.0
'''
    canary = os.path.join(common.SCRATCH, "private-canary")
    with open(canary, "w") as handle:
        handle.write("PRIVATE_CANARY_DO_NOT_LEAK\n")
    os.chmod(canary, 0o600)
    try:
        environment = dict(os.environ)
        environment["OPENMLE_SERVICE_SECRET"] = "PRIVATE_SERVICE_SECRET_DO_NOT_LEAK"
        isolated = private_grade(
            isolation_metric, b"y\n1\n", b"y\n1\n", True, [], env=environment
        )
    finally:
        os.unlink(canary)
    probes.append(
        {
            "name": "environment_proc_host_private_path",
            "ok": isolated["classification"] == "graded" and isolated["native_score"] == 1.0,
            "result": isolated,
        }
    )

    output_metric = b'''\
class Metric:
    higher_is_better=True
    def validate_submission(self,prediction,truth):
        import os; os.write(1,b'PRIVATE_ANSWER_LEAK'); return True
    def evaluate(self,y_true,y_pred): return 1.0
'''
    output = private_grade(output_metric, b"y\nSECRET\n", b"y\n1\n", True, [])
    encoded = common.canonical_json(output)
    probes.append(
        {
            "name": "output_sanitization",
            "ok": output["classification"] == "infrastructure_fault"
            and "PRIVATE_ANSWER_LEAK" not in encoded
            and "SECRET" not in encoded,
            "result": output,
        }
    )

    fresh_metric = b'''\
class Metric:
    higher_is_better=True
    def validate_submission(self,prediction,truth):
        import os
        assert not os.path.exists('/tmp/metric-state')
        open('/tmp/metric-state','w').write('one')
        return True
    def evaluate(self,y_true,y_pred): return 1.0
'''
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        fresh = list(
            pool.map(
                lambda _index: private_grade(
                    fresh_metric, b"y\n1\n", b"y\n1\n", True, []
                ),
                range(4),
            )
        )
    probes.append(
        {
            "name": "concurrency_safe_fresh_worker",
            "ok": all(item["classification"] == "graded" for item in fresh),
            "result": fresh,
        }
    )

    residue = common.residue_snapshot()
    failures = [item["name"] for item in probes if not item["ok"]]
    summary = {
        "schema": "openmle_fast_private_integration_probe_summary_v1",
        "ok": not failures and common.residue_is_zero(residue),
        "failures": failures,
        "probe_count": len(probes),
        "pass_count": len(probes) - len(failures),
        "probes": probes,
        "final_residue": residue,
    }
    return write_evidence("private-probe-summary.json", summary)

def cleanup_receipt():
    residue = common.residue_snapshot()
    marker_present = os.path.lexists("/tmp/camg-autoresearch/verification.lock")
    value = {
        "schema": "openmle_fast_integration_cleanup_receipt_v1",
        "ok": common.residue_is_zero(residue)
        and not marker_present,
        "residue": residue,
        "verification_lock_present": marker_present,
    }
    return write_evidence("cleanup-receipt.json", value)

def write_rootfs_evidence():
    identity = common.rootfs_identity(deadline=time.monotonic() + 900.0)
    value = {
        "schema": "openmle_fast_rootfs_admission_evidence_v2",
        "ok": identity["valid"],
        "identity": identity,
    }
    return write_evidence("rootfs-evidence.json", value)

def invalidate_admission():
    try:
        os.unlink(common.ADMISSION_STAMP)
    except FileNotFoundError:
        pass

def _load_admission_evidence():
    session = common.load_probe_session()
    if session is None:
        raise RuntimeError("probe session is missing or stale")
    values = {}
    for name, filename in common.ADMISSION_EVIDENCE_FILES.items():
        with open(os.path.join(EVIDENCE, filename), "r") as handle:
            values[name] = common.strict_json_loads(handle.read())
    if any(
        not common.evidence_context_matches(value, session)
        for value in values.values()
    ):
        raise RuntimeError("admission evidence crossed a probe session")
    return session, values

def activate_admission():
    session, evidence = _load_admission_evidence()
    public_summary = evidence["public_probe_summary"]
    private_summary = evidence["private_probe_summary"]
    cleanup = evidence["cleanup_receipt"]
    live = evidence["cgroup_v1_live"]
    g64 = evidence["g64_public_execution"]
    lock = evidence["installation_lock_cleanup"]
    rootfs = evidence["rootfs_evidence"]
    if not (
        public_summary["ok"]
        and private_summary["ok"]
        and cleanup["ok"]
        and live["ok"]
        and g64["ok"]
        and lock.get("ok") is True
        and lock.get("lock_state") == "released"
        and lock.get("marker_present") is False
        and rootfs.get("ok") is True
    ):
        raise RuntimeError("admission evidence is incomplete")
    preflight = public_metadata()["active_verification"]
    if not preflight["all_checks_pass"]:
        raise RuntimeError("active runtime preflight failed")
    identity = common.admission_runtime_identity(preflight["rootfs_identity"])
    if rootfs.get("identity") != identity["rootfs_identity"]:
        raise RuntimeError("rootfs identity drifted after verification")
    paths = {
        name: os.path.join(EVIDENCE, filename)
        for name, filename in common.ADMISSION_EVIDENCE_FILES.items()
    }
    stamp = {
        "schema": common.ADMISSION_SCHEMA,
        "runtime_digest": common.RUNTIME_DIGEST,
        "probe_session_id": session["probe_session_id"],
        "boot_id": common.boot_id(),
        "kernel_release": os.uname()[2],
        "artifact_lock_sha256": identity["artifact_lock_sha256"],
        "runner_sha256": identity["runner_sha256"],
        "artifact_sha256": identity["artifact_sha256"],
        "rootfs_identity": identity["rootfs_identity"],
        "evidence_sha256": {
            name: sha256_file(path) for name, path in paths.items()
        },
        "eligible": True,
    }
    temporary = common.ADMISSION_STAMP + ".tmp-%d" % os.getpid()
    with open(temporary, "w") as handle:
        handle.write(common.canonical_json(stamp) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.chmod(temporary, 0o444)
    os.replace(temporary, common.ADMISSION_STAMP)
    try:
        public_after = public_metadata()
        private_after = private_metadata()
        if not public_after.get("formal_eligible") or not private_after.get(
            "formal_eligible"
        ):
            raise RuntimeError("post-admission metadata remained ineligible")
        write_json(os.path.join(EVIDENCE, "public-metadata-admitted.json"), public_after)
        write_json(os.path.join(EVIDENCE, "private-metadata-admitted.json"), private_after)
    except BaseException:
        invalidate_admission()
        raise
    return stamp

def finalize_admission():
    if os.path.lexists("/tmp/camg-autoresearch/verification.lock"):
        raise RuntimeError("Installation verification lock remains during final validation")
    cleanup_receipt()
    stamp = activate_admission()
    print(
        common.canonical_json(
            {
                "schema": "openmle_fast_admission_finalization_v1",
                "ok": True,
                "admission_stamp_sha256": common.sha256_file(common.ADMISSION_STAMP),
                "stamp_schema": stamp["schema"],
            }
        )
    )
    return 0

def main(argv):
    if len(argv) in (2, 3) and argv[1] == "measure-rootfs":
        if os.geteuid() != 0 or os.uname().sysname != "Linux":
            raise SystemExit("rootfs measurement requires root on the exact Linux pod")
        try:
            timeout_seconds = 900 if len(argv) == 2 else int(argv[2])
        except ValueError:
            return 2
        if timeout_seconds <= 0 or timeout_seconds > 1800:
            return 2
        proposal = common.rootfs_tree_lock_proposal(
            deadline=time.monotonic() + timeout_seconds
        )
        print(common.canonical_json(proposal))
        return 0
    if len(argv) == 2 and argv[1] == "invalidate-admission":
        invalidate_admission()
        print(
            common.canonical_json(
                {"schema": "openmle_fast_admission_invalidation_v1", "ok": True}
            )
        )
        return 0
    if len(argv) == 2 and argv[1] == "finalize-admission":
        try:
            return finalize_admission()
        except BaseException:
            invalidate_admission()
            return 1
    if len(argv) != 1:
        return 2
    if os.geteuid() != 0 or os.uname().sysname != "Linux":
        raise SystemExit("remote probes require root on the exact Linux pod")
    start_probe_session()
    rootfs = write_rootfs_evidence()
    if not rootfs["ok"]:
        raise SystemExit("pinned rootfs identity/content verification failed")
    before_public = public_metadata()
    before_private = private_metadata()
    write_json(os.path.join(EVIDENCE, "public-metadata-pre-admission.json"), before_public)
    write_json(os.path.join(EVIDENCE, "private-metadata-pre-admission.json"), before_private)
    if before_public.get("formal_eligible") or before_private.get("formal_eligible"):
        raise SystemExit("unexpected pre-existing admission stamp")
    if not before_public["active_verification"]["all_checks_pass"]:
        raise SystemExit("public active preflight failed")
    if not before_private["active_verification"]["all_checks_pass"]:
        raise SystemExit("private active preflight failed")

    public_summary = run_public_probes()
    g64, submission, public_record, private_record = run_g64_public()
    live = run_live_cgroup_probe()
    private_summary = run_private_probes(submission, public_record, private_record)
    if not (public_summary["ok"] and g64["ok"] and live["ok"] and private_summary["ok"]):
        return 1
    print(
        common.canonical_json(
            {
                "schema": "openmle_fast_exact_runtime_integration_probe_v1",
                "ok": True,
                "public_probes": public_summary["pass_count"],
                "private_probes": private_summary["pass_count"],
                "g64": g64["ok"],
                "live_cgroup_v1": live["ok"],
                "admission_pending_lock_release": True,
            }
        )
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
