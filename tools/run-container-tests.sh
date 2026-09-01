#!/usr/bin/env bash
# Diagnostic wrapper for Red / Red/System container execution.
#
# EV-01 contract: observability only. This script must not change Red or
# Red/System semantics, expected test results, or the GitHub job timeout.
set -Eeuo pipefail

usage() {
  cat <<'EOF'
Usage: tools/run-container-tests.sh [options]

Runs a Rebol identity smoke check, then the Red and Red/System suites in a
32-bit Docker image. Streams logs, emits elapsed-time heartbeats, and writes
execution records even if the job is cancelled.

Options:
  --image IMAGE             Docker image (default: red-cognition/rebol-bootstrap:2.7.8)
  --rebol PATH              Rebol executable inside the image (default: /opt/rebol/rebol)
  --out DIR                 Output directory (default: artifacts/test-run-<UTC timestamp>)
  --display DISPLAY         Set DISPLAY and start Xvfb when available (default: :0)
  --no-gui                  Do not start Xvfb or set DISPLAY
  --heartbeat-seconds N     Heartbeat interval (default: 60)
  --skip-identity           Skip the Rebol identity smoke check
  --phase PHASE             identity | hello | red | red-system | all (default: all)
  --hello-timeout N         Seconds to allow red.r tests/hello.red (default: 480; 0 disables)
  --help                    Show this help
EOF
}

IMAGE="red-cognition/rebol-bootstrap:2.7.8"
REBOL="/opt/rebol/rebol"
OUT=""
DISPLAY_VALUE=":0"
USE_GUI=1
HEARTBEAT_SECONDS=60
RUN_IDENTITY=1
PHASE=all
HELLO_TIMEOUT=480

while (($#)); do
  case "$1" in
    --image) IMAGE=${2:?missing value for --image}; shift 2 ;;
    --rebol) REBOL=${2:?missing value for --rebol}; shift 2 ;;
    --out) OUT=${2:?missing value for --out}; shift 2 ;;
    --display) DISPLAY_VALUE=${2:?missing value for --display}; shift 2 ;;
    --no-gui) USE_GUI=0; shift ;;
    --heartbeat-seconds) HEARTBEAT_SECONDS=${2:?missing value for --heartbeat-seconds}; shift 2 ;;
    --skip-identity) RUN_IDENTITY=0; shift ;;
    --phase)
      PHASE=${2:?missing value for --phase}
      case "$PHASE" in
        identity|hello|red|red-system|all) ;;
        *) echo "Unknown --phase: $PHASE" >&2; usage >&2; exit 2 ;;
      esac
      shift 2
      ;;
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
IMAGE_ID=$(docker image inspect "$IMAGE" --format '{{.Id}}' 2>/dev/null || printf 'unknown')
START=$(date -u +%Y-%m-%dT%H:%M:%SZ)
RUNNER_PID=$$
CURRENT_SUITE=""
CURRENT_CONTAINER=""
HEARTBEAT_PID=""
HEARTBEAT_STOP=""
FINALIZED=0
OVERALL_STATE="STARTED"
TERMINATION_SIGNAL=""

iso_now() { date -u +%Y-%m-%dT%H:%M:%SZ; }

gha_notice() {
  local title=$1
  shift
  echo "==> $*"
  echo "::notice title=${title}::$*"
}

gha_error() {
  local title=$1
  shift
  echo "==> $*" >&2
  echo "::error title=${title}::$*"
}

gha_warning() {
  local title=$1
  shift
  echo "==> $*" >&2
  echo "::warning title=${title}::$*"
}

append_phase_status() {
  printf '%s %s\n' "$(iso_now)" "$*" >>"$OUT/phase-status.txt"
}

exit_from_suite() {
  local name=$1
  local rcfile="$OUT/${name}.exit"
  local rc=1
  if [[ -f "$rcfile" ]]; then
    rc=$(cat "$rcfile")
  fi
  echo "==> phase=$PHASE suite=$name returning $rc"
  exit "$rc"
}

preview_text() {
  local path=$1
  if [[ -f "$path" ]]; then
    python3 - "$path" <<'PY'
from pathlib import Path
import sys
text = Path(sys.argv[1]).read_text(errors="replace")
print(text[-1200:].replace("\r", "\n"))
PY
  fi
}

