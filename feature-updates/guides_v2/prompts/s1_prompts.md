# S1 Prompts: Epic Planning

**Stage:** 1
**Purpose:** Epic planning with Discovery Phase and folder structure creation

---

## Starting S1: Epic Planning

**User says:** "Help me develop the {epic_name} epic" or "Let's plan {epic_name}"

**Prerequisite:** User has created `feature-updates/{epic_name}.txt` with initial scratchwork notes.

**Agent MUST respond:**

```bash
I'm reading `stages/s1/s1_epic_planning.md` to ensure I follow the complete epic planning workflow...

**The guide requires:**
- Step 1: Initial Setup (git branch, epic folder, EPIC_README.md)
- Step 2: Epic Analysis (read request, identify goals, estimate scope)
- Step 3: Discovery Phase (MANDATORY - iterative research and Q&A)
- Step 4: Feature Breakdown Proposal (based on Discovery findings)
- Step 5: Epic Structure Creation (folders, specs with Discovery Context)
- Step 6: Transition to S2

**Critical Discovery Phase Requirements:**
- Discovery is MANDATORY for every epic
- Discovery Loop continues until NO NEW QUESTIONS emerge
- User answers questions throughout Discovery
- DISCOVERY.md becomes epic-level source of truth
- Feature folders NOT created until Discovery approved

**Prerequisites I'm verifying:**
[ ] Epic request file exists: `feature-updates/{epic_name}.txt`
[ ] Epic request contains user's initial notes
[ ] Git working directory is clean

**I'll now proceed with Step 1 (Initial Setup)...**

**Creating initial EPIC_README.md status:**
- Current Stage: S1 - Epic Planning
- Current Step: Step 1 - Initial Setup
- Current Guide: stages/s1/s1_epic_planning.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "Discovery is mandatory", "Loop until no questions", "User approves Discovery before features"
- Next Action: Create git branch and epic folder structure

Starting Step 1...
```

---

## Starting S1.P3: Discovery Phase

**When:** After completing S1 Step 2 (Epic Analysis)

**Agent MUST respond:**

```markdown
I'm reading `stages/s1/s1_p3_discovery_phase.md` to ensure I follow the Discovery Phase workflow...

**The guide requires:**
- S1.P3.1: Initialize DISCOVERY.md
- S1.P3.2: Discovery Loop (iterative)
  - Research (read code, examine patterns)
  - Document findings in DISCOVERY.md
  - Identify questions
  - Ask user, record answers
  - Repeat until NO NEW QUESTIONS emerge
- S1.P3.3: Synthesize findings
- S1.P3.4: User approval of recommended approach

**Critical Discovery Rules:**
- Discovery is MANDATORY (no exceptions)
- Continue loop until research produces no new questions
- All findings and answers go in DISCOVERY.md
- User answers questions throughout (not just at end)
- Feature breakdown informed by Discovery findings

**Time-Box for this epic:**
- Epic Size: {SMALL/MEDIUM/LARGE}
- Time-Box: {1-2 / 2-3 / 3-4} hours

**I'll now proceed with S1.P3.1 (Initialize DISCOVERY.md)...**

**Updating EPIC_README.md status:**
- Current Step: S1.P3 - Discovery Phase
- Current Guide: stages/s1/s1_p3_discovery_phase.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "Loop until no questions", "Document all findings", "User approves before features"
- Next Action: Create DISCOVERY.md and extract initial questions

Starting S1.P3.1...
```

---

## Discovery Loop Iteration

**When:** Starting each iteration of the Discovery Loop (S1.P3.2)

**Agent MUST respond:**

```markdown
**Discovery Loop - Iteration {N}**

**Research Focus:**
{What I'm investigating this iteration}

**Files Examined:**
- {file_path}: {what I found}
- {file_path}: {what I found}

**Key Findings:**
- {finding 1}
- {finding 2}

**Questions Identified:**
{List questions that emerged from research}

---

**Questions for User:**

### Question {N}: {Category}
{Question text}

**Context:** {Why this matters}

**Options (if applicable):**
- Option A: {description}
- Option B: {description}

---

Please answer so I can continue research.
```

---

## Discovery Phase Complete

**When:** Discovery Loop exits (no new questions), ready for synthesis

**Agent MUST respond:**

```markdown
**Discovery Phase Complete**

**Iterations Completed:** {N}
**Questions Resolved:** {M}
**Time Spent:** {X} hours

**Summary of Findings:**
{2-3 sentence summary of key findings}

**Recommended Approach:**
{Brief description of recommended solution}

**Proposed Scope:**

**In Scope:**
- {item 1}
- {item 2}

**Out of Scope:**
- {item 1}

**Proposed Feature Breakdown:**
1. **{Feature 1}:** {brief description}
2. **{Feature 2}:** {brief description}
...

**Questions for You:**
- Does this approach align with your expectations?
- Any scope adjustments needed?
- Does the feature breakdown make sense?

**Please approve to proceed to feature breakdown (Step 4).**
```

---

## S1 Complete: Transitioning to S2

**When:** S1 Step 6 complete, ready to announce transition to S2

**Agent MUST respond:**

```markdown
**S1 (Epic Planning) Complete**

**Summary:**
- Epic folder created: feature-updates/KAI-{N}-{epic_name}/
- Feature folders created: {count}
- Discovery iterations: {N}
- Questions resolved: {M}

**Parallelization Assessment (Step 5.8-5.9):**
- Feature count: {N}
- Parallelization assessed: {YES/NO}
- Parallelization offered: {YES/NO/N/A (only 1 feature)}
- User choice: {PARALLEL / SEQUENTIAL / N/A}

**S1 Completion Checklist:**
- [x] Epic folder created
- [x] All feature folders created
- [x] EPIC_README.md created
- [x] DISCOVERY.md created and approved
- [x] epic_smoke_test_plan.md created
- [x] epic_lessons_learned.md created
- [x] Parallelization assessment completed (Step 5.8-5.9)
- [x] User choice documented: {PARALLEL/SEQUENTIAL}

**🚨 VERIFICATION: If feature count >= 2 and parallelization NOT assessed, STOP and complete Step 5.8-5.9 before proceeding.**

**Ready to proceed to S2 (Feature Deep Dives).**

Would you like me to begin S2 for Feature 01?
```

---

*For prompts for other stages, see the [prompts index](../prompts_reference_v2.md)*
