import hashlib
import json
from pathlib import Path
import sys
from types import SimpleNamespace

import pytest

from camg import hub


def test_release_file_selection():
    files = {name: {} for name in (
        "README.md", "LICENSES.md", "metadata/train_schedule.jsonl", "licenses/source.txt",
        "tasks/general/pool.parquet", "assets/general/envs/example/input.csv",
        "metadata/general/tasks.jsonl", "tasks/coding/train.parquet",
        "assets/autoresearch/archives/example@1.tar.zst",
    )}
    manifest = {"files": files}
    general = hub.selected_files(manifest, "general")
    assert "tasks/coding/train.parquet" not in general
    assert "metadata/train_schedule.jsonl" in general
    assert "licenses/source.txt" in general
    assert hub.selected_files(manifest, "general", assets_only=True) == ["assets/general/envs/example/input.csv"]
    assert hub.selected_files(manifest, "autoresearch", task_id="example@1") == ["assets/autoresearch/archives/example@1.tar.zst"]
    assert hub.selected_files(manifest, "all") == sorted(files)


@pytest.mark.parametrize("path", ["../secret", "/tmp/secret", "a/../../secret", "a\\b", "x\0y", ""])
def test_invalid_release_paths(path):
    with pytest.raises(ValueError):
        hub.selected_files({"files": {path: {}}}, "all")


def test_both_checksum_formats_and_corruption(tmp_path):
    data = b"dataset contents\n"
    file = tmp_path / "data"
    file.write_bytes(data)
    sha = hashlib.sha256(data).hexdigest()
    blob = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
    hub.verify_file(file, {"size": len(data), "sha256": sha})
    hub.verify_file(file, {"size": len(data), "git_blob_sha1": blob})
    with pytest.raises(ValueError, match="checksum"):
        hub.verify_file(file, {"size": len(data), "sha256": "0" * 64})
    with pytest.raises(ValueError, match="size"):
        hub.verify_file(file, {"size": len(data) + 1, "sha256": sha})


def test_download_is_revision_and_manifest_bound(tmp_path, monkeypatch):
    name = "assets/general/envs/example/input.txt"
    data = b"example"
    manifest = {"files": {name: {"size": len(data), "sha256": hashlib.sha256(data).hexdigest()}}}
    raw = json.dumps(manifest).encode()
    revision = "a" * 40
    monkeypatch.setattr(hub, "release_spec", lambda: {
        "repo_id": "owner/data", "revision": revision, "manifest_sha256": hashlib.sha256(raw).hexdigest(),
    })
    calls = []
    def fetch(repo, filename, **kwargs):
        assert repo == "owner/data" and kwargs["revision"] == revision
        target = Path(kwargs["local_dir"]) / filename
        target.write_bytes(raw)
        return str(target)
    def snapshot(repo, **kwargs):
        assert kwargs["revision"] == revision
        calls.append(kwargs["allow_patterns"])
        target = Path(kwargs["local_dir"]) / name
        target.parent.mkdir(parents=True)
        target.write_bytes(data)
    monkeypatch.setitem(sys.modules, "huggingface_hub", SimpleNamespace(hf_hub_download=fetch, snapshot_download=snapshot))
    assert hub.download_dataset(tmp_path, "general", assets_only=True) == tmp_path
    assert calls == [["assets/general/**"]]
    monkeypatch.setattr(hub, "release_spec", lambda: {
        "repo_id": "owner/data", "revision": revision, "manifest_sha256": "0" * 64,
    })
    with pytest.raises(ValueError, match="manifest"):
        hub.download_dataset(tmp_path, "general")


def test_missing_archive_is_not_a_reduced_task_set():
    assert hub.selected_files({"files": {}}, "autoresearch", task_id="recipe-only@1") == []
    with pytest.raises(ValueError):
        hub.selected_files({"files": {}}, "general", task_id="example")


def test_shop_source_matches_native_index():
    spec = json.loads((hub.DATA / "shop/catalog.json").read_text())
    assert len(spec["revision"]) == 40
    expected = (hub.DATA / "shop/lucene.sha256").read_text().splitlines()
    for line in expected:
        digest, name = line.split()
        assert spec["files"]["search_engine/indexes-full/" + name.removeprefix("./")]["sha256"] == digest
    assert "items_shuffle.json" in spec["files"]
    assert "items_ins_v2.json" in spec["files"]
