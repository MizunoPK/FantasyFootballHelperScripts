#!/usr/bin/env python3
"""
Intelligent code block tagging for markdown files.
Tags untagged code blocks (```) with appropriate language identifiers.
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple

def detect_language(content: str) -> str:
    """Detect the appropriate language tag for a code block."""
    lines = content.strip().split('\n')
    if not lines:
        return 'text'

    first_line = lines[0].strip()

    # Bash/Shell patterns
    bash_patterns = [
        r'^\$',  # Command prompt
        r'^cd\s',
        r'^ls\s',
        r'^grep\s',
        r'^git\s',
        r'^bash\s',
        r'^echo\s',
        r'^cat\s',
        r'^mkdir\s',
        r'^rm\s',
        r'^mv\s',
        r'^cp\s',
        r'^chmod\s',
        r'^find\s',
        r'^awk\s',
        r'^sed\s',
        r'^for\s',
        r'^while\s',
        r'^if\s\[',
        r'^#!/bin/(ba)?sh',
    ]

    for pattern in bash_patterns:
        if re.search(pattern, first_line):
            return 'bash'

    # Check all lines for strong bash indicators
    bash_keywords = ['#!/bin/bash', '#!/bin/sh', 'set -e', 'set -u', 'function ', 'do\n', 'done\n']
    for keyword in bash_keywords:
        if keyword in content:
            return 'bash'

    # Markdown patterns
    markdown_patterns = [
        r'^#{1,6}\s',  # Headers
        r'^\*\s',  # Unordered list
        r'^-\s',  # Unordered list
        r'^\d+\.\s',  # Ordered list
        r'^\[.*\]\(.*\)',  # Links
        r'^>',  # Blockquote
    ]

    for pattern in markdown_patterns:
        if re.search(pattern, first_line):
            return 'markdown'

    # JSON patterns
    if first_line.startswith('{') or first_line.startswith('['):
        if '"' in content and ':' in content:
            return 'json'

    # YAML patterns
    if re.search(r'^[\w-]+:\s', first_line) and not re.search(r'[{}]', content):
        return 'yaml'

    # Python patterns
    python_patterns = [
        r'^import\s',
        r'^from\s',
        r'^def\s',
        r'^class\s',
        r'^if __name__',
        r'^#!.*python',
    ]

    for pattern in python_patterns:
        if re.search(pattern, first_line):
            return 'python'

    # ASCII art / Box drawing characters
    box_chars = ['┌', '│', '└', '├', '─', '═', '║', '┐', '┘', '┤', '┬', '┴', '┼']
    if any(char in content for char in box_chars):
        return 'text'

    # Tables (markdown or text)
    if re.search(r'^\|.*\|.*\|', first_line):
        return 'text'

    # Check for all-caps variable names (common in text blocks)
    if re.search(r'^[A-Z_]+:', first_line):
        return 'text'

    # Diff patterns
    if re.search(r'^[\+\-]{3}\s', first_line) or re.search(r'^@@.*@@', first_line):
        return 'diff'

    # Default to text for anything else
    return 'text'


def process_file(filepath: Path) -> Tuple[int, int]:
    """
    Process a single markdown file, tagging untagged code blocks.
    Returns (blocks_found, blocks_tagged).
    """
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)
        return 0, 0

    lines = content.split('\n')
    new_lines = []
    in_block = False
    block_content = []
    blocks_found = 0
    blocks_tagged = 0

    for line in lines:
        # Check for code fence
        if line.strip().startswith('```'):
            if not in_block:
                # Opening fence
                fence = line.strip()
                if fence == '```':
                    # Untagged block
                    in_block = True
                    block_content = []
                    blocks_found += 1
                    new_lines.append(line)  # Keep original for now
                else:
                    # Already tagged
                    new_lines.append(line)
            else:
                # Closing fence
                if line.strip() == '```':
                    # This is the closing fence for an untagged block
                    # Detect language and update opening fence
                    language = detect_language('\n'.join(block_content))

                    # Update the opening fence (last occurrence before block_content)
                    # Find it in new_lines
                    for i in range(len(new_lines) - 1, -1, -1):
                        if new_lines[i].strip() == '```':
                            new_lines[i] = new_lines[i].replace('```', f'```{language}')
                            blocks_tagged += 1
                            break

                    new_lines.append(line)
                    in_block = False
                    block_content = []
                else:
                    # This shouldn't happen for untagged blocks
                    new_lines.append(line)
                    in_block = False
        else:
            new_lines.append(line)
            if in_block:
                block_content.append(line)

    # Write back if changes were made
    if blocks_tagged > 0:
        try:
            filepath.write_text('\n'.join(new_lines), encoding='utf-8')
            return blocks_found, blocks_tagged
        except Exception as e:
            print(f"Error writing {filepath}: {e}", file=sys.stderr)
            return blocks_found, 0

    return blocks_found, blocks_tagged


def main():
    """Main entry point."""
    guides_dir = Path(__file__).parent.parent.parent

    total_files = 0
    total_found = 0
    total_tagged = 0

    print("Scanning for untagged code blocks...")
    print()

    # Process all markdown files
    md_files = sorted(guides_dir.rglob('*.md'))

    for filepath in md_files:
        # Skip certain directories
        skip_dirs = ['.git', 'node_modules', '__pycache__']
        if any(skip in filepath.parts for skip in skip_dirs):
            continue

        found, tagged = process_file(filepath)

        if tagged > 0:
            rel_path = filepath.relative_to(guides_dir)
            print(f"✓ {rel_path}: {tagged} blocks tagged")
            total_files += 1
            total_found += found
            total_tagged += tagged

    print()
    print(f"Summary:")
    print(f"  Files modified: {total_files}")
    print(f"  Blocks found: {total_found}")
    print(f"  Blocks tagged: {total_tagged}")

    return 0 if total_tagged == total_found else 1


if __name__ == '__main__':
    sys.exit(main())
