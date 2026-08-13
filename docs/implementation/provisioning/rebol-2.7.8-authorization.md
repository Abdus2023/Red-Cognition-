# Rebol 2.7.8 — Authorized Toolchain Metadata (Gate A)

**Purpose:** Provide provenance-backed metadata so Gate A can transition from BLOCKED_TOOLCHAIN_ABSENT to READY per docs/implementation/gate-a-protocol.md. This file records artifact identity, provenance, authorization, and verification steps — it does NOT vendor the binary itself unless repository policy explicitly allows binary artifacts.

**Status:** PLACEHOLDER — awaiting authorized artifact and real SHA-256. No hash is fabricated.

## Artifact identity (to be filled by Provisioning Council)

```yaml
artifact: rebol-2.7.8.bin
artifact_url: https://example.org/releases/rebol-2.7.8.bin  # MUST be faithful binary-transfer channel, not markdown-escaped
platform: i386  # official Linux artifacts are i386 (ELF 32-bit, /lib/ld-linux.so.2) ; use x86_64 only if approved 64-bit build exists and is ratified
expected_lib: /lib/ld-linux.so.2  # requires libc6-i386 on Debian or equivalent; or qemu-i386+binsfm shim if authorized
size_bytes: <TO_BE_FILLED>  # e.g., 1234567 — from ls -l
sha256: <TO_BE_FILLED_WITH_REAL_SHA256>  # computed via: sha256sum rebol-2.7.8.bin
sha256_command: sha256sum rebol-2.7.8.bin
```

## Provenance (to be filled)

```yaml
provenance:
  provider: <TO_BE_FILLED>  # e.g., AcmeCorp CI, Red-lang.org official
  delivery: <TO_BE_FILLED>  # e.g., signed-release + GitHub release URL, or container image pre-placement
  gpg_signature_url: <OPTIONAL>  # e.g., https://example.org/releases/rebol-2.7.8.bin.asc
  release_notes_url: <OPTIONAL>
  ci_job_url: <OPTIONAL>  # link to CI that produced/hosted artifact
```

## Authorization (required, explicit)

```yaml
authorized_by:
  name: <TO_BE_FILLED>  # e.g., "Project Provisioning Council"
  role: <TO_BE_FILLED>  # e.g., "Approver" / "Maintainer"
  date: <TO_BE_FILLED ISO-8601>  # e.g., 2026-08-14
authorization_evidence_url: <TO_BE_FILLED>  # PR, issue, meeting minutes, signed document
allowed_use:
  - pipeline execution only when --allow-tool rebol-278 is provided
  - no redistribution beyond CI workspace unless approved
```

## Compatibility / host requirements

- Official Rebol 2.7.8 Linux artifacts: ELF 32-bit x86, interpreter /lib/ld-linux.so.2, GLIBC_2.0/2.1 per IMPLEMENTATION-BASELINE.md §G.2
- Host check (current sandbox):
  - uname -m = x86_64
  - /lib/ld-linux.so.2 absent — requires libc6-i386 or equivalent, or qemu-i386 + binfmt_misc shim, each requiring explicit authorization
  - file rebol-2.7.8.bin should report: ELF 32-bit LSB executable, Intel 80386, interpreter /lib/ld-linux.so.2
  - ldd rebol-2.7.8.bin should succeed after compat libs installed
- If approved 64-bit build exists: file should report ELF 64-bit, no 32-bit compat needed, but must be recorded as approved 64-bit substitute with ratification reference.

## Verification commands (to be executed after artifact + compat present)

