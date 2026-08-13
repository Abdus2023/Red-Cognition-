Red [
    Title: "Red/Cognition — Lint & Capability Check (RFC-0006 Capability Analysis + RFC-0012 ergonomic proof + RFC-0013 totality)"
    Version: 0.1.0
    RFCs: "RFC-0006 §3.6, RFC-0012 Tier 1, RFC-0013 totality, RFC-0015 yield"
]

; RFC-0006 §3.6 — Policy-as-Type mock lint: dangerous capability requires with-authorisation
; RFC-0012 — with-authorisation elaborates to proof term; here welint the *absence*
; RFC-0013 — recursion without base case
; RFC-0015 — yield-required for long goals

cog/lint-dangerous: function [code [block!] /authorised "inside with-authorisation"][
    ; Very small mock lint: walks block, flags `execute [delete ...]` without authorised flag
    foreach expr code [
        if block? expr [cog/lint-dangerous/with expr authorised]
        if all [word? expr expr = 'execute not authorised][
            print ["[lint] ERROR RFC-0012 Tier 1: `execute` without `with-authorisation` — would be rejected by Capability Analysis (see RFC-0006 §3.6)"]
            return false
        ]
    ]
    true
]

cog/lint-yield: function [steps [block!]][
    if (length? steps) >= 5 [
        unless find steps 'yield [
            print "[lint] WARN RFC-0015: goal/plan with ≥5 steps must contain `yield` — cooperative scheduling (see RFC-0015 §1.2)"
            return false
        ]
    ]
    true
]

cog/lint-recursion: function [name [word!] body [block!]][
    if find body name [
        unless find body 'on-failure [
            print rejoin ["[lint] ERROR RFC-0013: recursive cognitive block `" name "` without base case / on-failure — totality violation (see RFC-0013 §1.1)"]
            return false
        ]
    ]
    true
]

print "[cog/lint] loaded — try: cog/lint-dangerous [execute [delete %temp/]]"
print "             → should ERROR;   cog/lint-dangerous/with [execute [delete %temp/]] true → mocked authorised"

; Example: Gate A golden file lint checks
example: [
    cog/reason [identify changed modules]
    cog/plan [run tests]
    execute [delete %temp/]   ; ← bare, should lint error
]

probe cog/lint-dangerous example
probe cog/lint-dangerous/with [execute [delete %temp/]] true
probe cog/lint-yield [a b c d e]           ; warn
probe cog/lint-yield [a b c d e yield]     ; pass
