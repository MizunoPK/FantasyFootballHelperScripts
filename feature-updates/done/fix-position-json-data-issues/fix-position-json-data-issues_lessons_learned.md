# Fix Position JSON Data Issues - Lessons Learned

This file captures issues encountered during feature development that should be used to improve the development guides.

---

## Purpose

Document any:
- Process gaps discovered
- Guide improvements needed
- Common mistakes to add to guides
- Verification steps that should be mandatory
- Things that worked well and should be emphasized

---

## Lessons Learned

(To be populated during development and post-implementation)

### Planning Phase Lessons
(To be added)

### Development Phase Lessons

#### Lesson 1: Agent Made Incorrect Assumption About "Minimum Required" Verification (2024-12-24)

**What Happened:**
- Agent completed Round 1 (7 iterations) + Iteration 4a (TODO Specification Audit)
- Agent incorrectly stated this was "minimum required" and TODO was "ready for implementation"
- Agent offered user choice: "proceed to implementation OR continue Round 2"
- User correctly challenged this assumption

**Root Cause:**
- Agent did not re-read `todo_creation_guide.md` after completing Round 1
- Agent made assumption based on having passed "mandatory" Iteration 4a audit
- Guide clearly states on lines 86-92: "All 24 iterations complete" required for implementation
- Context compaction can cause agents to lose track of guide requirements

**Impact:**
- Could have led to premature implementation without proper verification
- 16 more iterations required (8-16 and 17-24) before implementation ready
- User had to correct agent - wasted user time

**What Should Have Happened:**
- Agent should have re-read guide section on "READY FOR IMPLEMENTATION" checklist
- Agent should have checked lines 86-92 before declaring readiness
- Agent should have continued directly to Round 2 without asking user

### QC Phase Lessons
(To be added)

---

## Guide Update Recommendations

(To be populated when issues are discovered)

### Recommended Updates to Planning Guide
- [ ] (None yet)

### Recommended Updates to TODO Creation Guide (`todo_creation_guide.md`)

- [ ] **Add reminder checkpoints after each round:** After completing Round 1, Round 2, etc., add explicit reminder to re-read the "READY FOR IMPLEMENTATION" checklist (lines 86-92) before declaring completion
  - Example: "🔄 CHECKPOINT: Re-read lines 86-92 before proceeding. Are ALL 24 iterations complete?"

- [ ] **Add reminder in Quick Start section:** Make it explicit that all 7 steps must be completed, not just steps 1-4
  - Current wording could be misinterpreted as Round 1 being sufficient

- [ ] **Add "What NOT to do" examples:** Include anti-pattern showing agent declaring ready after Round 1 only
  - Show correct behavior: complete all rounds before declaring ready

### Recommended Updates to ALL Guides (General Pattern)

- [ ] **Add "Re-read This Section" reminders at major checkpoints**
  - After completing each phase, remind agent to re-read the guide section for next phase
  - Example: "✅ Phase X complete. 🔄 NOW: Re-read Phase X+1 section below before proceeding"

- [ ] **Add reminders to feature-specific README.md files**
  - Include section: "📖 Current Phase Guide: feature-updates/guides/[guide_name].md"
  - Update this section as phases progress
  - Agent should check README for current guide before each major action

- [ ] **Add reminders to TODO files**
  - Include section at top: "📖 Active Guide: todo_creation_guide.md (re-read before declaring complete)"
  - Update when transitioning to implementation_execution_guide.md

- [ ] **Add "Context Compaction Resilience" sections to guides**
  - Recognize that agents lose context during compaction
  - Build in redundant reminders at critical decision points
  - Make completion criteria unmistakably clear (e.g., large warning boxes)

### Recommended Updates to Templates (`templates.md`)

- [ ] **Add guide reminder section to README template**
  ```markdown
  ## 📖 Active Development Guide

  **Current Phase:** [PLANNING | TODO_CREATION | IMPLEMENTATION | POST_IMPLEMENTATION]
  **Active Guide:** feature-updates/guides/[guide_file].md
  **Critical Section:** [specific section to reference]

  ⚠️ AGENTS: Re-read the active guide section before major decisions!
  ```

- [ ] **Add guide reminder section to TODO template**
  ```markdown
  ## 📖 Guide Reminder

  **This file is governed by:** `todo_creation_guide.md`
  **Ready for implementation when:** ALL 24 iterations complete (see guide lines 86-92)
  **DO NOT proceed to implementation until:** Iteration 24 passed

  ⚠️ If you think verification is complete, re-read guide lines 86-92 first!
  ```

### Recommended Updates to Post-Implementation Guide
- [ ] (None yet)

---

## Notes

This feature is itself a result of process lessons learned:
- **Context:** Original position JSON feature was accepted with "partial work" despite being non-functional
- **Issue:** QC validated structure but not data semantics
- **Result:** Recent guide updates to ban "acceptable partial" work
- **This feature:** First test of the new "no partial work" requirement