```bash
# 1. Hash verification (ground truth)
sha256sum rebol-2.7.8.bin
# compare to sha256 field above

# 2. File type / loader
file rebol-2.7.8.bin
ls -l /lib/ld-linux.so.2 || echo "32-bit loader absent — needs authorization to install"

# 3. Executable probe
chmod +x rebol-2.7.8.bin
./rebol-2.7.8.bin -qws -c "print system/version"

# 4. Controller ground-truth check (must be on PATH as 'rebol')
sudo cp rebol-2.7.8.bin /usr/bin/rebol || cp rebol-2.7.8.bin ./rebol
which rebol
python3 -c "import shutil; print(shutil.which('rebol'))"

# 5. Pipeline dry-run (should move RED-LEX-001 from BLOCKED to READY if all blockers satisfied)
python3 tools/run-implementation-pipeline.py --dry-run | python3 -m json.tool | grep -A5 '"task_id": "RED-LEX-001"'

# 6. Pipeline execute (only after dry-run shows READY, with explicit allow-tool)
python3 tools/run-implementation-pipeline.py --execute --allow-tool rebol-278

# 7. Expected lexical test (first source-backed implementation frontier)
./rebol -qws tests/source/compiler/lexer-test.r
# capture stdout/stderr -> evidence EVD-RED-LEX-001, hash-chained, provenance-bound
```

## What this file does NOT do (governance guardrails)

- Does NOT vendor the binary itself (only metadata + URL) unless repo policy explicitly allows binary artifacts and size is justified
- Does NOT contain fabricated SHA-256 — placeholder <TO_BE_FILLED> must be replaced with real hash computed from faithful artifact
- Does NOT substitute R3, r3-make, or Red binary for Rebol 2.7.8 (would violate toolchain discipline §10)
- Does NOT set tool_registry available true without executable on PATH — controller checks ground truth via shutil.which (see engine.py KNOWN_TOOL_BINARIES)
- Does NOT bypass 32-bit compatibility requirement — host compat must be authorized and documented

## Traceability

```
Requirement: README-L185-205 (Running Red from sources), build/build.r-L50 (system/version = 2.7.8.3.1)
    ↓
RFC / Authority: docs/IMPLEMENTATION-BASELINE.md §A,§G.1-G.6, docs/implementation/gate-a-protocol.md, .travis.yml (static.red-lang.org/tmp/rebol)
    ↓
Implementation Task: RED-LEX-001 (lexer baseline, UNCHANGED)
    ↓
Toolchain: rebol-278 (this metadata provides provenance + authorization)
    ↓
Evidence: EVD-RED-LEX-001 to be produced after Gate A READY
```

## Checklist for PR that adds this file

- [ ] Artifact URL is faithful binary-transfer (curl/wget succeeds with identical bytes)
- [ ] SHA-256 computed and pasted, size recorded
- [ ] Provenance (provider, delivery, optional GPG sig) filled
- [ ] Authorization (name, role, date, evidence URL) filled and linked to PR/issue
- [ ] Host compat instructions (libc6-i386 or qemu) documented and authorized
- [ ] Verification commands executed and logs attached to PR
- [ ] IMPLEMENTATION-BASELINE.md updated with authorized entry if required by governance
- [ ] Pipeline dry-run shows RED-LEX-001 READY (or BLOCKED only by remaining declared blockers if any)
- [ ] No binary added unless policy allows, no fabricated hash

## Notes from last execution (so far)

- Branch actual: arena/019ffaed-red-cognition @ af3fe44, requested arena/019ffad2 not found — discrepancy documented
- Gate A: BLOCKED_TOOLCHAIN_ABSENT with sub-blockers TOOLCHAIN, ARCHITECTURE, PROVISIONING, AUTHORIZATION
- Probes 2026-08-13: rebol absent, /lib/ld-linux.so.2 absent, curl 52/35 egress-filtered, Python socket empty/EOF, GitHub API 200 but no approved artifact
- Controller self-test 390/390 PASS (governance only), frontier PAUSED READY 0 BLOCKED 4, evidence integrity intact true records 0
- RFC-0075 independent blocker: 4 conflicts (lifecycle 8 vs 5 stages, KnowledgeExchange vs KnowledgeExchangeObject, 5 vs 3 profiles, parent title/terminology) + 4 critical gaps (schemas/wire, lifecycle guards, crypto/trust, replay boundary) — requires separate ratification patch, not coding
