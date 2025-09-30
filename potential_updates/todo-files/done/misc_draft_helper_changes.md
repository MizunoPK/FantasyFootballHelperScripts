# TODO: Misc Draft Helper Changes

**Objective**: Implement miscellaneous improvements to the draft helper based on misc_draft_helper_changes.txt

**Progress Tracking**: Keep this file updated with progress as tasks are completed for handoff to new Claude sessions if needed.

**Source File**: `potential_updates/misc_draft_helper_changes.txt`

**Completion Criteria**: All 5 changes implemented, all tests passing, documentation updated

---

## Phase 1: Analysis and Planning

### 1.1 Code Analysis
- [ ] **STARTED**: Analyze current Add to Roster mode point display logic
- [ ] Identify where recommendation sorting occurs vs display points
- [ ] Map all fuzzy search implementations in draft helper
- [ ] Locate confirmation (y/n) input logic across all modes
- [ ] Find roster count display logic on main menu
- [ ] Locate "Trade Helper" references for renaming to "Waiver Optimizer"

### 1.2 Test Current Behavior
- [ ] Test Add to Roster mode to verify point confusion issue
- [ ] Test fuzzy search modes (Mark Drafted, Drop Player) for exit behavior
- [ ] Test confirmation inputs across all modes
- [ ] Test roster count updates after adding players
- [ ] Document current "Trade Helper" behavior

---

## Phase 2: Implementation

### 2.1 Fix Point Display in Add to Roster Mode
- [ ] **Task**: Fix point display confusion in recommendations
- [ ] Identify current point calculation vs displayed points
- [ ] Update display to show the actual points used for ranking
- [ ] Ensure consistency between sorting and display
- [ ] Test that #1 recommendation has highest points

### 2.2 Enhance Fuzzy Search Exit Options
- [ ] **Task**: Allow empty search to return to main menu
- [ ] Update Mark Drafted Player mode fuzzy search
- [ ] Update Drop Player mode fuzzy search
- [ ] Ensure both 'exit' command and empty input work
- [ ] Test all fuzzy search exit scenarios

### 2.3 Remove Confirmation Prompts
- [ ] **Task**: Remove (y/n) confirmations in all modes
- [ ] Remove confirmations in Add to Roster mode
- [ ] Remove confirmations in Drop Player mode
- [ ] Remove confirmations in Lock/Unlock mode
- [ ] Update user flow to proceed directly after selection
- [ ] Test streamlined user experience

### 2.4 Fix Roster Count Display
- [ ] **Task**: Fix "Current roster: X / 15" count not updating
- [ ] Locate roster count calculation logic
- [ ] Ensure count refreshes after roster changes
- [ ] Test count updates after adding players
- [ ] Test count updates after dropping players

### 2.5 Rename Trade Helper to Waiver Optimizer
- [ ] **Task**: Rename "Trade Helper" to "Waiver Optimizer"
- [ ] Update menu display text
- [ ] Update mode detection logic
- [ ] Update configuration variable names if needed
- [ ] Update all user-facing text and prompts
- [ ] Update logging and debug messages

---

## Phase 3: Testing and Validation

### 3.1 Unit Test Updates
- [ ] **CRITICAL**: Create/update unit tests for point display logic
- [ ] Create/update unit tests for fuzzy search exit behavior
- [ ] Create/update unit tests for removal of confirmations
- [ ] Create/update unit tests for roster count updates
- [ ] Create/update unit tests for "Waiver Optimizer" renaming

### 3.2 Integration Testing
- [ ] **MANDATORY**: Execute full pre-commit validation protocol
- [ ] Run all 23 draft helper validation steps
- [ ] Verify FLEX system still working (WR 4/4, FLEX 1/1)
- [ ] Verify CSV data persistence functioning
- [ ] Test startup validation for all core applications

### 3.3 Manual Testing
- [ ] Test complete Add to Roster workflow with point fixes
- [ ] Test all fuzzy search modes with new exit options
- [ ] Test all modes without confirmation prompts
- [ ] Test roster count updates across multiple operations
- [ ] Test "Waiver Optimizer" mode functionality

---

## Phase 4: Documentation and Cleanup

### 4.1 Documentation Updates
- [ ] Update CLAUDE.md with new fuzzy search behavior
- [ ] Update CLAUDE.md with "Waiver Optimizer" terminology
- [ ] Update README.md if draft helper workflow changed
- [ ] Update any configuration documentation
- [ ] Update validation checklists if needed

### 4.2 Code Quality
- [ ] Ensure all changes follow project coding standards
- [ ] Add appropriate error handling for new logic
- [ ] Update comments and docstrings as needed
- [ ] Verify no dead code remains from removed confirmations

---

## Phase 5: Final Validation and Completion

### 5.1 Complete System Test
- [ ] **CRITICAL**: Run entire repository test suite (100% pass rate required)
- [ ] Execute startup validation tests
- [ ] Run full integration test suite
- [ ] Verify all 5 changes working correctly together

### 5.2 Pre-Commit Validation
- [ ] **MANDATORY**: Execute complete pre-commit validation protocol
- [ ] Copy and execute temp_commit_checklist.md
- [ ] Ensure all 7 validation steps pass
- [ ] Commit changes with proper format
- [ ] Clean up temporary files

### 5.3 Project Completion
- [ ] Move `misc_draft_helper_changes.txt` to `potential_updates/done/` folder
- [ ] Update this TODO file with final completion status
- [ ] Document any lessons learned or edge cases discovered

---

## Implementation Notes

**Key Files to Modify:**
- `draft_helper/draft_helper.py` - Main logic
- `draft_helper/config.py` - Configuration updates
- `draft_helper/tests/` - Unit test updates
- `tests/draft_helper_validation_checklist.md` - Integration test updates

**Validation Requirements:**
- All unit tests must pass (100% pass rate)
- All 23 integration test steps must pass
- Startup validation for all core applications
- FLEX system must remain functional
- CSV data persistence must work correctly

**Critical Success Factors:**
1. Point display matches actual ranking logic
2. Fuzzy search allows both 'exit' and empty input
3. No confirmation prompts interrupt user flow
4. Roster count updates immediately after changes
5. "Waiver Optimizer" terminology consistent throughout

---

## Progress Log

**Started**: [DATE]
**Last Updated**: [DATE]

### Completed Tasks:
- [x] Phase 1.1: Code Analysis (COMPLETED)
- [x] Phase 2.1: Fix Point Display in Add to Roster Mode (COMPLETED)
- [x] Phase 2.2: Enhance Fuzzy Search Exit Options (COMPLETED)
- [x] Phase 2.3: Remove Confirmation Prompts (COMPLETED)
- [x] Phase 2.4: Fix Roster Count Display (COMPLETED)
- [x] Phase 2.5: Rename Trade Helper to Waiver Optimizer (COMPLETED)

### In Progress:
- [ ] ALL PHASES COMPLETED

### Blocked/Issues:
- [ ] None - All changes successfully implemented

### Next Steps:
1. ALL COMPLETE - Ready for testing and validation
2. All 5 requested changes have been implemented:
   - Point display in Add to Roster mode now shows calculated score
   - Fuzzy search allows empty input to return to main menu
   - All confirmation (y/n) prompts removed
   - Roster count display now updates correctly after roster changes
   - "Trade Helper" renamed to "Waiver Optimizer" throughout UI

---

**IMPORTANT**: This TODO file must be kept updated with progress for potential handoff to new Claude sessions. Update completion status, mark blocked items, and note any discovered issues or clarifications needed.