# XLIII. Map Patterns — Complete Reference

```red
; ── Construction variants ─────────────────────────────────────────────
m1: make map! []
m2: make map! [name "Alice"  age 30  active true]
m3: #(x: 10  y: 20  z: 30)                    ; map! literal
m4: to map! [red 255  green 128  blue 0]       ; from block

; ── All key types ────────────────────────────────────────────────────
mixed: make map! []
put mixed 'word-key     "word key value"
put mixed "string-key"  "string key value"
put mixed 42            "integer key value"
put mixed 3.14          "float key value"
put mixed #"A"          "char key value"
put mixed 1.2.3         "tuple key value"
put mixed 100x200       "pair key value"
put mixed 2026-07-29    "date key value"

; ── Nested map structures ────────────────────────────────────────────
config: make map! []
put config 'database make map! [
    host "localhost"
    port 5432
    name "mydb"
]
put config 'server make map! [
    host "0.0.0.0"
    port 8080
    workers 4
]

; Deep path access
print config/database/host    ; → localhost
print config/server/port      ; → 8080

; ── Functional map operations ────────────────────────────────────────
; Filter: only keep entries where value > 5
scores: #(alice: 8  bob: 3  carol: 9  dave: 4  eve: 7)

high-scores: make map! []
foreach [name score] scores [
    if score > 5 [put high-scores name score]
]

; Transform: double all values
doubled: make map! []
foreach [k v] scores [put doubled k v * 2]

; Merge two maps (second wins on conflict)
merge-maps: func [base override][
    result: copy base
    foreach [k v] override [put result k v]
    result
]

; ── Map as graph adjacency list ──────────────────────────────────────
graph: make map! []
put graph 'A ['B 'C]
put graph 'B ['D]
put graph 'C ['D 'E]
put graph 'D []
put graph 'E []

; BFS traversal
bfs: func [start [word!]][
    visited: make map! []
    queue:   reduce [start]
    while [not empty? queue][
        node: take queue
        unless select visited node [
            put visited node true
            print node
            foreach neighbor select graph node [
                append queue neighbor
            ]
        ]
    ]
]

bfs 'A    ; → A B C D E

; ── Cognitive semantic memory as map ────────────────────────────────
; Subject-Predicate → Object triple store via nested maps
make-triple-store: func [][
    make object! [
        store: make map! []

        add: func [s p o confidence][
            subj-map: any [select store s  make map! []]
            put subj-map p reduce [o confidence now]
            put store s subj-map
        ]

        query-subject: func [s][
            select store s
        ]

        query-sp: func [s p][
            subj-map: select store s
            if subj-map [select subj-map p]
        ]

        all-subjects: func [][
            keys-of store
        ]
    ]
]

ts: make-triple-store
ts/add 'project 'name     "OpenClaw"  1.0
ts/add 'project 'language 'Rust       0.95
ts/add 'project 'status   'active     1.0

result: ts/query-sp 'project 'language
print rejoin ["Language: " result/1 " (conf: " result/2 ")"]
```