copy_quick_test_logs() {
  local name=$1
  if [[ -f "$ROOT/quick-test/quick-test.log" ]]; then
    cp -f "$ROOT/quick-test/quick-test.log" "$OUT/${name}.quick-test.log"
  fi
  if [[ -f "$ROOT/tests/quick-test.log" ]]; then
    cp -f "$ROOT/tests/quick-test.log" "$OUT/${name}.tests-quick-test.log"
  fi
  if [[ -f "$ROOT/system/tests/quick-test.log" ]]; then
    cp -f "$ROOT/system/tests/quick-test.log" "$OUT/${name}.system-quick-test.log"
  fi
}

write_incomplete_summary() {
  local note=${1:-execution still in progress or interrupted}
  cat >"$OUT/summary.md" <<EOF
# Container Test Report

- Commit: \`$COMMIT\`
- Image: \`$IMAGE\`
- Platform: \`linux/386\`
- Started: \`$START\`
- Updated: \`$(iso_now)\`
- Runner PID: \`$RUNNER_PID\`
- Current suite: \`${CURRENT_SUITE:-none}\`
- Overall state: \`$OVERALL_STATE\`
- Note: $note

This file is written continuously so a GitHub cancellation still leaves
attributable evidence. It is not a pass/fail claim for Red.
EOF
}

write_execution_record() {
  local name=$1
  local script=$2
  local state=$3
  local started_at=$4
  local started_epoch=$5
  local log=$6
  local cname=$7
  local rc=${8-}
  RC_SUITE=$name \
  RC_SCRIPT=$script \
  RC_STATE=$state \
  RC_STARTED_AT=$started_at \
  RC_STARTED_EPOCH=$started_epoch \
  RC_LOG=$log \
  RC_CNAME=$cname \
  RC_EXIT=$rc \
  RC_SIGNAL=$TERMINATION_SIGNAL \
  RC_OUT=$OUT \
  RC_COMMIT=$COMMIT \
  RC_REBOL=$REBOL \
  RC_IMAGE=$IMAGE \
  RC_IMAGE_ID=$IMAGE_ID \
  python3 <<'PY'
import json
import os
from datetime import datetime, timezone
from pathlib import Path

out = Path(os.environ["RC_OUT"])
name = os.environ["RC_SUITE"]
state = os.environ["RC_STATE"]
started_epoch = int(os.environ["RC_STARTED_EPOCH"])
elapsed = int(__import__("time").time()) - started_epoch
log = Path(os.environ["RC_LOG"])
qlog = out / f"{name}.quick-test.log"
exit_raw = os.environ.get("RC_EXIT", "")
signal_raw = os.environ.get("RC_SIGNAL", "")
ended_at = None
if state not in ("STARTED", "RUNNING"):
    ended_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
obj = {
    "suite": name,
    "script": os.environ["RC_SCRIPT"],
    "state": state,
    "commit": os.environ["RC_COMMIT"],
    "rebol": os.environ["RC_REBOL"],
    "image": os.environ["RC_IMAGE"],
    "architecture": "linux/386",
    "command": os.environ["RC_SCRIPT"],
    "container_name": os.environ["RC_CNAME"],
    "started_at": os.environ["RC_STARTED_AT"],
    "ended_at": ended_at,
    "elapsed_seconds": elapsed,
    "exit_code": int(exit_raw) if exit_raw != "" else None,
    "signal": signal_raw or None,
    "log": str(log),
    "quick_test_log": str(qlog) if qlog.exists() else None,
    "log_bytes": log.stat().st_size if log.exists() else 0,
    "quick_test_log_bytes": qlog.stat().st_size if qlog.exists() else 0,
}
(out / f"{name}.execution.json").write_text(json.dumps(obj, indent=2) + "\n")
PY
}

stop_heartbeat() {
  if [[ -n "$HEARTBEAT_STOP" ]]; then
    mkdir -p "$(dirname "$HEARTBEAT_STOP")"
    : >"$HEARTBEAT_STOP"
  fi
  if [[ -n "$HEARTBEAT_PID" ]] && kill -0 "$HEARTBEAT_PID" 2>/dev/null; then
    kill "$HEARTBEAT_PID" 2>/dev/null || true
    wait "$HEARTBEAT_PID" 2>/dev/null || true
  fi
  HEARTBEAT_PID=""
}

start_heartbeat() {
  local name=$1
  local script=$2
  local started_at=$3
  local started_epoch=$4
  local log=$5
  local cname=$6
  HEARTBEAT_STOP="$OUT/${name}.heartbeat.stop"
  rm -f "$HEARTBEAT_STOP"
  (
    while [[ ! -f "$HEARTBEAT_STOP" ]]; do
      sleep "$HEARTBEAT_SECONDS"
      [[ -f "$HEARTBEAT_STOP" ]] && break
      elapsed=$(( $(date +%s) - started_epoch ))
      echo "==> $name still running: ${elapsed}s"
      echo "    utc=$(iso_now) container=$cname"
      if [[ -f "$log" ]]; then
        echo "    stdout_bytes=$(wc -c <"$log" | tr -d ' ')"
      else
        echo "    stdout_bytes=0"
      fi
      copy_quick_test_logs "$name"
      if [[ -f "$OUT/${name}.quick-test.log" ]]; then
        echo "    quick_test_log_bytes=$(wc -c <"$OUT/${name}.quick-test.log" | tr -d ' ')"
        echo "==> $name quick-test.log tail:"
        preview_text "$OUT/${name}.quick-test.log" | tail -n 20 || true
      fi
      if [[ -f "$log" && -s "$log" ]]; then
        echo "==> $name stdout tail:"
        preview_text "$log" | tail -n 20 || true
      fi
      if docker top "$cname" >/tmp/rc-docker-top."$name" 2>/dev/null; then
        echo "==> $name docker top:"
        cat /tmp/rc-docker-top."$name" || true
      else
        echo "    docker top: unavailable"
      fi
      write_execution_record "$name" "$script" "RUNNING" "$started_at" "$started_epoch" "$log" "$cname" ""
      write_incomplete_summary "suite $name still running after ${elapsed}s"
    done
  ) &
  HEARTBEAT_PID=$!
}

docker_run_script() {
  local script=$1
  local cname=$2
  shift 2
  local env_args=(-e "HOME=/root")
  if (( USE_GUI )); then
    env_args+=(-e "DISPLAY=$DISPLAY_VALUE")
  fi
  docker run --rm --name "$cname" --platform linux/386 \
    --mount "type=bind,src=$ROOT,dst=/red" \
    --mount "type=bind,src=$OUT,dst=/artifacts" \
    --mount "type=tmpfs,dst=/red/quick-test/runnable,tmpfs-mode=1777" \
    --workdir /red \
    "${env_args[@]}" \
    --entrypoint /bin/sh "$IMAGE" -ceu '
      gui="$3"
      if [ "$gui" = "1" ] && command -v Xvfb >/dev/null 2>&1; then
        Xvfb "$DISPLAY" -screen 0 1024x768x24 >/tmp/Xvfb.log 2>&1 &
        xvfb_pid=$!
        trap "kill $xvfb_pid 2>/dev/null || true" EXIT
        sleep 2
      fi
      rebol="$1"
      script="$2"
      shift 3
      if command -v stdbuf >/dev/null 2>&1; then
        exec stdbuf -oL -eL "$rebol" -qws "$script" "$@"
      fi
      exec "$rebol" -qws "$script" "$@"
    ' sh "$REBOL" "$script" "$USE_GUI" "$@"
}

finalize_from_signal() {
  local sig=$1
  TERMINATION_SIGNAL=$sig
  OVERALL_STATE="CANCELLED"
  if [[ "$sig" == "TERM" ]]; then
    OVERALL_STATE="TIMED_OUT"
  fi
  echo "==> RUNNER RECEIVED SIG$sig" >&2
  echo "==> overall_state=$OVERALL_STATE suite=${CURRENT_SUITE:-none}" >&2
  gha_error "EV-01 $OVERALL_STATE" "signal=SIG$sig suite=${CURRENT_SUITE:-none} commit=$COMMIT"
  if [[ -n "$CURRENT_SUITE" ]]; then
    copy_quick_test_logs "$CURRENT_SUITE"
    if [[ -f "$OUT/${CURRENT_SUITE}.execution.json" ]]; then
      python3 - "$OUT/${CURRENT_SUITE}.execution.json" "$OVERALL_STATE" "$sig" <<'PY'
import json, sys
from pathlib import Path
from datetime import datetime, timezone
path = Path(sys.argv[1])
obj = json.loads(path.read_text())
obj["state"] = sys.argv[2]
obj["signal"] = sys.argv[3]
obj["ended_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
path.write_text(json.dumps(obj, indent=2) + "\n")
PY
    fi
  fi
  write_incomplete_summary "runner received SIG$sig; partial logs preserved"
  if [[ -n "$CURRENT_CONTAINER" ]]; then
    docker kill "$CURRENT_CONTAINER" >/dev/null 2>&1 || true
  fi
  stop_heartbeat
}

on_exit() {
  local rc=$?
  if (( FINALIZED )); then
    exit "$rc"
  fi
  FINALIZED=1
  stop_heartbeat
  if [[ -n "$CURRENT_CONTAINER" ]]; then
    docker kill "$CURRENT_CONTAINER" >/dev/null 2>&1 || true
  fi
  if [[ "$OVERALL_STATE" == "STARTED" || "$OVERALL_STATE" == "RUNNING" ]]; then
    if [[ $rc -eq 0 ]]; then
      OVERALL_STATE="COMPLETED"
    else
      OVERALL_STATE="FAILED"
    fi
  fi
  printf 'finished=%s\n' "$(iso_now)" >>"$OUT/manifest.txt"
  printf 'overall_state=%s\n' "$OVERALL_STATE" >>"$OUT/manifest.txt"
  printf 'exit_code=%s\n' "$rc" >>"$OUT/manifest.txt"
  if [[ -n "$TERMINATION_SIGNAL" ]]; then
    printf 'signal=%s\n' "$TERMINATION_SIGNAL" >>"$OUT/manifest.txt"
  fi
  exit "$rc"
}

trap 'finalize_from_signal INT; exit 130' INT
trap 'finalize_from_signal TERM; exit 143' TERM
trap 'on_exit' EXIT

cat >"$OUT/manifest.txt" <<EOF
repository=$ROOT
commit=$COMMIT
image=$IMAGE
rebol=$REBOL
started=$START
platform=linux/386
runner_pid=$RUNNER_PID
heartbeat_seconds=$HEARTBEAT_SECONDS
observability=stream+heartbeat+execution-json
phase=$PHASE
EOF

write_incomplete_summary "runner started; no suite has completed yet"

echo "==> EV-01 container runner"
echo "    commit=$COMMIT"
echo "    image=$IMAGE"
echo "    rebol=$REBOL"
echo "    platform=linux/386"
echo "    out=$OUT"
echo "    heartbeat_seconds=$HEARTBEAT_SECONDS"
echo "    phase=$PHASE"
echo "    image_id=$IMAGE_ID"
echo "    hello_timeout=$HELLO_TIMEOUT"
echo "    started=$START"
gha_notice "EV-01 runner" "commit=$COMMIT phase=$PHASE image=$IMAGE image_id=$IMAGE_ID"
: >"$OUT/phase-status.txt"
append_phase_status "RUNNER_START commit=$COMMIT phase=$PHASE"

run_suite() {
  local name=$1
  local script=$2
  shift 2
  local extra=("$@")
  local log="$OUT/${name}.stdout.log"
  local rcfile="$OUT/${name}.exit"
  local started_at
  local started_epoch
  local cname
  local rc=0
  local killer=""
  local suite_timeout=${SUITE_TIMEOUT:-0}
  local cmd="$REBOL -qws $script"
  if ((${#extra[@]})); then
    cmd="$cmd ${extra[*]}"
  fi

  started_at=$(iso_now)
  started_epoch=$(date +%s)
  cname="rc-${name}-$$-${started_epoch}"
  CURRENT_SUITE=$name
  CURRENT_CONTAINER=$cname
  OVERALL_STATE="RUNNING"
  : >"$log"

  printf '%s\n' "$cmd" >"$OUT/${name}.command.txt"
  cat >"$OUT/${name}.environment.txt" <<EOF
commit=$COMMIT
suite=$name
image=$IMAGE
image_id=$IMAGE_ID
architecture=linux/386
rebol=$REBOL
command=$cmd
started=$started_at
suite_timeout=$suite_timeout
heartbeat_seconds=$HEARTBEAT_SECONDS
phase=$PHASE
EOF

  echo "==> Running $name"
  echo "    image=$IMAGE"
  echo "    image_id=$IMAGE_ID"
  echo "    script=$script"
  echo "    rebol=$REBOL"
  echo "    platform=linux/386"
  echo "    commit=$COMMIT"
  echo "    container=$cname"
  echo "    started=$started_at"
  echo "    command=$cmd"
  echo "    log=$log"
  echo "    suite_timeout=$suite_timeout"
  gha_notice "EV-01 $name" "START commit=$COMMIT command=$cmd"
  append_phase_status "START $name $cmd"

  write_execution_record "$name" "$cmd" "STARTED" "$started_at" "$started_epoch" "$log" "$cname" ""
  start_heartbeat "$name" "$cmd" "$started_at" "$started_epoch" "$log" "$cname"

  if (( suite_timeout > 0 )); then
    (
      sleep "$suite_timeout"
      echo "==> $name suite-timeout ${suite_timeout}s; killing $cname" >&2
      docker kill "$cname" >/dev/null 2>&1 || true
    ) &
    killer=$!
  fi

  set +e
  set +o pipefail
  docker_run_script "$script" "$cname" "${extra[@]}" 2>&1 | tee "$log" | tr '\r' '\n'
  rc=${PIPESTATUS[0]}
  set -o pipefail
  set -e

  if [[ -n "$killer" ]]; then
    kill "$killer" 2>/dev/null || true
    wait "$killer" 2>/dev/null || true
  fi

  stop_heartbeat
  copy_quick_test_logs "$name"

  local elapsed=$(( $(date +%s) - started_epoch ))
  local state="COMPLETED"
  if (( suite_timeout > 0 )) && { [[ $rc -eq 137 || $rc -eq 143 ]] || (( elapsed >= suite_timeout )); }; then
    state="TIMED_OUT"
    rc=124
    TERMINATION_SIGNAL=${TERMINATION_SIGNAL:-TERM}
    gha_error "EV-01 $name" "TIMED_OUT after ${elapsed}s limit=${suite_timeout}s command=$cmd"
    append_phase_status "TIMED_OUT $name elapsed=${elapsed}s"
  elif [[ $rc -eq 0 ]]; then
    gha_notice "EV-01 $name" "COMPLETED exit=0 elapsed=${elapsed}s command=$cmd"
    append_phase_status "COMPLETED $name elapsed=${elapsed}s"
  else
    state="FAILED"
    gha_warning "EV-01 $name" "FAILED exit=$rc elapsed=${elapsed}s command=$cmd"
    append_phase_status "FAILED $name exit=$rc elapsed=${elapsed}s"
  fi

  printf '%s\n' "$rc" >"$rcfile"
  write_execution_record "$name" "$cmd" "$state" "$started_at" "$started_epoch" "$log" "$cname" "$rc"
  CURRENT_CONTAINER=""
  echo "==> $name state: $state"
  echo "==> $name exit code: $rc"
  echo "==> $name elapsed: ${elapsed}s"
  echo "==> $name stdout_bytes: $(wc -c <"$log" | tr -d ' ')"
  return 0
}

if [[ $PHASE == all || $PHASE == identity ]] && (( RUN_IDENTITY )); then
  cat >"$OUT/rebol-identity.r" <<'EOF'
REBOL [
    Title: "Rebol identity smoke check"
]
print ["rebol-version:" system/version]
print "rebol-identity-ok"
quit
EOF
  run_suite rebol-identity /artifacts/rebol-identity.r
  identity_rc=$(cat "$OUT/rebol-identity.exit" 2>/dev/null || echo missing)
  if [[ "$identity_rc" != "0" ]] || ! grep -q "rebol-identity-ok" "$OUT/rebol-identity.stdout.log" 2>/dev/null; then
    echo "WARNING: Rebol identity smoke check did not succeed (rc=$identity_rc)" >&2
    if [[ $PHASE == identity ]]; then
      write_incomplete_summary "Rebol identity smoke check failed"
      exit_from_suite rebol-identity
    fi
    echo "WARNING: continuing so later phases can still run" >&2
    write_incomplete_summary "Rebol identity smoke check failed; continuing"
  else
    echo "==> Rebol identity smoke check PASS"
    if [[ $PHASE == identity ]]; then
      exit 0
    fi
  fi
fi

if [[ $PHASE == all || $PHASE == hello ]]; then
  if [[ -f "$ROOT/tests/hello.red" ]]; then
    echo "==> Compiler smoke: red.r tests/hello.red"
    run_suite red-hello red.r tests/hello.red
    hello_rc=$(cat "$OUT/red-hello.exit" 2>/dev/null || echo missing)
    if [[ "$hello_rc" != "0" ]]; then
      echo "WARNING: red-hello compiler smoke rc=$hello_rc" >&2
    else
      echo "==> red-hello compiler smoke completed with exit 0"
    fi
    if [[ $PHASE == hello ]]; then
      exit_from_suite red-hello
    fi
  elif [[ $PHASE == hello ]]; then
    echo "ERROR: tests/hello.red is missing" >&2
    exit 2
  fi
fi

if [[ $PHASE == all || $PHASE == red ]]; then
  run_suite red tests/run-all.r --batch
  if [[ $PHASE == red ]]; then
    exit_from_suite red
  fi
fi

if [[ $PHASE == all || $PHASE == red-system ]]; then
  run_suite red-system system/tests/run-all.r --batch
  if [[ $PHASE == red-system ]]; then
    exit_from_suite red-system
  fi
fi

CURRENT_SUITE=""
END=$(iso_now)
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


def load_execution(name):
    path = out / f"{name}.execution.json"
    if path.exists():
        return json.loads(path.read_text())
    return {"suite": name, "state": "NOT_STARTED", "exit_code": None}


identity = parse_file(out / "rebol-identity.stdout.log")
identity_exec = load_execution("rebol-identity")
identity["name"] = "rebol-identity"
identity["execution"] = identity_exec
identity["identity_ok"] = bool(re.search(r"rebol-identity-ok", (out / "rebol-identity.stdout.log").read_text(errors="replace") if (out / "rebol-identity.stdout.log").exists() else ""))

suites = []
for name, qlog_name in (("red", "red.quick-test.log"), ("red-system", "red-system.quick-test.log")):
    parsed = parse_file(out / f"{name}.stdout.log")
    parsed["name"] = name
    parsed["execution"] = load_execution(name)
    qlog = out / qlog_name
    parsed["quick_test_log"] = str(qlog) if qlog.exists() else None
    if qlog.exists():
        q = parse_file(qlog)
        for key in ("assertions", "passed", "failed"):
            if parsed[key] is None:
                parsed[key] = q[key]
        parsed["failure_marker"] = parsed["failure_marker"] or q["failure_marker"]
    suites.append(parsed)

completed = all(
    s["execution"].get("state") in ("COMPLETED", "FAILED") and s["exit_code"] is not None
    for s in suites
)
functional_pass = all(
    s["exit_code"] == 0 and not s["failure_marker"] and (s["failed"] in (None, 0))
    for s in suites
)
identity_ok = identity["exit_code"] == 0 and identity.get("identity_ok")
if not completed:
    overall_state = "INCOMPLETE"
elif functional_pass:
    overall_state = "COMPLETED"
else:
    overall_state = "FAILED"

result = {
    "repository_commit": commit,
    "image": image,
    "rebol": rebol,
    "platform": "linux/386",
    "started": started,
    "finished": finished,
    "identity": identity,
    "hello": load_execution("red-hello"),
    "suites": suites,
    "identity_ok": bool(identity_ok),
    "execution_complete": completed,
    "overall_state": overall_state,
    "overall_pass": bool(completed and functional_pass),
}
(out / "summary.json").write_text(json.dumps(result, indent=2) + "\n")

lines = [
    "# Container Test Report", "",
    f"- Commit: `{commit}`",
    f"- Image: `{image}`",
    f"- Platform: `{result['platform']}`",
    f"- Started: `{started}`",
    f"- Finished: `{finished}`",
    f"- Overall state: `{overall_state}`",
    "",
    "| Suite | State | Exit | Assertions | Passed | Failed | Failure marker |",
    "|---|---|---:|---:|---:|---:|---|",
]
if (out / "rebol-identity.exit").exists():
    lines.append(
        f"| Rebol identity | {identity_exec.get('state')} | {identity['exit_code']} |  |  |  | {identity.get('identity_ok')} |"
    )
for s, label in zip(suites, ["Red", "Red/System"]):
    lines.append(
        f"| {label} | {s['execution'].get('state')} | {s['exit_code']} | {s['assertions']} | {s['passed']} | {s['failed']} | {s['failure_marker']} |"
    )
lines += [
    "",
    f"**Execution complete:** {'YES' if result['execution_complete'] else 'NO'}",
    f"**Overall result:** {'PASS' if result['overall_pass'] else overall_state}",
    "",
    "PASS means both Red suites completed with exit 0 and no failure markers.",
    "INCOMPLETE / TIMED_OUT / CANCELLED are execution states, not Red test verdicts.",
    "",
]
(out / "summary.md").write_text("\n".join(lines))
print(json.dumps(result, indent=2))
raise SystemExit(0 if result["overall_pass"] else 1)
PY
