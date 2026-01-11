# Research: User PR Review Tools (#7)

**Date:** 2026-01-10
**Request:** "I want a way to more easily let the user do their own PR"
**Approach:** Research existing tools + GitHub PR workflow modification

---

## Executive Summary

**Recommendation:** Implement **GitHub PR workflow** (push to branch, create PR to main) + provide users with **tool recommendations** for local review.

**Why this approach:**
- ✅ GitHub PR UI provides best-in-class code review experience (diff view, inline comments, approval workflow)
- ✅ Works with any IDE/editor the user prefers
- ✅ Integrates with GitHub Actions for automated checks
- ✅ Maintains clean git history with PR merge commits
- ✅ Users can use additional tools (VS Code extensions, CLI, diff tools) based on preference

---

## Category 1: VS Code Extensions (In-Editor Review)

### **Essential Extensions**

#### 1. **GitHub Pull Requests & Issues**
- **What:** Official GitHub extension - review and manage PRs without leaving VS Code
- **Best for:** Users who want GitHub PR workflow integrated into their editor
- **Key features:** View diffs, leave comments, approve/request changes, merge PRs
- **Install:** Search "GitHub Pull Requests" in VS Code extensions
- **Source:** [Best VS Code Extensions for AI Development](https://graphite.com/guides/best-vscode-extensions-ai)

#### 2. **GitLens**
- **What:** Supercharges Git capabilities in VS Code
- **Best for:** Understanding code history and context during review
- **Key features:** Blame annotations, commit history, file history, compare branches
- **Why useful:** See who last modified each line, understand why changes were made
- **Source:** [Enhancing Code Reviews with VSCode](https://thiraphat-ps-dev.medium.com/enhancing-your-code-reviews-with-vscode-essential-tools-and-extensions-fa3881abe5e4)

#### 3. **CodeStream**
- **What:** Collaborative code review directly in VS Code
- **Best for:** Team code reviews (supports GitHub, GitLab, Bitbucket)
- **Key features:** Inline discussions, issue tracking, integrates with existing workflow
- **Source:** [Top VSCode Extensions 2026](https://www.jit.io/blog/vscode-extensions-for-2023)

### **AI-Powered Review Extensions**

#### 4. **Sourcery**
- **What:** AI code review and refactoring tool
- **Best for:** Automated code quality checks during review
- **Key features:** Suggests improvements, detects code smells, refactoring hints
- **Source:** [Best VSCode Extensions 2026](https://rasathuraikaran26.medium.com/best-vs-code-extensions-2026-top-tools-every-developer-must-try-5bfa8f9e8a05)

#### 5. **Vortex**
- **What:** GPT-powered code editing and review
- **Best for:** Natural language code review ("explain this change", "find issues")
- **Source:** [AI Tools for Coding 2026](https://manus.im/blog/best-ai-coding-assistant-tools)

#### 6. **Windsurf Reviews**
- **What:** AI code review for quality and consistency
- **Best for:** Catching quality issues automatically
- **Source:** [Best AI Coding Tools 2026](https://manus.im/blog/best-ai-coding-assistant-tools)

### **Code Quality Extensions**

#### 7. **SonarLint**
- **What:** Detects quality issues and security vulnerabilities as you write
- **Best for:** Catching bugs and security issues before review
- **Languages:** JavaScript, TypeScript, Python, Java, and more
- **Source:** [Enhancing Code Reviews with VSCode](https://thiraphat-ps-dev.medium.com/enhancing-your-code-reviews-with-vscode-essential-tools-and-extensions-fa3881abe5e4)

#### 8. **Better Comments**
- **What:** Create human-friendly comments with annotations (TODO, FIXME, NOTE)
- **Best for:** Making comments stand out during review
- **Source:** [Enhancing Code Reviews with VSCode](https://thiraphat-ps-dev.medium.com/enhancing-your-code-reviews-with-vscode-essential-tools-and-extensions-fa3881abe5e4)

---

## Category 2: CLI Tools (Terminal-Based Review)

### **GitHub CLI (gh) - Official Tool**

#### **Core Commands:**
```bash
# Review PRs from command line
gh pr review <pr-number>

# Find your open PRs across all repos
gh search prs author:@me is:open

# Find PRs that need your review
gh search prs review-requested:@me is:open

# Check CI status
gh pr checks

# View PR diff
gh pr diff <pr-number>

# Approve PR
gh pr review <pr-number> --approve

# Request changes
gh pr review <pr-number> --request-changes --body "Comments here"

# View PR details
gh pr view <pr-number>
```

**Source:** [GitHub CLI Manual](https://cli.github.com/manual/gh_pr_review), [GitHub CLI Power Tips 2026](https://onlyutkarsh.com/posts/2026/github-cli-power-tips/)

#### **Enhanced PR Review Extension:**
```bash
# Install gh-pr-review extension
gh extension install agynio/gh-pr-review

# Read PR comments including inline comments
gh pr-review review view
```

**Source:** [Using GitHub CLI to Review PR](https://www.jesusamieiro.com/using-the-github-cli-to-review-pr/)

### **AI-Powered CLI Tools**

#### **PR-Agent (Qodo AI)**
```bash
# Install
pip install pr-agent

# Review PR from CLI
pr-agent --pr_url https://github.com/owner/repo/pull/123 review

# Each tool uses single LLM call (~30 seconds)
```

**What:** AI-powered PR reviewer using LLMs
**Best for:** Automated code review suggestions
**Source:** [Qodo PR-Agent GitHub](https://github.com/qodo-ai/pr-agent), [Best GitHub AI Code Review Tools 2026](https://www.codeant.ai/blogs/best-github-ai-code-review-tools-2025)

#### **Reviewdog**
```bash
# List supported error formats
reviewdog -list

# Use with specific format
reviewdog -f={name}
```

**What:** Automated code review tool integrated with any code analysis tools
**Best for:** Running linters and formatters with PR comments
**Source:** [Reviewdog GitHub](https://github.com/reviewdog/reviewdog)

---

## Category 3: Standalone Diff/Merge Tools

### **Free & Open Source**

#### **1. Meld**
- **Platform:** Linux, Windows, Mac
- **Best for:** Visual diff and merge with 2-way or 3-way comparison
- **Why recommended:** Clear UI, open-source, widely used
- **Use case:** Compare agent changes vs your expected changes
- **Website:** [meldmerge.org](https://meldmerge.org/)
- **Source:** [11 Diff and Merge Tools](https://geekflare.com/dev/diff-and-merge-tools/)

#### **2. WinMerge** (Windows only)
- **Platform:** Windows
- **Best for:** Comparing folders and files with Windows integration
- **Why recommended:** Free, integrates with Windows Explorer, easy to use
- **Use case:** Folder-level comparisons across epic changes
- **Source:** [Best Diff Tools for Git](https://www.slant.co/topics/1324/~best-diff-tools-for-git)

#### **3. Code Compare**
- **Platform:** Windows (standalone or Visual Studio extension)
- **Best for:** Integration with source control (TFS, SVN, Git, Mercurial, Perforce)
- **Why recommended:** Free version available, designed specifically for code
- **Website:** [devart.com/codecompare](https://www.devart.com/codecompare/)
- **Source:** [DiffMerge Alternatives](https://alternativeto.net/software/diffmerge/)

### **Commercial Options**

#### **4. Beyond Compare** ($60)
- **Platform:** Windows, Mac, Linux
- **Best for:** Advanced file/folder comparison, FTP, sync
- **Why recommended:** Industry standard, powerful features, worth the cost for heavy use
- **Use case:** Deep comparison across multiple features in epic
- **Source:** [Beyond Compare Alternatives 2026](https://slashdot.org/software/p/Beyond-Compare/alternatives)

#### **5. Araxis Merge** ($129-$269)
- **Platform:** Windows, Mac
- **Best for:** Professional code review and audit trails
- **Why recommended:** Can create standalone HTML/XML reports of findings
- **Use case:** Generate review reports for complex epics
- **Website:** [araxis.com/merge](https://www.araxis.com/merge/index.en)
- **Source:** [Araxis Merge](https://www.araxis.com/merge/index.en)

#### **6. DeltaWalker**
- **Platform:** Windows, Mac, Linux
- **Best for:** Binary-level comparison, three-way merging
- **Why recommended:** Powerful for finding subtle differences
- **Source:** [DiffMerge Alternatives](https://alternativeto.net/software/diffmerge/)

---

## Category 4: Full Code Review Platforms

### **Team Collaboration Tools**

#### **Gerrit**
- **What:** Combines bug tracker and review tool
- **Best for:** Team code reviews with side-by-side diffs
- **Features:** Line-by-line conversations, approval workflow
- **Source:** [12 Best Code Review Tools 2026](https://kinsta.com/blog/code-review-tools/)

#### **Crucible (Atlassian)**
- **What:** Enterprise code review from Atlassian (makers of Jira)
- **Best for:** Organizations already using Atlassian products
- **Source:** [12 Best Code Review Tools 2026](https://kinsta.com/blog/code-review-tools/)

#### **Collaborator (SmartBear)**
- **What:** Enterprise peer code review
- **Best for:** Large teams with formal review processes
- **Source:** [12 Best Code Review Tools 2026](https://kinsta.com/blog/code-review-tools/)

---

## Recommended Workflow: GitHub PR Approach

### **Why GitHub PR Workflow?**

**Current workflow issues:**
- Agent merges directly to `main` after Stage 7
- User has no opportunity to review before merge
- Mistakes in `main` require revert commits

**GitHub PR workflow benefits:**
- ✅ User reviews changes in GitHub PR UI (best-in-class diff view)
- ✅ Can request changes before merge
- ✅ GitHub Actions can run automated checks
- ✅ Clean git history with PR merge commits
- ✅ Works with any tool the user prefers (VS Code, CLI, diff tools)
- ✅ Standard 2026 best practice for team workflows

**Source:** [Git Feature Branch Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow), [Pull Request Workflow Guide](https://medium.com/@urna.hybesis/pull-request-workflow-with-git-6-steps-guide-3858e30b5fa4)

### **Modified Workflow (Stage 7)**

**Current (Direct merge to main):**
```bash
# Stage 7 - Epic Cleanup (current)
git checkout main
git pull origin main
git merge epic/KAI-{N}
git push origin main
```

**Proposed (Push branch + Create PR):**
```bash
# Stage 7 - Epic Cleanup (modified)
git push origin epic/KAI-{N}  # Push branch to remote
gh pr create --base main --head epic/KAI-{N} \
  --title "Epic KAI-{N}: {epic_name}" \
  --body "$(cat <<'EOF'
## Epic Summary
{High-level description}

## Features Completed
- Feature 01: {name}
- Feature 02: {name}
- {Continue for all features}

## Test Status
- Unit tests: 2,486/2,486 passing (100%)
- Epic smoke tests: PASSED
- User testing: PASSED (no bugs found)

## Files Changed
- {N} files changed
- {additions} insertions, {deletions} deletions

## Review Checklist for User
- [ ] Review epic_smoke_test_plan.md results
- [ ] Review lessons_learned.md for all features
- [ ] Review code changes in GitHub PR diff view
- [ ] Verify all requirements from original {epic_name}.txt met
- [ ] Approve and merge when satisfied

🤖 Generated with Claude Code

Epic folder: feature-updates/KAI-{N}-{epic_name}/
EOF
)"

# Agent outputs PR URL for user
echo "Pull Request created: {PR_URL}"
echo "Please review the PR and merge when satisfied."
```

**User review process:**
1. Open PR URL in browser
2. Review changes in GitHub UI (or use VS Code extension / CLI)
3. Leave comments on specific lines if needed
4. Request changes or approve
5. Merge when satisfied

---

## Implementation Plan for Guides

### **Files to Modify:**

#### **1. stage_7/epic_cleanup.md**
- **Current:** Steps 6-7 merge to main and push
- **Change:** Replace with "push branch + create PR" workflow
- **Add:** User review step before merge
- **Add:** Instructions for using gh CLI to create PR

#### **2. CLAUDE.md - Git Branching Workflow**
- **Current:** "When completing an epic (Stage 7): Commit changes on branch, Merge to main"
- **Change:** "When completing an epic (Stage 7): Commit changes on branch, Push to remote, Create PR to main"
- **Add:** Note about user review and merge

#### **3. New File: USER_PR_REVIEW_GUIDE.md**
- **Location:** `feature-updates/`
- **Content:**
  - Recommended tools (from this research)
  - How to review PRs in GitHub UI
  - How to use VS Code extensions
  - How to use GitHub CLI
  - How to use diff tools
  - Approval workflow

#### **4. prompts/stage_7_prompts.md**
- **Update:** Phase transition prompt for Stage 7
- **Add:** Instructions to create PR instead of merge

---

## Tool Recommendations by User Preference

### **For VS Code Users (Easiest):**
1. Install "GitHub Pull Requests & Issues" extension
2. Install "GitLens" for code history
3. Review PR directly in VS Code
4. Approve and merge from VS Code

### **For Command Line Users:**
```bash
# Install GitHub CLI
gh pr list
gh pr view {number}
gh pr diff {number}
gh pr review {number} --approve
gh pr merge {number}
```

### **For Visual Diff Users:**
1. Download **Meld** (free) or **Beyond Compare** ($60)
2. Check out PR branch locally
3. Compare branch to main using diff tool
4. Approve PR in GitHub UI

### **For Hands-Off Users:**
1. Open PR URL in browser
2. Review changes in GitHub UI
3. Click "Approve" and "Merge"
4. Done!

---

## Next Steps

**Immediate action:**
1. User reviews this research document
2. User decides: Implement GitHub PR workflow? (Recommended: YES)
3. User picks preferred review tool(s) from recommendations

**If YES to GitHub PR workflow:**
1. Modify stage_7/epic_cleanup.md (replace merge with PR creation)
2. Update CLAUDE.md Git Branching Workflow section
3. Create USER_PR_REVIEW_GUIDE.md with tool recommendations
4. Update prompts/stage_7_prompts.md
5. Test workflow on next epic

**Tool setup (user chooses):**
- [ ] Install VS Code extension: "GitHub Pull Requests & Issues"
- [ ] Install VS Code extension: "GitLens"
- [ ] Install GitHub CLI: `gh` (if not already installed)
- [ ] Install diff tool: Meld (free) or Beyond Compare ($60)
- [ ] Set up AI review tool: PR-Agent (optional)

---

## Sources

**VS Code Extensions:**
- [Best VS Code Extensions for 2026](https://www.builder.io/blog/best-vs-code-extensions-2026)
- [10 Must-Know VS Code Extensions 2026](https://dev.to/thebitforge/10-must-know-vs-code-extensions-for-supercharged-development-in-2026-5c8a)
- [Best VS Code Extensions for AI Development](https://graphite.com/guides/best-vscode-extensions-ai)
- [Code Review Extension](https://marketplace.visualstudio.com/items?itemName=d-koppenhagen.vscode-code-review)
- [Enhancing Code Reviews with VSCode](https://thiraphat-ps-dev.medium.com/enhancing-your-code-reviews-with-vscode-essential-tools-and-extensions-fa3881abe5e4)
- [Best AI Coding Tools 2026](https://manus.im/blog/best-ai-coding-assistant-tools)

**GitHub CLI & Workflow:**
- [GitHub CLI Manual - PR Review](https://cli.github.com/manual/gh_pr_review)
- [GitHub CLI Power Tips 2026](https://onlyutkarsh.com/posts/2026/github-cli-power-tips/)
- [Using GitHub CLI to Review PR](https://www.jesusamieiro.com/using-the-github-cli-to-review-pr/)
- [Qodo PR-Agent](https://github.com/qodo-ai/pr-agent)
- [Reviewdog](https://github.com/reviewdog/reviewdog)
- [Best GitHub AI Code Review Tools 2026](https://www.codeant.ai/blogs/best-github-ai-code-review-tools-2025)

**Diff/Merge Tools:**
- [Best Diff Tools for Git](https://www.slant.co/topics/1324/~best-diff-tools-for-git)
- [Comprehensive Guide to Diff Tools](https://graphite.com/guides/comprehensive-guide-to-diff-tools)
- [Araxis Merge](https://www.araxis.com/merge/index.en)
- [Meld](https://meldmerge.org/)
- [Code Compare](https://www.devart.com/codecompare/)
- [11 Diff and Merge Tools](https://geekflare.com/dev/diff-and-merge-tools/)
- [12 Best Code Review Tools 2026](https://kinsta.com/blog/code-review-tools/)
- [DiffMerge Alternatives](https://alternativeto.net/software/diffmerge/)
- [Beyond Compare Alternatives 2026](https://slashdot.org/software/p/Beyond-Compare/alternatives)

**Git Workflow:**
- [Git Feature Branch Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow)
- [Pull Request Workflow Guide](https://medium.com/@urna.hybesis/pull-request-workflow-with-git-6-steps-guide-3858e30b5fa4)
- [Feature Branch Workflow: Local Merge vs PR](https://medium.com/@jahangir80842/feature-branch-workflow-39c16d11e3fc)
- [What Is a Pull Request?](https://www.atlassian.com/git/tutorials/making-a-pull-request)
