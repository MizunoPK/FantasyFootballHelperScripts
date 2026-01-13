# Workflow Visual Diagrams

**Purpose:** Visual representations of workflow stages

---

## Complete 7-Stage Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    EPIC-DRIVEN DEVELOPMENT                      │
│                         7 Stages                                 │
└─────────────────────────────────────────────────────────────────┘

                         User creates
                      {epic_name}.txt
                            │
                            ▼
         ┌──────────────────────────────────────┐
         │  STAGE 1: Epic Planning              │
         │  - Assign KAI number                 │
         │  - Create git branch                 │
         │  - Propose features (user approves)  │
         │  - Create epic folder structure      │
         └──────────────────┬───────────────────┘
                            │
                            ▼
         ┌──────────────────────────────────────┐
         │  STAGE 2: Feature Deep Dives         │
         │  (Loop through ALL features)         │
         │  - S2.P1: Research               │
         │  - Step 2: Specification            │
         │  - S2.P3: Refinement             │
         │  - Gate 3: User checklist approval   │
         └──────────────────┬───────────────────┘
                            │
                            ▼
         ┌──────────────────────────────────────┐
         │  STAGE 3: Cross-Feature Sanity Check │
         │  - Systematic pairwise comparison    │
         │  - Resolve conflicts                 │
         │  - User sign-off on plan             │
         └──────────────────┬───────────────────┘
                            │
                            ▼
         ┌──────────────────────────────────────┐
         │  STAGE 4: Epic Testing Strategy      │
         │  - Update epic_smoke_test_plan.md    │
         │  - Identify integration points       │
         │  - Gate 4.5: User approval           │
         └──────────────────┬───────────────────┘
                            │
                            ▼
         ┌──────────────────────────────────────┐
         │  STAGE 5: Feature Implementation     │
         │  (Loop per feature: 5a→5b→5c→5d→5e)  │
         │  5a: Planning (28 iterations)        │
         │      Gate 4a, 23a, Gate 5 (user)     │
         │  5b: Execution (implement code)      │
         │  5c: Post-Implementation Testing     │
         │      - Smoke Testing (3 parts)       │
         │      - QC Rounds (3 rounds)          │
         │      - Final Review                  │
         │  5d: Cross-Feature Alignment         │
         │  5e: Epic Testing Plan Update        │
         └──────────────────┬───────────────────┘
                            │
                            ▼
         ┌──────────────────────────────────────┐
         │  STAGE 6: Epic-Level Final QC        │
         │  - Epic smoke testing (4 parts)      │
         │  - Epic QC rounds (3 rounds)         │
         │  - Epic final review                 │
         │  - User testing (MANDATORY)          │
         │    If bugs → loop back to 6a         │
         └──────────────────┬───────────────────┘
                            │
                            ▼
         ┌──────────────────────────────────────┐
         │  STAGE 7: Epic Cleanup               │
         │  - Run unit tests (100% pass)        │
         │  - S10.P1: Guide updates          │
         │  - Commit changes                    │
         │  - Create Pull Request               │
         │  - User reviews and merges           │
         │  - Move epic to done/                │
         └──────────────────┬───────────────────┘
                            │
                            ▼
                    Epic Complete!
                 (moved to done/ folder)
