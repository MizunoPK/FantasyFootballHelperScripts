# D10: File Size Assessment - Stage 2 Fix Planning (Session 2)

**Dimension:** D10 - File Size Assessment
**Audit Round:** Round 1
**Stage:** Stage 2 - Fix Planning (Continued)
**Session Date:** 2026-02-05
**Auditor:** Claude (Primary Agent)
**Files Analyzed:** Files 3-5 (s1, s2, s4)

---

## Session 2 Summary

**Files Analyzed:** 3 CRITICAL files (s1_epic_planning, s2_p3_refinement, s4_epic_testing_strategy)

**Analysis Completed:**
- ✅ s1_epic_planning.md (1116 lines) - Parallelization sections verbose
- ✅ s2_p3_refinement.md (1106 lines) - Phase 6 investigation checklist verbose
- ✅ s4_epic_testing_strategy.md (1060 lines) - Example scenarios verbose

**Reduction Strategies:**
- All 3 files: Strategy 4 (Condense Verbose Sections)
- Estimated total reduction: ~295-325 lines across 3 files
- All files projected to be just under 1000-line threshold after reduction

**Session Time:** 1.5 hours analysis

---

## FILE 3: stages/s1/s1_epic_planning.md

### Current State

**File:** `feature-updates/guides_v2/stages/s1/s1_epic_planning.md`
**Size:** 1116 lines
**Over Threshold:** 116 lines (1000-line CRITICAL threshold)
**Category:** CRITICAL - MUST reduce

### Analysis

**Purpose Analysis:**
- **Primary Purpose:** Stage guide for S1 Epic Planning (git branch, Discovery, feature breakdown, folder creation)
- **File Type:** Sequential workflow guide (agents read start-to-finish during S1)
- **Usage Pattern:** Read once when executing S1, referenced during feature creation

**Content Analysis:**
- **Natural Subdivisions:** ✅ YES - 6 Steps (Step 1-6) with substeps
- **Duplicate Content:** ⚠️ PARTIAL - Step 3 (Discovery Phase) already extracted to s1_p3_discovery_phase.md (988 lines), but S1 still contains 68-line overview
- **Verbose Sections:** ✅ YES - Step 5 contains extremely verbose parallelization sections:
  - Step 5.7.5: Analyze Feature Dependencies (78 lines)
  - Step 5.8: Analyze Features for Parallelization (64 lines)
  - Step 5.9: Offer Parallel Work to User (82 lines)
  - **Total parallelization content: 224 lines**
- **Detailed Examples:** Step 5.8 and 5.9 contain verbose calculation examples and offering templates
- **Reference Material:** Separate `parallel_work/` directory exists with comprehensive guides (s2_parallel_protocol.md: 1233 lines)

**Line Distribution:**
```
Header/Overview (1-235):       234 lines (includes Critical Rules, Prerequisites, Workflow Overview)
Step 1 (Initial Setup):         41 lines
Step 2 (Epic Analysis):         39 lines
Step 3 (Discovery Phase):       68 lines (already condensed, references s1_p3_discovery_phase.md)
Step 4 (Feature Breakdown):    114 lines
Step 5 (Epic Structure):       319 lines (includes 224 lines of parallelization content)
Step 6 (Transition):            20 lines
Checkpoints section:           280 lines (5 checkpoints + supporting content)
Total:                        1116 lines
```

**Usage Analysis:**
- **How Agents Use:** Read sequentially when executing S1
- **Need All Content:** No - parallelization sections (5.7.5-5.9) are decision-making logic that could be condensed
- **Context:** Step 5 parallelization sections are S1-specific (offering/decision), while parallel_work/ guides are execution protocols

**Evaluation:**
- ❌ 1116 lines exceeds CRITICAL threshold by 116 lines
- ✅ Step 3 already appropriately condensed (references full guide)
- ❌ Step 5 parallelization sections (224 lines) are verbose with extensive examples
- ✅ Parallelization decision logic is important, but examples are overly detailed
- ⚠️ Parallel work execution protocols exist in separate guides (not duplicative)
- ✅ Clear reduction path: Condense parallelization examples, keep decision logic

