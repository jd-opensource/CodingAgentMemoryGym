from __future__ import annotations

import copy
import concurrent.futures
import contextlib
import hashlib
import importlib.util
import json
import math
import os
import re
import stat
import subprocess
import sys
import tempfile
import time
import types
import unittest
from unittest import mock
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import adapter_fixture
import private_runner
import private_worker
import public_runner
import remote_probe
import runtime_common as common

TMP_PARENT = ROOT / "tests" / ".tmp"
TMP_PARENT.mkdir(mode=0o700, exist_ok=True)

def _schema_error(schema, instance, root, location="$"):
    if "$ref" in schema:
        reference = schema["$ref"]
        if not reference.startswith("#/"):
            return location + ": unsupported reference"
        target = root
        for part in reference[2:].split("/"):
            target = target[part.replace("~1", "/").replace("~0", "~")]
        return _schema_error(target, instance, root, location)

    expected_type = schema.get("type")
    if expected_type is not None:
        names = expected_type if isinstance(expected_type, list) else [expected_type]

        def matches(name):
            if name == "null":
                return instance is None
            if name == "boolean":
                return type(instance) is bool
            if name == "integer":
                return isinstance(instance, int) and not isinstance(instance, bool)
            if name == "number":
                return (
                    isinstance(instance, (int, float))
                    and not isinstance(instance, bool)
                    and math.isfinite(float(instance))
                )
            if name == "string":
                return isinstance(instance, str)
            if name == "array":
                return isinstance(instance, list)
            if name == "object":
                return isinstance(instance, dict)
            return False

        if not any(matches(name) for name in names):
            return location + ": type mismatch"

    if "const" in schema and instance != schema["const"]:
        return location + ": const mismatch"
    if "enum" in schema and instance not in schema["enum"]:
        return location + ": enum mismatch"

    if isinstance(instance, dict):
        required = set(schema.get("required", []))
        if not required.issubset(instance):
            return location + ": missing required property"
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extras = set(instance) - set(properties)
            if extras:
                return location + ": additional property"
        for name, value in instance.items():
            if name in properties:
                error = _schema_error(
                    properties[name], value, root, location + "/" + name
                )
                if error:
                    return error

    if isinstance(instance, list):
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            return location + ": too many items"
        if schema.get("uniqueItems") and len(
            {common.canonical_json(item) for item in instance}
        ) != len(instance):
            return location + ": duplicate item"
        if "items" in schema:
            for index, value in enumerate(instance):
                error = _schema_error(
                    schema["items"], value, root, location + "/" + str(index)
                )
                if error:
                    return error

    if isinstance(instance, str):
        if "minLength" in schema and len(instance) < schema["minLength"]:
            return location + ": string too short"
        if "maxLength" in schema and len(instance) > schema["maxLength"]:
            return location + ": string too long"
        if "pattern" in schema and re.search(schema["pattern"], instance) is None:
            return location + ": pattern mismatch"

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            return location + ": below minimum"
        if "maximum" in schema and instance > schema["maximum"]:
            return location + ": above maximum"

    for condition in schema.get("allOf", []):
        error = _schema_error(condition, instance, root, location)
        if error:
            return error
    if "if" in schema:
        matched = _schema_error(schema["if"], instance, root, location) is None
        branch = schema.get("then" if matched else "else")
        if branch is not None:
            error = _schema_error(branch, instance, root, location)
            if error:
                return error
    return None

def schema_accepts(schema, instance):
    return _schema_error(schema, instance, schema) is None

