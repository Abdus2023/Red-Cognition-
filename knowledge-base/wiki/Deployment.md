# Deployment

> Provenance: Corpus message #2, sub-messages [1], [2], [4], [18].

## Ultra-Lightweight Toolchain (sub-message [1])

The entire compiler, linker, interpreter, and runtime library are packed into a single **1 MB executable** with zero installation required.

## No Dependencies (sub-message [1])

Compiles directly into small, standalone native executables with no external runtimes required.

## Cross-Compilation (sub-message [1])

You can build binaries for Windows, Linux, macOS, Android, and ARM devices from any host OS instantly.

## Tiny Runtime Deployment Targets (sub-message [2])

The complete compiler/interpreter is around **1 MB**, making it suitable for:

- embedded devices
- Raspberry Pi
- Android
- IoT
- offline AI agents

instead of requiring hundreds of megabytes of runtime dependencies.

Small standalone binaries are attractive for deploying local, offline agents ([4]).

## Local First (sub-message [18], agent system prompt)

Assume cognition should execute locally whenever possible. Optimise for:

- offline execution
- embedded systems
- Raspberry Pi
- Android
- edge devices

Remote models are optional accelerators—not requirements.

## Model Deployment Tiers (sub-message [6])

Small Local Model → Medium Local Model → Large Remote Model (**SN-036**, embedded in [Components](Components.md)); selection criteria: task complexity, latency requirements, privacy constraints, energy consumption, financial cost.

## Related pages

[Overview](Overview.md) · [Design Decisions](Design-Decisions.md)

---

## Message #3 additions — Release model & conformance (RC-000)

### Release Model (RC-000 §6.4; proposed [26] §7: "Borrow from Rust and LLVM")

**Nightly → Experimental → Beta → Stable → LTS** — "especially valuable for experimental cognitive features" ([26]).

### Conformance Levels (RC-000 §6.5; [26] §8)

Level 0 Red/System · Level 1 Core Red · Level 2 Standard Library · Level 3 Cognitive Runtime · Level 4 Multi-Agent Runtime · Level 5 Distributed Cognitive Platform. "This enables lightweight embedded implementations while still defining a common standard" ([26]).

### Conformance Reporting (RC-000 §12; [30]; [40] Rec. 3 YAML profile example)

Every implementation claiming conformance must publish: supported specification version · conformance level · implemented RFCs · known deviations · enabled experimental features.

### Local-first reinforced

Non-Goals (RC-000 §2.2): the project does **not** aim to depend on cloud services or require large language models for execution. Cognitive Neutrality Principle (RC-100 v1.1 §16) prevents provider lock-in: see [Architecture](Architecture.md).
