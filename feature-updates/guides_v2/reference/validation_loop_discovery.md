# Validation Loop: Discovery Context

**Master Protocol:** See `validation_loop_protocol.md`

**Context:** S1.P3 Discovery Phase, S2.P1.I1 Feature Discovery

---

## What's Being Validated

Discovery documents and research findings including:
- DISCOVERY.md (epic-level)
- RESEARCH_NOTES.md (feature-level)
- Integration points identified
- External dependencies researched
- User questions answered

---

## What Counts as "Issue"

An issue in discovery context is any of:
- **Missing research areas:** Components mentioned in epic but not researched
- **Unanswered questions:** Questions posed but not resolved
- **Assumptions instead of facts:** "Probably works" vs "Verified works"
- **Gaps in integration understanding:** Integration points not fully explored
- **Incomplete dependency analysis:** External libraries not verified compatible
- **Missing error scenarios:** Edge cases not considered

---

## Fresh Eyes Patterns Per Round

### Round 1: Sequential Read + Completeness Check
**Pattern:**
1. Read discovery document top to bottom
2. Check against epic requirements (all components mentioned?)
3. Verify all questions have answers
4. Check for TODO or placeholder text

**Checklist:**
- [ ] All epic components researched
- [ ] All integration points identified
- [ ] All external dependencies documented
- [ ] All user questions answered
- [ ] No assumptions remain (all verified)

### Round 2: Different Order + Integration Verification
**Pattern:**
1. Read in different folder/file order (reverse, by component, etc.)
2. Focus on integration points
3. Verify external library compatibility claims
4. Check user questions were actually answered (not just marked resolved)

**Checklist:**
- [ ] Integration points between features clear
- [ ] External library versions compatible
- [ ] API contracts understood
- [ ] Data flow documented
- [ ] All "verified" claims are actually verified

### Round 3: Random Spot-Checks + Alignment
**Pattern:**
1. Random spot-check 5 epic requirements
2. Verify each has corresponding research
3. Check alignment with epic intent
4. Look for research that's nice-to-have vs necessary

**Checklist:**
- [ ] All mandatory research complete
- [ ] No over-researching (scope appropriate)
- [ ] Epic intent preserved
- [ ] User questions fully resolved
- [ ] Ready to proceed to specification

---

## Specific Criteria

**All of these MUST pass for loop to exit:**
- [ ] All components mentioned in epic are researched
- [ ] All integration points identified and documented
- [ ] All user questions answered (not just acknowledged)
- [ ] Zero assumptions remain (everything verified)
- [ ] All external dependencies checked for compatibility
- [ ] No TODO markers or placeholders
- [ ] Ready to write spec.md (all info needed is present)

---

## Example Round Sequence

```text
Round 1: Sequential read + completeness
- Read DISCOVERY.md top to bottom
- Check: Missing research on authentication flow, 2 assumptions about API
- Fix: Research authentication, verify API compatibility
- Continue to Round 2

Round 2: Different order + integration focus
- Read by component (not sequential)
- Check: Integration point between Feature 1 and Feature 2 unclear
- Fix: Clarify integration point with code inspection
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

## Common Issues in Discovery Context

1. **Assumptions:** "Probably compatible" → Verify actual compatibility
2. **Missing components:** Epic mentions Feature X, no research on X → Research X
3. **Unanswered questions:** User asked about Y, question not resolved → Answer Y
4. **Vague integration:** "Features will integrate" → How? What data? What API?
5. **Placeholder research:** "TODO: Check library" → Actually check library

---

## Integration with Stages

**S1.P3 Discovery Phase:**
- Use this protocol for epic-level discovery
- Validate DISCOVERY.md has all epic components researched
- Must pass before proceeding to S1.P4 (feature breakdown)

**S2.P1.I1 Feature Discovery:**
- Use this protocol for feature-level discovery
- Validate RESEARCH_NOTES.md for each feature
- Includes Gate 1 (Research Completeness Audit) embedded
- Must pass before proceeding to S2.P1.I2

---

## Exit Criteria Specific to Discovery

**Can only exit when ALL true:**
- [ ] 3 consecutive rounds found zero issues
- [ ] All epic/feature components researched
- [ ] All questions answered
- [ ] Zero assumptions
- [ ] Integration points clear
- [ ] Ready for next stage (S1.P4 or S2.P1.I2)

---

**Remember:** Follow all 7 principles from master protocol. This guide only specifies HOW to apply them in discovery context, not WHETHER to apply them.
