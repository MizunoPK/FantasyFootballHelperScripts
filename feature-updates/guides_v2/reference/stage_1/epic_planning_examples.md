# Epic Planning Examples

**Purpose:** Detailed real-world examples of feature breakdowns, epic analysis, and planning scenarios
**Prerequisites:** S1 overview read from s1_epic_planning.md
**Main Guide:** `stages/s1/s1_epic_planning.md`

---

## Real-World Examples

### Example 1: Good Feature Breakdown

**Epic Request:** "Improve draft helper with more data sources"

**GOOD Breakdown:**
```text
Feature 1: ADP Integration
- Purpose: Load average draft position data from external API
- Scope: API client, data normalization, storage
- Dependencies: None (foundation)
- Estimate: ~25 items, MEDIUM risk

Feature 2: Expert Rankings Integration
- Purpose: Integrate consensus expert rankings
- Scope: Load rankings, calculate consensus, apply multiplier
- Dependencies: None (parallel to Feature 1)
- Estimate: ~20 items, LOW risk

Feature 3: Injury Risk Assessment
- Purpose: Evaluate injury history and calculate penalty
- Scope: Parse injury data, calculate risk score, apply penalty
- Dependencies: None (parallel to Features 1, 2)
- Estimate: ~15 items, LOW risk

Feature 4: Recommendation Engine Updates
- Purpose: Integrate new data sources into scoring algorithm
- Scope: Update PlayerManager, add new multipliers, integration tests
- Dependencies: Features 1, 2, 3 (consumes their outputs)
- Estimate: ~30 items, HIGH risk (integration complexity)
```bash

**Why GOOD:**
- Each feature delivers independent value
- Clear boundaries (data loading vs integration)
- Logical dependency chain (parallel data loading, then integration)
- Risk levels identified
- Foundation features (1, 2, 3) can be tested independently

---

### Example 2: Bad Feature Breakdown

**Epic Request:** "Improve draft helper with more data sources"

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
```markdown

**Why BAD:**
- Vague purposes ("data stuff", "calculations")
- No clear boundaries (what's in Feature 1 vs 2?)
- No testability (how do you verify "math and stuff"?)
- Unknown estimates (no analysis)
- Generic "miscellaneous" feature (dumping ground)

---

### Example 3: Feature vs Epic Confusion

**Request:** "Add JSON export for player data"

**WRONG (treating as multi-feature epic):**
```text
Feature 1: JSON Serialization
Feature 2: File Writing
Feature 3: Export Command
```markdown

**RIGHT (single feature, not epic):**
```text
This is a single feature, not an epic requiring multiple features.

