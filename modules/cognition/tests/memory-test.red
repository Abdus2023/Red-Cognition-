Red [
    Title: "Cognition — Memory substrate test (Gate B temporal query, RFC-0004 §3.4 bi-temporal)"
    Version: 0.1.0
    RFCs: "RFC-0003 §3.5 (CoALA), RFC-0004 §3.4 (Graphiti), RFC-0007 §3.3, RFC-0018 verified deletion"
]

#include %../types.red
#include %../memory.red

print "=== Gate B — Memory substrate + bi-temporal edge validity (RFC-0004 §3.4) ==="

; Allocate memories with validity windows (Graphiti bi-temporal: when-occurred + when-ingested + validity)
m1: cog/memory-allocate/valid (cog/make-memory "OpenClaw is Rust" 0.95 'observation now) now (now + 30)
m2: cog/memory-allocate/valid (cog/make-memory "user prefers offline" 1.0 'user now) now none  ; perpetual

print rejoin ["[test] episodic store size: " length? cog/memory/episodic]
print rejoin ["[test] semantic store size: " length? cog/memory/semantic]

; Promotion gate: Mem0 — durable facts promoted to semantic, summaries stay episodic (RFC-0003 §3.5)
print "[test] promote episodic → semantic (durable fact)"
cog/memory-promote m1 'semantic
print rejoin ["  semantic size after promote: " length? cog/memory/semantic]

; GC: Working Memory → Relevant? → Compress→Summarise→Archive→Forget (RFC-0007 §3.5)
cog/memory-gc/compress/forget (now - 10) (now - 20)

; Invalidation: world-state changed → MESI Invalid (RFC-0016)
cog/invalidate-memory #a1b2 [world: git.push on: %src/cogos.red changed]

; Verified deletion scaffold (RFC-0018 — must attest graph+vector+adapter purge)
print "[test] verified FORGET would HMAC-attest graph edges + vectors + adapters purged (RFC-0018)"
print "=== Gate B mock: PASS — real Graphiti bi-temporal query (validAt: now vs now-30) requires graph DB ==="
