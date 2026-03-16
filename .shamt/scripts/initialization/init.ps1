# =============================================================================
# Shamt Initialization Script (PowerShell — Windows)
# =============================================================================
# Run this script from the root of the project you want to initialize Shamt in.
# Usage: & "C:\path\to\shamt-ai-dev\.shamt\scripts\initialization\init.ps1"
# =============================================================================

$ErrorActionPreference = "Stop"

$ShamtSourceDir = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
$TargetDir = Get-Location
$ShamtDir = Join-Path $TargetDir ".shamt"

Write-Host ""
Write-Host "============================================================"
Write-Host "  Shamt Initialization"
Write-Host "============================================================"
Write-Host "  Source: $ShamtSourceDir"
Write-Host "  Target: $TargetDir"
Write-Host "============================================================"
Write-Host ""

# --- Helpers -----------------------------------------------------------------

function Prompt-Input {
    param([string]$Question, [string]$Default = "")
    if ($Default) {
        $answer = Read-Host "$Question [$Default]"
        if ([string]::IsNullOrWhiteSpace($answer)) { return $Default }
        return $answer
    } else {
        return Read-Host $Question
    }
}

function Prompt-Required {
    param([string]$Question)
    $answer = ""
    while ([string]::IsNullOrWhiteSpace($answer)) {
        $answer = Read-Host $Question
        if ([string]::IsNullOrWhiteSpace($answer)) {
            Write-Host "  (This field is required)" -ForegroundColor Yellow
        }
    }
    return $answer
}

function Write-Separator {
    param([string]$Title)
    Write-Host ""
    Write-Host "------------------------------------------------------------"
    Write-Host "  $Title"
    Write-Host "------------------------------------------------------------"
}

function Apply-Substitutions {
    param([string]$FilePath, [hashtable]$Replacements)
    $content = Get-Content $FilePath -Raw
    foreach ($key in $Replacements.Keys) {
        $content = $content -replace [regex]::Escape($key), $Replacements[$key]
    }
    Set-Content $FilePath $content -NoNewline
}

function Add-ExcludeEntry {
    param([string]$ExcludeFile, [string]$Entry)
    if (Test-Path $ExcludeFile) {
        $existing = Get-Content $ExcludeFile -Raw
        if ($existing -notlike "*$Entry*") {
            Add-Content $ExcludeFile "`n$Entry"
        }
    } else {
        Set-Content $ExcludeFile $Entry
    }
}

# --- AI Service Selection ----------------------------------------------------

Write-Separator "AI Service"
Write-Host "Which AI coding assistant will you use with this project?"
Write-Host ""
Write-Host "  1) Claude Code (Anthropic)       -> CLAUDE.md at project root"
Write-Host "  2) GitHub Copilot                -> .github/copilot-instructions.md"
Write-Host "  3) Cursor                        -> .cursorrules at project root"
Write-Host "  4) Windsurf (Codeium)            -> .windsurfrules at project root"
Write-Host "  5) Amazon Q Developer            -> (setup TBD)"
Write-Host "  6) Other                         -> you will specify"
Write-Host ""
$aiChoice = Prompt-Input "Enter choice" "1"

switch ($aiChoice) {
    "2" { $AiService = "github_copilot"; $RulesFileName = "copilot-instructions.md"; $RulesFileSubdir = ".github" }
    "3" { $AiService = "cursor"; $RulesFileName = ".cursorrules"; $RulesFileSubdir = "" }
    "4" { $AiService = "windsurf"; $RulesFileName = ".windsurfrules"; $RulesFileSubdir = "" }
    "5" {
        $AiService = "amazon_q"; $RulesFileName = "TBD"; $RulesFileSubdir = ""
        Write-Host "  WARNING: Amazon Q rules file convention is not yet confirmed." -ForegroundColor Yellow
        Write-Host "  The agent will help you determine the correct setup." -ForegroundColor Yellow
    }
    "6" {
        $AiService = "other"
        $RulesFileName = Prompt-Required "  Rules file name (e.g. .myrules)"
        $subdir = Prompt-Input "  Rules file subdirectory relative to project root (leave blank for root)" ""
        $RulesFileSubdir = $subdir
    }
    default { $AiService = "claude_code"; $RulesFileName = "CLAUDE.md"; $RulesFileSubdir = "" }
}

