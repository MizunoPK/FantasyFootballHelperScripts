# S5 v2 Quick Reference

**Purpose:** Quick lookup for S5 v2 Validation Loop structure and mapping from S5 v1 iterations

**Full Guide:** `stages/s5/s5_v2_validation_loop.md`

---

## S5 v2 Structure Overview

**Phase 1: Draft Creation (60-90 minutes)**
- Create complete implementation plan draft
- Focus on content, not perfection
- Output: `implementation_plan.md` (ready for validation)

**Phase 2: Validation Loop (3.5-6 hours, typically 6-8 rounds)**
- Systematic validation across 11 dimensions
- Fix ALL issues immediately (zero deferred issues)
- Exit criteria: 3 consecutive clean rounds (all dimensions passing)
- Maximum: 10 rounds (escalate to user if exceeded)

---

## The 11 Validation Dimensions

| # | Dimension | Focus Area | Key Checks |
|---|-----------|------------|------------|
| **D1** | Requirements Completeness | All spec items covered | Every requirement has implementation tasks |
| **D2** | Interface & Dependency Verification | Integration points correct | Verify all imports, method signatures, data contracts |
| **D3** | Algorithm Traceability | Logic implementation | Map each algorithm step to implementation tasks |
| **D4** | Task Specification Quality | Implementation clarity | Each task has clear what/how/output (Gate 3a) |
| **D5** | Data Flow & Consumption | Data transformation path | Track data from input → processing → output |
| **D6** | Error Handling & Edge Cases | Robustness coverage | Identify failure modes, validation, boundary cases |
| **D7** | Integration & Compatibility | Cross-feature coherence | Check for conflicts with existing features |
| **D8** | Test Coverage Quality | Testing comprehensiveness | Unit tests, integration tests, edge case tests |
| **D9** | Performance & Dependencies | Resource efficiency | Identify bottlenecks, unnecessary dependencies |
| **D10** | Implementation Readiness | Execution preparedness | Phasing, rollback plan, go/no-go checklist (Gate 24) |
| **D11** | Spec Alignment & Cross-Validation | Completeness verification | Final spec audit, no gaps (Gates 23a, 25) |

---

## S5 v1 to S5 v2 Migration Guide

### Complete Iteration Mapping

| S5 v1 Iteration | S5 v1 File Name | Focus | S5 v2 Dimension | S5 v2 Section |
|-----------------|-----------------|-------|-----------------|---------------|
| **Phase 1: Round 1 (Draft Creation)** |
| I1 | `s5_p1_i1_requirements.md` | Requirements coverage | **D1** | Requirements Completeness |
| I2 | `s5_p1_i2_algorithms.md` | Algorithm mapping | **D3** | Algorithm Traceability |
| I3 | `s5_p1_i3_integration.md` | Interface verification | **D2** | Interface & Dependency Verification |
| I4 (Gate 4a) | Embedded in I2 | TODO specification | **D4** | Task Specification Quality (Gate 3a) |
| I5 | `s5_p1_i3_iter5_dataflow.md` | Data transformations | **D5** | Data Flow & Consumption |
| I5a | `s5_p1_i3_iter5a_downstream.md` | Data consumers | **D5** | Data Flow & Consumption |
| I6 | `s5_p1_i3_iter6_errorhandling.md` | Error scenarios | **D6** | Error Handling & Edge Cases |
| I6a | `s5_p1_i3_iter6a_dependencies.md` | Dependencies audit | **D9** | Performance & Dependencies |
| I7 | `s5_p1_i3_iter7_integration.md` | Integration points | **D7** | Integration & Compatibility |
| I7a (Gate 7a) | `s5_p1_i3_iter7a_compatibility.md` | Backward compatibility | **D7** | Integration & Compatibility |
| **Phase 2: Round 2 (Verification)** |
| I8 | `s5_p2_i1_test_strategy.md` | Test coverage | **D8** | Test Coverage Quality |
| I9-16 | `s5_p2_i2_reverification.md` | Re-verify all aspects | **All Dimensions** | Validation Loop Round 1 |
| I16 | `s5_p2_i3_final_checks.md` | Final verification | **All Dimensions** | Validation Loop (mid-rounds) |
| **Phase 3: Round 3 (Final Review)** |
| I17 | `s5_p3_i1_iter17_phasing.md` | Implementation phases | **D10** | Implementation Readiness |
| I18 | `s5_p3_i1_iter18_rollback.md` | Rollback strategy | **D10** | Implementation Readiness |
| I19 | `s5_p3_i1_iter19_traceability.md` | Algorithm traceability | **D3** | Algorithm Traceability |
| I20 | `s5_p3_i1_iter20_performance.md` | Performance analysis | **D9** | Performance & Dependencies |
| I21 | `s5_p3_i1_iter21_mockaudit.md` | Mock spec audit | **D11** | Spec Alignment & Cross-Validation |
| I22 | `s5_p3_i1_iter22_consumers.md` | Data consumers | **D5** | Data Flow & Consumption |
| I23 (Gate 23a) | `s5_p3_i2_gates_part1.md` | Pre-implementation audit | **D11** | Spec Alignment (Gate 23a) |
| I24 (Gate 24) | `s5_p3_i3_gates_part2.md` | GO/NO-GO decision | **D10** | Implementation Readiness (Gate 24) |
| I25 (Gate 25) | `s5_p3_i3_gates_part2.md` | Spec validation check | **D11** | Spec Alignment (Gate 25) |

