#!/usr/bin/env python3
"""
Validation script to check all file references in CLAUDE.md and guides.

Checks:
1. File references in CLAUDE.md point to existing files
2. Cross-references between guides are valid
3. Template references exist
4. Prompt references exist
"""

import re
import os
from pathlib import Path
from typing import List, Tuple

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
GUIDES_ROOT = PROJECT_ROOT / "feature-updates" / "guides_v2"
CLAUDE_MD = PROJECT_ROOT / "CLAUDE.md"

def extract_file_references(content: str, source_file: str) -> List[Tuple[str, int, str]]:
    """Extract all file references from markdown content.

    Returns list of (referenced_file, line_number, context)
    """
    references = []

    # Pattern 1: `path/to/file.md`
    pattern1 = r'`([a-zA-Z0-9_/\-\.]+\.md)`'

    # Pattern 2: [Link](path/to/file.md)
    pattern2 = r'\[([^\]]+)\]\(([a-zA-Z0-9_/\-\.]+\.md)\)'

    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        # Find all pattern1 matches
        for match in re.finditer(pattern1, line):
            ref_file = match.group(1)
            references.append((ref_file, i, line.strip()))

        # Find all pattern2 matches
        for match in re.finditer(pattern2, line):
            ref_file = match.group(2)
            references.append((ref_file, i, line.strip()))

    return references

def validate_reference(ref_file: str, source_file: Path) -> Tuple[bool, str]:
    """Validate that a referenced file exists.

    Returns (exists, resolved_path)
    """
    # Try relative to guides_v2/
    guides_path = GUIDES_ROOT / ref_file
    if guides_path.exists():
        return True, str(guides_path)

    # Try relative to source file directory
    source_dir = source_file.parent
    relative_path = source_dir / ref_file
    if relative_path.exists():
        return True, str(relative_path)

    # Try relative to project root
    root_path = PROJECT_ROOT / ref_file
    if root_path.exists():
        return True, str(root_path)

    return False, ""

def main():
    """Main validation logic."""
    print("="*70)
    print("File Reference Validation")
    print("="*70)
    print()

    errors = []
    warnings = []
    checked = 0

    # Files to check
    files_to_check = [
        (CLAUDE_MD, "CLAUDE.md"),
        (GUIDES_ROOT / "README.md", "guides_v2/README.md"),
        (GUIDES_ROOT / "prompts_reference_v2.md", "guides_v2/prompts_reference_v2.md"),
    ]

    # Add all guide files
    for guide_file in GUIDES_ROOT.rglob("*.md"):
        if guide_file.name not in ["README.md", "prompts_reference_v2.md"]:
            rel_path = guide_file.relative_to(PROJECT_ROOT)
            files_to_check.append((guide_file, str(rel_path)))

    for file_path, display_name in files_to_check:
        if not file_path.exists():
            warnings.append(f"Source file not found: {display_name}")
            continue

        print(f"Checking {display_name}...")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        references = extract_file_references(content, display_name)

        for ref_file, line_num, context in references:
            checked += 1
            exists, resolved = validate_reference(ref_file, file_path)

            if not exists:
                errors.append({
                    'file': display_name,
                    'line': line_num,
                    'reference': ref_file,
                    'context': context[:80]
                })

    # Print results
    print()
    print("="*70)
    print("Results")
    print("="*70)
    print(f"Total references checked: {checked}")
    print(f"Errors found: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    print()

    if warnings:
        print("WARNINGS:")
        for warning in warnings:
            print(f"  [!] {warning}")
        print()

    if errors:
        print("ERRORS (Broken References):")
        for error in errors:
            print(f"  [X] {error['file']}:{error['line']}")
            print(f"      Referenced: {error['reference']}")
            print(f"      Context: {error['context']}")
            print()
        return 1
    else:
        print("[OK] All file references are valid!")
        return 0

if __name__ == "__main__":
    exit(main())
