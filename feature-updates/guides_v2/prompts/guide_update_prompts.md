# Guide Update Prompts: Lessons Learned to Guide Improvements

**Stage:** 7.5 (Between user testing and final commit)
**Purpose:** Apply lessons learned from epic to improve guides for future agents

---

## Starting S10.P1: Guide Update from Lessons Learned (MANDATORY)

**User says:** Agent detects S10 user testing passed (Gate 7.2), OR user says "apply lessons to guides"

**Prerequisite:** S10 user testing passed (zero bugs), all lessons_learned.md files complete

**Agent MUST respond:**

```
I'm reading `stages/s10/s7_p1_guide_update_workflow.md` to apply lessons learned to guides...

**The guide requires:**
- **Analyze ALL lessons_learned.md files** from this epic:
  - epic_lessons_learned.md (epic-level lessons)
  - feature_XX_{name}/lessons_learned.md (all feature-level lessons)
- **Identify guide gaps:** For each lesson, determine which guide(s) could have prevented the issue
- **Create prioritized proposals** in GUIDE_UPDATE_PROPOSAL.md:
  - P0 (Critical): Prevents catastrophic bugs, mandatory gate gaps
  - P1 (High): Significantly improves quality, reduces major rework
  - P2 (Medium): Moderate improvements, clarifies ambiguity
  - P3 (Low): Minor improvements, cosmetic fixes
- **Get user approval INDIVIDUALLY:** Each proposal gets Approve/Modify/Reject/Discuss
- **Apply only approved changes** to guides
- **Create separate commit** for guide updates (before epic commit)

**Scope of guide updates:**
- All files in feature-updates/guides_v2/
- CLAUDE.md (root project instructions)
- Any files supporting future agents

**User approval process:**
- Each proposal presented individually with before/after
- User can: Approve (apply as-is) / Modify (provide alternative) / Reject (skip) / Discuss (ask questions)
- Agent applies only approved changes or user modifications

**Why this matters:**
- Continuous guide improvement based on real implementation experience
- Future agents benefit from lessons learned in this epic
- Systematic feedback loop: implementation → lessons → guide updates
- User has full control over guide evolution

**Prerequisites I'm verifying:**
✅ S10 user testing passed (Gate 7.2)
✅ All lessons_learned.md files complete
✅ Ready to analyze lessons and create proposal

**I'll now analyze the lessons learned from this epic and create GUIDE_UPDATE_PROPOSAL.md...**

**Updating EPIC_README.md Agent Status:**
- Current Stage: S10.P1 - Guide Update from Lessons Learned
- Current Phase: GUIDE_ANALYSIS
- Current Guide: stages/s10/s7_p1_guide_update_workflow.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "Analyze ALL lessons", "Prioritize P0-P3", "Individual approval", "Apply only approved", "Separate commit"
- Next Action: Read all lessons_learned.md files and identify guide gaps

Analyzing lessons learned...
```

---

## Presenting Proposals to User

**Trigger:** Agent completes GUIDE_UPDATE_PROPOSAL.md with all prioritized proposals

**Agent MUST present:**

```
🚨 **S10.P1: Guide Update Proposals Ready for Review**

I've analyzed all lessons learned from this epic and created prioritized guide update proposals.

**Summary:**
- Total lessons analyzed: {N} ({epic-level} epic, {feature-level} feature)
- Total proposals: {N}
  - P0 (Critical): {N} proposals - prevents catastrophic bugs
  - P1 (High): {N} proposals - significantly improves quality
  - P2 (Medium): {N} proposals - moderate improvements
  - P3 (Low): {N} proposals - minor improvements

**Proposal file:** `GUIDE_UPDATE_PROPOSAL.md`

**How to review:**
1. I'll present each proposal starting with P0 (critical)
2. For each proposal, you'll see:
   - The lesson learned (what went wrong/right)
   - Which guide(s) would be updated
   - Before/after comparison (exact text changes)
   - Rationale (how this prevents future issues)
3. Please respond for each proposal:
   - ✅ **Approve** - Apply as proposed
   - ✏️ **Modify** - Provide alternative text
   - ❌ **Reject** - Skip this change
   - 💬 **Discuss** - Ask questions or request clarification

**I'll start with P0 (Critical) proposals - these prevent major bugs:**

---

**Proposal P0-1:** {Title}

**Lesson Learned:**
> "{Quote from lessons_learned.md}"

**Problem:** {What went wrong and why}

**Affected Guide:** `{path/to/guide.md}` - Section: "{section}"

**Current text (BEFORE):**
```
{Current guide text}
```

**Proposed change (AFTER):**
```
{Proposed new text - highlighting additions/changes}
```

**Why this helps:** {How this prevents future agents from same issue}

**Your decision for Proposal P0-1:** Approve / Modify / Reject / Discuss?
```

