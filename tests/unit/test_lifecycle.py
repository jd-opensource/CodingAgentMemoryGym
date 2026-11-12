import pytest

from camg.services.lifecycle import close_all
from camg import serve


def test_cleanup_visits_every_episode_even_after_failure():
    visited = []
    def close(identifier):
        visited.append(identifier)
        if identifier == 1:
            raise KeyError(identifier)  # Already closed by an idle reaper.
        if identifier == 2:
            raise RuntimeError("simulated cleanup failure")
    with pytest.raises(RuntimeError, match="1 owned episodes"):
        close_all([1, 2, 3], close, lambda identifier: identifier != 1)
    assert visited == [1, 2, 3]


def test_unknown_key_error_is_not_silently_accepted():
    def close(_identifier):
        raise KeyError("internal failure")
    with pytest.raises(RuntimeError):
        close_all([1], close, lambda _identifier: True)


def test_failed_grader_spawn_removes_its_credential(tmp_path, monkeypatch):
    credential = tmp_path / "service" / "grader.key"
    monkeypatch.setenv("OPENMLE_FAST_GRADER_CREDENTIAL", str(credential))
    monkeypatch.setenv("OPENMLE_FAST_GRADER_ENDPOINT", str(credential.with_suffix(".sock")))
    def fail_spawn(*_args, **_kwargs):
        raise OSError("simulated spawn failure")
    monkeypatch.setattr(serve.subprocess, "Popen", fail_spawn)
    with pytest.raises(OSError):
        serve.run_autoresearch()
    assert not credential.exists()


def test_service_does_not_reuse_existing_credential(tmp_path, monkeypatch):
    credential = tmp_path / "grader.key"
    credential.write_bytes(b"existing-test-credential")
    monkeypatch.setenv("OPENMLE_FAST_GRADER_CREDENTIAL", str(credential))
    monkeypatch.setenv("OPENMLE_FAST_GRADER_ENDPOINT", str(tmp_path / "grader.sock"))
    with pytest.raises(FileExistsError):
        serve.run_autoresearch()
    assert credential.read_bytes() == b"existing-test-credential"
