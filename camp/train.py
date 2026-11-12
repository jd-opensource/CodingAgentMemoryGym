"""Launch CAMP reinforcement learning or CAMP-II on-policy distillation."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shlex
from string import Template
import sys
from datetime import datetime, timezone
import uuid


METHOD_NAMES = {"rl": "CAMP reinforcement learning", "opd": "CAMP-II on-policy distillation"}


def arguments(argv=None):
    package = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--method", choices=METHOD_NAMES, required=True)
    parser.add_argument("--student", default=os.environ.get("STUDENT_MODEL"), help="Local student model and tokenizer directory")
    parser.add_argument("--teacher", default=os.environ.get("TEACHER_MODEL"), help="Local frozen teacher model directory; required for OPD")
    parser.add_argument("--routes", type=Path, default=package / "configs/routes.json", help="Environment addresses and task-interface configuration")
    parser.add_argument("--schedule", type=Path, default=package.parent / "camg/data/train_schedule.jsonl", help="Ordered training task references")
    parser.add_argument("--output", type=Path, required=True, help="Directory for checkpoints, trajectories and logs")
    parser.add_argument("--resume", type=Path, help="Explicit training checkpoint to resume")
    parser.add_argument("--print-config", action="store_true", help="Print the resolved command without starting training or writing files")
    parser.add_argument("--check-inputs", action="store_true", help="Validate local inputs without importing the CUDA runtime")
    parser.add_argument("overrides", nargs=argparse.REMAINDER, help="Additional Hydra settings after --")
    args = parser.parse_args(argv)
    if not args.student:
        parser.error("--student or STUDENT_MODEL is required")
    if args.method == "opd" and not args.teacher:
        parser.error("--teacher or TEACHER_MODEL is required for OPD")
    # Diagnostic counters belong to this invocation, not to the checkpoint.
    # Preserve old attempts without replaying their transient failures.
    attempt = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:12]
    args.state_dir = args.output.expanduser().resolve() / "state" / attempt
    return package, args


def validate_schedule(routes: Path, schedule: Path) -> str:
    digest = hashlib.sha256(routes.read_bytes()).hexdigest()
    route_config = json.loads(routes.read_text())
    route_ids = {route["route_id"] for route in route_config["routes"]}
    seen = set()
    count = 0
    with schedule.open() as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                raise ValueError(f"Empty task row at line {line_number}")
            row = json.loads(line)
            if row["route_id"] not in route_ids:
                raise ValueError(f"Unknown environment in task row {line_number}: {row['route_id']}")
            if row["item_id"] in seen:
                raise ValueError(f"Repeated schedule item_id at line {line_number}")
            seen.add(row["item_id"])
            extra = row["extra_info"]
            if extra["schedule_position"] != count:
                raise ValueError(f"Task row {line_number} has an inconsistent schedule_position")
            if extra.get("route_registry_sha256") != digest:
                raise ValueError("The task schedule was prepared for a different environment configuration")
            count += 1
    if not count:
        raise ValueError("The task schedule is empty")
    return digest


def command(package: Path, args) -> list[str]:
    routes = args.routes.expanduser().resolve()
    schedule = args.schedule.expanduser().resolve()
    output = args.output.expanduser().resolve()
    route_digest = validate_schedule(routes, schedule)
    values = {
        "PACKAGE_ROOT": str(package.parent),
        "SCHEDULE": str(schedule),
        "ROUTES": str(routes),
        "ROUTES_SHA256": route_digest,
        "STUDENT": str(Path(args.student).expanduser().resolve()),
        "TEACHER": str(Path(args.teacher).expanduser().resolve()) if args.teacher else "",
        "RUN_NAME": output.name,
        "OUTPUT": str(output),
        "STATE_DIR": str(args.state_dir),
    }
    recipe = package / "configs" / f"{args.method}.txt"
    overrides = [Template(line).substitute(values) for line in recipe.read_text().splitlines() if line.strip() and not line.startswith("#")]
    # Starting a new run never silently reuses an existing checkpoint.
    overrides.append("trainer.resume_mode=resume_path" if args.resume else "trainer.resume_mode=disable")
    if args.resume:
        overrides.append(f"trainer.resume_from_path={args.resume.expanduser().resolve()}")
    extra = args.overrides[1:] if args.overrides[:1] == ["--"] else args.overrides
    managed = {
        "data.train_files", "data.val_files", "data.custom_cls",
        "actor_rollout_ref.model.path", "critic.model.path", "critic.model.tokenizer_path",
        "actor_rollout_ref.rollout.agent", "actor_rollout_ref.agentgym", "data.agentgym",
        "distillation.teacher_models", "trainer.default_local_dir", "trainer.rollout_data_dir",
        "trainer.validation_data_dir", "ray_kwargs", "hydra",
    }
    # Model files, tokenizer/template objects and external model libraries must
    # stay bound to the named model input, rather than bypassing its checks.
    for model in ("actor_rollout_ref.model", "critic.model"):
        managed.update(model + "." + field for field in (
            "path", "local_path", "hf_config_path", "local_hf_config_path",
            "tokenizer_path", "local_tokenizer_path", "lora_adapter_path",
            "hf_config", "tokenizer", "processor", "generation_config",
            "custom_chat_template", "external_lib",
        ))
    for setting in extra:
        key = setting.lstrip("+~").split("=", 1)[0]
        if "=" not in setting or key.startswith("trainer.resume_") or any(
            key == prefix or key.startswith(prefix + ".") or prefix.startswith(key + ".")
            for prefix in managed
        ):
            raise ValueError(f"Setting {key!r} is managed by the launch interface; use its named options instead")
    return [sys.executable, "-X", "faulthandler", "-m", "verl.trainer.main_ppo", *overrides, *extra]


def validate_local_inputs(args) -> None:
    names = ["student"] + (["teacher"] if args.method == "opd" else [])
    for name in names:
        model = Path(getattr(args, name)).expanduser()
        for filename in ("config.json", "tokenizer_config.json"):
            if not (model / filename).is_file():
                raise FileNotFoundError(f"Missing {name} model file: {model / filename}")
        if not any(model.glob("*.safetensors")) and not any(model.glob("pytorch_model*.bin")):
            raise FileNotFoundError(f"No model weights found in {model}")
    if args.resume and not args.resume.expanduser().is_dir():
        raise FileNotFoundError(args.resume)
    output = args.output.expanduser().resolve()
    if not args.resume and output.exists() and any(output.iterdir()):
        raise FileExistsError(f"Output directory is not empty: {output}. Choose a new directory or use --resume.")


def main(argv=None):
    package, args = arguments(argv)
    cmd = command(package, args)
    if args.print_config:
        print(shlex.join(cmd))
        return
    validate_local_inputs(args)
    if args.check_inputs:
        print(f"Local inputs checked for {METHOD_NAMES[args.method]}. Environment services and GPU execution have not been tested.")
        return
    if sys.platform != "linux":
        raise RuntimeError("Training requires Linux and CUDA; --print-config and --check-inputs can run without them")
    output = args.output.expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)
    args.state_dir.mkdir(parents=True, exist_ok=False)
    env = os.environ.copy()
    env["VERL_USE_EXTERNAL_MODULES"] = f"camp.{args.method}"
    env["PYTHONPATH"] = str(package.parent) + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    env["CAMP_STATE_DIR"] = str(args.state_dir)
    env.setdefault("SGLANG_NUMA_BIND_V2", "false")
    env.setdefault("WANDB_MODE", "disabled")
    env.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
    os.execvpe(sys.executable, cmd, env)


if __name__ == "__main__":
    main()
