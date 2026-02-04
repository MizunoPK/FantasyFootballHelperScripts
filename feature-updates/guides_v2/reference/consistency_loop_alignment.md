# Consistency Loop: Cross-Feature Alignment Context

**Master Protocol:** See `consistency_loop_protocol.md`

**Context:** S2.P1.I1 per-feature alignment, S2.P1.I3 per-feature alignment, S2.P2 group alignment

---

## What's Being Validated

Cross-feature consistency and compatibility including:
- Naming conventions across features
- Implementation approaches
- Data structures and formats
- Pattern consistency
- Integration points between features

---

## What Counts as "Issue"

An issue in alignment context is any of:
- **Naming conflicts:** Same name used for different purposes across features
- **Contradictory approaches:** Features solving similar problems differently
- **Incompatible data structures:** Features expecting different formats
- **Pattern inconsistencies:** One feature uses pattern X, another uses pattern Y for same problem
- **Integration mismatches:** Features have incompatible integration points
- **Shared resource conflicts:** Features accessing shared resources inconsistently

---

## Fresh Eyes Patterns Per Round

### Round 1: Forward Pairwise Comparison
**Pattern:**
1. Compare features in sequential order (F1 vs F2, F2 vs F3, etc.)
2. Check for naming conflicts
3. Check for approach contradictions
4. Check for data structure incompatibilities
5. Document ALL conflicts found

**Checklist:**
- [ ] No naming conflicts found
- [ ] No contradictory approaches found
- [ ] No incompatible data structures found
- [ ] Consistent patterns across features
- [ ] Integration points identified

### Round 2: Reverse Pairwise Comparison
**Pattern:**
1. Compare features in reverse order (FN vs FN-1, FN-1 vs FN-2, etc.)
2. Different comparison perspective from Round 1
3. Check integration points from opposite direction
4. Verify shared resource usage
5. Document ALL conflicts found

**Checklist:**
- [ ] Reverse comparison reveals no new conflicts
- [ ] Integration points work bidirectionally
- [ ] Shared resources accessed consistently
- [ ] Error handling approaches aligned
- [ ] Logging/telemetry patterns consistent

### Round 3: Random Pairs + Thematic Clustering
**Pattern:**
1. Random spot-check 5 feature pairs
2. Thematic clustering (all data structures together, all error handling together, etc.)
3. Check for global pattern consistency
4. Verify all integration points work together
5. Document ALL conflicts found

**Checklist:**
- [ ] Random pairs show no conflicts
- [ ] Thematic analysis shows consistent patterns
- [ ] All integration points documented and compatible
- [ ] No global inconsistencies found
- [ ] Ready for implementation

---

## Specific Criteria

**All of these MUST pass for loop to exit:**
- [ ] No naming conflicts (same name = same meaning across all features)
- [ ] No approach conflicts (similar problems solved consistently)
- [ ] No data structure conflicts (compatible formats everywhere)
- [ ] Consistent patterns across features (error handling, logging, etc.)
- [ ] All integration points identified and compatible
- [ ] Shared resources accessed consistently
- [ ] No contradictions found in any direction (forward/reverse/random)

---

## Example Round Sequence

```
Round 1: Forward pairwise (F1 vs F2, F2 vs F3)
- Compare F1 and F2: Found naming conflict ("session" means different things)
- Fix: Rename F1's "session" to "user_session", F2's "session" to "game_session"
- Compare F2 and F3: Found data structure conflict (date format)
- Fix: Standardize on ISO 8601 format across both
- Continue to Round 2

Round 2: Reverse pairwise (F3 vs F2, F2 vs F1)
- Compare F3 and F2: Integration point unclear (how F3 calls F2)
- Fix: Document integration in both specs
- Compare F2 and F1: Error handling approaches differ
- Fix: Align error handling patterns
- Continue to Round 3

Round 3: Random pairs + thematic
- Random check F1 vs F3: 0 issues found
- Thematic check (all data structures): 0 issues found
- Thematic check (all error handling): 0 issues found
- Continue (count = 1 clean)

Round 4: Repeat validation
- Check: 0 issues found → Continue (count = 2 clean)

Round 5: Final sweep
- Check: 0 issues found → PASSED (count = 3 consecutive clean)
```

---

## Common Issues in Alignment Context

1. **Naming conflicts:** F1 uses "player" for PlayerData, F2 uses "player" for PlayerID → Rename for clarity
2. **Approach conflicts:** F1 uses async/await, F2 uses callbacks → Standardize approach
3. **Data structure conflicts:** F1 expects JSON, F2 produces CSV → Add conversion layer or standardize
4. **Pattern inconsistencies:** F1 logs errors to file, F2 logs to console → Standardize logging
5. **Integration mismatches:** F1 exports function X, F2 expects function Y → Align interfaces

---

## Integration with Stages

**S2.P1.I1 Per-Feature Alignment:**
- Use this protocol after researching each feature
- Validate new feature aligns with existing features
- Must pass before proceeding to S2.P1.I2

**S2.P1.I3 Per-Feature Alignment:**
- Use this protocol after spec refinement for each feature
- Validate spec aligns with all existing feature specs
- Must pass before proceeding to S2.P2

**S2.P2 Group Alignment:**
- Use this protocol for all features together
- Pairwise comparison of all feature pairs
- Must pass before S3 (cross-feature sanity check)

---

## Exit Criteria Specific to Alignment

**Can only exit when ALL true:**
- [ ] 3 consecutive rounds found zero issues
- [ ] No naming conflicts across any features
- [ ] No approach contradictions across any features
- [ ] All data structures compatible
- [ ] All integration points identified and compatible
- [ ] Consistent patterns across all features
- [ ] Ready for next stage

---

**Remember:** Follow all 7 principles from master protocol. This guide only specifies HOW to apply them in alignment context, not WHETHER to apply them.
