from __future__ import annotations

import json
import re
import secrets
from dataclasses import dataclass
from typing import Any, Mapping

from .profile import SwesmithProfileBinding
from .sandbox import LinuxNamespaceEpisodeSandbox, SwesmithShellExecution
from .workspace import (
    PolicyWorkspaceViolationError,
    SwesmithWorkspace,
    restore_hidden_tests,
    write_runner_guard,
)

class SwesmithGraderError(RuntimeError):
    pass

_GUARD_MARKER_PREFIX = "SWESMITH-RUNNER-GUARD-TAMPERING"

_GUARD_MODULE_TEMPLATE = '''
import json as _json
import os as _os
import tempfile as _tempfile
import unittest as _unittest

import pytest

_MODULE_TOKEN = "__MODULE_TOKEN__"
_MARKER_PREFIX = "__MARKER_PREFIX__"
# The grading sandbox binds the workspace at /testbed and the scrubbed env
# never sets the override, so production always uses the default; the
# override exists only as a test seam for off-sandbox harness runs.
_VERDICT_PATH = _os.environ.get(
    "SWESMITH_GUARD_VERDICT_PATH", "/testbed/__VERDICT_NAME__"
)
_CANARY_TEST_NAME = "__CANARY_NAME__"

def _function_integrity_problem(label, function, qualname_suffix, package_file):
    if type(function).__name__ != "function" or not hasattr(function, "__code__"):
        return "%s is not a plain function: %r" % (label, function)
    filename = _os.path.abspath(str(function.__code__.co_filename))
    package_root = _os.path.abspath(
        _os.path.dirname(_os.path.dirname(package_file))
    ) + _os.sep
    if not filename.startswith(package_root):
        return "%s code lives outside its package: %s" % (label, filename)
    qualname = str(getattr(function, "__qualname__", ""))
    if not qualname.endswith(qualname_suffix):
        return "%s qualname drifted: %r" % (label, qualname)
    return None

def _runner_integrity_problems():
    problems = []
    for label, function, suffix, package_file in (
        ("pytest.Function.runtest", pytest.Function.runtest,
         "Function.runtest", pytest.__file__),
        ("pytest.Function._getobj", pytest.Function._getobj,
         "._getobj", pytest.__file__),
        ("unittest.TestCase.run", _unittest.TestCase.run,
         "TestCase.run", _unittest.__file__),
    ):
        problem = _function_integrity_problem(label, function, suffix, package_file)
        if problem is not None:
            problems.append(problem)
    return problems

_RUNTEST_AT_LOAD = pytest.Function.runtest
_GETOBJ_AT_LOAD = pytest.Function._getobj
_TESTCASE_RUN_AT_LOAD = _unittest.TestCase.run
_LOAD_PROBLEMS = _runner_integrity_problems()
# Early-bound at guard import: rebinding os.write or patching
# builtins.print from policy code cannot mute the marker line.
_os_write = _os.write
_canary_outcomes = {}
_canary_wasxfail = False

def pytest_configure(config):
    directory = _tempfile.mkdtemp(prefix="swesmith-rguard-")
    canary_path = _os.path.join(directory, _CANARY_TEST_NAME + ".py")
    with open(canary_path, "w", encoding="utf-8") as handle:
        handle.write(
            "import pytest\\n"
            "@pytest.mark.xfail(strict=True, "
            "reason='swesmith runner guard canary')\\n"
            "def __CANARY_NAME__():\\n"
            "    assert '__CANARY_A__' == '__CANARY_B__'\\n"
        )
    config.args.append(canary_path)

def pytest_runtest_logreport(report):
    global _canary_wasxfail
    nodeid = str(getattr(report, "nodeid", ""))
    if _CANARY_TEST_NAME in nodeid:
        _canary_outcomes[str(report.when)] = str(
            getattr(report, "outcome", "unknown")
        )
        if getattr(report, "wasxfail", None):
            _canary_wasxfail = True

def pytest_sessionfinish(session, exitstatus):
    problems = []
    for problem in _LOAD_PROBLEMS:
        problems.append("runner_integrity_at_load: " + problem)
    if pytest.Function.runtest is not _RUNTEST_AT_LOAD:
        problems.append("runtest_identity_drift")
    if pytest.Function._getobj is not _GETOBJ_AT_LOAD:
        problems.append("getobj_identity_drift")
    if _unittest.TestCase.run is not _TESTCASE_RUN_AT_LOAD:
        problems.append("testcase_run_identity_drift")
    problems.extend(_runner_integrity_problems())
    call = _canary_outcomes.get("call")
    if call != "skipped" or not _canary_wasxfail:
        # The only honest outcome for the strict-xfail must-fail canary is
        # an xfail, which pytest reports as a skip carrying wasxfail. A
        # plain failure is the strict-XPASS conversion firing (the test
        # "passed" under a vacuous-pass hijack); a pass means the marker
        # machinery was removed; no call at all means the canary never ran
        # or was deleted. Every one of those is tampering.
        problems.append(
            "canary_outcome_anomalous: call=%r wasxfail=%r"
            % (call, _canary_wasxfail)
        )
    verdict = {
        "schema": "swesmith_runner_guard_verdict_v1",
        "token": _MODULE_TOKEN,
        "status": "tampering" if problems else "clean",
        "problems": problems,
        "canary_call_outcome": call,
        "canary_wasxfail": _canary_wasxfail,
        "canary_setup_outcome": _canary_outcomes.get("setup"),
        "canary_teardown_outcome": _canary_outcomes.get("teardown"),
        "exitstatus": int(exitstatus),
    }
    try:
        with open(_VERDICT_PATH, "w", encoding="utf-8") as handle:
            handle.write(_json.dumps(verdict, sort_keys=True))
    except OSError:
        pass
    if problems:
        # Written through the early-bound _os_write on both streams so a
        # builtins.print patch cannot swallow it and padding one stream
        # past its capture limit cannot bury it.
        _message = (
            "%s %s problems=%s\\n"
            % (_MARKER_PREFIX, _MODULE_TOKEN, problems)
        ).encode("utf-8", "replace")
        for _fd in (1, 2):
            try:
                _os_write(_fd, _message)
            except OSError:
                pass
    else:
        # R2-A5: a second clean-attestation channel for the case where the
        # verdict file write itself failed (sandbox resource exhaustion).
        # The ack line on stderr needs no disk, so the grader can accept
        # either channel as proof the guard loaded and attested clean.
        _ack = (
            "%s-ACK %s clean\\n" % (_MARKER_PREFIX, _MODULE_TOKEN)
        ).encode("utf-8", "replace")
        try:
            _os_write(2, _ack)
        except OSError:
            pass
'''

