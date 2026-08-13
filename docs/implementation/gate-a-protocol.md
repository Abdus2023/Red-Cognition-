# Gate A — External Toolchain Activation Protocol

**Status:** Awaiting external input. Not a pipeline-development phase.
**Activation:** An authorized Rebol 2.7.8 executable must be placed in the workspace.

## Gate state machine

```
TOOLCHAIN_ABSENT
       │
       │ executable discovered
       ▼
TOOLCHAIN_PRESENT
       │
       │ version probe
       ▼
VERSION_VERIFIED
       │
       │ compatibility probe
       ▼
COMPATIBILITY_VERIFIED
       │
       │ authority confirmed
       ▼
TOOLCHAIN_AUTHORIZED
       │
       ▼
READY (RED-LEX-001)
```

Any failure → specific blocking state (not generic BLOCKED):

| Failure point | Blocking state |
|---|---|
| No executable found | BLOCKED_TOOLCHAIN_ABSENT |
| Version mismatch | BLOCKED_VERSION_MISMATCH |
| Architecture incompatible | BLOCKED_ARCH_INCOMPATIBLE |
| Not authorized | BLOCKED_AUTHORIZATION_REQUIRED |
| Execution failure | BLOCKED_EXECUTION_FAILURE |

## Gate A verifies four things

### 1. Executable existence
Not merely a file named `rebol`. It must actually execute (`rebol --version` or equivalent).

### 2. Version identity
The observed executable must report the expected Rebol version (2.7.8 or authorized equivalent).

### 3. Architecture compatibility
The controller must determine whether the executable can run on the current host:
- host architecture (x86_64)
- OS kernel
- binary format (ELF)
- 32-bit compatibility (libc6-i386, ld-linux.so.2)
- dynamic-loader requirements

### 4. Authorization
```
exists ≠ executable ≠ compatible ≠ authorized
```
Only ALL FOUR → READY.

## Execution sequence after Gate A opens

```
Gate A opens (toolchain authorized)
       │
       ▼
RED-LEX-001 (lexer baseline, unchanged)
       │
       ▼
OBSERVED RESULT (stdout, stderr, exit status)
       │
       ▼
EVIDENCE (hash-chained, provenance-bound)
       │
       ▼
PASS / FAIL / BLOCKED
       │
       ▼ (if PASS)
LIBRED-001 (depends on RED-LEX-001)
       │
       ▼
runtime validation
       │
       ▼
first source-backed implementation
       │
       ▼
first Cognition task
       │
       ▼
broader backlog execution (incremental, NOT batch)
```

## Critical principles

1. **Don't automatically execute all 74 tasks.** The first run establishes the execution substrate. Then proceed incrementally.

2. **The first execution proves the execution boundary** before attempting substantive implementation:
   ```
   environment → Rebol → Red → lexical execution → observable result → evidence
   ```

3. **Evidence becomes the next architectural product.** Until now: static evidence (requirements, inventories, matrices). Gate A introduces the first runtime evidence:
   ```
   EVD-RED-LEX-001
   ├── task_id
   ├── requirement_ids
   ├── toolchain_identity
   ├── executable_hash
   ├── host_identity
   ├── command
   ├── exit_code
   ├── stdout
   ├── stderr
   ├── timestamp
   ├── environment
   ├── observed_state
   └── verdict
   ```

4. **The controller will not transition BLOCKED → READY** until the executable prerequisite is observed. No state change without observed authority.

## What this protocol does NOT do

- Does not relax the Rebol 2.7.8 requirement
- Does not substitute R3 for R2
- Does not install 32-bit compatibility without authorization
- Does not use unofficial binaries
- Does not create placeholder PASS evidence
- Does not change BLOCKED → READY manually

## Relationship to frozen stages

Gate A is an **external activation boundary** applied to the frozen controller.
It does not modify Stage 4 or Stage 5 internals. It provides the external input
that the frozen controller was designed to consume.

```
FROZEN ARCHITECTURE
       │
EXTERNAL GATE (Gate A)
       │
FROZEN CONTROLLER OBSERVES → TRANSITIONS → EXECUTES → EVIDENCES
```
