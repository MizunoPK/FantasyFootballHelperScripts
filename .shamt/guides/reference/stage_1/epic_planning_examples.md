# Epic Planning Examples

**Purpose:** Detailed real-world examples of feature breakdowns, epic analysis, and planning scenarios
**Prerequisites:** S1 overview read from s1_epic_planning.md
**Main Guide:** `stages/s1/s1_epic_planning.md`

---

## Table of Contents

1. [Real-World Examples](#real-world-examples)
   - [Example 1: Good Feature Breakdown](#example-1-good-feature-breakdown)
   - [Example 2: Bad Feature Breakdown](#example-2-bad-feature-breakdown)
   - [Example 3: Feature vs Epic Confusion](#example-3-feature-vs-epic-confusion)
   - [Example 4: Session Compaction Recovery](#example-4-session-compaction-recovery)
   - [Example 5: Epic Ticket Example - Feature 02](#example-5-epic-ticket-example---feature-02)
   - [Example 6: Multi-Feature Epic Analysis](#example-6-multi-feature-epic-analysis)
   - [Example 7: Epic Ticket Template - Standard](#example-7-epic-ticket-template---standard)
   - [Example 8: Feature Breakdown Presentation](#example-8-feature-breakdown-presentation)
   - [Example 9: Common Breakdown Scenarios](#example-9-common-breakdown-scenarios)
   - [Example 10: Epic Size Classification](#example-10-epic-size-classification)

---

## Real-World Examples

### Example 1: Good Feature Breakdown

**Epic Request:** "Improve recommendation engine with more data sources"

**GOOD Breakdown:**
```text
Feature 1: Rank Data Integration
- Purpose: Load external ranking data from external API
- Scope: API client, data normalization, storage
- Dependencies: None (foundation)
- Estimate: ~25 items, MEDIUM risk

Feature 2: Expert Rankings Integration
- Purpose: Integrate consensus expert rankings
- Scope: Load rankings, calculate consensus, apply multiplier
- Dependencies: None (parallel to Feature 1)
- Estimate: ~20 items, LOW risk

Feature 3: Attribute Risk Assessment
- Purpose: Evaluate attribute history and calculate penalty
- Scope: Parse attribute data, calculate risk score, apply penalty
- Dependencies: None (parallel to Features 1, 2)
- Estimate: ~15 items, LOW risk

Feature 4: Scoring Engine Updates
- Purpose: Integrate new data sources into [domain algorithm]
- Scope: Update RecordManager, add new multipliers, integration tests
- Dependencies: Features 1, 2, 3 (consumes their outputs)
- Estimate: ~30 items, HIGH risk (integration complexity)
```

**Why GOOD:**
- Each feature delivers independent value
- Clear boundaries (data loading vs integration)
- Logical dependency chain (parallel data loading, then integration)
- Risk levels identified
- Foundation features (1, 2, 3) can be tested independently

---

### Example 2: Bad Feature Breakdown

**Epic Request:** "Improve recommendation engine with more data sources"

**BAD Breakdown:**
```text
Feature 1: Data Stuff
- Purpose: Get data
- Scope: All data things
- Dependencies: None
- Estimate: Unknown

Feature 2: Calculations
- Purpose: Do the calculations
- Scope: Math and stuff
- Dependencies: Feature 1
- Estimate: Unknown

Feature 3: Miscellaneous
- Purpose: Other improvements
- Scope: Whatever's left
- Dependencies: Features 1, 2
- Estimate: Unknown
```

**Why BAD:**
- Vague purposes ("data stuff", "calculations")
- No clear boundaries (what's in Feature 1 vs 2?)
- No testability (how do you verify "math and stuff"?)
- Unknown estimates (no analysis)
- Generic "miscellaneous" feature (dumping ground)

---

### Example 3: Feature vs Epic Confusion

**Request:** "Add JSON export for record data"

**WRONG (treating as multi-feature epic):**
```text
Feature 1: JSON Serialization
Feature 2: File Writing
Feature 3: Export Command
```

**RIGHT (single feature, not epic):**
```text
This is a single feature, not an epic requiring multiple features.

Create: .shamt/epics/json_export_feature/
Not: .shamt/epics/json_export_epic/feature_01_serialization/
```

**Why:** JSON export is small, tightly coupled, <20 items. Breaking into multiple features adds unnecessary overhead.

---

### Example 4: Session Compaction Recovery

**Scenario:** Agent started S1, then session compacted mid-Phase 3.

**WRONG Approach:**
```text
"I'll just continue creating features"
(Skips re-reading guide, doesn't check Agent Status)
```

**RIGHT Approach:**
```text
1. Read EPIC_README.md Agent Status
   - Sees: "Current Step: Phase 3 - Waiting for user approval"
   - Sees: "Blockers: Waiting for user confirmation of feature breakdown"

2. Read stages/s1/s1_epic_planning.md (this guide)
   - Re-read Phase 3 section
   - See requirement: WAIT for approval

3. Check conversation history
   - Find: Feature breakdown was proposed
   - Find: User has NOT yet responded

4. Correct action: Continue waiting
   - Update Agent Status: "Guide Last Read: {new timestamp} (RE-READ after compaction)"
   - Do NOT proceed without approval
```

---

### Example 5: Epic Ticket Example - Feature 02

**Epic Request:** "Integrate JSON record data into simulations"

**Epic Ticket:**

```markdown
## Epic Ticket: Integrate JSON Record Data into Simulations

## Description
Replace CSV-based record data loading with JSON format for both processing modules. The new JSON files contain weekly arrays instead of individual columns, enabling more efficient data organization and week-based queries across all {N} processing periods.

## Acceptance Criteria
- [ ] Both processing modules load data from JSON files
- [ ] All {N} periods of data are accessible and used correctly for both modules
- [ ] Actual points for all records across all {N} periods contain realistic non-zero values
- [ ] Projected values for all records across all {N} periods contain realistic non-zero values
- [ ] Processing produces equivalent or better results compared to baseline
- [ ] No regression in existing functionality
- [ ] All unit tests continue to pass

## Success Indicators
- Actual values have <1% zero values across all periods/records
- Projected values have <1% zero values across all periods/records
- Error metric calculations complete successfully for all {N} periods
- Processing completes {N} iterations without errors
- Standard deviation > 0 for both actual and projected values (values have variance)

## Failure Patterns
❌ >90% of actual_values are 0.0 (data loading issue)
❌ Only last 1-2 periods work while other periods have zeros (offset bug)
❌ Calculations return NaN or skip all records (consumption code not updated)
❌ "attribute not found" errors during execution (old API still used)
❌ Mean or standard deviation = 0 (all same value - calculation error)
❌ Only 1-2 records have non-zero values out of {N} total
```

**Why this would have caught Feature 02 bug:**
- "All {N} periods" makes clear it's not just week 17-18
- Failure pattern explicitly describes the ">90% zeros" bug that happened
- Success indicators would have failed (99.8% zeros >> 1% threshold)

---

### Example 6: Multi-Feature Epic Analysis

**Epic Request:** "Add trend projections feature"

**Phase 2 Analysis:**

**What problem is this solving?**
Users cannot predict trend outcomes or evaluate trend scenarios during the season.

**Explicit goals:**
1. Project trend bracket based on current standings
2. Calculate trend probabilities for each team
3. Show strength of schedule for target periods
4. Recommend roster moves optimized for trends

**Constraints:**
- Must use existing data (no new external APIs)
- Target periods only (configurable window)
- N-entity trend bracket (standard format)

**Out of scope:**
- Historical trend analysis
- Multi-tenant comparisons
- Custom bracket sizes

**Components Affected:**
- EntityManager ([module]/classes/[EntityClass].py)
- ConfigManager ([module]/util/ConfigManager.py)
- New TrendProjector module (to be created)
- Calculation engine ([module]/core/) - may need feature-specific logic

**Similar Existing Features:**
- Starter helper mode (similar projection logic)
- Schedule strength analyzer (similar data requirements)

**Scope Assessment:**
- Size: MEDIUM (estimated 3-4 features)
- Complexity: MODERATE
- Risk Level: MEDIUM
- Estimated Components: 4-5 classes/modules affected

---

### Example 7: Epic Ticket Template - Standard

```markdown
## Epic Ticket: [Epic Name]

## Description
[2-3 sentences describing what this epic achieves and why it matters]

## Acceptance Criteria (Epic-level)
- [ ] [Testable outcome 1 - applies to ENTIRE epic]
- [ ] [Testable outcome 2]
- [ ] [Testable outcome 3]
- [ ] [Testable outcome 4]

## Success Indicators
- [Measurable metric 1]
- [Measurable metric 2]
- [Measurable metric 3]

## Failure Patterns (How we'd know epic failed)
❌ [Symptom of failure 1]
❌ [Symptom of failure 2]
❌ [Symptom of failure 3]
```

**Guidelines for writing epic ticket:**

**Description:**
- Focus on WHAT is being achieved, not HOW
- Explain why this epic provides value
- Keep to 2-3 sentences maximum

**Acceptance Criteria:**
- Must be testable/verifiable outcomes
- Apply to entire epic (not individual features)
- Use "All X" language when patterns apply broadly (e.g., "All {N} periods", "All 6 positions")
- Avoid implementation details ("Create class X", "Use method Y")
- Focus on capabilities ("System can...", "Users can...", "Data shows...")

**Success Indicators:**
- Must be measurable/quantifiable
- Examples: "Zero percentage <1%", "All tests pass", "MAE calculation completes"
- Include both positive indicators (what should happen) and thresholds

**Failure Patterns:**
- Describe specific symptoms that would indicate epic failed
- Use patterns from similar past bugs if applicable
- Be explicit about edge cases (e.g., ">90% zeros", "Only week 17-18 work")
- Think: "What would I see in the output if this epic was broken?"

---

### Example 8: Feature Breakdown Presentation

**Presentation to User:**

```markdown
I've analyzed the epic request and propose breaking this into 4 features:

## Proposed Feature Breakdown

### Feature 1: Rank Data Integration
**Purpose:** Load and normalize external ranking data from API
**Scope:**
- Create API client for ranking data source
- Normalize rank values across different scoring formats
- Store rank data in item records
**Dependencies:** None (foundation feature)
**Estimate:** ~25 items, MEDIUM risk

### Feature 2: Expert Rankings Integration
**Purpose:** Integrate consensus expert rankings into item evaluations
**Scope:**
- Fetch expert rankings from multiple sources
- Calculate weighted consensus rankings
- Apply expert consensus multiplier to item scores
**Dependencies:** None (parallel to Feature 1)
**Estimate:** ~20 items, LOW risk

### Feature 3: Attribute Risk Assessment
**Purpose:** Evaluate item attribute history and calculate risk penalties
**Scope:**
- Parse attribute report data
- Calculate attribute risk score based on severity and frequency
- Apply risk penalty to item scores
**Dependencies:** None (parallel to Features 1, 2)
**Estimate:** ~15 items, LOW risk

### Feature 4: Scoring Engine Updates
**Purpose:** Integrate new data sources into item recommendation algorithm
**Scope:**
- Update RecordManager to consume rank, context, attribute data
- Add new multipliers to [domain algorithm]
- Create integration tests for end-to-end workflow
**Dependencies:** Features 1, 2, 3 (consumes all three outputs)
**Estimate:** ~30 items, HIGH risk (integration complexity)

## Rationale

**Why 4 features?**
- Each data source (rank, context, attribute) is independent and can be tested separately
- Parallel development possible for Features 1, 2, 3
- Clear integration point (Feature 4) consumes all data sources
- Foundation features establish data pipeline before integration

**Alternative considered:** 2 features (data loading + integration)
- Rejected because: Mixing three different data sources in one feature would create unclear boundaries and harder testing

## Recommended Implementation Order

1. Feature 1, 2, 3 (parallel - no dependencies, can implement in any order)
2. Feature 4 (depends on Features 1, 2, 3 being complete)

**Please review and let me know:**
- Are these the right feature boundaries?
- Should any features be combined or split?
- Are the dependencies correct?
- Should we add or remove any features?
```

---

### Example 9: Common Breakdown Scenarios

**Scenario A: Data Pipeline Epic**

**Pattern:**
```text
Feature 1: Data Ingestion (fetch/load)
Feature 2: Data Transformation (normalize/clean)
Feature 3: Data Storage (persist)
Feature 4: Data Consumption (integrate into existing features)
```

**When to use:** Epic involves new external data source being added to system

---

**Scenario B: UI Enhancement Epic**

**Pattern:**
```text
Feature 1: Backend API Updates (new endpoints/data)
Feature 2: UI Components (new interactive elements)
Feature 3: Workflow Integration (connect to existing modes)
Feature 4: User Preferences (settings/configuration)
```

**When to use:** Epic adds new user-facing capabilities to existing modes

---

**Scenario C: Algorithm Improvement Epic**

**Pattern:**
```text
Feature 1: Algorithm Core Logic (new calculation method)
Feature 2: Parameter Tuning (configuration/optimization)
Feature 3: Validation Framework (testing/benchmarking)
Feature 4: Production Integration (replace old algorithm)
```

**When to use:** Epic improves existing calculations or introduces new mathematical approach

---

**Scenario D: Cross-System Integration Epic**

**Pattern:**
```text
Feature 1: Module A Changes (updates to first system)
Feature 2: Module B Changes (updates to second system)
Feature 3: Shared Infrastructure (common utilities/interfaces)
Feature 4: Integration Layer (connects A and B via shared infrastructure)
```

**When to use:** Epic requires changes across multiple independent subsystems

---

### Example 10: Epic Size Classification

**SMALL Epic (1-2 features):**
```text
Epic: "Add CSV export for team rosters"

Feature 1: CSV Export Utility
- CSV serialization
- File writing
- Export command

Total estimate: ~15 items
Time: 1-2 days
```

**Why SMALL:** Single, focused capability with minimal cross-system impact

---

**MEDIUM Epic (3-5 features):**
```text
Epic: "Improve recommendation engine with more data sources"

Feature 1: Rank Data Integration (~25 items)
Feature 2: Expert Rankings Integration (~20 items)
Feature 3: Attribute Risk Assessment (~15 items)
Feature 4: Scoring Engine Updates (~30 items)

Total estimate: ~90 items
Time: 1-2 weeks
```

**Why MEDIUM:** Multiple independent data sources requiring integration

---

**LARGE Epic (6+ features):**
```text
Epic: "Add multi-tenant account support"

Feature 1: Multi-Year Entity Tracking (~40 items)
Feature 2: New Entity Onboarding (~35 items)
Feature 3: Subscription Management (~30 items)
Feature 4: Budget Limit Tracking (~25 items)
Feature 5: Subscription Renewal Logic (~20 items)
Feature 6: Account-Specific Scoring (~30 items)
Feature 7: Integration with Existing Modes (~40 items)

Total estimate: ~220 items
Time: 3-4 weeks
```

**Why LARGE:** Multiple complex subsystems, many cross-feature dependencies, high integration complexity

---

*End of reference/stage_1/epic_planning_examples.md*
