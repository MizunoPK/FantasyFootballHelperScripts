# Guide Update Recommendations - {Feature/Epic Name}

**Purpose:** Concrete, actionable guide improvements identified during debugging

**Source:** Per-issue root cause analysis (Phase 4b of debugging protocol)

**Usage:** These recommendations will be presented to user in Stage 7.5 for approval

**Priority Levels:**
- **P0 (Critical):** Prevents catastrophic bugs, user testing failures, epic restarts
- **P1 (High):** Prevents bugs reaching QC/smoke testing, major rework, >4hr debugging
- **P2 (Medium):** Moderate improvements, clarifies ambiguity, <2hr debugging
- **P3 (Low):** Minor improvements, cosmetic fixes

---

## Recommendation #1: {Short Title}

**Source Issue:** Issue #{number} - {issue name}
**Affected Guide:** `{path/to/guide.md}`
**Section:** {section name}
**Priority:** {P0/P1/P2/P3}
**User Confirmed:** ✅ YES (Date: {YYYY-MM-DD HH:MM})

### Root Cause

{Brief summary of why bug existed}

**5-Why Analysis:**
1. **Technical Cause:** {answer}
2. **Implementation Gap:** {answer}
3. **Planning Gap:** {answer}
4. **Process Gap:** {answer}
5. **Guide Gap:** {answer} ← ROOT CAUSE

**Root Cause Category:** {A/B/C/D/E/F}
- A = Missing guide section
- B = Unclear guide instruction
- C = Missing mandatory gate
- D = Process gap
- E = Tool/template gap
- F = Not a process issue (domain-specific)

### Prevention Point

**Should have been caught at:**
- **Stage:** {Stage 5a / 5b / Part 5.3.1 / Part 5.3.2 / 2 / etc.}
- **Step:** {Iteration X / QC Round X / etc.}
- **Guide:** `{guide name}`
- **Why missed:** {specific gap}

### Current State (BEFORE)

```markdown
{Current text from guide, OR "Section doesn't exist"}
```

### Proposed Change (AFTER)

```markdown
{Proposed new text with **BOLD** for additions/changes}
```

**Example with changes highlighted:**
```markdown
## Iteration 9: Edge Case Analysis

**Checklist:**
- [ ] Data edge cases (null, empty, invalid)
- [ ] Boundary conditions (min/max values)
- [ ] **Entity status fields (active, injured, suspended, bye week)** ← NEW
- [ ] Concurrent access scenarios
```

### Rationale

{Why this prevents future bugs - be specific}

### Impact Assessment

**Who benefits:** {Which agents/stages benefit from this change}

**When it helps:** {Specific situations where this guidance is needed}
- Example: "During Stage 5a Round 2 when analyzing player data edge cases"

**Severity if unfixed:** {What happens without this fix}
- Example: "Future epics will likely encounter same bug with player status"

**Estimated debugging time saved:** {X} hours per epic
- Example: "3 hours (this bug took 3 hours to debug, direct prevention)"

---

## Recommendation #2: {Short Title}

{Repeat structure for each issue}

---

{PATTERN-BASED RECOMMENDATIONS ADDED HERE DURING PHASE 5 STEP 3}

---

## CROSS-PATTERN RECOMMENDATIONS (Added from Phase 5 Step 3)

**Purpose:** Pattern-based guide improvements (IN ADDITION to per-issue recommendations above)

**Patterns Analyzed:** {count}
**Date Added:** {YYYY-MM-DD}

---

## Pattern-Based Recommendation #{next_number}: {Pattern Name}

**Source Pattern:** Cross-bug pattern affecting Issue #{X}, #{Y}, #{Z}
**Affected Guide:** `{guide_path}`
**Section:** {section}
**Priority:** {P0/P1/P2/P3}

### Pattern Description

{Description of pattern found across multiple bugs}

### Root Cause (Pattern-Level)

{What process/guide gap allows this pattern to recur}

### Current State (BEFORE)

```markdown
{Current text from guide, OR "Section doesn't exist"}
```

### Proposed Change (AFTER)

```markdown
{Proposed new text with **BOLD** for additions/changes}
```

### Rationale

{Why this prevents the PATTERN (affects multiple bug types)}

### Impact Assessment

**Bugs this pattern affected:**
- Issue #{X}: {brief description}
- Issue #{Y}: {brief description}
- Issue #{Z}: {brief description}

**Estimated bugs prevented per epic:** {count} similar bugs
**Estimated debugging time saved:** {X} hours per epic

---

## Template Usage Instructions

**DELETE THIS SECTION AFTER CREATING FILE**

