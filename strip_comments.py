#!/usr/bin/env python3
"""
Tokenize-based comment removal script.

Uses Python's tokenize module to safely identify and remove comments
from Python source files while preserving shebangs, noqa directives,
and type:ignore directives.
"""

import argparse
import sys
import tokenize
from io import BytesIO
from pathlib import Path


def should_preserve_comment(line_num: int, comment_text: str) -> bool:
    """
    Determine if a comment should be preserved.

    Args:
        line_num: Line number (1-indexed)
        comment_text: The comment token text (including #)

    Returns:
        True if comment should be preserved, False if it should be removed
    """
    if line_num == 1 and comment_text.startswith("#!"):
        return True

    if "noqa" in comment_text:
        return True

    if "type:ignore" in comment_text or "type: ignore" in comment_text:
        return True

    return False


def process_file(file_path: Path) -> tuple[int, int]:
    """
    Remove comments from a single Python file.

    Args:
        file_path: Path to the Python file to process

    Returns:
        Tuple of (files_processed, lines_removed)
    """
    try:
        with open(file_path, "rb") as f:
            original_content = f.read()

        normalized_content = original_content.replace(b'\r\n', b'\n').replace(b'\r', b'\n')

        try:
            tokens = list(
                tokenize.tokenize(BytesIO(normalized_content).readline)
            )
        except tokenize.TokenError:
            print(f"WARNING: Skipping {file_path} (tokenize error)", file=sys.stderr)
            return 0, 0

        content_str = normalized_content.decode("utf-8")
        lines = content_str.split("\n")

        pure_comment_lines = set()
        trailing_comment_ranges = {}

        for token in tokens:
            if token.type == tokenize.COMMENT:
                line_num = token.start[0]

                start_col = token.start[1]
                end_col = token.end[1]

                if should_preserve_comment(line_num, token.string):
                    continue

                line_content = lines[line_num - 1]
                before_comment = line_content[:start_col].strip()

                if not before_comment:
                    pure_comment_lines.add(line_num)
                else:
                    trailing_comment_ranges[line_num] = (start_col, end_col)

        new_lines = []
        lines_removed = 0

        for line_num, line_content in enumerate(lines, 1):
            if line_num in pure_comment_lines:
                lines_removed += 1
                continue

            if line_num in trailing_comment_ranges:
                start_col, end_col = trailing_comment_ranges[line_num]
                new_line = line_content[:start_col].rstrip()
                new_lines.append(new_line)
                lines_removed += 1
            else:
                new_lines.append(line_content)

        new_content = "\n".join(new_lines)

        has_crlf = b'\r\n' in original_content
        if has_crlf:
            new_content = new_content.replace("\n", "\r\n")

        with open(file_path, "wb") as f:
            f.write(new_content.encode("utf-8"))

        return 1, lines_removed

    except (PermissionError, OSError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


def process_directory(dir_path: Path) -> tuple[int, int]:
    """
    Recursively process all Python files in a directory.

    Args:
        dir_path: Path to the directory to process

    Returns:
        Tuple of (files_processed, lines_removed)
    """
    total_files = 0
    total_lines = 0

    for py_file in dir_path.rglob("*.py"):
        files, lines = process_file(py_file)
        total_files += files
        total_lines += lines

    return total_files, total_lines


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Remove comments from Python source files using tokenize module"
    )
    parser.add_argument(
        "path",
        type=Path,
        help="Path to file or directory to process",
    )

    args = parser.parse_args()
    path = args.path

    if not path.exists():
        print(f"ERROR: Path does not exist: {path}", file=sys.stderr)
        sys.exit(1)

    if path.is_file():
        files_processed, lines_removed = process_file(path)
    elif path.is_dir():
        files_processed, lines_removed = process_directory(path)
    else:
        print(f"ERROR: Path is neither file nor directory: {path}", file=sys.stderr)
        sys.exit(1)

    print(f"Processed {files_processed} file(s), removed {lines_removed} comment line(s)")
    sys.exit(0)


if __name__ == "__main__":
    main()
