# Consistency Loop: Spec Refinement Context

**Master Protocol:** See `consistency_loop_protocol.md`

**Context:** S2.P1.I3 Spec Refinement, S3.P2 Epic Documentation Refinement

---

## What's Being Validated

Specification documents including:
- spec.md (feature-level or epic-level)
- checklist.md (questions for user)
- Acceptance criteria sections
- Requirement sources and traceability

---

## What Counts as "Issue"

An issue in spec refinement context is any of:
- **Requirements without sources:** Requirement exists but no source (Epic/User Answer/Derived)
- **Scope creep:** Requirement not requested by user
- **Missing requirements:** User requested something not in spec
- **Gaps in spec coverage:** Incomplete requirement definitions
- **Inconsistencies between sections:** Contradictory requirements
- **Assumptions instead of confirmed facts:** Unverified claims in requirements
- **Vague requirements:** "Handle errors well" vs "Return HTTP 400 on invalid input"

---

## Fresh Eyes Patterns Per Round

### Round 1: Sequential Read + Traceability Check
**Pattern:**
1. Read spec.md top to bottom
2. Check every requirement has a source (Epic/User Answer/Derived)
3. Verify no scope creep (nothing user didn't ask for)
4. Check acceptance criteria are measurable

**Checklist (EMBEDS Gate 2):**
- [ ] Every requirement has source (Epic/User Answer/Derived)
- [ ] No scope creep (nothing user didn't ask for)
- [ ] No missing requirements (everything user asked for is included)
- [ ] All requirements trace to validated sources
- [ ] Zero assumptions in spec

### Round 2: Reverse Read + Gap Detection
**Pattern:**
1. Read spec.md in reverse order (bottom to top)
2. Look for gaps between requirements
3. Check for implicit vs explicit requirements
4. Verify acceptance criteria completeness

**Checklist:**
- [ ] No gaps between requirements (complete coverage)
- [ ] All implicit requirements made explicit
- [ ] Acceptance criteria for each requirement
- [ ] Clear "done" definition for each requirement
- [ ] No vague language ("handle errors" → specific error codes)

### Round 3: Random Spot-Checks + Alignment
**Pattern:**
1. Random spot-check 5 requirements
2. Verify each aligns with DISCOVERY.md findings
3. Check for consistency with epic intent
4. Verify no contradictions between requirements

**Checklist:**
- [ ] Requirements align with DISCOVERY.md
- [ ] Epic intent preserved
- [ ] No contradictions found
- [ ] All checklist questions resolved
- [ ] Ready for user approval (Gate 3)

---

## Specific Criteria (EMBEDS Gate 2)

**All of these MUST pass for loop to exit:**
- [ ] Every requirement has source (Epic/User Answer/Derived)
- [ ] No scope creep (nothing user didn't ask for)
- [ ] No missing requirements (everything user asked for is included)
- [ ] All requirements trace to validated sources
- [ ] Zero assumptions in spec
- [ ] All acceptance criteria are measurable
- [ ] No vague language remains
- [ ] Checklist.md has all QUESTIONS (agents don't mark [x])

---

## Example Round Sequence

```
Round 1: Sequential read + traceability
- Read spec.md top to bottom
- Check: Requirement R5 has no source, R7 is vague ("handle errors")
- Fix: Add source for R5, make R7 specific
- Continue to Round 2

Round 2: Reverse read + gap detection
- Read spec.md bottom to top
- Check: Gap between R3 and R4 (missing error handling requirement)
- Fix: Add error handling requirement with source
- Continue to Round 3

Round 3: Spot-checks + alignment
- Random spot-check 5 requirements
- Check: 0 issues found → Continue (count = 1 clean)

Round 4: Repeat validation
- Check: 0 issues found → Continue (count = 2 clean)

Round 5: Final sweep
- Check: 0 issues found → PASSED (count = 3 consecutive clean)
```

---

## Common Issues in Spec Refinement Context

1. **Missing sources:** Requirement exists but no "(Source: Epic/User Answer/Derived)"
2. **Scope creep:** Added feature user didn't ask for
3. **Vague requirements:** "System should be fast" → "Response time < 200ms"
4. **Missing acceptance criteria:** Requirement has no "done" definition
5. **Contradictory requirements:** R1 says X, R5 says NOT X
6. **Assumptions:** "User probably wants Y" → Verify with user

---

## Integration with Stages

**S2.P1.I3 Spec Refinement (Feature-Level):**
- Use this protocol for feature spec.md
- Embeds Gate 2 (Spec-to-Epic Alignment)
- Must pass before Gate 3 (User Approval)

**S3.P2 Epic Documentation Refinement:**
- Use this protocol for epic-level documentation
- Validate EPIC_README.md, epic_smoke_test_plan.md
- Must pass before S3.P3 (Gate 4.5 - User Approval)

---

## Exit Criteria Specific to Spec Refinement

**Can only exit when ALL true:**
- [ ] 3 consecutive rounds found zero issues
- [ ] Gate 2 criteria passed (embedded)
- [ ] All requirements have sources
- [ ] Zero scope creep
- [ ] All acceptance criteria measurable
- [ ] Ready for user approval (Gate 3 or Gate 4.5)

---

**Remember:** Follow all 7 principles from master protocol. This guide only specifies HOW to apply them in spec refinement context, not WHETHER to apply them.
