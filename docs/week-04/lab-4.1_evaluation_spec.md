# Lab 4.1 — Evaluation Specification (Week 4)

## Purpose
Define how Week 1 atomic control assertions will be evaluated using Week 3 normalised AWS evidence.
This document defines the evaluation contract only. No control outcomes are produced in Lab 4.1.

## Evidence Inputs (Week 3 Normalised)
All evaluators must read evidence from these paths:

- data/week-03/aws_normalised_evidence/iam_users.normalized.json
- data/week-03/aws_normalised_evidence/iam_roles.normalized.json
- data/week-03/aws_normalised_evidence/iam_policies.normalized.json
- data/week-03/aws_normalised_evidence/cloudtrail_trails.normalized.json
- data/week-03/aws_normalised_evidence/cloudtrail_status.normalized.json
- data/week-03/aws_normalised_evidence/security_groups.normalized.json

## Output Location (Week 4 Results)
All evaluators must write results to:
- data/week-04/evaluation_results/

Each result file must be JSON and include:
- assertion_id
- evaluated_at (UTC)
- result: PASS | FAIL | NOT_APPLICABLE | INFORMATIONAL
- reason (machine-readable, deterministic)
- affected_objects (array)
- evidence_refs (array of evidence filenames)

---

# Assertions In Scope (Week 4)

## RAP-02: Administrative access is granted only through role-based mechanisms.
### Evaluation intent
Detect any direct administrative privilege assigned to user accounts outside role-based mechanisms.

### Evidence required
- iam_users.normalized.json
- iam_policies.normalized.json
- iam_roles.normalized.json (optional for enrichment)

### Evaluation logic (deterministic)
1. Identify "admin-equivalent" policy attachments to IAM users.
2. FAIL if any IAM user has admin-equivalent privileges directly attached.
3. PASS if no IAM users have direct admin-equivalent privileges.

### Output contract
- assertion_id: RAP-02
- affected_objects: list of IAM usernames with direct admin privileges
- reason:
  - FAIL: "Direct admin-equivalent privilege attached to user(s)"
  - PASS: "No direct admin-equivalent privilege attached to any user"

### Notes / assumptions
- Definition of "admin-equivalent" will be encoded explicitly in code (Week 4 Lab 4.2).
- No judgement of whether admin access is justified. Only the mechanism is tested.

---

## MFA-01: All privileged user accounts require multi-factor authentication for interactive access.
### Evaluation intent
Ensure privileged identities cannot perform interactive access without MFA.

### Evidence required
- iam_users.normalized.json

### Dependency
Privileged users are defined as:
- Users identified as admin/privileged by the RAP-02 evaluator logic.

### Evaluation logic (deterministic)
1. Build the privileged user set.
2. For each privileged user, check MFA device presence/enabled state.
3. FAIL if any privileged user lacks MFA enabled.
4. PASS if all privileged users have MFA enabled.

### Output contract
- assertion_id: MFA-01
- affected_objects: privileged IAM usernames without MFA enabled
- reason:
  - FAIL: "Privileged user(s) lack MFA enabled"
  - PASS: "All privileged users have MFA enabled"

### Notes / assumptions
- This evaluates MFA state for IAM users only (AWS context). It does not evaluate external IdP MFA enforcement.

---

## RAP-03: All administrative role assignments are logged centrally.
### Evaluation intent
Verify that central logging is enabled for administrative activity.

### Evidence required
- cloudtrail_trails.normalized.json
- cloudtrail_status.normalized.json

### Evaluation logic (deterministic)
1. Confirm at least one CloudTrail trail exists.
2. Confirm logging is enabled (CloudTrail status indicates logging).
3. FAIL if CloudTrail is absent or logging is disabled.
4. PASS if CloudTrail exists and logging is enabled.

### Output contract
- assertion_id: RAP-03
- affected_objects:
  - if FAIL: ["cloudtrail"]
  - if PASS: []
- reason:
  - FAIL: "CloudTrail missing or logging disabled"
  - PASS: "CloudTrail enabled and logging active"

### Notes / assumptions
- This lab proves logging enablement. It does not yet prove log delivery to a SIEM destination.

---

# Assertions Out of Scope (Explicitly Deferred)

## RAP-04: Administrative access configurations cannot be modified without approval.
Reason deferred: requires workflow/approval evidence and change management integration.

## MFA-03: Only cryptographically strong authentication factors are permitted.
Reason deferred: requires factor metadata from an identity provider, not visible in AWS IAM evidence.

## POS-01 to POS-04 (Patch Operating Systems)
Reason deferred: Week 3 did not collect host patch evidence; requires SSM/endpoint/vuln telemetry.

---

# Partial / Informational Assertions (Week 4 may label as INFORMATIONAL)

## RAP-01: No user accounts have permanent administrative privileges.
Week 4 can detect direct admin privileges but cannot prove time-bounded access without JIT/approval evidence.

## MFA-02: MFA enforcement cannot be bypassed for privileged user accounts.
Week 4 can detect absence of MFA but not all bypass mechanisms without IdP/conditional access evidence.

## MFA-04: All changes to MFA configuration are logged centrally.
Week 4 can show CloudTrail is enabled but not prove specific MFA change events are monitored.
