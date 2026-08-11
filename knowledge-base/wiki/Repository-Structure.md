# Repository Structure

> Provenance: Corpus message #2, sub-messages [19], [20]. Cross-checked against the actual repository checkout on 2026-08-10.

## Documented Governance Layout (sub-message [20])

Repository governance recommendation: directory layout `specs/`, `rfcs/`, `compiler/`, `runtime/`, `dialects/`, `cognition/`, `tests/`, `examples/`, `docs/` and expected outputs. *(Source quirk: unmatched closing `)` after the list — preserved in archive.)*

Operating context (sub-message [19]): "You are now operating inside the `Red-Cognition-` repository. All work should align with the documented architecture and the long-term goal of turning Red into a true cognitive computing platform."

## Status vs. actual repository (checked 2026-08-10, branch `arena/019fecf1-red-cognition`, base commit `9b5b15aa8a650f13b33e20509430fde10c3a35b1`)

| Documented directory | Repository state | Action taken |
|---|---|---|
| `specs/` | did not exist | Scaffolded (empty, `.gitkeep`) |
| `rfcs/` | did not exist | Scaffolded (empty, `.gitkeep`) |
| `compiler/` | did not exist (note: upstream Red has a root file `compiler.r`, not a `compiler/` directory) | Scaffolded (empty, `.gitkeep`) |
| `runtime/` | **pre-exists** (upstream Red runtime sources) | Left as-is; documented layout name collides with existing upstream directory |
| `dialects/` | did not exist | Scaffolded (empty, `.gitkeep`) |
| `cognition/` | did not exist | Scaffolded (empty, `.gitkeep`) |
| `tests/` | **pre-exists** (upstream Red tests) | Left as-is |
| `examples/` | did not exist | Scaffolded (empty, `.gitkeep`) |
| `docs/` | **pre-exists** (upstream Red documentation: lexer docs, red-system specs, matrices) | Left as-is |

