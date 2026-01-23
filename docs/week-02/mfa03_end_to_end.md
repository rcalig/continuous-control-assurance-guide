
# MFA-03 End-to-End (Week 2)

## Assertion
MFA-03: Only cryptographically strong authentication factors are permitted.

## Evidence Object
mfa_policy_state

## Evidence Type
configuration_state

## Evidence Acceptance
- allowed_factors present
- no weak factors included (policy evaluation later)
- timestamp + source present

## Output Artifacts
- sample evidence: data/week-02/sample_evidence/mfa_policy_state.sample.json
- normalized evidence: data/week-02/normalized_evidence/mfa_policy_state.normalized.json
