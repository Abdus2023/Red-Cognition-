# XLIII. The `map!` Datatype — Hash Map Deep Specification

```ascii
┌──────────────────────────────────────────────────────────────────────┐
│              MAP! DATATYPE — COMPLETE SPECIFICATION                  │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  PURPOSE: Hash map (associative array) with O(1) average lookup.    │
│  Keys: any Red value except block! path! image! (unhashable)        │
│  Values: any Red value                                               │
│                                                                      │
│  INTERNAL STRUCTURE:                                                 │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  map! object                                                │    │
│  │    hashtable:  array of bucket heads                        │    │
│  │    data:       flat series [k1 v1 k2 v2 k3 v3 ...]         │    │
│  │    size:       current number of key-value pairs            │    │
│  │    load-factor: 0.75 (rehash threshold)                     │    │
│  │                                                             │    │
│  │  HASH FUNCTION: murmur3 or FNV (type-dependent)            │    │
│  │  COLLISION RESOLUTION: chaining (linked list per bucket)    │    │
│  │                                                             │    │
│  │  From v0.6.4: Hashtables used for fast context lookups     │    │
│  │  This same mechanism powers map! and object field lookup   │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  CONSTRUCTION:                                                       │
│    m: make map! []                      ; empty                      │
│    m: make map! [a 1  b 2  c 3]        ; from block (pairs)        │
│    m: #(a: 1  b: 2  c: 3)             ; map literal syntax         │
│    m: to map! [a 1  b "hello"  c true] ; conversion from block      │
│                                                                      │
│  KEY OPERATIONS:                                                     │
│    put   m 'key value    ; set key (creates if absent)              │
│    select m 'key         ; get value (none if absent)               │
│    find   m 'key         ; returns [key value ...] tail or none     │
│    remove/key m 'key     ; delete key-value pair                    │
│    keys-of m             ; all keys as block                        │
│    values-of m           ; all values as block                      │
│    length? m             ; number of key-value pairs                │
│    clear m               ; remove all entries                       │
│    copy m                ; shallow copy                             │
│    copy/deep m           ; deep copy including nested values        │
│                                                                      │
│  ITERATION:                                                          │
│    foreach [k v] m [...]             ; iterate all pairs            │
│    foreach k keys-of m [...]         ; iterate keys only            │
│                                                                      │
│  KEY TYPES SUPPORTED:                                                │
│    word! string! integer! float! char! tuple! pair! date! url!       │
│    file! email! tag! issue! binary! any scalar type                  │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```