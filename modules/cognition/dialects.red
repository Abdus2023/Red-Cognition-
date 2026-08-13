Red [
    Title: "Red/Cognition — Dialects (RFC-0005 §3.4–3.8 + RFC-0012 ergonomic proof)"
    Version: 0.1.0
    RFCs: "RFC-0005 (reasoning/memory/capability dialects), RFC-0012 (with-authorisation), RFC-0015 (yield)"
    Needs: 'View
]

#include %types.red

; RFC-0005 §3.4 — Native reasoning blocks become reasoning graphs, not control flow (LoT)
cog/reason: function [spec [block!] /using model [word! block!]][
    print ["[reason" either using [rejoin [" using " mold model]][ "" "] " mold spec]
    ; Real impl: build Intent Graph (RFC-0006 CIR) — mocked here
]

; RFC-0005 §3.5 — Memory primitives (runtime determines vector vs graph route)
cog/remember: function [fact [block!]][ print ["[remember]" mold fact] ]
cog/recall:   function [query [block!]][ print ["[recall]" mold query]  ]
cog/forget:   function [spec [block!]][ print ["[forget]" mold spec " — see RFC-0018 sovereignty attestation"] ]

; RFC-0005 §3.6 — Capability-gated execution (policy/risk/sandbox/audit before action)
cog/execute: function [action [block!]][
    print ["[execute] capability-gated" mold action]
    print "  → Policy Evaluation → Budget Check → MCP Gateway (RFC-0011) → INTENT-CLASSIFIER (RFC-0017) → HMAC COMMIT (RFC-0007)"
]

; RFC-0012 — Ergonomic proof: with-authorisation elaborates to dependent-type proof term
; Usage: with-authorisation [delete: [scope %temp/ expiry now + 00:30:00]] [execute [delete %temp/]]
cog/with-authorisation: function [permissions [block!] body [block!]][
    print ["[with-authorisation] granting" mold permissions "— elaborates to proof term (RFC-0012 Tier 1)"]
    do body
]

; RFC-0015 — Cooperative yield (non-preemptible LLM liveness)
cog/yield: function [/hint spec [block!]][
    print ["[yield" either hint [rejoin [" hint " mold spec]][ "] " "— Goal Scheduler checkpoint (RFC-0015)"]
]

; RFC-0005 §3.8 — Event-driven: when <event> [observe reason update notify]
cog/when: function [event [word! block! path!] body [block!]][
    print ["[when]" mold event "triggered → Observe→Reason→Plan→Act→Reflect loop (RFC-0003)"]
    do body
]

cog/goal: function [name [word! block!] body [block!]][
    print ["[goal]" mold name "→" mold body " (RFC-0005 §3.3 — runtime decides how)"]
    do body
]

cog/plan: function [steps [block!]][ print ["[plan]" mold steps " — expands to DAG (RFC-0006)"] ]

print "[cog/dialects] loaded (reason/remember/recall/execute/with-authorisation/yield/when/goal/plan)"
