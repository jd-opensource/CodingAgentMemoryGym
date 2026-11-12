#!/usr/bin/env python3
"""Check source syntax, local documentation links and common accidental disclosures.

This is a source-only check, not a security certification or runtime test.
"""
import ast
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


def main():
    names = subprocess.check_output(
        ["git", "-C", str(ROOT), "ls-files", "--cached", "--others", "--exclude-standard", "-z"]
    ).decode().split("\0")
    patterns = {
        "private home directory": r"/Users/(?!name(?:/|\b))[A-Za-z0-9._-]+/",
        "private infrastructure path": r"/(?:home/ai-jingyan|mnt/amg-nfs|root/jd-coding)(?:/|\b)",
        "private infrastructure hostname": r"(?:\bjd\.local\b|\bjoybuilder\b|\b9Nctl\b)",
        "internal experiment name": r"\br(?:1[0-9]{2}|2[0-9]{2})[a-z]*(?:[-_]|\b)",
        "private key": r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----",
        "access token": r"\b(?:sk-proj-[A-Za-z0-9_-]{30,}|gh[pousr]_[A-Za-z0-9]{30,})\b",
    }
    failures, counts = [], {"python": 0, "json": 0, "shell": 0, "text": 0, "local_links": 0, "internal_imports": 0}
    for name in sorted(set(names) - {""}):
        path = ROOT / name
        if not path.is_file():
            continue
        if path.is_symlink():
            failures.append(f"Unexpected symbolic link: {name}")
            continue
        try:
            content = path.read_text()
        except UnicodeError:
            failures.append(f"Unexpected binary source artifact: {name}")
            continue
        counts["text"] += 1
        for label, pattern in patterns.items():
            if re.search(pattern, content):
                failures.append(f"Check {label}: {name}")
        try:
            if path.suffix == ".py":
                tree = ast.parse(content, filename=name)
                counts["python"] += 1
                if Path(name).parts[0] in {"verl", "camp", "camg"}:
                    for node in ast.walk(tree):
                        if not isinstance(node, ast.ImportFrom) or not node.module:
                            continue
                        if node.level:
                            parent = path.parent
                            for _ in range(node.level - 1):
                                parent = parent.parent
                            target = parent.joinpath(*node.module.split("."))
                        elif node.module.split(".")[0] in {"verl", "camp", "camg"}:
                            target = ROOT.joinpath(*node.module.split("."))
                        else:
                            continue
                        counts["internal_imports"] += 1
                        if not target.is_dir() and not target.with_suffix(".py").is_file():
                            failures.append(f"Missing internal module: {name}:{node.lineno} -> {node.module}")
            elif path.suffix == ".json":
                json.loads(content)
                counts["json"] += 1
            elif path.suffix == ".sh":
                subprocess.run(["bash", "-n", str(path)], check=True, capture_output=True)
                counts["shell"] += 1
        except (SyntaxError, ValueError, subprocess.CalledProcessError) as exc:
            failures.append(f"Invalid source {name}: {exc}")
        if path.suffix == ".md" and (path.parent == ROOT or name.startswith("docs/") or name == "runtimes/autoresearch/README.md"):
            for link in re.findall(r"\]\(([^\s)]+)\)", content):
                if "://" in link or link.startswith(("mailto:", "#")):
                    continue
                target = unquote(link.split("#", 1)[0])
                if not (path.parent / target).exists():
                    failures.append(f"Missing documentation target: {name} -> {target}")
                counts["local_links"] += 1
    result = {"status": "fail" if failures else "pass", "checks": counts, "failures": failures,
              "gpu_executed": False, "environment_services_executed": False}
    print(json.dumps(result, indent=2))
    return bool(failures)


if __name__ == "__main__":
    sys.exit(main())
