# Week 1 – Lessons Learned  
## Continuous Control Assurance (Essential Eight + SOCI)

## Purpose
This document captures key lessons from Week 1 to ensure that
mistakes are not repeated and foundational decisions remain consistent
as the program progresses toward continuous, automated assurance.

Week 1 focused on **control decomposition, base assertions, maturity logic,
and SOCI alignment**. This was the most conceptually difficult week and
sets the quality ceiling for all future automation.

---

## What I Need to Remember (Non-Negotiables)

### 1. Atomic Control Assertions = Base Assertions
- Atomic control assertions define **what must always be true**
- They do **not change** across maturity levels
- Maturity strengthens **scope, enforcement, and monitoring only**

If I ever feel tempted to rewrite base assertions for maturity,
I am doing it wrong.

---

### 2. Controls Are Outcomes, Not Activities
Good controls describe **truths about system state**, not actions.

Bad (activity-based):
- "Review admin access quarterly"
- "Ensure patches are applied"

Good (outcome-based):
- "No user accounts have permanent administrative privileges"
- "Supported operating systems have current security patches installed"

Continuous assurance only works with outcome-based controls.

---

### 3. Subjective Language Breaks Automation
Words that caused problems:
- approved
- authorised
- verified
- on time
- SLA (without technical definition)

These terms introduce **human judgement** and block automation.

Controls must be provable using:
- configuration
- logs
- system state
- events

If a human must decide pass/fail, the assertion is not ready.

---

### 4. One Assertion = One Failure Mode
Several early assertions bundled multiple concepts together
(e.g. enforcement + logging).

Key rule learned:
> If two things can fail independently, they must be separate assertions.

This rule is critical for:
- Policy as Code
- Accurate findings
- Clean remediation tracking

---

### 5. Maturity Does NOT Introduce New Intent
Essential Eight maturity:
- does not create new controls
- does not change risk intent
- represents stronger and more resilient enforcement

Maturity is implemented by:
- expanding scope
- removing bypass paths
- increasing monitoring and detection

This mirrors NIST base controls + enhancements, even though
Essential Eight does not explicitly say this.

---

## Where I Struggled (And Why)

### 1. Separating Base Assertions from Maturity
Initial confusion:
- I tried to encode “good practice” directly into base assertions
- This collapsed maturity levels and made later strengthening impossible

Resolution:
- Base assertions were simplified to the minimum defensible truth
- Maturity levels were used to add strength, not new meaning

Lesson:
> Simpler base assertions make stronger maturity models.

---

### 2. Letting Audit Language Leak In
Early drafts included:
- governance terms
- approval concepts
- process-oriented wording

This came from traditional audit habits.

Resolution:
- Reframed everything as technical conditions
- Treated controls as engineering constraints, not audit questions

Lesson:
> This program is not an audit checklist. It is a control system.

---

### 3. Overlapping Controls (Especially MFA)
Initial MFA assertions overlapped heavily:
- MFA for all users
- MFA for privileged users

This made maturity mapping messy.

Resolution:
- Identified the **true base condition** (privileged access)
- Pushed broader coverage into maturity levels

Lesson:
> Base assertions should feel almost “too small”.
> That is intentional.

---

### 4. Mixing Control Families (Patch vs Vulnerability)
I initially mixed:
- OS patching
- vulnerability remediation SLAs

Resolution:
- Kept Patch Operating Systems focused on patch state
- Left vulnerability prioritisation out of Week 1

Lesson:
> Mixing control families early creates automation debt later.

---

## What I Got Right (Important Confidence Builders)

- Atomic assertions are now **binary, testable, and tool-agnostic**
- Essential Eight intent is preserved without copying ACSC wording
- SOCI Act requirements are met without adding duplicate controls
- Maturity logic is consistent across all control families
- Repo structure supports Policy as Code and continuous assurance

This confirms the engineering-first approach is sound.

---

## How This Changes How I Think About GRC

Before:
- Controls were documentation artifacts
- Maturity was descriptive
- Evidence was point-in-time

After Week 1:
- Controls are executable truths
- Maturity is enforcement strength
- Evidence is continuous and replayable

This mental shift is required before touching AWS, Python,
or Policy as Code.

---

## Warnings for Future Weeks

- Do not reintroduce screenshots
- Do not reintroduce manual attestations
- Do not hard-code maturity into base assertions
- Do not let SOCI create parallel control sets
- Do not optimise evidence collection before assertions are correct

Any of the above will require rework.

---

## Ready for Week 2 When

I should only proceed to Week 2 if:
- Every assertion feels boring but precise
- I can explain each assertion without referencing a policy
- I can imagine how code would test each assertion
- I am comfortable saying "this runs continuously"

Week 1 is complete only if the foundation is stable.

