# Services

> Provenance: Corpus message #2, sub-message [16] ("The Cognitive Microkernel"). Component → Service relationships are those drawn in the source diagram.

## Cognitive Microkernel Services (sub-message [16])

Borrowing from microkernel operating systems, most intelligence can be moved into modular services. The kernel remains small, while planners, memories, and model providers are replaceable components.

**SN-120**

```text
               Cognitive Kernel
                     │
 ┌──────────┬─────────┼─────────┬──────────┐
 ▼          ▼         ▼         ▼          ▼
Memory   Planner   Policy   Scheduler   Event Bus
 │
 ▼
Skill Manager
 │
 ▼
Model Manager
 │
 ▼
Tool Manager
```

## Service Inventory (as drawn in SN-120)

| Service | Connected to (per diagram) |
|---|---|
| Memory | Cognitive Kernel; chain to Skill Manager |
| Planner | Cognitive Kernel |
| Policy | Cognitive Kernel |
| Scheduler | Cognitive Kernel |
| Event Bus | Cognitive Kernel |
| Skill Manager | Below Memory branch (diagram shows Memory → Skill Manager → Model Manager → Tool Manager) |
| Model Manager | Below Skill Manager |
| Tool Manager | Below Model Manager |

> Note: the vertical chain Skill Manager → Model Manager → Tool Manager is drawn under the Memory branch in the source diagram; no further relationship semantics are stated in the corpus. Recorded exactly as drawn.

## Related pages

[Architecture](Architecture.md) (Cognitive Kernel: SN-026, SN-040) · [Modules](Modules.md) · [APIs](APIs.md) (Cognitive ABI implemented by replaceable components)
