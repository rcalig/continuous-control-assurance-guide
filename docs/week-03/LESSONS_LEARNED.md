# Week 3 – Lessons Learned  
AWS Evidence Collection & Normalisation

## Purpose

This document captures the key lessons from Week 3 of the Continuous Control Assurance program, focused on collecting and normalising real control evidence from AWS without screenshots or human judgement.

Week 3 shifted the work from *control definition* and *evidence modelling* into **live system interaction**, which exposed practical challenges that do not appear in purely conceptual design.

The primary outcome of this week was not “checking controls,” but proving that **trustworthy, replayable evidence can be collected programmatically and prepared for automated evaluation**.

---

## What Went Well (Foundational Wins)

### 1. Evidence Must Be Treated as a First-Class Artifact

Collecting AWS evidence via CLI immediately reinforced that evidence is not a by-product of assessment. It is a primary system output that must be:

- captured consistently
- preserved in raw form
- enriched with context and provenance
- reproducible on demand

This validated the program’s insistence that evidence engineering must come *before* policy-as-code or evaluation logic.

---

### 2. Raw Evidence and Normalised Evidence Serve Different Purposes

Separating raw AWS outputs from normalised evidence artifacts proved critical.

- Raw evidence represents **ground truth**
- Normalised evidence represents **assurance-ready context**

This separation ensures that:
- no interpretation contaminates raw data
- assurance logic can evolve without recollecting evidence
- audits and disputes can always reference the original payload

This distinction is often blurred in traditional GRC processes and becomes a source of credibility risk later.

---

### 3. Normalisation Is About Trust, Not Convenience

The Python normalisation scripts did not make the data “simpler” or “cleaner” for humans. They made it **defensible for machines and auditors**.

Adding fields such as:
- `collected_at`
- `collector`
- `collector_version`
- `cloud_account`
- `region`

transformed anonymous JSON into evidence that can answer the questions:
- when was this captured?
- by what mechanism?
- from which environment?
- under which assumptions?

This is a non-negotiable requirement for continuous assurance.

---

### 4. Evidence Collection Exposes Real-World Friction Early (Which Is Good)

Working with AWS CLI surfaced several practical realities:
- region scoping matters
- multi-region services still have a home region
- permissions and access are as important as control intent
- evidence collection fails loudly if assumptions are wrong

Encountering these issues in Week 3 is a success, not a failure. It confirms that the program is grounded in real system behaviour, not idealised diagrams.

---

## Key Challenges (And Why They Matter)

### 1. Region Awareness Is Mandatory for Evidence Accuracy

The CloudTrail `TrailNotFoundException` demonstrated that:
- evidence collection is context-sensitive
- APIs may succeed in one region and fail in another
- multi-region services still have authoritative locations

Lesson:
> Evidence must always carry region and account metadata, or it risks being misleading or unusable.

This directly justified the inclusion of `region` and `cloud_account` in the normalised schema.

---

### 2. Git Hygiene Is Part of Assurance Engineering

Merge conflicts, divergent branches, and `.DS_Store` pollution were not just “git problems.” They highlighted that:

- evidence pipelines are code
- code must be reproducible
- repositories must remain clean and deterministic

Poor repo hygiene undermines confidence in automation just as much as poor control logic.

Lesson:
> Operational discipline (branching, ignoring OS artifacts, resolving conflicts cleanly) is part of assurance credibility.

---

### 3. Attaching Assertions Early Is About Traceability, Not Evaluation

Linking evidence to assertion IDs during normalisation felt premature at first. However, this proved valuable for:

- maintaining lineage between control intent and system state
- enabling future evaluation without retrofitting metadata
- preventing “orphaned” evidence with unclear purpose

Lesson:
> Evidence should always know *why* it exists, even before it is evaluated.

---

## What Was Explicitly Avoided (Correctly)

### 1. No PASS / FAIL Logic

Resisting the urge to implement evaluation logic confirmed the importance of architectural sequencing.

If evaluation had been added prematurely:
- evidence design would have been biased
- failure modes would be hidden
- future maturity layering would be harder

Week 3 correctly stopped at “ready for evaluation.”

---

### 2. No Screenshots or Manual Interpretation

AWS CLI evidence eliminated:
- subjective judgement
- point-in-time screenshots
- narrative explanations of state

This reinforced the program’s core principle:
> If a control cannot be evidenced programmatically, it cannot be continuously assured.

---

## Mental Model Shift (Most Important Outcome)

Before Week 3:
- evidence felt like something requested *after* controls were designed

After Week 3:
- evidence is the **primary input**
- controls are hypotheses tested against evidence
- assurance becomes a data pipeline, not a checklist

This shift is essential before moving into policy-as-code.

---

## Warnings for Future Weeks

- Do not retrofit evidence fields later; evolve schemas intentionally
- Do not allow evaluation logic to mutate raw evidence
- Do not optimise for dashboards before confidence is earned
- Do not assume cloud APIs behave uniformly across regions or services

Any of the above will introduce hidden assurance debt.

---

## Readiness Check Before Proceeding to Week 4

Week 4 can proceed safely only if:

- raw evidence is preserved unchanged
- normalised evidence includes provenance and context
- evidence can be recollected deterministically
- assertion IDs are consistently referenced
- repository structure is stable

If any of these are not true, Week 3 should be revisited.

---

## Summary

Week 3 validated the most fragile part of any continuous control assurance program: **evidence integrity**.

By successfully collecting and normalising live AWS configuration data, the program now has a solid, defensible foundation for policy-as-code, automated evaluation, and continuous assurance.

Everything that follows depends on this layer being correct.
