# XX. Concurrency Infrastructure — Threading and MPMC Queue

```ascii
┌──────────────────────────────────────────────────────────────────────┐
│            RED CONCURRENCY ARCHITECTURE (Current + Planned)          │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  CURRENT (v0.6.6):                                                   │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │  Red Runtime Threading Library                             │     │
│  │  ┌─────────────────┐  ┌─────────────────────────────────┐ │     │
│  │  │ Thread Primitives│  │ MPMC Queue (FIFO)               │ │     │
│  │  │                  │  │                                 │ │     │
│  │  │ thread-create    │  │ Multiple producers can push     │ │     │
│  │  │ thread-wait      │  │ Multiple consumers can pop      │ │     │
│  │  │ thread-terminate │  │ Lock-free / wait-free design    │ │     │
│  │  │ mutex-create     │  │ Used for async IO messaging     │ │     │
│  │  │ mutex-lock       │  │                                 │ │     │
│  │  │ mutex-unlock     │  │                                 │ │     │
│  │  │ semaphore ops    │  │                                 │ │     │
│  │  └─────────────────┘  └─────────────────────────────────┘ │     │
│  └────────────────────────────────────────────────────────────┘     │
│                                                                      │
│  PLANNED (v0.7.0):                                                   │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │  Full Async IO (Port system)                               │     │
│  │                                                            │     │
│  │  ┌──────────────────────────────────────────────────────┐ │     │
│  │  │           ASYNC IO ARCHITECTURE                       │ │     │
│  │  │                                                       │ │     │
│  │  │  port! datatype (already exists, async extension)    │ │     │
│  │  │                                                       │ │     │
│  │  │  Scheme handlers:                                     │ │     │
│  │  │    file://  → async file IO                          │ │     │
│  │  │    http://  → async HTTP with callbacks              │ │     │
│  │  │    tcp://   → async TCP socket                       │ │     │
│  │  │    dns://   → async DNS resolution                   │ │     │
│  │  │    event:// → timer and event port                   │ │     │
│  │  │                                                       │ │     │
│  │  │  await-style programming via port actors:             │ │     │
│  │  │    p: open tcp://localhost:8080                       │ │     │
│  │  │    write p "GET / HTTP/1.1^/"                         │ │     │
│  │  │    data: read p                                       │ │     │
│  │  └──────────────────────────────────────────────────────┘ │     │
│  └────────────────────────────────────────────────────────────┘     │
│                                                                      │
│  COGNITIVE CONCURRENCY MODEL (Proposed for Red/Cognition):           │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │                                                            │     │
│  │  Goal A (high priority)                                    │     │
│  │      │                                                     │     │
│  │  Goal B (background)    ← all goals in cooperative        │     │
│  │      │                    multitasking — yield at         │     │
│  │  Goal C (event-driven)    defined cognitive checkpoints   │     │
│  │      │                                                     │     │
│  │  MPMC Queue  ← events, messages, observations             │     │
│  │      │                                                     │     │
│  │  Agent Scheduler ← priority + dependency + budget aware   │     │
│  │                                                            │     │
│  └────────────────────────────────────────────────────────────┘     │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```