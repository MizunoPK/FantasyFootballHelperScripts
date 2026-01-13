# Phase Transition Prompts Reference (v2) - Router

**Version:** 2.1
**Last Updated:** 2026-01-04
**Purpose:** MANDATORY prompts for stage transitions

---

## ⚠️ CRITICAL: When to Use These Prompts

**You MUST use these prompts when:**
- Starting ANY stage (S1-S10)
- Starting ANY stage phase (S5, S6, S7, S8.P1, S8.P2)
- Resuming work after session compaction
- Creating a bug fix
- Creating a missed requirement
- Starting debugging protocol
- Encountering problems or blockers

**These prompts are MANDATORY. Do NOT skip them.**

**Why prompts are required:**
1. Proves you READ the guide (not working from memory)
2. Lists critical requirements for accountability
3. Verifies prerequisites before starting
4. Updates README Agent Status for persistence
5. Prevents guide abandonment (documented 40% failure rate without prompts)

---

## How to Use This Router

**This file has been optimized for agent usability.** Instead of searching through 1,474 lines, prompts are now organized by category:

### Stage Transition Prompts

**[S1: Epic Planning](prompts/stage_1_prompts.md)**
- Starting S1: Epic Planning

**[S2: Feature Deep Dive](prompts/stage_2_prompts.md)**
- Starting S2: Feature Deep Dive

**[S2b.5: Specification Validation](prompts/stage_2b5_prompts.md)**
- Starting S2b.5: Specification Validation

**[S3: Cross-Feature Sanity Check](prompts/stage_3_prompts.md)**
- Starting S3: Cross-Feature Sanity Check

**[S4: Epic Testing Strategy](prompts/stage_4_prompts.md)**
- Starting S4: Epic Testing Strategy

**[S5: Feature Implementation](prompts/stage_5_prompts.md)**
- Starting S5: Implementation Planning (Round 1)
- Starting S5: Implementation Planning (Round 2)
- Starting S5 Round 3 Part 1: Implementation Planning (Preparation)
- Starting S5 Round 3 Part 2: Implementation Planning (Final Gates)
- Starting S6: Implementation
- Starting S7 (Phase 1): Smoke Testing
- Starting S7 (Phase 2): QC Rounds
- Starting S7 (Phase 3): Final Review
- Starting S8.P1: Cross-Feature Alignment
- Starting S8.P2: Epic Testing Plan Update

**[S9: Epic Final QC](prompts/stage_6_prompts.md)**
- Starting S9: Epic Final QC

**[S10: Epic Cleanup](prompts/stage_7_prompts.md)**
- Starting S10: Epic Cleanup
- Starting S10.P1: Guide Update from Lessons Learned (see prompts/guide_update_prompts.md)

### Special Workflow Prompts

**[Special Workflows](prompts/special_workflows_prompts.md)**
- Creating a Bug Fix
- Creating Missed Requirement
- Starting Debugging Protocol
- Resuming In-Progress Epic

### Problem Situation Prompts

**[Problem Situations](prompts/problem_situations_prompts.md)**
- When Tests Are Failing
- When Stuck or Blocked
- When Confidence < Medium
- Presenting Options to User
- Asking for Clarification

---

## Quick Reference: Which Prompt File?

**If you're starting a stage:**
→ Use the corresponding `stage_X_prompts.md` file

**If you're dealing with bugs, missed requirements, or debugging:**
→ Use `special_workflows_prompts.md`

**If you're stuck, have failing tests, or need user input:**
→ Use `problem_situations_prompts.md`

**If you're resuming after session compaction:**
→ Use `special_workflows_prompts.md` → "Resuming In-Progress Epic"

---

## How to Use These Prompts

**STEP 1: Read the guide FIRST**
```
Use Read tool to load the ENTIRE guide for the stage you're starting
```

**STEP 2: Use the appropriate prompt from the file above**
```
Navigate to the correct prompt file using the links above
Read the prompt template for your situation
Fill in {placeholders} with actual values
Include ALL sections (requirements, prerequisites, status update)
```

**STEP 3: Actually DO what the prompt says**
```
Don't just say it - verify prerequisites, update status, proceed with workflow
```