if ($RulesFileSubdir) {
    $RulesFileDir = Join-Path $TargetDir $RulesFileSubdir
} else {
    $RulesFileDir = $TargetDir
}

Write-Host "  OK AI service: $AiService"

# --- Project Details ---------------------------------------------------------

Write-Separator "Project Details"

$ProjectName = Prompt-Required "  Project name"
$EpicTag = (Prompt-Input "  Epic tag (e.g. SHAMT, MYPROJ)" "SHAMT").ToUpper()
$ShamtName = Prompt-Input "  Agent name (your version of Shamt)" "Shamt"
$StartingEpic = Prompt-Input "  Starting epic number" "1"

# --- Git Configuration -------------------------------------------------------

Write-Separator "Git Configuration"

Write-Host "Which git platform will you use?"
Write-Host "  1) GitHub"
Write-Host "  2) GitLab"
Write-Host "  3) Other / none"
$gitChoice = Prompt-Input "Enter choice" "1"

switch ($gitChoice) {
    "2" { $GitPlatform = "gitlab" }
    "3" { $GitPlatform = "other" }
    default { $GitPlatform = "github" }
}

$DefaultBranch = Prompt-Input "  Default/main branch name" "main"

Write-Host "  OK Git platform: $GitPlatform"
Write-Host "  OK Default branch: $DefaultBranch"

# --- Repository Configuration ------------------------------------------------

Write-Separator "Repository Configuration"

Write-Host "  Should .shamt/ and the rules file be excluded from git in this project?"
Write-Host "  This uses .git/info/exclude — local only, never committed or visible to other users."
Write-Host "  Default: YES (recommended for solo/multi-agent work — keeps epic state files out of git)."
Write-Host "  Choose 'no' only if you need to share .shamt/ with other developers via git."
Write-Host ""
$excludeChoice = Prompt-Input "  Locally exclude .shamt/ and rules file from git? [Y/n]" "Y"
if ($excludeChoice -match '^[Yy]$') {
    $ExcludeShamt = $true
} else {
    $ExcludeShamt = $false
}

Write-Host "  OK Locally exclude .shamt/ and rules file (default: yes): $ExcludeShamt"

# --- Confirmation ------------------------------------------------------------

Write-Separator "Review"
Write-Host "  Project name:          $ProjectName"
Write-Host "  Epic tag:              $EpicTag"
Write-Host "  Agent name:            $ShamtName"
Write-Host "  Starting epic #:       $StartingEpic"
Write-Host "  AI service:            $AiService"
Write-Host "  Rules file:            $RulesFileName"
Write-Host "  Rules file path:       $RulesFileDir\"
Write-Host "  Git platform:          $GitPlatform"
Write-Host "  Default branch:        $DefaultBranch"
Write-Host "  Exclude .shamt/ (local): $ExcludeShamt"
Write-Host "  Epic directory:        .shamt\epics\"
Write-Host ""

$confirm = Prompt-Input "Proceed with initialization? [Y/n]" "Y"
if ($confirm -notmatch '^[Yy]$') {
    Write-Host "Initialization cancelled."
    exit 0
}

# --- Create Folder Structure -------------------------------------------------

Write-Separator "Creating folder structure"

$dirs = @(
    "$ShamtDir\guides",
    "$ShamtDir\scripts",
    "$ShamtDir\project-specific-configs",
    "$ShamtDir\epics\requests",
    "$ShamtDir\epics\done",
    $RulesFileDir
)
foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
}

Write-Host "  OK .shamt\ structure created"

# --- Write Config Files ------------------------------------------------------

Write-Separator "Writing config files"

Set-Content "$ShamtDir\shamt_master_path.conf" $ShamtSourceDir -NoNewline
Write-Host "  OK Master path written to .shamt\shamt_master_path.conf"

