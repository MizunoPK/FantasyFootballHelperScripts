## Feature Checklist: schedule_fetcher_cli

**Created:** 2026-02-18 (S2.P1.I1)
**Purpose:** Open questions requiring user input before spec can be finalized

*Note: Agents NEVER mark [x]. Only user answers trigger resolution.*

---

## Resolved Questions

### Q1: Does `--data-folder` exist as a separate arg, or is it redundant with `--output-path`?

**Status:** RESOLVED — Option A: `--output-path` only. `--data-folder` dropped.
**Source:** User answer 2026-02-18

---

### Q5: For `--debug` mode, what is the data scope reduction?

**Status:** RESOLVED — N/A. No `--debug` flag in this epic (design correction in HANDOFF_PACKAGE.md 2026-02-18).
`--e2e-test` handles both E2E testing and debug use cases. `--log-level DEBUG` provides verbose output.

---

## Open Questions (S2.P1.I2 — Checklist Resolution)

### Q2: Should `--output-format` support JSON, or is CSV the only format?

**Status:** RESOLVED — Option A: `--output-format` dropped. CSV only.
**Source:** User answer 2026-02-18

---

### Q3: Should `--request-timeout` be exposed as a CLI arg?

**Status:** RESOLVED — Option A: internal constant only. Not exposed as CLI arg.
**Source:** User answer 2026-02-18

---

### Q4: Should `--rate-limit-delay` be exposed as a CLI arg?

**Status:** RESOLVED — Option A: internal constant only. Not exposed as CLI arg.
**Source:** User answer 2026-02-18

---

## Summary

**Gate 3 approved by user: 2026-02-18**

| Q# | Topic | Status |
|----|-------|--------|
| [x] Q1 | --data-folder vs --output-path | RESOLVED — A: --output-path only |
| [x] Q2 | --output-format (CSV/JSON) | RESOLVED — A: dropped, CSV only |
| [x] Q3 | --request-timeout | RESOLVED — A: internal constant |
| [x] Q4 | --rate-limit-delay | RESOLVED — A: internal constant |
| [x] Q5 | Debug mode data scope | RESOLVED — N/A (no --debug flag) |