```

---

## S5: Feature Implementation Detail

```
┌────────────────────────────────────────────────────────────────┐
│              STAGE 5: FEATURE IMPLEMENTATION                   │
│           (Repeat for EACH feature: 5a→5b→5c→5d→5e)            │
└────────────────────────────────────────────────────────────────┘

    Feature_01                Feature_02              Feature_03
       │                          │                       │
       ▼                          │                       │
  ┌─────────┐                    │                       │
  │ S5│ Implementation Planning (28 iterations)    │
  │         │ - Round 1 (9 iterations)                   │
  │         │   Gate 4a: TODO Spec Audit                 │
  │         │ - Round 2 (9 iterations)                   │
  │         │ - Round 3 (10 iterations)                  │
  │         │   Gate 23a: Pre-Impl Spec Audit            │
  │         │   Gate 24: GO/NO-GO Decision               │
  │         │ - Gate 5: User Approval (MANDATORY)        │
  └────┬────┘                    │                       │
       │                          │                       │
       ▼                          │                       │
  ┌─────────┐                    │                       │
  │ S6│ Implementation Execution                   │
  │         │ - Follow implementation_plan.md            │
  │         │ - Track via implementation_checklist.md    │
  │         │ - Mini-QC after each component             │
  └────┬────┘                    │                       │
       │                          │                       │
       ▼                          │                       │
  ┌─────────┐                    │                       │
  │ S7│ Post-Implementation Testing                │
  │         │ Step 1: Smoke Testing (3 parts)           │
  │         │ Step 2: QC Rounds (3 rounds)              │
  │         │   If issues → debugging → loop back S10.P1    │
  │         │ Step 3: Final Review                      │
  │         │ Step 4: Commit feature code               │
  └────┬────┘                    │                       │
       │                          │                       │
       ▼                          │                       │
  ┌─────────┐                    │                       │
  │ S8.P1│ Cross-Feature Alignment                    │
  │         │ - Update remaining feature specs           │
  └────┬────┘                    │                       │
       │                          │                       │
       ▼                          │                       │
  ┌─────────┐                    │                       │
  │ S8.P2│ Epic Testing Plan Update                   │
  │         │ - Update epic_smoke_test_plan.md           │
  └────┬────┘                    │                       │
       │                          │                       │
   Feature 1 Done                 │                       │
       │                          ▼                       │
       │                     Repeat 5a→5e                │
       │                     for Feature 2               │
       │                          │                       │
       │                      Feature 2 Done             │
       │                          │                       │
       │                          │                       ▼
       │                          │                  Repeat 5a→5e
       │                          │                  for Feature 3
       │                          │                       │
       └──────────────────────────┴───────────────────────┘
                                  │
                            All Features Done
                                  │
                                  ▼
                             STAGE 6: Epic QC
```

---

## Debugging Protocol Integration

```
┌────────────────────────────────────────────────────────────────┐
│            DEBUGGING PROTOCOL (INTEGRATED WITH TESTING)        │
└────────────────────────────────────────────────────────────────┘

     Smoke Testing or QC Rounds
              │
              ▼
        Issues Found?
              │
         ┌────┴────┐
         │         │
        YES       NO
         │         └─────────> Continue Testing
         │
         ▼
  ┌──────────────┐
  │ PHASE 1      │  Issue Discovery
  │ Discovery    │  - Create debugging/ISSUES_CHECKLIST.md
  └──────┬───────┘  - Add all discovered issues
         │
         ▼
  ┌──────────────┐  (Work through checklist)
  │ PHASE 2      │  Investigation (Per Issue)
  │ Investigation│  - Round 1: Code Tracing
  └──────┬───────┘  - Round 2: Hypothesis Formation
         │          - Round 3: Diagnostic Testing
         │          (Max 5 rounds per issue)
         ▼
  ┌──────────────┐
  │ PHASE 3      │  Solution Design & Implementation
  │ Resolution   │  - Design fix
  └──────┬───────┘  - Implement with tests
         │          - Document in debugging/code_changes.md
         ▼
  ┌──────────────┐
  │ PHASE 4      │  User Verification (MANDATORY)
  │ Verification │  - Present before/after to user
  └──────┬───────┘  - Wait for user confirmation
         │
         ▼
  ┌──────────────┐
  │ PHASE 4b     │  Root Cause Analysis (MANDATORY)
  │ Root Cause   │  - 5-why analysis (immediately!)
  └──────┬───────┘  - Draft guide improvements
         │          - User confirms root cause
         │          (10-20 min per issue)
         │
         │  More issues in checklist?
         │
    ┌────┴────┐
    │         │
   YES       NO
    │         │
    └─────┐   │
          │   ▼
          │ ┌──────────────┐
          │ │ PHASE 5      │  Loop Back to Testing
          │ │ Loop Back    │  - Cross-bug pattern analysis
          │ └──────┬───────┘  - Final review
          │        │          - Loop back to START of testing
          │        ▼
          │   Re-run Testing (from Part 1)
          │        │
          └────────┘  (If new issues, repeat)
                   │
                   ▼ (Zero issues)
              Proceed to Next Stage
```

---

**END OF WORKFLOW DIAGRAMS**
