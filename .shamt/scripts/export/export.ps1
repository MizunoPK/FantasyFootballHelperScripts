# =============================================================================
# Shamt Export Script (PowerShell — Windows)
# =============================================================================
# Run this script from the root of your child project.
# Usage: & ".shamt\scripts\export\export.ps1"
#
# Copies all modified shared files (guides/ and scripts/) from this project
# to the local shamt-ai-dev master repo. Open a PR after running.
# =============================================================================

param(
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$ChildShamtDir = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$ChildRoot = Split-Path -Parent $ChildShamtDir

# --- Read master path --------------------------------------------------------

$MasterPathConf = Join-Path $ChildShamtDir "shamt_master_path.conf"
if (-not (Test-Path $MasterPathConf)) {
    Write-Host ""
    Write-Host "  Error: .shamt\shamt_master_path.conf not found." -ForegroundColor Red
    Write-Host "  Run the init script to set up the master path."
    Write-Host ""
    exit 1
}

$MasterDir = (Get-Content $MasterPathConf -Raw).Trim()
if (-not (Test-Path $MasterDir)) {
    Write-Host ""
    Write-Host "  Error: Master directory not found: $MasterDir" -ForegroundColor Red
    Write-Host "  Update .shamt\shamt_master_path.conf with the correct path."
    Write-Host ""
    exit 1
}

$MasterShamtDir = Join-Path $MasterDir ".shamt"

Write-Host ""
Write-Host "============================================================"
Write-Host "  Shamt Export"
Write-Host "============================================================"
Write-Host "  From: $ChildRoot"
Write-Host "  To:   $MasterDir"
Write-Host "============================================================"
Write-Host ""

# --- Dirty tree check --------------------------------------------------------

$masterStatus = & git -C $MasterDir status --porcelain 2>&1
if ($masterStatus -and ($masterStatus | Where-Object { $_ -ne "" }).Count -gt 0) {
    Write-Host "  Warning: master working tree has uncommitted changes." -ForegroundColor Yellow
    Write-Host "  Exported files will be mixed with existing changes. Proceed with care." -ForegroundColor Yellow
    Write-Host ""
}

# --- Compare and copy changed files ------------------------------------------

$Exported = @()
$Deleted = @()

function Export-Dir {
    param(
        [string]$SourceDir,
        [string]$MasterShamtPath,
        [string]$ChildShamtPath
    )
    if (-not (Test-Path $SourceDir)) { return }

    Get-ChildItem -Path $SourceDir -Recurse -File | Sort-Object FullName | ForEach-Object {
        $srcFile = $_.FullName
        $relPath = $srcFile.Substring($ChildShamtPath.Length).TrimStart('\', '/')
        $relPathFwd = $relPath.Replace('\', '/')

        # Never export audit outputs — child-specific, not relevant to master
        if ($relPathFwd.StartsWith("guides/audit/outputs/")) {
            return
        }

        $dstFile = Join-Path $MasterShamtPath $relPath

        if (-not (Test-Path $dstFile)) {
            # New file in child — copy to master
            if (-not $DryRun) {
                $dstDir = Split-Path $dstFile -Parent
                New-Item -ItemType Directory -Force -Path $dstDir | Out-Null
                Copy-Item $srcFile $dstFile
            }
            $script:Exported += "$relPathFwd (new)"
        } else {
            $srcHash = (Get-FileHash $srcFile -Algorithm MD5).Hash
            $dstHash = (Get-FileHash $dstFile -Algorithm MD5).Hash
            if ($srcHash -ne $dstHash) {
                if (-not $DryRun) {
                    Copy-Item $srcFile $dstFile -Force
                }
                $script:Exported += $relPathFwd
            }
        }
    }
}

function Remove-FromMaster {
    param(
        [string]$MasterDir,
        [string]$MasterShamtPath,
        [string]$ChildShamtPath
    )
    if (-not (Test-Path $MasterDir)) { return }

    Get-ChildItem -Path $MasterDir -Recurse -File | Sort-Object FullName | ForEach-Object {
        $masterFile = $_.FullName
        $relPath = $masterFile.Substring($MasterShamtPath.Length).TrimStart('\', '/')
        $relPathFwd = $relPath.Replace('\', '/')

        # Never touch audit outputs
        if ($relPathFwd.StartsWith("guides/audit/outputs/")) {
            return
        }

        $childFile = Join-Path $ChildShamtPath $relPath
        if (-not (Test-Path $childFile)) {
            if (-not $DryRun) {
                Remove-Item $masterFile -Force
            }
            $script:Deleted += $relPathFwd
        }
    }
}

Export-Dir -SourceDir (Join-Path $ChildShamtDir "guides") -MasterShamtPath $MasterShamtDir -ChildShamtPath $ChildShamtDir
Export-Dir -SourceDir (Join-Path $ChildShamtDir "scripts") -MasterShamtPath $MasterShamtDir -ChildShamtPath $ChildShamtDir
Remove-FromMaster -MasterDir (Join-Path $MasterShamtDir "guides") -MasterShamtPath $MasterShamtDir -ChildShamtPath $ChildShamtDir
Remove-FromMaster -MasterDir (Join-Path $MasterShamtDir "scripts") -MasterShamtPath $MasterShamtDir -ChildShamtPath $ChildShamtDir

# --- Summary -----------------------------------------------------------------

if ($Exported.Count -eq 0 -and $Deleted.Count -eq 0) {
    Write-Host "  No differences found. Child is in sync with master."
    Write-Host ""
    Write-Host "============================================================"
    Write-Host ""
    exit 0
}

if ($Exported.Count -gt 0) {
    if ($DryRun) {
        Write-Host "  Would export $($Exported.Count) file(s) to master:"
    } else {
        Write-Host "  Exported $($Exported.Count) file(s) to master:"
    }
    Write-Host ""
    foreach ($f in $Exported) {
        Write-Host "    + $f"
    }
    Write-Host ""
}

if ($Deleted.Count -gt 0) {
    if ($DryRun) {
        Write-Host "  Would delete $($Deleted.Count) file(s) from master (not present in child):" -ForegroundColor Yellow
    } else {
        Write-Host "  Deleted $($Deleted.Count) file(s) from master (not present in child):"
    }
    Write-Host ""
    foreach ($f in $Deleted) {
        Write-Host "    - $f"
    }
    Write-Host ""
}

if ($DryRun) {
    Write-Host "------------------------------------------------------------"
    Write-Host "  DRY RUN — no changes were made to master." -ForegroundColor Cyan
    Write-Host "  Re-run without -DryRun to apply."
    Write-Host ""
    Write-Host "============================================================"
    Write-Host ""
    exit 0
}

# --- Generate commit message -------------------------------------------------

if ($Exported.Count -le 3 -and $Deleted.Count -eq 0) {
    $names = $Exported | ForEach-Object { [System.IO.Path]::GetFileName($_ -replace ' \(new\)$', '') }
    $commitMsg = "sync: " + ($names -join ', ')
} elseif ($Deleted.Count -gt 0) {
    $commitMsg = "sync: $($Exported.Count) file(s) updated, $($Deleted.Count) deleted"
} else {
    $commitMsg = "sync: $($Exported.Count) guide/script improvements"
}

# --- Next steps --------------------------------------------------------------

$today = Get-Date -Format "yyyyMMdd"
Write-Host "------------------------------------------------------------"
Write-Host "  Next steps"
Write-Host "------------------------------------------------------------"
Write-Host ""
Write-Host "  1. Go to the shamt-ai-dev directory:"
Write-Host "       cd `"$MasterDir`""
Write-Host ""
Write-Host "  2. Create a new branch and commit:"
Write-Host "       git checkout main"
Write-Host "       git checkout -b feat/child-sync-$today"
Write-Host "       git add -A .shamt/guides/ .shamt/scripts/"
Write-Host "       git commit -m `"$commitMsg`""
Write-Host ""
Write-Host "  3. Push and open a PR against main:"
Write-Host "       git push origin feat/child-sync-$today"
Write-Host ""
if (Get-Command gh -ErrorAction SilentlyContinue) {
    Write-Host "  gh is available — open the PR directly:"
    Write-Host "       gh pr create --title `"$commitMsg`" --body `"<paste .shamt\CHANGES.md entries>`""
    Write-Host ""
}
Write-Host "  Tip: Include content from .shamt\CHANGES.md in the PR description"
Write-Host "  to give reviewers context on what changed and why."
Write-Host ""
Write-Host "============================================================"
Write-Host ""