$rulesFilePath = Join-Path $RulesFileDir $RulesFileName
Set-Content "$ShamtDir\rules_file_path.conf" $rulesFilePath -NoNewline
Write-Host "  OK Rules file path written to .shamt\rules_file_path.conf"

$syncDate = Get-Date -Format "yyyy-MM-dd"
$masterHashResult = & git -C $ShamtSourceDir rev-parse --short HEAD 2>&1
$masterHash = if ($LASTEXITCODE -eq 0) { ($masterHashResult | Out-String).Trim() } else { "unknown" }
Set-Content (Join-Path $ShamtDir "last_sync.conf") "$syncDate | $masterHash" -NoNewline
Write-Host "  OK Sync state written to .shamt\last_sync.conf"

# --- Configure local git excludes --------------------------------------------

Write-Separator "Configuring local git excludes"

$GitExcludeDir = Join-Path $TargetDir ".git\info"
$GitExcludeFile = Join-Path $GitExcludeDir "exclude"

if (-not (Test-Path $GitExcludeDir)) {
    Write-Host "  WARNING: .git\info\ not found — is this a git repository?" -ForegroundColor Yellow
    Write-Host "  Run 'git init' first, then re-run init to apply local excludes." -ForegroundColor Yellow
    Write-Host "  Skipping local excludes configuration." -ForegroundColor Yellow
} else {
    # Always exclude *.conf files (covers shamt_master_path.conf, last_sync.conf, rules_file_path.conf, etc.)
    Add-ExcludeEntry -ExcludeFile $GitExcludeFile -Entry ".shamt/*.conf"
    Write-Host "  OK .shamt/*.conf added to .git/info/exclude (always)"

    # Always exclude import_diff*.md (transient diff files — never commit)
    Add-ExcludeEntry -ExcludeFile $GitExcludeFile -Entry ".shamt/import_diff*.md"
    Write-Host "  OK .shamt/import_diff*.md added to .git/info/exclude (always)"

    # Always exclude VALIDATION_LOG* (transient validation logs — never commit)
    Add-ExcludeEntry -ExcludeFile $GitExcludeFile -Entry "*VALIDATION_LOG*"
    Write-Host "  OK *VALIDATION_LOG* added to .git/info/exclude (always)"

    # Optionally exclude .shamt/ and rules file
    if ($ExcludeShamt) {
        # Warn if .shamt/ is already tracked by git (migration required)
        $trackedCheck = & git -C $TargetDir ls-files .shamt/ 2>&1 | Select-Object -First 1
        if ($LASTEXITCODE -eq 0 -and -not [string]::IsNullOrWhiteSpace($trackedCheck)) {
            Write-Host ""
            Write-Host "  WARNING: .shamt/ is currently tracked by git. To migrate:" -ForegroundColor Yellow
            Write-Host "       git rm -r --cached .shamt/" -ForegroundColor Yellow
            Write-Host "       git commit -m ""stop tracking .shamt/ framework directory""" -ForegroundColor Yellow
            Write-Host "  (Continuing -- adding .shamt/ to .git/info/exclude now; run the commands above when ready)" -ForegroundColor Yellow
        }
        Add-ExcludeEntry -ExcludeFile $GitExcludeFile -Entry ".shamt/"
        if ($RulesFileDir -eq $TargetDir) {
            $RulesExcludePath = $RulesFileName
        } else {
            $RulesExcludePath = (Resolve-Path -Relative $rulesFilePath).TrimStart(".\").Replace("\", "/")
        }
        Add-ExcludeEntry -ExcludeFile $GitExcludeFile -Entry $RulesExcludePath
        Write-Host "  OK .shamt/ and $RulesExcludePath added to .git/info/exclude"
    }
}

# --- Copy Guides -------------------------------------------------------------

Write-Separator "Copying guides"

Copy-Item -Path "$ShamtSourceDir\.shamt\guides\*" -Destination "$ShamtDir\guides\" -Recurse -Force
# Exclude master's audit output history — child projects start fresh
$auditOutputs = Join-Path $ShamtDir "guides\audit\outputs"
if (Test-Path $auditOutputs) {
    Remove-Item $auditOutputs -Recurse -Force
}
New-Item -ItemType Directory -Force -Path $auditOutputs | Out-Null
Write-Host "  OK Guides copied (audit/outputs/ cleared for fresh start)"

# --- Copy Scripts ------------------------------------------------------------

Write-Separator "Copying scripts"

Copy-Item -Path "$ShamtSourceDir\.shamt\scripts\*" -Destination "$ShamtDir\scripts\" -Recurse -Force
Write-Host "  OK Scripts copied"

# --- Configure Rules File ----------------------------------------------------

Write-Separator "Configuring rules file"

$RulesDest = Join-Path $RulesFileDir $RulesFileName
$RulesTemplate = Join-Path $ShamtDir "scripts\initialization\RULES_FILE.template.md"
$RulesFileExisted = $false

if (Test-Path $RulesDest) {
    Write-Host "  WARNING: $RulesFileName already exists at $RulesFileDir\" -ForegroundColor Yellow
    $overwrite = Prompt-Input "  Overwrite? [y/N]" "N"
    if ($overwrite -notmatch '^[Yy]$') {
        Write-Host "  Skipping rules file - agent will incorporate existing file."
        $RulesFileExisted = $true
    }
}

if (-not $RulesFileExisted) {
    Copy-Item $RulesTemplate $RulesDest -Force
    Write-Host "  OK Rules file written to $RulesDest"
}

# --- Apply Substitutions -----------------------------------------------------

Write-Separator "Applying configuration"

$replacements = @{
    "{{PROJECT_NAME}}"   = $ProjectName
    "{{EPIC_TAG}}"       = $EpicTag
    "{{SHAMT_NAME}}"     = $ShamtName
    "{{GIT_PLATFORM}}"   = $GitPlatform
    "{{DEFAULT_BRANCH}}" = $DefaultBranch
    "SHAMT-{N}"          = "$EpicTag-{N}"
}

# Apply to rules file
if (-not $RulesFileExisted) {
    Apply-Substitutions -FilePath $RulesDest -Replacements $replacements
}

# Apply to guides (epic tag and branch name only)
Get-ChildItem -Path "$ShamtDir\guides" -Filter "*.md" -Recurse | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $content = $content -replace [regex]::Escape("{{EPIC_TAG}}"), $EpicTag
    $content = $content -replace [regex]::Escape("SHAMT-{N}"), "$EpicTag-{N}"
    $content = $content -replace [regex]::Escape("{{DEFAULT_BRANCH}}"), $DefaultBranch
    $content = $content -replace [regex]::Escape("{{GIT_PLATFORM}}"), $GitPlatform
    Set-Content $_.FullName $content -NoNewline
}

