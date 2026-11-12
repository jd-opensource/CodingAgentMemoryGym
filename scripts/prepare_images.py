#!/usr/bin/env python3
"""Materialize the selected, digest-pinned Coding/AutoResearch root filesystems."""
import argparse
import json
from pathlib import Path
import shlex
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def command(args):
    manifest = json.loads((ROOT / "camg/data/coding/images.json").read_text())
    selected = [row for row in manifest["images"] if not args.image or row["image"] == args.image]
    if not selected:
        raise ValueError("Image is not part of the selected manifest")
    upstream = manifest["upstream"]
    cmd = [sys.executable, str(ROOT / "scripts/prepare_oci_rootfs.py"),
           "--cache-root", str(args.cache_root), "--crane", str(args.crane),
           "--transport-prefix", "index.docker.io", "--dataset-revision", upstream["dataset_revision"],
           "--source-revision", upstream["source_revision"], "--image-manifest-output", str(args.output)]
    for row in selected:
        cmd.extend(["--binding", f"{row['image']}={row['image']}@{row['digest']}"])
    return cmd


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache-root", type=Path, required=True)
    parser.add_argument("--crane", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--image", help="Prepare one named image for an installation check")
    parser.add_argument("--print-command", action="store_true")
    args = parser.parse_args()
    cmd = command(args)
    if args.print_command:
        print(shlex.join(cmd))
    else:
        if sys.platform != "linux":
            raise RuntimeError("Root filesystem preparation requires Linux")
        subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
