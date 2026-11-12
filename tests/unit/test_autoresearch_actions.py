"""Regression checks for AutoResearch's released shell and submit protocol."""
import pytest
from camg.services.autoresearch.actions import parse_policy_action, MAX_SHELL_TIMEOUT_MS


def envelope(command):
    return f'<tool_call>\n<function=bash>\n<parameter=command>\n{command}\n</parameter>\n</function>\n</tool_call>'


def test_shell_timeout_is_preserved():
    assert MAX_SHELL_TIMEOUT_MS == 250000
    parsed = parse_policy_action('bash {"command":"python solution.py"}')
    assert parsed.kind == 'bash'
    assert parsed.arguments == {'command': 'python solution.py', 'timeout_ms': 250000}
    assert parse_policy_action('bash {"command":"pwd","timeout_ms":250001}').kind == 'parser_error'


@pytest.mark.parametrize('text', ['submit', 'submit {}', '<tool_call>\n<function=submit>\n</function>\n</tool_call>'])
def test_explicit_submission(text):
    assert parse_policy_action(text).kind == 'submit'


@pytest.mark.parametrize('text', [
    'final', 'submit now', 'bash {"command":"pwd","workdir":"/tmp"}',
    'bash {"command":"a\\u0000b"}', 'bash {"command":"pwd","timeout_ms":true}',
    'bash {"command":"pwd","command":"ls"}',
    'apply_patch\n*** Begin Patch\n*** Add File: a\n+x\n*** End Patch',
])
def test_rejects_noncanonical_actions(text):
    assert parse_policy_action(text).kind == 'parser_error'


def test_multi_call_order_and_submit_isolation():
    parsed = parse_policy_action(envelope('pwd') + '\n' + envelope('ls'))
    assert parsed.kind == 'bash'
    assert [call.arguments['command'] for call in parsed.calls] == ['pwd', 'ls']
    assert parse_policy_action(envelope('pwd') + '\n<tool_call>\n<function=submit>\n</function>\n</tool_call>').kind == 'parser_error'
