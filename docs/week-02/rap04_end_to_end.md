# RAP-04 End-to-End (Week 2)

## Assertion
RAP-04: Administrative access configurations cannot be modified without approval.

## Evidence Object
admin_config_controls

## Evidence Type
configuration_state

## Evidence Acceptance
- change control constraints are present (e.g., protected settings)
- privileged scope for who can change is defined
- timestamp + source present

## Output Artifacts
- sample evidence: data/week-02/sample_evidence/admin_config_controls.sample.json
- normalized evidence: data/week-02/normalized_evidence/admin_config_controls.normalized.json

