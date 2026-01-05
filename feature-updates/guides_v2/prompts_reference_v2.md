# Phase Transition Prompts Reference (v2) - Router

**Version:** 2.1
**Last Updated:** 2026-01-04
**Purpose:** MANDATORY prompts for stage transitions

---

## ⚠️ CRITICAL: When to Use These Prompts

**You MUST use these prompts when:**
- Starting ANY stage (Stages 1-7)
- Starting ANY sub-stage (5a, 5b, 5c, 5d, 5e)
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

**[Stage 1: Epic Planning](prompts/stage_1_prompts.md)**
- Starting Stage 1: Epic Planning

**[Stage 2: Feature Deep Dive](prompts/stage_2_prompts.md)**
- Starting Stage 2: Feature Deep Dive

**[Stage 3: Cross-Feature Sanity Check](prompts/stage_3_prompts.md)**
- Starting Stage 3: Cross-Feature Sanity Check

**[Stage 4: Epic Testing Strategy](prompts/stage_4_prompts.md)**
- Starting Stage 4: Epic Testing Strategy

**[Stage 5: Feature Implementation](prompts/stage_5_prompts.md)**
- Starting Stage 5a: TODO Creation (Round 1)
- Starting Stage 5a: TODO Creation (Round 2)
- Starting Stage 5ac Part 1: TODO Creation (Round 3 - Preparation)
- Starting Stage 5ac Part 2: TODO Creation (Round 3 - Final Gates)
- Starting Stage 5b: Implementation
- Starting Stage 5c (Phase 1): Smoke Testing
- Starting Stage 5c (Phase 2): QC Rounds
- Starting Stage 5c (Phase 3): Final Review
- Starting Stage 5d: Cross-Feature Alignment
- Starting Stage 5e: Epic Testing Plan Update

**[Stage 6: Epic Final QC](prompts/stage_6_prompts.md)**
- Starting Stage 6: Epic Final QC

**[Stage 7: Epic Cleanup](prompts/stage_7_prompts.md)**
- Starting Stage 7: Epic Cleanup

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
"I'm familiar with Stage 5a, let me start the TODO creation..."
```

**Why wrong:** No proof you read the guide. Leads to guide abandonment.

**✅ CORRECT:**
```
I'm reading `stages/stage_5/round1_todo_creation.md` to ensure I follow all 8 iterations in Round 1...
{List critical requirements for Round 1}
```

---

### ❌ WRONG: Generic acknowledgment

```
❌ DON'T SAY THIS:
"I'll follow the guide for Stage 5c..."
```

**Why wrong:** No proof you read it. No accountability for specific requirements.

**✅ CORRECT:**
```
I'm reading `stages/stage_5/smoke_testing.md`...
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
"Starting Stage 5b implementation..."
```

**Why wrong:** Might not be ready. Could be missing prerequisites.

**✅ CORRECT:**
```
**Prerequisites I'm verifying:**
✅ Stage 5a complete (24 iterations done)
✅ Iteration 24: Implementation Readiness = PASSED
✅ todo.md exists with complete task list
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

- **prompts/stage_1_prompts.md** - Stage 1 prompts (67 lines)
- **prompts/stage_2_prompts.md** - Stage 2 prompts (~50 lines)
- **prompts/stage_3_prompts.md** - Stage 3 prompts (~40 lines)
- **prompts/stage_4_prompts.md** - Stage 4 prompts (~40 lines)
- **prompts/stage_5_prompts.md** - All Stage 5 sub-stage prompts (~650 lines)
- **prompts/stage_6_prompts.md** - Stage 6 prompts (~65 lines)
- **prompts/stage_7_prompts.md** - Stage 7 prompts (~70 lines)
- **prompts/special_workflows_prompts.md** - Bug fix, missed requirement, debugging, resuming (~200 lines)
- **prompts/problem_situations_prompts.md** - Test failures, blockers, user interactions (~120 lines)

**Total:** 1,474 lines → 9 focused files averaging ~150 lines each
**Search time reduction:** ~80% (agents can go directly to relevant file)

---

**END OF PROMPTS REFERENCE v2 ROUTER**
