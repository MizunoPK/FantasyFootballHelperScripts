# Metric 47: TD Equity (RB)

**Position Applicability:** RB
**Priority:** MEDIUM
**Research Date:** 2025-12-20

---

## 1. Existing Data Analysis

**Can this metric be calculated from existing data?**

- [ ] Yes
- [x] No - Requires advanced TD probability modeling

**Details:**

TD Equity = Expected TDs based on usage, field position, team scoring

**Note:** Very similar to Metric 22 (Expected Fantasy Points) and Metric 46 (Goal-Line Role)

---

## 2. ESPN API Availability

**Is this metric available?**

- [x] No

---

## 3. Free Alternative Sources

### Derivable from existing metrics:
- Metric 46: Goal-Line Role (RB TD predictor)
- Metric 22: Expected Fantasy Points (includes TD expectation)
- Metric 7: Red Zone Opportunity (RZ touches predict TDs)

---

## 4-5. Data Quality & Historical Availability

**Reliability:** Medium (modeling required)
**Historical:** ⚠️ Partial (via other metrics)
**Predictive:** ✅ Yes

---

## 6. Implementation Complexity

**Difficulty:** Medium-Hard
**Effort:** 2-3 days (modeling)

---

## 7. Recommendation

**Should we pursue this metric?**

- [ ] **DEFER** - Overlap with Metrics 22, 46, 7

**Value:** ⭐⭐ (Low - redundant with existing metrics)
**Feasibility:** ⭐⭐ (Medium-Hard)
**Historical:** ⭐⭐ (Limited - modeling required)

**Rationale:** TD equity already captured by:
- Metric 46 (Goal-Line Role): Direct TD predictor
- Metric 22 (xFP): Includes expected TDs
- Metric 7 (Red Zone Opportunity): RZ touches

**Alternative:** Use combination of existing metrics instead of separate TD equity model

---

*Research conducted: 2025-12-20*