---

## After User Approval

**Trigger:** User has reviewed all proposals and provided decisions

**Agent MUST respond:**

```
✅ **Guide Update Approvals Received**

**Summary of decisions:**
- Total proposals: {N}
- Approved: {N} proposals
- Modified: {N} proposals (user provided alternatives)
- Rejected: {N} proposals
- Pending discussion: {N} proposals

**Applying approved changes:**

{For each approved/modified proposal:}
✅ Proposal P{X}-{N}: {Title}
   - Updating: {guide_path}
   - Change: {brief description}

**Next steps:**
1. Apply all approved changes to guides
2. Apply user modifications where provided
3. Create separate commit for guide updates
4. Update reference/guide_update_tracking.md
5. Update guide-updates.txt if any items addressed
6. Proceed to S10 Step 7 (Final Commit & PR)

Applying guide updates...
```

---

## After Applying Changes

**Trigger:** Agent completes applying all approved guide updates

**Agent MUST respond:**

```
✅ **Guide Updates Applied Successfully**

**Changes committed:**
- Commit: {commit_hash}
- Message: "docs(guides): Apply lessons from KAI-{N}-{epic_name}"
- Files modified: {N} guide files
- Proposals applied: {N} approved + {N} modified

**Breakdown by priority:**
- P0 (Critical): {N} applied
- P1 (High): {N} applied
- P2 (Medium): {N} applied
- P3 (Low): {N} applied

**Updated tracking:**
- ✅ reference/guide_update_tracking.md updated
- ✅ Applied lessons logged with commit hash
- ✅ Rejected lessons documented with rationale

**Benefits for future agents:**
{List 2-3 key improvements that future agents will see}

**Next: S10 Step 7 - Final Commit & Pull Request**

I'll now proceed with creating the epic commit and pull request for your review.

Following `stages/s10/s7_epic_cleanup.md` Step 7...
```

---

## Handling "Modify" Responses

**Trigger:** User requests modification instead of approving as-is

**Agent MUST respond:**

```
📝 **Modification Request Received for Proposal P{X}-{N}**

**Your modification:**
> {User's alternative text}

**I'll apply your version instead of my proposal.**

**Updating guide with your modification:**
- Guide: {path/to/guide.md}
- Section: {section}
- Using your text: "{user's text preview...}"

Applied modification ✅

{Continue with next proposal if more exist}
```

---

## Handling "Discuss" Responses

**Trigger:** User requests discussion/clarification on proposal

**Agent MUST respond:**

```
💬 **Discussion Request for Proposal P{X}-{N}**

**Your question/concern:**
> {User's question or concern}

**My response:**
{Agent provides clarification, examples, or additional context}

**Would you like to:**
1. Approve the original proposal
2. Propose a modification
3. Reject this proposal
4. Continue discussion

Please let me know your decision.
```

---

## Handling "Reject" Responses

**Trigger:** User rejects proposal

**Agent MUST respond:**

```
❌ **Proposal P{X}-{N} Rejected**

**Understood.** I'll skip this guide update.

**Documenting rejection:**
- Adding to reference/guide_update_tracking.md "Rejected Lessons" section
- Rationale: {User's reason if provided, or "User declined"}

This helps avoid re-proposing the same change in future epics.

{Continue with next proposal if more exist}
```

---

## If No Proposals Generated

**Trigger:** Agent analyzes lessons but finds no actionable guide improvements

**Agent MUST respond:**

```
✅ **Lessons Learned Analyzed - No Guide Updates Needed**

I've analyzed all lessons learned from this epic:
- Epic lessons: {N}
- Feature lessons: {N}
- Total: {N} lessons

**Analysis result:**
All lessons were either:
- Specific to this epic's domain (not generalizable to guides)
- Already covered by existing guide content
- User-specific decisions (not guide issues)

**No guide update proposals to present.**

**Next: S10 Step 7 - Final Commit & Pull Request**

I'll proceed directly to creating the epic commit and pull request.

Following `stages/s10/s7_epic_cleanup.md` Step 7...
```

---

*For prompts for other stages, see the [prompts index](../prompts_reference_v2.md)*
