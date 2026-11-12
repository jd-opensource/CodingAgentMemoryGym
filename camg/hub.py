"""Download and verify the published CAMG-II task data and environment assets."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath

DATA = Path(__file__).resolve().parent / "data"
ENVIRONMENTS = ("shop", "coding", "autoresearch", "general", "visual")


def release_spec() -> dict:
    return json.loads((DATA / "hub.json").read_text())


def validate_path(name: str) -> None:
    path = PurePosixPath(name)
    if not name or path.is_absolute() or ".." in path.parts or "\\" in name or "\0" in name:
        raise ValueError(f"Invalid dataset path: {name!r}")


def verify_file(path: Path, spec: dict) -> None:
    if not path.is_file() or path.stat().st_size != spec["size"]:
        raise ValueError(f"Dataset file missing or has the wrong size: {path}")
    digest = hashlib.sha256() if "sha256" in spec else hashlib.sha1()
    if "sha256" not in spec:
        digest.update(f"blob {spec['size']}\0".encode())
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    expected = spec.get("sha256", spec.get("git_blob_sha1"))
    if digest.hexdigest() != expected:
        raise ValueError(f"Dataset checksum mismatch: {path}")


def selected_files(manifest: dict, environment: str, *, assets_only=False, task_id=None) -> list[str]:
    if environment not in (*ENVIRONMENTS, "all"):
        raise ValueError(f"Unknown environment: {environment}")
    if task_id is not None and environment != "autoresearch":
        raise ValueError("A task ID can only select an AutoResearch archive")
    chosen = []
    for name in manifest["files"]:
        validate_path(name)
        if task_id is not None:
            match = name == f"assets/autoresearch/archives/{task_id}.tar.zst"
        elif assets_only:
            match = name.startswith("assets/") if environment == "all" else name.startswith(f"assets/{environment}/")
        else:
            match = environment == "all" or name.startswith(tuple(
                f"{root}/{environment}/" for root in ("assets", "tasks", "metadata")
            )) or name.startswith("licenses/") or name in ("README.md", "LICENSES.md", "metadata/train_schedule.jsonl")
        if match:
            chosen.append(name)
    return sorted(chosen)


def download_dataset(output: Path, environment="all", *, assets_only=False, task_id=None) -> Path:
    from huggingface_hub import hf_hub_download, snapshot_download

    release = release_spec()
    root = output.expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    filename = "manifest.json"
    manifest_path = Path(hf_hub_download(release["repo_id"], filename,
        repo_type="dataset", revision=release["revision"], local_dir=root))
    if hashlib.sha256(manifest_path.read_bytes()).hexdigest() != release["manifest_sha256"]:
        raise ValueError("The published dataset manifest differs from this code release")
    manifest = json.loads(manifest_path.read_text())
    names = selected_files(manifest, environment, assets_only=assets_only, task_id=task_id)
    if task_id is not None and not names:
        raise ValueError(f"{task_id} uses upstream recipe reconstruction; see docs/data.md")
    if names:
        if task_id is not None:
            patterns = names
        elif assets_only:
            patterns = ["assets/**"] if environment == "all" else [f"assets/{environment}/**"]
        else:
            patterns = ["**"] if environment == "all" else [
                f"{section}/{environment}/**" for section in ("assets", "tasks", "metadata")
            ] + ["licenses/**", "README.md", "LICENSES.md", "metadata/train_schedule.jsonl"]
        snapshot_download(release["repo_id"], repo_type="dataset", revision=release["revision"],
            allow_patterns=patterns, local_dir=root)
        for name in names:
            path = root / name
            if not path.resolve().is_relative_to(root):
                raise ValueError(f"Dataset path escapes the output directory: {name}")
            verify_file(path, manifest["files"][name])
    return root


def download_shop_catalog(output: Path) -> Path:
    """Fetch the original Shop assets without redistributing the catalog."""
    from huggingface_hub import snapshot_download

    spec = json.loads((DATA / "shop/catalog.json").read_text())
    root = output.expanduser().resolve()
    for name in spec["files"]:
        validate_path(name)
    snapshot_download(spec["repo_id"], repo_type="dataset", revision=spec["revision"],
        allow_patterns=list(spec["files"]), local_dir=root)
    for name, expected in spec["files"].items():
        if not (root / name).resolve().is_relative_to(root):
            raise ValueError(f"Catalog path escapes the output directory: {name}")
        verify_file(root / name, expected)
    return root