class ProtocolTests(unittest.TestCase):
    def test_monotonic_ns_falls_back_on_python36(self) -> None:
        with (
            mock.patch.object(common.time, "monotonic_ns", None, create=True),
            mock.patch.object(common.time, "monotonic", return_value=12.5),
        ):
            self.assertEqual(common.monotonic_ns(), 12_500_000_000)

    def _probe_capability_fixture(self, request):
        now = 12_000_000_000
        parent_pid = os.getppid()
        parent_start_ticks = 123456
        session = {"probe_session_id": "a" * 32}
        artifact_identity = {"fixture": "artifact-v1"}
        rootfs_identity = {"schema": "fixture_rootfs_v1", "valid": True}
        expected_lock = hashlib.sha256(
            (ROOT / "artifact-lock.json").read_bytes()
        ).hexdigest()
        capability = {
            "schema": common.PROBE_CAPABILITY_SCHEMA,
            "capability_id": "b" * 32,
            "probe_session_id": session["probe_session_id"],
            "boot_id": "fixture-boot",
            "kernel_release": os.uname()[2],
            "artifact_identity": artifact_identity,
            "artifact_lock_sha256": expected_lock,
            "rootfs_identity_sha256": common.canonical_sha256(rootfs_identity),
            "operation": "public.execute",
            "request_sha256": common.canonical_sha256(request),
            "parent_pid": parent_pid,
            "parent_start_ticks": parent_start_ticks,
            "issued_monotonic_ns": now - 1_000_000,
            "expires_monotonic_ns": now + 1_000_000,
        }
        preflight = {
            "all_checks_pass": True,
            "admission_stamp_valid": False,
            "rootfs_identity": rootfs_identity,
        }
        dependencies = {
            "now": now,
            "parent_pid": parent_pid,
            "parent_start_ticks": parent_start_ticks,
            "session": session,
            "artifact_identity": artifact_identity,
            "rootfs_identity": rootfs_identity,
            "expected_lock": expected_lock,
            "preflight": preflight,
            "capability": capability,
        }
        return dependencies

    def test_all_schema_json_reparses(self) -> None:
        schemas = sorted((ROOT / "schemas").glob("*.json"))
        self.assertEqual(len(schemas), 7)
        for path in schemas:
            with self.subTest(path=path.name):
                value = json.loads(path.read_text())
                self.assertEqual(value["type"], "object")
                self.assertIn("$id", value)

    def test_emitted_instances_validate_against_schemas(self) -> None:
        public_request = {
            "schema": public_runner.REQUEST_SCHEMA,
            "workspace": common.PUBLIC_WORKSPACE_ROOT + "/schema-fixture",
            "command": "python -c 'print(1)'",
            "timeout_ms": 1000,
            "managed_runtime_budget_ms": 750,
        }
        private_request = {
            "schema": private_runner.REQUEST_SCHEMA,
            "task_id": "schema-fixture",
            "grader_binding_sha256": "1" * 64,
            "package_identity_sha256": "2" * 64,
            "metric_sha256": "3" * 64,
            "answer_sha256": "4" * 64,
            "submission_sha256": "5" * 64,
            "higher_is_better": True,
            "validator_success_forms": [],
            "metric_fd": 3,
            "answer_fd": 4,
            "submission_fd": 5,
            "timeout_ms": 1000,
        }
        instances = {
            "public-runner-metadata.schema.json": [public_runner.metadata()],
            "private-runner-metadata.schema.json": [private_runner.metadata()],
            "public-runner-request.schema.json": [public_request],
            "private-runner-request.schema.json": [private_request],
            "public-runner-receipt.schema.json": [
                public_runner.infrastructure_receipt()
            ],
            "public-runner-lifecycle.schema.json": [
                public_runner.lifecycle_failure("freeze"),
                public_runner._lifecycle_receipt(
                    "teardown", True, True, False, True, None
                ),
            ],
            "private-runner-result.schema.json": [
                private_runner.infrastructure_result(False),
                {
                    "schema": private_runner.RESULT_SCHEMA,
                    "classification": "invalid_submission",
                    "native_score": None,
                    "higher_is_better": True,
                },
                {
                    "schema": private_runner.RESULT_SCHEMA,
                    "classification": "graded",
                    "native_score": 0.25,
                    "higher_is_better": True,
                },
            ],
        }
        for name, values in instances.items():
            schema = json.loads((ROOT / "schemas" / name).read_text())
            for index, value in enumerate(values):
                with self.subTest(schema=name, index=index):
                    self.assertIsNone(_schema_error(schema, value, schema))

    def test_private_result_schema_binds_classification_to_score(self) -> None:
        schema = json.loads(
            (ROOT / "schemas" / "private-runner-result.schema.json").read_text()
        )
        base = {
            "schema": private_runner.RESULT_SCHEMA,
            "classification": "graded",
            "native_score": 1.0,
            "higher_is_better": True,
        }
        self.assertTrue(schema_accepts(schema, base))
        self.assertFalse(schema_accepts(schema, dict(base, native_score=None)))
        self.assertFalse(
            schema_accepts(
                schema,
                dict(base, classification="invalid_submission", native_score=1.0),
            )
        )
        self.assertFalse(
            schema_accepts(
                schema,
                dict(base, classification="infrastructure_fault", native_score=1.0),
            )
        )

    def test_rootfs_lock_is_verified_and_content_complete(self) -> None:
        with tempfile.TemporaryDirectory(dir=TMP_PARENT) as raw:
            lock_path = Path(raw) / "rootfs-tree-lock.json"
            lock_path.write_text(
                common.canonical_json(
                    {
                        "schema": "openmle_fast_rootfs_tree_lock_v2",
                        "runtime_digest": common.RUNTIME_DIGEST,
                        "algorithm": common.ROOTFS_TREE_ALGORITHM,
                        "tree_sha256": None,
                        "python_path": common.ROOTFS_PYTHON_PATH,
                        "python_sha256": None,
                        "regular_files": 1,
                        "bytes": 1,
                        "status": "unverified_authorized_pod_unavailable",
                    }
                )
                + "\n"
            )
            with mock.patch.object(common, "ROOTFS_TREE_LOCK", str(lock_path)):
                self.assertIsNone(common.load_rootfs_tree_lock())
                identity = common.rootfs_identity()
            self.assertFalse(identity["valid"])
            self.assertIsNone(identity["tree_measurement"])

    def test_rootfs_tree_measurement_covers_nested_content_and_python(self) -> None:
        with tempfile.TemporaryDirectory(dir=TMP_PARENT) as raw:
            root = Path(raw) / "rootfs"
            python = root / "opt" / "python"
            nested = root / "data" / "nested.txt"
            python.parent.mkdir(parents=True)
            nested.parent.mkdir(parents=True)
            python.write_bytes(b"python-v1")
            nested.write_bytes(b"payload-v1")
            first = common.measure_rootfs_tree(
                str(root), "opt/python", time.monotonic() + 2.0
            )
            lock = dict(first)
            lock.pop("schema")
            self.assertTrue(common._rootfs_measurement_matches_lock(first, lock))
            self.assertFalse(
                common._rootfs_measurement_matches_lock(
                    first, dict(lock, tree_sha256="0" * 64)
                )
            )
            self.assertFalse(
                common._rootfs_measurement_matches_lock(
                    first, dict(lock, python_sha256="0" * 64)
                )
            )
            nested.write_bytes(b"payload-v2")
            second = common.measure_rootfs_tree(
                str(root), "opt/python", time.monotonic() + 2.0
            )
            self.assertNotEqual(first["tree_sha256"], second["tree_sha256"])
            self.assertEqual(first["python_sha256"], second["python_sha256"])
            python.write_bytes(b"python-v2")
            third = common.measure_rootfs_tree(
                str(root), "opt/python", time.monotonic() + 2.0
            )
            self.assertNotEqual(second["python_sha256"], third["python_sha256"])

    def test_rootfs_tree_measurement_obeys_deadline(self) -> None:
        with tempfile.TemporaryDirectory(dir=TMP_PARENT) as raw:
            root = Path(raw) / "rootfs"
            python = root / "opt" / "python"
            python.parent.mkdir(parents=True)
            python.write_bytes(b"python")
            with self.assertRaises(common.RuntimeErrorClosed):
                common.measure_rootfs_tree(
                    str(root), "opt/python", time.monotonic() - 1.0
                )

    def test_workspace_mount_rejects_bind_subroot_and_subordinate_mount(self) -> None:
        workspace = "/owned/workspace"
        exact = "31 20 0:41 / %s rw,noexec,nosuid,nodev - tmpfs tmpfs rw\n" % workspace
        bind_subroot = (
            "31 20 0:41 /subdir %s rw,noexec,nosuid,nodev - tmpfs tmpfs rw\n"
            % workspace
        )
        nested = (
            exact
            + "32 31 0:42 / %s/nested rw,noexec,nosuid,nodev - tmpfs tmpfs rw\n"
            % workspace
        )
        for payload in (bind_subroot, nested):
            with self.subTest(payload=payload):
                with mock.patch("builtins.open", mock.mock_open(read_data=payload)):
                    with self.assertRaises(common.RuntimeErrorClosed):
                        common.exact_mount(workspace)

    def test_workspace_bind_is_plain_not_recursive(self) -> None:
        source = (ROOT / "sandbox_supervisor.c").read_text()
        self.assertIn(
            "mount(cfg->workspace, workspace, NULL, MS_BIND, NULL)", source
        )
        self.assertNotIn(
            "mount(cfg->workspace, workspace, NULL, MS_BIND | MS_REC, NULL)",
            source,
        )

    def test_residue_uncertainty_fails_closed(self) -> None:
        with mock.patch.object(
            common,
            "_numeric_proc_entries",
            side_effect=common.RuntimeErrorClosed("proc unreadable"),
        ):
            snapshot = common.residue_snapshot("fixture")
        self.assertIn("proc_unreadable", snapshot["errors"])
        self.assertFalse(common.residue_is_zero(snapshot))

        real_listdir = os.listdir

        def listdir(path):
            if path == common.RUN_ROOT:
                raise PermissionError("run root unreadable")
            if path.startswith("/sys/fs/cgroup/"):
                return []
            return real_listdir(path)

        with (
            mock.patch.object(common, "_numeric_proc_entries", return_value=[]),
            mock.patch.object(common.os, "listdir", side_effect=listdir),
            mock.patch("builtins.open", mock.mock_open(read_data="")),
        ):
            snapshot = common.residue_snapshot("fixture")
        self.assertIn("run_root_unreadable", snapshot["errors"])
        self.assertFalse(common.residue_is_zero(snapshot))

    def test_residue_scan_ignores_long_non_target_concurrent_sandbox(self) -> None:
        target = "private-target123"
        other = "private-other456"
        long_other = (
            "/usr/bin/unshare --pid --fork openmle-sandbox-supervisor "
            "--run-dir /tmp/openmle/runs/%s --command " % other
        ).encode("utf-8") + b"x" * 5000
        long_target = long_other.replace(other.encode("utf-8"), target.encode("utf-8"))

        def snapshot_for(payload):
            real_open = open

            def open_fixture(path, *args, **kwargs):
                if path == "/proc/4242/cmdline":
                    return mock.mock_open(read_data=payload)()
                if path == "/proc/self/mountinfo":
                    return mock.mock_open(read_data="")()
                return real_open(path, *args, **kwargs)

            real_listdir = os.listdir

            def listdir_fixture(path):
                if path == common.RUN_ROOT:
                    return []
                if path.startswith("/sys/fs/cgroup/"):
                    return []
                return real_listdir(path)

            with (
                mock.patch.object(common, "_numeric_proc_entries", return_value=["4242"]),
                mock.patch.object(common.os, "listdir", side_effect=listdir_fixture),
                mock.patch("builtins.open", side_effect=open_fixture),
            ):
                return common.residue_snapshot(target)

        concurrent = snapshot_for(long_other)
        self.assertEqual(concurrent["errors"], [])
        self.assertEqual(concurrent["processes"], [])
        self.assertTrue(common.residue_is_zero(concurrent))

        matching = snapshot_for(long_target)
        self.assertEqual(matching["errors"], ["proc_cmdline_too_large:4242"])
        self.assertFalse(common.residue_is_zero(matching))

    def test_runtime_directory_setup_is_thread_safe_and_never_toggles_umask(self) -> None:
        with tempfile.TemporaryDirectory(dir=TMP_PARENT) as raw:
            scratch = Path(raw) / "runtime"
            paths = (
                scratch,
                scratch / "runs",
                scratch / "state",
                scratch / "workspaces",
            )
            with (
                mock.patch.object(common, "SCRATCH", str(paths[0])),
                mock.patch.object(common, "RUN_ROOT", str(paths[1])),
                mock.patch.object(common, "STATE_ROOT", str(paths[2])),
                mock.patch.object(common, "PUBLIC_WORKSPACE_ROOT", str(paths[3])),
                mock.patch.object(
                    common.os,
                    "umask",
                    side_effect=AssertionError("runtime setup must not mutate umask"),
                ),
            ):
                with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
                    list(pool.map(lambda _index: common.ensure_runtime_directories(), range(32)))
            for path in paths:
                self.assertTrue(path.is_dir())
                self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o700)

    def test_supervisor_enforces_instrumentation_directory_modes(self) -> None:
        source = (ROOT / "sandbox_supervisor.c").read_text()
        self.assertIn("chmod(bindir, 0555)", source)
        self.assertIn("chmod(hookdir, 0555)", source)
        self.assertIn("chmod instrumentation directories", source)

    def test_workspace_scan_deadline_is_absolute(self) -> None:
        with tempfile.TemporaryDirectory(dir=TMP_PARENT) as raw:
            with self.assertRaises(common.RuntimeErrorClosed):
                common.scan_workspace(
                    raw, common.PUBLIC_LIMITS, deadline=time.monotonic() - 1.0
                )

    def test_artifact_lock_is_exact_install_membership(self) -> None:
        expected = {
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
        }
        self.assertEqual(set(common.ARTIFACT_LOCK_MEMBERS), expected)
        value = json.loads((ROOT / "artifact-lock.json").read_text())
        self.assertEqual({record["path"] for record in value["files"]}, expected)
        lock_sha256 = hashlib.sha256((ROOT / "artifact-lock.json").read_bytes()).hexdigest()
        self.assertTrue(common.validate_artifact_lock(lock_sha256))
        self.assertFalse(common.validate_install_inventory(str(ROOT), lock_sha256))

    def test_installer_replaces_stale_inventory_atomically(self) -> None:
        source = (ROOT / "install_bundle.sh").read_text()
        self.assertIn("validate_install_inventory", source)
        self.assertIn("source.previous", source)

    def test_strict_json_rejects_duplicate_keys(self) -> None:
        with self.assertRaises(ValueError):
            common.strict_json_loads('{"x":1,"x":2}')

    def test_runtime_artifact_lock(self) -> None:
        self.assertTrue(
            common.validate_artifact_lock(public_runner.ARTIFACT_LOCK_SHA256)
        )
        self.assertEqual(
            public_runner.ARTIFACT_LOCK_SHA256,
            private_runner.ARTIFACT_LOCK_SHA256,
        )

    def test_legacy_admission_stamp_cannot_be_reused(self) -> None:
        with tempfile.TemporaryDirectory(dir=TMP_PARENT) as raw:
            root = Path(raw)
            evidence = root / "evidence"
            evidence.mkdir()
            evidence_hashes = {}
            for field, name in (
                ("public_probe_summary_sha256", "public-probe-summary.json"),
                ("private_probe_summary_sha256", "private-probe-summary.json"),
                ("cleanup_receipt_sha256", "cleanup-receipt.json"),
            ):
                payload = (field + "\n").encode()
                (evidence / name).write_bytes(payload)
                evidence_hashes[field] = hashlib.sha256(payload).hexdigest()
            stamp = {
                "schema": "openmle_fast_runtime_admission_stamp_v1",
                "runtime_digest": common.RUNTIME_DIGEST,
                "boot_id": common.boot_id(),
                "kernel_release": os.uname()[2],
                "artifact_hashes": common.verified_component_digests(public_runner.ARTIFACT_LOCK_SHA256),
                "eligible": True,
                **evidence_hashes,
            }
            stamp_path = root / "admission-stamp.json"
            stamp_path.write_text(common.canonical_json(stamp) + "\n")
            with mock.patch.multiple(
                common,
                ADMISSION_STAMP=str(stamp_path),
                SCRATCH=str(root),
            ):
                valid, value = common._admission_stamp_valid({"test": True})
            self.assertFalse(valid)
            self.assertIsNone(value)

    def test_public_and_private_operations_recheck_live_admission(self) -> None:
        public_execute = {
            "schema": public_runner.REQUEST_SCHEMA,
            "workspace": common.PUBLIC_WORKSPACE_ROOT + "/admission-fixture",
            "command": "true",
            "timeout_ms": 1000,
            "managed_runtime_budget_ms": 1000,
        }
        lifecycle = {
            "schema": public_runner.LIFECYCLE_REQUEST_SCHEMA,
            "workspace": common.PUBLIC_WORKSPACE_ROOT + "/admission-fixture",
            "operation": "freeze",
            "timeout_ms": 1000,
        }
        private_request = {
            "schema": private_runner.REQUEST_SCHEMA,
            "task_id": "admission-fixture",
            "grader_binding_sha256": "1" * 64,
            "package_identity_sha256": "2" * 64,
            "metric_sha256": "3" * 64,
            "answer_sha256": "4" * 64,
            "submission_sha256": "5" * 64,
            "higher_is_better": True,
            "validator_success_forms": [],
            "metric_fd": 3,
            "answer_fd": 4,
            "submission_fd": 5,
            "timeout_ms": 1000,
        }
        rejection = common.RuntimeErrorClosed("live runtime admission failed")
        with mock.patch.object(
            common, "require_runtime_admission", side_effect=rejection
        ) as admission:
            with self.assertRaises(common.RuntimeErrorClosed):
                public_runner.execute(public_execute)
            with self.assertRaises(common.RuntimeErrorClosed):
                public_runner.freeze(lifecycle)
            lifecycle["operation"] = "teardown"
            with self.assertRaises(common.RuntimeErrorClosed):
                public_runner.teardown(lifecycle)
            with self.assertRaises(common.RuntimeErrorClosed):
                private_runner.grade(private_request)
        self.assertEqual(admission.call_count, 4)

    def test_probe_capability_environment_without_live_fd_fails_closed(self) -> None:
        request = {
            "schema": public_runner.REQUEST_SCHEMA,
            "workspace": common.PUBLIC_WORKSPACE_ROOT + "/capability-fixture",
            "command": "true",
            "timeout_ms": 1000,
            "managed_runtime_budget_ms": 1000,
        }
        fixture = self._probe_capability_fixture(request)
        with (
            mock.patch.object(
                common, "active_preflight", return_value=fixture["preflight"]
            ),
            mock.patch.dict(
                os.environ, {common.PROBE_CAPABILITY_ENV: "999999"}, clear=False
            ),
        ):
            with self.assertRaisesRegex(
                common.RuntimeErrorClosed, "live runtime admission failed"
            ):
                common.require_runtime_admission(
                    fixture["expected_lock"],
                    operation="public.execute",
                    request=request,
                )
            self.assertNotIn(common.PROBE_CAPABILITY_ENV, os.environ)

    def test_live_cgroup_probe_launch_inherits_one_bound_capability(self) -> None:
        request = {
            "schema": public_runner.REQUEST_SCHEMA,
            "workspace": common.PUBLIC_WORKSPACE_ROOT + "/live-cgroup-fixture",
            "command": "true",
            "timeout_ms": 1000,
            "managed_runtime_budget_ms": 1000,
        }
        read_fd, write_fd = os.pipe()
        process = object()
        try:
            with (
                mock.patch.object(
                    remote_probe,
                    "_create_probe_capability",
                    return_value=read_fd,
                ) as create,
                mock.patch.object(
                    remote_probe.subprocess, "Popen", return_value=process
                ) as popen,
                mock.patch.dict(os.environ, {}, clear=True),
            ):
                self.assertIs(
                    remote_probe._popen_probe(
                        [str(ROOT / "public_runner.py"), "execute"],
                        request,
                        "public.execute",
                    ),
                    process,
                )
            create.assert_called_once_with("public.execute", request)
            self.assertEqual(popen.call_args.kwargs["pass_fds"], (read_fd,))
            self.assertEqual(
                popen.call_args.kwargs["env"][common.PROBE_CAPABILITY_ENV],
                str(read_fd),
            )
            with self.assertRaises(OSError):
                os.fstat(read_fd)
        finally:
            try:
                os.close(read_fd)
            except OSError:
                pass
            os.close(write_fd)

    def test_probe_capability_rejects_wrong_bindings_and_expiry(self) -> None:
        request = {
            "schema": public_runner.REQUEST_SCHEMA,
            "workspace": common.PUBLIC_WORKSPACE_ROOT + "/capability-fixture",
            "command": "true",
            "timeout_ms": 1000,
            "managed_runtime_budget_ms": 1000,
        }
        fixture = self._probe_capability_fixture(request)
        cases = {
            "operation": dict(fixture["capability"], operation="public.freeze"),
            "request": dict(
                fixture["capability"], request_sha256=common.canonical_sha256({})
            ),
            "session": dict(
                fixture["capability"], probe_session_id="c" * 32
            ),
            "artifact": dict(
                fixture["capability"], artifact_identity={"fixture": "drifted"}
            ),
            "expiry": dict(
                fixture["capability"],
                issued_monotonic_ns=fixture["now"]
                - common.PROBE_CAPABILITY_MAX_NS,
                expires_monotonic_ns=fixture["now"] - 1,
            ),
        }
        for name, capability in cases.items():
            with (
                self.subTest(name=name),
                mock.patch.object(
                    common,
                    "_read_sealed_probe_capability",
                    return_value=capability,
                ),
                mock.patch.object(
                    common, "load_probe_session", return_value=fixture["session"]
                ),
                mock.patch.object(
                    common, "boot_id", return_value=capability["boot_id"]
                ),
                mock.patch.object(
                    common,
                    "probe_artifact_identity",
                    return_value=fixture["artifact_identity"],
                ),
                mock.patch.object(
                    common,
                    "_process_start_ticks",
                    return_value=fixture["parent_start_ticks"],
                ),
                mock.patch.object(
                    common, "_parent_is_exact_remote_probe", return_value=True
                ),
                mock.patch.object(
                    common.time, "monotonic_ns", return_value=fixture["now"]
                ),
            ):
                self.assertFalse(
                    common._probe_capability_valid(
                        9,
                        "public.execute",
                        request,
                        fixture["preflight"],
                        fixture["expected_lock"],
                    )
                )

    @unittest.skipUnless(
        sys.platform.startswith("linux")
        and hasattr(os, "geteuid")
        and os.geteuid() == 0,
        "sealed probe capabilities require root on Linux",
    )
    def test_valid_sealed_probe_capability_is_consumed_before_work(self) -> None:
        request = {
            "schema": public_runner.REQUEST_SCHEMA,
            "workspace": common.PUBLIC_WORKSPACE_ROOT + "/capability-fixture",
            "command": "true",
            "timeout_ms": 1000,
            "managed_runtime_budget_ms": 1000,
        }
        fixture = self._probe_capability_fixture(request)
        session = dict(
            fixture["session"],
            schema="openmle_fast_probe_session_v1",
            boot_id="fixture-boot",
            kernel_release=os.uname()[2],
            artifact_identity=fixture["artifact_identity"],
        )
        with (
            mock.patch.object(common, "load_probe_session", return_value=session),
            mock.patch.object(
                common,
                "verified_rootfs_identity",
                return_value=fixture["rootfs_identity"],
            ),
            mock.patch.object(common, "boot_id", return_value="fixture-boot"),
            mock.patch.object(
                common,
                "probe_artifact_identity",
                return_value=fixture["artifact_identity"],
            ),
            mock.patch.object(
                common,
                "_process_start_ticks",
                return_value=fixture["parent_start_ticks"],
            ),
        ):
            descriptor = remote_probe._create_probe_capability(
                "public.execute", request
            )
        decoded = common._read_sealed_probe_capability(descriptor)
        self.assertEqual(decoded["operation"], "public.execute")
        self.assertEqual(decoded["request_sha256"], common.canonical_sha256(request))
        with self.assertRaises(OSError):
            os.pwrite(descriptor, b"x", 0)
        preflight = dict(fixture["preflight"])
        with (
            mock.patch.object(common, "active_preflight", return_value=preflight),
            mock.patch.object(common, "load_probe_session", return_value=session),
            mock.patch.object(common, "boot_id", return_value="fixture-boot"),
            mock.patch.object(
                common,
                "probe_artifact_identity",
                return_value=fixture["artifact_identity"],
            ),
            mock.patch.object(
                common,
                "_process_start_ticks",
                return_value=fixture["parent_start_ticks"],
            ),
            mock.patch.object(
                common, "_parent_is_exact_remote_probe", return_value=True
            ),
            mock.patch.object(common.os, "getppid", return_value=os.getpid()),
            mock.patch.dict(
                os.environ, {common.PROBE_CAPABILITY_ENV: str(descriptor)}, clear=False
            ),
        ):
            admitted = common.require_runtime_admission(
                fixture["expected_lock"],
                operation="public.execute",
                request=request,
            )
            self.assertIs(admitted, preflight)
            self.assertNotIn(common.PROBE_CAPABILITY_ENV, os.environ)
            with self.assertRaises(OSError):
                os.fstat(descriptor)

    def test_final_admission_needs_no_probe_capability(self) -> None:
        request = {
            "schema": public_runner.REQUEST_SCHEMA,
            "workspace": common.PUBLIC_WORKSPACE_ROOT + "/admitted-fixture",
            "command": "true",
            "timeout_ms": 1000,
            "managed_runtime_budget_ms": 1000,
        }
        fixture = self._probe_capability_fixture(request)
        preflight = dict(fixture["preflight"], admission_stamp_valid=True)
        with (
            mock.patch.dict(os.environ, {}, clear=False),
            mock.patch.object(common, "active_preflight", return_value=preflight),
            mock.patch.object(common, "_probe_capability_valid") as validator,
        ):
            os.environ.pop(common.PROBE_CAPABILITY_ENV, None)
            self.assertIs(
                common.require_runtime_admission(
                    fixture["expected_lock"],
                    operation="public.execute",
                    request=request,
                ),
                preflight,
            )
        validator.assert_not_called()

    def test_metadata_never_performs_full_rootfs_measurement(self) -> None:
        with mock.patch.object(
            common,
            "measure_rootfs_tree",
            side_effect=AssertionError("metadata attempted a full rootfs scan"),
        ), mock.patch.object(
            common,
            "rootfs_identity",
            side_effect=AssertionError("metadata attempted full rootfs identity"),
        ):
            public_runner.metadata()
            private_runner.metadata()

    def test_active_preflight_requires_exact_installed_inventory(self) -> None:
        preflight = common.active_preflight(public_runner.ARTIFACT_LOCK_SHA256)
        self.assertIn("artifact_install_inventory", preflight["checks"])
        self.assertFalse(preflight["checks"]["artifact_install_inventory"])
        for name in ("public_runner.py", "private_runner.py", "remote_probe.py"):
            source = (ROOT / name).read_text()
            self.assertLess(
                source.index("sys.dont_write_bytecode = True"),
                source.index("import runtime_common as common"),
            )

    def test_probe_session_rejects_stale_cross_session_evidence(self) -> None:
        with tempfile.TemporaryDirectory(dir=TMP_PARENT) as raw:
            root = Path(raw)
            evidence = root / "evidence"
            inputs = root / "probe-inputs"
            stale = evidence / "public-probe-summary.json"
            evidence.mkdir()
            stale.write_text("stale\n")
            artifact_identity = {"fixture": "artifact-v1"}
            with (
                mock.patch.multiple(
                    common,
                    SCRATCH=str(root),
                    ADMISSION_STAMP=str(root / "admission-stamp.json"),
                ),
                mock.patch.multiple(
                    remote_probe,
                    EVIDENCE=str(evidence),
                    INPUT_ROOT=str(inputs),
                    PROBE_FAULT_ROOT=str(root / "probe-private-faults"),
                    PUBLIC_FAULT_ROOT=str(root / "public-faults"),
                ),
                mock.patch.object(
                    common,
                    "probe_artifact_identity",
                    return_value=artifact_identity,
                ),
            ):
                first = remote_probe.start_probe_session()
                self.assertFalse(stale.exists())
                bound = common.bind_evidence_context({"schema": "fixture_v1"}, first)
                self.assertTrue(common.evidence_context_matches(bound, first))
                second = remote_probe.start_probe_session()
                self.assertNotEqual(
                    first["probe_session_id"], second["probe_session_id"]
                )
                self.assertFalse(common.evidence_context_matches(bound, second))
                self.assertIn("probe_session", common.ADMISSION_EVIDENCE_FILES)

    def test_cleanup_propagates_unmount_failure(self) -> None:
        mounts = {name: "/mount/" + name.replace(",", "_") for name in common.CONTROLLERS}
        children = {name: mounts[name] + "/child" for name in common.CONTROLLERS}
        with (
            mock.patch.object(common, "_kill_cgroup", return_value=[]),
            mock.patch.object(common.os, "rmdir"),
            mock.patch.object(common, "exact_mount", return_value={"mountpoint": "/mount"}),
            mock.patch.object(
                common,
                "run_checked",
                side_effect=common.RuntimeErrorClosed("unmount failed"),
            ),
        ):
            with self.assertRaises(common.RuntimeErrorClosed):
                common._cleanup_cgroups(mounts, children)

    def test_cgroup_cleanup_accepts_exact_bind_subroot_mount(self) -> None:
        mountpoint = "/owned/run/cgroup/pids"
        payload = (
            "31 20 0:41 /kubepods/pod/container %s "
            "rw,nosuid,nodev,noexec,relatime - cgroup cgroup rw,pids\n"
            % mountpoint
        )
        with (
            mock.patch.object(common, "_kill_cgroup", return_value=[]),
            mock.patch.object(common.os, "rmdir"),
            mock.patch("builtins.open", mock.mock_open(read_data=payload)),
            mock.patch.object(common, "run_checked") as run,
        ):
            receipt = common._cleanup_cgroups(
                {"pids": mountpoint}, {}, deadline=time.monotonic() + 1.0
            )
        run.assert_called_once_with(
            ["/usr/bin/umount", mountpoint],
            deadline=mock.ANY,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        self.assertTrue(receipt["mounts_unmounted"])

    def test_cleanup_skips_bookkept_destination_when_bind_never_landed(self) -> None:
        mountpoint = "/mount/cpu_cpuacct"
        with (
            mock.patch.object(common, "exact_mount", return_value=None),
            mock.patch.object(common, "run_checked") as run,
        ):
            receipt = common._cleanup_cgroups(
                {"cpu,cpuacct": mountpoint}, {}, deadline=time.monotonic() + 1.0
            )
        run.assert_not_called()
        self.assertTrue(receipt["mounts_unmounted"])

    def test_cgroup_bind_attempt_is_bookkept_before_subprocess_returns(self) -> None:
        mounts = {}
        children = {}
        run_dir = "/owned/run"
        expected = run_dir + "/cgroup/cpu_cpuacct"

        def fail_first_bind(argv, **_kwargs):
            self.assertEqual(
                argv[:3],
                ["/usr/bin/mount", "--bind", "/sys/fs/cgroup/cpu,cpuacct"],
            )
            self.assertEqual(mounts.get("cpu,cpuacct"), expected)
            raise common.RuntimeErrorClosed("bind subprocess timed out")

        with (
            mock.patch.object(common, "_unshare_mount_namespace"),
            mock.patch.object(common, "check_deadline"),
            mock.patch.object(common.os, "makedirs"),
            mock.patch.object(common, "run_checked", side_effect=fail_first_bind),
        ):
            with self.assertRaises(common.RuntimeErrorClosed):
                common._create_cgroups(
                    run_dir,
                    cpu_vcpus=2,
                    memory_bytes=1024,
                    max_processes=8,
                    managed_ms=1000,
                    name="fixture",
                    mounts=mounts,
                    children=children,
                )

    def test_policy_timeout_excludes_validation_overhead_and_caps_managed_budget(self) -> None:
        state = {
            "schema": public_runner.STATE_SCHEMA,
            "state_id": "0123456789abcdef",
            "workspace": "/owned/workspace",
            "boot_id": common.boot_id(),
            "lifecycle": "active",
            "shell_actions": 0,
            "managed_runtime_ms": 119500,
            "started_monotonic": 0.0,
            "updated_monotonic": 0.0,
        }

        @contextlib.contextmanager
        def locked(_workspace, deadline=None):
            del deadline
            yield "/state.json"

        sandbox_result = {
            "stdout": b"",
            "stderr": b"",
            "exit_code": 0,
            "timed_out": False,
            "wall_seconds": 0.1,
            "managed_runtime_wall_seconds": 0.1,
            "cpu_seconds": 0.1,
            "peak_rss_bytes": 1,
            "bytes_read": 0,
            "bytes_written": 0,
            "process_peak": 1,
            "execution_attempt_delta": 1,
            "execution_completed_delta": 1,
            "nested_subprocess_delta": 1,
            "fit_delta": 0,
            "failure_class": None,
            "infrastructure_fault": False,
        }
        scan = {
            "file_count": 0,
            "total_bytes": 0,
            "max_file_bytes": 0,
            "free_bytes": 100000,
            "capacity_bytes": 1000000,
        }
        request = {
            "schema": public_runner.REQUEST_SCHEMA,
            "workspace": "/owned/workspace",
            "command": "python -c 'print(1)'",
            "timeout_ms": 2000,
            "managed_runtime_budget_ms": 400,
        }
        clock = [10.0]
        scan_deadlines = []

        def monotonic():
            return clock[0]

        def scan_workspace(_workspace, _limits, deadline=None):
            scan_deadlines.append(deadline)
            clock[0] += 0.4
            return scan

        with (
            mock.patch.object(common, "require_runtime_admission"),
            mock.patch.object(public_runner, "_workspace_lock", locked),
            mock.patch.object(
                public_runner, "_adopt_or_validate_active", return_value=state
            ),
            mock.patch.object(public_runner, "_write_state"),
            mock.patch.object(public_runner.time, "monotonic", side_effect=monotonic),
            mock.patch.object(common, "scan_workspace", side_effect=scan_workspace),
            mock.patch.object(common, "run_sandbox", return_value=sandbox_result) as run,
        ):
            public_runner.execute(request)
        self.assertEqual(run.call_args.kwargs["timeout_ms"], 2000)
        self.assertLessEqual(run.call_args.kwargs["managed_ms"], 400)
        self.assertEqual(len(scan_deadlines), 2)
        self.assertTrue(all(item is not None for item in scan_deadlines))
        self.assertIsNotNone(run.call_args.kwargs.get("deadline"))

    def test_host_preparation_latency_does_not_consume_policy_timeout(self) -> None:
        state = {
            "schema": public_runner.STATE_SCHEMA,
            "state_id": "0123456789abcdef",
            "workspace": "/owned/workspace",
            "boot_id": common.boot_id(),
            "lifecycle": "active",
            "shell_actions": 0,
            "managed_runtime_ms": 0,
            "started_monotonic": 10.0,
            "updated_monotonic": 10.0,
        }

        @contextlib.contextmanager
        def locked(_workspace, deadline=None):
            del deadline
            yield "/state.json"

        sandbox_result = {
            "stdout": b"",
            "stderr": b"",
            "exit_code": 0,
            "timed_out": False,
            "wall_seconds": 0.1,
            "managed_runtime_wall_seconds": 0.1,
            "cpu_seconds": 0.1,
            "peak_rss_bytes": 1,
            "bytes_read": 0,
            "bytes_written": 0,
            "process_peak": 1,
            "execution_attempt_delta": 1,
            "execution_completed_delta": 1,
            "nested_subprocess_delta": 1,
            "fit_delta": 0,
            "failure_class": None,
            "infrastructure_fault": False,
        }
        scan = {
            "file_count": 0,
            "total_bytes": 0,
            "max_file_bytes": 0,
            "free_bytes": 100000,
            "capacity_bytes": 1000000,
        }
        request = {
            "schema": public_runner.REQUEST_SCHEMA,
            "workspace": "/owned/workspace",
            "command": "true",
            "timeout_ms": 2000,
            "managed_runtime_budget_ms": 1000,
        }
        clock = [10.0]
        scans = [0]

        def monotonic():
            return clock[0]

        def scan_workspace(_workspace, _limits, deadline=None):
            del deadline
            if scans[0] == 0:
                clock[0] += 8.0
            scans[0] += 1
            return scan

        with (
            mock.patch.object(common, "require_runtime_admission"),
            mock.patch.object(public_runner, "_workspace_lock", locked),
            mock.patch.object(
                public_runner, "_adopt_or_validate_active", return_value=state
            ),
            mock.patch.object(public_runner, "_write_state"),
            mock.patch.object(public_runner.time, "monotonic", side_effect=monotonic),
            mock.patch.object(common, "scan_workspace", side_effect=scan_workspace),
            mock.patch.object(common, "run_sandbox", return_value=sandbox_result) as run,
        ):
            public_runner.execute(request)
        self.assertEqual(run.call_args.kwargs["timeout_ms"], 2000)
        self.assertGreaterEqual(
            run.call_args.kwargs["deadline"] - clock[0],
            (2000 + public_runner.ACTION_COMPLETION_GRACE_MS) / 1000.0,
        )

    def test_short_requested_timeout_preserves_cleanup_grace(self) -> None:
        state = {
            "schema": public_runner.STATE_SCHEMA,
            "state_id": "0123456789abcdef",
            "workspace": "/owned/workspace",
            "boot_id": common.boot_id(),
            "lifecycle": "active",
            "shell_actions": 0,
            "managed_runtime_ms": 0,
            "started_monotonic": 0.0,
            "updated_monotonic": 0.0,
        }

        @contextlib.contextmanager
        def locked(_workspace, deadline=None):
            del deadline
            yield "/state.json"

        sandbox_result = {
            "stdout": b"",
            "stderr": b"",
            "exit_code": 124,
            "timed_out": True,
            "wall_seconds": 0.08,
            "managed_runtime_wall_seconds": 0.08,
            "cpu_seconds": 0.01,
            "peak_rss_bytes": 1,
            "bytes_read": 0,
            "bytes_written": 0,
            "process_peak": 1,
            "execution_attempt_delta": 1,
            "execution_completed_delta": 0,
            "nested_subprocess_delta": 1,
            "fit_delta": 0,
            "failure_class": "wall_timeout",
            "infrastructure_fault": False,
        }
        scan = {
            "file_count": 0,
            "total_bytes": 0,
            "max_file_bytes": 0,
            "free_bytes": 100000,
            "capacity_bytes": 1000000,
        }
        request = {
            "schema": public_runner.REQUEST_SCHEMA,
            "workspace": "/owned/workspace",
            "command": "python -c 'import time; time.sleep(5)'",
            "timeout_ms": 100,
            "managed_runtime_budget_ms": 1000,
        }
        clock = [10.0]

        def monotonic():
            return clock[0]

        def scan_workspace(_workspace, _limits, deadline=None):
            del deadline
            clock[0] += 0.02
            return scan

        with (
            mock.patch.object(common, "require_runtime_admission"),
            mock.patch.object(public_runner, "_workspace_lock", locked),
            mock.patch.object(
                public_runner, "_adopt_or_validate_active", return_value=state
            ),
            mock.patch.object(public_runner, "_write_state"),
            mock.patch.object(public_runner.time, "monotonic", side_effect=monotonic),
            mock.patch.object(common, "scan_workspace", side_effect=scan_workspace),
            mock.patch.object(common, "run_sandbox", return_value=sandbox_result) as run,
        ):
            receipt = public_runner.execute(request)
        self.assertEqual(receipt["failure_class"], "wall_timeout")
        self.assertTrue(receipt["timed_out"])
        self.assertGreater(run.call_args.kwargs["timeout_ms"], 0)
        self.assertLessEqual(run.call_args.kwargs["timeout_ms"], 100)

    def test_public_fault_diagnostic_is_bounded_root_only_and_redacted(self) -> None:
        with tempfile.TemporaryDirectory(dir=TMP_PARENT) as raw:
            fault_root = Path(raw) / "public-faults"
            command = "printf OPENMLE_DIAGNOSTIC_SECRET_6ad1"
            request = {
                "schema": public_runner.REQUEST_SCHEMA,
                "workspace": "/tmp",
                "command": command,
                "timeout_ms": 100,
                "managed_runtime_budget_ms": 1000,
            }
            try:
                raise ValueError("failed command: " + command)
            except ValueError as cause:
                error = common.SandboxInfrastructureError("cgroup_setup", cause)
            with mock.patch.object(public_runner, "PUBLIC_FAULT_ROOT", str(fault_root)):
                public_runner._write_public_fault(request, error)
            records = list(fault_root.glob("*.json"))
            self.assertEqual(len(records), 1)
            raw_payload = records[0].read_bytes()
            value = json.loads(raw_payload)
            self.assertLessEqual(len(raw_payload), 4096)
            self.assertEqual(stat.S_IMODE(fault_root.stat().st_mode), 0o700)
            self.assertEqual(stat.S_IMODE(records[0].stat().st_mode), 0o600)
            self.assertEqual(value["phase"], "cgroup_setup")
            self.assertEqual(value["exception_type"], "ValueError")
            self.assertEqual(value["command_bytes"], len(command.encode()))
            self.assertEqual(value["command_sha256"], hashlib.sha256(command.encode()).hexdigest())
            self.assertEqual(value["request_sha256"], common.canonical_sha256(request))
            self.assertNotIn(command.encode(), raw_payload)
            self.assertTrue(value["traceback_frames"])

    def test_public_fault_retention_is_exact_under_concurrency(self) -> None:
        with tempfile.TemporaryDirectory(dir=TMP_PARENT) as raw:
            fault_root = Path(raw) / "public-faults"

            def write_fault(index: int) -> None:
                command = "printf diagnostic-%d" % index
                request = {
                    "schema": public_runner.REQUEST_SCHEMA,
                    "workspace": "/tmp",
                    "command": command,
                    "timeout_ms": 100,
                    "managed_runtime_budget_ms": 1000,
                }
                try:
                    raise ValueError("failed command: " + command)
                except ValueError as cause:
                    error = common.SandboxInfrastructureError(
                        "concurrent_diagnostic", cause
                    )
                public_runner._write_public_fault(request, error)

            with (
                mock.patch.object(
                    public_runner, "PUBLIC_FAULT_ROOT", str(fault_root)
                ),
                mock.patch.object(public_runner, "PUBLIC_FAULT_MAX_RECORDS", 8),
                concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool,
            ):
                list(pool.map(write_fault, range(64)))

            records = list(fault_root.glob("*.json"))
            self.assertEqual(len(records), 8)
            self.assertEqual(stat.S_IMODE(fault_root.stat().st_mode), 0o700)
            for path in records:
                self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
                value = json.loads(path.read_text())
                self.assertEqual(value["phase"], "concurrent_diagnostic")
                self.assertNotIn(b"printf diagnostic-", path.read_bytes())

    def test_sandbox_host_cleanup_budget_covers_bounded_reap(self) -> None:
        self.assertGreaterEqual(common.SANDBOX_CLEANUP_GRACE_SECONDS, 4.0)
        self.assertGreaterEqual(common.SANDBOX_OPERATION_GRACE_SECONDS, 1.0)
        self.assertGreaterEqual(
            public_runner.ACTION_COMPLETION_GRACE_MS / 1000.0,
            common.SANDBOX_SETUP_GRACE_SECONDS
            + common.SANDBOX_OPERATION_GRACE_SECONDS
            + common.SANDBOX_CLEANUP_GRACE_SECONDS
            + 0.5,
        )
        source = (ROOT / "runtime_common.py").read_text()
        self.assertIn(
            "operation_deadline = execution_deadline + SANDBOX_OPERATION_GRACE_SECONDS",
            source,
        )
        self.assertIn(
            "cleanup_deadline = time.monotonic() + SANDBOX_CLEANUP_GRACE_SECONDS",
            source,
        )
        self.assertGreaterEqual(
            remote_probe.PUBLIC_RUNNER_PROCESS_GRACE_SECONDS,
            (
                public_runner.ACTION_PREPARATION_GRACE_MS
                + public_runner.ACTION_COMPLETION_GRACE_MS
            )
            / 1000.0
            + 1.0,
        )
        probe_source = (ROOT / "remote_probe.py").read_text()
        self.assertIn(
            "timeout=timeout_ms / 1000.0 + PUBLIC_RUNNER_PROCESS_GRACE_SECONDS",
            probe_source,
        )

    def test_sandbox_command_deadline_starts_after_host_setup(self) -> None:
        source = (ROOT / "runtime_common.py").read_text()
        cgroup_setup = source.index("mounts, children, effective = _create_cgroups(")
        command_started = source.index("command_started = time.monotonic()")
        command_deadline = source.index(
            "execution_deadline = command_started + timeout_ms / 1000.0"
        )
        self.assertGreater(command_started, cgroup_setup)
        self.assertGreater(command_deadline, command_started)
        self.assertNotIn("execution_deadline = started + timeout_ms", source)

    def test_public_concurrency_stress_waits_for_wave_before_global_residue(self) -> None:
        normal_receipt = {
            "exit_code": 0,
            "failure_class": None,
            "infrastructure_fault": False,
        }
        lifecycle_receipts = {
            "freeze": {"success": True, "workspace_read_only": True},
            "execute_after_freeze": {"infrastructure_fault": True},
            "teardown": {"success": True},
            "teardown_repeated": {"success": True},
        }
        zero_residue = {
            "errors": [],
            "processes": [],
            "mounts": [],
            "cgroups": [],
            "run_entries": [],
        }
        cleanup = mock.Mock()
        with (
            mock.patch.object(remote_probe, "PUBLIC_CONCURRENCY_WORKERS", 2),
            mock.patch.object(remote_probe, "PUBLIC_CONCURRENCY_WAVES", 3),
            mock.patch.object(
                remote_probe,
                "mount_workspace",
                side_effect=lambda label: "/owned/" + label,
            ),
            mock.patch.object(
                remote_probe,
                "execute_request",
                side_effect=lambda *_args, **_kwargs: dict(normal_receipt),
            ) as execute,
            mock.patch.object(
                remote_probe,
                "complete_lifecycle",
                side_effect=lambda _workspace: copy.deepcopy(lifecycle_receipts),
            ),
            mock.patch.object(remote_probe, "force_workspace_cleanup", cleanup),
            mock.patch.object(common, "exact_mount", return_value=None),
            mock.patch.object(
                common, "residue_snapshot", return_value=copy.deepcopy(zero_residue)
            ) as residue,
        ):
            result = remote_probe.run_public_concurrency_stress()

        self.assertTrue(result["ok"])
        self.assertEqual(result["completed_waves"], 3)
        self.assertEqual(result["execution_count"], 6)
        self.assertEqual(execute.call_count, 6)
        self.assertEqual(cleanup.call_count, 6)
        self.assertEqual(residue.call_count, 4)
        self.assertTrue(all(len(wave["receipt_sha256"]) == 2 for wave in result["waves"]))

    def test_remote_probe_distinguishes_unsafe_from_patch_only_freeze(self) -> None:
        source = (ROOT / "remote_probe.py").read_text()
        self.assertIn('"unsafe_nonowned_freeze_rejected"', source)
        self.assertIn('unsafe_freeze = lifecycle("/tmp", "freeze")', source)
        self.assertIn('"patch_only_freeze_adopted_and_torn_down"', source)
        self.assertNotIn('"nonowned_freeze_rejected"', source)

    def test_patch_only_lifecycle_adopts_before_freeze_or_teardown(self) -> None:
        state = {"lifecycle": "active", "state_id": "0123456789abcdef"}
        with (
            mock.patch.object(public_runner, "_read_state", return_value=None),
            mock.patch.object(
                public_runner,
                "_adopt_or_validate_active",
                return_value=state,
            ) as adopt,
        ):
            observed = public_runner._owned_state_or_adopt(
                "/state.json", "/owned/workspace", deadline=123.0
            )
        self.assertIs(observed, state)
        adopt.assert_called_once_with(
            "/state.json", "/owned/workspace", deadline=123.0
        )

        with (
            mock.patch.object(public_runner, "_read_state", return_value=state),
            mock.patch.object(public_runner, "_adopt_or_validate_active") as adopt,
        ):
            observed = public_runner._owned_state_or_adopt(
                "/state.json", "/owned/workspace", deadline=456.0
            )
        self.assertIs(observed, state)
        adopt.assert_not_called()

    def test_transitional_lifecycle_states_are_authenticated(self) -> None:
        with tempfile.TemporaryDirectory(dir=TMP_PARENT) as raw:
            root = Path(raw)
            scratch = root / "scratch"
            state_root = scratch / "state"
            run_root = scratch / "runs"
            workspace_root = scratch / "workspaces"
            with mock.patch.multiple(
                common,
                SCRATCH=str(scratch),
                STATE_ROOT=str(state_root),
                RUN_ROOT=str(run_root),
                PUBLIC_WORKSPACE_ROOT=str(workspace_root),
            ):
                for lifecycle in ("freezing", "tearing_down"):
                    state_path = state_root / (lifecycle + ".json")
                    body = {
                        "schema": public_runner.STATE_SCHEMA,
                        "state_id": "0123456789abcdef",
                        "lifecycle": lifecycle,
                    }
                    public_runner._write_state(str(state_path), body)
                    self.assertEqual(public_runner._read_state(str(state_path)), body)

    def test_supervisor_proc_mount_and_instrumentation_fail_closed(self) -> None:
        supervisor = (ROOT / "sandbox_supervisor.c").read_text()
        wrapper = (ROOT / "python_wrapper.c").read_text()
        self.assertEqual(supervisor.count('mount("proc", proc, "proc"'), 1)
        self.assertIn("fit_write", supervisor)
        self.assertIn("verify_fd_identity", wrapper)
        self.assertIn("S_ISFIFO", wrapper)
        self.assertIn("O_ACCMODE", wrapper)

    def test_socket_denial_is_nonfatal_and_live_probes_cover_basic_ls(self) -> None:
        supervisor = (ROOT / "sandbox_supervisor.c").read_text()
        probe = (ROOT / "remote_probe.py").read_text()
        self.assertIn("ERRNO_SYSCALL(socket, EPERM)", supervisor)
        self.assertIn("ERRNO_SYSCALL(socketpair, EPERM)", supervisor)
        self.assertNotIn("DENY_SYSCALL(socket)", supervisor)
        self.assertNotIn("DENY_SYSCALL(socketpair)", supervisor)
        self.assertIn('"basic_long_listing_with_nss_fallback"', probe)
        self.assertIn('"ls -la"', probe)
        self.assertIn('"network_socket_denied_without_sigsys"', probe)
        self.assertIn('"malicious_metric_network_denied_without_sigsys"', probe)
        self.assertIn(
            'network["classification"] == "invalid_submission"', probe
        )

    def test_supervisor_shell_devices_and_reserved_fd_order(self) -> None:
        supervisor = (ROOT / "sandbox_supervisor.c").read_text()
        self.assertIn('execl("/bin/sh", "sh", "-c"', supervisor)
        self.assertIn('chmod(dev, 0555)', supervisor)
        self.assertIn('chmod(node, devices[i].mode & 07777)', supervisor)
        self.assertNotIn('remount minimal dev read-only', supervisor)
        nofile = supervisor.index('set_limit(RLIMIT_NOFILE, cfg->max_open_files)')
        real_fd = supervisor.index('make real Python fd inheritable')
        fit_fd = supervisor.index('make fit event fd inheritable')
        self.assertGreater(nofile, real_fd)
        self.assertGreater(nofile, fit_fd)

    def test_runtime_sources_remain_python36_compatible(self) -> None:
        for name in (
            "runtime_common.py",
            "public_runner.py",
            "private_runner.py",
            "private_worker.py",
            "remote_probe.py",
        ):
            source = (ROOT / name).read_text()
            self.assertNotIn(".removeprefix(", source, msg=name)
            self.assertNotIn(".removesuffix(", source, msg=name)
        private_source = (ROOT / "private_runner.py").read_text()
        self.assertIn("STAGE_CLEANUP_TIMEOUT_MS = 2000", private_source)
        self.assertIn("cleanup_deadline = time.monotonic()", private_source)

    def test_live_probe_quotes_multiline_python_and_preserves_timeout_grace(self) -> None:
        source = (ROOT / "remote_probe.py").read_text()
        self.assertIn("shlex.quote(identity_source)", source)
        self.assertIn("time.sleep(30)'\", 1500", source)
        self.assertIn(
            '"short-timeout", "python -c \'import time; time.sleep(1)\'", 100',
            source,
        )
        self.assertIn('"concurrent_public_setup_and_short_execution"', source)
        self.assertIn("PUBLIC_CONCURRENCY_WORKERS = 8", source)
        self.assertIn("PUBLIC_CONCURRENCY_WAVES = 64", source)
        self.assertIn('"root_only_bounded_public_fault_diagnostic"', source)

    def test_metadata_schemas_are_recursive_and_exact(self) -> None:
        def assert_strict_objects(node, location="$"):
            if isinstance(node, dict):
                if node.get("type") == "object":
                    self.assertIs(
                        node.get("additionalProperties"),
                        False,
                        msg=location,
                    )
                    properties = node.get("properties")
                    if properties is not None:
                        self.assertEqual(
                            set(node.get("required", [])),
                            set(properties),
                            msg=location,
                        )
                for key, value in node.items():
                    assert_strict_objects(value, location + "/" + key)
            elif isinstance(node, list):
                for index, value in enumerate(node):
                    assert_strict_objects(value, location + "/" + str(index))

        pairs = (
            ("public-runner-metadata.schema.json", public_runner.metadata()),
            ("private-runner-metadata.schema.json", private_runner.metadata()),
        )
        for name, metadata in pairs:
            with self.subTest(name=name):
                schema = json.loads((ROOT / "schemas" / name).read_text())
                assert_strict_objects(schema)
                self.assertEqual(set(schema["properties"]), set(metadata))



    def test_public_metadata_is_truthful_on_non_linux_host(self) -> None:
        value = public_runner.metadata()
        self.assertEqual(value["resource_limits"], common.PUBLIC_LIMITS)
        self.assertFalse(value["formal_eligible"])
        self.assertFalse(value["cgroup_v2_cpu"])
        self.assertFalse(value["cgroup_v2_memory"])
        self.assertFalse(value["cgroup_v2_pids"])
        self.assertFalse(value["active_verification"]["admission_stamp_valid"])

    def test_private_metadata_is_truthful_on_non_linux_host(self) -> None:
        value = private_runner.metadata()
        self.assertEqual(value["resource_limits"], common.PRIVATE_LIMITS)
        self.assertFalse(value["formal_eligible"])
        self.assertEqual(
            value["staged_task_files"],
            ["metric.py", "answer.csv", "submission.csv"],
        )

    def test_version_aware_adapter_fixture_accepts_v1_without_v2_fabrication(self) -> None:
        public = public_runner.metadata()
        private = private_runner.metadata()
        for value in (public, private):
            value["cgroup_version"] = "v1"
            value["cgroup_mode"] = "v1"
            value["cgroup_controller_attestation"]["version"] = "v1"
            for name in ("cpu", "memory", "pids"):
                value["cgroup_controller_attestation"]["controllers"][name][
                    "available"
                ] = True
                value["cgroup_v1_" + name] = True
                value["cgroup_v2_" + name] = False
            value["active_verification"]["admission_stamp_valid"] = True
            value["formal_eligible"] = True
        for name, item in list(public.items()):
            if isinstance(item, bool) and name not in {
                "cgroup_v2_cpu",
                "cgroup_v2_memory",
                "cgroup_v2_pids",
            }:
                public[name] = True
        for name, item in list(private.items()):
            if isinstance(item, bool) and name not in {
                "cgroup_v2_cpu",
                "cgroup_v2_memory",
                "cgroup_v2_pids",
            }:
                private[name] = True
        self.assertTrue(
            adapter_fixture.attest_public(
                public, common.RUNTIME_DIGEST, common.PUBLIC_LIMITS
            )
        )
        self.assertTrue(
            adapter_fixture.attest_private(
                private, common.RUNTIME_DIGEST, common.PRIVATE_LIMITS
            )
        )

    def test_version_aware_adapter_rejects_v2_fabrication(self) -> None:
        value = public_runner.metadata()
        value["cgroup_version"] = "v1"
        value["cgroup_controller_attestation"]["version"] = "v1"
        value["formal_eligible"] = True
        value["active_verification"]["admission_stamp_valid"] = True
        for name, item in list(value.items()):
            if isinstance(item, bool):
                value[name] = True
        with self.assertRaisesRegex(ValueError, "fabricated"):
            adapter_fixture.attest_public(
                value, common.RUNTIME_DIGEST, common.PUBLIC_LIMITS
            )

    def test_public_request_exact_fields(self) -> None:
        valid = {
            "schema": public_runner.REQUEST_SCHEMA,
            "workspace": common.PUBLIC_WORKSPACE_ROOT + "/slot-1",
            "command": "python -c 'print(1)'",
            "timeout_ms": 1000,
            "managed_runtime_budget_ms": 750,
        }
        self.assertEqual(
            public_runner._validate_execute_request(valid),
            (
                valid["workspace"],
                valid["command"],
                valid["timeout_ms"],
                valid["managed_runtime_budget_ms"],
            ),
        )
        missing_budget = dict(valid)
        missing_budget.pop("managed_runtime_budget_ms")
        with self.assertRaises(common.RuntimeErrorClosed):
            public_runner._validate_execute_request(missing_budget)
        invalid = dict(valid, extra=True)
        with self.assertRaises(common.RuntimeErrorClosed):
            public_runner._validate_execute_request(invalid)

    def test_public_request_rejects_invalid_managed_runtime_budget(self) -> None:
        valid = {
            "schema": public_runner.REQUEST_SCHEMA,
            "workspace": common.PUBLIC_WORKSPACE_ROOT + "/slot-1",
            "command": "python -c 'print(1)'",
            "timeout_ms": 1000,
            "managed_runtime_budget_ms": 750,
        }
        for invalid_budget in (
            True,
            0,
            -1,
            common.PUBLIC_LIMITS["managed_runtime_per_action_ms"] + 1,
        ):
            with self.subTest(invalid_budget=invalid_budget):
                with self.assertRaises(common.RuntimeErrorClosed):
                    public_runner._validate_execute_request(
                        dict(valid, managed_runtime_budget_ms=invalid_budget)
                    )

    def test_lifecycle_receipt_exact_shape(self) -> None:
        value = public_runner._lifecycle_receipt(
            "freeze", True, True, True, True, None
        )
        self.assertEqual(
            set(value),
            {
                "schema",
                "operation",
                "success",
                "processes_reaped",
                "workspace_read_only",
                "cgroup_empty",
                "failure_class",
            },
        )

    def test_workspace_state_is_authenticated(self) -> None:
        with tempfile.TemporaryDirectory(dir=TMP_PARENT) as raw:
            root = Path(raw)
            scratch = root / "scratch"
            state_root = scratch / "state"
            run_root = scratch / "runs"
            workspace_root = scratch / "workspaces"
            with mock.patch.multiple(
                common,
                SCRATCH=str(scratch),
                STATE_ROOT=str(state_root),
                RUN_ROOT=str(run_root),
                PUBLIC_WORKSPACE_ROOT=str(workspace_root),
            ):
                state_path = state_root / "state.json"
                body = {
                    "schema": public_runner.STATE_SCHEMA,
                    "state_id": "0123456789abcdef",
                    "lifecycle": "active",
                }
                public_runner._write_state(str(state_path), body)
                self.assertEqual(public_runner._read_state(str(state_path)), body)
                raw_value = json.loads(state_path.read_text())
                raw_value["lifecycle"] = "frozen"
                state_path.write_text(json.dumps(raw_value))
                with self.assertRaises(common.RuntimeErrorClosed):
                    public_runner._read_state(str(state_path))

    def test_cli_invalid_requests_are_sanitized(self) -> None:
        public = subprocess.run(
            [str(ROOT / "public_runner.py"), "execute"],
            input=b'{"schema":',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        public_value = json.loads(public.stdout)
        self.assertTrue(public_value["infrastructure_fault"])
        self.assertEqual(public_value["stdout_b64"], "")
        self.assertEqual(public.stderr, b"")

        private = subprocess.run(
            [str(ROOT / "private_runner.py"), "grade"],
            input=b'{"schema":',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        private_value = json.loads(private.stdout)
        self.assertEqual(private_value["classification"], "infrastructure_fault")
        self.assertEqual(set(private_value), {
            "schema", "classification", "native_score", "higher_is_better"
        })
        self.assertEqual(private.stderr, b"")

class PrivateRunnerTests(unittest.TestCase):
    def _write(self, root: Path, name: str, payload: bytes) -> Path:
        path = root / name
        path.write_bytes(payload)
        path.chmod(0o400)
        return path

    def test_formal_private_fault_diagnostic_is_root_only_bounded_and_redacted(self) -> None:
        with tempfile.TemporaryDirectory(dir=TMP_PARENT) as raw:
            root = Path(raw) / "formal-private-audit"
            root.mkdir(mode=0o700)
            request_secret = "OPENMLE_PRIVATE_DIAGNOSTIC_SECRET_721a"
            request = {
                "schema": private_runner.REQUEST_SCHEMA,
                "task_id": "2d-datasets@1",
                "grader_binding_sha256": "1" * 64,
                "package_identity_sha256": "2" * 64,
                "metric_sha256": "3" * 64,
                "answer_sha256": "4" * 64,
                "submission_sha256": "5" * 64,
                "higher_is_better": True,
                "validator_success_forms": [request_secret],
                "metric_fd": 3,
                "answer_fd": 4,
                "submission_fd": 5,
                "timeout_ms": 7000,
            }
            sandbox = {
                "infrastructure_fault": True,
                "failure_class": "wall_timeout",
                "exit_code": None,
                "timed_out": True,
                "wall_seconds": 7.0,
                "managed_runtime_wall_seconds": 7.0,
                "cpu_seconds": 6.5,
                "peak_rss_bytes": 123456,
                "process_peak": 7,
                "execution_attempt_delta": 1,
                "execution_completed_delta": 0,
                "nested_subprocess_delta": 1,
                "fit_delta": 1,
                "stdout": request_secret.encode(),
                "stderr": request_secret.encode(),
            }
            environment = {
                "OPENMLE_FAST_PRIVATE_FAULT_AUDIT_ROOT": str(root),
                "OPENMLE_FAST_PROCESS_OWNER": "test-owner",
                "OPENMLE_FAST_RUN_ID": "test-run",
                "OPENMLE_FAST_PRIVATE_REQUEST_ID_SHA256": "6" * 64,
                "OPENMLE_FAST_PRIVATE_EPISODE_ID_SHA256": "7" * 64,
            }
            with (
                mock.patch.object(
                    common, "_parent_is_exact_remote_probe", return_value=False
                ),
                mock.patch.dict(os.environ, environment, clear=False),
            ):
                private_runner._write_probe_fault(
                    "sandbox_result", request=request, sandbox=sandbox
                )

            records = list(root.glob("runtime-fault-*.json"))
            self.assertEqual(len(records), 1)
            raw_payload = records[0].read_bytes()
            value = json.loads(raw_payload)
            self.assertLessEqual(len(raw_payload), 4096)
            self.assertEqual(stat.S_IMODE(root.stat().st_mode), 0o700)
            self.assertEqual(stat.S_IMODE(records[0].stat().st_mode), 0o600)
            self.assertEqual(value["schema"], "openmle_fast_private_runtime_fault_v1")
            self.assertEqual(value["run_id"], "test-run")
            self.assertEqual(value["process_owner"], "test-owner")
            self.assertEqual(value["request_id_sha256"], "6" * 64)
            self.assertEqual(value["episode_id_sha256"], "7" * 64)
            self.assertEqual(value["task_id"], "2d-datasets@1")
            self.assertEqual(value["submission_sha256"], "5" * 64)
            self.assertEqual(value["sandbox"]["failure_class"], "wall_timeout")
            self.assertNotIn(request_secret.encode(), raw_payload)

    def test_inherited_read_only_fd_and_exact_request(self) -> None:
        with tempfile.TemporaryDirectory(dir=TMP_PARENT) as raw:
            root = Path(raw)
            payloads = (b"metric", b"answer", b"submission")
            paths = [self._write(root, str(index), data) for index, data in enumerate(payloads)]
            descriptors = [os.open(path, os.O_RDONLY) for path in paths]
            try:
                request = {
                    "schema": private_runner.REQUEST_SCHEMA,
                    "task_id": "task@1",
                    "grader_binding_sha256": "1" * 64,
                    "package_identity_sha256": "2" * 64,
                    "metric_sha256": hashlib.sha256(payloads[0]).hexdigest(),
                    "answer_sha256": hashlib.sha256(payloads[1]).hexdigest(),
                    "submission_sha256": hashlib.sha256(payloads[2]).hexdigest(),
                    "higher_is_better": True,
                    "validator_success_forms": [],
                    "metric_fd": descriptors[0],
                    "answer_fd": descriptors[1],
                    "submission_fd": descriptors[2],
                    "timeout_ms": 1000,
                }
                self.assertEqual(private_runner._validate_request(request), tuple(descriptors))
                self.assertEqual(
                    private_runner._read_regular_fd(descriptors[2], 1024), payloads[2]
                )
                with self.assertRaises(common.RuntimeErrorClosed):
                    private_runner._validate_request(dict(request, metric_fd=descriptors[1]))
            finally:
                for descriptor in descriptors:
                    os.close(descriptor)

    def test_writeable_fd_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(dir=TMP_PARENT) as raw:
            path = Path(raw) / "input"
            path.write_bytes(b"x")
            descriptor = os.open(path, os.O_RDWR)
            try:
                with self.assertRaises(common.RuntimeErrorClosed):
                    private_runner._read_regular_fd(descriptor, 1024)
            finally:
                os.close(descriptor)

    def test_private_fd_read_obeys_overall_deadline(self) -> None:
        with tempfile.TemporaryDirectory(dir=TMP_PARENT) as raw:
            path = Path(raw) / "input"
            path.write_bytes(b"payload")
            path.chmod(0o400)
            descriptor = os.open(path, os.O_RDONLY)
            try:
                self.assertEqual(
                    private_runner._read_regular_fd(
                        descriptor, 1024, time.monotonic() + 1.0
                    ),
                    b"payload",
                )
                with self.assertRaises(common.RuntimeErrorClosed):
                    private_runner._read_regular_fd(
                        descriptor, 1024, time.monotonic() - 1.0
                    )
            finally:
                os.close(descriptor)

    def test_private_stage_cleanup_failure_is_propagated(self) -> None:
        with tempfile.TemporaryDirectory(dir=TMP_PARENT) as raw:
            run_root = Path(raw) / "runs"
            stage = run_root / ("private-stage-" + "a" * 32)
            workspace = stage / "workspace"
            workspace.mkdir(parents=True)
            with (
                mock.patch.object(common, "RUN_ROOT", str(run_root)),
                mock.patch.object(common, "exact_mount", return_value={"fstype": "tmpfs"}),
                mock.patch.object(
                    common,
                    "run_checked",
                    side_effect=common.RuntimeErrorClosed("unmount failed"),
                ),
            ):
                with self.assertRaises(common.RuntimeErrorClosed):
                    private_runner._cleanup_private_stage(
                        str(stage), str(workspace), time.monotonic() + 1.0
                    )

    def test_result_sanitization(self) -> None:
        valid = {
            "schema": private_runner.RESULT_SCHEMA,
            "classification": "graded",
            "native_score": 0.25,
            "higher_is_better": True,
        }
        self.assertEqual(private_runner._decode_and_sanitize(
            json.dumps(valid).encode(), True
        ), valid)
        leaked = dict(valid, private_path="/private/answer.csv")
        with self.assertRaises(common.RuntimeErrorClosed):
            private_runner._decode_and_sanitize(json.dumps(leaked).encode(), True)
        nonfinite = dict(valid, native_score=float("nan"))
        with self.assertRaises(common.RuntimeErrorClosed):
            private_runner._decode_and_sanitize(json.dumps(nonfinite).encode(), True)

    def test_native_metric_valid_invalid_and_single_call(self) -> None:
        class FakeSeries:
            def __init__(self, values):
                self.values = list(values)

            def __eq__(self, other):
                return FakeSeries(
                    left == right for left, right in zip(self.values, other.values)
                )

            def mean(self):
                return sum(bool(item) for item in self.values) / len(self.values)

        class FakeFrame:
            def __init__(self, columns, rows):
                self.columns = list(columns)
                self.rows = {name: list(values) for name, values in rows.items()}

            def copy(self):
                return FakeFrame(self.columns, self.rows)

            def __getitem__(self, name):
                return FakeSeries(self.rows[name])

        def read_csv(path):
            lines = Path(path).read_text().strip().splitlines()
            columns = lines[0].split(",")
            rows = {name: [] for name in columns}
            for line in lines[1:]:
                for name, value in zip(columns, line.split(",")):
                    rows[name].append(value)
            return FakeFrame(columns, rows)

        fake_pandas = types.SimpleNamespace(read_csv=read_csv)
        metric = b'''\
class NativeMetric:
    higher_is_better = True
    validate_calls = 0
    evaluate_calls = 0
    def validate_submission(self, prediction, truth):
        type(self).validate_calls += 1
        if type(self).validate_calls != 1:
            raise RuntimeError("validate called twice")
        return list(prediction.columns) == list(truth.columns)
    def evaluate(self, y_true, y_pred):
        type(self).evaluate_calls += 1
        if type(self).evaluate_calls != 1:
            raise RuntimeError("evaluate called twice")
        return float((y_true["y"] == y_pred["y"]).mean())
'''
        with tempfile.TemporaryDirectory(dir=TMP_PARENT) as raw:
            root = Path(raw)
            metric_path = self._write(root, "metric.py", metric)
            answer = self._write(root, "answer.csv", b"y\n1\n2\n")
            valid = self._write(root, "valid.csv", b"y\n1\n2\n")
            invalid = self._write(root, "invalid.csv", b"z\n1\n2\n")
            with mock.patch.dict(sys.modules, {"pandas": fake_pandas}):
                graded = private_worker._grade(
                    str(metric_path), str(answer), str(valid), True, ()
                )
                self.assertEqual(graded["classification"], "graded")
                self.assertEqual(graded["native_score"], 1.0)
                rejected = private_worker._grade(
                    str(metric_path), str(answer), str(invalid), True, ()
                )
                self.assertEqual(rejected["classification"], "invalid_submission")
                self.assertIsNone(rejected["native_score"])

    def test_admitted_spearman_domain_fault_is_invalid(self) -> None:
        class FakeFrame:
            def __init__(self, columns):
                self.columns = list(columns)

            def copy(self):
                return FakeFrame(self.columns)

        fake_pandas = types.SimpleNamespace(
            read_csv=lambda path: FakeFrame(["id", "score"])
        )
        metric = b'''\
class NativeMetric:
    higher_is_better = True
    def validate_submission(self, prediction, truth):
        return "Submission is valid."
    def evaluate(self, y_true, y_pred):
        raise Exception("Spearman correlation is undefined for the provided data.")
'''
        with tempfile.TemporaryDirectory(dir=TMP_PARENT) as raw:
            root = Path(raw)
            metric_path = self._write(root, "metric.py", metric)
            answer = self._write(root, "answer.csv", b"id,target\n1,0\n2,1\n")
            submission = self._write(
                root, "submission.csv", b"id,score\n1,0.5\n2,0.5\n"
            )
            with mock.patch.dict(sys.modules, {"pandas": fake_pandas}):
                rejected = private_worker._grade(
                    str(metric_path),
                    str(answer),
                    str(submission),
                    True,
                    ("Submission is valid.",),
                )
            self.assertEqual(rejected["classification"], "invalid_submission")
            self.assertIsNone(rejected["native_score"])

    def test_nonfinite_scores_are_invalid_but_score_contract_drift_escapes(self) -> None:
        class FakeFrame:
            def copy(self):
                return self

        fake_pandas = types.SimpleNamespace(read_csv=lambda path: FakeFrame())
        with tempfile.TemporaryDirectory(dir=TMP_PARENT) as raw:
            root = Path(raw)
            answer = self._write(root, "answer.csv", b"y\n1\n")
            submission = self._write(root, "submission.csv", b"y\n1\n")
            for label, expression in (
                ("nan", "float('nan')"),
                ("positive infinity", "float('inf')"),
                ("negative infinity", "float('-inf')"),
            ):
                metric_path = self._write(
                    root,
                    "metric_" + label.replace(" ", "_") + ".py",
                    ("class NativeMetric:\n"
                     "    higher_is_better = True\n"
                     "    def validate_submission(self, prediction, truth): return True\n"
                     "    def evaluate(self, y_true, y_pred): return " + expression + "\n").encode(),
                )
                with mock.patch.dict(sys.modules, {"pandas": fake_pandas}):
                    result = private_worker._grade(
                        str(metric_path), str(answer), str(submission), True, ()
                    )
                self.assertEqual(result["classification"], "invalid_submission", label)
            for label, expression in (("bool", "True"), ("string", "'0.5'")):
                metric_path = self._write(
                    root,
                    "metric_" + label + ".py",
                    ("class NativeMetric:\n"
                     "    higher_is_better = True\n"
                     "    def validate_submission(self, prediction, truth): return True\n"
                     "    def evaluate(self, y_true, y_pred): return " + expression + "\n").encode(),
                )
                with mock.patch.dict(sys.modules, {"pandas": fake_pandas}):
                    with self.assertRaises(TypeError, msg=label):
                        private_worker._grade(
                            str(metric_path), str(answer), str(submission), True, ()
                        )

    def test_evaluator_runtime_and_control_faults_reach_worker_infrastructure_boundary(self) -> None:
        class FakeFrame:
            def copy(self):
                return self

        fake_pandas = types.SimpleNamespace(read_csv=lambda path: FakeFrame())
        fault_types = (
            RuntimeError,
            MemoryError,
            SystemExit,
            KeyboardInterrupt,
            GeneratorExit,
        )
        with tempfile.TemporaryDirectory(dir=TMP_PARENT) as raw:
            root = Path(raw)
            answer = self._write(root, "answer.csv", b"y\n1\n")
            submission = self._write(root, "submission.csv", b"y\n1\n")
            for fault_type in fault_types:
                metric_path = self._write(
                    root,
                    "metric_" + fault_type.__name__ + ".py",
                    ("class NativeMetric:\n"
                     "    higher_is_better = True\n"
                     "    def validate_submission(self, prediction, truth): return True\n"
                     "    def evaluate(self, y_true, y_pred): raise "
                     + fault_type.__name__ + "('probe')\n").encode(),
                )
                with mock.patch.dict(sys.modules, {"pandas": fake_pandas}):
                    with self.assertRaises(fault_type):
                        private_worker._grade(
                            str(metric_path), str(answer), str(submission), True, ()
                        )
                written = []
                with (
                    mock.patch.object(
                        private_worker,
                        "_grade",
                        side_effect=fault_type("probe"),
                    ),
                    mock.patch.object(
                        private_worker,
                        "_parse_arguments",
                        return_value=(True, ()),
                    ),
                    mock.patch.object(
                        private_worker,
                        "SAFE_WRITE",
                        side_effect=lambda descriptor, payload: written.append(payload),
                    ),
                ):
                    self.assertEqual(private_worker.main(["private_worker"]), 0)
                self.assertEqual(len(written), 1)
                result = json.loads(written[0])
                self.assertEqual(result["classification"], "infrastructure_fault")

    def test_metric_load_construction_truth_and_direction_faults_stay_outside_rejection(self) -> None:
        class FakeFrame:
            def copy(self):
                return self

        metric_import_fault = b"raise RuntimeError('metric import fault')\n"
        metric_construction_fault = b'''\
class NativeMetric:
    higher_is_better = True
    def __init__(self): raise RuntimeError("metric construction fault")
    def validate_submission(self, prediction, truth): return True
    def evaluate(self, y_true, y_pred): return 0.5
'''
        metric_direction_drift = b'''\
class NativeMetric:
    higher_is_better = False
    def validate_submission(self, prediction, truth): return True
    def evaluate(self, y_true, y_pred): return 0.5
'''
        with tempfile.TemporaryDirectory(dir=TMP_PARENT) as raw:
            root = Path(raw)
            answer = self._write(root, "answer.csv", b"y\n1\n")
            submission = self._write(root, "submission.csv", b"y\n1\n")
            for label, metric in (
                ("import", metric_import_fault),
                ("construction", metric_construction_fault),
                ("direction", metric_direction_drift),
            ):
                metric_path = self._write(root, "metric_" + label + ".py", metric)
                fake_pandas = types.SimpleNamespace(read_csv=lambda path: FakeFrame())
                with mock.patch.dict(sys.modules, {"pandas": fake_pandas}):
                    with self.assertRaises((RuntimeError, ValueError), msg=label):
                        private_worker._grade(
                            str(metric_path), str(answer), str(submission), True, ()
                        )
            calls = 0
            def read_csv_with_truth_fault(path):
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise RuntimeError("truth load fault")
                return FakeFrame()
            metric_path = self._write(
                root,
                "metric_truth.py",
                b"class NativeMetric:\n"
                b"    higher_is_better = True\n"
                b"    def validate_submission(self, prediction, truth): return True\n"
                b"    def evaluate(self, y_true, y_pred): return 0.5\n",
            )
            fake_pandas = types.SimpleNamespace(read_csv=read_csv_with_truth_fault)
            with mock.patch.dict(sys.modules, {"pandas": fake_pandas}):
                with self.assertRaises(RuntimeError):
                    private_worker._grade(
                        str(metric_path), str(answer), str(submission), True, ()
                    )

if __name__ == "__main__":
    unittest.main()
