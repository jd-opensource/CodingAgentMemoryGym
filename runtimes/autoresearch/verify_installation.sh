#!/usr/bin/env bash
# Run real isolation probes under an exclusive installation lock.
set -Eeuo pipefail
export PYTHONDONTWRITEBYTECODE=1
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRATCH=/tmp/camg-autoresearch
MARKER="$SCRATCH/verification.lock"
OWNER="$$:$(date +%s)"
[[ $(id -u) == 0 && -d "$SCRATCH" && ! -L "$SCRATCH" ]] || { echo 'Install the runtime as root before verification.' >&2; exit 64; }
cleanup() {
  if [[ -f "$MARKER" && ! -L "$MARKER" && "$(cat "$MARKER")" == "$OWNER" ]]; then rm -f -- "$MARKER"; fi
}
trap cleanup EXIT
trap 'rm -f -- "$SCRATCH/admission-stamp.json"; exit 130' INT
trap 'rm -f -- "$SCRATCH/admission-stamp.json"; exit 143' TERM
(set -o noclobber; printf '%s\n' "$OWNER" > "$MARKER") || { echo 'Another verification process owns this installation.' >&2; exit 65; }
rm -f -- "$SCRATCH/admission-stamp.json"
python3 "$SCRIPT_DIR/remote_probe.py"
cleanup
python3 - "$SCRIPT_DIR" <<'PY'
import os,sys
sys.path.insert(0,sys.argv[1]);import runtime_common as common
session=common.load_probe_session()
if session is None: raise SystemExit('Real probe session missing; refusing admission.')
marker=os.path.join(common.SCRATCH,'verification.lock')
value=common.bind_evidence_context({'schema':'camg_installation_lock_cleanup_v1','marker_present':os.path.lexists(marker),'lock_state':'released' if not os.path.lexists(marker) else 'owned','ok':not os.path.lexists(marker)},session)
path=os.path.join(common.SCRATCH,'evidence','installation-lock-cleanup.json')
with open(path+'.tmp','w') as f: f.write(common.canonical_json(value)+'\n')
os.replace(path+'.tmp',path)
PY
python3 "$SCRIPT_DIR/remote_probe.py" finalize-admission