### Reduction Strategy

**Selected Strategy:** Strategy 4 - Condense Verbose Sections (parallelization content)

**Target Sections for Condensing:**
1. **Step 5.7.5: Analyze Feature Dependencies** (78 lines → 35 lines)
   - Keep: Purpose, basic dependency identification steps
   - Condense: Example dependency analysis (currently has 3+ detailed examples)
   - Remove: Verbose walkthrough of dependency determination process
   - Reference: `parallel_work/s2_parallel_protocol.md` for detailed dependency analysis

2. **Step 5.8: Analyze Features for Parallelization** (64 lines → 30 lines)
   - Keep: Purpose, feature counting, time savings formula
   - Condense: Time savings examples (currently has 2 features, 3 features, 4 features examples)
   - Simplify: Show formula once with one example instead of 3-4 examples
   - Reference: `parallel_work/s2_parallel_protocol.md` for detailed analysis

3. **Step 5.9: Offer Parallel Work to User** (82 lines → 35 lines)
   - Keep: Purpose, prerequisites, basic offering template format
   - Condense: Offering message template (currently 50+ lines of example)
   - Simplify: Short template showing structure, not full verbatim example
   - Reference: `parallel_work/parallel_work_prompts.md` for complete offering templates

**Implementation Plan:**

**Step 1: Condense 5.7.5 (Feature Dependencies)**

Current: 78 lines with detailed dependency analysis walkthrough

Revised (~35 lines):
```markdown
### Step 5.7.5: Analyze Feature Dependencies

**Purpose:** Determine which features can start S2 simultaneously vs must wait for dependencies

**For EACH feature, identify:**
1. **Data Dependencies:** Does it need data structures from other features?
2. **Method Dependencies:** Does it call methods created by other features?
3. **Config Dependencies:** Does it need config keys from other features?

**Document in EPIC_README.md:**

```markdown
## Feature Dependencies
- Feature 01: No dependencies (can start immediately)
- Feature 02: Depends on Feature 01 (PlayerManager changes)
- Feature 03: No dependencies (independent)
```

**Dependency groups determine S2 sequencing:**
- Independent features: Can run S2 in parallel
- Dependent features: Must wait for dependencies to complete S2

**See:** `parallel_work/s2_parallel_protocol.md` for detailed dependency analysis and examples
```

**Reduction:** 78 → 35 lines (43 lines saved)

---

**Step 2: Condense 5.8 (Parallelization Analysis)**

Current: 64 lines with multiple time savings examples

Revised (~30 lines):
```markdown
### Step 5.8: Analyze Features for Parallelization (MANDATORY when 2+ features)

**Purpose:** Determine if S2 parallelization should be offered to user

**MANDATORY:** This step is REQUIRED when the epic has 2+ features.

**Analysis Steps:**

1. **Count Features:**
   ```bash
   FEATURE_COUNT=$(ls -d feature_* | wc -l)
   ```

2. **Calculate Potential Savings:**
   ```text
   Sequential S2: FEATURE_COUNT × 2 hours
   Parallel S2: 2 hours (max across all features)
   Savings: (FEATURE_COUNT - 1) × 2 hours

   Example (3 features):
   - Sequential: 6 hours
   - Parallel: 2 hours
   - Savings: 4 hours (67% reduction)
   ```

3. **Check Prerequisites:**
   - Epic has 2+ features
   - User is available for multi-session coordination
   - Complexity justifies coordination overhead

**Decision:** Offer parallelization if savings ≥ 2 hours (i.e., 2+ features)

**See:** `parallel_work/s2_parallel_protocol.md` for complete analysis guide
```

**Reduction:** 64 → 30 lines (34 lines saved)

---

**Step 3: Condense 5.9 (Offering Template)**

Current: 82 lines with full verbose offering message

Revised (~35 lines):
```markdown
### Step 5.9: Offer Parallel Work to User (If Applicable)

**Prerequisites:**
- Analysis shows 2+ features
- Decision made to offer parallelization

**Offering Template Structure:**

```markdown
✅ S1 (Epic Planning) complete!

I've identified {N} features for this epic: [list with ~2 hour estimates]

