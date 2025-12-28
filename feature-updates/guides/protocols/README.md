# Protocol Reference - Index

This folder contains detailed protocol definitions referenced during feature development. Each protocol is in its own file for easy reference.

---

## Quick Protocol Lookup

| Protocol | When to Execute | File |
|----------|-----------------|------|
| **Cheat Sheet** | Quick reference during development | [This file](#protocol-quick-reference-cheat-sheet) |
| **Verification Failure** | When any iteration finds issues | [verification_failure.md](verification_failure.md) |
| **Anti-Patterns** | Learn from common mistakes | [anti_patterns.md](anti_patterns.md) |
| Standard Verification | Iterations 1-3, 8-10, 15-16 | [standard_verification.md](standard_verification.md) |
| Algorithm Traceability Matrix | Iterations 4, 11, 19 | [algorithm_traceability_matrix.md](algorithm_traceability_matrix.md) |
| TODO Specification Audit | Iteration 4a (NEW) | [todo_specification_audit.md](todo_specification_audit.md) |
| End-to-End Data Flow | Iterations 5, 12 | [end_to_end_data_flow.md](end_to_end_data_flow.md) |
| Skeptical Re-verification | Iterations 6, 13, 22 | [skeptical_reverification.md](skeptical_reverification.md) |
| Integration Gap Check | Iterations 7, 14, 23 | [integration_gap_check.md](integration_gap_check.md) |
| Fresh Eyes Review | Iterations 17, 18 | [fresh_eyes_review.md](fresh_eyes_review.md) |
| Pre-Implementation Spec Audit | Iteration 23a (NEW) | [pre_implementation_spec_audit.md](pre_implementation_spec_audit.md) |
| Edge Case Verification | Iteration 20 | [edge_case_verification.md](edge_case_verification.md) |
| Test Coverage Planning + Mock Audit | Iteration 21 | [test_coverage_planning.md](test_coverage_planning.md) |
| Implementation Readiness | Iteration 24 | [implementation_readiness.md](implementation_readiness.md) |
| Interface Verification | Before implementation | [interface_verification.md](interface_verification.md) |
| Smoke Testing | Before declaring complete | [smoke_testing.md](smoke_testing.md) |
| Requirement Verification | Before marking complete | [requirement_verification.md](requirement_verification.md) |
| Quality Control Review | After implementation | [quality_control_review.md](quality_control_review.md) |
| Lessons Learned | Ongoing + before completion | [lessons_learned.md](lessons_learned.md) |
| Guide Update | After QA complete | [guide_update.md](guide_update.md) |
| Pre-commit Validation | Before any commit | [pre_commit_validation.md](pre_commit_validation.md) |

---

## Protocol Quick Reference (Cheat Sheet)

Use this table for fast lookup during development:

| Iteration | Protocol | Key Action | Output |
|-----------|----------|------------|--------|
| 1-3 | Standard | Read → Question → Research → Update | TODO updates |
| 4 | Algorithm Traceability | Map spec algorithms to code locations | Traceability Matrix |
| 4a | TODO Specification Audit | Add acceptance criteria to TODO items | TODO with criteria |
| 5 | End-to-End Data Flow | Trace entry → output | Data Flow Traces |
| 6 | Skeptical Re-verification | Challenge ALL assumptions | Verification Results |
| 7 | Integration Gap Check | Every method needs a caller | Integration Matrix |
| 8-10 | Standard | Re-verify with user answers | TODO updates |
| 11 | Algorithm Traceability | Re-verify algorithms with answers | Matrix updates |
| 12 | End-to-End Data Flow | Re-trace with answers | Trace updates |
| 13 | Skeptical Re-verification | Challenge answer interpretations | Verification Results |
| 14 | Integration Gap Check | Final caller verification | Matrix updates |
| 15-16 | Standard | Final preparation | Integration checklist |
| 17-18 | Fresh Eyes | Re-read spec as if first time | Gap identification |
| 19 | Algorithm Deep Dive | Quote exact spec text | Algorithm verification |
| 20 | Edge Case | Each edge case → task + test | Edge case matrix |
| 21 | Test Coverage + Mock Audit | Plan behavior tests, audit mocks | Test plan |
| 22 | Skeptical Re-verification | Final assumption challenge | Confidence assessment |
| 23 | Integration Gap Check | Final orphan code check | Clean matrix |
| 23a | Pre-Implementation Spec Audit | 4-part fresh-eyes audit: Coverage, Clarity, Structure, Mapping | Audit report |
| 24 | Implementation Readiness | Final go/no-go checklist (REQUIRES 23a PASS) | READY or BLOCKED |

---

## Protocols by Phase

### Planning Phase
- [verification_failure.md](verification_failure.md) - What to do when iterations find issues

### TODO Creation Phase (24 Iterations)
**Round 1 (Iterations 1-7):**
- [standard_verification.md](standard_verification.md) - Iterations 1-3
- [algorithm_traceability_matrix.md](algorithm_traceability_matrix.md) - Iteration 4
- [todo_specification_audit.md](todo_specification_audit.md) - Iteration 4a
- [end_to_end_data_flow.md](end_to_end_data_flow.md) - Iteration 5
- [skeptical_reverification.md](skeptical_reverification.md) - Iteration 6
- [integration_gap_check.md](integration_gap_check.md) - Iteration 7

**Round 2 (Iterations 8-16):**
- [standard_verification.md](standard_verification.md) - Iterations 8-10
- [algorithm_traceability_matrix.md](algorithm_traceability_matrix.md) - Iteration 11
- [end_to_end_data_flow.md](end_to_end_data_flow.md) - Iteration 12
- [skeptical_reverification.md](skeptical_reverification.md) - Iteration 13
- [integration_gap_check.md](integration_gap_check.md) - Iteration 14
- [standard_verification.md](standard_verification.md) - Iterations 15-16

**Round 3 (Iterations 17-24):**
- [fresh_eyes_review.md](fresh_eyes_review.md) - Iterations 17-18
- [algorithm_traceability_matrix.md](algorithm_traceability_matrix.md) - Iteration 19
- [edge_case_verification.md](edge_case_verification.md) - Iteration 20
- [test_coverage_planning.md](test_coverage_planning.md) - Iteration 21
- [skeptical_reverification.md](skeptical_reverification.md) - Iteration 22
- [integration_gap_check.md](integration_gap_check.md) - Iteration 23
- [pre_implementation_spec_audit.md](pre_implementation_spec_audit.md) - Iteration 23a
- [implementation_readiness.md](implementation_readiness.md) - Iteration 24

### Implementation Phase
- [interface_verification.md](interface_verification.md) - Before coding begins
- [requirement_verification.md](requirement_verification.md) - Continuous verification

### Post-Implementation Phase
- [smoke_testing.md](smoke_testing.md) - 3-part mandatory testing
- [quality_control_review.md](quality_control_review.md) - QC Rounds 1-3
- [requirement_verification.md](requirement_verification.md) - Final check

### Completion Phase
- [lessons_learned.md](lessons_learned.md) - Document improvements
- [guide_update.md](guide_update.md) - Update guides
- [pre_commit_validation.md](pre_commit_validation.md) - Before committing

---

## How to Use These Protocols

1. **During TODO Creation:** Reference protocols by iteration number
2. **During Implementation:** Use continuous verification protocols
3. **During QC:** Follow post-implementation protocols sequentially
4. **When Blocked:** Check verification_failure.md for guidance
5. **Learning:** Review anti_patterns.md to avoid common mistakes

---

## Related Files

- `../todo_creation_guide.md` - References these protocols during 24 iterations
- `../implementation_execution_guide.md` - Uses verification protocols
- `../post_implementation_guide.md` - Uses QC and smoke testing protocols
- `../templates.md` - Templates for matrices and checklists
