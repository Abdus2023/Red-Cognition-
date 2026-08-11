# APIs

> Provenance: Corpus message #2, sub-messages [4], [6], [14], [16], [18]. Snippet IDs link to [Code Snippets](Code-Snippets.md). All interfaces are proposals from the corpus.

## System Primitives — Unix vs Cognitive OS (sub-messages [4], [6])

A Unix shell manages **processes**; an agent runtime manages **thoughts** ([4]). Unix introduced powerful primitives; a Cognitive OS would introduce different primitives, which become first-class runtime operations ([6]).

**SN-015** — Unix shell process management ([4]):

```
fork()
exec()
wait()
exit()
```

**SN-016** — Agent runtime thought management ([4]):

```
observe()
reason()
plan()
execute()
reflect()
remember()
```

**SN-027** — Unix primitives ([6]):

```text
fork()
exec()
pipe()
signal()
wait()
open()
close()
```

**SN-028** — Cognitive OS primitives ([6]):

```text
observe()
infer()
reason()
plan()
delegate()
remember()
forget()
verify()
reflect()
sleep()
wake()
```

## Unix Runtime → Agent Runtime Concept Mapping (sub-message [4])

| Unix Runtime | Agent Runtime |
|--------------|---------------|
| Process | Task |
| PID | Goal ID |
| File | Knowledge |
| Environment Variables | Working Memory |
| Process Tree | Reasoning Tree |
| Scheduler | Planner |
| Signals | Events |
| Exit Code | Confidence / Verification |

## A Universal Cognitive ABI (sub-message [16])

Just as operating systems define an Application Binary Interface (ABI), a Cognitive Runtime could define a **Cognitive ABI**. Every component would expose common interfaces such as:

**SN-121**

```text
Observe()
Reason()
Plan()
Execute()
Verify()
Reflect()
Learn()
Checkpoint()
Restore()
```

Any reasoning engine, memory backend, or AI model implementing this ABI could plug into the runtime without changing user code.

## A Cognitive Instruction Set Architecture (CISA) (sub-message [14])

Just as CPUs expose an ISA, a Cognitive VM could expose a **Cognitive ISA**. These are architecture-independent semantic operations that different runtimes could implement.

**SN-088**

```text
Memory Instructions
-------------------
OBSERVE
REMEMBER
RECALL
FORGET
SUMMARISE

Reasoning Instructions
----------------------
COMPARE
CLASSIFY
INFER
EXPLAIN
ESTIMATE

Planning Instructions
---------------------
PLAN
SCHEDULE
DELEGATE
CANCEL

Execution Instructions
----------------------
EXECUTE
VERIFY
ROLLBACK
COMMIT

Learning Instructions
---------------------
REFLECT
LEARN
UPDATE
```

Traditional VM opcodes for comparison:

**SN-086**

```text
LOAD
STORE
CALL
RETURN
JUMP
ADD
SUB
```

Semantic opcodes of the CVM (**SN-087**, embedded in [Components](Components.md)): OBSERVE, RECALL, INFER, PLAN, SELECT, EXECUTE, VERIFY, REFLECT, LEARN.

## The Cognitive Register File (sub-message [14])

CPUs have registers:

**SN-089**

```text
RAX
RBX
RCX
RDX
```

A Cognitive VM might instead expose logical registers. The runtime continuously updates these during execution.

**SN-090**

```text
Current Goal
Current Plan
Working Memory
Attention
Context
Confidence
Policy
Capability
```

**SN-091** — Example register contents:

```text
Goal Register
----------------
"Analyse repository"

Confidence Register
-------------------
0.82

Attention Register
------------------
Architecture module
```

## First-Class Cognitive Concepts (sub-message [18], agent system prompt)

Treat the following as language primitives rather than library constructs:

Goals · Plans · Intent · Observation · Evidence · Beliefs · Knowledge · Memory · Reflection · Policies · Capabilities · Skills · Events · Attention · Reasoning · Verification · Learning · Uncertainty · Confidence · Provenance

## Runtime Vision Loop (sub-message [18], agent system prompt)

The runtime continuously performs: Observe ↓ Understand ↓ Reason ↓ Plan ↓ Execute ↓ Verify ↓ Reflect ↓ Learn ↓ Remember ↓ Loop. This loop replaces the traditional Read–Eval–Print Loop. (Variant flows: **SN-011** in [Workflows](Workflows.md).)

## Related pages

[Components](Components.md) (CVM) · [Services](Services.md) · [Data Models](Data-Models.md) · [Workflows](Workflows.md)

---

## Message #4 additions — Interfaces & protocols (msg#4 [52]–[60])

### Dialect Compiler Protocol (DCP) (RC-300 v1.1 §8; [52] §7)

Every cognitive dialect SHOULD provide: Parser · Validator · Lowering Rules · Type Rules · Effect Rules · Metadata Generator. Flow ([54]): Dialect → Parser → Validator → Lowering → IR → Runtime.

### Compiler Version Contract (recommended, [54] Amendment B)

Every compiler implementation MUST publish: compiler version · supported RC-300 version · supported RC-200 language version · supported dialects · backend targets · determinism level · known deviations.

### Cognitive Runtime Interface Contract (recommended, [58])

CognitiveRuntimeAPI: execute-cycle() · store-memory() · retrieve-memory() · request-capability() · emit-trace() · create-checkpoint() · restore-checkpoint().

### Runtime Event Contract (recommended, [56])

Event { id, timestamp, source, capability-context, payload, provenance } — every event MUST contain these fields (RFC-0008 proposed).

### Shell Command Boundary (recommended, [60])

Human Command → Shell Parser → Intent Request → Cognitive Runtime → Trace Result.
