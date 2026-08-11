# RFC-0072 v1.6 — Final Ratification Review

**Status:** Candidate for Final Ratification Review  
**Assessment:** Strong candidate. RFC-0072 v1.6 successfully extends RFC-0057 from an abstract transaction semantics layer into an interoperable transport-neutral wire specification.

The document now establishes the missing **CDTCP interoperability boundary**:

```
Cognitive Transaction Model
         │
         ▼
RFC-0057 CDTCP (Transaction semantics)
         │
         ▼
RFC-0058 CTWP (Wire encoding + interoperability)
         │
         ▼
Transport Layer (TCP / QUIC / IPC / Message Bus)
```

## Ratification Review Findings

### ✅ Strengths

RFC-0072 v1.6 defines:

- Deterministic binary framing model
- Canonical message envelope
- Stable message type registry
- Explicit flag registry
- Version negotiation
- Deterministic serialization requirements
- Encoding profiles
- Stream multiplexing
- Sequence ordering and replay protection
- Structured error model
- Explicit conformance requirements

The RFC now provides sufficient foundation for independent implementations.

### Remaining Normative Gaps

#### 1. Binary layout is still partially ambiguous

The frame includes variable-sized structures:

```
TraceContext
Payload
IntegrityBlock
```

There is no definition of how receivers determine where one begins and the next ends.

The RFC should define explicit length fields, for example:

```
uint32 TraceContextLength
TraceContext

uint32 PayloadLength
Payload

uint32 IntegrityLength
IntegrityBlock
```

Without these, decoding is ambiguous.

#### 2. Canonical Binary Encoding is not specified

The document repeatedly references:

> Canonical Binary Encoding

but never defines it.

An implementation cannot know:

- string encoding
- array ordering
- map ordering
- integer encoding
- floating point rules
- optional field encoding
- null representation

A future RFC should define this completely.

#### 3. Feature bitmap registry is missing

Handshake contains:

> SupportedFeatures (uint32 bitmap)

but nowhere defines:

```
bit 0 = Compression
bit 1 = Replay
bit 2 = Integrity
bit 3 = Signature
bit 4 = Streaming
...
```

Without a registry, different implementations could assign different meanings.

#### 4. Encoding bitmap registry

Similarly:

> SupportedEncodings

should define the bitmap.

Example:

```
Bit0 Binary
Bit1 CBOR
Bit2 MessagePack
Bit3 JSON
```

#### 5. Security profile registry

Handshake negotiates:

> SelectedSecurityProfile

No profile definitions exist.

Need profiles such as:

```
Profile 0  No authentication
Profile 1  SHA-256 + Ed25519
Profile 2  SHA-512 + Ed448
...
```

Otherwise implementations cannot negotiate security.

#### 6. Integrity algorithms

Current definition:

> AlgorithmID

needs a registry.

Example:

```
1 SHA-256
2 SHA-512
3 BLAKE3
4 SHA3-256
```

Likewise for signatures.

#### 7. Compression registry

Flags indicate:

> Compressed

No compression algorithm is specified.

Need identifiers such as:

```
0 None
1 Zstd
2 LZ4
3 Brotli
```

#### 8. Version negotiation algorithm

The RFC specifies exchanging ranges but not how a version is selected.

It should specify something like:

> highest mutually supported version
> major first, then highest minor
> otherwise fail

This avoids divergent implementations.

#### 9. Replay window

Replay protection exists but acceptance rules do not.

Need normative guidance:

- acceptable clock skew
- nonce cache lifetime
- sequence window size
- epoch rollover behavior

#### 10. Stream lifecycle

Need definitions for:

- stream creation
- stream closure
- stream reset
- stream cancellation
- maximum StreamID
- stream reuse

Without these, multiplexing behavior is underspecified.

#### 11. Reserved flag semantics

Reserved bits are listed but not specified.

Typically RFCs require:

> Reserved bits MUST be zero on transmission and ignored on reception.

Otherwise extensions become ambiguous.

#### 12. Unknown message types

Need interoperability rules.

Should receiver:

- ignore
- reject
- forward
- generate ErrorMessage

RFC should define this.

#### 13. Maximum frame size

No limits exist.

Need something like:

> minimum supported frame: 64 KiB
> recommended: 16 MiB
> maximum: implementation defined

to avoid implementation divergence and resource exhaustion.

#### 14. UUID specification

Specify:

- UUID version
- byte order
- wire order
- network representation

especially for UUIDv7.

#### 15. Transport bindings

The protocol is transport-independent, but the RFC should explicitly state:

> CRCP is transport-independent. Transport-specific bindings SHALL be defined by separate RFCs.

This prevents differing interpretations.

## Editorial Issue

The closing paragraph still says:

> **v1.3**

although the document is labeled **v1.6**.

This should be corrected before publication.

## Suggested future RFCs

The remaining work naturally separates into dedicated specifications:

- **RFC-0073** — Canonical Binary Encoding (CBE)
- **RFC-0074** — CRCP Security Profiles
- **RFC-0075** — CRCP Transport Bindings (TCP, QUIC, IPC)
- **RFC-0076** — CRCP Compression Profiles
- **RFC-0077** — CRCP Capability & Feature Registry
- **RFC-0078** — CRCP Message Schema Registry

Keeping these as separate RFCs will make the protocol easier to evolve while maintaining a stable wire format.

## Ratification recommendation

**Status:** Candidate for Final Ratification with Required Revisions

**Assessment:** **9.6/10**

The architecture is mature and internally coherent, and the document is close to production quality. The remaining work is concentrated in protocol completeness rather than architectural design. Before final ratification, the RFC should define payload schemas, registries for feature and algorithm identifiers, precise variable-length encoding rules, stream semantics, and deterministic handling of unknown protocol elements. Completing those areas would elevate RFC-0072 from a strong wire-format specification to a fully interoperable protocol standard suitable for independent implementations.