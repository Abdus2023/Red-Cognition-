Red [
    Title: "Red/Cognition — Memory Substrate (RFC-0003/0004/0007 scaffold)"
    Version: 0.1.0
    RFCs: "RFC-0003 §3.5 (CoALA 4-store), RFC-0004 §3.4/3.9 (Graphiti bi-temporal + GC), RFC-0007 §3.3 (heap allocator), RFC-0004 §3.6 + RFC-0020 (UQ)"
]

; RFC-0003 §3.5 — CoALA 4 parallel stores (Tulving/Baddeley/Squire), not vertical stack
; RFC-0004 §3.4 — Graphiti bi-temporal: every edge carries when-occurred + when-ingested + validity window

cog/memory: make object! [
    working: copy []    ; bounded by context window — session scoped, in-context scratchpad (LTM router stays in-window)
    episodic: copy []   ; indexed by embedding — past interactions, experiences (Generative Agents importance)
    semantic: copy []   ; context-independent — stable facts, world model (durable facts per Mem0)
    procedural: copy [] ; compiled expertise — skills/workflows, performance history
    router-log: copy [] ; query router decisions: semantic vs graph dispatch (hybrid benchmark)
]

; RFC-0007 §3.3 — allocate(entity) → {classify, confidence, provenance, validity, route, lifecycle}
cog/memory-allocate: function [
    entity [object!] "must have type: belief!/hypothesis!/memory! etc. (see types.red)"
    /confidence c [float!] "overrides entity/confidence"
    /provenance chain [block!] "Sensor→Observation→Reasoning→Decision→Action"
    /valid from [date! none!] to [date! none!]
][
    type: entity/type
    conf: any [c entity/confidence 1.0]
    store: case [
        find [working!] type  ['working]
        find [episodic! memory!] type ['episodic]  ; memory! defaults to episodic pending promotion
        find [semantic! belief! hypothesis! evidence!] type ['semantic]
        find [procedural! skill!] type ['procedural]
        true ['working] ; fallback — working memory scratchpad
    ]
    ; Route to store per hybrid router (see RFC-0004 §3.4 — factual relational → graph, semantic → vector, in-window stays)
    entry: make object! [
        id: #a1b2  ; mock HMAC (RFC-0007 COMMIT)
        type: type
        content: entity/content
        confidence: conf
        provenance: any [chain copy [source: 'reconstruction]]
        valid-from: from
        valid-to: to
        store: store
    ]
    append get in cog/memory store entry
    append cog/memory/router-log reduce [type "→" store mold now]
    print rejoin ["[memory-allocate] " mold type " → " store " (confidence " conf ") — Graphiti bi-temporal edge valid " mold reduce [from to]]
    entry
]

; RFC-0003 §3.5 + RFC-0004 §3.9 — Memory Promotion Gate + Reflection→(Episodic/Semantic/Procedural/Discard)
; Mem0 hierarchy: summaries stay episodic, durable facts promoted to semantic, compiled workflows to procedural
cog/memory-promote: function [entry [object!] target [word!] "episodic | semantic | procedural | discard"][
    print rejoin ["[memory-promote] #" entry/id " " mold entry/type " → " target]
    if target = 'discard [print "  → discard (noise, no long-term value)"]; return none
    ; Mock move: remove from current store, append to target
    foreach store [working episodic semantic procedural][
        if entry = find get in cog/memory store entry [remove find get in cog/memory store entry]
    ]
    append get in cog/memory target entry
    entry
]

; RFC-0004 §3.9 + RFC-0007 §3.5 — Reflection-as-GC: Working Memory → Relevant? → Keep / Compress→Summarise→Archive→Forget
; + RFC-0018 verified FORGET: must attest graph+vector+adapter purge (mock here)
cog/memory-gc: function [/compress episodic-end [date!] /forget stale-threshold [date!]][
    print "[memory-gc] Working Memory → Relevant? → Keep / Compress→Summarise→Archive→Forget (RFC-0007)"
    if compress [
        print rejoin ["  → compress episodic before " episodic-end " → Summarise → Archive (mock)"]
    ]
    if forget [
        print rejoin ["  → forget stale entries before " stale-threshold " — verified deletion audit (RFC-0018)"]
    ]
]

; RFC-0004 §3.5 invalidation — invalidate-goal (cache-coherence analog)
cog/invalidate-memory: function [id [word! issue!] reason [block!]][
    print rejoin ["[invalidate-memory] " id " — world-state changed: " mold reason " (MESI Invalid, see RFC-0016)"]
]

print "[cog/memory] loaded 4-store + allocate→route + promotion gate + GC — try: cog/memory-allocate cog/make-belief {OpenClaw is Rust} 0.95 'observation"