def _generate_runner_guard() -> tuple[str, str, str]:

    module_name = f"swesmith_rguard_{secrets.token_hex(8)}"
    module_token = secrets.token_hex(16)
    canary_name = f"test_rguard_canary_{secrets.token_hex(8)}"
    canary_a = secrets.token_hex(16)
    canary_b = canary_a[:-1] + ("0" if canary_a[-1] != "0" else "1")
    source = (
        _GUARD_MODULE_TEMPLATE.replace("__MODULE_TOKEN__", module_token)
        .replace("__MARKER_PREFIX__", _GUARD_MARKER_PREFIX)
        .replace("__VERDICT_NAME__", f"{module_name}.verdict.json")
        .replace("__CANARY_NAME__", canary_name)
        .replace("__CANARY_A__", canary_a)
        .replace("__CANARY_B__", canary_b)
    )
    return module_name, module_token, source

_PYTEST_RUNNER_RE = re.compile(
    r"(?:\A|&&|\|\||;|\||\n|\r)[ \t]*"
    r"(?:[A-Za-z_][A-Za-z0-9_]*=\S*[ \t]+)*"
    r"pytest(?=[ \t]|\Z)"
    r"|(?:\A|[ \t])python(?:\d(?:\.\d+)*)?[ \t]+-m[ \t]+pytest(?=[ \t]|\Z)"
)

