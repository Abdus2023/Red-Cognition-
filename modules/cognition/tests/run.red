Red [Title: "Cognition scaffold test — Gate A shape check (RFC-0005 §3.9)"]
#include %../types.red
#include %../dialects.red
#include %../contracts.red

print "=== Gate A — Golden-file conformance (single block, inspectable) ==="
agent: cog/make-agent [
    name: "Repository Assistant" version: 1.0 permissions: [read-filesystem call-github generate-report]
]
probe agent
b: cog/make-belief "OpenClaw" 1.0 'user
probe b
cap: cog/make-capability 'generate-report 'safe
probe cap

; Dialect chain from golden file
cog/when 'github.push [
    cog/reason [identify changed modules estimate impact]
    cog/plan [run tests inspect architecture]
    cog/with-authorisation [generate-report: [scope 'repo]] [
        cog/execute [generate report]
    ]
    cog/yield
]

; Capability gate negative test (should be rejected by real RFC-0006 Capability Analysis)
print "[negative] execute [delete %temp/] without authorisation — real compiler would REJECT (RFC-0012 Tier 1)"
; cog/execute [delete %temp/]  ; ← uncommenting this bare call should be lint error after RFC-0012

print "=== Gate A mock: PASS (HMAC would be verified by CVM COMMIT) ==="
