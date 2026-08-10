Red [
    Title: "Red/Cognition — Types & Dialects Prototype (Phase 1 scaffold)"
    Version: 0.1.0
    RFCs: "RFC-0005 (16 types), RFC-0006 (capability analysis), RFC-0012 (ergonomic proof), RFC-0013 (totality), RFC-0014 (cognitive lock)"
    Status: "Prototype — illustrative; not normative. Run with: red prototypes/red-cognition-types.red"
    Traceability: "Implements REQ-011 (16 types) at mock level; REQ-002/015 capability-dialect shape"
]

; ----------------------------------------------------------------------
; 16-type taxonomy (RFC-0005 §3.2) — mocked as objects with metadata slots
; epistemic | intentional | temporal | normative — each carries confidence/validity/source/scope
; ----------------------------------------------------------------------
make-belief: func [content confidence source][
    ; belief! mock — see RFC-0005 §3.2
    make object! [
        type: 'belief!
        content: content
        confidence: confidence  ; 0.0..1.0 — see 4-dim UQ (RFC-0004 §3.6) for future split
        source: source         ; 'user | 'observation | 'inference
        validity: none         ; datetime interval | none = perpetual — see Graphiti bi-temporal
    ]
]

make-observation: func [source event payload][
    make object! [
        type: 'observation!
        source: source  ; 'github | 'sensor | 'filesystem | ...
        event: event
        payload: payload
    ]
]

make-capability: func [name [word!] policy [word!]][
    make object! [
        type: 'capability!
        name: name
        policy: policy ; 'safe | 'dangerous | 'trusted | 'reversible | ...
    ]
]

; ----------------------------------------------------------------------
; Dialect-embedded capability + ergonomic proof (RFC-0012: with-authorisation)
; Usage: with-authorisation [delete: [scope %temp/ expiry now + 00:30:00]] [execute [delete %temp/]]
; ----------------------------------------------------------------------
with-authorisation: func [permissions [block!] body [block!]][
    print ["[with-authorisation] granting" mold permissions]
    ; In real RFC-0006 Capability Analysis, this would elaborate to a dependent-type proof term
    ; and least-privilege check. Here we mock the HMAC receipt trace (RFC-0007 COMMIT).
    do body
]

execute: func [action [block!]][
    print ["[execute] capability-gated action:" mold action]
    print ["[execute] → Policy check → Budget check → MCP gateway → HMAC receipt (see RFC-0006/0007)"]
]

; ----------------------------------------------------------------------
; Reasoning, memory primitives (RFC-0005 §3.4–3.5) — mocks
; ----------------------------------------------------------------------
reason: func [spec [block!]][ print ["[reason]" mold spec] ]
remember: func [fact [block!]][ print ["[remember]" mold fact] ]
recall: func [query [block!]][ print ["[recall]" mold query] ]

goal: func [name [word! block!] body [block!]][
    print ["[goal]" mold name "→" mold body]
    do body
]

when: func [event [word! block!] body [block!]][
    print ["[when]" mold event "triggered → observing + reasoning"]
    do body
]

; ----------------------------------------------------------------------
; Repository Assistant — golden-file conformance test (RFC-0005 §3.9 normative)
; Must be single-block, human-readable, machine-executable, runtime-inspectable
; ----------------------------------------------------------------------
print "=== Red/Cognition — Golden-file conformance test (RFC-0005 §3.9) ==="

agent-prototype: context [
    project: make-belief "OpenClaw" 1.0 'user
    language: make-belief 'Rust 0.95 'observation

    ; Tool-like capability requiring proof if dangerous (RFC-0012 Tier 1)
    cap-delete: make-capability 'delete 'dangerous
    cap-generate-report: make-capability 'generate-report 'safe

    ; Event handle mock (in real CogOS, this is Event Bus subscription)
    on-github-push: does [
        print {"[event] github.push — entering observe→reason→plan→act→reflect loop"}

        obs: make-observation 'github 'push [% changed-modules: [%src/cogos.red %runtime/cogos.red]]

        reason [identify changed modules  estimate impact  choose review-strategy]
        print ["[plan] run tests  inspect architecture  summarize changes"]
        with-authorisation [generate-report: [scope 'repo expiry none]] [
            execute [generate report]
        ]

        ; Reflection with confidence divergence → semantic promotion (RFC-0003 promotion gate)
        print "[reflect] compare prediction with results; divergence 0.12 < 0.2 → no belief update"
        remember [lesson: "review-strategy matched prediction"]
    ]
]

agent-prototype/on-github-push

print "=== Governance: attempted dangerous without token (should be type error in real compiler) ==="
; In real RFC-0006 Capability Analysis this line would NOT TYPE-CHECK:
; execute [delete %temp/]
; Mock shows the intended gate:
print "[compiler] would reject: execute [delete %temp/] — missing with-authorisation [delete: scope %temp/] (see RFC-0012 Tier 1)"

with-authorisation [delete: [scope %temp/ expiry now]] [
    execute [delete %temp/]
]

print "=== Cognitive Lock File (RFC-0014) — illustrative ==="
print {cognitive.lock: [skills: [summarize:1.2.0] capabilities: [delete: dangerous v2] models: [small-local: ollama/llama3]]}
print "=== Prototype complete — next: implement Totality checker (RFC-0013) on recursive plan without base case ==="