🚀 **PARALLEL WORK OPPORTUNITY**

TIME SAVINGS: {X} hours ({percent}% reduction in S2 time)
- Sequential: {N} × 2 hours = {total}
- Parallel: 2 hours (simultaneously)

**Would you like to enable parallel work for S2 (Feature Deep Dives)?**

[If Yes: I'll provide handoff packages for secondary agents]
[If No: I'll proceed sequentially through features]
```

**Complete offering template:** See `parallel_work/parallel_work_prompts.md`

**After User Response:**
- If YES: Generate handoff packages (see `parallel_work/s2_primary_agent_guide.md`)
- If NO: Proceed to Step 6 (sequential S2)
```

**Reduction:** 82 → 35 lines (47 lines saved)

---

### Projected Outcome

**Before:**
```
stages/s1/s1_epic_planning.md: 1116 lines (❌ CRITICAL)
- Step 5.7.5: 78 lines
- Step 5.8: 64 lines
- Step 5.9: 82 lines
- Total parallelization: 224 lines
```

**After:**
```
stages/s1/s1_epic_planning.md: ~992 lines (✅ BELOW CRITICAL)
- Step 5.7.5: 35 lines (-43)
- Step 5.8: 30 lines (-34)
- Step 5.9: 35 lines (-47)
- Total parallelization: 100 lines (-124 lines saved)
```

**Total Reduction:** 1116 → 992 lines (**124 lines saved, 11% reduction**)
**Status:** ✅ **BELOW CRITICAL threshold** (<1000 lines)

### Estimated Effort

- **Analysis:** 1 hour (completed in this session)
- **Condensing 5.7.5:** 0.5 hours (careful editing, preserve logic)
- **Condensing 5.8:** 0.5 hours (simplify examples)
- **Condensing 5.9:** 0.5 hours (create template structure)
- **Validation:** 0.5 hours (verify no information loss, test references)
- **Total:** 3 hours

### Implementation Commands

```bash
cd feature-updates/guides_v2/stages/s1

# Step 1: Backup
cp s1_epic_planning.md s1_epic_planning.md.backup

# Step 2: Use Edit tool or Python script to replace sections
# Replace Step 5.7.5 (lines ~592-670)
# Replace Step 5.8 (lines ~670-734)
# Replace Step 5.9 (lines ~734-816)

# Step 3: Validate
wc -l s1_epic_planning.md  # Should be ~992 lines
git diff s1_epic_planning.md | head -100  # Review changes

# Step 4: Verify cross-references
grep -r "s1_epic_planning" ../../../ | grep -v ".backup"
```

---

## FILE 4: stages/s2/s2_p3_refinement.md

### Current State

**File:** `feature-updates/guides_v2/stages/s2/s2_p3_refinement.md`
**Size:** 1106 lines
**Over Threshold:** 106 lines (1000-line CRITICAL threshold)
**Category:** CRITICAL - MUST reduce

### Analysis

**Purpose Analysis:**
- **Primary Purpose:** Phase guide for S2.P3 Refinement Phase (question resolution, scope adjustment, alignment, approval)
- **File Type:** Sequential workflow guide (agents follow 4 phases sequentially)
- **Usage Pattern:** Read when executing S2.P3, after S2.P1 and S2.P2 complete

**Content Analysis:**
- **Natural Subdivisions:** ✅ YES - 4 phases (Phase 3, 4, 5, 6)
- **Duplicate Content:** ❌ NO - Examples already extracted to refinement_examples_phase*.md files
- **Verbose Sections:** ✅ YES - Phase 6 has extensive content:
  - **Comprehensive Investigation Checklist** at Phase 6 intro (46 lines) - 5-category framework with detailed explanations
  - **Step 6.2 Presentation Template** (54 lines) - Full verbose message template to user
  - Total Phase 6: 401 lines
- **Reference Material:** Phase-specific example files exist (created in Quick Win 1)

**Line Distribution:**
```
Header/Overview (1-231):              231 lines (includes Parallel Work Coordination: 81 lines)
Phase 3 (Question Resolution):        190 lines
Phase 4 (Scope Adjustment):           103 lines
Phase 5 (Cross-Feature Alignment):    181 lines
Phase 6 (Acceptance & Approval):      401 lines (includes 46-line investigation checklist + 54-line presentation template)
Total:                               1106 lines
```

**Parallel Work Coordination** (lines 150-231 = 81 lines):
- Contains coordination heartbeat, escalation protocol, completion signal
- Specific to S2.P3 parallel work
- Could be condensed with reference to parallel_work/ guides

**Usage Analysis:**
- **How Agents Use:** Read sequentially when executing S2.P3
- **Need All Content:** Mostly yes, but investigation checklist and presentation templates are verbose
- **Context:** Referenced from S2 router guide

**Evaluation:**
- ❌ 1106 lines exceeds CRITICAL threshold by 106 lines
- ✅ Examples already extracted (not inline)
- ❌ Phase 6 investigation checklist (46 lines) is very detailed
- ❌ Phase 6 presentation template (54 lines) could be condensed
- ❌ Parallel Work Coordination section (81 lines) could reference parallel_work/ guides
- ✅ Clear reduction path: Condense verbose checklists and templates

### Reduction Strategy

**Selected Strategy:** Strategy 4 - Condense Verbose Sections (Phase 6 content + Parallel Work)

**Target Sections for Condensing:**

1. **Parallel Work Coordination Section** (81 lines → 40 lines)
   - Keep: Essential coordination requirements (heartbeat, escalation)
   - Condense: Detailed protocols (currently very verbose)
   - Reference: `parallel_work/communication_protocol.md` and `parallel_work/checkpoint_protocol.md` for details
   - Savings: 41 lines

2. **Phase 6 Investigation Checklist** (46 lines → 20 lines)
   - Keep: 5-category framework structure
   - Condense: Detailed explanations for each category (currently 8-10 lines per category)
   - Simplify: Brief description per category (2-3 lines each)
   - Note: This is S2-specific guidance for user investigation requests, not redundant with other guides
   - Savings: 26 lines

3. **Phase 6 Step 6.2 Presentation Template** (54 lines → 30 lines)
   - Keep: Template structure and key elements
   - Condense: Example presentation message (currently very verbose)
   - Simplify: Show template structure, not full verbatim example
   - Reference: `reference/stage_2/refinement_examples_phase6_approval.md` for full presentation examples
   - Savings: 24 lines

**Implementation Plan:**

**Step 1: Condense Parallel Work Coordination (81 → 40 lines)**

Current: Detailed protocols inline

Revised (~40 lines):
```markdown
## 🔄 Parallel Work Coordination (If Applicable)

**If this epic is using parallel S2 work, follow these coordination requirements:**

### Coordination Heartbeat (Every 15 Minutes)

**Update your checkpoint:**
```json
{
  "agent_id": "secondary_agent_2",
  "feature": "feature_02_trade_analyzer",
  "stage": "S2.P3",
  "progress": "Phase 5 complete, starting Phase 6",
  "timestamp": "2026-01-15T14:30:00Z"
}
```

**Check your inbox:** `agent_comms/primary_to_{your_agent_id}.md`

**Essential coordination:**
- Update checkpoint every 15 minutes
- Check inbox every 15 minutes
- Escalate blockers within 15 minutes
- Signal completion when S2.P3 done

**Complete protocols:** See `parallel_work/communication_protocol.md` and `parallel_work/checkpoint_protocol.md`

### Completion Signal Protocol (S2.P3 Only)

After Phase 6 approval, signal completion to Primary:

Create message: `agent_comms/{your_agent_id}_to_primary.md`

**Content:** "✅ S2.P3 COMPLETE for feature_{NN}_{name}. Ready for S3 sync point."

**See:** `parallel_work/s2_secondary_agent_guide.md` for complete S2.P3 coordination workflow
```

**Reduction:** 81 → 40 lines (41 lines saved)

---

**Step 2: Condense Phase 6 Investigation Checklist (46 → 20 lines)**

Current: Extensive 5-category checklist with detailed explanations

Revised (~20 lines):
```markdown
## Phase 6: Acceptance Criteria & User Approval

**Goal:** Create user-facing summary of what this feature will do, get explicit approval

⚠️ **CRITICAL:** This is a MANDATORY gate. Cannot proceed to S3 without user approval.

**When user requests investigation (e.g., "check compatibility"), use systematic 5-category framework:**

1. **Method/Function Calls** - Where does X call the new code? Parameters correct?
2. **Configuration/Data Loading** ⚠️ (commonly missed) - How does X load new config keys?
3. **Integration Points** - Does new code affect X's flow? Other files affected?
4. **Timing/Dependencies** - Transition period issues? Sequencing requirements?
5. **Edge Cases** - Old config with new code? New config with old code?

**After investigation:**
- Mark checklist status: PENDING USER APPROVAL
- Present findings covering ALL 5 categories
- Wait for explicit user approval
- ONLY THEN mark as RESOLVED

**See:** `reference/stage_2/compatibility_investigation_guide.md` for detailed category explanations and examples (if exists)
```

**Reduction:** 46 → 20 lines (26 lines saved)

---

**Step 3: Condense Step 6.2 Presentation Template (54 → 30 lines)**

Current: Full verbose presentation message

Revised (~30 lines):
```markdown
### Step 6.2: Present to User for Approval

**Message template structure:**

```markdown
## Feature {N} ({Name}) - Ready for Approval

**Spec Status:**
- All {N} checklist questions resolved
- Cross-feature alignment complete
- Scope validated ({items} checklist items)

**Summary:** {2-3 sentence description of what feature will do}

**Impact:**
- Files: {N} new, {M} modified
- API changes: {summary}
- Dependencies: {summary or "None"}

**Full Details:** Please review Acceptance Criteria section in spec.md:
`feature-updates/KAI-{N}-{epic_name}/feature_{NN}_{name}/spec.md`

**Next Steps:**
- If you approve: I'll mark S2 complete and move to next feature or S3
- If changes needed: Let me know what to modify

**Do you approve these acceptance criteria?**
```

**See:** `reference/stage_2/refinement_examples_phase6_approval.md` → "Example 2: User Approval Process" for complete presentation examples

---
```

**Reduction:** 54 → 30 lines (24 lines saved)

---

### Projected Outcome

**Before:**
```
stages/s2/s2_p3_refinement.md: 1106 lines (❌ CRITICAL)
- Parallel Work Coordination: 81 lines
- Phase 6 Investigation Checklist: 46 lines
- Phase 6 Step 6.2 Template: 54 lines
- Total verbose content: 181 lines
```

**After:**
```
stages/s2/s2_p3_refinement.md: ~1015 lines (⚠️ LARGE, CLOSE to threshold)
- Parallel Work Coordination: 40 lines (-41)
- Phase 6 Investigation Checklist: 20 lines (-26)
- Phase 6 Step 6.2 Template: 30 lines (-24)
- Total condensed content: 90 lines (-91 lines saved)
```

**Total Reduction:** 1106 → 1015 lines (**91 lines saved, 8% reduction**)
**Status:** ⚠️ **LARGE** (still close to 1000-line threshold, may need further reduction)

**Note:** File is at 1015 lines after reduction, which is just 15 lines over threshold. Could achieve <1000 by condensing one additional section (e.g., Overview/preamble sections) or accepting LARGE status as this is comprehensive phase guide.

### Estimated Effort

- **Analysis:** 1 hour (completed in this session)
- **Condensing Parallel Work:** 0.5 hours
- **Condensing Investigation Checklist:** 0.5 hours
- **Condensing Presentation Template:** 0.5 hours
- **Validation:** 0.5 hours
- **Total:** 3 hours

### Implementation Commands

```bash
cd feature-updates/guides_v2/stages/s2

# Step 1: Backup
cp s2_p3_refinement.md s2_p3_refinement.md.backup

# Step 2: Replace sections using Edit tool
# Replace Parallel Work (lines ~150-231)
# Replace Phase 6 intro checklist (lines ~705-751)
# Replace Step 6.2 (lines ~769-823)

# Step 3: Validate
wc -l s2_p3_refinement.md  # Should be ~1015 lines
git diff s2_p3_refinement.md | head -100

# Step 4: Consider additional reduction if needed
# Could condense Overview/Critical Rules to get under 1000 lines
```

---

## FILE 5: stages/s4/s4_epic_testing_strategy.md

### Current State

**File:** `feature-updates/guides_v2/stages/s4/s4_epic_testing_strategy.md`
**Size:** 1060 lines
**Over Threshold:** 60 lines (1000-line CRITICAL threshold)
**Category:** CRITICAL - Just over threshold

### Analysis

**Purpose Analysis:**
- **Primary Purpose:** Stage guide for S4 Epic Testing Strategy development
- **File Type:** Sequential workflow guide (7 steps from review to validation)
- **Usage Pattern:** Read when executing S4, after S3 complete

**Content Analysis:**
- **Natural Subdivisions:** ✅ YES - 7 Steps
- **Duplicate Content:** ❌ NO
- **Verbose Sections:** ✅ YES - Contains many example test scenarios:
  - **Step 4: Create Specific Test Scenarios** (207 lines) - Contains 6 detailed test scenario examples
  - **Step 6: S4 Validation Loop** (359 lines) - Contains detailed loop process, examples, and Gate 4.5 presentation
- **Reference Material:** Test scenario templates could be extracted

**Line Distribution:**
```
Header/Overview (1-161):                      160 lines
Step 1 (Review Initial Test Plan):            48 lines
Step 2 (Identify Integration Points):         75 lines
Step 3 (Define Epic Success Criteria):        90 lines
Step 4 (Create Specific Test Scenarios):     206 lines (contains 6 example scenarios with 30-50 lines each)
Step 5 (Update epic_smoke_test_plan.md):     121 lines
Step 6 (S4 Validation Loop):                 359 lines (includes validation process + Gate 4.5 presentation)
Total:                                      1060 lines
```

**Usage Analysis:**
- **How Agents Use:** Read sequentially when executing S4
- **Need All Content:** Mostly yes, but example scenarios are verbose
- **Context:** One-time read during S4 execution

**Evaluation:**
- ❌ 1060 lines exceeds CRITICAL threshold by 60 lines (just barely over)
- ⚠️ Only 60 lines over - close to threshold
- ❌ Step 4 test scenarios (206 lines) contain very detailed examples
- ❌ Step 6 (359 lines) is quite long with validation loop details and Gate 4.5
- ✅ Examples are helpful for agents, but could be condensed
- ✅ Clear reduction path: Condense example scenarios and validation loop content

### Reduction Strategy

**Selected Strategy:** Strategy 4 - Condense Verbose Sections (example scenarios + validation loop)

**Target Sections for Condensing:**

1. **Step 4: Create Specific Test Scenarios** (206 lines → 120 lines)
   - Currently contains 6 detailed test scenario examples (Test Scenarios 1-6)
   - Each scenario has: Title, Context, Steps, Expected Output, Success Criteria (30-50 lines each)
   - Condense to: Show 2-3 complete examples, summarize format for others
   - Create reference file: `reference/stage_4/test_scenario_templates.md` with all examples
   - Savings: 86 lines

2. **Step 6: S4 Validation Loop** (359 lines → 250 lines)
   - Contains: Validation loop process (80 lines) + Step 7 (Mark S4 Complete including Gate 4.5 presentation: 279 lines)
   - Gate 4.5 presentation is quite verbose (similar to other gate presentations)
   - Condense: Validation loop examples, Gate 4.5 presentation template
   - Keep: Essential loop logic, gate requirement, basic presentation structure
   - Savings: 109 lines

**Note:** Only need ~80 lines total reduction to get under 1000. Could achieve with just one of the above, but doing both improves readability.

**Implementation Plan:**

**Step 1: Condense Step 4 Test Scenarios (206 → 120 lines)**

Current: 6 detailed test scenario examples inline

Revised (~120 lines):
```markdown
## Step 4: Create Specific Test Scenarios

### Step 4.1: Convert High-Level Categories to Concrete Tests

**Goal:** Transform abstract test categories into specific, executable test scenarios

**Test Scenario Format:**
```markdown
### Test Scenario {N}: {Name}

**Context:** {What features/components this tests}

**Steps:**
1. {Specific command or action}
2. {Expected system response}
3. {Validation check}

**Expected Output:**
- {Concrete, measurable output}

**Success Criteria:**
- [ ] {Specific pass condition 1}
- [ ] {Specific pass condition 2}
```

**Example Scenarios:**

### Test Scenario 1: Data File Creation (Features 1, 2, 3)

**Context:** Features 1, 2, 3 create data files (adp_rankings.csv, injury_data.json, matchup_difficulty.csv)

**Steps:**
1. Delete existing data files if present
2. Run: `python run_league_helper.py --mode draft`
3. Check data/ directory

**Expected Output:**
- `data/adp_rankings.csv` exists with ≥10 rows
- `data/injury_data.json` exists with valid JSON
- `data/matchup_difficulty.csv` exists with 32 teams

**Success Criteria:**
- [ ] All 3 files created
- [ ] Files contain valid data (not empty)
- [ ] CSV/JSON formats parseable

---

### Test Scenario 2: End-to-End Workflow

**Context:** Complete draft recommendation flow with all features integrated

**Steps:**
1. Run: `python run_league_helper.py --mode draft --use-adp --week 1`
2. Select player: "Patrick Mahomes"
3. Verify scoring includes ALL multipliers

**Expected Output:**
- Score calculated: `base × injury × matchup × adp × team_ranking`
- Each multiplier value shown in output

**Success Criteria:**
- [ ] All 5 multipliers applied
- [ ] Final score = product of all multipliers
- [ ] No errors or warnings

---

**Additional Test Scenarios:** Create similar detailed scenarios for:
- Cross-feature integration points (identified in Step 2)
- Edge cases (missing data files, invalid config)
- Feature-specific functionality
- Data quality validation

**Complete test scenario templates:** See `reference/stage_4/test_scenario_templates.md` for 10+ example scenarios (if created)

### Step 4.2: Add Integration-Specific Tests

{Condensed section focusing on integration test requirements}
```

**Reduction:** 206 → 120 lines (86 lines saved)

---

**Step 2: Condense Step 6 Validation Loop (359 → 270 lines)**

Current: Detailed validation loop + verbose Gate 4.5 presentation

Revised (~270 lines):
```markdown
## Step 6: S4 Validation Loop (MANDATORY)

**Goal:** Achieve 2-3 consecutive clean loops with ZERO issues in test plan

**Loop Process:**
1. Review test plan from chosen perspective
2. Find issues (missing tests, unclear scenarios, inconsistent validation)
3. Resolve ALL issues immediately (zero tolerance)
4. Loop again with fresh perspective
5. **Exit:** 2-3 consecutive clean loops (ZERO issues found)

**Validation Perspectives:**
1. **Test Coverage Reviewer** (Loop 1): Every feature has specific test scenarios
2. **Integration Validator** (Loop 2): All cross-feature integration points tested
3. **User Acceptance Tester** (Loop 3): Success criteria clear and measurable

**Time:** ~15-30 minutes total (prevents S9 rework)

**Documentation:** Create validation log in epic_smoke_test_plan.md Update Log

---

## Step 7: Mark S4 Complete & Get User Approval

### Step 7.1: Update EPIC_README.md

{Condensed checklist update instructions}

### Step 7.2: Present Test Plan to User (🚨 GATE 4.5 - MANDATORY)

**🚨 CRITICAL:** You MUST get user approval of epic_smoke_test_plan.md before proceeding to S5.

**Why:** Agent needs to know EXACTLY how to test work BEFORE creating implementation plans. User can adjust test strategy early (cheap at S4 vs expensive at S5).

**Present to user:**

```markdown
🚨 **Gate 4.5: Epic Test Plan Approval Required**

**Location:** `epic_smoke_test_plan.md`

**Summary:**
- {N} success criteria defined
- {M} test scenarios identified
- Integration points documented
- Data quality checks included

**Please review and approve:**
1. Are success criteria correct and measurable?
2. Do test scenarios cover all features?
3. Are integration points identified?
4. Any missing test cases?

**Once approved, I'll proceed to S5 (Implementation Planning).**
```

**If user approves:**
- Mark Gate 4.5 complete in EPIC_README.md
- Update Agent Status
- Proceed to S5

**If user requests changes:**
- Update epic_smoke_test_plan.md
- Re-run validation loop
- Present again for approval
```

**Reduction:** 359 → 270 lines (89 lines saved)

---

### Projected Outcome

**Before:**
```
stages/s4/s4_epic_testing_strategy.md: 1060 lines (❌ CRITICAL, just over threshold)
- Step 4 (Test Scenarios): 206 lines
- Step 6 (Validation Loop): 359 lines
```

**After:**
```
stages/s4/s4_epic_testing_strategy.md: ~985 lines (✅ BELOW CRITICAL)
- Step 4 (Test Scenarios): 120 lines (-86)
- Step 6 (Validation Loop): 270 lines (-89)
- Total reduction: -175 lines
```

**Note:** Target is ~985 lines but we only need 60 lines reduction. The above reduction (-175 lines) exceeds requirements but improves readability. Could reduce less aggressively if desired (e.g., only condense Step 4 by 60 lines).

**Total Reduction:** 1060 → 885 lines (**175 lines saved, 17% reduction**)
**Status:** ✅ **BELOW CRITICAL threshold** (<1000 lines)

### Estimated Effort

- **Analysis:** 0.5 hours (completed in this session)
- **Condensing Step 4:** 1 hour (careful condensing of examples)
- **Condensing Step 6:** 1 hour (condense validation + gate presentation)
- **Validation:** 0.5 hours
- **Total:** 3 hours

### Implementation Commands

```bash
cd feature-updates/guides_v2/stages/s4

# Step 1: Backup
cp s4_epic_testing_strategy.md s4_epic_testing_strategy.md.backup

# Step 2: Replace sections using Edit tool
# Replace Step 4 (lines ~374-580)
# Replace Step 6 (lines ~701-1060)

# Step 3: Validate
wc -l s4_epic_testing_strategy.md  # Should be ~885 lines
git diff s4_epic_testing_strategy.md | head -100

# Step 4: Optional - create reference file for full examples
# Create reference/stage_4/test_scenario_templates.md with all 6 example scenarios
```

---

## Session 2 Summary

### Files Analyzed (3 of 9 remaining)

| File | Current | Target | Reduction | Strategy | Effort |
|------|---------|--------|-----------|----------|--------|
| s1_epic_planning.md | 1116 | 992 | -124 (11%) | Condense parallelization | 3h |
| s2_p3_refinement.md | 1106 | 1015 | -91 (8%) | Condense Phase 6 + parallel | 3h |
| s4_epic_testing_strategy.md | 1060 | 885 | -175 (17%) | Condense examples + validation | 3h |

**Total Reduction Across 3 Files:** -390 lines
**Total Execution Effort:** 9 hours

### Remaining Files to Analyze (6 files)

**Session 3:** Files 6-8 (s5 iteration files)
- stages/s5/s5_p1_i3_integration.md (1239 lines)
- stages/s5/s5_p3_i1_preparation.md (1145 lines)
- stages/s5/s5_p3_i2_gates_part1.md (1155 lines)

**Session 4:** Files 9-11 (s3, s8, glossary)
- stages/s3/s3_cross_feature_sanity_check.md (1354 lines)
- stages/s8/s8_p2_epic_testing_update.md (1344 lines)
- reference/glossary.md (1446 lines)

**Session Time:** 1.5 hours analysis complete

---

**Next Action:** Proceed to Session 3 analysis (files 6-8) OR begin Stage 3 execution for files 3-5

**Recommendation:** Complete Session 3 and 4 analyses first (another 3-4 hours) to have complete reduction plans for all files before beginning Stage 3 execution.

**Total Remaining Analysis:** 2 sessions × 1.5-2 hours = 3-4 hours

---

**Session 2 Planning Complete**
**Date:** 2026-02-05
**Auditor:** Claude (Primary Agent)
**Status:** D10 Round 1 - Stage 2 Analysis: 5/11 files complete (45%)
