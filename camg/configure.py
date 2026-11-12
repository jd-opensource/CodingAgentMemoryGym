"""Bind local assets and service addresses to a CAMG-II training schedule."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from .prepare import DATA, OPENMLE_REVISION, sha256, write_json

ROOT = Path(__file__).resolve().parents[1]
ENVIRONMENTS = {"shop": "webshop", "coding": "swesmith", "autoresearch": "openmle_fast", "general": "agentgeneral", "visual": "webdev"}
PORTS = {"shop": 65131, "coding": 65134, "autoresearch": 65133, "general": 65139, "visual": 65140}


def revision() -> str:
    dirty = subprocess.check_output(
        ["git", "-C", str(ROOT), "status", "--porcelain", "--untracked-files=all"], text=True)
    if dirty.strip():
        raise ValueError("Commit local source changes before binding a deployment to its source revision")
    return subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()


def environment_settings(config: dict, commit: str) -> dict[str, dict[str, str]]:
    data = Path(config["data_root"]).expanduser().resolve()
    state = Path(config["state_root"]).expanduser().resolve()
    rg = Path(config["ripgrep_binary"]).expanduser().resolve()
    rg_hash = sha256(rg)
    shop = config["shop"]
    common = {"PYTHONDONTWRITEBYTECODE": "1", "PYTHONUNBUFFERED": "1"}
    settings = {name: dict(common) for name in ENVIRONMENTS}
    settings["shop"].update({
        "AGENTMEMORY_SURFACE": "agentmemory_webshop_procedural_natural_chain_filesystem_v2",
        "MEMORYARENA_ROOT": shop["source_root"], "MEMORYARENA_BASE_COMMIT": "6cd9de14b71915e39ac742a20dc33785e14b6aab",
        "MEMORYARENA_WEBSHOP_ITEMS_FILE": shop["items_file"], "MEMORYARENA_WEBSHOP_ATTR_FILE": shop["attributes_file"],
        "MEMORYARENA_WEBSHOP_SEARCH_ROOT": shop["search_root"], "MEMORYARENA_WEBSHOP_JAVA_HOME": shop["java_home"],
        "MEMORYARENA_LUCENE_INDEX_MANIFEST": str(DATA / "shop/lucene.sha256"),
        "AGENTMEMORY_PROCEDURAL_PRODUCT_POOL": shop["product_pool"],
        "AGENTMEMORY_PROCEDURAL_PRODUCT_POOL_SHA256": "7ca77d3f9f2a0007eed54a17aa6f8d275ce8ec200ae47daeca3b70cafdd506c6",
        "AGENTMEMORY_PROCEDURAL_TASK_COUNT": "6400", "AGENTMEMORY_PROCEDURAL_GENERATOR_SEED": "233",
        "AGENTMEMORY_PROCEDURAL_PROVIDER_MODE": "reseeded_stream", "AGENTMEMORY_PROCEDURAL_START_ORBIT": "0",
        "AGENTMEMORY_SPLIT": "train", "AGENTMEMORY_WEBSHOP_PRICE_SEED": "233",
        "AGENTMEMORY_FIRST_VALID_ADD_REWARD": "0", "AGENTMEMORY_FIRST_VALID_LATER_SESSION_RETRIEVE_REWARD": "0",
        "AGENTMEMORY_LTM_INVENTORY_MODE": "hidden", "AGENTMEMORY_LTM_TRANSITION_NOTICE_MODE": "none",
        "AGENTMEMORY_MEMORY_PROMPT_MODE": "natural_filesystem", "AGENTMEMORY_ACTION_LISTING_MODE": "separate",
        "AGENTMEMORY_WORKSPACE_RG_BINARY": str(rg), "AGENTMEMORY_WORKSPACE_RG_SHA256": rg_hash,
        "AGENTMEMORY_RUN_ID": state.name, "AGENTMEMORY_SERVICE_ROLE": "formal", "AGENTMEMORY_RUNTIME_SOURCE_ID": commit,
    })
    settings["coding"].update({
        "SWESMITH_DATASET_MANIFEST": str(data / "coding/manifest.json"), "SWESMITH_IMAGE_MANIFEST": str(data / "coding/images.json"),
        "SWESMITH_SOURCE_ROOT": config["coding"]["source_root"], "SWESMITH_SOURCE_REVISION": "9b74ac08118a85c39c356802f7961893af73e07f",
        "SWESMITH_MIRRORS_ROOT": config["coding"]["mirrors_root"], "SWESMITH_EPISODES_ROOT": str(state / "coding/episodes"),
        "SWESMITH_OCI_CACHE_ROOT": config["oci_rootfs_cache"], "SWESMITH_RG_BINARY": str(rg), "SWESMITH_RG_SHA256": rg_hash,
        "SWESMITH_UID_LEASE_ROOT": str(state / "coding/uid-leases"), "SWESMITH_AUDIT_ROOT": str(state / "coding/audits"),
        "SWESMITH_MAX_STEPS": "200", "SWESMITH_PROMPT_TURNS": "64", "SWESMITH_MAX_OBSERVATION_TOKENS": "8192",
        "SWESMITH_MAX_OBSERVATION_BYTES": "8191", "SWESMITH_RUNTIME_OUTER_COMMIT": commit, "SWESMITH_RUNTIME_INNER_COMMIT": commit,
        "SWESMITH_HOST": "127.0.0.1", "SWESMITH_PORT": str(PORTS["coding"]),
    })
    runtime = Path(config["autoresearch"]["runtime_directory"]).expanduser().resolve()
    om_state = state / "autoresearch"
    env = settings["autoresearch"]
    limits = json.loads((ROOT / "camp/configs/environments/autoresearch-limits.json").read_text())
    from .services.autoresearch.launch import _LIMIT_ENVIRONMENT
    env.update({key: str(limits[field]) for field, key in _LIMIT_ENVIRONMENT.items()})
    digest = "sha256:ada19e0d27dadb991c5b6112e00f116b26359067d5298650eb2eeff7d8385af2"
    env.update({
        "OPENMLE_FAST_TASK_MANIFEST": str(data / "autoresearch/train.json"),
        "OPENMLE_FAST_TASK_MANIFEST_SHA256": sha256(data / "autoresearch/train.json"),
        "OPENMLE_FAST_PACKAGE_ROOT": str(data / "autoresearch"), "OPENMLE_FAST_ARCHIVE_ROOT": str(data / "autoresearch"),
        "OPENMLE_FAST_EPISODES_ROOT": "/tmp/camg-autoresearch/public-workspaces/episodes", "OPENMLE_FAST_RELEASE_REVISION": OPENMLE_REVISION,
        "OPENMLE_FAST_MANIFEST_ROLE": "train_pool", "OPENMLE_FAST_MATERIALIZER_SHA256": sha256(ROOT / "camg/services/autoresearch/materializer.py"),
        "OPENMLE_FAST_ACTIONS_SHA256": sha256(ROOT / "camg/services/autoresearch/actions.py"),
        "OPENMLE_FAST_EXECUTOR_RUNNER": str(runtime / "public_runner.py"), "OPENMLE_FAST_EXECUTOR_RUNNER_SHA256": sha256(runtime / "public_runner.py"),
        "OPENMLE_FAST_EXECUTOR_RUNTIME_DIGEST": digest, "OPENMLE_FAST_RUNTIME_ARTIFACT_LOCK_SHA256": sha256(runtime / "artifact-lock.json"),
        "OPENMLE_FAST_GRADER_CLIENT_TIMEOUT_SECONDS": "8.5", "OPENMLE_FAST_GRADER_TIMEOUT_MARGIN_SECONDS": "1",
        "OPENMLE_FAST_CLIENT_TIMEOUT_SECONDS": "3660", "OPENMLE_FAST_CLIENT_TIMEOUT_MARGIN_SECONDS": "60",
        "OPENMLE_FAST_GRADER_ENDPOINT": str(om_state / "grader.sock"), "OPENMLE_FAST_GRADER_CREDENTIAL": str(om_state / "grader.key"),
        "OPENMLE_FAST_AUDIT_ROOT": str(om_state / "public-audits"), "OPENMLE_FAST_RUNTIME_OUTER_COMMIT": commit,
        "OPENMLE_FAST_RUNTIME_INNER_COMMIT": commit, "OPENMLE_FAST_MAX_OBSERVATION_TOKENS": "8192",
        "OPENMLE_FAST_PRIVATE_RUNTIME_DIGEST": digest, "OPENMLE_FAST_PRIVATE_RUNNER": str(runtime / "private_runner.py"),
        "OPENMLE_FAST_PRIVATE_RUNNER_SHA256": sha256(runtime / "private_runner.py"),
        "OPENMLE_FAST_PRIVATE_TASK_MANIFEST": str(data / "autoresearch/grader.json"),
        "OPENMLE_FAST_PRIVATE_TASK_MANIFEST_SHA256": sha256(data / "autoresearch/grader.json"),
        "OPENMLE_FAST_PRIVATE_PACKAGE_ROOT": str(data / "autoresearch/private-grader"),
        "OPENMLE_FAST_PRIVATE_ARCHIVE_ROOT": str(data / "autoresearch"), "OPENMLE_FAST_PRIVATE_AUDIT_ROOT": str(om_state / "private-audits"),
        "OPENMLE_FAST_HOST": "127.0.0.1", "OPENMLE_FAST_PORT": str(PORTS["autoresearch"]),
    })
    for suffix, field in {"CPU_VCPUS": "grader_cpu_vcpus", "MEMORY_BYTES": "grader_memory_bytes", "MAX_PROCESSES": "grader_max_processes", "WORKER_WALL_MS": "grader_worker_wall_ms", "TOTAL_WALL_MS": "grader_total_wall_ms", "MAX_CONCURRENT_REQUESTS": "grader_max_concurrent_requests"}.items():
        env["OPENMLE_FAST_PRIVATE_" + suffix] = str(limits[field])
    for name, prefix in (("general", "AGENTGENERAL"), ("visual", "WEBDEV")):
        settings[name].update({
            prefix + "_PARQUET": str(data / name / "tasks.parquet"), prefix + "_MIMOAGENT_CONFIG": str(ROOT / f"camp/configs/environments/{name}.yaml"),
            prefix + "_PORT": str(PORTS[name]), prefix + "_MAX_STEPS": "200", prefix + "_PROMPT_TURNS": "64",
            "MIMOAGENT_DOCKER_VOL_ROOT": str(state / name / "containers"), "AG_EP_CLAIM_FILE": str(state / name / "episode-claims.jsonl"),
            "WEBDEV_DIMS_DIR": str(state / name / "judge-results"), "WEBDEV_TASK_DIR_ROOT": str(state / name / "tasks"),
            "MIMOAGENT_AGENT_VENV_HOST_DIR": config["mimo"]["agent_environment"],
        })
    return {name: {key: str(value) for key, value in env.items()} for name, env in settings.items()}


def bind_schedule(routes: dict, destination: Path) -> None:
    write_json(destination / "routes.json", routes)
    digest = sha256(destination / "routes.json")
    by_route = {r["route_id"]: r for r in routes["routes"]}
    target = destination / "train_schedule.jsonl"
    with target.open("w") as out, (DATA / "train_schedule.jsonl").open() as source:
        for line in source:
            row = json.loads(line)
            extra = row["extra_info"]
            extra["route_registry_sha256"] = digest
            extra["route_attestation_sha256"] = by_route[row["route_id"]]["route_attestation_sha256"]
            out.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deployment", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    config = json.loads(args.deployment.read_text())
    commit = revision()
    settings = environment_settings(config, commit)
    routes = json.loads((ROOT / "camp/configs/routes.json").read_text())
    for route in routes["routes"]:
        client = route["client"]
        name = next(k for k, v in ENVIRONMENTS.items() if v == route["route_id"])
        client["env_addr"] = f"http://127.0.0.1:{PORTS[name]}"
        for field in ("expected_inner_commit", "expected_outer_commit"):
            if field in client:
                client[field] = commit
        if name == "autoresearch":
            for target, source in {"expected_manifest_sha256": "OPENMLE_FAST_TASK_MANIFEST_SHA256", "expected_actions_sha256": "OPENMLE_FAST_ACTIONS_SHA256", "expected_materializer_sha256": "OPENMLE_FAST_MATERIALIZER_SHA256"}.items():
                client[target] = settings[name][source]
        # This binds configuration content; it is NOT a claim of runtime success.
        route["route_attestation_sha256"] = hashlib.sha256(json.dumps({"client": client, "settings": settings[name]}, sort_keys=True).encode()).hexdigest()
        write_json(args.output / f"{name}.json", {"environment": name, "source_revision": commit, "settings": settings[name]})
    bind_schedule(routes, args.output)
    write_json(args.output / "configuration.json", {"source_revision": commit, "runtime_verified": False,
        "routes_sha256": sha256(args.output / "routes.json"), "schedule_sha256": sha256(args.output / "train_schedule.jsonl")})
    print("Prepared local configuration. Service startup and GPU execution have not been tested.")


if __name__ == "__main__":
    main()
