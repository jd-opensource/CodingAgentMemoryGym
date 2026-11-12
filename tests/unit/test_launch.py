import json
from pathlib import Path

import pytest

from camp.train import arguments, command, main, validate_local_inputs, validate_schedule

ROOT = Path(__file__).resolve().parents[2]


def parse(tmp_path, method="rl", *extra):
    return arguments(["--method", method, "--student", str(tmp_path / "student"),
                      "--teacher", str(tmp_path / "teacher"), "--output", str(tmp_path / "run"), *extra])


def test_bundled_schedule_validates():
    digest = validate_schedule(ROOT / "camp/configs/routes.json", ROOT / "camg/data/train_schedule.jsonl")
    assert len(digest) == 64


@pytest.mark.parametrize("method,learner,rollout,teacher,critic,batch", [
    ("rl", 6, 2, 0, True, 510), ("opd", 4, 2, 2, False, 512),
])
def test_recipe_layout(tmp_path, method, learner, rollout, teacher, critic, batch):
    package, args = parse(tmp_path, method)
    cmd = command(package, args)
    cfg = dict(item.lstrip("+").split("=", 1) for item in cmd[5:])
    assert cfg["trainer.n_gpus_per_node"] == str(learner)
    assert cfg["actor_rollout_ref.rollout.n_gpus_per_node"] == str(rollout)
    assert cfg["critic.enable"].lower() == str(critic).lower()
    assert cfg["actor_rollout_ref.actor.ppo_mini_batch_size"] == str(batch)
    assert cfg["trainer.resume_mode"] == "disable"
    assert cfg["trainer.total_training_steps"] == "100"
    assert cfg["data.train_batch_size"] == "64"
    assert cfg["distillation.enabled"].lower() == str(bool(teacher)).lower()
    if teacher:
        assert cfg["distillation.n_gpus_per_node"] == str(teacher)
        assert cfg["distillation.distillation_loss.use_task_rewards"].lower() == "false"


@pytest.mark.parametrize("setting", [
    "data={}", "+data.train_files=/tmp/other", "~data.train_files", "data.custom_cls.name=Other",
    "actor_rollout_ref.model.path=/tmp/other", "actor_rollout_ref={}",
    "trainer.resume_mode=auto", "trainer.resume_from_path=/tmp/other", "trainer={}",
    "distillation.teacher_models={}", "critic.model.tokenizer_path=/tmp/other",
    "hydra.run.dir=/tmp/other", "ray_kwargs={}", "actor_rollout_ref.agentgym.state_dir=/tmp/other",
    "actor_rollout_ref.model.tokenizer_path=/tmp/other", "actor_rollout_ref.model.hf_config_path=/tmp/other",
    "critic.model.hf_config_path=/tmp/other", "actor_rollout_ref.model.local_path=/tmp/other",
    "actor_rollout_ref.model.lora_adapter_path=/tmp/other", "critic.model.local_tokenizer_path=/tmp/other",
    "actor_rollout_ref.model.custom_chat_template=unvalidated", "actor_rollout_ref.model.external_lib=custom",
])
def test_managed_paths_cannot_be_overridden(tmp_path, setting):
    package, args = parse(tmp_path, "rl", "--", setting)
    with pytest.raises(ValueError, match="managed"):
        command(package, args)


def test_ordinary_hyperparameter_override(tmp_path):
    package, args = parse(tmp_path, "rl", "--", "trainer.total_training_steps=1")
    assert command(package, args)[-1] == "trainer.total_training_steps=1"


def test_resume_and_attempt_counters_are_separate(tmp_path):
    package, first = parse(tmp_path)
    _, second = parse(tmp_path, "rl", "--resume", str(tmp_path / "checkpoint"))
    assert first.state_dir != second.state_dir
    assert first.state_dir.parent == second.state_dir.parent
    assert "trainer.resume_mode=resume_path" in command(package, second)
    assert not first.state_dir.exists() and not second.state_dir.exists()


def test_check_inputs_and_fresh_output_guard(tmp_path):
    _, args = parse(tmp_path)
    with pytest.raises(FileNotFoundError):
        validate_local_inputs(args)
    model = tmp_path / "student"
    model.mkdir()
    for name in ("config.json", "tokenizer_config.json", "model.safetensors"):
        (model / name).write_text("{}")
    validate_local_inputs(args)
    args.output.mkdir()
    (args.output / "old.log").write_text("old attempt")
    with pytest.raises(FileExistsError, match="not empty"):
        validate_local_inputs(args)


def test_print_does_not_create_output_or_import_training(tmp_path, capsys):
    main(["--method", "rl", "--student", "/models/example", "--output", str(tmp_path / "new"), "--print-config"])
    assert "verl.trainer.main_ppo" in capsys.readouterr().out
    assert not (tmp_path / "new").exists()


@pytest.mark.parametrize("change", ["position", "digest", "route", "duplicate"])
def test_rejects_inconsistent_schedule(tmp_path, change):
    source = ROOT / "camg/data/train_schedule.jsonl"
    with source.open() as stream:
        rows = [json.loads(next(stream)) for _ in range(2)]
    if change == "position": rows[0]["extra_info"]["schedule_position"] = 1
    if change == "digest": rows[0]["extra_info"]["route_registry_sha256"] = "0" * 64
    if change == "route": rows[0]["route_id"] = "unknown"
    if change == "duplicate": rows[1]["item_id"] = rows[0]["item_id"]
    schedule = tmp_path / "schedule.jsonl"
    schedule.write_text("".join(json.dumps(row) + "\n" for row in rows))
    with pytest.raises(ValueError):
        validate_schedule(ROOT / "camp/configs/routes.json", schedule)
