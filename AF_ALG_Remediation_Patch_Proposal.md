# AF_ALG Remediation Patch Proposal

**Status:** Proposal only; not applied to the repository or verification source tree.

## Objective

Prevent `runtime/crypto.reds` from returning an uninitialized digest buffer when Linux AF_ALG is unavailable or any AF_ALG operation fails. The proposal intentionally separates defensive error propagation from the later choice of a validated fallback backend.

## Proposed change

In the Linux AF_ALG `get-digest` implementation at `runtime/crypto.reds:640–679`:

```diff
@@
 				hash: allocate 64					;-- caller should free it
 				sa: allocate 88
 				set-memory sa #"^@" 88
@@
-				fd: socket AF_ALG SOCK_SEQPACKET 0
-				sock-bind fd sa 88
-				opfd: accept fd null null
-				_write opfd as c-string! data len
-				_read opfd hash alg-digest-size type
+				fd: socket AF_ALG SOCK_SEQPACKET 0
+				if fd < 0 [
+					free sa
+					free hash
+					fire [TO_ERROR(script no-connect) integer/push fd]
+				]
+				if sock-bind fd sa 88 < 0 [
+					_close fd
+					free sa
+					free hash
+					fire [TO_ERROR(script no-connect) integer/push fd]
+				]
+				opfd: accept fd null null
+				if opfd < 0 [
+					_close fd
+					free sa
+					free hash
+					fire [TO_ERROR(script no-connect) integer/push opfd]
+				]
+				if _write opfd as c-string! data len <> len [
+					_close opfd
+					_close fd
+					free sa
+					free hash
+					fire [TO_ERROR(script no-connect) integer/push opfd]
+				]
+				size: _read opfd hash alg-digest-size type
+				if size <> alg-digest-size type [
+					_close opfd
+					_close fd
+					free sa
+					free hash
+					fire [TO_ERROR(script no-connect) integer/push opfd]
+				]
 				_close opfd
 				_close fd
***
```

## Required review corrections before application

The exact Red/System error constructor and cleanup idiom must be confirmed against the repository’s established conventions before this diff is applied. In particular, the final implementation must use the project’s canonical error identifier for an unavailable crypto backend, must ensure `fire` does not bypass required cleanup, and must use a local variable for the expected digest length if the compiler rejects the direct refinement expression in the comparison.

This defensive patch would make the current host failure explicit and safe, but it would not make MD5, SHA, or HMAC tests pass on an AF_ALG-less host. A validated fallback backend remains required for functional portability.

## Required tests after application

The patch must be tested in two environments or modes. On the current host, the checksum diagnostic should raise a controlled runtime error rather than return malformed bytes. On a host with AF_ALG support, all existing checksum and HMAC known-answer vectors must pass. The existing Adler-32 tests must remain unchanged and passing.

## Non-application record

This proposal is stored outside the repository so the user’s branch and its pre-existing dirty state remain unchanged. It is not a claim that the proposed Red/System syntax has compiled, and it must undergo project-native syntax validation before use.
