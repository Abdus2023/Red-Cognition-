# III. The Red/System Compiler — Internal Source Map

```
red-system/
  compiler.r
  emitter.r
  linker.r
  rsc.r
  formats/
    PE.r
    ELF.r
  library/
  runtime/
    common.reds
    win32.r
    linux.r
  targets/
    target-class.r
    IA32.r
  tests/
```

**Objects hierarchy after loading:**

```
system/words/
system-dialect/
  loader/
    process
  compiler/
    compile
  emitter/
```