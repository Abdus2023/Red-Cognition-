Red [
    Title: "Red/Cognition — Inter-Layer Contracts (RFC-0005 §3.10)"
    Version: 0.1.0
    RFCs: "RFC-0005 §3.10 (Cognitive Pipe + Capability Binding), RFC-0007 dual substrates"
]

; RFC-0005 §3.10 — Cognitive Pipe Protocol
;   Downward: goal! → plan! → function call + policy check
;   Upward:   result + confidence + provenance + reflection
cog/pipe-downward: function [goal [object!]][
    print ["[Cognitive Pipe ↓] goal!" mold goal/spec "→ plan! → call+policy (RFC-0005 §3.10)"]
    ; Mock: shed cognitive metadata to typed Red value (see types.red)
]

cog/pipe-upward: function [result [any-type!] confidence [float!] provenance [block!]][
    print ["[Cognitive Pipe ↑]" mold result "confidence" confidence "provenance" mold provenance]
    ; Mock: acquire confidence/provenance before cognitive layer acts
    cog/make-belief result confidence 'inference
]

; RFC-0005 §3.10 — Capability Binding
;   Downward: Red function → Red/System native call + sandbox
;   Upward:   result + exit status + resource consumption
cog/bind-downward: function [fn [any-type!]][
    print ["[Capability Binding ↓]" mold fn "→ Red/System native + sandbox"]
]

cog/bind-upward: function [result [any-type!] exit-status [integer!] resources [block!]][
    print ["[Capability Binding ↑]" mold result "exit" exit-status "resources" mold resources]
]

print "[cog/contracts] loaded (pipe-downward/upward, bind-downward/upward — see RFC-0005 §3.10 diagram)"
