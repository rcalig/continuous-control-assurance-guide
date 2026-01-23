# POS-02 End-to-End (Week 2)

## Assertion
POS-02: No unsupported or end-of-life operating systems are in use.

## Evidence Object
patch_inventory_state

## Evidence Type
patch_inventory

## Evidence Acceptance
- is_supported present (true/false)
- os_name and os_version present
- timestamp + source present

## Output Artifacts
- sample evidence: data/week-02/sample_evidence/patch_inventory_state.sample.json
- normalized evidence: data/week-02/normalized_evidence/patch_inventory_state.normalized.json

