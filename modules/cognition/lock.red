Red [
    Title: "Red/Cognition — Cognitive Lock File & Drift Protocol (RFC-0014 scaffold)"
    Version: 0.1.0
    RFCs: "RFC-0014 (cognitive.lock + drift protocol), RFC-0006 CIR, RFC-0007 CVM, RFC-0011 adapters"
]

; RFC-0014 §1.1 — cognitive.lock schema (env snapshot) — auto-generated, do not edit
; Illustrative; real impl hashes CIR + captures live versions from build/build.r + adapters + models

cog/generate-lock: function [
    cir-hash [string! none!] "hex of CIR artifact (Intent→Task→Capability→Exec)"
    /skills list [block!] "e.g. [summarize: 1.2.0 vector-store: 3.0.1]"
    /capabilities list [block!]
    /models list [block!]
    /adapters list [block!]
][
    lock: rejoin [
        "; auto-generated — do not edit; see RFC-0014" newline
        "lockfile 1.0 [" newline
        "  red-version: " system/version newline
        "  cir-hash: " any [cir-hash "#a1b2c3..."] newline
        "  skills: " mold any [list [summarize: 1.2.0 vector-store: 3.0.1]] newline
        "  capabilities: [delete: policy dangerous v2  read: policy safe v1]" newline
        "  models: [small-local: ollama/llama3  large-remote: openai/gpt-5]" newline
        "  adapters: [mcp-gateway: 0.4.1  graphiti: 1.0.3]" newline
        "  provenance: [compiled: " now "  by: " system/version "  source: RED-AI-SYNTHESIS-001]" newline
        "]" newline
    ]
    print "[cog/generate-lock] RFC-0014 schema:"
    print lock
    write %cognitive.lock lock
    print "[cog/generate-lock] → wrote %cognitive.lock (HMAC + provenance — drift check on next EXECUTE)"
    lock
]

; RFC-0014 §1.2 — Drift protocol: Compile → Execute (check lock vs live before EXECUTE) → refuse+receipt if drift
cog/check-drift: function [
    lock-file [file!] live-env [block!] "live versions to compare, e.g. [graphiti: 1.0.3]"
][
    print rejoin ["[cog/check-drift] RFC-0014: checking " lock-file " vs live " mold live-env]
    either exists? lock-file [
        lock: load lock-file
        ; Mock: compare one field (graphiti version)
        if find mold lock "graphiti: 1.0.3" [
            print "  → no drift → EXECUTE allowed + HMAC receipt (RFC-0007 COMMIT)"
            true
        ] [
            print "  → DRIFT detected → refuse EXECUTE, emit drift receipt, require `red --recompile-cir`"
            false
        ]
    ][
        print "  → no lock file — compile first (`red --recompile-cir` per RFC-0014) — refuse EXECUTE"
        false
    ]
]

cog/recompile-cir: function [][
    print "[cog/recompile-cir] RFC-0014: recompiling CIR against live env — regenerates cognitive.lock + new cir-hash"
    cog/generate-lock "#new-hash..."
]

print "[cog/lock] loaded — try: cog/generate-lock #abc123 / cog/check-drift %cognitive.lock [graphiti: 1.0.4]"
