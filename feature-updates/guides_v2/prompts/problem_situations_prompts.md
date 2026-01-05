# Problem Situations Prompts

**Purpose:** Prompts for handling common problem situations during epic development

---

## When Tests Are Failing

**Situation:** Unit tests failing during Stage 5b or 5c

**Agent MUST respond:**

```
Unit tests are failing. Following the guide requirements, I need to fix these before proceeding...

**Test Failures:**
- Total tests: {N}
- Passing: {X}
- Failing: {Y}
- Failure rate: {percentage}%

**Failed Tests:**
1. {test_name}: {failure reason}
2. {test_name}: {failure reason}
{List all failures}

**Root Cause Analysis:**
{Analysis of why tests are failing}

**Fix Plan:**
1. {Fix step 1}
2. {Fix step 2}
3. {Fix step 3}

**I'll fix these issues and re-run the test suite. Will not proceed until exit code = 0 (100% pass rate).**

Fixing test failures...
```

---

## When Stuck or Blocked

**Situation:** Agent encounters blocker that prevents progress

**Agent MUST respond:**

```
I've encountered a blocker that prevents me from continuing. Following guide requirements (STOP when blocked), I need your help...

**Blocker Description:**
{Clear description of what's blocking progress}

**What I was trying to do:**
{Context - what task/step was being attempted}

**Why I'm blocked:**
{Explanation of the blocker}

**What I need to proceed:**
{Specific ask - e.g., "Clarification on...", "Decision on...", "Access to..."}

**Options:**
1. {Option 1 and implications}
2. {Option 2 and implications}
3. {Option 3 and implications}

Which option should I take, or do you have another approach?

Waiting for your guidance...
```

---

## When Confidence < Medium

**Situation:** Agent's confidence drops below Medium during Stage 5a (TODO Creation)

**Agent MUST respond:**

```
My confidence level has dropped below Medium. Following STAGE_5a requirements, I'm STOPPING to create a question...

**Low Confidence Area:**
{What area has low confidence - e.g., "Interface verification for Feature 02 integration"}

**Current Iteration:** {N}/24
**Current Task:** {Task description}

**Why Confidence is Low:**
{Explanation - e.g., "Interface documentation unclear", "Dependency code not found", "Multiple valid approaches"}

**Question for User:**
{Clear, specific question}

**Options (if applicable):**
1. {Option 1 and implications}
2. {Option 2 and implications}

**I'm creating/updating questions.md to track this question. Will wait for your answer before proceeding with iteration {N}.**

Creating question in questions.md...
```

---

## Presenting Options to User

**Situation:** Agent needs user decision (e.g., feature breakdown in Stage 1)

**Agent MUST respond:**

```
I need your decision on {topic}. Here are the options I've identified...

**Context:**
{Brief context for why decision is needed}

**Option 1: {Option Name}**
**Description:** {What this option means}
**Pros:**
- {Pro 1}
- {Pro 2}
**Cons:**
- {Con 1}
- {Con 2}
**Implications:** {What happens if this option is chosen}

**Option 2: {Option Name}**
**Description:** {What this option means}
**Pros:**
- {Pro 1}
- {Pro 2}
**Cons:**
- {Con 1}
- {Con 2}
**Implications:** {What happens if this option is chosen}

{Continue for all options}

**My Recommendation:** Option {N} - {Option Name}
**Reason:** {Why this is recommended}

Which option would you like to proceed with?

Waiting for your decision...
```

---

## Asking for Clarification

**Situation:** Agent needs user to clarify requirements

**Agent MUST respond:**

```
I need clarification on {topic} before I can proceed correctly...

**What I'm trying to do:**
{Context - current task/step}

**What's unclear:**
{Specific area that needs clarification}

**Why this matters:**
{Impact of getting this wrong}

**My current understanding:**
{What agent thinks is meant}

**Please clarify:**
{Specific question}

**Examples (if helpful):**
- Scenario A: {example scenario 1}
- Scenario B: {example scenario 2}

Which scenario aligns with your intent, or is there a different approach?

Waiting for your clarification...
```

---

*For prompts for other stages, see the [prompts index](../prompts_reference_v2.md)*
