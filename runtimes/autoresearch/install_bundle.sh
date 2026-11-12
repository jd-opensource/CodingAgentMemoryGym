#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRATCH=/tmp/camg-autoresearch
TARGET="${1:-$SCRATCH/source}"

validate_path_ancestor() {
  local candidate="$1"
  if [[ ! -e "$candidate" ]]; then
    return 0
  fi
  if [[ -L "$candidate" || ! -d "$candidate" ]]; then
    printf 'unsafe install path ancestor: %s\n' "$candidate" >&2
    return 1
  fi
  if [[ "$(stat -c '%u' -- "$candidate")" != 0 ]]; then
    printf 'install path ancestor is not root-owned: %s\n' "$candidate" >&2
    return 1
  fi
}

assert_no_mounts_below() {
  PYTHONDONTWRITEBYTECODE=1 python3 - "$1" <<'PY'
import os
import sys

target = os.path.realpath(sys.argv[1])
with open("/proc/self/mountinfo", "r") as handle:
    for line in handle:
        fields = line.rstrip("\n").split()
        if len(fields) < 5:
            continue
        mountpoint = (
            fields[4]
            .replace("\\040", " ")
            .replace("\\011", "\t")
            .replace("\\012", "\n")
            .replace("\\134", "\\")
        )
        mountpoint = os.path.normpath(mountpoint)
        try:
            inside = os.path.commonpath((target, mountpoint)) == target
        except ValueError:
            inside = False
        if inside:
            raise SystemExit("install target contains a mount: " + mountpoint)
PY
}

if [[ "$TARGET" != "$SCRATCH/source" ]]; then
  printf 'refusing non-contract install target: %s\n' "$TARGET" >&2
  exit 64
fi
validate_path_ancestor /tmp || exit 65
if (( (8#$(stat -c '%a' -- /tmp) & 8#1000) == 0 )); then
  printf '/tmp lacks the sticky bit\n' >&2
  exit 65
fi
if [[ ! -e "$SCRATCH" ]]; then
  mkdir -m 0700 -- "$SCRATCH"
fi
validate_path_ancestor "$SCRATCH" || exit 65
chmod 0700 -- "$SCRATCH"
if [[ -e "$TARGET" ]]; then
  validate_path_ancestor "$TARGET" || exit 65
  assert_no_mounts_below "$TARGET" || exit 65
  # Remove the legacy in-tree location during upgrades.
  rm -f -- "$TARGET/admission-stamp.json"
fi
rm -f -- "$SCRATCH/admission-stamp.json"

LOCK_SHA256="$(sha256sum "$SCRIPT_DIR/artifact-lock.json" | awk '{print $1}')"
PYTHONDONTWRITEBYTECODE=1 python3 - "$SCRIPT_DIR" "$LOCK_SHA256" <<'PY'
import sys

root, expected = sys.argv[1:]
sys.path.insert(0, root)
import runtime_common

if not runtime_common.validate_artifact_lock(expected, artifact_root=root):
    raise SystemExit("source artifact lock validation failed")
PY

STAGE="$(mktemp -d "$SCRATCH/.source.install.XXXXXXXX")"
BACKUP="$SCRATCH/source.previous.$BASHPID"
ROLLBACK=0
cleanup_install() {
  if [[ -n "${STAGE:-}" && -e "$STAGE" ]]; then
    rm -rf --one-file-system -- "$STAGE"
  fi
  if [[ "$ROLLBACK" == 1 && -e "$BACKUP" && ! -e "$TARGET" ]]; then
    mv -- "$BACKUP" "$TARGET"
  fi
}
trap cleanup_install EXIT INT TERM HUP

PYTHONDONTWRITEBYTECODE=1 python3 - "$SCRIPT_DIR" "$STAGE" <<'PY'
import os
import shutil
import sys

source, target = sys.argv[1:]
sys.path.insert(0, source)
import runtime_common

members = list(runtime_common.ARTIFACT_LOCK_MEMBERS) + ["artifact-lock.json"]
for relative in members:
    source_path = os.path.join(source, *relative.split("/"))
    target_path = os.path.join(target, *relative.split("/"))
    os.makedirs(os.path.dirname(target_path), mode=0o700, exist_ok=True)
    shutil.copyfile(source_path, target_path, follow_symlinks=False)
    os.chmod(
        target_path,
        0o555 if relative in runtime_common.ARTIFACT_EXECUTABLE_MEMBERS else 0o444,
    )
PY

PYTHONDONTWRITEBYTECODE=1 python3 - "$STAGE" "$LOCK_SHA256" <<'PY'
import sys

root, expected = sys.argv[1:]
sys.path.insert(0, root)
import runtime_common

if not runtime_common.validate_install_inventory(root, expected):
    raise SystemExit("staged install inventory validation failed")
PY

# A redeploy never inherits live admission or evidence from an earlier source,
# boot, rootfs, runner pair, or verification-lock release.
for owned in "$SCRATCH/evidence" "$SCRATCH/probe-inputs"; do
  if [[ -e "$owned" ]]; then
    validate_path_ancestor "$owned" || exit 65
    assert_no_mounts_below "$owned" || exit 65
    rm -rf --one-file-system -- "$owned"
  fi
done

if [[ -e "$BACKUP" ]]; then
  printf 'stale installer backup exists: %s\n' "$BACKUP" >&2
  exit 65
fi
if [[ -e "$TARGET" ]]; then
  ROLLBACK=1
  mv -- "$TARGET" "$BACKUP"
fi
mv -- "$STAGE" "$TARGET"
STAGE=""
ROLLBACK=0

if [[ -e "$BACKUP" ]]; then
  assert_no_mounts_below "$BACKUP" || exit 65
  rm -rf --one-file-system -- "$BACKUP"
fi

PYTHONDONTWRITEBYTECODE=1 "$TARGET/public_runner.py" metadata \
  | python3 -m json.tool >/dev/null
PYTHONDONTWRITEBYTECODE=1 "$TARGET/private_runner.py" metadata \
  | python3 -m json.tool >/dev/null
PYTHONDONTWRITEBYTECODE=1 python3 - "$TARGET" "$LOCK_SHA256" <<'PY'
import sys

root, expected = sys.argv[1:]
sys.path.insert(0, root)
import runtime_common

if not runtime_common.validate_install_inventory(root, expected):
    raise SystemExit("installed inventory validation failed")
PY

printf '%s\n' "$TARGET"