def _command_runs_pytest(full_command: str) -> bool:
    return _PYTEST_RUNNER_RE.search(full_command) is not None

_GUARD_TESTBED_ROOT = "/testbed"

def _guarded_test_command(guard_name: str, full_command: str) -> str:
    if not guard_name or "\x00" in full_command:
        raise SwesmithGraderError("guarded command construction inputs are invalid")

    guard_dir = f"{_GUARD_TESTBED_ROOT}/.{guard_name}.d"
    return (
        "export PYTEST_ADDOPTS=\"-p {name}${{PYTEST_ADDOPTS:+ $PYTEST_ADDOPTS}}\"; "
        "export PYTHONPATH=\"${{PYTHONPATH:+$PYTHONPATH:}}{dir}\"; "
        "export PYTHONNOUSERSITE=1; "
        "{command}"
    ).format(name=guard_name, dir=guard_dir, command=full_command)

def _runner_guard_verdict(
    workspace: SwesmithWorkspace,
    guard_name: str,
    module_token: str,
    full_run: TestRunEvidence | None,
    gold: Mapping[str, Any],
) -> dict[str, Any] | None:

    if full_run is None:
        return None
    verdict: Any = None
    try:
        verdict = json.loads(
            (workspace.policy_root / f"{guard_name}.verdict.json").read_text(
                encoding="utf-8"
            )
        )
    except (OSError, ValueError):
        verdict = None
    problems: list[str] = []
    if isinstance(verdict, Mapping) and verdict.get("token") == module_token:
        status = verdict.get("status")
        if status == "tampering":
            reported = verdict.get("problems")
            if isinstance(reported, list) and reported:
                problems.extend(str(problem) for problem in reported)
            else:
                problems.append("guard_reported_tampering")
        elif status != "clean":
            problems.append(f"unexpected_verdict_status: {status!r}")
        elif (
            not full_run.timed_out
            and full_run.exit_code == 0
            and type(verdict.get("exitstatus")) is int
            and verdict["exitstatus"] != full_run.exit_code
        ):

            problems.append(
                "verdict_exitstatus_mismatch: "
                f"verdict={verdict['exitstatus']} process={full_run.exit_code}"
            )
    elif isinstance(verdict, Mapping):
        problems.append("verdict_token_mismatch")
    elif (
        not full_run.timed_out
        and full_run.exit_code == 0
    ):

        combined_output = full_run.stdout + "\n" + full_run.stderr
        if f"{_GUARD_MARKER_PREFIX}-ACK {module_token} clean" not in combined_output:
            declared = set(gold.get("FAIL_TO_PASS", [])) | set(
                gold.get("PASS_TO_PASS", [])
            )
            if any(
                full_run.status_map.get(str(key)) == "PASSED" for key in declared
            ):
                problems.append("verdict_missing_while_tests_passed")

    if f"{_GUARD_MARKER_PREFIX} " in (full_run.stdout + "\n" + full_run.stderr):
        problems.append("guard_marker_line_in_output")
    if not problems:
        return None
    return {
        "schema": "swesmith_runner_tampering_v1",
        "problems": problems,
        "verdict": verdict if isinstance(verdict, Mapping) else None,
        "exit_code": full_run.exit_code,
        "timed_out": full_run.timed_out,
    }

@dataclass(frozen=True)
class TestRunEvidence:
    role: str
    command: str
    exit_code: int
    timed_out: bool
    output_truncated: bool
    elapsed_ms: int
    stdout: str
    stderr: str
    status_map: Mapping[str, str]
    status_source: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "role": self.role,
            "command": self.command,
            "exit_code": self.exit_code,
            "timed_out": self.timed_out,
            "output_truncated": self.output_truncated,
            "elapsed_ms": self.elapsed_ms,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "status_map": dict(self.status_map),
            "status_source": self.status_source,
        }

