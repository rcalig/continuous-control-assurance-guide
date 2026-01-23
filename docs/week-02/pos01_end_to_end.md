# POS-01 End-to-End (Week 2)

## Assertion
POS-01: Supported operating systems have current security patches installed within a defined timeframe.

## Evidence Object
patch_inventory_state

## Evidence Type
patch_inventory

## Evidence Acceptance
- last_patch_date present
- patch_compliance_state present
- timestamp + source present

## Output Artifacts
- sample evidence: data/week-02/sample_evidence/patch_inventory_state.sample.json
- normalized evidence: data/week-02/normalized_evidence/patch_inventory_state.normalized.json