---

## Key Differences: V1 vs V2

### Structure
- **V1:** Linear 22 iterations (I1 → I2 → ... → I25)
- **V2:** Iterative validation loop (Draft → Validate 11 dimensions → Fix → Repeat until 3 clean rounds)

### Time
- **V1:** 9-11 hours (fixed iterations)
- **V2:** 4.5-7 hours typical (variable rounds based on quality)

### Quality Assurance
- **V1:** Sequential checks (could skip or defer issues)
- **V2:** Systematic validation with ZERO deferred issues, 3 consecutive clean rounds required

### File Structure
- **V1:** 25+ separate files (one per iteration)
- **V2:** 1 comprehensive guide (`s5_v2_validation_loop.md`)

---

## Common Mappings (Quick Lookup)

**Looking for Gates?**
- Gate 3a (TODO spec) → Dimension 4
- Gate 7a (Compatibility) → Dimension 7
- Gate 23a (Spec audit) → Dimension 11
- Gate 24 (GO/NO-GO) → Dimension 10
- Gate 25 (Spec validation) → Dimension 11

**Looking for specific checks?**
- Requirements coverage → D1
- Algorithm implementation → D3
- Interface verification → D2
- Data flow → D5
- Error handling → D6
- Test coverage → D8
- Performance → D9
- Integration points → D7
- Implementation readiness → D10
- Final spec alignment → D11

**Looking for task quality checks?**
- See Dimension 4 (Task Specification Quality)
- Embeds Gate 3a checks

---

## When to Reference This Guide

**Use this guide when:**
- Updating documentation that references S5 v1 files
- Migrating bug reports or lessons learned from S5 v1 format
- Understanding which dimension covers a specific S5 v1 iteration
- Creating new documentation that needs to reference S5 structure

**Primary Guide:**
- For actual S5 workflow: See `stages/s5/s5_v2_validation_loop.md`
- For migration details: See `stages/s5/S5_V1_TO_V2_MIGRATION.md`
- For S5 design rationale: See `stages/s5/S5_V2_DESIGN_PLAN.md`

---

## File Reference Format (Standard)

**When referencing S5 v2 in documentation:**

✅ **Correct format:**
- `stages/s5/s5_v2_validation_loop.md` (general reference)
- `stages/s5/s5_v2_validation_loop.md` (Dimension N) - when referring to specific dimension
- `stages/s5/s5_v2_validation_loop.md` (Gate Xa) - when referring to specific gate

❌ **Incorrect format (S5 v1):**
- `stages/s5/s5_p1_i1_requirements.md` (file doesn't exist)
- `stages/s5/s5_p3_i3_gates_part2.md` (file doesn't exist)
- Any reference to `s5_p[0-9]` files

---

## Cross-References

- **Full S5 v2 Guide:** `stages/s5/s5_v2_validation_loop.md`
- **Migration Guide:** `stages/s5/S5_V1_TO_V2_MIGRATION.md`
- **Design Plan:** `stages/s5/S5_V2_DESIGN_PLAN.md`
- **Prompts:** `prompts/s5_s8_prompts.md`
- **S5 Reference Card:** `reference/stage_5/stage_5_reference_card.md` (updated for v2)

---

**Last Updated:** 2026-02-10 (Round 5.1 audit fixes)
