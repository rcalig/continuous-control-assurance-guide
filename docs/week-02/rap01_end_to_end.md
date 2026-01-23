# RAP-01 End-to-End (Week 2)

## Assertion
RAP-01: No user accounts have permanent administrative privileges.

## Evidence Object
privileged_role_assignments

## Evidence Type
identity_inventory

## Evidence Acceptance
- principal_type identifies user vs service/role
- assignment_type identifies permanent vs temporary
- timestamp + source present

## Output Artifacts
- sample evidence: data/week-02/sample_evidence/privileged_role_assignments.sample.json
- normalized evidence: data/week-02/normalized_evidence/privileged_role_assignments.normalized.json

