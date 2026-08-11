# Overview

> Provenance: Corpus message #2 (2026-08-10), sub-messages [1], [2], [10], [16], [18]. Verbatim: [`sources/message-002-original-part1.md`](../sources/message-002-original-part1.md), [`…-part2.md`](../sources/message-002-original-part2.md). All items are proposals/descriptions from the corpus; nothing verified against an implementation unless noted.

## What is Red (sub-message [1])

**Red** is a next-generation, multi-paradigm programming language strongly inspired by **Rebol**. It is uniquely designed to be a "full-stack" language, meaning it can handle everything from high-level scripting down to low-level systems programming. (Stated twice in [1]; citations: see [References](References.md) R1–R4.)

## Core Features (sub-message [1])

- **Homoiconic** — Red treats code as data and data as code, which makes advanced metaprogramming very easy.
- **Ultra-Lightweight Toolchain** — The entire compiler, linker, interpreter, and runtime library are packed into a single **1 MB executable** with zero installation required.
- **Built-in Dialects (DSLs)** — Red uses Domain-Specific Languages to drastically simplify complex coding tasks:
  - **Red/System**: A C-level, low-level system programming layer.
  - **Parse**: A powerful Parsing Expression Grammar (PEG) engine.
  - **VID & Draw**: Dialects for rapid native GUI layout and 2D vector drawing.
- **No Dependencies** — Compiles directly into small, standalone native executables with no external runtimes required.
- **Cross-Compilation** — You can build binaries for Windows, Linux, macOS, Android, and ARM devices from any host OS instantly.

## Architecture Overview — Two Execution Tiers (sub-message [1])

Red splits its execution model into two distinct tiers to bridge the gap between abstract software and hardware (source cited in [1]: IEEE paper, see [References](References.md) R11):

| Language Layer | Execution Level | Use Cases | Performance |
|---|---|---|---|
| **Red** | High-level (Interpreted/JIT) | Scripting, GUI apps, data processing | Flexible & Dynamic |
| **Red/System** | Low-level (Compiled) | OS kernels, device drivers, inline performance | Near-C Speed |

## Basic Syntax Example (sub-message [1])

Red syntax is highly human-readable and doesn't require boilerplate code. Here is how you declare a variable and build a graphical window with a button:

**SN-001** (language tag as given: `rebol`). ⚠ Received flattened onto one line; preserved unchanged — see [Code Snippets](Code-Snippets.md).

```
Red [Title: "Simple Example"]  ; Declaring a variable (types are inferred) message: "Hello from Red!"  ; Creating a native GUI window using the VID dialect view [     title "My App"     text message     button "Click Me" [print "Button was clicked!"] ]
```

*(Source artifact included the caution line: "Use code with caution.")*

## Current Status (sub-message [1])

Red is developed by a core team led by Nenad Rakočević. Stable releases and continuous optimization (such as adding atomic operation intrinsics) can be tracked on the official Red GitHub Repository. While highly innovative for rapid GUI prototyping and custom DSLs, its mainstream ecosystem remains relatively niche.

## The Three-Layer Red Vision (sub-message [10])

One way to unify the language is as follows:

| Layer | Purpose | Primary Abstraction |
|--------|---------|---------------------|
| **Red/System** | Hardware and systems programming | Machine resources |
| **Red** | General programming and DSLs | Computation |
| **Red/Cognition** | Autonomous agents and AI | Intent, memory, reasoning, and goals |

This mirrors Red's original "full-stack" philosophy: **downward** to hardware through Red/System and **upward** to cognition through a new cognitive layer.

If realised, such an evolution would make Red more than a scripting or systems language. It would become a language whose native abstractions are not only variables and functions, but also **goals, memories, capabilities, plans, reflection, and autonomous behaviour**—providing a foundation for long-lived, agent-oriented systems.

## Positioning of Red/Cognition (sub-messages [10], [14], [16])

- Refactoring **Red** into a true **Cognitive Language** would mean changing its primary abstraction. Today, Red is a language for describing **computations**. A cognitive version of Red would be a language for describing **intent, reasoning, memory, and action**. ([10])
- Rather than replacing Red, think of it as adding a new, higher layer—just as **Red/System** extends downward toward hardware, a **Red/Cognition** layer would extend upward toward autonomous intelligence. ([10])
- Red's original slogan: **"One language from system programming to scripting."** A cognitive evolution could extend it to: **"One language from hardware to intelligence."** ([16])
- **Red/Cognition** is not simply an AI library or a new syntax. It is a proposal to elevate **intent, knowledge, reasoning, and autonomous behaviour** to the same level of importance that variables, functions, and objects occupy in conventional programming languages. The compiler, runtime, and language evolve together so that the fundamental unit of programming shifts from *instructions* to *goals*, from *algorithms* to *cognitive workflows*, and from *execution* to *verified intelligent behaviour*. ([16])
- Red would not merely be a language that compiles to native code, but a language that compiles **intent** into **verified cognitive execution**. Computation remains the foundation, but the primary abstraction becomes **goal-directed behaviour**, supported by native concepts such as memory, planning, reflection, uncertainty, provenance, and capabilities. Such an evolution would preserve Red's minimalist, dialect-oriented design while extending it into a platform for long-lived, trustworthy autonomous agents. ([14])
- This preserves Red's original philosophy of being a **full-stack language**, but extends the stack upward into **cognitive computing**, making intelligence itself a first-class compilation target rather than something implemented as a library on top of the language. ([12] — see [Architecture](Architecture.md))

## Why Red Fits Agent Runtimes (sub-messages [2], [4])

Red already provides several primitives that map naturally onto an agent runtime ([2]):

1. **Homoiconicity → Reasoning** — Because **code is data**, an agent can inspect, rewrite, generate, and execute programs using the same data structures. This is much simpler than manipulating source code strings in languages like C or Java. (Flow: **SN-007**, [Code Snippets](Code-Snippets.md))
2. **Dialects → AI Skills** — Red's dialect system is essentially a built-in DSL framework. Instead of writing parsers, an AI can emit a Red dialect. Example dialects listed: Filesystem, HTTP, GUI, Robotics, SQL, Workflow. This is very similar to modern tool-calling. (Flow: **SN-008**)
3. **Tiny Runtime** — The complete compiler/interpreter is around **1 MB**, suitable for: embedded devices, Raspberry Pi, Android, IoT, offline AI agents — instead of requiring hundreds of megabytes of runtime dependencies. (See also [Deployment](Deployment.md))
4. **Red/System → Hardware Layer** — An agent eventually reaches the physical world. Unlike Python, Red already includes a systems programming layer. (Stack: **SN-009**)

Red provides several language features that fit naturally into this architecture ([4]):

- **Blocks** are ideal for representing plans and workflows.
- **Homoiconicity** allows an agent to inspect and transform its own reasoning structures.
- **Dialects (DSLs)** make it easy to define specialised languages for planning, permissions, workflows, or robotics.
- **Red/System** provides a path to efficient, low-level execution without leaving the language ecosystem.
- **Small standalone binaries** are attractive for deploying local, offline agents.

Because a plan is a data structure, it can be analysed, modified, optimised, or executed by the runtime itself. (Example: **SN-022**)

Red's block-based syntax and dialect mechanism make it well suited for expressing cognitive workflows; a workflow is not just executable code—it is also a readable representation of intent. Because Red is homoiconic, the runtime can inspect, transform, optimise, or even synthesise these workflows before executing them. ([6]; example: **SN-037**)

## Related pages

[Architecture](Architecture.md) · [Workflows](Workflows.md) · [Design Decisions](Design-Decisions.md) · [Specifications](Specifications.md) · [References](References.md)
