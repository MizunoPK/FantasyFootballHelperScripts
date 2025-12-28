## Quality Control Round [N]
- Reviewed: [date/time]
- Issues Found: [list or "None"]

**Related:** [README.md](README.md) - Protocol index

---

- Issues Fixed: [list or "N/A"]
- Status: PASSED / ISSUES FOUND (fixed)
```

### Why 3 Rounds? (And Why You Cannot Skip Any)

Experience shows that:
- Round 1 catches obvious issues
- Round 2 catches algorithm/logic issues missed in Round 1
- Round 3 catches subtle issues that require "adversarial" thinking

**Real-world example:** A "simple" config parameter move:
- Round 1: Verified all requirements met
- Round 2: Found outdated docstring examples that would confuse developers
- Round 3: Found inconsistent test fixture that could cause false test passes

**Each round catches issues the previous rounds missed. Skipping any round allows bugs to ship.**

---

