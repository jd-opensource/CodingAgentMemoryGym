#!/usr/bin/env python3
"""Enable the teacher log-probability request API in SGLang 0.5.12."""
import argparse
import hashlib
import importlib.metadata
from pathlib import Path


BASE_SHA256 = "69b4aa9d6456f571796275db62606be1bcb573427dd56ec8d7e204ab8d52d52f"


def patched_source(source):
    if "detokenize: bool = True," in source and "self.detokenize = detokenize" in source:
        return source
    digest = hashlib.sha256(source.encode()).hexdigest()
    if digest != BASE_SHA256:
        raise ValueError("SamplingParams source differs from SGLang 0.5.12")
    source = source.replace("        sampling_seed: Optional[int] = None,\n", "        sampling_seed: Optional[int] = None,\n        detokenize: bool = True,\n", 1)
    source = source.replace("        self.sampling_seed = sampling_seed\n", "        self.sampling_seed = sampling_seed\n        self.detokenize = detokenize\n", 1)
    return source


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-packages", type=Path)
    args = parser.parse_args()
    if args.site_packages:
        root = args.site_packages
    else:
        dist = importlib.metadata.distribution("sglang")
        if dist.version != "0.5.12":
            raise ValueError("Install sglang==0.5.12")
        root = Path(dist.locate_file(""))
    path = root / "sglang/srt/sampling/sampling_params.py"
    source = path.read_text()
    patched = patched_source(source)
    if patched != source:
        path.write_text(patched)
    print("SGLang teacher sampling API ready")


if __name__ == "__main__":
    main()
