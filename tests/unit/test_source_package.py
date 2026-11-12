from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_training_configuration_and_export_modules_are_present():
    for name in (
        "verl/utils/qat/core.py",
        "verl/model_merger/__init__.py", "verl/model_merger/__main__.py",
        "verl/model_merger/base_model_merger.py", "verl/model_merger/fsdp_model_merger.py",
        "verl/model_merger/megatron_model_merger.py", "verl/model_merger/output_validation.py",
    ):
        assert (ROOT / name).is_file(), name


def test_data_and_runtime_assets_are_declared_for_distribution():
    manifest = (ROOT / "MANIFEST.in").read_text()
    assert "recursive-include runtimes" in manifest
    assert any(line.startswith("recursive-include third_party") and "*.sh" in line for line in manifest.splitlines())
    ignore = (ROOT / ".gitignore").read_text().splitlines()
    assert "core.*" not in ignore
    assert "core.[0-9]*" in ignore