# Create EPIC_TRACKER.md
$epicTrackerDest = Join-Path $ShamtDir "epics\EPIC_TRACKER.md"
Copy-Item (Join-Path $ShamtDir "scripts\initialization\EPIC_TRACKER.template.md") $epicTrackerDest -Force
Apply-Substitutions -FilePath $epicTrackerDest -Replacements $replacements
(Get-Content $epicTrackerDest -Raw) -replace "$EpicTag-1", "$EpicTag-$StartingEpic" | Set-Content $epicTrackerDest -NoNewline

Write-Host "  OK Configuration applied"

# --- Write init_config.md Handoff File ---------------------------------------

Write-Separator "Writing handoff file for agent"

$needsAiDiscovery = ($AiService -eq "other" -or $AiService -eq "amazon_q")
$today = Get-Date -Format "yyyy-MM-dd"
$rulesNote = if ($RulesFileExisted) {
    "- Existing rules file was preserved — agent should incorporate it into the new rules file content."
} else {
    "- Rules file written fresh from template."
}
$aiNote = if ($needsAiDiscovery) {
    "- AI service '$AiService' needs rules file convention confirmed. Agent should research and update ai_services.md."
} else { "" }
$excludeNote = if ($ExcludeShamt) {
    "- .shamt/ and rules file are excluded via .git/info/exclude (local only — not committed or visible to other users)."
} else {
    "- .shamt/ is not excluded from git — it will be tracked and visible to all repo users."
}

