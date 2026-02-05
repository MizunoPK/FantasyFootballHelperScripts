# Feature Breakdown Patterns

**Purpose:** Patterns and strategies for breaking epics into features with decision trees
**Prerequisites:** S1 overview read from s1_epic_planning.md
**Main Guide:** `stages/s1/s1_epic_planning.md`

---

## Feature Breakdown Criteria

**Each feature should:**

1. **Deliver distinct value** (user can describe benefit in 1 sentence)
2. **Be independently testable** (can verify without other features)
3. **Have clear boundaries** (knows what's in vs out of scope)
4. **Be reasonably sized** (20-50 implementation items estimate)
5. **Have defined dependencies** (knows what it needs from other features)

---

## Decision Tree: How Many Features?

```text
START: Analyze Epic Request
│
├─ Is this <20 implementation items?
│  └─ YES → This is a SINGLE FEATURE, not an epic
│           Create feature folder (not epic with features)
│
├─ Is this 20-50 items with single focus?
│  └─ YES → Consider 1-2 features
│           Split only if clear subsystem boundaries
│
├─ Is this 50-100 items with multiple concerns?
│  └─ YES → Consider 3-5 features
│           Split by data source, subsystem, or workflow phase
│
└─ Is this >100 items with complex integrations?
   └─ YES → Consider 6+ features
            Split by major subsystems, then integration layers
```markdown

---

## Pattern 1: Data Pipeline Epic

**Use when:** Epic involves new external data source

**Structure:**
```text
Feature 1: Data Ingestion
- Fetch/load from source
- Basic validation
- Error handling

Feature 2: Data Transformation
- Normalize formats
- Clean/sanitize
- Calculate derived fields

Feature 3: Data Storage
- Persist to appropriate format
- Update existing data structures
- Migration if needed

Feature 4: Data Consumption
- Integrate into existing features
- Update UI/reports
- End-to-end testing
```markdown

**Dependencies:**
```text
Feature 1 (ingestion)
    ↓
Feature 2 (transformation) ← depends on Feature 1
    ↓
Feature 3 (storage) ← depends on Feature 2
    ↓
Feature 4 (consumption) ← depends on Feature 3
```markdown

**Example:**
```text
Epic: "Add injury data tracking"

Feature 1: Injury Data Ingestion (fetch from injury API)
Feature 2: Injury Data Normalization (clean/categorize)
Feature 3: Injury Data Storage (add to player records)
Feature 4: Injury Risk Integration (use in recommendations)
```markdown

---

## Pattern 2: Algorithm Enhancement Epic

**Use when:** Epic improves calculation/scoring logic

**Structure:**
```text
Feature 1: Algorithm Core
- New calculation method
- Core logic implementation
- Unit tests for algorithm

Feature 2: Parameter Configuration
- Configuration options
- Tuning interface
- Default values

Feature 3: Validation Framework
- Benchmark against old method
- Accuracy tests
- Performance tests

Feature 4: Production Integration
- Replace old algorithm
- Migration path
- Fallback mechanism
```markdown

**Dependencies:**
```text
Feature 1 (core logic)
    ↓
Feature 2 (configuration) ← depends on Feature 1
    ↓
Feature 3 (validation) ← depends on Features 1, 2
    ↓
Feature 4 (integration) ← depends on Features 1, 2, 3
```markdown

**Example:**
```text
Epic: "Improve projection accuracy"

Feature 1: New Projection Algorithm (core math)
Feature 2: Projection Parameters (tuning options)
Feature 3: Accuracy Benchmarking (validation)
Feature 4: Replace Old Projections (integration)
```markdown

---

## Pattern 3: Multi-Source Data Epic

**Use when:** Epic adds multiple independent data sources

**Structure:**
```text
Feature 1: Data Source A Integration
- Source A ingestion
- Source A normalization
- Source A storage

Feature 2: Data Source B Integration
- Source B ingestion
- Source B normalization
- Source B storage

Feature 3: Data Source C Integration
- Source C ingestion
- Source C normalization
- Source C storage

Feature 4: Unified Consumption Layer
- Aggregate all sources
- Resolve conflicts
- Integration tests
```markdown

**Dependencies:**
```text
Feature 1, 2, 3 (parallel - independent sources)
    ↓
Feature 4 (aggregation) ← depends on Features 1, 2, 3
```markdown

**Example:**
```text
Epic: "Enhance player rankings"

Feature 1: ADP Integration (average draft position)
Feature 2: Expert Rankings Integration (consensus rankings)
Feature 3: Injury Risk Integration (injury data)
Feature 4: Combined Recommendation Engine (aggregate all)
```markdown

---

## Pattern 4: Cross-System Integration Epic

**Use when:** Epic requires changes across multiple subsystems

**Structure:**
```text
Feature 1: Subsystem A Updates
- Changes to System A
- System A tests
- System A backwards compatibility

Feature 2: Subsystem B Updates
- Changes to System B
- System B tests
- System B backwards compatibility

Feature 3: Shared Infrastructure
- Common interfaces
- Shared utilities
- Common data structures

Feature 4: Integration Layer
- Connect A and B via shared infrastructure
- End-to-end workflows
- Integration tests
```markdown

**Dependencies:**
```text
Feature 1, 2 (parallel - independent systems)
    ↓
Feature 3 (shared infrastructure) ← depends on Features 1, 2
    ↓
Feature 4 (integration) ← depends on Features 1, 2, 3
```markdown

**Example:**
```text
Epic: "Integrate draft helper with trade analyzer"

Feature 1: Draft Helper Updates (expose draft data)
Feature 2: Trade Analyzer Updates (expose trade logic)
Feature 3: Shared Player Evaluation (common utilities)
Feature 4: Draft-Trade Integration (connect both systems)
```markdown

---

## Pattern 5: UI Enhancement Epic

**Use when:** Epic adds new user-facing capabilities

**Structure:**
```text
Feature 1: Backend API Updates
- New endpoints
- Data models
- Business logic

Feature 2: UI Components
- New interactive elements
- Display logic
- Input validation

Feature 3: Workflow Integration
- Connect to existing modes
- Navigation updates
- User flows

Feature 4: User Preferences
- Settings/configuration
- Persistence
- User customization
```markdown

**Dependencies:**
```text
Feature 1 (backend)
    ↓
Feature 2 (UI components) ← depends on Feature 1
    ↓
Feature 3 (workflow integration) ← depends on Features 1, 2
    ↓
Feature 4 (preferences) ← depends on Features 1, 2, 3
```markdown

**Example:**
```text
Epic: "Add interactive draft board"

Feature 1: Draft State API (backend data/logic)
Feature 2: Draft Board UI (visual components)
Feature 3: Mode Integration (add to draft helper)
Feature 4: Draft Preferences (user settings)
```markdown

---

## Pattern 6: Refactoring Epic

**Use when:** Epic restructures existing code without adding features

**Structure:**
```text
Feature 1: Extract Common Utilities
- Identify shared code
- Create utility modules
- Update references

Feature 2: Consolidate Duplicates
- Find duplicate logic
- Merge into single implementation
- Update all callers

Feature 3: Improve Abstractions
- Define clear interfaces
- Implement abstractions
- Migrate to new abstractions

Feature 4: Remove Technical Debt
- Delete dead code
- Fix TODO items
- Update documentation
```markdown

**Dependencies:**
```text
Feature 1 (utilities) ← foundation
    ↓
Feature 2 (consolidate) ← depends on Feature 1
    ↓
Feature 3 (abstractions) ← depends on Features 1, 2
    ↓
Feature 4 (cleanup) ← depends on Features 1, 2, 3
```markdown

**Example:**
```text
Epic: "Refactor data loading architecture"

Feature 1: Common CSV Utilities (shared readers)
Feature 2: Consolidate Parsers (merge duplicate logic)
Feature 3: Data Loader Interface (new abstraction)
Feature 4: Remove Legacy Code (cleanup)
```markdown

---

## Common Breakdown Mistakes

### Mistake 1: Features Too Small

**BAD:**
```text
Feature 1: Create JSON serializer (5 items)
Feature 2: Add file writer (3 items)
Feature 3: Add export command (4 items)
```markdown

**WHY BAD:** Each feature is too small, high overhead for minimal scope

**BETTER:**
```text
Feature 1: JSON Export Capability (12 items)
- JSON serialization
- File writing
- Export command
```markdown

---

### Mistake 2: Features Too Large

**BAD:**
```text
Feature 1: Complete Draft Enhancement (150 items)
- ADP integration
- Expert rankings
- Injury risk
- Recommendation updates
```markdown

**WHY BAD:** Feature is too large, unclear boundaries, hard to test

**BETTER:**
```text
Feature 1: ADP Integration (25 items)
Feature 2: Expert Rankings (20 items)
Feature 3: Injury Risk (15 items)
Feature 4: Recommendation Engine (30 items)
```markdown

---

### Mistake 3: Vague Boundaries

**BAD:**
```text
Feature 1: Data Stuff
Feature 2: Calculations
Feature 3: Miscellaneous
```markdown

**WHY BAD:** No clear boundaries, "miscellaneous" is dumping ground

**BETTER:**
```text
Feature 1: Data Ingestion (clear scope: fetch/load)
Feature 2: Data Transformation (clear scope: normalize/clean)
Feature 3: Recommendation Updates (clear scope: integrate data)
```markdown

---

### Mistake 4: Missing Dependencies

**BAD:**
```text
Feature 1: Recommendation Engine (needs ADP data)
Feature 2: ADP Integration (provides ADP data)
```markdown

**WHY BAD:** Wrong order, Feature 1 can't work without Feature 2

**BETTER:**
```text
Feature 1: ADP Integration (foundation - no dependencies)
Feature 2: Recommendation Engine (depends on Feature 1)
```markdown

---

### Mistake 5: Circular Dependencies

**BAD:**
```text
Feature 1: Player Manager Updates (depends on Feature 2)
Feature 2: Draft Helper Updates (depends on Feature 1)
```markdown

**WHY BAD:** Cannot determine implementation order

**BETTER:**
```text
Feature 1: Shared Player Utilities (foundation - no dependencies)
Feature 2: Player Manager Updates (depends on Feature 1)
Feature 3: Draft Helper Updates (depends on Features 1, 2)
```markdown

---

## Decision Framework: Split or Combine?

### When to SPLIT features:

✅ **Split if:**
- Different subsystems/modules affected
- Different data sources
- Different testing strategies
- Can implement in parallel
- Clear dependency boundary
- Each delivers independent value

**Example:**
```text
COMBINED (BAD): "Data Integration" (ADP + Rankings + Injuries)
SPLIT (GOOD):
- Feature 1: ADP Integration
- Feature 2: Expert Rankings Integration
- Feature 3: Injury Risk Integration
```markdown

---

### When to COMBINE features:

✅ **Combine if:**
- Tightly coupled (can't test one without other)
- Very small scope (<15 items total)
- Single responsibility
- No clear boundary between them
- Dependencies force sequential implementation anyway

**Example:**
```text
SPLIT (BAD):
- Feature 1: JSON Parser (3 items)
- Feature 2: File Writer (2 items)

COMBINED (GOOD): "JSON Export" (5 items)
```markdown

---

## Feature Naming Conventions

### Pattern: `feature_{NN}_{descriptive_name}`

**GOOD Names:**
```text
feature_01_adp_integration
feature_02_injury_risk_assessment
feature_03_recommendation_engine_updates
```markdown

**BAD Names:**
```text
feature_1_data (not zero-padded, too vague)
feature_02_improvements (too vague)
feature_03_misc (not descriptive)
feature_04_FeatureStuff (not snake_case)
```markdown

---

### Naming Guidelines:

1. **Use zero-padded numbers** (01, 02, 03) for consistent sorting
2. **Use snake_case** (not camelCase or kebab-case)
3. **Be specific** (not "updates", "improvements", "misc")
4. **Keep concise** (2-4 words max)
5. **Match epic domain** (if epic is "draft_helper", features should relate to drafting)

**Examples:**

```text
Epic: improve_draft_helper

✅ GOOD:
- feature_01_adp_integration
- feature_02_injury_assessment
- feature_03_schedule_analysis

❌ BAD:
- feature_1_data
- feature_02_stuff
- feature_03_DraftHelperImprovements
```markdown

---

## Dependency Patterns

### Pattern A: Sequential Chain

```text
Feature 1 → Feature 2 → Feature 3 → Feature 4
```markdown

**Use when:** Each feature builds on previous
**Example:** Data pipeline (ingest → transform → store → consume)

---

### Pattern B: Parallel + Integration

```text
Feature 1 ─┐
Feature 2 ─┼→ Feature 4
Feature 3 ─┘
```markdown

**Use when:** Multiple independent sources + integration layer
**Example:** Multi-source data epic (ADP, rankings, injuries → combined engine)

---

### Pattern C: Shared Foundation

```text
        Feature 1 (foundation)
           ↓        ↓
    Feature 2    Feature 3
```markdown

**Use when:** Multiple features depend on common infrastructure
**Example:** Shared utilities → subsystem A, subsystem B

---

### Pattern D: Diamond

```text
       Feature 1
      ↓         ↓
Feature 2    Feature 3
      ↓         ↓
       Feature 4
```markdown

**Use when:** Two parallel tracks converge to integration
**Example:** Backend updates + UI updates → workflow integration

---

## Estimating Feature Size

### Small Feature (15-25 items)

**Characteristics:**
- Single file or small module
- Focused responsibility
- Minimal cross-system impact
- 1-2 days implementation

**Example:**
```python
Feature: CSV Export Utility
- Create CSVExporter class (3 items)
- Add serialization methods (4 items)
- File writing logic (3 items)
- Error handling (2 items)
- Unit tests (8 items)
Total: ~20 items
```markdown

---

### Medium Feature (25-50 items)

**Characteristics:**
- Multiple files or module
- Moderate integration
- Cross-module dependencies
- 3-5 days implementation

**Example:**
```text
Feature: ADP Integration
- API client (5 items)
- Data normalization (6 items)
- Storage updates (5 items)
- PlayerManager integration (4 items)
- Configuration (3 items)
- Unit tests (12 items)
- Integration tests (5 items)
Total: ~40 items
```markdown

---

### Large Feature (50-80 items)

**Characteristics:**
- Multiple modules
- High complexity
- Many integration points
- 1-2 weeks implementation

**Example:**
```text
Feature: Recommendation Engine Overhaul
- Algorithm redesign (10 items)
- Data aggregation (8 items)
- Scoring logic (12 items)
- PlayerManager updates (6 items)
- Configuration system (5 items)
- UI updates (4 items)
- Unit tests (20 items)
- Integration tests (10 items)
Total: ~75 items
```markdown

---

### Very Large Feature (>80 items)

**⚠️ WARNING:** Features >80 items should be split

**If you estimate >80 items:**
1. Re-evaluate boundaries
2. Look for natural split points
3. Consider subsystems as separate features
4. Ask: "Can this be 2-3 smaller features?"

---

## Implementation Order Strategies

### Strategy 1: Foundation First

**Pattern:** Build infrastructure before features that use it

```text
Order:
1. Shared utilities
2. Data ingestion
3. Data transformation
4. Consumer features
```markdown

**Use when:** Multiple features depend on common infrastructure

---

### Strategy 2: Vertical Slice

**Pattern:** Complete one end-to-end workflow before adding more

```text
Order:
1. Core feature with basic integration
2. Enhancement feature A
3. Enhancement feature B
4. Optimization features
```markdown

**Use when:** Want working end-to-end functionality early

---

### Strategy 3: Risk-First

**Pattern:** Implement highest-risk features first

```text
Order:
1. HIGH RISK feature (unknown complexity)
2. MEDIUM RISK features
3. LOW RISK features
```markdown

**Use when:** Want to validate feasibility early

---

### Strategy 4: User-Value First

**Pattern:** Implement features with highest user value first

```text
Order:
1. HIGH VALUE feature (most requested)
2. MEDIUM VALUE features
3. LOW VALUE features (nice-to-have)
```

**Use when:** Want to deliver value incrementally

---

*End of reference/stage_1/feature_breakdown_patterns.md*
