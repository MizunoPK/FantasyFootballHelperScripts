# S2 Parallelization Decision Tree

**Purpose:** Reference guide for determining S2 parallelization mode and group assignment
**Audience:** Primary agents during S1 Step 5.7-5.9 (dependency analysis and parallelization offering)
**Status:** Reference documentation (not mandatory workflow guide)

---

## Decision Tree Flowchart

**START: Features created in S1**
```text
Q1: Does epic have 3+ features?
├─ NO → Sequential S2 (no parallelization offered)
│        ↓
│        Proceed to S2 with sequential mode
│
└─ YES → Continue to Q2
        ↓
Q2: User accepted parallel work offering?
├─ NO → Sequential S2
│        ↓
│        Proceed to S2 with sequential mode
│
└─ YES → Continue to Q3
        ↓
Q3: Do any features have spec-level dependencies?
├─ NO → Full Parallelization Mode
│        ↓
│        All features in Group 1 (single wave)
│        All features do S2 simultaneously
│        Guide: parallel_work/s2_primary_agent_guide.md
│
└─ YES → Group-Based Parallelization Mode
         ↓
         Organize into dependency groups
         Each group completes S2 before next group starts
         Within each group: features parallelize
         Guide: parallel_work/s2_primary_agent_group_wave_guide.md
```

---

## Dependency Type Identification

### Spec-Level Dependency (Affects S2)

**Definition:** Feature B needs Feature A's SPEC to write its own spec

**Example:**
```text
Feature A: Create logging infrastructure with setup_logger() API
Feature B: Integrate script with logging infrastructure

Feature B dependency:
- Needs to know setup_logger() function signature to write integration spec
- Needs to know folder structure to document file paths
- Must reference Feature A's spec during research

Result: Feature B has SPEC-LEVEL dependency on Feature A
Impact: Feature A must complete S2 before Feature B starts S2
```

**Detection Questions:**
1. Does Feature B need to reference Feature A's API during spec writing?
2. Does Feature B need to know Feature A's folder structure?
3. Does Feature B's spec require examples from Feature A's spec?
4. Would Feature B's research be incomplete without Feature A's spec?

**If YES to any:** Spec-level dependency exists

---

### Implementation Dependency (Affects S5-S8, NOT S2)

**Definition:** Feature B needs Feature A's CODE to build its implementation

**Example:**
```text
Feature A: Create logging infrastructure with setup_logger() function
Feature B: Integrate script with logging infrastructure

Feature B dependency:
- Calls setup_logger() function in code
- Imports from Feature A's module
- Requires Feature A's code to exist before building integration

Result: Feature B has IMPLEMENTATION dependency on Feature A
Impact: Feature A must complete S5-S8 before Feature B starts S5-S8
       BUT: Both can do S2 in parallel (specs don't require code)
```

**Detection Questions:**
1. Does Feature B import from Feature A's modules?
2. Does Feature B call Feature A's functions?
3. Does Feature B extend Feature A's classes?
4. Would Feature B's code fail to run without Feature A's code?

