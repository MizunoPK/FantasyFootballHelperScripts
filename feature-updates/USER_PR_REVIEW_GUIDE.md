# User PR Review Guide

**Purpose:** Help you review Pull Requests created by agents at the end of epics

**When to use:** When agent completes Stage 7 and creates a PR for you to review

---

## Quick Start (First-Time Users)

**Simplest approach - No setup required:**

1. Agent creates PR and provides URL
2. Open URL in your browser
3. Click "Files changed" tab
4. Review all code changes
5. Click "Review changes" → "Approve"
6. Click "Merge pull request"
7. Done!

**Time:** 5-15 minutes depending on epic size

---

## Review Methods (Choose One)

### Method 1: GitHub Web UI (Recommended for First-Time)

**Pros:** Zero setup, best diff viewer, familiar interface
**Cons:** Requires browser, not integrated with editor

**Steps:**
1. Open PR URL provided by agent
2. Review the PR description (epic summary, features, tests)
3. Click "Files changed" tab at top
4. Review each file's changes:
   - Green lines = additions
   - Red lines = deletions
   - Click line numbers to add inline comments
5. When satisfied, click "Review changes" button (top right)
6. Select "Approve"
7. Add optional comment
8. Click "Submit review"
9. Click "Merge pull request"
10. Confirm merge

**See screenshots:** https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests

---

### Method 2: VS Code Extension (Best for Regular Use)

**Pros:** Review in editor, familiar environment, powerful
**Cons:** Requires extension installation

#### **One-Time Setup:**

1. Open VS Code
2. Click Extensions icon (left sidebar) or press `Ctrl+Shift+X`
3. Search for "GitHub Pull Requests and Issues"
4. Click "Install" on the official GitHub extension
5. Click "Sign in to GitHub" when prompted
6. Authorize VS Code to access your GitHub account

**Optional but recommended:**
- Install "GitLens" extension for enhanced Git features
- Install "SonarLint" extension for code quality checks

#### **Reviewing PRs in VS Code:**

