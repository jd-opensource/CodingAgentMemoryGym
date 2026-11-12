from __future__ import print_function

import base64
import contextlib
import importlib.util
import inspect
import io
import json
import math
import numbers
import os
import sys
import uuid

RESULT_SCHEMA = "openmle_fast_private_worker_result_v1"
SAFE_DUMPS = json.dumps
SAFE_EXCEPTION = Exception
SAFE_FLOAT = float
SAFE_ISFINITE = math.isfinite
SAFE_REAL = numbers.Real
SAFE_TYPE = type
SAFE_WRITE = os.write
ADMITTED_EVALUATOR_DOMAIN_ERROR_ARGS = (
    "Spearman correlation is undefined for the provided data.",
)

def main(argv):
    direction = False
    try:
        direction, forms = _parse_arguments(argv)
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(
            io.StringIO()
        ):
            result = _grade(
                "/workspace/metric.py",
                "/workspace/answer.csv",
                "/workspace/submission.csv",
                direction,
                forms,
            )
    except BaseException:  
        result = _result("infrastructure_fault", None, direction)
    payload = SAFE_DUMPS(result, sort_keys=True, separators=(",", ":")).encode("utf-8")
    SAFE_WRITE(1, payload)
    return 0

def _parse_arguments(argv):
    if len(argv) != 3 or argv[1] not in ("true", "false"):
        raise ValueError("invalid worker arguments")
    direction = argv[1] == "true"
    raw = base64.b64decode(argv[2].encode("ascii"), validate=True)
    if len(raw) > 8192:
        raise ValueError("validation convention list too large")
    forms = json.loads(raw.decode("utf-8"))
    if (
        not isinstance(forms, list)
        or len(forms) > 64
        or any(not isinstance(item, str) or len(item.encode("utf-8")) > 256 for item in forms)
    ):
        raise ValueError("invalid validation convention list")
    return direction, tuple(forms)

def _grade(metric_path, answer_path, submission_path, expected_direction, success_forms):
    import pandas as pd

    try:
        prediction = pd.read_csv(submission_path)
    except BaseException:
        return _result("invalid_submission", None, expected_direction)
    truth = pd.read_csv(answer_path)
    instance, module_name = _load_native_scorer(metric_path)
    try:
        direction = getattr(instance, "higher_is_better", None)
        if type(direction) is not bool or direction != expected_direction:
            raise ValueError("direction drift")
        try:
            validation = instance.validate_submission(prediction.copy(), truth.copy())
        except BaseException:
            return _result("invalid_submission", None, expected_direction)
        if not _canonicalize_validation(validation, success_forms):
            return _result("invalid_submission", None, expected_direction)

        try:
            score_value = instance.evaluate(
                y_true=truth.copy(), y_pred=prediction.copy()
            )
        except BaseException as error:
            if (
                SAFE_TYPE(error) is SAFE_EXCEPTION
                and error.args == ADMITTED_EVALUATOR_DOMAIN_ERROR_ARGS
            ):
                return _result("invalid_submission", None, expected_direction)
            raise
        if isinstance(score_value, bool) or not isinstance(score_value, SAFE_REAL):
            raise TypeError("invalid native score")
        score = SAFE_FLOAT(score_value)
        if not SAFE_ISFINITE(score):
            return _result("invalid_submission", None, expected_direction)
        return _result("graded", score, expected_direction)
    finally:
        sys.modules.pop(module_name, None)

def _load_native_scorer(path):
    module_name = "_openmle_fast_native_" + uuid.uuid4().hex
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load native scorer")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(module_name, None)
        raise
    eligible = [
        value
        for value in vars(module).values()
        if inspect.isclass(value)
        and value.__module__ == module_name
        and callable(getattr(value, "validate_submission", None))
        and callable(getattr(value, "evaluate", None))
    ]
    if len(eligible) != 1:
        sys.modules.pop(module_name, None)
        raise ValueError("native scorer class contract drift")
    return eligible[0](), module_name

def _canonicalize_validation(value, success_forms):
    if type(value) is bool:
        return value
    if (
        isinstance(value, tuple)
        and len(value) == 2
        and type(value[0]) is bool
        and isinstance(value[1], str)
    ):
        return value[0]
    if isinstance(value, str):
        if not success_forms:
            raise ValueError("unadmitted string validation convention")
        return value in success_forms
    raise ValueError("validator convention drift")

def _result(classification, score, direction):
    return {
        "schema": RESULT_SCHEMA,
        "classification": classification,
        "native_score": score,
        "higher_is_better": direction,
    }

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
