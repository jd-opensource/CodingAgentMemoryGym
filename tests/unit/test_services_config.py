import json
from pathlib import Path
import subprocess

import pytest

from camg import configure
from camg.serve import PORTS, validate_settings


@pytest.mark.parametrize("name", list(PORTS))
def test_service_configuration_is_loopback_only(name, monkeypatch):
    for prefix in ("GA", "WD"):
        for field in ("URL", "KEY", "MODEL"):
            monkeypatch.setenv(prefix + "_JUDGE_" + field, "unit-test-value")
    validate_settings(name, {"SERVICE_HOST": "127.0.0.1", "SERVICE_PORT": str(PORTS[name])})
    with pytest.raises(ValueError, match="127.0.0.1"):
        validate_settings(name, {"SERVICE_HOST": "0.0.0.0"})
    with pytest.raises(ValueError, match="port"):
        validate_settings(name, {"SERVICE_PORT": "1"})


@pytest.mark.parametrize("name,prefix", [("general", "GA"), ("visual", "WD")])
def test_judge_must_be_supplied_explicitly(name, prefix, monkeypatch):
    monkeypatch.delenv(prefix + "_JUDGE_URL", raising=False)
    with pytest.raises(ValueError, match=prefix + "_JUDGE_URL"):
        validate_settings(name, {})


def test_revision_refuses_uncommitted_new_source(tmp_path, monkeypatch):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "-c", "user.name=Test", "-c", "user.email=test@example.org",
                    "commit", "--allow-empty", "-qm", "Initial"], check=True)
    monkeypatch.setattr(configure, "ROOT", tmp_path)
    assert len(configure.revision()) == 40
    (tmp_path / "new_source.py").write_text("value = 1\n")
    with pytest.raises(ValueError, match="Commit"):
        configure.revision()


def test_environment_settings_bind_real_hashes_and_frozen_limits(tmp_path):
    root = Path(__file__).resolve().parents[2]
    config = json.loads((root / "deployment.example.json").read_text())
    binary = tmp_path / "rg"
    binary.write_bytes(b"fixture only; not executed")
    runtime = tmp_path / "runtime"
    runtime.mkdir()
    for name in ("public_runner.py", "private_runner.py", "artifact-lock.json"):
        (runtime / name).write_text("{}")
    (tmp_path / "autoresearch").mkdir()
    (tmp_path / "autoresearch/train.json").write_text("{}")
    (tmp_path / "autoresearch/grader.json").write_text("{}")
    config.update(data_root=str(tmp_path), state_root=str(tmp_path / "state"), ripgrep_binary=str(binary))
    config["autoresearch"]["runtime_directory"] = str(runtime)
    settings = configure.environment_settings(config, "a" * 40)
    assert set(settings) == {"shop", "coding", "autoresearch", "general", "visual"}
    assert settings["autoresearch"]["OPENMLE_FAST_SHELL_WALL_MS"] == "250000"
    assert settings["autoresearch"]["OPENMLE_FAST_MAX_POLICY_TURNS"] == "200"
    assert settings["shop"]["AGENTMEMORY_PROCEDURAL_GENERATOR_SEED"] == "233"
    assert settings["coding"]["SWESMITH_PROMPT_TURNS"] == "64"
    assert not any("JUDGE_KEY" in key for env in settings.values() for key in env)