$initConfigContent = @"
# Shamt Initialization Config

**Generated:** $today
**Status:** PENDING_AGENT_COMPLETION

## Project Configuration
- **Project Name:** $ProjectName
- **Epic Tag:** $EpicTag
- **Shamt Agent Name:** $ShamtName
- **Starting Epic Number:** $StartingEpic
- **Epic Working Directory:** .shamt/epics/

## AI Service
- **Service:** $AiService
- **Rules File Name:** $RulesFileName
- **Rules File Path:** $RulesFileDir\
- **Rules File Template:** .shamt\scripts\initialization\RULES_FILE.template.md
- **Needs AI Discovery:** $($needsAiDiscovery.ToString().ToLower())

## Git Configuration
- **Platform:** $GitPlatform
- **Default Branch:** $DefaultBranch

## Script Actions Completed
- [x] Created .shamt\ folder structure (including project-specific-configs\)
- [x] Copied guides from master Shamt (audit\outputs\ cleared for fresh start)
- [x] Copied scripts from master Shamt
- [x] Placed rules file at $RulesFileDir\$RulesFileName
- [x] Created EPIC_TRACKER.md at .shamt\epics\EPIC_TRACKER.md
- [x] Written .shamt\shamt_master_path.conf
- [x] Written .shamt\rules_file_path.conf
- [x] Written .shamt\last_sync.conf (initialized from master HEAD)
- [x] Applied configuration substitutions to guides and rules file

## Agent Remaining Tasks

**Before beginning:** Re-read the validation loop protocol at:
`.shamt/guides/reference/validation_loop_master_protocol.md`

Then run a validation loop to complete initialization:

- [ ] Handle AI service discovery (if Needs AI Discovery = true)
- [ ] Analyze codebase structure, languages, frameworks
- [ ] Ask clarifying questions until codebase is fully understood
- [ ] Write ARCHITECTURE.md to `.shamt/project-specific-configs/`
- [ ] Write CODING_STANDARDS.md to `.shamt/project-specific-configs/`
- [ ] Add 3-5 key coding rules to rules file summary section
- [ ] Fill in Project Context section in rules file (tech stack, runtime, test runner, deployment target, critical gotchas)
- [ ] Validate all outputs meet quality bar (3 consecutive clean validation rounds)
- [ ] Mark this file complete: change Status to COMPLETE

## Notes
$rulesNote
$aiNote
$excludeNote
- ARCHITECTURE.md and CODING_STANDARDS.md belong in `.shamt/project-specific-configs/`, not the project root.
- Shared guide files in `.shamt/guides/` must remain generic — never write project-specific content into them.
- The only exception: a pointer note in a shared guide directing the agent to check `.shamt/project-specific-configs/` for a supplement.
"@

Set-Content "$ShamtDir\project-specific-configs\init_config.md" $initConfigContent

Write-Host "  OK Handoff file written to .shamt\project-specific-configs\init_config.md"

# --- Done --------------------------------------------------------------------

Write-Separator "Done!"
Write-Host ""
Write-Host "  Shamt has been initialized in: $TargetDir"
Write-Host ""
Write-Host "  Next step: open your project in $ShamtName (your AI assistant) and say:"
Write-Host ""
Write-Host "    `"Read .shamt/project-specific-configs/init_config.md and complete the Shamt initialization.`""
Write-Host ""
Write-Host "  The agent will analyze your codebase and finish setup."
Write-Host ""
Write-Host "  To sync with master later:"
Write-Host "    Import updates from master: bash .shamt/scripts/import/import.sh (or import.ps1)"
Write-Host "    Export changes to master:   bash .shamt/scripts/export/export.sh (or export.ps1)"
Write-Host ""
Write-Host "============================================================"
Write-Host ""
