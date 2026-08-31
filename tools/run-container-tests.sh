#!/usr/bin/env bash
set -Eeuo pipefail

usage() {
  cat <<'EOF'
Usage: tools/run-container-tests.sh [options]

Runs the Red and Red/System suites in a 32-bit Docker image, captures logs,
and writes summary.json and summary.md.

Options:
  --image IMAGE       Docker image (default: red-cognition/rebol-bootstrap:2.7.8)
  --rebol PATH        Rebol executable inside the image (default: /opt/rebol/rebol)
  --out DIR           Output directory (default: artifacts/test-run-<UTC timestamp>)
  --display DISPLAY   Set DISPLAY and start Xvfb when available (default: :0)
  --no-gui            Do not start Xvfb or set DISPLAY
  --help              Show this help
EOF
}

IMAGE="red-cognition/rebol-bootstrap:2.7.8"
REBOL="/opt/rebol/rebol"
OUT=""
DISPLAY_VALUE=":0"
USE_GUI=1

while (($#)); do
  case "$1" in
    --image) IMAGE=${2:?missing value for --image}; shift 2 ;;
    --rebol) REBOL=${2:?missing value for --rebol}; shift 2 ;;
    --out) OUT=${2:?missing value for --out}; shift 2 ;;
    --display) DISPLAY_VALUE=${2:?missing value for --display}; shift 2 ;;
    --no-gui) USE_GUI=0; shift ;;
    --help|-h) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$ROOT"

if [[ -z "$OUT" ]]; then
  OUT="$ROOT/artifacts/test-run-$(date -u +%Y%m%dT%H%M%SZ)"
