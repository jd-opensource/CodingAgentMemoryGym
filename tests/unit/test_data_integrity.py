from collections import Counter
import hashlib
import json
from pathlib import Path

from camg.configure import bind_schedule
from camg.prepare import DATA, sha256
from camp.train import validate_schedule

ROOT = Path(__file__).resolve().parents[2]


def load(name):
    return json.loads((DATA / name).read_text())


def test_schedule_preserves_five_domain_budget():
    rows = [json.loads(line) for line in (DATA / "train_schedule.jsonl").read_text().splitlines()]
    assert len(rows) == 12800
    assert Counter(row["route_id"] for row in rows) == dict.fromkeys(
        ["webshop", "swesmith", "openmle_fast", "agentgeneral", "webdev"], 2560)
    assert len({row["item_id"] for row in rows}) == 12800
    assert [row["extra_info"]["schedule_position"] for row in rows] == list(range(12800))
    coding = load("coding/index.json")
    for row in rows:
        if row["route_id"] == "swesmith":
            identity = coding[row["data_idx"]]["instance_id"]
            assert hashlib.sha256(identity.encode()).hexdigest() == row["extra_info"]["instance_id_sha256"]
        if row["route_id"] == "openmle_fast":
            assert 0 <= row["data_idx"] < 762
        if row["route_id"] == "agentgeneral":
            assert 0 <= row["data_idx"] < 925
        if row["route_id"] == "webdev":
            assert 0 <= row["data_idx"] < 500
    assert len({row["data_idx"] for row in rows if row["route_id"] == "agentgeneral"}) == 797


def test_autoresearch_splits_and_task_files():
    train, heldout = load("autoresearch/train.json"), load("autoresearch/heldout.json")
    assert len(train["records"]) == 762 and len(heldout["records"]) == 169
    assert not {r["task_id"] for r in train["records"]} & {r["task_id"] for r in heldout["records"]}
    for manifest in (train, heldout):
        for row in manifest["records"]:
            instructions = next(f for f in row["public_files"] if f["path"] == "TASK.md")
            assert sha256(DATA / "autoresearch/instructions" / (row["task_id"] + ".md")) == instructions["sha256"]
    grader = load("autoresearch/grader.json")
    assert len(grader["records"]) == 931
    bindings = grader["public_manifest_sha256"]
    assert isinstance(bindings, dict)
    assert bindings["train"] == sha256(DATA / "autoresearch/train.json")
    assert bindings["heldout"] == sha256(DATA / "autoresearch/heldout.json")
    acquisition = load("autoresearch/acquisition.json")
    assert len(acquisition) == 931
    assert sum(bool(r["package"]) for r in acquisition) == 651


def test_mimo_tables_are_selected_and_content_bound():
    for name, count in (("general", 925), ("visual", 500)):
        source = load(f"{name}/source.json")
        assert source["sha256"] == sha256(DATA / name / "tasks.jsonl")
        rows = [json.loads(line) for line in (DATA / name / "tasks.jsonl").read_text().splitlines()]
        assert len(rows) == count
        if name == "general":
            for row in rows:
                instance = json.loads(row["extra_info"]["instance_json"])
                assert instance["env_task_dir"] == "${GENERAL_ASSETS}/" + instance["instance_id"]


def test_binding_changes_only_configuration_digests(tmp_path):
    routes = json.loads((ROOT / "camp/configs/routes.json").read_text())
    for row in routes["routes"]:
        row["route_attestation_sha256"] = "a" * 64
    bind_schedule(routes, tmp_path)
    validate_schedule(tmp_path / "routes.json", tmp_path / "train_schedule.jsonl")
    with (DATA / "train_schedule.jsonl").open() as original, (tmp_path / "train_schedule.jsonl").open() as bound:
        for first, second in zip(original, bound, strict=True):
            first, second = json.loads(first), json.loads(second)
            for key in ("route_registry_sha256", "route_attestation_sha256"):
                first["extra_info"].pop(key)
                second["extra_info"].pop(key)
            assert first == second
