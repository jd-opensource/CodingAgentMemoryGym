from __future__ import annotations

import os
import sys

def ensure_import_paths() -> None:

    staging = os.environ.get("MIMO_STAGING_ROOT", "")
    if not staging:
        return
    repo = os.path.join(staging, "repo", "verl-mimo-oss")
    mimoagent_src = os.path.join(
        repo, "third_party", "mimoagent-osr", "src"
    )
    for path in (repo, mimoagent_src):
        if os.path.isdir(path) and path not in sys.path:
            sys.path.insert(0, path)

ensure_import_paths()

def main() -> None:
    import uvicorn

    ensure_import_paths()
    port = int(os.environ.get("WEBDEV_PORT", "65126"))
    uvicorn.run(
        "camg.services.visual.server:app",
        host="127.0.0.1",
        port=port,
        log_level=os.environ.get("WEBDEV_UVICORN_LOG_LEVEL", "info"),
    )

if __name__ == "__main__":
    main()