@dataclass(frozen=True)
class SwesmithGradeResult:
    reward: float
    resolution_status: str | None
    report: Mapping[str, Any]
    restored_test_paths: tuple[str, ...]
    f2p_run: TestRunEvidence | None
    full_run: TestRunEvidence | None
    error: str | None = None

    policy_caused: bool = False

    runner_tampering: Mapping[str, Any] | None = None

    @property
    def resolved(self) -> bool:
        return self.reward == 1.0

    def as_private_dict(self) -> dict[str, Any]:
        return {
            "schema": "swesmith_grade_evidence_v1",
            "reward": self.reward,
            "resolution_status": self.resolution_status,
            "report": _jsonable(self.report),
            "restored_test_paths": list(self.restored_test_paths),
            "f2p_run": None if self.f2p_run is None else self.f2p_run.as_dict(),
            "full_run": None if self.full_run is None else self.full_run.as_dict(),
            "error": self.error,
            "runner_tampering": (
                None if self.runner_tampering is None
                else _jsonable(self.runner_tampering)
            ),
        }

class SwesmithHiddenGrader:

    def __init__(
        self,
        *,
        timeout_ms: int,
        output_joiner: str = "\n",
        private_output_bytes: int = 4 * 1024 * 1024,
    ) -> None:
        if type(timeout_ms) is not int or timeout_ms <= 0:
            raise ValueError("grader timeout_ms must be a positive integer")
        if type(private_output_bytes) is not int or private_output_bytes <= 0:
            raise ValueError("private_output_bytes must be a positive integer")
        self.timeout_ms = timeout_ms
        self.output_joiner = output_joiner
        self.private_output_bytes = private_output_bytes

    def grade(
        self,
        *,
        instance: Mapping[str, Any],
        profile: SwesmithProfileBinding,
        workspace: SwesmithWorkspace,
        sandbox: LinuxNamespaceEpisodeSandbox,
    ) -> SwesmithGradeResult:

        restored: list[str] = []
        full_run: TestRunEvidence | None = None
        guard_name = ""
        module_token = ""
        try:
            restored.extend(restore_hidden_tests(workspace))

            sandbox.refresh_after_host_mutation()

            if _command_runs_pytest(profile.full_command):

                guard_name, module_token, guard_source = _generate_runner_guard()
                write_runner_guard(workspace, guard_name, guard_source)
                sandbox.refresh_after_host_mutation()
                command = _guarded_test_command(guard_name, profile.full_command)
            else:
                command = profile.full_command
            full_run = self._run_tests(
                role="P2P/full",
                command=command,
                profile=profile,
                instance=instance,
                sandbox=sandbox,
            )
            gold = _gold_results(instance)
            tampering = (
                _runner_guard_verdict(
                    workspace, guard_name, module_token, full_run, gold
                )
                if guard_name
                else None
            )
            if tampering is not None:

                return SwesmithGradeResult(
                    reward=0.0,
                    resolution_status=None,
                    report={"runner_tampering": tampering},
                    restored_test_paths=tuple(restored),
                    f2p_run=None,
                    full_run=full_run,
                    error=None,
                    runner_tampering=tampering,
                )
            report = _eval_report(profile, full_run.status_map, gold)
            status = _resolution(profile, report)
            reward = (
                1.0
                if _healthy(full_run) and status == profile.full_resolution_status
                else 0.0
            )
            return SwesmithGradeResult(
                reward=reward,
                resolution_status=status,
                report=report,
                restored_test_paths=tuple(restored),
                f2p_run=None,
                full_run=full_run,
            )
        except Exception as exc:
            return SwesmithGradeResult(
                reward=0.0,
                resolution_status=None,
                report={},
                restored_test_paths=tuple(restored),
                f2p_run=None,
                full_run=full_run,
                error=f"{type(exc).__name__}: {exc}",
                policy_caused=isinstance(exc, PolicyWorkspaceViolationError),
            )

    def _run_tests(
        self,
        *,
        role: str,
        command: str,
        profile: SwesmithProfileBinding,
        instance: Mapping[str, Any],
        sandbox: LinuxNamespaceEpisodeSandbox,
    ) -> TestRunEvidence:
        execution: SwesmithShellExecution = sandbox.run_trusted(
            command=command,
            workdir=".",
            timeout_ms=self.timeout_ms,
            stdout_limit_bytes=self.private_output_bytes,
            stderr_limit_bytes=self.private_output_bytes,
        )
        stdout = execution.result.stdout.decode("utf-8", errors="replace")
        stderr = execution.result.stderr.decode("utf-8", errors="replace")
        combined = stdout + self.output_joiner + stderr
        output_truncated = (
            execution.result.stdout_truncated or execution.result.stderr_truncated
        )
        if (
            output_truncated
            and execution.result.exit_code == 0
            and not execution.result.timed_out
        ):

            status_map = _declared_pass_status(role, instance)
            status_source = "exit_zero_declared_tests"
        elif output_truncated:
            status_map = {}
            status_source = "unavailable_truncated_output"
        else:
            status_map = dict(profile.log_parser(combined))
            status_source = "profile_log_parser"
        return TestRunEvidence(
            role=role,
            command=command,
            exit_code=execution.result.exit_code,
            timed_out=execution.result.timed_out,
            output_truncated=output_truncated,
            elapsed_ms=execution.result.elapsed_ms,
            stdout=stdout,
            stderr=stderr,
            status_map=status_map,
            status_source=status_source,
        )