Additionally maintained: `knowledge-base/` (this knowledge base; established by corpus message #1 governance).

## Discrepancies recorded (not resolved — no inference attempted)

1. The documented layout is a **recommendation inside a proposal** (sub-message [20]), not an established fact of the existing upstream Red repository, whose actual layout (`build/`, `bridges/`, `docs/`, `environment/`, `libRed/`, `modules/`, `quick-test/`, `runtime/`, `system/`, `tests/`, `utils/`, root files `compiler.r`, `lexer.r`, `red.r`, `boot.red`, etc.) differs.
2. Three documented names (`runtime/`, `tests/`, `docs/`) collide with pre-existing upstream directories holding unrelated upstream content; `compiler/` vs root `compiler.r` is a naming divergence.
3. No code snippet in the corpus carries a documented repository path, so **no extracted code has been scaffolded into these directories** — all snippets remain **Unresolved Location** (see [Code Snippets](Code-Snippets.md)).

## Related pages

[Specifications](Specifications.md) (SPEC-3) · [Code Snippets](Code-Snippets.md) · [Source Traceability](Source-Traceability.md)

## Message #3 update — specs/ now populated (2026-08-10)

Corpus message #3 delivers ratified/draft specifications whose placement in `specs/` is documented by RC-000 §8 Repository Governance:

| File | Content | Origin | Status |
|---|---|---|---|
| `specs/RC-000-constitution.md` | RC-000 Constitution v1.0 — **Ratified** (Date 2026-07-29) | corpus [33] | Scaffolded verbatim |
| `specs/RC-100-architecture-specification.md` | RC-100 Architecture Specification v1.1 — Candidate for Ratification; freeze review APPROVED ([40]); ratification record not yet in corpus | corpus [39] | Scaffolded verbatim |

`rfcs/` remains empty: RFC-0001…0004 exist only as recommended outlines ([34]); no RFC document text exists in the corpus (no content fabricated).

## Message #5 update — specs/ populated with RC-100…RC-600 documents (2026-08-10)

| File | Content | Origin | Status |
|---|---|---|---|
| `specs/RC-100-ratification-record.md` | RC-100 ratification record (v1.0 ratified, 2026-07-29) | corpus msg#4 [41] | Scaffolded verbatim |
| `specs/RC-200-language-specification.md` | RC-200 v1.2 (ratified content) | corpus msg#4 [47] | Scaffolded verbatim |
| `specs/RC-200-ratification-record.md` | RC-200 ratification record (v1.0 ratified, 2026-07-29) | corpus msg#4 [49] | Scaffolded verbatim |
| `specs/RC-300-compiler-specification.md` | RC-300 v1.1 Candidate for Ratification (approved for ratification in [54]; ratification record absent from corpus) | corpus msg#4 [53] | Scaffolded verbatim |
| `specs/RC-400-runtime-specification.md` | RC-400 v1.0 Draft | corpus msg#4 [55] | Scaffolded verbatim |
| `specs/RC-500-cognitive-runtime-specification.md` | RC-500 v1.0 Draft | corpus msg#4 [57] | Scaffolded verbatim |
| `specs/RC-600-agent-runtime-shell-specification.md` | RC-600 v1.0 Draft | corpus msg#4 [59] | Scaffolded verbatim |

`rfcs/` remains empty: RFC-0001…0008 exist only as registrations/proposals/outlines — no RFC document text in corpus (nothing fabricated).

## Message #8 update — specs/ and rfcs/ populated; Phase-0 skeleton recorded (2026-08-10)

Newly scaffolded (verbatim from corpus message #8):

| File | Content | Origin | Status |
|---|---|---|---|
| `specs/RC-700-cognitive-vm-specification.md` | RC-700 v1.0 Draft | [61] | Scaffolded verbatim |
| `specs/RC-800-cognitive-os-specification.md` | RC-800 v1.0 Draft | [63] | Scaffolded verbatim |
| `specs/RC-900-governance-manual.md` | RC-900 v1.0 Draft | [65] | Scaffolded verbatim |
| `rfcs/RFC-0001-cognitive-type-system.md` | RFC-0001 v1.2 (ratified content) | [71] | Scaffolded verbatim |
| `rfcs/RFC-0001-ratification-record.md` | RFC-0001 ratification record | [72] | Scaffolded verbatim |
| `rfcs/RFC-0002-effect-ordering-model.md` | RFC-0002 v1.1 (ratified content) | [75] | Scaffolded verbatim |
| `rfcs/RFC-0002-ratification-record.md` | RFC-0002 ratification record | [76] | Scaffolded verbatim |
| `rfcs/RFC-0003-belief-revision-system.md` | RFC-0003 v1.1 (candidate) | [79] | Scaffolded verbatim |

**Phase-0 reference-implementation skeleton ([66]) — recorded as documented proposal, NOT scaffolded:** `red-cognition/` with `specs/ (RC-000.md, RC-100.md, RC-200.md, …)`, `compiler/ (parser/, ast/, red-ir/, cognitive-ir/, backend/)`, `runtime/ (red-runtime/, cognitive-runtime/, memory/, scheduler/, tracing/)`, `cvm/ (instruction-set/, interpreter/, bytecode/)`, `cogos/ (process-manager/, capability-manager/, distributed-services/)`, `tests/`. Differences vs. current scaffolding: filename style (RC-000.md vs RC-000-constitution.md), new dirs `cvm/`, `cogos/` not in the RC-000 §8 mandated layout, no `rfcs/ dialects/ cognition/ examples/ docs/`. Discrepancy recorded, unresolved (ambiguity: whether Phase-0 skeleton supersedes or complements the mandated layout is not stated in corpus).

## Message #10 update — rfcs/ populated with RFC-0003…RFC-0008 (2026-08-10)

| File | Content | Origin | Status |
|---|---|---|---|
| `rfcs/RFC-0003-belief-revision-system.md` | RFC-0003 v1.2 (ratified; supersedes previously scaffolded v1.1, kept in archive) | msg#10 [81] | Scaffolded verbatim |
| `rfcs/RFC-0004-goal-lifecycle-satisfaction-model.md` | RFC-0004 v1.1 (ratified per [86]) | msg#10 [85] | Scaffolded verbatim |
| `rfcs/RFC-0005-planning-semantics.md` | RFC-0005 v1.0 Draft | msg#10 [87] | Scaffolded verbatim |
| `rfcs/RFC-0006-capability-model.md` | RFC-0006 v1.2 (approved for final ratification per [94]) | msg#10 [93] | Scaffolded verbatim |
| `rfcs/RFC-0007-skill-model.md` | RFC-0007 v1.1 Candidate | msg#10 [97] | Scaffolded verbatim |
| `rfcs/RFC-0008-memory-model.md` | RFC-0008 v1.0 Draft | msg#10 [99] | Scaffolded verbatim |

Current scaffold totals: 12 documents in `specs/` (RC-000…RC-900 incl. RC-100 and RC-200 ratification records), 10 files in `rfcs/` (RFC-0001…RFC-0008 current versions + RFC-0001/RFC-0002 ratification records). Only current normative versions scaffolded; superseded versions preserved in archive.

## Message #12 update — rfcs/ populated with RFC-0009…RFC-0013 (2026-08-10)

| File | Content | Origin | Status |
|---|---|---|---|
| `rfcs/RFC-0009-agent-model.md` | RFC-0009 v1.0 Draft | msg#12 [101] | Scaffolded verbatim |
| `rfcs/RFC-0010-checkpoint-recovery-model.md` | RFC-0010 v1.0 Draft | msg#12 [103] | Scaffolded verbatim |
| `rfcs/RFC-0011-scheduler-execution-model.md` | RFC-0011 v1.2 (ratified content) | msg#12 [109] | Scaffolded verbatim |
| `rfcs/RFC-0011-ratification-record.md` | RFC-0011 ratification document (Ratified, 2026-07-29) | msg#12 [111] | Scaffolded verbatim |
| `rfcs/RFC-0012-cvm-execution-semantics.md` | RFC-0012 v1.1 Candidate (approved for ratification per [116]) | msg#12 [115] | Scaffolded verbatim |
| `rfcs/RFC-0013-cisa.md` | RFC-0013 CISA v1.1 Candidate | msg#12 [119] | Scaffolded verbatim |

Current scaffold totals: 12 documents in `specs/`, 16 files in `rfcs/` (13 RFC documents: RFC-0001…RFC-0013 current versions + 3 ratification records: RFC-0001, RFC-0002, RFC-0011). Only current normative versions scaffolded; superseded versions preserved in archive.

## Message #14 update — rfcs/ populated with RFC-0014…RFC-0023 (2026-08-10)

| File | Content | Origin | Status |
|---|---|---|---|
| `rfcs/RFC-0014-cisa-binary-encoding.md` | RFC-0014 v1.0 Draft | msg#14 [121] | Scaffolded verbatim |
| `rfcs/RFC-0015-cognitive-exception-semantics.md` | RFC-0015 v1.0 Draft | msg#14 [123] | Scaffolded verbatim |
| `rfcs/RFC-0016-cognitive-runtime-architecture.md` | RFC-0016 v1.0 Draft | msg#14 [125] | Scaffolded verbatim |
| `rfcs/RFC-0017-runtime-interface-service-model.md` | RFC-0017 v1.0 Draft | msg#14 [127] | Scaffolded verbatim |
| `rfcs/RFC-0018-event-log-replay-protocol.md` | RFC-0018 v1.0 Draft | msg#14 [129] | Scaffolded verbatim |
| `rfcs/RFC-0019-cogos-architecture.md` | RFC-0019 v1.0 Draft | msg#14 [131] | Scaffolded verbatim |
| `rfcs/RFC-0020-distributed-execution-protocol.md` | RFC-0020 v1.0 Draft | msg#14 [133] | Scaffolded verbatim |
| `rfcs/RFC-0021-cognitive-network-protocol.md` | RFC-0021 v1.0 Draft | msg#14 [135] | Scaffolded verbatim |
| `rfcs/RFC-0022-identity-trust-framework.md` | RFC-0022 v1.0 Draft | msg#14 [137] | Scaffolded verbatim |
| `rfcs/RFC-0023-consensus-causal-agreement.md` | RFC-0023 v1.0 Draft | msg#14 [139] | Scaffolded verbatim |

Current scaffold totals: 12 documents in `specs/`, 26 files in `rfcs/` (23 RFC documents RFC-0001…RFC-0023 current versions + 3 ratification records: RFC-0001, RFC-0002, RFC-0011). Only current versions scaffolded; superseded versions preserved in archive.

## Message #16 update — rfcs/ populated with RFC-0024…RFC-0033 (2026-08-10)

| File | Content | Origin | Status |
|---|---|---|---|
| `rfcs/RFC-0024-resource-management-quota-model.md` | RFC-0024 v1.0 Draft | msg#16 [141] | Scaffolded verbatim |
| `rfcs/RFC-0025-security-policy-language.md` | RFC-0025 CSPL v1.0 Draft | msg#16 [143] | Scaffolded verbatim |
| `rfcs/RFC-0026-hardware-acceleration-model.md` | RFC-0026 v1.0 Draft | msg#16 [145] | Scaffolded verbatim |
| `rfcs/RFC-0027-compiler-toolchain-architecture.md` | RFC-0027 v1.0 Draft | msg#16 [147] | Scaffolded verbatim |
| `rfcs/RFC-0028-cognitive-intermediate-representation.md` | RFC-0028 CIR v1.0 Draft | msg#16 [149] | Scaffolded verbatim |
| `rfcs/RFC-0029-cir-serialization-format.md` | RFC-0029 CIR-SER v1.0 Draft | msg#16 [151] | Scaffolded verbatim |
| `rfcs/RFC-0030-optimization-pass-framework.md` | RFC-0030 v1.0 Draft | msg#16 [153] | Scaffolded verbatim |
| `rfcs/RFC-0031-coil-transformation-language.md` | RFC-0031 COIL v1.0 Draft | msg#16 [155] | Scaffolded verbatim |
| `rfcs/RFC-0032-covf-verification-framework.md` | RFC-0032 COVF v1.0 Draft | msg#16 [157] | Scaffolded verbatim |
| `rfcs/RFC-0033-proof-carrying-program-format.md` | RFC-0033 CPCPF v1.0 Draft | msg#16 [159] | Scaffolded verbatim |

Current scaffold totals: 12 documents in `specs/`, 36 files in `rfcs/` (33 RFC documents RFC-0001…RFC-0033 current versions + 3 ratification records: RFC-0001, RFC-0002, RFC-0011). Only current versions scaffolded; superseded versions preserved in archive.

## Message #18 update — rfcs/ populated with RFC-0034…RFC-0042 (2026-08-10)

| File | Content | Origin | Status |
|---|---|---|---|
| `rfcs/RFC-0034-cpr-tdp-package-registry.md` | RFC-0034 v1.0 Draft | msg#18 [163] | Scaffolded verbatim |
| `rfcs/RFC-0035-cseim-sandbox-isolation.md` | RFC-0035 v1.0 Draft (from review msg) | msg#18 [164] | Scaffolded verbatim |
| `rfcs/RFC-0036-cbr-scp-supply-chain.md` | RFC-0036 v1.0 Draft | msg#18 [165] | Scaffolded verbatim |
| `rfcs/RFC-0037-cslemp-lifecycle-evolution.md` | RFC-0037 v1.0 Draft (from review msg) | msg#18 [166] | Scaffolded verbatim |
| `rfcs/RFC-0038-cmaep-marketplace-economy.md` | RFC-0038 v1.0 Draft (duplicated RFC-0034 text in [167] truncated at duplication point; note in file) | msg#18 [167] | Scaffolded verbatim |
| `rfcs/RFC-0039-cieop-identity-economy-ownership.md` | RFC-0039 v1.0 Draft | msg#18 [169] | Scaffolded verbatim |
| `rfcs/RFC-0040-cgcdp-governance-collective-decision.md` | RFC-0040 v1.0 Draft | msg#18 [171] | Scaffolded verbatim |
| `rfcs/RFC-0041-cifp-interoperability-federation.md` | RFC-0041 v1.0 Draft | msg#18 [173] | Scaffolded verbatim |
| `rfcs/RFC-0042-cadp-autonomous-deployment.md` | RFC-0042 v1.0 Draft (ratified per [179]) | msg#18 [177] | Scaffolded verbatim |
| `rfcs/RFC-0042-ratification-record.md` | RFC-0042 ratification acknowledgement | msg#18 [179] | Scaffolded verbatim |

Current scaffold totals: 12 documents in `specs/`, 46 files in `rfcs/` (42 RFC documents RFC-0001…RFC-0042 current versions + 4 ratification records: RFC-0001, RFC-0002, RFC-0011, RFC-0042). Only current versions scaffolded; superseded/truncated precursors preserved in archive.

## Message #21 update — rfcs/ populated with RFC-0043…RFC-0047 (2026-08-11)

`rfcs/` now contains **51 files**: 47 RFC documents (RFC-0001…RFC-0047) + 4 ratification records (RFC-0001, RFC-0002, RFC-0011, RFC-0042). New scaffolds (documented placement per RC-000 §8, byte-exact from archive): RFC-0043-cls-language-specification.md ([181]), RFC-0044-csl-standard-library.md ([185]), RFC-0045-ctdx-tooling-developer-experience.md ([189]), RFC-0046-codp-observability-diagnostics.md ([195]), RFC-0047-cpmws-package-manager-workspace.md ([199]). No standalone ratification record for RFC-0046: its ratification exists as the review declaration in [196] (recorded in the scaffold's provenance header and RFC Index).

## Message #22 update — rfcs/ populated with RFC-0048…RFC-0050; RFC-0047 updated (2026-08-11)

`rfcs/` now contains **55 files**: 50 RFC documents (RFC-0001…RFC-0050) + 5 ratification records (RFC-0001, RFC-0002, RFC-0011, RFC-0042, RFC-0049). Changes: RFC-0047 scaffold updated to v1.2 ([201], ratified per [202]); new scaffolds RFC-0048-cffi-foreign-function-interface.md ([205] v1.1), RFC-0049-csts-standard-toolchain.md ([211] v1.2), RFC-0049-ratification-record.md ([215]), RFC-0050-architecture-conformance-specification.md ([219] v1.1) — documented placement per RC-000 §8, byte-exact from archive.

## Message #23 update — rfcs/ populated with RFC-0051…RFC-0053; RFC-0050 updated (2026-08-11)

`rfcs/` now contains **60 files**: 53 RFC documents (RFC-0001…RFC-0053) + 7 ratification records (RFC-0001, RFC-0002, RFC-0011, RFC-0042, RFC-0049, RFC-0050, RFC-0052). Changes: RFC-0050 scaffold updated to v1.2 ([221], ratified per [224]/[225]) + new RFC-0050-ratification-record.md ([225]); new RFC-0051-cmms-macro-metaprogramming.md ([227]), RFC-0052-ctvf-testing-verification.md ([233] v1.2, ratified per [235]), RFC-0052-ratification-record.md ([235]), RFC-0053-craip-remote-agent-invocation.md ([239] v1.1) — documented placement per RC-000 §8, byte-exact from archive.
