# Observability traceability

§14 defines `FederationEvent` fields; §§5,8 require event production; §16 requires standard-interface visibility. Event ID, AgreementID, source domains, timestamp, provenance and outcome are named. **Correlation ID, logical epoch in event, persistence durability, schema types, wire encoding, interface endpoint, metric cardinality, and replay participation rules are absent.** §7 requires logical epochs for provenance but does not connect them to §14 event schema. RFC-0018 and RFC-0046 are Draft in this checkout and no implementation mapping was found.
