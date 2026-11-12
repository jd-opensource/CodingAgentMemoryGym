import hashlib
import io
import json
from pathlib import Path
from types import SimpleNamespace
import tarfile

import pyarrow.parquet as pq
import pytest
import zstandard

from camg.prepare import DATA, checked_bytes, copy_verified, extract_regular_archive, prepare_mimo


def archive(tmp_path, members):
    contents = io.BytesIO()
    with tarfile.open(fileobj=contents, mode="w") as tar:
        for name, kind, payload in members:
            member = tarfile.TarInfo(name)
            member.type = kind
            if kind == tarfile.REGTYPE:
                member.size = len(payload)
                tar.addfile(member, io.BytesIO(payload))
            else:
                member.linkname = payload.decode()
                tar.addfile(member)
    path = tmp_path / "task.tar.zst"
    path.write_bytes(zstandard.ZstdCompressor().compress(contents.getvalue()))
    return path


def test_extract_regular_files(tmp_path):
    path = archive(tmp_path, [("data/public/a.csv", tarfile.REGTYPE, b"x\n1\n")])
    output = tmp_path / "out"
    extract_regular_archive(path, output)
    assert (output / "data/public/a.csv").read_bytes() == b"x\n1\n"
    with pytest.raises(ValueError, match="empty"):
        extract_regular_archive(path, output)


@pytest.mark.parametrize("name,kind,payload", [
    ("../escape", tarfile.REGTYPE, b"bad"), ("/escape", tarfile.REGTYPE, b"bad"),
    ("a\\b", tarfile.REGTYPE, b"bad"), ("link", tarfile.SYMTYPE, b"/tmp"),
    ("link", tarfile.LNKTYPE, b"target"), ("pipe", tarfile.FIFOTYPE, b""),
])
def test_extract_rejects_unsafe_members(tmp_path, name, kind, payload):
    with pytest.raises(ValueError):
        extract_regular_archive(archive(tmp_path, [(name, kind, payload)]), tmp_path / "out")


def test_extract_rejects_duplicate_files_and_symlink_destination(tmp_path):
    path = archive(tmp_path, [("a", tarfile.REGTYPE, b"x"), ("a", tarfile.REGTYPE, b"y")])
    with pytest.raises(ValueError, match="unique"):
        extract_regular_archive(path, tmp_path / "out")
    real = tmp_path / "real"
    real.mkdir()
    link = tmp_path / "link"
    link.symlink_to(real, target_is_directory=True)
    with pytest.raises(ValueError, match="symlink"):
        extract_regular_archive(path, link)


def test_verified_copy_never_accepts_different_content(tmp_path):
    source, target = tmp_path / "source", tmp_path / "target"
    source.write_bytes(b"original")
    expected = hashlib.sha256(b"original").hexdigest()
    copy_verified(source, target, expected)
    copy_verified(source, target, expected)
    assert target.stat().st_mode & 0o777 == 0o444
    assert checked_bytes(target, expected) == b"original"
    with pytest.raises(ValueError, match="checksum"):
        copy_verified(source, target, "0" * 64)


def test_visual_jsonl_to_parquet_is_lossless(tmp_path):
    args = SimpleNamespace(environment="visual", output=tmp_path, source=None, download=False)
    prepare_mimo(args)
    expected = [json.loads(line) for line in (DATA / "visual/tasks.jsonl").read_text().splitlines()]
    assert pq.read_table(tmp_path / "tasks.parquet").to_pylist() == expected
    report = json.loads((tmp_path / "prepared.json").read_text())
    assert report["tasks"] == 500
    assert report["containers_and_verifiers_executed"] is False


def test_general_requires_real_assets(tmp_path):
    args = SimpleNamespace(environment="general", output=tmp_path / "out", source=tmp_path, download=False)
    with pytest.raises(FileNotFoundError):
        prepare_mimo(args)
    assert not args.output.exists()
