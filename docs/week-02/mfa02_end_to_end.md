
# MFA-02 End-to-End (Week 2)

## Assertion
MFA-02: MFA enforcement cannot be bypassed for privileged user accounts.

## Evidence Object
mfa_policy_state

## Evidence Type
configuration_state

## Evidence Acceptance
- privileged scope defined
- bypass_rules present (empty or disabled)
- timestamp + source present

## Output Artifacts
- sample evidence: data/week-02/sample_evidence/mfa_policy_state.sample.json
- normalized evidence: data/week-02/normalized_evidence/mfa_policy_state.normalized.json
