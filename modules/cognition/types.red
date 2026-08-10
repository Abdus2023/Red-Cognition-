Red [
    Title: "Red/Cognition — Cognitive Types (RFC-0005 §3.2, 16 types scaffold)"
    Version: 0.1.0
    RFCs: "RFC-0005 (16 types), RFC-0020 (4-dim UQ), RFC-0018 (sovereignty)"
    License: "BSL-1.0"
    Needs: 'View
]

; RFC-0005 §3.2 — 16-type taxonomy with cognitive metadata slots
; Each type carries confidence/validity/source/scope per normative property.
; Mocked as objects until runtime/ datatype registration (see RFC-0009 evaluator dispatch).

; === Epistemic — carry truth & confidence (RFC-0005 §3.2 epistemic) ===
cog/make-belief: function [
    content [any-type!] confidence [float!] source [word!]
    /uq "override 4-dim UQ per RFC-0020 (default: reason=confidence, others 1.0)"
        input-uq [float!] reasoning-uq [float!] parameter-uq [float!] prediction-uq [float!]
    /valid "validity interval per Graphiti bi-temporal (RFC-0004 §3.4) — future"
        valid-from [date!] valid-to [date!]
][
    make object! [
        type: 'belief!                           ; RFC-0005 §3.2
        content: content
        confidence: confidence                   ; scalar aggregate — see RFC-0020 for 4-dim split
        source: source                           ; 'user | 'observation | 'inference — provenance chain start
        uq: reduce [any [input-uq 1.0] any [reasoning-uq confidence] any [parameter-uq 1.0] any [prediction-uq confidence]]
        validity: either valid [reduce [valid-from valid-to]][none] ; none = perpetual
        scope: none
    ]
]

cog/make-hypothesis: function [content confidence source][
    make object! [type: 'hypothesis! content: content confidence: confidence source: source]
]

cog/make-evidence: function [observation [object!] delta [float!]][
    make object! [type: 'evidence! observation: observation delta: delta] ; updates belief confidence
]

cog/make-observation: function [source [word!] event [word! block!] payload [any-type!]][
    make object! [type: 'observation! source: source event: event payload: payload timestamp: now]
]

; === Intentional — carry goal structure (RFC-0005 §3.2 intentional) ===
cog/make-goal: function [spec [block!] /achieve "declarative: desired state (modal-logic verifiable per GOAL language)"][
    make object! [type: 'goal! spec: spec declarative: achieve] ; RFC-0005 §3.3 vs plan! procedural
]

cog/make-plan: function [steps [block!]][
    make object! [type: 'plan! steps: steps dag: none hmac: none] ; dag/hmac filled by CIR/CVM (RFC-0006/0007)
]

cog/make-intention: function [plan [object!] commitment [block!]][
    make object! [type: 'intention! plan: plan commitment: commitment timestamp: now]
]

cog/make-capability: function [name [word!] policy [word! block!] /scope s [block!] /expiry e [date!]][
    make object! [
        type: 'capability!
        name: name
        policy: policy   ; 'safe | 'dangerous | [role: ... expiry: ...] — ABAC per RFC-0012 Tier
        scope: any [s []]
        expiry: e
    ]
]

; === Temporal — carry validity windows (RFC-0005 §3.2 temporal) ===
cog/make-memory: function [content confidence source [word!] timestamp [date!]][
    make object! [type: 'memory! content: content confidence: confidence source: source timestamp: timestamp]
]

cog/make-skill: function [name [word!] procedure [block!] domain [word!]][
    make object! [type: 'skill! name: name procedure: procedure domain: domain performance-history: copy []]
]

cog/make-episode: function [events [block!] narrative [string!]][
    make object! [type: 'episode! events: events narrative: narrative]
]

; === Normative — carry policy & constraint (RFC-0005 §3.2 normative) ===
cog/make-policy: function [name [word!] rule [block!]][
    make object! [type: 'policy! name: name rule: rule]
]

cog/make-permission: function [capability [object!] scope [block!] expiry [date! none!]][
    make object! [type: 'permission! capability: capability scope: scope expiry: expiry granted-at: now]
]

cog/make-event: function [trigger [block!] response [block!]][
    make object! [type: 'event! trigger: trigger response: response]
]

; === RFC-0024: agent! housing (facets) ===
cog/make-agent: function [spec [block!]][
    make object! [
        type: 'agent!
        beliefs: copy []
        goals: copy []
        memories: copy []
        skills: copy []
        policies: copy []
        capabilities: copy []
        reflection: copy []
        spec: spec
    ]
]

print "[cog/types] loaded 16-type scaffold (RFC-0005 §3.2) — try: probe cog/make-belief 'OpenClaw 1.0 'user"
