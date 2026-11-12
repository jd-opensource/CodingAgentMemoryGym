"""Regression checks for the released command-only Coding interface."""
import pytest
from camg.services.coding.actions import parse_policy_action


def envelope(command):
    return f'<tool_call>\n<function=bash>\n<parameter=command>\n{command}\n</parameter>\n</function>\n</tool_call>'


@pytest.mark.parametrize('text', ['bash {"command":"pwd"}', envelope('pwd')])
def test_command_only_shell(text):
    parsed = parse_policy_action(text)
    assert parsed.kind == 'bash'
    assert parsed.arguments == {'command': 'pwd', 'workdir': '.'}


def test_submission_is_a_shell_command_not_plain_text():
    parsed = parse_policy_action('bash {"command":"echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT"}')
    assert parsed.kind == 'bash'
    assert parse_policy_action('COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT').kind == 'parser_error'
    assert parse_policy_action('The issue is fixed.').kind == 'parser_error'


@pytest.mark.parametrize('text', [
    'bash {"command":"pwd","workdir":"."}',
    'bash {"command":"pwd","timeout_ms":1000}',
    'bash {"command":"pwd","command":"ls"}',
    'bash {"command":"a\\u0000b"}', 'bash []', 'bash {bad}', '',
    'apply_patch\n*** Begin Patch\n*** Add File: a\n+x\n*** End Patch',
])
def test_rejects_noncanonical_actions(text):
    assert parse_policy_action(text).kind == 'parser_error'


def test_multiple_complete_calls_preserve_order():
    parsed = parse_policy_action(envelope('pwd') + '\n' + envelope('ls'))
    assert parsed.kind == 'bash'
    assert [call.arguments['command'] for call in parsed.calls] == ['pwd', 'ls']


def test_bounded_reasoning_and_multiline_command():
    parsed = parse_policy_action('<think>Inspect first.</think>\n' + envelope('python - <<\'PY\'\nprint(1)\nPY'))
    assert parsed.kind == 'bash'
    assert parsed.thought == 'Inspect first.'
    assert '\nprint(1)\n' in parsed.arguments['command']
