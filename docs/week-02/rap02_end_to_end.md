# RAP-02 End-to-End (Week 2)

## Assertion
RAP-02: Administrative access is granted only through role-based mechanisms.

## Evidence Object
privileged_role_assignments

## Evidence Type
identity_inventory

## Evidence Acceptance
- assignments reference roles/groups (not direct admin flag)
- timestamp + source present

## Output Artifacts
- sample evidence: data/week-02/sample_evidence/privileged_role_assignments.sample.json
- normalized evidence: data/week-02/normalized_evidence/privileged_role_assignments.normalized.json

