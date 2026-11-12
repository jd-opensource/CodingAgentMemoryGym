import ast
import io
import json
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

_TESTS = Path(__file__).resolve().parent
_ROOT = _TESTS.parent
sys.path.insert(0, str(_ROOT))
sys.path.insert(0, str(_TESTS))

import public_runner  
import test_protocols  

_schema_error = test_protocols._schema_error
ROOT = test_protocols.ROOT

RECEIPT_SCHEMA_NAME = "public-runner-receipt.schema.json"

FAILURE_CLASSES = (
    "wall_timeout",
    "managed_runtime_limit",
    "action_budget_exhausted",
)

class BudgetLedgerReceiptTest(unittest.TestCase):
    def test_exception_class_validates_failure_class(self) -> None:
        for allowed in FAILURE_CLASSES:
            exc = public_runner.BudgetLedgerExhausted("msg", failure_class=allowed)
            self.assertEqual(exc.failure_class, allowed)
        with self.assertRaises(ValueError):
            public_runner.BudgetLedgerExhausted("msg", failure_class="output_limit")
        self.assertIsInstance(
            public_runner.BudgetLedgerExhausted("m", failure_class="wall_timeout"),
            RuntimeError,
        )

    def test_budget_receipt_is_policy_not_infrastructure(self) -> None:
        for failure_class in FAILURE_CLASSES:
            receipt = public_runner.budget_exhausted_receipt(failure_class)
            self.assertFalse(receipt["infrastructure_fault"])
            self.assertEqual(receipt["failure_class"], failure_class)
            schema = json.loads((ROOT / "schemas" / RECEIPT_SCHEMA_NAME).read_text())
            self.assertIsNone(_schema_error(schema, receipt, schema))

    def _run_main_execute(self, side_effect):
        request = {
            "schema": public_runner.REQUEST_SCHEMA,
            "workspace": "/schema-fixture",
            "command": "true",
            "timeout_ms": 1000,
            "managed_runtime_budget_ms": 750,
        }
        with mock.patch.object(public_runner, "execute", side_effect=side_effect), \
                mock.patch.object(
                    public_runner.common, "read_stdin_json", return_value=dict(request)
                ), \
                mock.patch.object(public_runner, "_write_public_fault") as fault_writer:
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                code = public_runner.main(["public_runner.py", "execute"])
        return code, buffer.getvalue(), fault_writer

    def test_catch_all_routes_budget_exhaustion_to_policy_receipt(self) -> None:
        for failure_class in FAILURE_CLASSES:
            code, out, fault_writer = self._run_main_execute(
                public_runner.BudgetLedgerExhausted(
                    "ledger exhaustion", failure_class=failure_class
                )
            )
            self.assertEqual(code, 0)
            receipt = json.loads(out)
            self.assertFalse(receipt["infrastructure_fault"])
            self.assertEqual(receipt["failure_class"], failure_class)
            fault_writer.assert_not_called()

    def test_admission_fault_stays_infrastructure(self) -> None:
        code, out, fault_writer = self._run_main_execute(
            RuntimeError("request exhausted the host preparation grace")
        )
        self.assertEqual(code, 0)
        receipt = json.loads(out)
        self.assertTrue(receipt["infrastructure_fault"])
        self.assertEqual(
            receipt["failure_class"],
            "runner_infrastructure_fault",
        )
        fault_writer.assert_called_once()

    def test_wall_boundary_arithmetic(self) -> None:
        episode_wall_ms = public_runner.common.PUBLIC_LIMITS["episode_wall_ms"]
        grace = public_runner.ACTION_COMPLETION_GRACE_MS
        self.assertEqual(episode_wall_ms, 180_000)
        self.assertEqual(grace, 20_000)

        def action_timeout(elapsed_ms, request_ms):
            remaining_wall_ms = int(episode_wall_ms - elapsed_ms)
            return min(request_ms, remaining_wall_ms - grace)

        self.assertEqual(action_timeout(0, 159_000), 159_000)
        self.assertGreater(action_timeout(0, 159_000), 0)
        
        self.assertEqual(action_timeout(0, 160_000), 160_000)
        self.assertEqual(160_000, episode_wall_ms - grace)
        
        self.assertTrue(180_000 >= episode_wall_ms)
        
        self.assertLessEqual(action_timeout(165_000, 159_000), 0)

    def test_all_five_budget_branches_raise_policy_terminal(self) -> None:
        tree = ast.parse((_ROOT / "public_runner.py").read_text())

        def class_arg(node):
            for kw in node.exc.keywords:
                if kw.arg == "failure_class":
                    return ast.literal_eval(kw.value)
            raise AssertionError("missing failure_class keyword")

        budget_raises = {}
        runtime_closed = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.Raise) or node.exc is None:
                continue
            func = node.exc.func if isinstance(node.exc, ast.Call) else node.exc
            name = getattr(func, "id", None) or getattr(func, "attr", None)
            if name == "BudgetLedgerExhausted":
                budget_raises[ast.literal_eval(node.exc.args[0])] = class_arg(node)
            elif name == "RuntimeErrorClosed":
                runtime_closed.append(ast.literal_eval(node.exc.args[0]))
        expected = {
            "shell action ledger exhausted": "action_budget_exhausted",
            "episode wall ledger exhausted": "wall_timeout",
            "episode managed-runtime ledger exhausted": "managed_runtime_limit",
            "episode wall ledger leaves no action budget": "wall_timeout",
            "episode managed-runtime ledger leaves no action budget": (
                "managed_runtime_limit"
            ),
        }
        self.assertEqual(budget_raises, expected)
        self.assertIn(
            "request exhausted the host preparation grace", runtime_closed
        )

if __name__ == "__main__":
    unittest.main()
