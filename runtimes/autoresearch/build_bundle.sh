#!/usr/bin/env bash
# Build the isolated executor from source and record its actual content identity.
set -Eeuo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
[[ "$(uname -s)/$(uname -m)" == Linux/x86_64 ]] || { echo 'Build requires Linux x86_64.' >&2; exit 64; }
[[ "$(cc -dumpfullversion)" == 11.4.0 && "$(cc -dumpmachine)" == x86_64-linux-gnu ]] || { echo 'Use GCC 11.4.0 for the reproducible runtime build.' >&2; exit 65; }
FIRST=$(mktemp -d); SECOND=$(mktemp -d)
trap 'rm -rf -- "$FIRST" "$SECOND"' EXIT
export LC_ALL=C TZ=UTC SOURCE_DATE_EPOCH=0 PYTHONDONTWRITEBYTECODE=1
for target in "$FIRST" "$SECOND"; do
  cp "$SCRIPT_DIR/sandbox_supervisor.c" "$SCRIPT_DIR/python_wrapper.c" "$target/"
  (
    cd "$target"
    flags=(-O2 -g -Wall -Wextra -std=gnu11 "-ffile-prefix-map=$target=/src" "-fdebug-prefix-map=$target=/src" "-fmacro-prefix-map=$target=/src")
    cc "${flags[@]}" -o openmle-sandbox-supervisor sandbox_supervisor.c
    cc "${flags[@]}" -o openmle-python-wrapper python_wrapper.c
  )
done
mkdir -p "$SCRIPT_DIR/bin"
for binary in openmle-sandbox-supervisor openmle-python-wrapper; do
  cmp "$FIRST/$binary" "$SECOND/$binary"
  install -m 0555 "$FIRST/$binary" "$SCRIPT_DIR/bin/$binary"
done
python3 - "$SCRIPT_DIR" <<'PY'
import hashlib, json, pathlib, sys
root=pathlib.Path(sys.argv[1]); sys.path.insert(0,str(root))
import runtime_common as common
(root/'build-provenance.json').write_text(json.dumps({'compiler':'GCC 11.4.0','target':'x86_64-linux-gnu','independent_builds_identical':True},sort_keys=True)+'\n')
files=[]
for relative in sorted(common.ARTIFACT_LOCK_MEMBERS):
    file=root/relative
    if not file.is_file() or file.is_symlink(): raise SystemExit('Missing or unsafe build input: '+relative)
    files.append({'path':relative,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
lock={'schema':'openmle_fast_runtime_artifact_lock_v1','runtime_digest':common.RUNTIME_DIGEST,'files':files}
p=root/'artifact-lock.json';p.write_text(json.dumps(lock,sort_keys=True,indent=2)+'\n')
if not common.validate_artifact_lock(hashlib.sha256(p.read_bytes()).hexdigest(),artifact_root=str(root)):
    raise SystemExit('Built artifact verification failed')
print('Built and verified source/binary manifest. Runtime admission has NOT been performed.')
PY
python3 -m unittest discover -s "$SCRIPT_DIR/tests" -p 'test_*.py'
