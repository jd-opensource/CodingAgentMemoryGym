from __future__ import print_function

import ctypes
import errno
import fcntl
import hashlib
import json
import math
import os
import selectors
import signal
import stat
import subprocess
import time
import uuid

RUNTIME_DIGEST = (
    "sha256:ada19e0d27dadb991c5b6112e00f116b26359067d5298650eb2eeff7d8385af2"
)
ROOTFS = (
    "/var/lib/camg/oci-rootfs/"
    "sha256-ada19e0d27dadb991c5b6112e00f116b26359067d5298650eb2eeff7d8385af2/rootfs"
)
SCRATCH = "/tmp/camg-autoresearch"
PUBLIC_WORKSPACE_ROOT = os.path.join(SCRATCH, "public-workspaces")
RUN_ROOT = os.path.join(SCRATCH, "runs")
STATE_ROOT = os.path.join(SCRATCH, "public-state")

SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__))
SUPERVISOR = os.path.join(SCRIPT_ROOT, "bin", "openmle-sandbox-supervisor")
PYTHON_WRAPPER = os.path.join(SCRIPT_ROOT, "bin", "openmle-python-wrapper")
FIT_HOOK = os.path.join(SCRIPT_ROOT, "fit_hook.py")
PRIVATE_WORKER = os.path.join(SCRIPT_ROOT, "private_worker.py")
ADMISSION_STAMP = os.path.join(SCRATCH, "admission-stamp.json")
ARTIFACT_LOCK = os.path.join(SCRIPT_ROOT, "artifact-lock.json")
ROOTFS_TREE_LOCK = os.path.join(SCRIPT_ROOT, "rootfs-tree-lock.json")
PUBLIC_RUNNER = os.path.join(SCRIPT_ROOT, "public_runner.py")
PRIVATE_RUNNER = os.path.join(SCRIPT_ROOT, "private_runner.py")
REMOTE_PROBE = os.path.join(SCRIPT_ROOT, "remote_probe.py")

ROOTFS_TREE_ALGORITHM = "sha256_path_type_mode_uid_gid_nlink_size_content_v1"
ROOTFS_PYTHON_PATH = "/opt/miniconda3/envs/testbed/bin/python3.10"

ARTIFACT_LOCK_MEMBERS = (
    "bin/openmle-python-wrapper",
    "bin/openmle-sandbox-supervisor",
    "build-provenance.json",
    "build_bundle.sh",
    "fit_hook.py",
    "install_bundle.sh",
    "private_runner.py",
    "private_worker.py",
    "public_runner.py",
    "python_wrapper.c",
    "remote_cleanup.sh",
    "remote_probe.py",
    "rootfs-tree-lock.json",
    "runtime_common.py",
    "sandbox_supervisor.c",
    "schemas/private-runner-metadata.schema.json",
    "schemas/private-runner-request.schema.json",
    "schemas/private-runner-result.schema.json",
    "schemas/public-runner-lifecycle.schema.json",
    "schemas/public-runner-metadata.schema.json",
    "schemas/public-runner-receipt.schema.json",
    "schemas/public-runner-request.schema.json",
    "tests/adapter_fixture.py",
    "tests/generic_openmle_baseline.py",
    "tests/test_budget_ledger_receipt.py",
    "tests/test_protocols.py",
    "verify_installation.sh",
)
ARTIFACT_EXECUTABLE_MEMBERS = frozenset(
    (
        "bin/openmle-python-wrapper",
        "bin/openmle-sandbox-supervisor",
        "build_bundle.sh",
        "install_bundle.sh",
        "private_runner.py",
        "public_runner.py",
        "remote_cleanup.sh",
        "remote_probe.py",
        "verify_installation.sh",
    )
)

ADMISSION_SCHEMA = "openmle_fast_runtime_admission_stamp_v3"
PROBE_CAPABILITY_SCHEMA = "openmle_fast_probe_operation_capability_v1"
PROBE_CAPABILITY_ENV = "OPENMLE_EXACT_PROBE_AUTH_FD"
PROBE_CAPABILITY_OPERATIONS = frozenset(
    ("public.execute", "public.freeze", "public.teardown", "private.grade")
)
PROBE_CAPABILITY_MAX_NS = 10 * 1000 * 1000 * 1000
ADMISSION_EVIDENCE_FILES = {
    "probe_session": "probe-session.json",
    "public_probe_summary": "public-probe-summary.json",
    "private_probe_summary": "private-probe-summary.json",
    "cleanup_receipt": "cleanup-receipt.json",
    "g64_public_execution": "g64-public-execution.json",
    "cgroup_v1_live": "cgroup-v1-live.json",
    "installation_lock_cleanup": "installation-lock-cleanup.json",
    "rootfs_evidence": "rootfs-evidence.json",
}

ROOTFS_MANIFEST_SHA256 = "ada19e0d27dadb991c5b6112e00f116b26359067d5298650eb2eeff7d8385af2"
ROOTFS_CONFIG_SHA256 = "6fd8e715386b93a5b952e8f22a2c6b97ecbef51f51164c4a13cf4129e08e93bf"
ROOTFS_BASH_SHA256 = "59474588a312b6b6e73e5a42a59bf71e62b55416b6c9d5e4a6e1c630c2a9ecd4"
ROOTFS_REGULAR_FILES = 210770
ROOTFS_BYTES = 30495880931


GIB = 1024 ** 3
MIB = 1024 ** 2
KIB = 1024

PUBLIC_LIMITS = {
    "max_policy_actions": 200,
    "cpu_vcpus": 2,
    "memory_bytes": 4 * GIB,
    "swap_bytes": 0,
    "workspace_bytes": 2 * GIB,
    "tmp_bytes": 256 * MIB,
    "max_processes": 64,
    "max_open_files": 256,
    "max_files": 100000,
    "max_file_bytes": 256 * MIB,
    "max_submission_bytes": 64 * MIB,
    "shell_wall_ms": 250000,
    "managed_runtime_per_action_ms": 240000,
    "managed_runtime_per_episode_ms": 3000000,
    "episode_wall_ms": 3600000,
    "grader_cpu_vcpus": 1,
    "grader_memory_bytes": 2 * GIB,
    "grader_max_processes": 32,
    "grader_worker_wall_ms": 7000,
    "grader_total_wall_ms": 7500,
    "grader_max_concurrent_requests": 8,
    "grader_input_bytes": 64 * MIB,
    "raw_output_bytes": 8 * MIB,
    "observation_bytes": 64 * KIB,
    "observation_head_bytes": 32 * KIB,
    "observation_tail_bytes": 32 * KIB,
}

PRIVATE_LIMITS = {
    "cpu_vcpus": 1,
    "memory_bytes": 2 * GIB,
    "max_processes": 32,
    "wall_ms": 7000,
    "input_bytes": 64 * MIB,
}

CONTROLLERS = ("cpu,cpuacct", "memory", "pids")
CLONE_NEWNS = 0x00020000
SUPERVISOR_SCHEMA = "openmle_fast_supervisor_stats_v1"

SANDBOX_SETUP_GRACE_SECONDS = 8.0
SANDBOX_OPERATION_GRACE_SECONDS = 3.0
SANDBOX_CLEANUP_GRACE_SECONDS = 8.0

class RuntimeErrorClosed(RuntimeError):
    pass

class SandboxInfrastructureError(RuntimeErrorClosed):

    def __init__(self, phase, cause, prior_phase=None):
        if not isinstance(phase, str) or not phase:
            phase = "unknown"
        self.phase = phase[:96]
        self.cause_type = type(cause).__name__[:96]
        self.original_cause = cause
        self.prior_phase = (
            prior_phase[:96] if isinstance(prior_phase, str) and prior_phase else None
        )
        RuntimeErrorClosed.__init__(
            self, "sandbox %s failed (%s)" % (self.phase, self.cause_type)
        )

def monotonic_ns():

    native = getattr(time, "monotonic_ns", None)
    if native is not None:
        return native()
    return int(time.monotonic() * 1000 * 1000 * 1000)

def canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))

def canonical_sha256(value):
    return hashlib.sha256((canonical_json(value) + "\n").encode("utf-8")).hexdigest()