elif [[ "$OUT" != /* ]]; then
  OUT="$ROOT/$OUT"
fi
mkdir -p "$OUT"

if ! command -v docker >/dev/null 2>&1; then
  echo "ERROR: docker is not installed or not on PATH" >&2
  exit 127
fi

if [[ ! -f "$ROOT/red.r" || ! -f "$ROOT/tests/run-all.r" || ! -f "$ROOT/system/tests/run-all.r" ]]; then
  echo "ERROR: run this script from the Red-Cognition repository checkout" >&2
  exit 2
fi

COMMIT=$(git rev-parse HEAD 2>/dev/null || printf 'unknown')
START=$(date -u +%Y-%m-%dT%H:%M:%SZ)

cat >"$OUT/manifest.txt" <<EOF
repository=$ROOT
commit=$COMMIT
image=$IMAGE
rebol=$REBOL
started=$START
platform=linux/386
EOF

run_suite() {
  local name=$1
  local script=$2
  local log="$OUT/${name}.stdout.log"
  local rcfile="$OUT/${name}.exit"

  echo "==> Running $name"
  set +e
  if (( USE_GUI )); then
    docker run --rm --platform linux/386 \
      --mount "type=bind,src=$ROOT,dst=/red" \
      --mount "type=bind,src=$OUT,dst=/artifacts" \
      --tmpfs "/red/quick-test/runnable:exec,mode=1777" \
      --workdir /red \
      -e "HOME=/root" \
      -e "DISPLAY=$DISPLAY_VALUE" \
      --entrypoint /bin/sh "$IMAGE" -ceu '
        if command -v Xvfb >/dev/null 2>&1; then
          Xvfb "$DISPLAY" -screen 0 1024x768x24 >/tmp/Xvfb.log 2>&1 &
          xvfb_pid=$!
          trap "kill $xvfb_pid 2>/dev/null || true" EXIT
          sleep 2
        fi
        exec "$1" -qws "$2" --batch
      ' sh "$REBOL" "$script" >"$log" 2>&1
  else
    docker run --rm --platform linux/386 \
      --mount "type=bind,src=$ROOT,dst=/red" \
      --mount "type=bind,src=$OUT,dst=/artifacts" \
      --tmpfs "/red/quick-test/runnable:exec,mode=1777" \
      --workdir /red \
      -e "HOME=/root" \
      --entrypoint "$REBOL" "$IMAGE" \
      -qws "$script" --batch >"$log" 2>&1
  fi
  local rc=$?
  set -e
  printf '%s\n' "$rc" >"$rcfile"
  cat "$log"
  echo "==> $name exit code: $rc"
}

run_suite red tests/run-all.r
# Preserve the Red suite log before the second suite overwrites quick-test.log.
if [[ -f "$ROOT/quick-test/quick-test.log" ]]; then
  cp "$ROOT/quick-test/quick-test.log" "$OUT/red.quick-test.log"
fi

run_suite red-system system/tests/run-all.r
if [[ -f "$ROOT/quick-test/quick-test.log" ]]; then
  cp "$ROOT/quick-test/quick-test.log" "$OUT/red-system.quick-test.log"
fi

END=$(date -u +%Y-%m-%dT%H:%M:%SZ)
printf 'finished=%s\n' "$END" >>"$OUT/manifest.txt"

python3 - "$OUT" "$COMMIT" "$IMAGE" "$REBOL" "$START" "$END" <<'PY'
import json
import re
import sys
from pathlib import Path

out = Path(sys.argv[1])
commit, image, rebol, started, finished = sys.argv[2:]


def parse_file(path):
    text = path.read_text(errors="replace") if path.exists() else ""
    def last(pattern):
        values = re.findall(pattern, text, flags=re.I | re.M)
        return int(values[-1]) if values else None
    return {
        "log": str(path),
        "exit_code": int((path.parent / (path.stem.replace(".stdout", "") + ".exit")).read_text().strip())
            if (path.parent / (path.stem.replace(".stdout", "") + ".exit")).exists() else None,
        "assertions": last(r"(?:Number of Assertions Performed|No of asserts)\s*:?\s*(\d+)"),
        "passed": last(r"(?:Number of Assertions Passed|Passed)\s*:?\s*(\d+)"),
        "failed": last(r"(?:Number of Assertions Failed|Failed)\s*:?\s*(\d+)"),
        "failure_marker": bool(re.search(r"TEST FAILURES|\bFailed\s*:?\s*[1-9]\d*|\*\*\s+(?:Access|Syntax|Internal|Script|Throw|Math|User)?\s*Error\s*:|^\s*not ok\b", text, re.I | re.M)),
    }

suites = [parse_file(out / "red.stdout.log"), parse_file(out / "red-system.stdout.log")]
for suite, qlog in zip(suites, [out / "red.quick-test.log", out / "red-system.quick-test.log"]):
    suite["quick_test_log"] = str(qlog) if qlog.exists() else None
    if qlog.exists():
        q = parse_file(qlog)
        for key in ("assertions", "passed", "failed"):
            if suite[key] is None:
                suite[key] = q[key]
        suite["failure_marker"] = suite["failure_marker"] or q["failure_marker"]

result = {
    "repository_commit": commit,
    "image": image,
    "rebol": rebol,
    "platform": "linux/386",
    "started": started,
    "finished": finished,
    "suites": suites,
    "overall_pass": all(
        s["exit_code"] == 0 and not s["failure_marker"] and (s["failed"] in (None, 0))
        for s in suites
    ),
}
(out / "summary.json").write_text(json.dumps(result, indent=2) + "\n")

lines = [
    "# Container Test Report", "", f"- Commit: `{commit}`", f"- Image: `{image}`",
    f"- Platform: `{result['platform']}`", f"- Started: `{started}`", f"- Finished: `{finished}`", "",
    "| Suite | Exit | Assertions | Passed | Failed | Failure marker |", "|---|---:|---:|---:|---:|---|",
]
for s, name in zip(suites, ["Red", "Red/System"]):
    lines.append(f"| {name} | {s['exit_code']} | {s['assertions']} | {s['passed']} | {s['failed']} | {s['failure_marker']} |")
lines += ["", f"**Overall result:** {'PASS' if result['overall_pass'] else 'FAIL'}", ""]
(out / "summary.md").write_text("\n".join(lines))
print(json.dumps(result, indent=2))
raise SystemExit(0 if result["overall_pass"] else 1)
PY