def _gold_results(instance: Mapping[str, Any]) -> dict[str, list[str]]:
    f2p = instance.get("FAIL_TO_PASS")
    p2p = instance.get("PASS_TO_PASS")
    if not isinstance(f2p, list) or not isinstance(p2p, list):
        raise SwesmithGraderError("instance lacks declared FAIL_TO_PASS/PASS_TO_PASS lists")
    return {
        "FAIL_TO_PASS": [str(value) for value in f2p],
        "PASS_TO_PASS": [str(value) for value in p2p],
    }

def _declared_f2p_passed(
    status_map: Mapping[str, str],
    gold: Mapping[str, Any],
    profile: SwesmithProfileBinding,
) -> bool:
    report = _eval_report(profile, status_map, gold)
    failures = report.get("FAIL_TO_PASS", {})
    return isinstance(failures, Mapping) and not failures.get("failure", [])

def _declared_pass_status(
    role: str, instance: Mapping[str, Any]
) -> dict[str, str]:
    gold = _gold_results(instance)
    if role == "F2P":
        paths = gold["FAIL_TO_PASS"]
    elif role == "P2P/full":
        paths = [*gold["FAIL_TO_PASS"], *gold["PASS_TO_PASS"]]
    else:
        raise SwesmithGraderError(f"unknown test phase: {role!r}")
    return {path: "PASSED" for path in paths}

def _eval_report(
    profile: SwesmithProfileBinding,
    status_map: Mapping[str, str],
    gold: Mapping[str, Any],
) -> Mapping[str, Any]:
    return profile.get_eval_tests_report(dict(status_map), dict(gold))

def _resolution(profile: SwesmithProfileBinding, report: Mapping[str, Any]) -> str | None:
    try:
        return str(profile.get_resolution_status(report))
    except Exception:
        return None

def _healthy(run: TestRunEvidence | None) -> bool:

    return bool(
        run is not None
        and not run.timed_out
        and run.status_source in {"profile_log_parser", "exit_zero_declared_tests"}
    )

def _jsonable(value: Any) -> Any:
    try:
        json.dumps(value)
        return value
    except (TypeError, ValueError):
        if isinstance(value, Mapping):
            return {str(key): _jsonable(item) for key, item in value.items()}
        if isinstance(value, (list, tuple)):
            return [_jsonable(item) for item in value]
        return repr(value)
