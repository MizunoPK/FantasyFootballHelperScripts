# Player Rating Fixes - Questions for Clarification

Based on comprehensive codebase research (3 verification iterations), the following questions need clarification before implementation begins.

## Question 1: Normalization Formula Verification

**Context**: The specification says "A 1 should still be for the worst player, and a 100 should still be for the best player."

**Current Understanding**:
- Best player = lowest rank number (e.g., QB1)
- Worst player = highest rank number (e.g., QB50)
- Formula: `normalized = 1 + ((rank - max_rank) / (min_rank - max_rank)) * 99`

**Question**: Can you confirm this interpretation is correct?
- min_rank (e.g., 1.0 for QB1) → rating = 100
- max_rank (e.g., 50.0 for QB50) → rating = 1

**Options**:
A) Yes, this is correct (best = 100, worst = 1)
B) No, reverse it (best = 1, worst = 100)

**Recommendation**: Option A - matches existing 0-100 scale comment in player_data_models.py:45

---

## Question 2: Division by Zero Edge Case Handling

**Context**: When a position has only one player (or all players have the same rank), we get min_rank == max_rank, causing division by zero.

**Question**: What rating should be assigned in this edge case?

**Options**:
A) Set rating to 50.0 (neutral/middle value)
B) Set rating to 100.0 (treat single player as "best")
C) Set rating to None and use fallback calculation
D) Set rating to 1.0 (conservative approach)

**Recommendation**: Option A (50.0 neutral) - most mathematically sound and prevents bias

---

## Question 3: Old Method Removal Strategy

**Context**: The `_convert_positional_rank_to_rating()` method (espn_client.py:1168) implements the old tier-based system.

**Question**: Should this method be:

**Options**:
A) Completely removed (clean break, requires test updates)
B) Deprecated with warning (gradual transition, keeps tests)
C) Kept as fallback for players without rankings

**Recommendation**: Option A (remove) - cleaner codebase, existing fallback logic at lines 1486-1505 handles missing rankings

---

## Question 4: Simulation Script Execution

**Context**: Need to create normalize_player_ratings.py script to process backup CSV files.

**Question**: Should this normalization script:

**Options**:
A) Run automatically as part of existing workflow
B) Be a standalone script run manually when needed
C) Integrated into simulation setup/initialization

**Recommendation**: Option B (standalone manual script) - safer for one-time migration, can be deleted after use

---

## Question 5: CSV Backup Strategy

**Context**: Step 3.4 mentions creating backups before overwriting files.

**Question**: When writing new players_projected.csv and players_actual.csv, should we:

**Options**:
A) Create timestamped backups (e.g., players_projected_20251105.csv) before overwriting
B) Assume backup files already exist, directly overwrite
C) Prompt user before overwriting existing files

**Recommendation**: Option B (direct overwrite) - backup files already exist with "_backup" suffix, new files are the "production" versions

---

## Question 6: Test Failure Threshold

**Context**: The pre-commit protocol requires 100% test pass rate.

**Question**: If updating tests for new normalization logic, should we:

**Options**:
A) Update all tests before implementation (test-driven development)
B) Update tests alongside implementation (parallel development)
C) Update tests after implementation completes (implementation-first)

**Recommendation**: Option B (parallel) - update tests as each phase completes, verify immediately

---

## Question 7: Data Model Comment Update

**Context**: player_data_models.py:45 has comment "0-100 scale from ESPN position-specific consensus rankings"

**Question**: Should the comment be updated to:

**Options**:
A) "0-100 scale normalized from ESPN position-specific rankings (100=best, 1=worst within position)"
B) Keep existing comment (no change needed)
C) "0-100 scale with position-specific normalization"

**Recommendation**: Option A - provides clarity on normalization method and scale direction

---

## Question 8: Logging Verbosity During Development

**Context**: Added extensive DEBUG and INFO logging throughout implementation.

**Question**: Should the default logging level during development be:

**Options**:
A) DEBUG (very detailed, helps with troubleshooting)
B) INFO (milestones and progress, less verbose)
C) WARNING (only issues, minimal output)

**Recommendation**: Option B (INFO) - balances useful progress updates with manageable output volume

---

## Question 9: Phase 2 vs Phase 3 Execution Order

**Context**: Phase 2 (ESPN client) and Phase 3 (simulation CSV) are independent.

**Question**: Should implementation proceed:

**Options**:
A) Phase 2 first, then Phase 3 (sequential)
B) Phase 3 first, then Phase 2 (sequential, reverse order)
C) Both phases in parallel (faster but requires careful coordination)

**Recommendation**: Option A (Phase 2 first) - validates normalization logic on live data before applying to static CSV files

---

## Question 10: Fallback Behavior for Players Without Rankings

**Context**: Some players may not have positional_rank data from ESPN API.

**Question**: For players without positional_rank, should we:

**Options**:
A) Use existing fallback calculation (draft rank formula, lines 1486-1505)
B) Set player_rating to None (let downstream code handle it)
C) Assign a default low rating (e.g., 10.0)

**Recommendation**: Option A (use existing fallback) - preserves current behavior, provides reasonable estimates

---

## Summary

**Critical Questions** (blocking implementation):
- Question 1: Formula direction confirmation
- Question 2: Division by zero handling

**Important Questions** (affects architecture):
- Question 3: Old method removal strategy
- Question 4: Simulation script execution approach
- Question 9: Phase execution order

**Minor Questions** (preferences):
- Questions 5-8, 10: Can proceed with recommendations if no response

**Next Steps**:
After receiving answers, I will:
1. Update TODO file with user's chosen approaches (Step 4 of rules protocol)
2. Execute second verification round (3 more iterations)
3. Begin implementation with clear direction on all ambiguities