def strict_json_loads(raw):
    def reject_duplicates(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate JSON key")
            result[key] = value
        return result

    return json.loads(raw, object_pairs_hook=reject_duplicates)

def read_stdin_json(maximum=1024 * 1024):
    payload = sys_stdin_buffer_read(maximum + 1)
    if len(payload) > maximum:
        raise RuntimeErrorClosed("request exceeds byte cap")
    try:
        return strict_json_loads(payload.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        raise RuntimeErrorClosed("request is not strict UTF-8 JSON")

def sys_stdin_buffer_read(size):

    import sys

    return sys.stdin.buffer.read(size)

def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()

def bytes_sha256(payload):
    return hashlib.sha256(payload).hexdigest()

def create_memfd(name, flags):

    if not isinstance(name, str) or not name or "\x00" in name:
        raise RuntimeErrorClosed("invalid memfd name")
    if isinstance(flags, bool) or not isinstance(flags, int) or flags < 0:
        raise RuntimeErrorClosed("invalid memfd flags")
    creator = getattr(os, "memfd_create", None)
    if creator is not None:
        return creator(name, flags)
    try:
        libc = ctypes.CDLL(None, use_errno=True)
        creator = libc.memfd_create
    except (AttributeError, OSError) as exc:
        raise RuntimeErrorClosed("memfd_create is unavailable") from exc
    creator.argtypes = (ctypes.c_char_p, ctypes.c_uint)
    creator.restype = ctypes.c_int
    ctypes.set_errno(0)
    descriptor = creator(os.fsencode(name), flags)
    if descriptor < 0:
        error = ctypes.get_errno()
        raise RuntimeErrorClosed("memfd_create failed: errno %d" % error)
    return descriptor

def boot_id():
    try:
        with open("/proc/sys/kernel/random/boot_id", "r") as handle:
            value = handle.read().strip()
        if value:
            return value
    except OSError:
        pass
    return "unavailable"

def probe_artifact_identity():

    expected = _safe_hash(ARTIFACT_LOCK)
    return {
        "runtime_digest": RUNTIME_DIGEST,
        "artifact": artifact_identity(expected),
    }

def probe_session_path():
    return os.path.join(SCRATCH, "evidence", "probe-session.json")

def load_probe_session():
    try:
        with open(probe_session_path(), "r") as handle:
            value = strict_json_loads(handle.read())
    except (OSError, ValueError):
        return None
    required = {
        "schema",
        "probe_session_id",
        "boot_id",
        "kernel_release",
        "artifact_identity",
    }
    session_id = value.get("probe_session_id") if isinstance(value, dict) else None
    if (
        not isinstance(value, dict)
        or set(value) != required
        or value.get("schema") != "openmle_fast_probe_session_v1"
        or not isinstance(session_id, str)
        or len(session_id) != 32
        or any(character not in "0123456789abcdef" for character in session_id)
        or value.get("boot_id") != boot_id()
        or value.get("kernel_release") != os.uname()[2]
        or value.get("artifact_identity") != probe_artifact_identity()
    ):
        return None
    return value

def evidence_context(session=None):
    current = load_probe_session() if session is None else session
    if not isinstance(current, dict):
        raise RuntimeErrorClosed("probe session is unavailable")
    return {
        "probe_session_id": current.get("probe_session_id"),
        "boot_id": current.get("boot_id"),
        "kernel_release": current.get("kernel_release"),
        "artifact_identity": current.get("artifact_identity"),
    }

def bind_evidence_context(value, session=None):
    if not isinstance(value, dict):
        raise RuntimeErrorClosed("admission evidence must be an object")
    result = dict(value)
    context = evidence_context(session)
    if set(result).intersection(context):
        raise RuntimeErrorClosed("admission evidence context was prepopulated")
    result.update(context)
    return result

def evidence_context_matches(value, session=None):
    try:
        expected = evidence_context(session)
    except RuntimeErrorClosed:
        return False
    return isinstance(value, dict) and all(
        value.get(name) == expected_value for name, expected_value in expected.items()
    )

def cgroup_mode():
    has_v1 = False
    try:
        with open("/proc/self/cgroup", "r") as handle:
            for line in handle:
                fields = line.rstrip("\n").split(":", 2)
                if len(fields) == 3 and fields[0] != "0" and fields[1]:
                    has_v1 = True
    except OSError:
        pass
    has_v2 = os.path.isfile("/sys/fs/cgroup/cgroup.controllers")
    if has_v1 and has_v2:
        return "hybrid"
    if has_v1:
        return "v1"
    if has_v2:
        return "v2"
    return "unknown"

def controller_attestation():
    required = {
        "cpu": ("cpu,cpuacct", ("cpu.cfs_period_us", "cpu.cfs_quota_us", "tasks")),
        "memory": (
            "memory",
            (
                "memory.limit_in_bytes",
                "memory.memsw.limit_in_bytes",
                "memory.swappiness",
                "tasks",
            ),
        ),
        "pids": ("pids", ("pids.max", "tasks")),
    }
    controllers = {}
    for logical, pair in required.items():
        hierarchy, names = pair
        root = os.path.join("/sys/fs/cgroup", hierarchy)
        controllers[logical] = {
            "hierarchy": hierarchy,
            "required_files": list(names),
            "available": all(os.path.isfile(os.path.join(root, name)) for name in names),
        }
    return {
        "schema": "openmle_fast_cgroup_controller_attestation_v1",
        "version": cgroup_mode(),
        "controllers": controllers,
        "no_swap_contract": "memory_limit_equals_memsw_limit_and_swappiness_zero",
    }

def _stable_stat_signature(info):
    return (
        int(info.st_dev),
        int(info.st_ino),
        int(info.st_mode),
        int(info.st_uid),
        int(info.st_gid),
        int(info.st_nlink),
        int(info.st_size),
        int(info.st_mtime_ns),
        int(info.st_ctime_ns),
    )

def _hash_framed(digest, payload):
    digest.update(len(payload).to_bytes(8, "big"))
    digest.update(payload)

def _hash_tree_header(digest, relative, kind, info):
    digest.update(b"E")
    for value in (
        os.fsencode(relative),
        kind,
        str(stat.S_IMODE(info.st_mode)).encode("ascii"),
        str(int(info.st_uid)).encode("ascii"),
        str(int(info.st_gid)).encode("ascii"),
        str(int(info.st_nlink)).encode("ascii"),
        str(int(info.st_size)).encode("ascii"),
    ):
        _hash_framed(digest, value)

def _symlink_stays_in_root(root, path, target):
    if os.path.isabs(target):
        resolved = os.path.normpath(os.path.join(root, target.lstrip("/")))
    else:
        resolved = os.path.normpath(os.path.join(os.path.dirname(path), target))
    try:
        return os.path.commonpath((root, resolved)) == root
    except ValueError:
        return False

def _sha256_file_deadline(path, deadline):
    digest = hashlib.sha256()
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
    descriptor = os.open(path, flags)
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise RuntimeErrorClosed("rootfs Python is not a regular file")
        with os.fdopen(descriptor, "rb", closefd=False) as handle:
            while True:
                check_deadline(deadline, "rootfs measurement")
                chunk = handle.read(1024 * 1024)
                if not chunk:
                    break
                digest.update(chunk)
        after = os.fstat(descriptor)
        if _stable_stat_signature(before) != _stable_stat_signature(after):
            raise RuntimeErrorClosed("rootfs Python changed during measurement")
    finally:
        os.close(descriptor)
    return digest.hexdigest()

def measure_rootfs_tree(rootfs=ROOTFS, python_path=ROOTFS_PYTHON_PATH, deadline=None):

    check_deadline(deadline, "rootfs measurement")
    root = os.path.abspath(rootfs)
    root_before = os.lstat(root)
    if os.path.islink(root) or not stat.S_ISDIR(root_before.st_mode):
        raise RuntimeErrorClosed("rootfs measurement target is not a real directory")
    digest = hashlib.sha256()
    digest.update((ROOTFS_TREE_ALGORITHM + "\0").encode("ascii"))
    regular_files = [0]
    regular_bytes = [0]

    def visit(path, relative):
        check_deadline(deadline, "rootfs measurement")
        before = os.lstat(path)
        signature = _stable_stat_signature(before)
        if stat.S_ISDIR(before.st_mode):
            _hash_tree_header(digest, relative, b"directory", before)
            try:
                with os.scandir(path) as iterator:
                    names = sorted((entry.name for entry in iterator), key=os.fsencode)
            except OSError as exc:
                raise RuntimeErrorClosed("rootfs directory is unreadable") from exc
            for name in names:
                child_relative = name if relative == "." else relative + "/" + name
                visit(os.path.join(path, name), child_relative)
            after = os.lstat(path)
            if signature != _stable_stat_signature(after):
                raise RuntimeErrorClosed("rootfs directory changed during measurement")
            return
        if stat.S_ISREG(before.st_mode):
            _hash_tree_header(digest, relative, b"regular", before)
            digest.update(b"C")
            digest.update(int(before.st_size).to_bytes(8, "big"))
            flags = (
                os.O_RDONLY
                | getattr(os, "O_CLOEXEC", 0)
                | getattr(os, "O_NOFOLLOW", 0)
            )
            descriptor = os.open(path, flags)
            size = 0
            try:
                opened = os.fstat(descriptor)
                if _stable_stat_signature(opened) != signature:
                    raise RuntimeErrorClosed("rootfs file identity changed before read")
                with os.fdopen(descriptor, "rb", closefd=False) as handle:
                    while True:
                        check_deadline(deadline, "rootfs measurement")
                        chunk = handle.read(1024 * 1024)
                        if not chunk:
                            break
                        size += len(chunk)
                        digest.update(chunk)
                after_open = os.fstat(descriptor)
            finally:
                os.close(descriptor)
            after_path = os.lstat(path)
            if (
                size != before.st_size
                or _stable_stat_signature(after_open) != signature
                or _stable_stat_signature(after_path) != signature
            ):
                raise RuntimeErrorClosed("rootfs file changed during measurement")
            regular_files[0] += 1
            regular_bytes[0] += size
            return
        if stat.S_ISLNK(before.st_mode):
            target = os.readlink(path)
            if not _symlink_stays_in_root(root, path, target):
                raise RuntimeErrorClosed("rootfs symlink escapes the root")
            _hash_tree_header(digest, relative, b"symlink", before)
            _hash_framed(digest, os.fsencode(target))
            after = os.lstat(path)
            if signature != _stable_stat_signature(after):
                raise RuntimeErrorClosed("rootfs symlink changed during measurement")
            return
        raise RuntimeErrorClosed("rootfs contains unsupported special entry")

    visit(root, ".")
    root_after = os.lstat(root)
    if _stable_stat_signature(root_before) != _stable_stat_signature(root_after):
        raise RuntimeErrorClosed("rootfs changed during measurement")
    relative_python = python_path.lstrip("/")
    if not relative_python or os.path.normpath(relative_python).startswith(".."):
        raise RuntimeErrorClosed("rootfs Python path is unsafe")
    python_host_path = os.path.realpath(os.path.join(root, relative_python))
    try:
        python_inside = os.path.commonpath((root, python_host_path)) == root
    except ValueError:
        python_inside = False
    if not python_inside:
        raise RuntimeErrorClosed("rootfs Python escapes the root")
    python_sha256 = _sha256_file_deadline(python_host_path, deadline)
    check_deadline(deadline, "rootfs measurement")
    return {
        "schema": "openmle_fast_rootfs_tree_measurement_v1",
        "algorithm": ROOTFS_TREE_ALGORITHM,
        "tree_sha256": digest.hexdigest(),
        "python_path": "/" + relative_python,
        "python_sha256": python_sha256,
        "regular_files": regular_files[0],
        "bytes": regular_bytes[0],
    }

def _rootfs_tree_lock_evidence(path=None):
    lock_path = ROOTFS_TREE_LOCK if path is None else path
    try:
        with open(lock_path, "r") as handle:
            value = strict_json_loads(handle.read())
    except (OSError, ValueError):
        return None
    required = {
        "schema",
        "runtime_digest",
        "algorithm",
        "tree_sha256",
        "python_path",
        "python_sha256",
        "regular_files",
        "bytes",
        "status",
    }
    if (
        not isinstance(value, dict)
        or set(value) != required
        or value.get("schema") != "openmle_fast_rootfs_tree_lock_v2"
        or value.get("runtime_digest") != RUNTIME_DIGEST
        or value.get("algorithm") != ROOTFS_TREE_ALGORITHM
        or value.get("python_path") != ROOTFS_PYTHON_PATH
        or (
            value.get("tree_sha256") is not None
            and not _is_sha256(value.get("tree_sha256"))
        )
        or (
            value.get("python_sha256") is not None
            and not _is_sha256(value.get("python_sha256"))
        )
        or isinstance(value.get("regular_files"), bool)
        or not isinstance(value.get("regular_files"), int)
        or value.get("regular_files") < 0
        or isinstance(value.get("bytes"), bool)
        or not isinstance(value.get("bytes"), int)
        or value.get("bytes") < 0
        or not isinstance(value.get("status"), str)
        or not value.get("status")
    ):
        return None
    return value

def load_rootfs_tree_lock(path=None):
    value = _rootfs_tree_lock_evidence(path)
    if (
        value is None
        or not _is_sha256(value.get("tree_sha256"))
        or not _is_sha256(value.get("python_sha256"))
        or value.get("regular_files") <= 0
        or value.get("bytes") <= 0
        or value.get("status") != "verified_authorized_pod"
    ):
        return None
    return value

def rootfs_tree_lock_proposal(deadline=None):
    measured = measure_rootfs_tree(deadline=deadline)
    return {
        "schema": "openmle_fast_rootfs_tree_lock_v2",
        "runtime_digest": RUNTIME_DIGEST,
        "algorithm": measured["algorithm"],
        "tree_sha256": measured["tree_sha256"],
        "python_path": measured["python_path"],
        "python_sha256": measured["python_sha256"],
        "regular_files": measured["regular_files"],
        "bytes": measured["bytes"],
        "status": "measurement_proposal",
    }

def _rootfs_measurement_matches_lock(measurement, lock):
    return (
        isinstance(measurement, dict)
        and isinstance(lock, dict)
        and measurement.get("algorithm") == lock.get("algorithm")
        and measurement.get("tree_sha256") == lock.get("tree_sha256")
        and measurement.get("python_path") == lock.get("python_path")
        and measurement.get("python_sha256") == lock.get("python_sha256")
        and measurement.get("regular_files") == lock.get("regular_files")
        and measurement.get("bytes") == lock.get("bytes")
    )

def _rootfs_identity_impl(deadline=None, measure_tree=True):

    parent = os.path.dirname(ROOTFS)
    tree_lock_sha256 = _safe_hash(ROOTFS_TREE_LOCK)
    tree_lock = load_rootfs_tree_lock()
    tree_lock_evidence = _rootfs_tree_lock_evidence()
    tree_measurement = None
    sidecar_names = (".complete", "metadata.json", "manifest.json", "config.json")
    sidecars = {name: None for name in sidecar_names}
    critical_files = {"bash": None, "python": None}
    root_stat = None
    metadata_contract = {
        "resolved_digest": None,
        "manifest_sha256": None,
        "config_sha256": None,
        "bash_sha256": None,
        "regular_files": None,
        "bytes": None,
    }
    valid = True
    try:
        root_info = os.lstat(ROOTFS)
        valid = valid and stat.S_ISDIR(root_info.st_mode) and not os.path.islink(ROOTFS)
        valid = valid and root_info.st_uid == 0 and not (root_info.st_mode & 0o022)
        root_stat = {
            "device": int(root_info.st_dev),
            "inode": int(root_info.st_ino),
            "mode": int(stat.S_IMODE(root_info.st_mode)),
            "uid": int(root_info.st_uid),
            "gid": int(root_info.st_gid),
            "mtime_ns": int(root_info.st_mtime_ns),
            "ctime_ns": int(root_info.st_ctime_ns),
        }
        for name in sidecar_names:
            path = os.path.join(parent, name)
            info = os.lstat(path)
            if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or os.path.islink(path):
                valid = False
            sidecars[name] = _safe_hash(path)
        with open(os.path.join(parent, "metadata.json"), "r") as handle:
            metadata = strict_json_loads(handle.read())
        rootfs_metadata = metadata.get("rootfs") if isinstance(metadata, dict) else None
        metadata_contract = {
            "resolved_digest": metadata.get("resolved_digest") if isinstance(metadata, dict) else None,
            "manifest_sha256": metadata.get("manifest_sha256") if isinstance(metadata, dict) else None,
            "config_sha256": metadata.get("config_sha256") if isinstance(metadata, dict) else None,
            "bash_sha256": rootfs_metadata.get("bash_sha256")
            if isinstance(rootfs_metadata, dict)
            else None,
            "regular_files": rootfs_metadata.get("regular_files")
            if isinstance(rootfs_metadata, dict)
            else None,
            "bytes": rootfs_metadata.get("bytes")
            if isinstance(rootfs_metadata, dict)
            else None,
        }
        critical_paths = {
            "bash": os.path.join(ROOTFS, "bin", "bash"),
            "python": os.path.join(ROOTFS, ROOTFS_PYTHON_PATH.lstrip("/")),
        }
        for name, path in critical_paths.items():
            if not os.path.isfile(path):
                valid = False
                critical_files[name] = None
            else:
                critical_files[name] = _safe_hash(path)
        if tree_lock is not None and measure_tree:
            tree_measurement = measure_rootfs_tree(deadline=deadline)
    except (OSError, ValueError, AttributeError):
        valid = False
    except RuntimeErrorClosed:
        valid = False
    expected_metadata = {
        "resolved_digest": RUNTIME_DIGEST,
        "manifest_sha256": ROOTFS_MANIFEST_SHA256,
        "config_sha256": ROOTFS_CONFIG_SHA256,
        "bash_sha256": ROOTFS_BASH_SHA256,
        "regular_files": ROOTFS_REGULAR_FILES,
        "bytes": ROOTFS_BYTES,
    }
    anchor_valid = bool(
        valid
        and os.path.basename(parent) == "sha256-" + ROOTFS_MANIFEST_SHA256
        and sidecars.get("manifest.json") == ROOTFS_MANIFEST_SHA256
        and sidecars.get("config.json") == ROOTFS_CONFIG_SHA256
        and critical_files.get("bash") == ROOTFS_BASH_SHA256
        and tree_lock is not None
        and critical_files.get("python") == tree_lock.get("python_sha256")
        and tree_lock.get("regular_files") == ROOTFS_REGULAR_FILES
        and tree_lock.get("bytes") == ROOTFS_BYTES
        and metadata_contract == expected_metadata
    )
    valid = bool(
        anchor_valid
        and (
            not measure_tree
            or _rootfs_measurement_matches_lock(tree_measurement, tree_lock)
        )
    )
    return {
        "schema": "openmle_fast_rootfs_identity_v2",
        "path": ROOTFS,
        "runtime_digest": RUNTIME_DIGEST,
        "tree_lock_sha256": tree_lock_sha256,
        "tree_lock": tree_lock_evidence,
        "tree_measurement": tree_measurement,
        "root_stat": root_stat,
        "sidecar_sha256": sidecars,
        "critical_file_sha256": critical_files,
        "metadata_contract": metadata_contract,
        "valid": valid,
    }

def rootfs_identity(deadline=None):

    return _rootfs_identity_impl(deadline=deadline, measure_tree=True)

def rootfs_anchor(deadline=None):

    value = _rootfs_identity_impl(deadline=deadline, measure_tree=False)
    value["schema"] = "openmle_fast_rootfs_anchor_v1"
    return value

def _anchor_from_full_identity(value):
    if not isinstance(value, dict):
        return None
    result = dict(value)
    result["schema"] = "openmle_fast_rootfs_anchor_v1"
    result["tree_measurement"] = None
    return result

def verified_rootfs_identity(deadline=None):

    current_anchor = rootfs_anchor(deadline=deadline)
    fallback = dict(current_anchor)
    fallback["schema"] = "openmle_fast_rootfs_identity_v2"
    fallback["valid"] = False
    session = load_probe_session()
    try:
        with open(
            os.path.join(SCRATCH, "evidence", ADMISSION_EVIDENCE_FILES["rootfs_evidence"]),
            "r",
        ) as handle:
            evidence = strict_json_loads(handle.read())
    except (OSError, ValueError):
        return fallback
    identity = evidence.get("identity") if isinstance(evidence, dict) else None
    lock = load_rootfs_tree_lock()
    if (
        session is None
        or not evidence_context_matches(evidence, session)
        or set(evidence)
        != {
            "schema",
            "ok",
            "identity",
            "probe_session_id",
            "boot_id",
            "kernel_release",
            "artifact_identity",
        }
        or evidence.get("schema") != "openmle_fast_rootfs_admission_evidence_v2"
        or evidence.get("ok") is not True
        or not isinstance(identity, dict)
        or identity.get("schema") != "openmle_fast_rootfs_identity_v2"
        or identity.get("valid") is not True
        or lock is None
        or not _rootfs_measurement_matches_lock(identity.get("tree_measurement"), lock)
        or _anchor_from_full_identity(identity) != current_anchor
    ):
        return fallback
    return identity

def admission_runtime_identity(rootfs_value=None):
    rootfs = verified_rootfs_identity() if rootfs_value is None else rootfs_value
    return {
        "artifact_lock_sha256": _safe_hash(ARTIFACT_LOCK),
        "runner_sha256": {
            "public": _safe_hash(PUBLIC_RUNNER),
            "private": _safe_hash(PRIVATE_RUNNER),
        },
        "artifact_sha256": {
            "supervisor": _safe_hash(SUPERVISOR),
            "python_wrapper": _safe_hash(PYTHON_WRAPPER),
            "fit_hook": _safe_hash(FIT_HOOK),
        },
        "rootfs_identity": rootfs,
    }

def _admission_stamp_valid(active_checks, runtime_identity=None, session=None):
    try:
        with open(ADMISSION_STAMP, "r") as handle:
            value = strict_json_loads(handle.read())
    except (OSError, ValueError):
        return False, None
    required = {
        "schema",
        "runtime_digest",
        "probe_session_id",
        "boot_id",
        "kernel_release",
        "artifact_lock_sha256",
        "runner_sha256",
        "artifact_sha256",
        "rootfs_identity",
        "evidence_sha256",
        "eligible",
    }
    current_session = load_probe_session() if session is None else session
    identity = (
        admission_runtime_identity()
        if runtime_identity is None
        else runtime_identity
    )
    evidence_paths = {
        name: os.path.join(SCRATCH, "evidence", filename)
        for name, filename in ADMISSION_EVIDENCE_FILES.items()
    }
    evidence_hashes = value.get("evidence_sha256") if isinstance(value, dict) else None
    evidence_values = {}
    try:
        for name, path in evidence_paths.items():
            with open(path, "r") as handle:
                evidence_values[name] = strict_json_loads(handle.read())
    except (OSError, ValueError):
        evidence_values = {}
    valid = (
        isinstance(value, dict)
        and isinstance(current_session, dict)
        and set(value) == required
        and value.get("schema") == ADMISSION_SCHEMA
        and value.get("runtime_digest") == RUNTIME_DIGEST
        and value.get("probe_session_id")
        == current_session.get("probe_session_id")
        and value.get("boot_id") == boot_id()
        and value.get("kernel_release") == os.uname()[2]
        and value.get("artifact_lock_sha256") == identity["artifact_lock_sha256"]
        and value.get("runner_sha256") == identity["runner_sha256"]
        and value.get("artifact_sha256") == identity["artifact_sha256"]
        and value.get("rootfs_identity") == identity["rootfs_identity"]
        and identity["artifact_sha256"]
        == verified_component_digests(identity["artifact_lock_sha256"])
        and identity["rootfs_identity"].get("valid") is True
        and value.get("eligible") is True
        and isinstance(evidence_hashes, dict)
        and set(evidence_hashes) == set(evidence_paths)
        and set(evidence_values) == set(evidence_paths)
        and all(
            evidence_context_matches(item, current_session)
            for item in evidence_values.values()
        )
        and all(
            _is_sha256(evidence_hashes.get(name))
            and _safe_hash(path) == evidence_hashes.get(name)
            for name, path in evidence_paths.items()
        )
        and all(active_checks.values())
    )
    return valid, value if valid else None

def validate_artifact_lock(expected_sha256, artifact_root=None):
    root = SCRIPT_ROOT if artifact_root is None else os.path.realpath(artifact_root)
    lock_path = os.path.join(root, "artifact-lock.json")
    if (
        not isinstance(expected_sha256, str)
        or len(expected_sha256) != 64
        or any(character not in "0123456789abcdef" for character in expected_sha256)
        or _safe_hash(lock_path) != expected_sha256
    ):
        return False
    try:
        with open(lock_path, "r") as handle:
            value = strict_json_loads(handle.read())
    except (OSError, ValueError):
        return False
    if (
        not isinstance(value, dict)
        or set(value) != {"schema", "runtime_digest", "files"}
        or value.get("schema") != "openmle_fast_runtime_artifact_lock_v1"
        or value.get("runtime_digest") != RUNTIME_DIGEST
        or not isinstance(value.get("files"), list)
    ):
        return False
    seen = set()
    for record in value["files"]:
        if not isinstance(record, dict) or set(record) != {"path", "sha256"}:
            return False
        relative = record.get("path")
        expected = record.get("sha256")
        if (
            not isinstance(relative, str)
            or not relative
            or relative.startswith("/")
            or ".." in relative.split("/")
            or relative in seen
            or not isinstance(expected, str)
            or len(expected) != 64
        ):
            return False
        seen.add(relative)
        path = os.path.join(root, *relative.split("/"))
        try:
            info = os.lstat(path)
        except OSError:
            return False
        if (
            stat.S_ISLNK(info.st_mode)
            or not stat.S_ISREG(info.st_mode)
            or info.st_nlink != 1
            or not _is_sha256(expected)
            or _safe_hash(path) != expected
        ):
            return False
    return seen == set(ARTIFACT_LOCK_MEMBERS)

def verified_component_digests(expected_sha256, artifact_root=None):
    """Use the content-verified build inventory as the sole component identity."""
    root = SCRIPT_ROOT if artifact_root is None else os.path.realpath(artifact_root)
    if not validate_artifact_lock(expected_sha256, artifact_root=root):
        return None
    try:
        with open(os.path.join(root, "artifact-lock.json"), "rb") as handle:
            raw = handle.read()
        if hashlib.sha256(raw).hexdigest() != expected_sha256:
            return None
        entries = {item["path"]: item["sha256"] for item in strict_json_loads(raw.decode())["files"]}
        return {
            "supervisor": entries["bin/openmle-sandbox-supervisor"],
            "python_wrapper": entries["bin/openmle-python-wrapper"],
            "fit_hook": entries["fit_hook.py"],
        }
    except (OSError, ValueError, KeyError, TypeError, UnicodeError):
        return None

def validate_install_inventory(root, expected_sha256):

    real = os.path.realpath(root)
    if os.path.islink(root) or not os.path.isdir(real):
        return False
    root_info = os.stat(real)
    if root_info.st_uid != 0 or stat.S_IMODE(root_info.st_mode) != 0o700:
        return False
    if not validate_artifact_lock(expected_sha256, artifact_root=real):
        return False
    expected_files = set(ARTIFACT_LOCK_MEMBERS) | {"artifact-lock.json"}
    expected_directories = set()
    for relative in expected_files:
        parent = os.path.dirname(relative)
        while parent:
            expected_directories.add(parent)
            parent = os.path.dirname(parent)
    actual_files = set()
    actual_directories = set()
    try:
        for current, directories, files in os.walk(real, topdown=True, followlinks=False):
            relative_root = os.path.relpath(current, real)
            if relative_root == ".":
                relative_root = ""
            for name in directories:
                path = os.path.join(current, name)
                info = os.lstat(path)
                if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
                    return False
                relative = os.path.join(relative_root, name).replace(os.sep, "/")
                if info.st_uid != 0 or stat.S_IMODE(info.st_mode) != 0o700:
                    return False
                actual_directories.add(relative)
            for name in files:
                path = os.path.join(current, name)
                info = os.lstat(path)
                if (
                    stat.S_ISLNK(info.st_mode)
                    or not stat.S_ISREG(info.st_mode)
                    or info.st_nlink != 1
                ):
                    return False
                relative = os.path.join(relative_root, name).replace(os.sep, "/")
                expected_mode = (
                    0o555 if relative in ARTIFACT_EXECUTABLE_MEMBERS else 0o444
                )
                if info.st_uid != 0 or stat.S_IMODE(info.st_mode) != expected_mode:
                    return False
                actual_files.add(relative)
    except OSError:
        return False
    return actual_files == expected_files and actual_directories == expected_directories

def _is_sha256(value):
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )

def active_preflight(expected_artifact_lock_sha256=None):
    attestation = controller_attestation()
    controllers = attestation["controllers"]
    rootfs = verified_rootfs_identity()
    expected_lock = (
        _safe_hash(ARTIFACT_LOCK)
        if expected_artifact_lock_sha256 is None
        else expected_artifact_lock_sha256
    )
    components = verified_component_digests(expected_lock)
    checks = {
        "linux": os.name == "posix" and getattr(os.uname(), "sysname", "") == "Linux",
        "x86_64": getattr(os.uname(), "machine", "") == "x86_64",
        "root_identity": hasattr(os, "geteuid") and os.geteuid() == 0,
        "cgroup_v1_or_hybrid": attestation["version"] in ("v1", "hybrid"),
        "cpu_controller": controllers["cpu"]["available"],
        "memory_controller": controllers["memory"]["available"],
        "pids_controller": controllers["pids"]["available"],
        "rootfs_identity": rootfs["valid"],
        "supervisor": (
            components is not None
            and os.path.isfile(SUPERVISOR)
            and os.access(SUPERVISOR, os.X_OK)
            and _safe_hash(SUPERVISOR) == components["supervisor"]
        ),
        "python_wrapper": (
            components is not None
            and os.path.isfile(PYTHON_WRAPPER)
            and os.access(PYTHON_WRAPPER, os.X_OK)
            and _safe_hash(PYTHON_WRAPPER) == components["python_wrapper"]
        ),
        "fit_hook": components is not None and os.path.isfile(FIT_HOOK) and _safe_hash(FIT_HOOK) == components["fit_hook"],
        "mount_tool": os.path.isfile("/usr/bin/mount") and os.path.isfile("/usr/bin/umount"),
        "unshare_tool": os.path.isfile("/usr/bin/unshare"),
        "artifact_lock": components is not None,
        "artifact_install_inventory": validate_install_inventory(
            SCRIPT_ROOT, expected_lock
        ),
    }
    identity = admission_runtime_identity(rootfs)
    session = load_probe_session()
    stamp_valid, stamp = _admission_stamp_valid(
        checks, runtime_identity=identity, session=session
    )
    return {
        "schema": "openmle_fast_active_runtime_preflight_v1",
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "admission_stamp_valid": stamp_valid,
        "admission_stamp_digest": None if stamp is None else canonical_sha256(stamp),
        "boot_id": boot_id(),
        "rootfs_identity": rootfs,
    }

def _process_start_ticks(pid):
    try:
        with open("/proc/%d/stat" % pid, "r") as handle:
            raw = handle.read()
        tail = raw[raw.rfind(")") + 2 :].split()
        return int(tail[19])
    except (OSError, ValueError, IndexError):
        return None

def _parent_is_exact_remote_probe(pid):
    try:
        with open("/proc/%d/cmdline" % pid, "rb") as handle:
            arguments = [
                os.fsdecode(item)
                for item in handle.read(64 * KIB).split(b"\0")
                if item
            ]
    except OSError:
        return False
    candidates = []
    for argument in arguments[1:4]:
        if argument.startswith("/"):
            candidates.append(os.path.realpath(argument))
    return (
        REMOTE_PROBE in candidates
        and _safe_hash(REMOTE_PROBE) is not None
        and validate_artifact_lock(_safe_hash(ARTIFACT_LOCK))
    )

def _read_sealed_probe_capability(descriptor):
    required_seals = (
        getattr(fcntl, "F_SEAL_SEAL", 0x0001)
        | getattr(fcntl, "F_SEAL_SHRINK", 0x0002)
        | getattr(fcntl, "F_SEAL_GROW", 0x0004)
        | getattr(fcntl, "F_SEAL_WRITE", 0x0008)
    )
    get_seals = getattr(fcntl, "F_GET_SEALS", 1034)
    try:
        info = os.fstat(descriptor)
        if (
            not stat.S_ISREG(info.st_mode)
            or info.st_nlink != 0
            or info.st_uid != 0
            or stat.S_IMODE(info.st_mode) != 0o400
            or info.st_size <= 0
            or info.st_size > 64 * KIB
            or fcntl.fcntl(descriptor, get_seals) & required_seals
            != required_seals
        ):
            return None
        payload = os.pread(descriptor, info.st_size + 1, 0)
    except OSError:
        return None
    if len(payload) != info.st_size:
        return None
    try:
        return strict_json_loads(payload.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return None

def _probe_capability_valid(descriptor, operation, request, preflight, expected_lock):
    capability = _read_sealed_probe_capability(descriptor)
    session = load_probe_session()
    required = {
        "schema",
        "capability_id",
        "probe_session_id",
        "boot_id",
        "kernel_release",
        "artifact_identity",
        "artifact_lock_sha256",
        "rootfs_identity_sha256",
        "operation",
        "request_sha256",
        "parent_pid",
        "parent_start_ticks",
        "issued_monotonic_ns",
        "expires_monotonic_ns",
    }
    now = monotonic_ns()
    capability_id = capability.get("capability_id") if isinstance(capability, dict) else None
    parent_pid = os.getppid()
    return bool(
        isinstance(capability, dict)
        and isinstance(session, dict)
        and set(capability) == required
        and capability.get("schema") == PROBE_CAPABILITY_SCHEMA
        and isinstance(capability_id, str)
        and len(capability_id) == 32
        and all(character in "0123456789abcdef" for character in capability_id)
        and operation in PROBE_CAPABILITY_OPERATIONS
        and capability.get("operation") == operation
        and capability.get("request_sha256") == canonical_sha256(request)
        and capability.get("probe_session_id") == session.get("probe_session_id")
        and capability.get("boot_id") == boot_id()
        and capability.get("kernel_release") == os.uname()[2]
        and capability.get("artifact_identity") == probe_artifact_identity()
        and capability.get("artifact_lock_sha256") == expected_lock
        and capability.get("artifact_lock_sha256") == _safe_hash(ARTIFACT_LOCK)
        and capability.get("rootfs_identity_sha256")
        == canonical_sha256(preflight["rootfs_identity"])
        and preflight["rootfs_identity"].get("valid") is True
        and capability.get("parent_pid") == parent_pid
        and capability.get("parent_start_ticks") == _process_start_ticks(parent_pid)
        and _parent_is_exact_remote_probe(parent_pid)
        and isinstance(capability.get("issued_monotonic_ns"), int)
        and not isinstance(capability.get("issued_monotonic_ns"), bool)
        and isinstance(capability.get("expires_monotonic_ns"), int)
        and not isinstance(capability.get("expires_monotonic_ns"), bool)
        and capability["issued_monotonic_ns"] <= now
        and now <= capability["expires_monotonic_ns"]
        and 0
        < capability["expires_monotonic_ns"] - capability["issued_monotonic_ns"]
        <= PROBE_CAPABILITY_MAX_NS
    )

def require_runtime_admission(
    expected_artifact_lock_sha256, operation=None, request=None
):

    raw_descriptor = os.environ.pop(PROBE_CAPABILITY_ENV, None)
    descriptor = None
    if raw_descriptor is not None:
        try:
            descriptor = int(raw_descriptor)
        except ValueError:
            descriptor = None
    try:
        preflight = active_preflight(expected_artifact_lock_sha256)
        if not preflight["all_checks_pass"]:
            raise RuntimeErrorClosed("live runtime admission failed")
        if preflight["admission_stamp_valid"]:
            return preflight
        if (
            descriptor is None
            or descriptor < 3
            or operation is None
            or request is None
            or (
                operation == "private.grade"
                and descriptor
                in {
                    request.get("metric_fd"),
                    request.get("answer_fd"),
                    request.get("submission_fd"),
                }
            )
            or not _probe_capability_valid(
                descriptor,
                operation,
                request,
                preflight,
                expected_artifact_lock_sha256,
            )
        ):
            raise RuntimeErrorClosed("live runtime admission failed")
        return preflight
    finally:
        if descriptor is not None and descriptor >= 3:
            try:
                os.close(descriptor)
            except OSError:
                pass

def _safe_hash(path):
    try:
        return sha256_file(path)
    except OSError:
        return None

def artifact_identity(expected_artifact_lock_sha256=None):
    return {
        "supervisor_sha256": _safe_hash(SUPERVISOR),
        "python_wrapper_sha256": _safe_hash(PYTHON_WRAPPER),
        "fit_hook_sha256": _safe_hash(FIT_HOOK),
        "artifact_lock_sha256": _safe_hash(ARTIFACT_LOCK),
        "artifact_lock_expected_sha256": expected_artifact_lock_sha256,
        "rootfs_tree_lock_sha256": _safe_hash(ROOTFS_TREE_LOCK),
        "verification_wrapper_sha256": _safe_hash(
            os.path.join(SCRIPT_ROOT, "verify_installation.sh")
        ),
        "install_bundle_sha256": _safe_hash(
            os.path.join(SCRIPT_ROOT, "install_bundle.sh")
        ),
        "remote_cleanup_sha256": _safe_hash(
            os.path.join(SCRIPT_ROOT, "remote_cleanup.sh")
        ),
        "build_bundle_sha256": _safe_hash(
            os.path.join(SCRIPT_ROOT, "build_bundle.sh")
        ),
        "public_runner_sha256": _safe_hash(PUBLIC_RUNNER),
        "private_runner_sha256": _safe_hash(PRIVATE_RUNNER),
    }

def ensure_runtime_directories(deadline=None):

    for path in (SCRATCH, RUN_ROOT, STATE_ROOT, PUBLIC_WORKSPACE_ROOT):
        check_deadline(deadline, "runtime directory setup")
        if os.path.lexists(path) and (os.path.islink(path) or not os.path.isdir(path)):
            raise RuntimeErrorClosed("runtime directory is unsafe")
        try:
            os.makedirs(path, 0o700)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise RuntimeErrorClosed("cannot create runtime directory") from exc
        if os.path.islink(path) or not os.path.isdir(path):
            raise RuntimeErrorClosed("runtime directory is unsafe")
        os.chmod(path, 0o700)

def decode_mount_field(value):
    return (
        value.replace("\\040", " ")
        .replace("\\011", "\t")
        .replace("\\012", "\n")
        .replace("\\134", "\\")
    )

def exact_mount(
    path, required=True, deadline=None, require_filesystem_root=True
):
    check_deadline(deadline, "mount inspection")
    target = os.path.realpath(path)
    matches = []
    subordinate = []
    try:
        with open("/proc/self/mountinfo", "r") as handle:
            for line in handle:
                check_deadline(deadline, "mount inspection")
                fields = line.rstrip("\n").split()
                if "-" not in fields or len(fields) < 10:
                    continue
                split = fields.index("-")
                if split + 3 >= len(fields):
                    continue
                mountpoint = os.path.normpath(decode_mount_field(fields[4]))
                if not mountpoint.startswith("/"):
                    raise RuntimeErrorClosed("mount table contains a relative mountpoint")
                try:
                    inside = os.path.commonpath((mountpoint, target)) == target
                except ValueError:
                    inside = False
                if not inside:
                    continue
                record = {
                    "mount_id": fields[0],
                    "parent_mount_id": fields[1],
                    "major_minor": fields[2],
                    "root": decode_mount_field(fields[3]),
                    "mountpoint": mountpoint,
                    "mount_options": sorted(set(fields[5].split(","))),
                    "fstype": fields[split + 1],
                    "super_options": sorted(set(fields[split + 3].split(","))),
                }
                if mountpoint == target:
                    matches.append(record)
                else:
                    subordinate.append(record)
    except OSError as exc:
        raise RuntimeErrorClosed("mount table is unreadable") from exc
    if subordinate:
        raise RuntimeErrorClosed("workspace contains a subordinate mount")
    if not matches and not required:
        return None
    if len(matches) != 1:
        raise RuntimeErrorClosed("workspace must be one exact dedicated mount")
    if require_filesystem_root and matches[0]["root"] != "/":
        raise RuntimeErrorClosed("workspace mount is not the filesystem root")
    return matches[0]

def validate_public_workspace(workspace, require_writable=True, deadline=None):
    check_deadline(deadline, "workspace validation")
    if not isinstance(workspace, str) or not workspace.startswith("/"):
        raise RuntimeErrorClosed("workspace must be absolute")
    normalized = os.path.normpath(workspace)
    if normalized != workspace or os.path.islink(workspace) or not os.path.isdir(workspace):
        raise RuntimeErrorClosed("workspace path is not canonical real directory")
    real = os.path.realpath(workspace)
    root = os.path.realpath(PUBLIC_WORKSPACE_ROOT)
    try:
        inside = os.path.commonpath((real, root)) == root
    except ValueError:
        inside = False
    if not inside or real == root:
        raise RuntimeErrorClosed("workspace lies outside the configured owned root")
    mount = exact_mount(real, deadline=deadline)
    if mount["fstype"] != "tmpfs":
        raise RuntimeErrorClosed("workspace must be a dedicated tmpfs")
    options = set(mount["mount_options"]) | set(mount["super_options"])
    for required in ("noexec", "nosuid", "nodev"):
        if required not in options:
            raise RuntimeErrorClosed("workspace mount lacks " + required)
    if require_writable and "rw" not in options:
        raise RuntimeErrorClosed("active workspace is not writable")
    fs = os.statvfs(real)
    capacity = fs.f_frsize * fs.f_blocks
    if capacity <= 0 or capacity > PUBLIC_LIMITS["workspace_bytes"]:
        raise RuntimeErrorClosed("workspace capacity exceeds frozen cap")
    if fs.f_files > PUBLIC_LIMITS["max_files"] + 1024:
        raise RuntimeErrorClosed("workspace inode capacity exceeds frozen cap")
    scan_workspace(real, PUBLIC_LIMITS, deadline=deadline)
    check_deadline(deadline, "workspace validation")
    info = os.stat(real)
    return {
        "path": real,
        "device": int(info.st_dev),
        "inode": int(info.st_ino),
        "mount": mount,
    }

def scan_workspace(workspace, limits, deadline=None):
    total = 0
    count = 0
    maximum = 0
    for root, directories, files in os.walk(workspace, topdown=True, followlinks=False):
        check_deadline(deadline, "workspace scan")
        for name in list(directories):
            check_deadline(deadline, "workspace scan")
            path = os.path.join(root, name)
            info = os.lstat(path)
            if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
                raise RuntimeErrorClosed("workspace contains unsafe directory entry")
        for name in files:
            check_deadline(deadline, "workspace scan")
            path = os.path.join(root, name)
            info = os.lstat(path)
            if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
                raise RuntimeErrorClosed("workspace contains non-independent file")
            count += 1
            total += info.st_size
            maximum = max(maximum, info.st_size)
            if info.st_size > limits["max_file_bytes"]:
                raise RuntimeErrorClosed("regular-file cap exceeded")
            if count > limits["max_files"] or total > limits["workspace_bytes"]:
                raise RuntimeErrorClosed("workspace capacity cap exceeded")
    check_deadline(deadline, "workspace scan")
    fs = os.statvfs(workspace)
    return {
        "file_count": count,
        "total_bytes": total,
        "max_file_bytes": maximum,
        "free_bytes": fs.f_bavail * fs.f_frsize,
        "capacity_bytes": fs.f_blocks * fs.f_frsize,
    }

def _write_text(path, value, deadline=None):
    check_deadline(deadline, "cgroup setup")
    with open(path, "w") as handle:
        handle.write(str(value))
    check_deadline(deadline, "cgroup setup")

def _read_int(path):
    try:
        with open(path, "r") as handle:
            return int(handle.read().strip())
    except (OSError, ValueError) as exc:
        raise RuntimeErrorClosed("cgroup counter is unreadable") from exc

def _read_key_values(path):
    result = {}
    try:
        with open(path, "r") as handle:
            for line in handle:
                parts = line.split()
                if len(parts) != 2:
                    raise RuntimeErrorClosed("cgroup event counter is malformed")
                try:
                    result[parts[0]] = int(parts[1])
                except ValueError as exc:
                    raise RuntimeErrorClosed("cgroup event counter is malformed") from exc
    except OSError as exc:
        raise RuntimeErrorClosed("cgroup event counter is unreadable") from exc
    return result

def _unshare_mount_namespace(deadline=None):
    check_deadline(deadline, "mount namespace setup")
    libc = ctypes.CDLL(None, use_errno=True)
    if libc.unshare(CLONE_NEWNS) != 0:
        code = ctypes.get_errno()
        raise RuntimeErrorClosed("cannot create private mount namespace: " + os.strerror(code))
    run_checked(["/usr/bin/mount", "--make-rprivate", "/"], deadline=deadline)

def _verification_limit(name, frozen):
    if os.environ.get("OPENMLE_EXACT_VERIFICATION_MODE") != "1":
        return frozen
    raw = os.environ.get(name)
    if not raw:
        return frozen
    try:
        value = int(raw)
    except ValueError:
        raise RuntimeErrorClosed("invalid verification-only limit")
    if value <= 0 or value > frozen:
        raise RuntimeErrorClosed("verification limit weakens frozen cap")
    return value

def check_deadline(deadline, label="operation"):
    if deadline is not None and time.monotonic() >= deadline:
        raise RuntimeErrorClosed(label + " deadline expired")

def remaining_seconds(deadline, label="operation"):
    if deadline is None:
        return None
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise RuntimeErrorClosed(label + " deadline expired")
    return remaining

def run_checked(argv, deadline=None, **kwargs):
    timeout = remaining_seconds(deadline, "subprocess")
    try:
        return subprocess.run(argv, timeout=timeout, check=True, **kwargs)
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        raise RuntimeErrorClosed("bounded subprocess failed") from exc

def _create_cgroups(
    run_dir,
    cpu_vcpus,
    memory_bytes,
    max_processes,
    managed_ms,
    name,
    deadline=None,
    mounts=None,
    children=None,
):
    _unshare_mount_namespace(deadline=deadline)
    mounts = {} if mounts is None else mounts
    children = {} if children is None else children
    cgroup_root = os.path.join(run_dir, "cgroup")
    check_deadline(deadline, "cgroup setup")
    os.makedirs(cgroup_root)
    safe_name = "".join(character for character in name if character.isalnum() or character == "-")
    safe_name = safe_name[:48]
    for controller in CONTROLLERS:
        check_deadline(deadline, "cgroup setup")
        source = os.path.join("/sys/fs/cgroup", controller)
        destination = os.path.join(cgroup_root, controller.replace(",", "_"))
        os.makedirs(destination)

        mounts[controller] = destination
        run_checked(
            ["/usr/bin/mount", "--bind", source, destination],
            deadline=deadline,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        run_checked(
            ["/usr/bin/mount", "-o", "remount,rw,bind", destination],
            deadline=deadline,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        child = os.path.join(destination, safe_name + "-" + uuid.uuid4().hex[:12])
        os.mkdir(child, 0o700)
        children[controller] = child

    cpu = children["cpu,cpuacct"]
    _write_text(os.path.join(cpu, "cpu.cfs_period_us"), 100000, deadline)
    _write_text(os.path.join(cpu, "cpu.cfs_quota_us"), cpu_vcpus * 100000, deadline)

    effective_memory = _verification_limit("OPENMLE_TEST_MEMORY_BYTES", memory_bytes)
    memory = children["memory"]
    _write_text(os.path.join(memory, "memory.limit_in_bytes"), effective_memory, deadline)
    _write_text(
        os.path.join(memory, "memory.memsw.limit_in_bytes"), effective_memory, deadline
    )
    _write_text(os.path.join(memory, "memory.swappiness"), 0, deadline)

    effective_processes = _verification_limit("OPENMLE_TEST_MAX_PROCESSES", max_processes)
    _write_text(
        os.path.join(children["pids"], "pids.max"), effective_processes, deadline
    )
    return mounts, children, {
        "memory_bytes": effective_memory,
        "max_processes": effective_processes,
        "managed_runtime_ms": _verification_limit("OPENMLE_TEST_MANAGED_RUNTIME_MS", managed_ms),
    }

def _cgroup_pids(children):
    path = os.path.join(children["pids"], "cgroup.procs")
    result = []
    try:
        with open(path, "r") as handle:
            for line in handle:
                try:
                    pid = int(line.strip())
                except ValueError as exc:
                    raise RuntimeErrorClosed("cgroup membership is malformed") from exc
                if pid > 1 and pid != os.getpid():
                    result.append(pid)
    except OSError as exc:
        raise RuntimeErrorClosed("cgroup membership is unreadable") from exc
    return sorted(set(result))

def _kill_cgroup(children, exclude_pids=(), deadline=None):
    excluded = set(exclude_pids)
    killed = []
    for _ in range(30):
        check_deadline(deadline, "cgroup reap")
        pids = [pid for pid in _cgroup_pids(children) if pid not in excluded]
        if not pids:
            break
        for pid in pids:
            try:
                os.kill(pid, signal.SIGKILL)
                killed.append(pid)
            except OSError:
                pass
        time.sleep(0.02)
    return sorted(set(killed))

def _same_executable(pid, path):
    try:
        expected = os.stat(path)
        actual = os.stat("/proc/%d/exe" % pid)
    except OSError:
        return False
    return expected.st_dev == actual.st_dev and expected.st_ino == actual.st_ino

def _trusted_runtime_pids(children, launcher_pid):
    result = {launcher_pid}
    for pid in _cgroup_pids(children):
        if _same_executable(pid, SUPERVISOR):
            result.add(pid)
    return result

def _cgroup_stats(children):
    cpu = children["cpu,cpuacct"]
    memory = children["memory"]
    pids = children["pids"]
    oom = _read_key_values(os.path.join(memory, "memory.oom_control"))
    pid_events = _read_key_values(os.path.join(pids, "pids.events"))
    if "oom_kill" not in oom or "max" not in pid_events:
        raise RuntimeErrorClosed("required cgroup event counter is absent")
    return {
        "cpu_usage_ns": _read_int(os.path.join(cpu, "cpuacct.usage")),
        "memory_peak_bytes": _read_int(os.path.join(memory, "memory.max_usage_in_bytes")),
        "memory_failcnt": _read_int(os.path.join(memory, "memory.failcnt")),
        "oom_kill_count": oom.get("oom_kill", 0),
        "pids_max_events": pid_events.get("max", 0),
    }

def _cleanup_cgroups(mounts, children, deadline=None):
    failures = []
    has_membership = "pids" in children
    if has_membership:
        _kill_cgroup(children, deadline=deadline)
        remaining = _cgroup_pids(children)
        if remaining:
            failures.append("live_cgroup_processes")
    for controller in reversed(CONTROLLERS):
        child = children.get(controller)
        if child:
            removed = False
            for _ in range(30):
                check_deadline(deadline, "cgroup cleanup")
                try:
                    os.rmdir(child)
                    removed = True
                    break
                except OSError as exc:
                    if exc.errno not in (errno.EBUSY, errno.ENOTEMPTY):
                        failures.append("cgroup_rmdir:%s:%s" % (controller, exc.errno))
                        break
                    if has_membership:
                        _kill_cgroup(children, deadline=deadline)
                    time.sleep(0.02)
            if not removed and not any(
                item.startswith("cgroup_rmdir:%s:" % controller) for item in failures
            ):
                failures.append("cgroup_not_empty:" + controller)
        mountpoint = mounts.get(controller)
        if mountpoint:
            try:

                mounted = exact_mount(
                    mountpoint,
                    required=False,
                    deadline=deadline,
                    require_filesystem_root=False,
                )
            except RuntimeErrorClosed:
                failures.append("cgroup_mount_inspection:" + controller)
                mounted = None
            if mounted is not None:
                try:
                    run_checked(
                        ["/usr/bin/umount", mountpoint],
                        deadline=deadline,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                except RuntimeErrorClosed:
                    failures.append("cgroup_unmount:" + controller)
    if failures:
        raise RuntimeErrorClosed("cgroup cleanup failed: " + ",".join(failures))
    return {
        "processes_empty": True,
        "cgroups_removed": True,
        "mounts_unmounted": True,
    }

def _move_self_to_cgroups(children, deadline=None):
    os.setsid()
    pid = os.getpid()
    for controller in CONTROLLERS:
        _write_text(os.path.join(children[controller], "tasks"), pid, deadline)

def _parse_supervisor_stats(payload):
    try:
        value = strict_json_loads(payload.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        raise RuntimeErrorClosed("supervisor did not return strict JSON stats")
    if not isinstance(value, dict) or value.get("schema") != SUPERVISOR_SCHEMA:
        raise RuntimeErrorClosed("supervisor stats schema mismatch")
    for name in (
        "exit_code",
        "execution_attempt_delta",
        "execution_completed_delta",
        "nested_subprocess_delta",
        "fit_delta",
        "process_peak",
        "bytes_read",
        "bytes_written",
    ):
        item = value.get(name)
        if isinstance(item, bool) or not isinstance(item, int) or item < 0:
            raise RuntimeErrorClosed("invalid supervisor counter")
    managed = value.get("managed_runtime_wall_seconds")
    if not isinstance(managed, (int, float)) or not math.isfinite(float(managed)) or managed < 0:
        raise RuntimeErrorClosed("invalid supervisor timing")
    if value["execution_completed_delta"] > value["execution_attempt_delta"]:
        raise RuntimeErrorClosed("completed Python count exceeds attempts")
    return value

def _remove_tree_strict(path, deadline=None):
    if not os.path.lexists(path):
        return
    info = os.lstat(path)
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
        raise RuntimeErrorClosed("cleanup target is not a real directory")
    for current, directories, files in os.walk(path, topdown=False, followlinks=False):
        check_deadline(deadline, "tree cleanup")
        for name in files:
            check_deadline(deadline, "tree cleanup")
            os.unlink(os.path.join(current, name))
        for name in directories:
            check_deadline(deadline, "tree cleanup")
            child = os.path.join(current, name)
            if os.path.islink(child):
                os.unlink(child)
            else:
                os.rmdir(child)
    os.rmdir(path)
    if os.path.lexists(path):
        raise RuntimeErrorClosed("cleanup target remains after removal")

def _start_sandbox_watchdog(run_name):
    try:
        read_fd, write_fd = os.pipe()
    except OSError as exc:
        raise RuntimeErrorClosed("cannot create sandbox watchdog pipe") from exc
    try:
        pid = os.fork()
    except OSError as exc:
        os.close(read_fd)
        os.close(write_fd)
        raise RuntimeErrorClosed("cannot fork sandbox watchdog") from exc
    if pid == 0:
        os.close(write_fd)
        try:
            token = os.read(read_fd, 1)
        except OSError:
            token = b""
        os.close(read_fd)
        if token != b"N":
            watchdog_deadline = time.monotonic() + 2.0
            for _ in range(3):
                try:
                    receipt = reap_named_cgroups(run_name, deadline=watchdog_deadline)
                    directories_clean = cleanup_named_run_directories(
                        run_name, deadline=watchdog_deadline
                    )
                    if (
                        receipt.get("child_exit_zero") is True
                        and not receipt.get("failures")
                        and directories_clean
                        and residue_is_zero(
                            residue_snapshot(run_name, deadline=watchdog_deadline)
                        )
                    ):
                        break
                except BaseException:
                    pass
                if time.monotonic() >= watchdog_deadline:
                    break
                time.sleep(0.05)
        os._exit(0)
    os.close(read_fd)
    return pid, write_fd

def run_sandbox(
    workspace,
    command,
    timeout_ms,
    cpu_vcpus,
    memory_bytes,
    max_processes,
    managed_ms,
    max_open_files,
    max_file_bytes,
    output_cap,
    run_name,
    deadline=None,
):

    started = time.monotonic()
    setup_deadline = started + SANDBOX_SETUP_GRACE_SECONDS
    if deadline is not None:
        setup_deadline = min(deadline, setup_deadline)
    operation_deadline = setup_deadline
    execution_deadline = None
    run_dir = None
    mounts = {}
    children = {}
    process = None
    stats_read = None
    stats_write = None
    stdout = bytearray()
    stderr = bytearray()
    stats_payload = bytearray()
    killed_for_output = False
    killed_for_timeout = False
    background_pids = []
    before_stats = None
    final_stats = None
    watchdog_pid = None
    watchdog_write = None
    cleanup_complete = False
    cleanup_error = None
    cleanup_error_phase = None
    cleanup_phase = None
    selector = None
    result = None
    primary_error = None
    phase = "runtime_directory_setup"
    try:
        if type(timeout_ms) is not int or timeout_ms <= 0:
            raise RuntimeErrorClosed("sandbox timeout must be a positive integer")
        ensure_runtime_directories(deadline=setup_deadline)
        check_deadline(setup_deadline, "sandbox setup")

        phase = "run_directory_setup"
        run_dir = os.path.join(RUN_ROOT, run_name + "-" + uuid.uuid4().hex)
        os.makedirs(run_dir, 0o700)

        phase = "watchdog_setup"
        watchdog_pid, watchdog_write = _start_sandbox_watchdog(run_name)

        phase = "cgroup_setup"
        mounts, children, effective = _create_cgroups(
            run_dir,
            cpu_vcpus,
            memory_bytes,
            max_processes,
            managed_ms,
            "openmle-" + run_name,
            deadline=setup_deadline,
            mounts=mounts,
            children=children,
        )
        check_deadline(setup_deadline, "sandbox setup")

        phase = "initial_accounting"
        before_stats = _cgroup_stats(children)

        phase = "supervisor_pipe_setup"
        stats_read, stats_write = os.pipe()
        os.set_inheritable(stats_write, True)
        argv = [
            "/usr/bin/unshare",
            "--mount",
            "--ipc",
            "--net",
            "--pid",
            "--fork",
            SUPERVISOR,
            "--rootfs",
            ROOTFS,
            "--workspace",
            workspace,
            "--run-dir",
            run_dir,
            "--wrapper",
            PYTHON_WRAPPER,
            "--fit-hook",
            FIT_HOOK,
            "--stats-fd",
            str(stats_write),
            "--real-python",
            "/opt/miniconda3/envs/testbed/bin/python3.10",
            "--managed-ms",
            str(effective["managed_runtime_ms"]),
            "--max-open-files",
            str(max_open_files),
            "--max-file-bytes",
            str(max_file_bytes),
        ]
        argv.extend(["--command", command])

        phase = "command_budget_setup"
        check_deadline(setup_deadline, "sandbox setup")
        command_started = time.monotonic()
        execution_deadline = command_started + timeout_ms / 1000.0
        if deadline is not None and deadline <= execution_deadline:
            raise RuntimeErrorClosed(
                "caller deadline cannot preserve the requested command timeout"
            )
        operation_deadline = execution_deadline + SANDBOX_OPERATION_GRACE_SECONDS
        if deadline is not None:
            operation_deadline = min(deadline, operation_deadline)

        phase = "supervisor_spawn"
        process = subprocess.Popen(
            argv,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=True,
            pass_fds=(stats_write,),
            preexec_fn=lambda: _move_self_to_cgroups(children, execution_deadline),
            env={"PATH": "/usr/bin:/bin", "LC_ALL": "C"},
        )
        os.close(stats_write)
        stats_write = None

        phase = "command_execution"
        selector = selectors.DefaultSelector()
        streams = {
            process.stdout.fileno(): (process.stdout, stdout),
            process.stderr.fileno(): (process.stderr, stderr),
            stats_read: (stats_read, stats_payload),
        }
        for descriptor, pair in streams.items():
            os.set_blocking(descriptor, False)
            selector.register(descriptor, selectors.EVENT_READ, pair)
        effective_output_cap = _verification_limit("OPENMLE_TEST_OUTPUT_BYTES", output_cap)
        while selector.get_map():
            now = time.monotonic()
            if now >= operation_deadline:
                raise RuntimeErrorClosed("sandbox pipe drain deadline expired")
            if now >= execution_deadline and not killed_for_timeout:
                launcher_alive = process.poll() is None
                residual = _cgroup_pids(children)
                if launcher_alive or residual:
                    killed_for_timeout = launcher_alive
                    _kill_cgroup(
                        children,
                        _trusted_runtime_pids(children, process.pid),
                        deadline=operation_deadline,
                    )
            next_deadline = (
                execution_deadline
                if time.monotonic() < execution_deadline
                else operation_deadline
            )
            wait = max(0.0, min(0.05, next_deadline - time.monotonic()))
            for key, _mask in selector.select(wait):
                descriptor = key.fd
                _stream, target = key.data
                try:
                    chunk = os.read(descriptor, 65536)
                except OSError as exc:
                    if exc.errno in (errno.EAGAIN, errno.EWOULDBLOCK):
                        continue
                    chunk = b""
                if not chunk:
                    selector.unregister(descriptor)
                    continue
                target.extend(chunk)
                if (
                    target is not stats_payload
                    and len(stdout) + len(stderr) > effective_output_cap
                    and not killed_for_output
                ):
                    killed_for_output = True
                    _kill_cgroup(
                        children,
                        _trusted_runtime_pids(children, process.pid),
                        deadline=operation_deadline,
                    )

        phase = "supervisor_wait"
        try:
            process.wait(
                timeout=min(1.0, remaining_seconds(operation_deadline, "sandbox wait"))
            )
        except subprocess.TimeoutExpired:
            _kill_cgroup(children, deadline=operation_deadline)
            process.wait(
                timeout=min(1.0, remaining_seconds(operation_deadline, "sandbox wait"))
            )

        phase = "background_reap"
        background_pids = _cgroup_pids(children)
        if background_pids:
            _kill_cgroup(children, deadline=operation_deadline)

        phase = "final_accounting"
        check_deadline(operation_deadline, "sandbox accounting")
        final_stats = _cgroup_stats(children)
        supervisor = _parse_supervisor_stats(bytes(stats_payload))

        memory_failures = final_stats["memory_failcnt"] - before_stats["memory_failcnt"]
        oom_kills = final_stats["oom_kill_count"] - before_stats["oom_kill_count"]
        pid_events = final_stats["pids_max_events"] - before_stats["pids_max_events"]
        failure_class = None
        timed_out = False
        if killed_for_output:
            failure_class = "output_limit"
        elif killed_for_timeout:
            failure_class = "wall_timeout"
            timed_out = True
        elif supervisor.get("security_violation") is True:
            failure_class = "security_violation"
        elif supervisor.get("managed_runtime_limit") is True:
            failure_class = "managed_runtime_limit"
        elif oom_kills > 0 or memory_failures > 0:
            failure_class = "memory_limit"
        elif pid_events > 0:
            failure_class = "pid_limit"
        elif supervisor.get("file_limit") is True:
            failure_class = "file_limit"
        elif supervisor.get("background_process") is True or background_pids:
            failure_class = "background_process"

        phase = "receipt_build"
        cpu_ns = max(0, final_stats["cpu_usage_ns"] - before_stats["cpu_usage_ns"])
        result = {
            "stdout": bytes(stdout),
            "stderr": bytes(stderr),
            "exit_code": supervisor["exit_code"],
            "timed_out": timed_out,
            "wall_seconds": max(0.0, time.monotonic() - started),
            "managed_runtime_wall_seconds": supervisor["managed_runtime_wall_seconds"],
            "cpu_seconds": cpu_ns / 1000000000.0,
            "peak_rss_bytes": final_stats["memory_peak_bytes"],
            "bytes_read": supervisor["bytes_read"],
            "bytes_written": supervisor["bytes_written"],
            "process_peak": supervisor["process_peak"],
            "execution_attempt_delta": supervisor["execution_attempt_delta"],
            "execution_completed_delta": supervisor["execution_completed_delta"],
            "nested_subprocess_delta": supervisor["nested_subprocess_delta"],
            "fit_delta": supervisor["fit_delta"],
            "failure_class": failure_class,
            "infrastructure_fault": False,
        }
    except BaseException as exc:
        if isinstance(exc, SandboxInfrastructureError):
            primary_error = exc
        else:
            primary_error = SandboxInfrastructureError(phase, exc)
    finally:
        cleanup_deadline = time.monotonic() + SANDBOX_CLEANUP_GRACE_SECONDS
        if deadline is not None:
            cleanup_deadline = min(deadline, cleanup_deadline)
        try:
            cleanup_phase = "selector_cleanup"
            if selector is not None:
                selector.close()
            cleanup_phase = "pipe_cleanup"
            if stats_write is not None:
                try:
                    os.close(stats_write)
                except OSError:
                    pass
            if stats_read is not None:
                try:
                    os.close(stats_read)
                except OSError:
                    pass
            cleanup_phase = "cgroup_cleanup"
            if mounts or children:
                _cleanup_cgroups(mounts, children, deadline=cleanup_deadline)
            cleanup_phase = "run_directory_cleanup"
            if run_dir is not None:
                _remove_tree_strict(run_dir, deadline=cleanup_deadline)
            cleanup_phase = "residue_verification"
            cleanup_complete = residue_is_zero(
                residue_snapshot(run_name, deadline=cleanup_deadline)
            )
            if not cleanup_complete:
                raise RuntimeErrorClosed("owned sandbox residue remains")
        except BaseException as exc:
            cleanup_error = exc
            cleanup_error_phase = cleanup_phase
        try:
            cleanup_phase = "watchdog_signal"
            if watchdog_write is not None:
                try:
                    if cleanup_complete:
                        os.write(watchdog_write, b"N")
                except OSError:
                    pass
                os.close(watchdog_write)
                watchdog_write = None
            cleanup_phase = "watchdog_wait"
            if watchdog_pid is not None:
                try:
                    while True:
                        waited, _status = os.waitpid(watchdog_pid, os.WNOHANG)
                        if waited == watchdog_pid:
                            break
                        check_deadline(cleanup_deadline, "sandbox watchdog")
                        time.sleep(0.01)
                except ChildProcessError:
                    pass
        except BaseException as exc:
            if cleanup_error is None:
                cleanup_error = exc
                cleanup_error_phase = cleanup_phase

    if cleanup_error is not None:
        prior_phase = primary_error.phase if primary_error is not None else None
        wrapped = SandboxInfrastructureError(
            cleanup_error_phase or "cleanup",
            cleanup_error,
            prior_phase=prior_phase,
        )
        raise wrapped from cleanup_error
    if primary_error is not None:
        raise primary_error from primary_error.original_cause
    if result is None:
        raise SandboxInfrastructureError(
            "receipt_build", RuntimeErrorClosed("sandbox returned no result")
        )
    return result

def residue_snapshot(run_fragment=None, deadline=None):

    errors = []
    processes = []
    try:
        proc_entries = _numeric_proc_entries()
    except RuntimeErrorClosed:
        proc_entries = []
        errors.append("proc_unreadable")
    for item in proc_entries:
        check_deadline(deadline, "residue scan")
        pid = int(item)
        try:
            with open("/proc/%d/cmdline" % pid, "rb") as handle:
                payload = handle.read(4097)
        except OSError as exc:
            if exc.errno in (errno.ENOENT, errno.ESRCH):
                continue
            errors.append("proc_cmdline_unreadable:%d" % pid)
            continue
        command = payload.replace(b"\0", b" ").decode("utf-8", "replace")
        owned = "openmle-sandbox-supervisor" in command or "/run/openmle-bin/" in command
        targeted = owned and (run_fragment is None or run_fragment in command)
        if not targeted:

            continue
        if len(payload) > 4096:
            errors.append("proc_cmdline_too_large:%d" % pid)
            continue
        processes.append({"pid": pid, "cmdline": command[:512]})
    mounts = []
    try:
        with open("/proc/self/mountinfo", "r") as handle:
            for line in handle:
                check_deadline(deadline, "residue scan")
                if SCRATCH + "/runs/" in line and (run_fragment is None or run_fragment in line):
                    mounts.append(line.rstrip("\n")[:1024])
    except OSError:
        errors.append("mountinfo_unreadable")
    cgroups = []
    for controller in CONTROLLERS:
        check_deadline(deadline, "residue scan")
        root = os.path.join("/sys/fs/cgroup", controller)
        try:
            for name in os.listdir(root):
                if name.startswith("openmle-") and (run_fragment is None or run_fragment in name):
                    cgroups.append(os.path.join(root, name))
        except OSError:
            errors.append("cgroup_root_unreadable:" + controller)
    runs = []
    try:
        for name in os.listdir(RUN_ROOT):
            if run_fragment is None or run_fragment in name:
                runs.append(name)
    except FileNotFoundError:
        pass
    except OSError:
        errors.append("run_root_unreadable")
    return {
        "errors": errors,
        "processes": processes,
        "mounts": mounts,
        "cgroups": cgroups,
        "run_entries": runs,
        "verification_lock_present": os.path.lexists("/tmp/camg-autoresearch/verification.lock"),
    }

def residue_is_zero(value):
    return not any(
        value.get(name)
        for name in ("errors", "processes", "mounts", "cgroups", "run_entries")
    )

def reap_named_cgroups(fragment, deadline=None):

    if not isinstance(fragment, str) or not fragment or any(
        character not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-"
        for character in fragment
    ):
        raise RuntimeErrorClosed("unsafe cgroup cleanup fragment")
    read_fd, write_fd = os.pipe()
    pid = os.fork()
    if pid == 0:
        os.close(read_fd)
        result = {"killed_pids": [], "removed": [], "failures": []}
        cleanup_root = None
        mounted = []
        try:
            check_deadline(deadline, "named cgroup reap")
            _unshare_mount_namespace(deadline=deadline)
            ensure_runtime_directories(deadline=deadline)
            cleanup_root = os.path.join(RUN_ROOT, "cleanup-" + uuid.uuid4().hex)
            os.makedirs(cleanup_root, 0o700)
            matches = []
            for controller in CONTROLLERS:
                source = os.path.join("/sys/fs/cgroup", controller)
                destination = os.path.join(cleanup_root, controller.replace(",", "_"))
                os.makedirs(destination)
                run_checked(
                    ["/usr/bin/mount", "--bind", source, destination],
                    deadline=deadline,
                )
                run_checked(
                    ["/usr/bin/mount", "-o", "remount,rw,bind", destination],
                    deadline=deadline,
                )
                mounted.append(destination)
                for name in os.listdir(destination):
                    path = os.path.join(destination, name)
                    if name.startswith("openmle-") and fragment in name and os.path.isdir(path):
                        matches.append(path)
            for _ in range(30):
                check_deadline(deadline, "named cgroup reap")
                live = []
                for path in matches:
                    try:
                        with open(os.path.join(path, "tasks"), "r") as handle:
                            live.extend(
                                int(line.strip()) for line in handle if line.strip()
                            )
                    except (OSError, ValueError) as exc:
                        raise RuntimeErrorClosed(
                            "named cgroup membership is unreadable"
                        ) from exc
                live = sorted(set(item for item in live if item > 1 and item != os.getpid()))
                if not live:
                    break
                for target in live:
                    try:
                        os.kill(target, signal.SIGKILL)
                        result["killed_pids"].append(target)
                    except OSError:
                        pass
                time.sleep(0.02)
            for path in matches:
                check_deadline(deadline, "named cgroup removal")
                try:
                    os.rmdir(path)
                    result["removed"].append(path)
                except OSError as exc:
                    result["failures"].append("%s:%s" % (path, exc.errno))
        except BaseException as exc:  
            result["failures"].append(type(exc).__name__)
        finally:
            for destination in reversed(mounted):
                try:
                    run_checked(
                        ["/usr/bin/umount", destination],
                        deadline=deadline,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                except RuntimeErrorClosed:
                    result["failures"].append("cleanup_bind_unmount")
            if cleanup_root:
                try:
                    _remove_tree_strict(cleanup_root, deadline=deadline)
                except RuntimeErrorClosed:
                    result["failures"].append("cleanup_root_removal")
        try:
            os.write(write_fd, canonical_json(result).encode("utf-8"))
        except OSError:
            pass
        os.close(write_fd)
        os._exit(0 if not result["failures"] else 1)
    os.close(write_fd)
    payload = bytearray()
    os.set_blocking(read_fd, False)
    selector = selectors.DefaultSelector()
    selector.register(read_fd, selectors.EVENT_READ)
    child_status = None
    eof = False
    timed_out = False
    while child_status is None or not eof:
        if deadline is not None and time.monotonic() >= deadline:
            timed_out = True
            try:
                os.kill(pid, signal.SIGKILL)
            except OSError:
                pass
            _waited, child_status = os.waitpid(pid, 0)
            break
        wait = 0.05
        if deadline is not None:
            wait = max(0.0, min(wait, deadline - time.monotonic()))
        for key, _mask in selector.select(wait):
            try:
                chunk = os.read(key.fd, 65536)
            except OSError as exc:
                if exc.errno in (errno.EAGAIN, errno.EWOULDBLOCK):
                    continue
                chunk = b""
            if chunk:
                payload.extend(chunk)
            else:
                eof = True
                selector.unregister(read_fd)
        if child_status is None:
            waited, status = os.waitpid(pid, os.WNOHANG)
            if waited == pid:
                child_status = status
    os.close(read_fd)
    selector.close()
    if child_status is None:
        _waited, child_status = os.waitpid(pid, 0)
    try:
        result = strict_json_loads(payload.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        result = {"killed_pids": [], "removed": [], "failures": ["invalid_cleanup_receipt"]}
    if timed_out:
        result.setdefault("failures", []).append("cleanup_deadline")
    result["child_exit_zero"] = os.WIFEXITED(child_status) and os.WEXITSTATUS(child_status) == 0
    return result

def cleanup_named_run_directories(fragment, deadline=None):

    if not isinstance(fragment, str) or not fragment or any(
        character not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-"
        for character in fragment
    ):
        raise RuntimeErrorClosed("unsafe run cleanup fragment")
    snapshot = residue_snapshot(fragment, deadline=deadline)
    if (
        snapshot["errors"]
        or snapshot["processes"]
        or snapshot["mounts"]
        or snapshot["cgroups"]
    ):
        return False
    root = os.path.realpath(RUN_ROOT)
    try:
        names = os.listdir(root)
    except FileNotFoundError:
        return True
    except OSError:
        return False
    for name in names:
        check_deadline(deadline, "run-directory cleanup")
        if fragment not in name:
            continue
        path = os.path.join(root, name)
        real = os.path.realpath(path)
        if (
            os.path.islink(path)
            or os.path.commonpath((real, root)) != root
            or not os.path.isdir(real)
        ):
            return False
        _remove_tree_strict(real, deadline=deadline)
    final = residue_snapshot(fragment, deadline=deadline)
    return not final["errors"] and not final["run_entries"]

def _numeric_proc_entries():
    try:
        return [name for name in os.listdir("/proc") if name.isdigit()]
    except OSError as exc:
        raise RuntimeErrorClosed("proc directory is unreadable") from exc
