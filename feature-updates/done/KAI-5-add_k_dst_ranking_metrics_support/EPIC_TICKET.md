# Epic Ticket: Add K and DST Support to Ranking Metrics

## Description
Add Kicker (K) and Defense/Special Teams (DST) positions to ranking-based accuracy metrics in the accuracy simulation. Currently, only QB/RB/WR/TE are evaluated using pairwise accuracy (primary metric), while K/DST are limited to MAE-only evaluation. This epic completes the accuracy metrics by including all 6 roster positions in ranking quality assessment.

## Acceptance Criteria (Epic-level)
- [ ] Research phase identifies ALL code locations requiring changes (minimum 2 known: AccuracyCalculator.py lines 258, 544)
- [ ] K and DST included in positions list for ranking metric calculations
- [ ] K and DST included in position_data dictionary for cross-season aggregation
- [ ] Pairwise accuracy calculated and reported for K and DST positions
- [ ] Top-N accuracy (top-5, top-10, top-20) calculated and reported for K and DST positions
- [ ] Spearman correlation calculated and reported for K and DST positions
- [ ] AccuracyResult.by_position dictionary includes 'K' and 'DST' keys with metrics
- [ ] Logs display K/DST ranking metrics during accuracy simulation runs
- [ ] Saved optimal config files include K/DST metrics in by_position section
- [ ] All unit tests pass (100% pass rate) including new K/DST test cases
- [ ] Documentation updated to reflect all 6 positions in ranking metrics

## Success Indicators
- Research findings document identifies all hardcoded position lists (no locations missed)
- K/DST metrics appear in simulation output logs with realistic values
- by_position dictionary has 6 keys (QB, RB, WR, TE, K, DST) not 4
- Pairwise accuracy for K/DST is calculated (not skipped or errored)
- Top-N accuracy values for K/DST are present (even if lower due to small sample size)
- No crashes or NaN errors during full 16-parameter accuracy simulation
- Unit test coverage includes K-specific and DST-specific test cases

## Failure Patterns (How we'd know epic failed)
❌ Only 4 positions appear in by_position dict (K/DST silently dropped during aggregation)
❌ Simulation crashes with KeyError when accessing K or DST metrics
❌ K/DST metrics show as 0.0 or NaN (calculation error)
❌ Logs show "Calculating metrics for 4 positions" instead of 6
❌ Research phase misses hardcoded position lists, implementation incomplete
❌ Tests pass but K/DST data never actually flows through ranking calculations
❌ Documentation still claims "ranking metrics for QB/RB/WR/TE only"
❌ Saved config files have empty or missing K/DST entries in by_position