1. Agent creates PR and provides PR number (e.g., #42)
2. In VS Code:
   - Click GitHub icon in left sidebar (looks like GitHub logo)
   - Find your PR in "Pull Requests" section
   - Click the PR to open it
3. Review changes:
   - View diff for each file in editor
   - Add comments by hovering over lines
   - See full conversation thread
4. Approve PR:
   - Click "Review Changes" in PR panel
   - Select "Approve"
   - Add optional comment
   - Click "Submit"
5. Merge PR:
   - Click "Merge Pull Request" button
   - Confirm merge

**VS Code Extension Docs:** https://code.visualstudio.com/docs/sourcecontrol/github

---

### Method 3: GitHub CLI (For Terminal Users)

**Pros:** Fast, scriptable, no browser needed
**Cons:** Requires CLI installation, less visual

#### **One-Time Setup:**

**Install GitHub CLI:**
- Windows: `winget install --id GitHub.cli`
- Mac: `brew install gh`
- Linux: See https://github.com/cli/cli/blob/trunk/docs/install_linux.md

**Authenticate:**
```bash
gh auth login
```

Follow prompts to authenticate with GitHub.

#### **Reviewing PRs with CLI:**

1. Agent creates PR (provides PR number, e.g., #42)

2. **List PRs:**
   ```bash
   gh pr list
   ```

3. **View PR details:**
   ```bash
   gh pr view 42
   ```

4. **View PR diff:**
   ```bash
   gh pr diff 42
   ```
   Use arrow keys to scroll, `q` to quit

5. **Check PR status (tests, etc.):**
   ```bash
   gh pr checks 42
   ```

6. **Review in browser (if you want visual):**
   ```bash
   gh pr view 42 --web
   ```

7. **Approve PR:**
   ```bash
   gh pr review 42 --approve
   ```
   Or with comment:
   ```bash
   gh pr review 42 --approve --body "Looks good, merging!"
   ```

8. **Merge PR:**
   ```bash
   gh pr merge 42
   ```
   Follow prompts to select merge type (usually "Create a merge commit")

**GitHub CLI Manual:** https://cli.github.com/manual/

---

### Method 4: Standalone Diff Tools (For Deep Inspection)

**Pros:** Powerful comparison, folder-level diffs
**Cons:** Requires tool installation, manual checkout

#### **Recommended Tools:**

**Free:**
- **Meld** - Visual diff tool (Windows/Mac/Linux)
  - Download: https://meldmerge.org/
- **WinMerge** - Windows-only diff tool
  - Download: https://winmerge.org/
- **Code Compare** - Windows diff tool with VS integration
  - Download: https://www.devart.com/codecompare/

**Commercial:**
- **Beyond Compare** ($60) - Industry standard
  - Download: https://www.scootersoftware.com/
- **Araxis Merge** ($129-$269) - Professional code review
  - Download: https://www.araxis.com/merge/

#### **Using Diff Tools:**

1. **Checkout PR branch locally:**
   ```bash
   git fetch origin
   git checkout epic/KAI-{number}
   ```

2. **Open diff tool and compare:**
   - **Meld:** Open Meld, select "Directory Comparison", choose branch vs main
   - **Beyond Compare:** File → Compare → Select folders
   - **WinMerge:** File → Open → Select folders

3. **Review changes visually:**
   - Navigate through changed files
   - Review line-by-line diffs
   - Take notes on any concerns

4. **Approve in GitHub:**
   - Use Method 1 (Web UI) or Method 3 (CLI) to approve
   - Merge when satisfied

---

## What to Look For During Review

### **Epic-Level Review Checklist:**

**Documentation:**
- [ ] `EPIC_README.md` accurately summarizes epic
- [ ] `epic_lessons_learned.md` contains insights
- [ ] `epic_smoke_test_plan.md` reflects actual implementation
- [ ] All feature `README.md` files are complete

**Code Quality:**
- [ ] No commented-out code
- [ ] No debugging print statements
- [ ] No TODOs or FIXMEs
- [ ] Code follows project conventions (see CLAUDE.md)

**Testing:**
- [ ] PR description shows 100% test pass rate
- [ ] Epic smoke testing passed (4/4 parts)
- [ ] Epic QC rounds passed (3/3)
- [ ] User testing passed (no bugs reported)

**Requirements:**
- [ ] All features from original `{epic_name}.txt` implemented
- [ ] No unexpected changes outside epic scope
- [ ] All acceptance criteria met

**Git:**
- [ ] Commit message is clear and descriptive
- [ ] File changes are reasonable (not too many deletions)
- [ ] No unintended file modifications

### **Red Flags (Request Changes):**

- ❌ Test failures mentioned in PR
- ❌ User testing skipped or incomplete
- ❌ Missing documentation
- ❌ Commented-out code or TODOs
- ❌ Files changed that are unrelated to epic
- ❌ Commit message is unclear or generic

---

## Common Scenarios

### **Scenario 1: Everything looks good**

1. Review PR (any method above)
2. Click "Approve"
3. Click "Merge pull request"
4. Tell agent: "I merged the PR"
5. Agent will update EPIC_TRACKER.md and move epic to done/

---

### **Scenario 2: I found issues**

1. Leave comments on specific lines (Web UI or VS Code)
2. Click "Request changes" instead of "Approve"
3. Tell agent about the issues
4. Agent will fix issues and push to same branch
5. PR automatically updates with new commits
6. Review again (repeat until satisfied)
7. Approve and merge

---

### **Scenario 3: I want to test code myself**

1. **Checkout PR branch:**
   ```bash
   git fetch origin
   git checkout epic/KAI-{number}
   ```

2. **Run tests:**
   ```bash
   python tests/run_all_tests.py
   ```

3. **Run the code:**
   - Test the features described in PR
   - Verify outputs match expectations

4. **Return to main:**
   ```bash
   git checkout main
   ```

5. **Approve and merge PR** (any method above)

---

### **Scenario 4: I'm not sure about something**

1. Leave a comment on the PR asking agent to clarify
2. Agent will respond with explanation
3. If you need changes, request them
4. If explanation is satisfactory, approve and merge

---

## Advanced: AI-Powered PR Review (Optional)

If you want automated code review before your manual review:

### **PR-Agent (Free, Open Source)**

**Install:**
```bash
pip install pr-agent
```

**Review PR:**
```bash
pr-agent --pr_url https://github.com/{owner}/{repo}/pull/{number} review
```

**What it does:**
- Analyzes code changes using AI (GPT-4)
- Suggests improvements
- Identifies potential bugs
- Estimates impact

**Time:** ~30 seconds per PR

**When to use:** Large epics with many file changes

**Docs:** https://github.com/qodo-ai/pr-agent

---

## Troubleshooting

### **"I don't see the GitHub icon in VS Code sidebar"**

1. Check if extension is installed:
   - Click Extensions icon
   - Search for "GitHub Pull Requests"
   - If not installed, install it
2. Check if signed in:
   - Bottom left corner should show GitHub account
   - If not, click "Sign in to GitHub"

### **"gh command not found"**

GitHub CLI is not installed. See Method 3 setup instructions above.

### **"I merged the PR but agent can't see it"**

Wait a few seconds and tell agent "The PR is merged". Agent will pull latest changes from main.

### **"Can I review multiple PRs at once?"**

No, each epic gets one PR. Review and merge one PR at a time.

### **"What if I accidentally merged a PR I shouldn't have?"**

1. Tell agent immediately
2. Agent can revert the PR merge:
   ```bash
   git revert -m 1 {merge_commit_hash}
   git push origin main
   ```
3. Agent can fix issues and create new PR

---

## Best Practices

**For every PR:**
1. ✅ Read the PR description (epic summary, features, tests)
2. ✅ Check test results (should be 100% passing)
3. ✅ Skim all changed files (don't need to read every line)
4. ✅ Focus on high-impact files (core logic, not tests)
5. ✅ Look for obvious issues (debugging code, TODOs, etc.)
6. ✅ Trust the agent's QC process (3 rounds + smoke testing)
7. ✅ Approve and merge if nothing concerning

**Time management:**
- Small epic (1-2 features): 5-10 minutes
- Medium epic (3-4 features): 10-20 minutes
- Large epic (5+ features): 20-30 minutes

**When to deep-dive:**
- Epic introduces new architecture
- Epic touches critical systems
- You're learning the codebase
- Agent made mistakes in past PRs

---

## Summary

**Quick Workflow:**
1. Agent completes epic → Creates PR → Provides URL
2. You review PR (Web UI, VS Code, or CLI)
3. You approve and merge
4. Agent updates EPIC_TRACKER.md and moves epic to done/

**Recommended Setup for Regular Use:**
- Install "GitHub Pull Requests & Issues" VS Code extension
- Review in VS Code (familiar environment)
- Fall back to Web UI for complex reviews

**First Time:**
- Use GitHub Web UI (zero setup)
- See if you like the workflow
- Add tools later if needed

---

## Resources

**Official Documentation:**
- GitHub PR Reviews: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests
- GitHub CLI Manual: https://cli.github.com/manual/
- VS Code GitHub Extension: https://code.visualstudio.com/docs/sourcecontrol/github

**Tools:**
- GitHub CLI: https://cli.github.com/
- VS Code GitHub Extension: Search "GitHub Pull Requests and Issues" in VS Code
- Meld Diff Tool: https://meldmerge.org/
- Beyond Compare: https://www.scootersoftware.com/

**Need Help?**
- Ask agent: "How do I review the PR?"
- Agent can provide specific instructions
- Agent can create screenshots/examples if needed
