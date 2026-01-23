# MFA-04 End-to-End (Week 2)

## Assertion
MFA-04: All changes to MFA configuration are logged centrally.

## Evidence Object
mfa_audit_events

## Evidence Type
audit_events

## Evidence Acceptance
- events include actor, action, target, result, timestamp
- source indicates central log/audit stream
- events are continuous (freshness enforced later)

## Output Artifacts
- sample evidence: data/week-02/sample_evidence/mfa_audit_events.sample.json
- normalized evidence: data/week-02/normalized_evidence/mfa_audit_events.normalized.json
