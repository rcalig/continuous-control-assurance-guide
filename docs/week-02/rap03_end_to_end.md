# RAP-03 End-to-End (Week 2)

## Assertion
RAP-03: All administrative role assignments are logged centrally.

## Evidence Object
admin_role_assignment_events

## Evidence Type
audit_events

## Evidence Acceptance
- events include actor, action, target, result, timestamp
- action set includes role assignment changes
- source indicates central log/audit stream

## Output Artifacts
- sample evidence: data/week-02/sample_evidence/mfa_audit_events.sample.json (contains admin role events too)
- normalized evidence: data/week-02/normalized_evidence/admin_role_assignment_events.normalized.json

