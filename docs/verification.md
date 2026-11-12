# Testing

## Local tests

Install the test dependencies in Python 3.12:

```bash
python -m pip install -e '.[test]'
python -m pytest tests/unit
```

The unit suite covers action protocols, training configuration, checkpoint restart, task manifests, archive extraction, runtime inventories and service cleanup.

Check source syntax, internal imports and documentation links:

```bash
python scripts/check_release.py
```

## Training tests

After installing the [Linux/CUDA training dependencies](training.md#installation), run:

```bash
CAMP_TEST_TRAINING=1 python -m pytest tests/training
```

The environment variable enables tests that require the training stack. Default test collection runs the lightweight suite.

## Build packages

```bash
python -m pip install build
python -m build
```

The build produces a wheel and source archive under `dist/`. The wheel contains training/client modules and task manifests. Use the full source checkout for service deployment, including `runtimes/` and `third_party/`.