Create: feature-updates/json_export_feature/
Not: feature-updates/json_export_epic/feature_01_serialization/
```markdown

**Why:** JSON export is small, tightly coupled, <20 items. Breaking into multiple features adds unnecessary overhead.

---

### Example 4: Session Compaction Recovery

**Scenario:** Agent started S1, then session compacted mid-Phase 3.

**WRONG Approach:**
```text
"I'll just continue creating features"
(Skips re-reading guide, doesn't check Agent Status)
```markdown

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
```markdown

---

### Example 5: Epic Ticket Example - Feature 02

**Epic Request:** "Integrate JSON player data into simulations"

**Epic Ticket:**

```markdown
# Epic Ticket: Integrate JSON Player Data into Simulations

## Description
Replace CSV-based player data loading with JSON format for both win rate and accuracy simulations. The new JSON files contain weekly arrays instead of individual columns, enabling more efficient data organization and week-based queries across all 18 NFL regular season weeks.

## Acceptance Criteria
- [ ] Both simulation types (win rate & accuracy) load player data from JSON files
- [ ] All 18 weeks of data are accessible and used correctly for both simulations
- [ ] Actual points for all players across all 18 weeks contain realistic non-zero values
- [ ] Projected points for all players across all 18 weeks contain realistic non-zero values
- [ ] Simulations produce equivalent or better results compared to CSV version
- [ ] No regression in existing simulation functionality
- [ ] All 2,200+ unit tests continue to pass

## Success Indicators
- Actual points have <1% zero values across all weeks/players
- Projected points have <1% zero values across all weeks/players
- Mean absolute error (MAE) calculations complete successfully for all 18 weeks
- Win rate simulations complete 10,000 iterations without errors
- Standard deviation > 0 for both actual and projected points (values have variance)

## Failure Patterns
❌ >90% of actual_points are 0.0 (data loading issue)
❌ Only week 17-18 work while other weeks have zeros (week offset bug)
❌ Calculations return NaN or skip all players (consumption code not updated)
❌ "attribute not found" errors during execution (old API still used)
❌ Mean or standard deviation = 0 (all same value - calculation error)
❌ Only 1-2 players have non-zero values out of 2500 total
```markdown

**Why this would have caught Feature 02 bug:**
- "All 18 weeks" makes clear it's not just week 17-18
- Failure pattern explicitly describes the ">90% zeros" bug that happened
- Success indicators would have failed (99.8% zeros >> 1% threshold)

---

### Example 6: Multi-Feature Epic Analysis

**Epic Request:** "Add playoff projections feature"

**Phase 2 Analysis:**

**What problem is this solving?**
Users cannot predict playoff outcomes or evaluate playoff scenarios during the season.

**Explicit goals:**
1. Project playoff bracket based on current standings
2. Calculate playoff probabilities for each team
3. Show strength of schedule for playoff weeks (14-17)
4. Recommend roster moves optimized for playoffs

**Constraints:**
- Must use existing league data (no new APIs)
- Playoff weeks only (weeks 14-17)
- 6-team playoff bracket (standard format)

**Out of scope:**
- Historical playoff analysis
- Multi-league comparisons
- Custom bracket sizes

**Components Affected:**
- FantasyTeam (league_helper/classes/FantasyTeam.py)
- ConfigManager (league_helper/util/ConfigManager.py)
- New PlayoffProjector module (to be created)
- Simulator (simulation/) - may need playoff-specific logic

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
# Epic Ticket: [Epic Name]

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
```markdown

**Guidelines for writing epic ticket:**

**Description:**
- Focus on WHAT is being achieved, not HOW
- Explain why this epic provides value
- Keep to 2-3 sentences maximum

**Acceptance Criteria:**
- Must be testable/verifiable outcomes
- Apply to entire epic (not individual features)
- Use "All X" language when patterns apply broadly (e.g., "All 18 weeks", "All 6 positions")
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

### Feature 1: ADP Integration
**Purpose:** Load and normalize average draft position data from external API
**Scope:**
- Create API client for ADP data source
- Normalize ADP values across different scoring formats
- Store ADP data in player records
**Dependencies:** None (foundation feature)
**Estimate:** ~25 items, MEDIUM risk

### Feature 2: Expert Rankings Integration
**Purpose:** Integrate consensus expert rankings into player evaluations
**Scope:**
- Fetch expert rankings from multiple sources
- Calculate weighted consensus rankings
- Apply expert consensus multiplier to player scores
**Dependencies:** None (parallel to Feature 1)
**Estimate:** ~20 items, LOW risk

### Feature 3: Injury Risk Assessment
**Purpose:** Evaluate player injury history and calculate risk penalties
**Scope:**
- Parse injury report data
- Calculate injury risk score based on severity and frequency
- Apply risk penalty to player scores
**Dependencies:** None (parallel to Features 1, 2)
**Estimate:** ~15 items, LOW risk

### Feature 4: Recommendation Engine Updates
**Purpose:** Integrate new data sources into draft recommendation algorithm
**Scope:**
- Update PlayerManager to consume ADP, rankings, injury data
- Add new multipliers to scoring algorithm
- Create integration tests for end-to-end workflow
**Dependencies:** Features 1, 2, 3 (consumes all three outputs)
**Estimate:** ~30 items, HIGH risk (integration complexity)

## Rationale

**Why 4 features?**
- Each data source (ADP, rankings, injury) is independent and can be tested separately
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
```markdown

---

### Example 9: Common Breakdown Scenarios

**Scenario A: Data Pipeline Epic**

**Pattern:**
```text
Feature 1: Data Ingestion (fetch/load)
Feature 2: Data Transformation (normalize/clean)
Feature 3: Data Storage (persist)
Feature 4: Data Consumption (integrate into existing features)
```markdown

**When to use:** Epic involves new external data source being added to system

---

**Scenario B: UI Enhancement Epic**

**Pattern:**
```text
Feature 1: Backend API Updates (new endpoints/data)
Feature 2: UI Components (new interactive elements)
Feature 3: Workflow Integration (connect to existing modes)
Feature 4: User Preferences (settings/configuration)
```markdown

**When to use:** Epic adds new user-facing capabilities to existing modes

---

**Scenario C: Algorithm Improvement Epic**

**Pattern:**
```text
Feature 1: Algorithm Core Logic (new calculation method)
Feature 2: Parameter Tuning (configuration/optimization)
Feature 3: Validation Framework (testing/benchmarking)
Feature 4: Production Integration (replace old algorithm)
```markdown

**When to use:** Epic improves existing calculations or introduces new mathematical approach

---

**Scenario D: Cross-System Integration Epic**

**Pattern:**
```text
Feature 1: Module A Changes (updates to first system)
Feature 2: Module B Changes (updates to second system)
Feature 3: Shared Infrastructure (common utilities/interfaces)
Feature 4: Integration Layer (connects A and B via shared infrastructure)
```markdown

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
```bash

**Why SMALL:** Single, focused capability with minimal cross-system impact

---

**MEDIUM Epic (3-5 features):**
```text
Epic: "Improve draft helper with more data sources"

Feature 1: ADP Integration (~25 items)
Feature 2: Expert Rankings Integration (~20 items)
Feature 3: Injury Risk Assessment (~15 items)
Feature 4: Recommendation Engine Updates (~30 items)

Total estimate: ~90 items
Time: 1-2 weeks
```markdown

**Why MEDIUM:** Multiple independent data sources requiring integration

---

**LARGE Epic (6+ features):**
```text
Epic: "Add dynasty league support"

Feature 1: Multi-Year Player Tracking (~40 items)
Feature 2: Rookie Draft System (~35 items)
Feature 3: Contract Management (~30 items)
Feature 4: Salary Cap Tracking (~25 items)
Feature 5: Keeper Selection Logic (~20 items)
Feature 6: Dynasty-Specific Scoring (~30 items)
Feature 7: Integration with Existing Modes (~40 items)

Total estimate: ~220 items
Time: 3-4 weeks
```

**Why LARGE:** Multiple complex subsystems, many cross-feature dependencies, high integration complexity

---

*End of reference/stage_1/epic_planning_examples.md*
