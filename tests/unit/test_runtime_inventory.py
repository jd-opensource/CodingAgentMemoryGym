"""Content-identity checks only; no native binary or sandbox is executed."""
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def common_module():
    spec = importlib.util.spec_from_file_location("inventory_test_common", ROOT / "runtimes/autoresearch/runtime_common.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def inventory(tmp_path, monkeypatch):
    common = common_module()
    names = ("bin/openmle-sandbox-supervisor", "bin/openmle-python-wrapper", "fit_hook.py")
    monkeypatch.setattr(common, "ARTIFACT_LOCK_MEMBERS", names)
    for index, name in enumerate(names):
        path = tmp_path / name
        path.parent.mkdir(exist_ok=True)
        path.write_bytes(f"unit-test rebuild {index}; not an executable".encode())
    def write_lock():
        value = {"schema": "openmle_fast_runtime_artifact_lock_v1", "runtime_digest": common.RUNTIME_DIGEST,
                 "files": [{"path": name, "sha256": hashlib.sha256((tmp_path / name).read_bytes()).hexdigest()} for name in names]}
        path = tmp_path / "artifact-lock.json"
        path.write_text(json.dumps(value))
        return hashlib.sha256(path.read_bytes()).hexdigest()
    return common, tmp_path, names, write_lock


def test_content_identity_comes_from_verified_build(inventory):
    common, root, names, write_lock = inventory
    digest = write_lock()
    expected = common.verified_component_digests(digest, str(root))
    assert expected == dict(zip(("supervisor", "python_wrapper", "fit_hook"),
                               [hashlib.sha256((root / name).read_bytes()).hexdigest() for name in names]))
    # A deliberate rebuild gets a new, explicit identity, not inherited hashes.
    (root / names[0]).write_bytes(b"another unit-test build")
    assert common.verified_component_digests(digest, str(root)) is None
    assert common.verified_component_digests(write_lock(), str(root)) != expected


@pytest.mark.parametrize("which", [0, 1, 2])
def test_tampered_component_is_rejected(inventory, which):
    common, root, names, write_lock = inventory
    digest = write_lock()
    (root / names[which]).write_bytes(b"changed after the recorded build")
    assert common.verified_component_digests(digest, str(root)) is None


def test_tampered_or_missing_inventory_is_rejected(inventory):
    common, root, _names, write_lock = inventory
    digest = write_lock()
    (root / "artifact-lock.json").write_text("{}")
    assert common.verified_component_digests(digest, str(root)) is None
    (root / "artifact-lock.json").unlink()
    assert common.verified_component_digests(digest, str(root)) is None


def test_symlink_is_not_a_valid_component(inventory):
    common, root, names, write_lock = inventory
    digest = write_lock()
    path = root / names[0]
    preserved = root / "original"
    path.rename(preserved)
    path.symlink_to(preserved)
    assert common.verified_component_digests(digest, str(root)) is None


def test_original_security_checks_remain_in_preflight():
    common = common_module()
    import inspect
    code = inspect.getsource(common.active_preflight)
    for check in ("root_identity", "cgroup_v1_or_hybrid", "rootfs_identity", "artifact_install_inventory"):
        assert check in code
    assert "all_checks_pass" in inspect.getsource(common.require_runtime_admission)
    assert "boot_id()" in inspect.getsource(common._admission_stamp_valid)
