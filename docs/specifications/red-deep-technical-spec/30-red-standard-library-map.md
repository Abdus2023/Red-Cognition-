# XXXVI. The Red Standard Library — Complete Module Map

```ascii
┌──────────────────────────────────────────────────────────────────────┐
│              RED STANDARD LIBRARY — COMPLETE MODULE MAP              │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  CORE RUNTIME (always loaded):                                       │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  actions.red         ; polymorphic action dispatch          │    │
│  │  boot.red            ; bootstrap, system object init        │    │
│  │  context.red         ; context/binding operations           │    │
│  │  control.red         ; if either while until loop foreach   │    │
│  │  error.red           ; error! type and handlers             │    │
│  │  format.red          ; form mold sprint printf              │    │
│  │  functions.red       ; higher-order: map-each collect etc.  │    │
│  │  math.red            ; sin cos tan sqrt log exp ...         │    │
│  │  mezz.red            ; miscellaneous high-level functions   │    │
│  │  natives.red         ; wrappers for C-level natives         │    │
│  │  object.red          ; object model, inheritance            │    │
│  │  paren.red           ; paren! evaluation rules              │    │
│  │  path.red            ; path! access and navigation          │    │
│  │  reactivity.red      ; ~250 LOC reactive framework          │    │
│  │  series.red          ; generic series operations            │    │
│  │  sort.red            ; sort algorithm (introsort)           │    │
│  │  string.red          ; string manipulation                  │    │
│  │  system.red          ; system object definition             │    │
│  │  unicode.red         ; UTF-8/16/32 support                  │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  OPTIONAL MODULES (loaded on demand):                                │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  view/view.red       ; VID dialect + View engine            │    │
│  │  view/draw.red       ; Draw 2D vector dialect               │    │
│  │  view/rich-text.red  ; Rich-text formatting dialect         │    │
│  │  codec/png.red       ; PNG image encode/decode              │    │
│  │  codec/jpeg.red      ; JPEG image encode/decode             │    │
│  │  codec/gif.red       ; GIF image decode                     │    │
│  │  codec/csv.red       ; CSV parse and format                 │    │
│  │  codec/json.red      ; JSON parse and format                │    │
│  │  codec/redbin.red    ; Redbin binary format                 │    │
│  │  network/http.red    ; HTTP client (scheme handler)         │    │
│  │  crypto/hash.red     ; MD5 SHA-1 SHA-256 SHA-512 CRC32      │    │
│  │  compress/gzip.red   ; gzip/zlib/deflate compress           │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  KEY STANDARD FUNCTIONS (selected reference):                        │
│  ┌────────────────┬───────────────────────────────────────────┐     │
│  │  Series        │  append insert remove find select pick     │     │
│  │                │  sort reverse copy skip head tail at       │     │
│  │                │  length? index? empty? single? last?       │     │
│  ├────────────────┼───────────────────────────────────────────┤     │
│  │  String        │  form mold trim split rejoin uppercase     │     │
│  │                │  lowercase trim replace to-string          │     │
│  ├────────────────┼───────────────────────────────────────────┤     │
│  │  Control       │  if either unless case switch             │     │
│  │                │  while until loop repeat foreach           │     │
│  │                │  break continue return exit                │     │
│  ├────────────────┼───────────────────────────────────────────┤     │
│  │  Meta          │  do load save compose reduce               │     │
│  │                │  bind unbind in context? get set           │     │
│  │                │  func function does has routine            │     │
│  │                │  body-of spec-of type-of reflect           │     │
│  ├────────────────┼───────────────────────────────────────────┤     │
│  │  Type check    │  integer? string? block? object? word?     │     │
│  │                │  function? number? series? any-type?       │     │
│  │                │  type? datatype?                           │     │
│  ├────────────────┼───────────────────────────────────────────┤     │
│  │  I/O           │  read write load save print prin           │     │
│  │                │  open close query update                   │     │
│  │                │  list-dir make-dir delete rename           │     │
│  ├────────────────┼───────────────────────────────────────────┤     │
│  │  Math          │  + - */ //* * mod abs max min             │     │
│  │                │  sin cos tan asin acos atan atan2          │     │
│  │                │  sqrt log exp round floor ceil             │     │
│  ├────────────────┼───────────────────────────────────────────┤     │
│  │  Crypto        │  checksum (md5/sha256/sha512/crc32)       │     │
│  ├────────────────┼───────────────────────────────────────────┤     │
│  │  Compress      │  compress uncompress                       │     │
│  │                │  (gzip zlib deflate algorithms)            │     │
│  └────────────────┴───────────────────────────────────────────┘     │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```