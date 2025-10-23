# Excel Trade Visualizer Reorganization - Questions

**Date**: 2025-10-23
**Source**: `updates/excel_reorganization_ideas.txt`
**TODO File**: `updates/todo-files/excel_reorganization_ideas_todo.md`

---

## INSTRUCTIONS

Please answer the questions below to clarify implementation requirements. Your answers will be integrated into the TODO file before implementation begins.

For each question, please provide:
1. Your chosen option (if multiple choices given)
2. Any additional context or preferences
3. Priority level if requesting a subset of features

---

## Q1: IMPLEMENTATION SCOPE (CRITICAL)

The specification file includes 8 reorganization ideas at 3 priority levels:

**HIGH PRIORITY** (biggest clarity improvements):
- IDEA 1: Add "Trade Impact Analysis" sheet
- IDEA 4: Add "Score Change Breakdown" sheet
- IDEA 2: Reorganize Detailed Calculations with side-by-side columns

**MEDIUM PRIORITY** (nice visual enhancements):
- IDEA 8: Add visual delta indicators (▲▼=)
- IDEA 5: Reorganize sheet order
- IDEA 6: Add trade summary metrics to Summary sheet

**LOWER PRIORITY** (polish):
- IDEA 3: Add color coding (requires openpyxl styling)
- IDEA 7: Split Detailed Calculations into two sheets

**Question**: Which ideas should be implemented?

**Options**:
A. HIGH PRIORITY only (Ideas 1, 2, 4)
B. HIGH + MEDIUM (Ideas 1, 2, 4, 5, 6, 8)
C. ALL ideas (Ideas 1-8)
D. Custom subset (specify which ideas)

**Your Answer**:
```
A
```

**Recommendation** (based on codebase research):
- Option A is recommended for initial implementation (HIGH PRIORITY only)
- These 3 ideas provide the biggest value with moderate effort
- MEDIUM and LOWER priority can be added later as enhancements

---

## Q2: "KEY CHANGES" COLUMN DETAIL LEVEL

The proposed "Trade Impact Analysis" sheet includes a "Key Changes" column explaining why player scores changed.

**Question**: How much detail should this column show?

**Options**:
A. **Abbreviated**: Brief summary (e.g., "Bye penalty +2 overlaps")
B. **Detailed**: Full explanation (e.g., "Bye penalty +2 same-position overlaps (-10.5 pts)")
C. **Very Detailed**: Include all scoring components that changed

**Example Comparison**:
```
Abbreviated:    "Bye penalty added"
Detailed:       "Bye penalty: +2 same-pos overlaps (-10.5 pts)"
Very Detailed:  "Bye penalty: 0→2 same-pos (-10.5 pts), Matchup: EXCELLENT→GOOD (-5.0 pts)"
```

**Your Answer**:
```
B
```

**Recommendation** (based on user experience):
- Option B (Detailed) provides good balance of clarity and conciseness
- Shows the key information without overwhelming the user

---

## Q3: SCORE CHANGE BREAKDOWN COMPONENTS

The proposed "Score Change Breakdown" sheet shows which scoring components changed and by how much.

**Question**: Which components should be included in this sheet?

**Options**:
A. **Bye & Injury Only**: Only show bye week penalties and injury status changes (most common)
B. **Major Components**: Bye, injury, matchup, performance (components that commonly change)
C. **All Components**: Every scoring component, even if unchanged (complete audit)

**Component List**:
- Bye week penalties ⭐ (changes frequently due to trades)
- Injury status ⭐ (changes frequently)
- Matchup rating (could change if team matchups updated)
- Performance rating (could change with new stats)
- ADP rating (rarely changes mid-season)
- Player rating (rarely changes)
- Team quality (rarely changes)
- Schedule (rarely changes)
- Draft bonus (never changes)

**Your Answer**:
```
A
```

**Recommendation** (based on expected use case):
- Option A (Bye & Injury Only) is recommended
- These are the components most likely to change due to trades
- Keeps the sheet focused and easy to read

---

## Q4: EMPTY SCORE CHANGE HANDLING

**Question**: What should happen if NO players have score changes (e.g., simple 1-for-1 trade with no bye week impacts)?

**Options**:
A. **Create empty sheet**: Create "Score Change Breakdown" sheet with informational message "No score changes detected"
B. **Skip sheet entirely**: Don't create the sheet if no score changes
C. **Always show traded players**: Show traded players even if their scores didn't change on remaining roster

**Your Answer**:
```
A
```

**Recommendation** (based on user expectations):
- Option A (Create empty sheet with message) is recommended
- Consistent sheet structure makes Excel easier to navigate
- Clear message explains why sheet is empty

---

## Q5: VISUAL DELTA INDICATORS (if implementing IDEA 8)

**Question**: Should delta columns use Unicode arrow symbols?

**Options**:
A. **Use symbols**: ▲ for positive, ▼ for negative, = for zero
B. **Use +/- signs only**: Standard "+5.0" or "-3.2" format
C. **Use color coding**: Green for positive, red for negative (requires openpyxl styling)

**Example**:
```
Option A: ▲ +5.0
Option B: +5.0
Option C: +5.0 (with green background)
```

