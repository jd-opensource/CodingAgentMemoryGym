"""Prepare the selected CAMG-II task data; never substitute a different task pool."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import tarfile
import tempfile
import urllib.request

DATA = Path(__file__).resolve().parent / "data"
OPENMLE_REVISION = "f56e4b31252a9b81d95fea100098cd49b7290398"
OPENMLE_URL = f"https://huggingface.co/datasets/FrontisAI/OpenMLE-Tasks/resolve/{OPENMLE_REVISION}"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".partial")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    temporary.replace(path)


def checked_bytes(path: Path, expected: str) -> bytes:
    content = path.read_bytes()
    if hashlib.sha256(content).hexdigest() != expected:
        raise ValueError(f"Content checksum mismatch: {path}")
    return content


def download(url: str, destination: Path, digest: str) -> None:
    if destination.exists():
        if sha256(destination) != digest:
            raise ValueError(f"Existing download has a different checksum: {destination}")
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.name + ".partial")
    request = urllib.request.Request(url, headers={"User-Agent": "CodingAgentMemoryGym/0.1"})
    with urllib.request.urlopen(request, timeout=120) as response, temporary.open("wb") as out:
        shutil.copyfileobj(response, out)
    if sha256(temporary) != digest:
        raise ValueError(f"Downloaded content checksum mismatch: {url}")
    temporary.replace(destination)


def extract_regular_archive(archive: Path, destination: Path) -> None:
    """Extract only ordinary files/directories, with traversal and size checks."""
    import zstandard
    if destination.is_symlink() or (destination.exists() and any(destination.iterdir())):
        raise ValueError("Archive extraction requires an empty, non-symlink directory")
    destination.mkdir(parents=True, exist_ok=True)
    total = 0
    seen = set()
    with archive.open("rb") as compressed, zstandard.ZstdDecompressor().stream_reader(compressed) as reader:
        with tarfile.open(fileobj=reader, mode="r|") as tar:
            for member in tar:
                relative = PurePosixPath(member.name)
                if relative.is_absolute() or ".." in relative.parts or "\\" in member.name or "\0" in member.name:
                    raise ValueError(f"Unsafe archive member: {member.name}")
                target = destination.joinpath(*relative.parts)
                if member.isdir():
                    target.mkdir(parents=True, exist_ok=True)
                    continue
                if not member.isfile() or target in seen:
                    raise ValueError(f"Archive member is not a unique ordinary file: {member.name}")
                total += member.size
                if total > 12 * 1024**3:
                    raise ValueError("Task archive exceeds the preparation size limit")
                seen.add(target)
                target.parent.mkdir(parents=True, exist_ok=True)
                with tar.extractfile(member) as source, target.open("xb") as output:
                    shutil.copyfileobj(source, output)


def prepare_coding(args) -> None:
    import pyarrow.parquet as pq
    manifest = json.loads((DATA / "coding/manifest.json").read_text())
    source = args.source
    if args.download:
        from camg.hub import download_dataset
        source = download_dataset(args.output / "dataset", "coding", assets_only=True) / "assets/coding"
    if source is None:
        raise ValueError("Supply --source containing the pinned parquet files or --download")
    parquet = sorted(source.rglob("train-*.parquet"))
    if len(parquet) != len(manifest["shards"]):
        raise ValueError(f"Expected {len(manifest['shards'])} parquet shards, found {len(parquet)}")
    args.output.mkdir(parents=True, exist_ok=True)
    for file, spec in zip(parquet, manifest["shards"]):
        destination = args.output / spec["path"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_suffix(".partial")
        with temporary.open("w", encoding="utf-8") as stream:
            for batch in pq.ParquetFile(file).iter_batches(batch_size=512):
                for row in batch.to_pylist():
                    stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")
        if sha256(temporary) != spec["sha256"]:
            raise ValueError(f"Converted shard differs from the selected dataset: {file.name}")
        temporary.replace(destination)
    shutil.copyfile(DATA / "coding/train_ids.json", args.output / "train_ids.json")
    shutil.copyfile(DATA / "coding/images.json", args.output / "images.json")
    write_json(args.output / "manifest.json", manifest)
    from camg.services.coding.dataset import SwesmithDataset
    dataset = SwesmithDataset(args.output / "manifest.json")
    expected = json.loads((DATA / "coding/index.json").read_text())
    for row in expected:
        if dataset[row["data_idx"]].instance_id != row["instance_id"]:
            raise ValueError(f"Coding task order changed at index {row['data_idx']}")
    write_json(args.output / "prepared.json", {"environment": "Coding", "tasks": len(expected),
        "manifest_sha256": sha256(args.output / "manifest.json"), "task_order_verified": True})


def copy_verified(source: Path, target: Path, digest: str, mode=0o444) -> None:
    content = checked_bytes(source, digest)
    if target.exists():
        checked_bytes(target, digest)
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content)
    target.chmod(mode)


def materialize_autoresearch_task(archive: Path, output: Path, record: dict, private: dict) -> None:
    with tempfile.TemporaryDirectory(prefix="camg-task-") as directory:
        raw = Path(directory)
        extract_regular_archive(archive, raw)
        for spec in record["public_files"]:
            relative = spec["path"]
            source = DATA / "autoresearch/instructions" / (record["task_id"] + ".md") if relative == "TASK.md" else raw / "data/public" / relative.removeprefix("data/")
            copy_verified(source, output / record["public_task_relpath"] / relative, spec["sha256"], spec["mode"])
        for spec in record["provenance_files"]:
            copy_verified(raw / spec["path"], output / record["provenance_relpath"] / spec["path"], spec["sha256"], spec["mode"])
        copy_verified(raw / "data/private/test_answer.csv", output / "private-grader" / private["answer_relpath"], private["answer_sha256"])
        copy_verified(raw / "utils/metric.py", output / "private-grader" / private["metric_relpath"], private["metric_sha256"])


def prepare_autoresearch(args) -> None:
    if not args.accept_upstream_terms:
        raise ValueError("Review per-task source terms first, then pass --accept-upstream-terms; this flag does not grant permission")
    args.output.mkdir(parents=True, exist_ok=True)
    acquisition = json.loads((DATA / "autoresearch/acquisition.json").read_text())
    manifests = {split: json.loads((DATA / f"autoresearch/{split}.json").read_text()) for split in ("train", "heldout")}
    public = {row["task_id"]: row for manifest in manifests.values() for row in manifest["records"]}
    private_manifest = json.loads((DATA / "autoresearch/grader.json").read_text())
    private = {row["task_id"]: row for row in private_manifest["records"]}
    selected = [entry for entry in acquisition if not args.task_id or entry["task_id"] == args.task_id]
    if not selected:
        raise ValueError("Task ID is not in the CAMG-II selection")
    downloaded_source = None
    if args.download and (not args.task_id or selected[0]["package"]):
        from camg.hub import download_dataset
        root = download_dataset(args.output / "dataset", "autoresearch", assets_only=True,
            task_id=args.task_id)
        downloaded_source = root / "assets/autoresearch/archives"
    missing = []
    completed = []
    for entry in selected:
        task = entry["task_id"]
        record = public[task]
        archive = args.output / record["archive_relpath"]
        supplied = None if args.source is None else args.source / (task + ".tar.zst")
        if (supplied is None or not supplied.is_file()) and downloaded_source is not None:
            supplied = downloaded_source / (task + ".tar.zst")
        if supplied is not None and supplied.is_file():
            copy_verified(supplied, archive, entry["required_archive_sha256"])
        if not archive.is_file():
            missing.append({"task_id": task, "required_archive_sha256": entry["required_archive_sha256"],
                "source": entry["upstream_index_records"]})
            continue
        if sha256(archive) != entry["required_archive_sha256"]:
            raise ValueError(f"Task archive identity mismatch: {task}")
        materialize_autoresearch_task(archive, args.output, record, private[task])
        completed.append(task)
    for split in manifests:
        shutil.copyfile(DATA / f"autoresearch/{split}.json", args.output / f"{split}.json")
    shutil.copyfile(DATA / "autoresearch/grader.json", args.output / "grader.json")
    report = {"environment": "AutoResearch", "completed": completed, "missing": missing,
        "full_selection": not args.task_id, "ready": not missing and not args.task_id}
    write_json(args.output / "preparation.json", report)
    if missing:
        raise RuntimeError(f"{len(missing)} selected task archives are still missing; see preparation.json and docs/data.md. No tasks were silently removed.")


def prepare_mimo(args) -> None:
    import pyarrow as pa
    import pyarrow.parquet as pq
    source_dir = DATA / args.environment
    source = json.loads((source_dir / "source.json").read_text())
    content = checked_bytes(source_dir / "tasks.jsonl", source["sha256"])
    rows = [json.loads(line) for line in content.splitlines()]
    if args.environment == "general":
        if args.download:
            from camg.hub import download_dataset
            downloaded = download_dataset(args.output / "dataset", "general", assets_only=True)
            args.source = downloaded / "assets/general/envs"
        if args.source is None:
            raise ValueError("General requires --source pointing to the downloaded general/envs directory, or --download")
        for row in rows:
            instance = json.loads(row["extra_info"]["instance_json"])
            task_root = args.source.resolve() / instance["instance_id"]
            for name in ("instruction.md", "manifest.json", "verify.py", "sidecar_entrypoint.py"):
                if not (task_root / name).is_file():
                    raise FileNotFoundError(task_root / name)
            instance["env_task_dir"] = str(task_root)
            row["extra_info"]["instance_json"] = json.dumps(instance, ensure_ascii=False)
    args.output.mkdir(parents=True, exist_ok=True)
    target = args.output / "tasks.parquet"
    pq.write_table(pa.Table.from_pylist(rows), target)
    write_json(args.output / "prepared.json", {"environment": args.environment, "tasks": len(rows),
        "source_sha256": source["sha256"], "parquet_sha256": sha256(target),
        "asset_download_revision": source["asset_download_revision"],
        "containers_and_verifiers_executed": False})


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--environment", choices=("coding", "autoresearch", "general", "visual"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source", type=Path, help="Already downloaded upstream assets; see docs/data.md")
    parser.add_argument("--download", action="store_true", help="Download the selected assets from the pinned CAMG-II dataset release")
    parser.add_argument("--accept-upstream-terms", action="store_true")
    parser.add_argument("--task-id", help="Prepare one AutoResearch task for installation testing, not a reduced training pool")
    args = parser.parse_args(argv)
    args.output = args.output.expanduser().resolve()
    if args.task_id and args.environment != "autoresearch":
        parser.error("--task-id is only supported for AutoResearch")
    {"coding": prepare_coding, "autoresearch": prepare_autoresearch,
     "general": prepare_mimo, "visual": prepare_mimo}[args.environment](args)


if __name__ == "__main__":
    main()