**STEP 4: Update EPIC_README.md or feature README.md Agent Status**
```
Document guide read, critical rules, next action
```

---

## Anti-Patterns to Avoid

**These are UNACCEPTABLE responses when starting a stage:**

### ❌ WRONG: "I'm familiar with the process"

```
❌ DON'T SAY THIS:
"I'm familiar with S5, let me start the TODO creation..."
```

**Why wrong:** No proof you read the guide. Leads to guide abandonment.

**✅ CORRECT:**
```
I'm reading `stages/s5/s5_p1_planning_round1.md` to ensure I follow all 8 iterations in Round 1...
{List critical requirements for Round 1}
```

---

### ❌ WRONG: Generic acknowledgment

```
❌ DON'T SAY THIS:
"I'll follow the guide for S7..."
```

**Why wrong:** No proof you read it. No accountability for specific requirements.

**✅ CORRECT:**
```
I'm reading `stages/s10/s7_p1_smoke_testing.md`...
**The guide requires:**
- Part 1: Import test
- Part 2: Entry point test
- Part 3: E2E execution test (CRITICAL - verify OUTPUT DATA VALUES)
- Re-reading checkpoints after Parts 2 and 3
- MANDATORY GATE before QC rounds
{Continue with specific requirements}
```

---

### ❌ WRONG: Skipping prerequisite verification

```
❌ DON'T SAY THIS:
"Starting S6 implementation..."
```

**Why wrong:** Might not be ready. Could be missing prerequisites.

**✅ CORRECT:**
```
**Prerequisites I'm verifying:**
✅ S5 complete (28 iterations done)
✅ Iteration 24: Implementation Readiness = PASSED
✅ implementation_plan.md v3.0 exists and user-approved
{Verify ALL prerequisites}
```

---

### ❌ WRONG: Not updating Agent Status

```
❌ DON'T SAY THIS:
{Just starts working without updating README}
```

**Why wrong:** Work is lost if session compacts. No resumability.

**✅ CORRECT:**
```
**Updating feature README Agent Status:**
- Current Phase: {PHASE}
- Current Guide: {guide_name}.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: {list 3-5 rules}
- Next Action: {exact next step}
```

---

## Summary

**When to use these prompts:**
- Starting ANY stage (1-7)
- Starting ANY sub-stage (5a-5e)
- Creating missed requirements
- Starting debugging workflow
- Creating bug fixes
- Resuming after compaction
- Encountering problems

**Why prompts are mandatory:**
1. Proves guide was read
2. Lists critical requirements
3. Verifies prerequisites
4. Updates Agent Status for persistence
5. Prevents guide abandonment (40% failure rate without)

**Key principles:**
- READ the guide FIRST (use Read tool)
- NAVIGATE to the correct prompt file from this router
- LIST critical requirements (proves you read it)
- VERIFY prerequisites (ensures readiness)
- UPDATE Agent Status (enables resumability)
- THEN proceed with work

**Remember:** These prompts take 2-3 minutes but prevent hours of rework. NEVER skip them.

---

## File Organization

This router file has been optimized from 1,474 lines to ~200 lines by splitting content into focused files:

- **prompts/stage_1_prompts.md** - S1 prompts (67 lines)
- **prompts/stage_2_prompts.md** - S2 prompts (~50 lines)
- **prompts/stage_3_prompts.md** - S3 prompts (~40 lines)
- **prompts/stage_4_prompts.md** - S4 prompts (~40 lines)
- **prompts/stage_5_prompts.md** - All S5 sub-stage prompts (~650 lines)
- **prompts/stage_6_prompts.md** - S9 prompts (~65 lines)
- **prompts/stage_7_prompts.md** - S10 prompts (~70 lines)
- **prompts/special_workflows_prompts.md** - Bug fix, missed requirement, debugging, resuming (~200 lines)
- **prompts/problem_situations_prompts.md** - Test failures, blockers, user interactions (~120 lines)

**Total:** 1,474 lines → 9 focused files averaging ~150 lines each
**Search time reduction:** ~80% (agents can go directly to relevant file)

---

**END OF PROMPTS REFERENCE v2 ROUTER**
