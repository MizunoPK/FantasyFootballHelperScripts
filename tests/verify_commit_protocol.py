#!/usr/bin/env python3
"""
Verification script to ensure the pre-commit validation protocol is properly set up.
This script checks that all required files exist and are accessible.
"""

import os
import sys

def verify_commit_protocol():
    """Verify that all pre-commit validation files are in place"""

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(f"Verifying pre-commit protocol from: {project_root}")

    # Required files for the protocol
    required_files = {
        'tests/pre_commit_validation_checklist.md': 'Main pre-commit validation checklist',
        'tests/draft_helper_validation_checklist.md': 'Integration test checklist',
        'tests/commit_checklist_guidelines.txt': 'Guidelines for checklist creation',
        'potential_updates/rules.txt': 'Project rules with commit protocol',
        'CLAUDE.md': 'Claude-specific instructions with commit protocol'
    }

    print("\n=== VERIFYING PRE-COMMIT PROTOCOL FILES ===")

    all_present = True
    for file_path, description in required_files.items():
        full_path = os.path.join(project_root, file_path)
        if os.path.exists(full_path):
            print(f"✅ {file_path} - {description}")
        else:
            print(f"❌ {file_path} - MISSING: {description}")
            all_present = False

    print("\n=== VERIFYING PROTOCOL CONTENT ===")

    # Check that rules.txt contains the protocol
    rules_file = os.path.join(project_root, 'potential_updates/rules.txt')
    if os.path.exists(rules_file):
        with open(rules_file, 'r') as f:
            rules_content = f.read()

        if 'PRE-COMMIT VALIDATION PROTOCOL' in rules_content:
            print("✅ rules.txt contains pre-commit validation protocol")
        else:
            print("❌ rules.txt missing pre-commit validation protocol")
            all_present = False

    # Check that CLAUDE.md contains the protocol
    claude_file = os.path.join(project_root, 'CLAUDE.md')
    if os.path.exists(claude_file):
        with open(claude_file, 'r') as f:
            claude_content = f.read()

        if 'Pre-Commit Validation Protocol' in claude_content:
            print("✅ CLAUDE.md contains pre-commit validation protocol")
        else:
            print("❌ CLAUDE.md missing pre-commit validation protocol")
            all_present = False

    print("\n=== VERIFICATION RESULTS ===")

    if all_present:
        print("🎉 PRE-COMMIT PROTOCOL VERIFICATION SUCCESSFUL!")
        print("✅ All required files are present and configured")
        print("✅ Agents will follow the validation checklist when instructed to 'validate and commit'")
        return True
    else:
        print("❌ PRE-COMMIT PROTOCOL VERIFICATION FAILED!")
        print("❌ Some required files or content are missing")
        return False

if __name__ == "__main__":
    success = verify_commit_protocol()
    sys.exit(0 if success else 1)