# S2b.5 Prompts: Specification Validation

**Stage:** 2b.5
**Purpose:** Specification validation and checklist self-resolution

---

## Starting S2b.5: Specification Validation

**User says:** "proceed" after S2.P2 completion, or agent transitions automatically

**Prerequisite:** S2.P2 complete (Phase 2.5 Spec-to-Epic Alignment Check PASSED)

**Agent MUST respond:**

```
I'm reading `stages/s2/s2_p2_5_spec_validation.md` to ensure I follow the complete validation workflow...

**The guide requires:**
- **🚨 CRITICAL: ASSUME EVERYTHING IS WRONG**
  - Treat spec.md as hypotheses to validate (not facts)
  - Treat checklist.md as assumptions to research (not final questions)
  - Question every claim, requirement, and implementation detail
  - Validate with additional evidence from codebase
- Phase 2.75: Deep research validation beyond Phase 1 research
- Self-resolve checklist questions where possible (reduce user burden)
- Identify new questions through comprehensive discovery
- Flag multi-approach questions for user decision
- Update spec immediately with validation findings

**Prerequisites I'm verifying:**
✅ S2.P2 complete: Phase 2.5 Spec-to-Epic Alignment Check PASSED
✅ spec.md exists with requirements and traceability
✅ checklist.md exists with open questions
✅ Research foundation exists from Phase 1

**I'll now proceed with Phase 2.75 (Specification Validation)...**

**Updating feature README Agent Status:**
- Current Phase: VALIDATION_PHASE
- Current Guide: stages/s2/s2_p2_5_spec_validation.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "Assume everything is wrong until validated", "Self-resolve checklist questions through research", "Deep investigation for new questions", "Flag multi-approach questions for user decision"
- Next Action: Begin validation of all spec claims

Starting Phase 2.75...
```

---

*For prompts for other stages, see the [prompts index](../prompts_reference_v2.md)*