**Phase 4b (Per Issue):**
1. After user confirms fix (Phase 4), perform root cause analysis
2. Present 5-why analysis and guide improvement to user
3. If user AGREES: Add Recommendation #N using template above
4. If user DISAGREES: Mark as "Not a process issue", don't add
5. Update issue file with root cause section
6. Mark "Root Cause?: ✅ YES" in ISSUES_CHECKLIST.md

**Phase 5 Step 3 (Cross-Pattern):**
1. After ALL issues resolved, review all recommendations above
2. Identify PATTERNS across multiple bugs
3. Add pattern-based recommendations to "CROSS-PATTERN RECOMMENDATIONS" section
4. These are IN ADDITION to per-issue recommendations

**Stage 7.5 (Guide Update from Lessons Learned):**
1. Agent reads this file (ALL recommendations)
2. Creates GUIDE_UPDATE_PROPOSAL.md with each recommendation as separate proposal
3. Presents each proposal to user for individual approval
4. User decides: Approve / Modify / Reject / Discuss
5. Agent applies only approved changes to guides
6. Updates guide_update_tracking.md with applied lessons

**Priority Assignment Guidelines:**

**P0 (Critical):**
- Bug reached user testing or production
- Caused epic restart
- Data loss / system crash / security issue
- Prevented by process gap (no gate exists)

**P1 (High):**
- Bug reached smoke testing or QC rounds
- Took >4 hours to debug
- Affected multiple features
- Prevented by unclear guide instruction

**P2 (Medium):**
- Bug caught quickly (<2 hours)
- Affected single feature
- Moderate improvement needed
- Prevented by missing checklist item

**P3 (Low):**
- Minor bug (cosmetic, non-critical)
- Edge case unlikely to recur
- Guide wording improvement
- Process already mostly works

**File Location:**
- Feature-level: `feature_XX_{name}/debugging/guide_update_recommendations.md`
- Epic-level: `{epic_name}/debugging/guide_update_recommendations.md`

**Example Recommendation:**

## Recommendation #1: Add Entity Status Field Check to Iteration 9

**Source Issue:** Issue #1 - player_scoring_returns_null
**Affected Guide:** `stages/s5/s5_p2_planning_round2.md`
**Section:** Iteration 9: Edge Case Analysis
**Priority:** P1 (High)
**User Confirmed:** ✅ YES (Date: 2026-01-15 14:30)

### Root Cause

Bug occurred because player injury status wasn't checked, causing null pointer when accessing injured player stats.

**5-Why Analysis:**
1. **Technical Cause:** Null pointer exception in calculate_score()
2. **Implementation Gap:** Missing null check for injured players
3. **Planning Gap:** Edge case not identified in implementation_plan.md Iteration 9
4. **Process Gap:** Iteration 9 (Edge Case Analysis) didn't consider injury status
5. **Guide Gap:** s5_p2_planning_round2.md Iteration 9 doesn't mention entity status fields ← ROOT CAUSE

**Root Cause Category:** A (Missing guide section)

### Prevention Point

**Should have been caught at:**
- **Stage:** Stage 5a Round 2
- **Step:** Iteration 9 (Edge Case Analysis)
- **Guide:** `stages/s5/s5_p2_planning_round2.md`
- **Why missed:** Guide doesn't explicitly mention checking entity status fields

### Current State (BEFORE)

```markdown
## Iteration 9: Edge Case Analysis

**Checklist:**
- [ ] Data edge cases (null, empty, invalid)
- [ ] Boundary conditions (min/max values)
- [ ] Concurrent access scenarios
```

### Proposed Change (AFTER)

```markdown
## Iteration 9: Edge Case Analysis

**Checklist:**
- [ ] Data edge cases (null, empty, invalid)
- [ ] Boundary conditions (min/max values)
- [ ] **Entity status fields (active, injured, suspended, bye week, etc.)**
- [ ] Concurrent access scenarios
```

### Rationale

Adding entity status fields to the checklist forces agents to systematically verify all status-related edge cases during planning. This prevents null pointer exceptions and incorrect calculations when entities have non-standard states.

### Impact Assessment

**Who benefits:** All agents implementing features with entity data (players, teams, games)

**When it helps:** During Stage 5a Round 2 when analyzing edge cases for any entity-based feature

**Severity if unfixed:** Future epics will likely encounter same bug pattern with entity status
- Estimated 60% of entity-based features have status fields
- Each bug takes ~3 hours to debug

**Estimated debugging time saved:** 3 hours per epic (50% chance of occurrence = 1.5 hrs expected value)