**If YES to any:** Implementation dependency exists (doesn't affect S2)

---

### Common Mistake: Confusing the Two

**WRONG:**
```text
Feature B calls Feature A's code
→ Agent thinks: "Feature B depends on Feature A"
→ Agent puts them in different S2 groups
→ Result: Unnecessary serialization, lost time savings
```

**CORRECT:**
```text
Feature B calls Feature A's code (implementation dependency)
BUT: Feature B can write its spec without Feature A's spec
→ Agent thinks: "No spec-level dependency"
→ Agent puts both in Group 1
→ Result: Both do S2 in parallel, save time
```

**Key Principle:** Only SPEC-LEVEL dependencies affect S2 grouping

---

## Group Assignment Examples

### Example 1: All Independent Features (Single Wave)

**Epic:** Player data enhancements (3 features)

**Features:**
- Feature 01: Add JSON export for player data
- Feature 02: Add CSV import for player data
- Feature 03: Add data validation rules

**Dependency Analysis:**
- Feature 01: No spec dependencies (new export feature)
- Feature 02: No spec dependencies (new import feature)
- Feature 03: No spec dependencies (new validation feature)
- All features work on same data structure but don't reference each other

**Group Assignment:**
```markdown
**Group 1 (All Features - Single S2 Wave):**
- Feature 01: JSON export
- Feature 02: CSV import
- Feature 03: Validation rules
- Spec Dependencies: None (all independent)
- S2 Workflow: All 3 features do S2 simultaneously (2 hours total)
```

**Time Savings:** 6 hours → 2 hours (67% reduction)

---

### Example 2: Foundation + Dependent Features (2 Waves)

**Epic:** Logging refactoring (7 features) - KAI-8 actual case

**Features:**
- Feature 01: Core logging infrastructure (LineBasedRotatingHandler, setup_logger API)
- Features 02-07: Script-specific logging integrations

**Dependency Analysis:**
- Feature 01: No spec dependencies (defines the API)
- Features 02-07: Spec-level dependency on Feature 01
  - Need to know setup_logger() signature
  - Need to know folder structure (logs/{script_name}/)
  - Need to reference Feature 01 spec during integration spec writing

**Group Assignment:**
```markdown
**Group 1 (Foundation - S2 Wave 1):**
- Feature 01: core_logging_infrastructure
- Spec Dependencies: None
- S2 Workflow: Completes S2 alone FIRST (2 hours)

**Group 2 (Dependent Scripts - S2 Wave 2):**
- Features 02-07: All script logging integrations
- Spec Dependencies: Need Feature 01's spec (API reference, folder structure)
- S2 Workflow: After Group 1 S2 complete, all 6 features do S2 in parallel (2 hours)

**Total S2 Time:** 4 hours (Wave 1: 2h + Wave 2: 2h)
**Sequential Would Be:** 14 hours (7 features × 2h)
**Time Savings:** 10 hours (71% reduction)
```

**Why Groups Matter:**
- Feature 02-07 specs reference setup_logger() API from Feature 01 spec
- Can't write integration specs without knowing what they're integrating with
- Once Feature 01 spec exists, all 6 can reference it simultaneously

---

### Example 3: Cascading Dependencies (3 Waves)

**Epic:** Multi-tier data pipeline (5 features)

**Features:**
- Feature 01: Raw data ingestion (API fetcher)
- Feature 02: Data transformation (depends on Feature 01 data format)
- Feature 03: Data validation (depends on Feature 02 transformed format)
- Feature 04: Data storage (independent database layer)
- Feature 05: Data export (depends on Feature 04 storage schema)

**Dependency Analysis:**
- Feature 01: No spec dependencies
- Feature 02: Spec-level dependency on Feature 01 (needs input data format)
- Feature 03: Spec-level dependency on Feature 02 (needs transformed data format)
- Feature 04: No spec dependencies (independent database layer)
- Feature 05: Spec-level dependency on Feature 04 (needs storage schema)

**Group Assignment:**
```markdown
**Group 1 (Foundation - S2 Wave 1):**
- Feature 01: Raw data ingestion
- Feature 04: Data storage
- Spec Dependencies: None (both independent)
- S2 Workflow: Both do S2 in parallel (2 hours)

**Group 2 (Dependent on Group 1 - S2 Wave 2):**
- Feature 02: Data transformation (depends on Feature 01)
- Feature 05: Data export (depends on Feature 04)
- Spec Dependencies: Need Group 1's specs
- S2 Workflow: After Group 1 S2 complete, both do S2 in parallel (2 hours)

**Group 3 (Dependent on Group 2 - S2 Wave 3):**
- Feature 03: Data validation (depends on Feature 02)
- Spec Dependencies: Need Feature 02's spec
- S2 Workflow: After Group 2 S2 complete, Feature 03 does S2 alone (2 hours)

**Total S2 Time:** 6 hours (Wave 1: 2h + Wave 2: 2h + Wave 3: 2h)
**Sequential Would Be:** 10 hours (5 features × 2h)
**Time Savings:** 4 hours (40% reduction)
```

**Key Insight:** Even with 3 waves, still save 40% because some parallelization happens

---

## Common Mistakes

### Mistake 1: Confusing Implementation Dependencies with Spec Dependencies

**Scenario:**
```text
Feature A: Create authentication module
Feature B: Add user profile page (calls auth module)

Agent thinks: "Feature B calls Feature A's code, so B depends on A for S2"
Agent creates: Group 1 (Feature A), Group 2 (Feature B)
```

**Why Wrong:** Feature B can write its spec (design user profile page, document auth calls) without Feature A's code existing. Both specs can be written simultaneously.

**Correct Approach:**
```text
Agent asks: "Does Feature B need Feature A's SPEC to write its own spec?"
Answer: "No - Feature B knows it will call auth module, can document that in spec without seeing Feature A's spec"
Agent creates: Group 1 (Feature A + B) - both do S2 in parallel
```

**Time Impact:** Unnecessary serialization loses time savings

---

### Mistake 2: Over-Splitting Groups

**Scenario:**
```text
3 features, all independent
Agent creates: Group 1 (F1), Group 2 (F2), Group 3 (F3)
Agent reasons: "This gives me fine-grained control over sequencing"
```

**Why Wrong:** Groups exist for DEPENDENCY management, not control. All independent features should parallelize together.

**Correct Approach:**
```text
Agent asks: "Do any features have spec-level dependencies?"
Answer: "No - all independent"
Agent creates: Group 1 (F1 + F2 + F3) - all do S2 simultaneously
```

**Time Impact:** Over-splitting forces unnecessary waves, loses time savings

---

### Mistake 3: Assuming All Features Can Parallelize

**Scenario:**
```text
Agent sees: 5 features
Agent offers: "All 5 features can parallelize! Save 8 hours!"
User accepts
Agent spawns: 5 secondary agents immediately
Secondary agents: "I need Feature 01's spec to write mine..."
Result: Blocked agents, coordination chaos
```

**Why Wrong:** Skipped dependency analysis in S1 Step 5.7.5

**Correct Approach:**
```text
Agent performs: S1 Step 5.7.5 dependency analysis
Agent identifies: Features 02-05 depend on Feature 01
Agent creates: Group 1 (F01), Group 2 (F02-05)
Agent offers: "Group-based parallelization - save 6 hours"
Agent spawns: Secondaries AFTER Group 1 S2 complete
```

**Prevention:** Always complete S1 Step 5.7.5 before offering parallelization

---

### Mistake 4: Ignoring "After S2" Note

**Scenario:**
```text
Agent creates: Group 1 (Feature 01), Group 2 (Features 02-05)
Agent plans: "Group 1 completes S2→S3→S4, then Group 2 starts S2"
```

**Why Wrong:** Groups only matter for S2. After S2, workflow returns to epic-level (S3) then sequential per-feature (S4+)

**Correct Approach:**
```text
Agent plans:
- Wave 1: Group 1 completes S2 only
- Wave 2: Group 2 completes S2 only
- After ALL S2 done: Primary runs S3 (epic-level, all features together)
- After S3: Primary runs S4 for each feature (sequential, no groups)
```

**Key Principle:** Groups are S2-only constructs, don't extend to other stages

---

## Summary

**When to use this guide:**
- S1 Step 5.7.5: Analyzing feature dependencies
- S1 Step 5.9: Determining parallelization offering
- Complex cases: 3+ groups, cascading dependencies, mixed dependency types

**Quick reference:**
- Spec-level dependency → Different groups
- Implementation dependency only → Same group
- No dependencies → Group 1 (parallelize freely)
- Groups only matter for S2 (not S3-S10)

**See Also:**
- `stages/s1/s1_epic_planning.md` Step 5.7.5 (dependency analysis workflow)
- `parallel_work/s2_primary_agent_group_wave_guide.md` (group wave execution)
- `parallel_work/s2_primary_agent_guide.md` (full parallelization execution)
