# Verification Failure Protocol

**Purpose:** Handle issues discovered during any verification iteration.

**Related:** [README.md](README.md) - Protocol index

---

**When a verification iteration finds a gap or issue:**

1. **STOP** - Do not continue to the next iteration
2. **Document** the gap in the TODO file under a "Verification Gaps" section:
   ```
   ## Verification Gaps (Iteration X)
   - [GAP-1] Missing task for {description}
   - [GAP-2] Orphan method {name} has no caller
   ```
3. **Assess severity:**
   - **Critical** (blocks implementation): Missing caller, wrong interface, algorithm mismatch
   - **Non-critical** (can be fixed during implementation): Missing test, documentation gap
4. **For Critical gaps:**
   - Add task to TODO immediately
   - Mark iteration as "INCOMPLETE - gaps found"
   - Re-run iteration after fixing
5. **For Non-critical gaps:**
   - Add task to TODO
   - Note in Progress Notes: "Non-critical gap found, task added"
   - Continue to next iteration
6. **Update confidence level** based on gaps found

**Example:**
```
Iteration 7 (Integration Gap Check):
- Found: save_optimal_config() method has no caller
- Severity: CRITICAL
- Action: Added Task 4.2 to modify SimulationManager
- Status: Re-running iteration 7 after fix
```

---

## Mandatory Stop Points

These situations REQUIRE stopping and asking the user before proceeding. Do NOT proceed past these points without user input.

```
┌─────────────────────────────────────────────────────────────────┐
│  STOP AND ASK - These situations require user input             │
└─────────────────────────────────────────────────────────────────┘
```

| Situation | Why Stop | What to Ask |
|-----------|----------|-------------|
| **Confidence is LOW** at any iteration | Low confidence = high bug risk | "I have low confidence because {X}. Should I investigate more or proceed?" |
| **Found unresolved alternative** in spec | Ambiguity causes wrong implementation | "The spec mentions both A and B. Which should I use?" |
| **Test failure** you can't quickly fix | May indicate design problem | "Tests are failing because {X}. Options: (1) fix Y, (2) change approach. Which do you prefer?" |
| **Scope seems to be expanding** | Scope creep is expensive | "This change would also require {X}. Is that in scope?" |
| **Interface doesn't match expectation** | May need spec update | "Expected method {X}, but found {Y}. Should I update the plan?" |
| **E2E script produces unexpected output** | May indicate misunderstanding | "Script runs but output is {X} instead of {Y}. Is this expected?" |
| **Missing data source** for a requirement | Can't implement without data | "Requirement {X} needs data from {Y}, but I can't find it. Where should I look?" |
| **Conflicting requirements** discovered | Both can't be satisfied | "Requirements A and B conflict because {X}. Which takes priority?" |
| **New edge case** discovered during implementation | May need spec clarification | "Found edge case: {X}. How should this be handled?" |
| **Architecture decision** with multiple valid approaches | User preference matters | "I can implement this with {A} or {B}. Here are trade-offs: ... Which do you prefer?" |

**How to Stop:**
1. Document the situation clearly in TODO or questions file
2. Present the issue to the user with context
3. Offer options when possible (don't just say "I'm stuck")
4. Wait for user response before proceeding

**Anti-pattern:** "I'll make a decision and tell them later"
- This causes rework when your guess was wrong
- Always ask BEFORE implementing when uncertain

