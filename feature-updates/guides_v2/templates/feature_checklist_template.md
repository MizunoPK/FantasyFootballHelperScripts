# Feature Checklist Template

**Filename:** `checklist.md`
**Location:** `feature-updates/{epic_name}/feature_XX_{name}/checklist.md`
**Created:** Stage 2 (Feature Deep Dive)

**Purpose:** Track resolved vs pending decisions during Stage 2 (Feature Deep Dive).

---

## Template

```markdown
# Feature Checklist: {feature_name}

**Part of Epic:** {epic_name}
**Last Updated:** {YYYY-MM-DD}

---

## Purpose

This checklist tracks decisions and open items for the feature. Items marked `[x]` are resolved. Items marked `[ ]` are pending.

**Stage 2 (Feature Deep Dive) is complete when ALL items are marked `[x]`.**

---

## Functional Decisions

- [x] Feature scope defined
- [x] Functional requirements documented (spec.md)
- [ ] {Pending decision 1}
- [ ] {Pending decision 2}

---

## Technical Decisions

- [x] Algorithms defined and documented
- [x] Data structures specified
- [x] Interfaces designed
- [ ] {Pending technical decision 1}
- [ ] {Pending technical decision 2}

---

## Integration Decisions

- [x] Integration points identified
- [x] Data flow documented
- [ ] {Pending integration decision}

---

## Error Handling Decisions

- [x] Error scenarios identified
- [x] Error handling strategy defined
- [ ] {Pending error handling decision}

---

## Testing Decisions

- [x] Unit test strategy defined
- [x] Integration test strategy defined
- [x] Smoke test scenarios identified
- [ ] {Pending testing decision}

---

## Open Questions

- [ ] {Open question 1 - needs answer before implementation}
- [ ] {Open question 2}

{When all questions resolved, mark them [x]}

---

## Dependencies

- [x] Feature 01 interface verified (if depends on other features)
- [ ] {Pending dependency verification}

{If no dependencies: "No dependencies"}

---

## Stage 2 Completion Status

**Total Items:** {N}
**Resolved:** {X}
**Pending:** {Y}

**Stage 2 Complete?** {YES (all items [x]) / NO (Y items pending)}

**If NO, do NOT proceed to Stage 5a until all items resolved.**
```