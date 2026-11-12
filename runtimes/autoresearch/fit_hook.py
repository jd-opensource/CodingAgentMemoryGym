import os
import runpy
import sys
import threading

FIT_FD = 199
FRAMEWORK_PREFIXES = (
    "sklearn",
    "xgboost",
    "lightgbm",
    "statsmodels",
)

def _fit_profile(frame, event, argument):
    del argument
    if event != "call" or frame.f_code.co_name != "fit":
        return
    module = str(frame.f_globals.get("__name__", ""))
    if module in FRAMEWORK_PREFIXES or module.startswith(
        tuple(prefix + "." for prefix in FRAMEWORK_PREFIXES)
    ):
        try:
            os.write(FIT_FD, b"F\n")
        except OSError:
            pass

def _install_fit_profile():
    sys.setprofile(_fit_profile)
    threading.setprofile(_fit_profile)

def bootstrap():
    mode = os.environ.pop("OPENMLE_PYTHON_MODE")
    arguments = list(sys.argv[1:])
    sys.executable = "/run/openmle-bin/python"
    sys.path.insert(0, "/workspace")
    _install_fit_profile()

    if mode == "script":
        if not arguments:
            raise SystemExit("managed launcher missing script")
        target = arguments[0]
        sys.argv = arguments
        sys.path[0] = os.path.abspath(os.path.dirname(target) or ".")
        runpy.run_path(target, run_name="__main__")
        return
    if mode == "command":
        if not arguments:
            raise SystemExit("managed launcher missing command")
        source = arguments[0]
        sys.argv = ["-c"] + arguments[1:]
        exec(compile(source, "<string>", "exec"), {"__name__": "__main__"})
        return
    if mode == "module":
        if not arguments:
            raise SystemExit("managed launcher missing module")
        module = arguments[0]
        sys.argv = [module] + arguments[1:]
        runpy.run_module(module, run_name="__main__", alter_sys=True)
        return
    if mode == "stdin":
        sys.argv = ["-"] + arguments
        source = sys.stdin.read()
        exec(compile(source, "<stdin>", "exec"), {"__name__": "__main__"})
        return
    raise SystemExit("unknown managed launcher mode")
