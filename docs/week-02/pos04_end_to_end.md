# POS-04 End-to-End (Week 2)

## Assertion
POS-04: Patch failures are detected and recorded.

## Evidence Object
patch_failure_events

## Evidence Type
audit_events

## Evidence Acceptance
- events include host, failure type, timestamp, result
- source indicates central log/audit stream
- events are continuous (freshness enforced later)

## Output Artifacts
- sample evidence: data/week-02/sample_evidence/patch_failure_events.sample.json
- normalized evidence: data/week-02/normalized_evidence/patch_failure_events.normalized.json