**Your Answer**:
```
[Your choice: A/B/C]
[Only answer if implementing IDEA 8 from Q1]
```

**Recommendation** (based on Excel compatibility):
- Option A (Unicode symbols) if implementing IDEA 8
- Visually clear without requiring additional styling code
- Compatible with all Excel versions

---

## Q6: COLOR CODING PALETTE (if implementing IDEA 3)

**Question**: Which color scheme should be used for color coding?

**Options**:
A. **Recommended colors**: Green (#90EE90) for received, Red (#FFB6C1) for traded away, Yellow (#FFFFE0) for changed, White for unchanged
B. **Excel defaults**: Let openpyxl use default PatternFill colors
C. **Custom palette**: Specify custom hex colors

**Your Answer**:
```
[Your choice: A/B/C]
[Only answer if implementing IDEA 3 from Q1]
[If C, provide hex codes for: received, traded away, score changed, unchanged]
```

**Recommendation** (based on accessibility):
- Option A (Recommended colors) if implementing IDEA 3
- Light pastel colors work well in Excel and are print-friendly
- Sufficient contrast for colorblind users

---

## Q7: SHEET ORDER PREFERENCE (if implementing IDEA 5)

The proposed sheet order is:
1. Summary
2. Trade Impact Analysis (NEW)
3. Score Change Breakdown (NEW)
4. Final Rosters
5. Initial Rosters
6. Detailed Calculations

**Question**: Do you want to use this order, or prefer a different arrangement?

**Options**:
A. **Use proposed order**: Summary → Impact → Breakdown → Final → Initial → Detailed
B. **Keep Initial Rosters earlier**: Summary → Impact → Initial → Final → Breakdown → Detailed
C. **Custom order**: Specify your preferred order

**Your Answer**:
```
[Your choice: A/B/C]
[Only answer if implementing IDEA 5 from Q1]
[If C, specify order: e.g., "Summary, Final, Initial, Impact, Breakdown, Detailed"]
```

**Recommendation** (based on user workflow):
- Option A (Proposed order) if implementing IDEA 5
- Follows logical progression: overview → what changed → why → final state → reference data

---

## Q8: LOGGING VERBOSITY

**Question**: What logging level should be used for new sheet creation?

**Options**:
A. **INFO level**: Log each sheet creation (e.g., "Created Trade Impact Analysis sheet with 15 rows")
B. **DEBUG level**: Only log detailed breakdown information
C. **MINIMAL**: Only log errors, no success messages

**Your Answer**:
```
A (using recommendation)
```

**Recommendation** (based on existing code patterns):
- Option A (INFO level) is recommended
- Consistent with existing sheet creation logging (lines 408, 475, 588, 699)
- Helps with debugging without cluttering logs

---

## Q9: PERFORMANCE CONCERNS

**Question**: Do you have any concerns about Excel file size or performance?

**Context**:
- Current file has 4 sheets
- Proposed changes add 0-4 new sheets depending on scope (Q1)
- Each sheet contains filtered data (not full rosters)
- Typical roster size: 10-15 players per team

**Your Answer**:
```
No (using recommendation)
```

**Recommendation**:
- No performance concerns expected
- Filtered data keeps sheets small
- pandas + openpyxl handle this data size efficiently

---

## Q10: BACKWARD COMPATIBILITY

**Question**: Should the code maintain backward compatibility with old Excel files (4 sheets only)?

**Options**:
A. **No compatibility needed**: New Excel files replace old format entirely
B. **Support reading old files**: Add logic to detect and handle old format if needed
C. **Not applicable**: Old Excel files are not read by the system, only created

**Your Answer**:
```
C (using recommendation - Not applicable)
```

**Note**: Based on code analysis, the system only CREATES Excel files, it doesn't READ them. This question is likely C (Not applicable).

---

## Q11: ADDITIONAL REQUIREMENTS

**Question**: Are there any additional requirements, features, or constraints not covered in the specification file?

**Your Answer**:
```
None
```

---

## SUMMARY OF ANSWERS

**Final Decisions**:

```
SCOPE: HIGH PRIORITY only (Ideas 1, 2, 4)
  - IDEA 1: Add "Trade Impact Analysis" sheet
  - IDEA 4: Add "Score Change Breakdown" sheet
  - IDEA 2: Reorganize Detailed Calculations with side-by-side columns

KEY CHANGES DETAIL: Detailed (show component names, counts, and point values)

BREAKDOWN COMPONENTS: Bye & Injury Only (most common changes from trades)

EMPTY SHEET HANDLING: Create empty sheet with informational message

LOGGING: INFO level (consistent with existing code)

PERFORMANCE CONCERNS: None

BACKWARD COMPATIBILITY: Not applicable (system only creates Excel files)

ADDITIONAL NOTES: None
```

---

## NEXT STEPS

After you provide answers:
1. Your answers will be integrated into the TODO file
2. Second verification round will be executed (3 more iterations)
3. Implementation will begin following the refined TODO
4. Progress will be tracked in `updates/excel_reorganization_ideas_code_changes.md`

Thank you!
