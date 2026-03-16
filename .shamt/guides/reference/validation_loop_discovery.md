# Validation Loop: Discovery

**Extends:** Master Validation Loop Protocol
**See:** `reference/validation_loop_master_protocol.md`

**Applicable Stages:**
- S1.P3: Epic Discovery Phase
- S2.P1.I1: Feature Discovery (initial research)

**Version:** 2.1 (Adversarial challenge dimensions + success criteria)
**Last Updated:** 2026-03-08

---

🚨 **BEFORE STARTING: Read the Hard Stop section at the top of `reference/validation_loop_master_protocol.md`** 🚨

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
- **Zero questions asked of user:** if no questions have been posed during Discovery, treat this as a signal of under-questioning. Justify absence of questions explicitly, or treat it as an open issue.
- **Alternative interpretations not considered:** if the request has only been read one way, without documenting other plausible interpretations and why they were ruled out.
- **Adjacent systems or workflows not assessed:** any system, file, workflow, or user role that could be affected but hasn't been examined or explicitly ruled out.
- **Implementation decisions not surfaced:** high-level choices that will need to be made during implementation (approach, API contracts, schema design, error handling strategy) that haven't been flagged as open questions or resolved. Note: this covers high-level architectural choices, not low-level implementation details (those belong in feature specs).
- **Non-functional requirements absent:** no consideration of performance, security, backward compatibility, or other constraints any production implementation should address.
- **Success criteria not defined:** no concrete description of what "done" looks like from the user's perspective. How will the user verify the epic was implemented correctly? What is the ideal end state in concrete terms?

---

## Fresh Eyes Patterns Per Round

### Adversarial Challenge Rules

Each round includes an **Adversarial Challenge** checklist — questions the agent must ask itself to surface unknowns that backward-looking checks miss.

> **Note:** The per-round Adversarial Challenge checklists in this file (shown in Rounds 1–3 below) serve as the Adversarial Self-Check for Discovery contexts — they satisfy and extend the master protocol's generic 5-question check. No additional self-check step is required in Discovery rounds; the per-round challenges replace it.

> **When any adversarial challenge item returns "No":** Document what is missing as an issue, add any unasked questions to the Pending Questions table, and treat this round as NOT clean (clean counter resets to 0).

---

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

**Adversarial Challenge:**
- [ ] Did I work through all 6 question brainstorm categories in DISCOVERY.md, and either list questions or write a one-line justification for each category?
- [ ] Have I asked the user at least one clarifying question? If not, what am I assuming that should be verified instead?
- [ ] Have I identified any adjacent systems or affected workflows not mentioned in the request?
- [ ] Have I surfaced implementation decisions that will require choices — as open questions or confirmed decisions?
- [ ] Have I considered non-functional constraints (performance, security, compatibility)?
- [ ] Have I documented what success looks like — how the user will concretely verify the epic is done?

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

**Adversarial Challenge:**
- [ ] What could go wrong with the current approach? Are the main risks documented?
- [ ] Are there user-facing edge cases or workflow variations not yet covered?
- [ ] Have I assumed any user preference that should be verified rather than decided unilaterally? (If yes, add a question to Pending Questions and present it to the user immediately.)

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

**Adversarial Challenge:**
- [ ] Would a skeptical reviewer find any obvious missing angle in this document?
- [ ] Is every "out of scope" item either (a) explicitly stated in the epic request, or (b) confirmed by the user in a Resolved Question? (If not, present to user for confirmation before this round can be clean.)
- [ ] Has the user confirmed what success looks like — do they agree on how to verify the epic is done correctly?

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
- [ ] 3 consecutive rounds found zero issues, OR user opted to stop at the 2-round checkpoint (see master protocol Exit Criteria)
- [ ] All epic/feature components researched
- [ ] All questions answered
- [ ] Zero assumptions
- [ ] Integration points clear
- [ ] Ready for next stage (S1.P4 or S2.P1.I2)
- [ ] Question brainstorm categories in DISCOVERY.md are complete — each has questions listed OR an explicit one-line justification for why none apply
- [ ] All questions asked during Discovery have been answered (Resolved Questions table not empty; Pending Questions table empty)
- [ ] All implementation decisions requiring user input have been resolved or explicitly deferred with user agreement
- [ ] Non-functional requirements considered and either addressed or explicitly ruled out with user agreement
- [ ] Success criteria confirmed with user
- [ ] Adversarial challenge checklist completed in the final round with no new issues found

---

**Remember:** Follow all 7 principles from master protocol. This guide only specifies HOW to apply them in discovery context, not WHETHER to apply them.
