# Stage 1 Prompts: Epic Planning

**Stage:** 1
**Purpose:** Epic planning and folder structure creation

---

## Starting Stage 1: Epic Planning

**User says:** "Help me develop the {epic_name} epic" or "Let's plan {epic_name}"

**Prerequisite:** User has created `feature-updates/{epic_name}.txt` with initial scratchwork notes.

**Agent MUST respond:**

```
I'm reading `stages/s1/s1_epic_planning.md` to ensure I follow the complete epic planning workflow...

**The guide requires:**
- Phase 1: Analyze epic request and codebase reconnaissance
- Phase 2: Propose feature breakdown to user (user MUST approve)
- Phase 3: Create epic folder structure
- Phase 4: Create initial epic_smoke_test_plan.md (placeholder)
- Phase 5: Create EPIC_README.md with Quick Reference Card
- Phase 6: Create epic_lessons_learned.md
- NO SKIPPING USER APPROVAL for feature breakdown
- If epic is large (>5 components): Propose feature breakdown early
- If epic is small (<3 components): Propose single-feature approach

**Prerequisites I'm verifying:**
✅ Epic request file exists: `feature-updates/{epic_name}.txt`
✅ Epic request contains user's initial notes
✅ Epic scope is clear from request

**I'll now proceed with Phase 1 (Analyze Epic Request & Reconnaissance)...**

**Creating initial EPIC_README.md status:**
- Current Stage: Stage 1 - Epic Planning
- Current Guide: stages/s1/s1_epic_planning.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "User must approve feature breakdown", "Create placeholder test plan", "No skipping reconnaissance"
- Next Action: Read epic request file and perform codebase reconnaissance

Starting Phase 1...
```

---

*For prompts for other stages, see the [prompts index](../prompts_reference_v2.md)*
