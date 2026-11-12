#!/usr/bin/env bash
# Remove only this idle installation after verifying zero owned resources.
set -Eeuo pipefail
ROOT=/tmp/camg-autoresearch
[[ "${1:-}" == --remove-idle-installation ]] || { echo 'Usage: remote_cleanup.sh --remove-idle-installation' >&2; exit 64; }
[[ $(id -u) == 0 && -d "$ROOT" && ! -L "$ROOT" ]] || exit 65
PYTHONDONTWRITEBYTECODE=1 python3 - "$ROOT" <<'PY'
import os,sys
root=sys.argv[1];sys.path.insert(0,root+'/source');import runtime_common as common
if os.path.lexists(root+'/verification.lock'):raise SystemExit('Verification is running.')
if not common.residue_is_zero(common.residue_snapshot()):raise SystemExit('Runtime still owns resources; refusing deletion.')
# Services can be idle while still listening. Any separate interpreter that
# imports this installation must stop before the user explicitly removes it.
for pid in os.listdir('/proc'):
    if not pid.isdigit() or int(pid) in {os.getpid(),os.getppid()}:continue
    try:cmd=open('/proc/'+pid+'/cmdline','rb').read()
    except (FileNotFoundError,ProcessLookupError):continue
    if (root+'/source').encode() in cmd:raise SystemExit('An installed runtime process is still alive: '+pid)
PY
rm -rf --one-file-system -- "$ROOT"
