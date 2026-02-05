# S2 Refinement Phase - Phase 4 Examples: Dynamic Scope Adjustment

**Guide Version:** 1.0
**Created:** 2026-02-05 (Split from refinement_examples.md)
**Purpose:** Detailed examples for Phase 4 (Dynamic Scope Adjustment)
**Prerequisites:** Read stages/s2/s2_p3_refinement.md Phase 4 first
**Main Guide:** stages/s2/s2_p3_refinement.md
**Parent Reference:** reference/stage_2/refinement_examples.md

---

## Purpose

This reference provides detailed examples specifically for **Phase 4: Dynamic Scope Adjustment** of the Refinement Phase (S2.P3).

**What's Covered:**
- Feature too large - proposing splits (examples with justification)
- New work discovered - creating separate features
- Scope reduction strategies
- Communication patterns for scope changes

**When to Use:** During S2.P3 Phase 4 when evaluating feature scope and determining if adjustments are needed

**Always read the main guide first.** This is a reference supplement, not a standalone guide.

---

## Phase 4 Examples: Dynamic Scope Adjustment

### Example 1: Feature Too Large (>35 Items) - Propose Split

```markdown
## Feature Scope Analysis: Feature 02 (Trade Analyzer)

**Current Status:**
- Checklist items: 42 items
- Threshold: 35 items (maximum for maintainability)
- **Assessment:** ⚠️ Feature is too large

**Why This Matters:**
- Features with >35 items are difficult to implement systematically
- Testing becomes complex (too many edge cases)
- Higher risk of bugs and missed requirements
- S5 implementation planning becomes unwieldy

**Checklist Breakdown:**
- Data loading: 8 items
- Trade evaluation logic: 12 items
- Multi-player trade handling: 15 items
- UI integration: 7 items

**Proposed Split:**

I recommend splitting this into 2 separate features:

**Feature 02a: Basic Trade Evaluator**
- Scope: 1-for-1 and 2-for-2 trades (simpler cases)
- Checklist items: ~20 items
- Includes:
  - Data loading (8 items)
  - Basic trade evaluation logic (7 items)
  - UI integration for simple trades (5 items)
- Rationale: Foundational functionality, most common use case

**Feature 02b: Multi-Player Trade Support**
- Scope: Complex trades (3+ players per side)
- Checklist items: ~15 items
- Includes:
  - Multi-player evaluation logic (10 items)
  - Advanced UI for complex trades (5 items)
- Rationale: Advanced functionality, builds on 02a
- Dependency: Must implement 02a first

**Benefits of Split:**
- ✅ Each feature <35 items (manageable scope)
- ✅ Clear dependency (02a → 02b)
- ✅ Can deliver basic functionality sooner
- ✅ Easier to test and validate each piece

**Dependencies:**
- Feature 02a: Independent (can start now)
- Feature 02b: Depends on 02a (implement after 02a complete)
- No circular dependencies

**Next Steps If Approved:**
1. Return to S1 to create new feature folders
   - `feature_02a_basic_trade_evaluator/`
   - `feature_02b_multi_player_trades/`
2. Split current spec.md and checklist.md
   - Move items 1-20 to 02a
   - Move items 21-35 to 02b
3. Update epic EPIC_README.md Feature Tracking table
4. Continue S2 for Feature 02a (implement first)
5. Then S2 for Feature 02b (implement second)

**Do you approve this split?** (or suggest alternative grouping)
```

**If user approves:**

```markdown
✅ User approved split on 2026-01-10

**Actions Taken:**
1. Created new feature folders:
   - feature_02a_basic_trade_evaluator/
   - feature_02b_multi_player_trades/
2. Split spec.md content:
   - 02a: Basic evaluation logic (20 items)
   - 02b: Multi-player support (15 items)
3. Updated EPIC_README.md Feature Tracking:
   | Feature | Name | S2 Complete |
   |---------|------|------------------|
   | 02a | Basic Trade Evaluator | [ ] |
   | 02b | Multi-Player Trades | [ ] |
4. Updated feature dependencies in specs

**Next Steps:**
- Resume S2 for Feature 02a (Research Phase)
- Complete 02a through S5
- Then begin S2 for Feature 02b
```

---

### Example 2: New Work Discovered - Create Separate Feature

```markdown
## New Work Discovered: Player Name Matching Utility

**What We Found:**

During question resolution for Feature 01 (ADP Integration), we discovered a need for player name matching logic. User confirmed need to:
- Normalize player names (remove periods, extra spaces)
- Handle common variations ("A.J. Brown" vs "AJ Brown")
- Match across multiple data sources (ADP CSV, injury reports, etc.)

**Current Feature:**
Feature 01: ADP Integration
- Original scope: Load ADP data, integrate into scoring
- Current checklist: 18 items

**New Work:**
Player Name Matching Utility
- Normalize names for consistent matching
- Handle initials, spacing variations, suffixes (Jr., Sr.)
- Provide utility function used by multiple features
- Estimated: 10-15 checklist items

**Assessment:**

This new work should be its own feature because:
1. **Independent subsystem:** Can be developed and tested independently
2. **Reusable:** Will be used by multiple features:
   - Feature 01: ADP Integration (match ADP CSV to players)
   - Feature 02: Injury Risk (match injury reports to players)
   - Feature 03: Schedule Strength (match team schedules to players)
3. **Clear interface:** Single utility function with well-defined inputs/outputs
4. **Testing isolation:** Can thoroughly test matching logic separately

**Recommendation:**

Create new Feature 05: Player Name Matching Utility

**Scope:**
- Name normalization function
- Matching algorithm (exact after normalization)
- Unit tests for various name formats
- Documentation of supported variations

**Dependencies:**
- Feature 01 will DEPEND on Feature 05
- Feature 02 will DEPEND on Feature 05
- Feature 03 will DEPEND on Feature 05
- Should implement Feature 05 FIRST (before 01, 02, 03)

**Impact on Current Feature (01):**
- Reduces Feature 01 scope by ~5 items (matching logic moved to 05)
- Feature 01 checklist goes from 18 → 13 items
- Feature 01 will call utility from Feature 05

**Alternative:**

Keep matching logic in Feature 01:
- Pros: Keeps all ADP logic together
- Cons: Duplicated code when Features 02 and 03 need same logic
- Cons: Harder to maintain (changes in 3 places)

**Do you want to create this as a separate feature?** (or keep in Feature 01)
```

**If user approves new feature:**

```markdown
✅ User approved separate feature on 2026-01-10

**Actions Taken:**
1. Created new feature folder:
   - feature_05_player_name_matching/
2. Updated EPIC_README.md Feature Tracking:
   | Feature | Name | S2 Complete | Priority |
   |---------|------|------------------|----------|
   | 05 | Player Name Matching | [ ] | HIGH (blocks 01,02,03) |
   | 01 | ADP Integration | [ ] | MEDIUM (after 05) |
   | 02 | Injury Risk | [ ] | MEDIUM (after 05) |
3. Updated feature dependencies:
   - Feature 01 spec.md: Added "Depends on: Feature 05"
   - Feature 02 spec.md: Added "Depends on: Feature 05"
   - Feature 05 spec.md: Added "Blocks: Features 01, 02, 03"
4. Reduced Feature 01 scope:
   - Removed 5 matching-related checklist items
   - Updated requirement to use utility from Feature 05
   - New checklist count: 13 items

**Next Steps:**
- Begin S2 for Feature 05 (high priority, blocks others)
- Complete Feature 05 through S5
- Then resume Feature 01 (can now use matching utility)
```

---

## Phase 5 Examples: Cross-Feature Alignment
