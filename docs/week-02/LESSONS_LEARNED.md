# Week 2 – Lessons Learned
## Continuous Control Assurance (Evidence-First, No Screenshots)

## Week 2 objective
Turn Week 1 assertions into something that can be proven continuously by defining:
- what evidence looks like (schemas)
- how we reject bad evidence early (validation)
- how we preserve provenance for replay (normalisation)

This week intentionally avoided:
- screenshots
- manual attestations
- point-in-time “audit packs”

---

## What I built (in plain terms)
- Evidence objects (e.g., `mfa_policy_state`, `patch_inventory_state`)
- JSON Schemas for each evidence object (minimum fields and structure)
- Sample evidence that conforms to each schema (mock API outputs)
- A Python validator that checks evidence matches schema
- A Python normaliser that wraps evidence with provenance (collected_at, collector version)

The end state is: evidence is “admissible” before it ever reaches policy evaluation.

---

## What I need to remember (non-negotiables)

### 1) Evidence quality must be enforced upfront
If evidence shape is not enforced early, everything downstream becomes untrustworthy.
- Bad input → bad evaluation → bad findings → wasted remediation effort

Schema validation is the quality gate.

---

### 2) One evidence object should serve multiple assertions
A key scaling insight:
- MFA-01, MFA-02, MFA-03 can reuse `mfa_policy_state`
- POS-01 and POS-02 can reuse `patch_inventory_state`
- RAP-01 and RAP-02 can reuse `privileged_role_assignments`

This keeps the program maintainable and avoids “evidence sprawl”.

---

### 3) Provenance matters as much as the payload
Normalisation adds:
- when evidence was collected
- what collector produced it
- what version of logic produced it

Without provenance, evidence cannot be replayed confidently for audits, SOCI, or investigations.

---

### 4) Avoid subjective words in evidence and schemas
The same Week 1 trap shows up in evidence design:
- “approved”
- “authorised”
- “verified”
- “on time”
- “within SLA”

If a field depends on human judgement, it is not a reliable evidence field.
Instead, store objective values:
- timestamps
- booleans
- enumerations
- lists of rules
- identifiers

---

### 5) Keep schemas minimal, then expand later
Over-designing schemas early causes friction and rework.
Minimum viable schemas should capture:
- identity (source, tenant/account)
- time (timestamp)
- scope (what the control applies to)
- the key state (boolean / list / event record)

---

## Where I struggled (and why)

### 1) Deciding what belongs in evidence vs policy logic
I initially wanted evidence to “prove everything”.
Lesson:
- evidence should capture facts
- policy evaluation should interpret those facts into PASS/FAIL

Example:
- evidence stores `allowed_factors`
- policy decides whether factors are “strong”

---

### 2) Designing fields that are future-proof
Some fields felt unnecessary at first (e.g., `bypass_rules`).
Lesson:
Capturing likely future needs early prevents schema churn later.

---

### 3) Avoiding “point-in-time thinking”
Even with JSON, it’s easy to slip into snapshot thinking.
Week 2 reminder:
- evidence must be replayable over time (timestamped + collectible repeatedly)
- “one perfect sample file” is not the goal
- repeatable collection is the goal (Week 3+)

---

## What went well (keep doing this)
- Reusing evidence objects across multiple assertions
- Keeping the evidence contract strict (schemas)
- Adding provenance via normalization
- Using Python as a thin “quality gate”, not a complex system

---

## Week 2 done means
- Every evidence object has a schema
- Every sample file validates successfully
- Normalized evidence exists and includes provenance
- Repo structure is consistent and predictable

---

## Next week (Week 3) focus
Turn normalised evidence into control results:
- Policy-as-Code (OPA/Rego or Python rules)
- PASS/FAIL per assertion + reason codes
- Findings output structure (machine-readable)
