"""
fix_applier.py
--------------
Applies a FIXABLE patch from the report back to the source file on disk.

The `before` and `after` strings come from the report renderer (already
stripped of 4-space display padding).  The line number is used to locate
the exact position in the file so the correct indentation can be restored.
"""


def apply_fix(filepath: str, lineno: int, before: str, after: str) -> tuple[bool, str]:
    """Patch a single FIXABLE issue in a source file.

    Returns (success: bool, message: str).
    """
    try:
        with open(filepath, "r", encoding="utf-8") as fh:
            lines = fh.readlines()
    except OSError as e:
        return False, f"Cannot read file: {e}"

    idx = lineno - 1
    if idx >= len(lines):
        return False, f"Line {lineno} is out of range (file has {len(lines)} lines)."

    actual_line = lines[idx].rstrip("\r\n")
    before_lines = before.strip().splitlines()

    # Safety check — verify the first line matches what we expect
    if actual_line.strip() != before_lines[0].strip():
        return False, (
            f"Content mismatch at line {lineno} — file may have changed since the scan.\n"
            f"  Expected : {before_lines[0].strip()[:70]}\n"
            f"  Found    : {actual_line.strip()[:70]}"
        )

    original_indent = len(actual_line) - len(actual_line.lstrip())
    indent_str = " " * original_indent

    after_lines = after.strip().splitlines()
    new_lines = []
    for i, al in enumerate(after_lines):
        al_stripped = al.lstrip()
        al_indent = len(al) - len(al_stripped)

        if i == 0:
            # Always restore the original file indentation on the first line.
            new_lines.append(indent_str + al_stripped + "\n")
        elif al_indent > original_indent:
            # Line already carries more indentation than the anchor line
            # (absolute — produced by lint_fix_server using the real indent).
            new_lines.append(al + "\n")
        else:
            # Relative indentation — add the original indent on top.
            new_lines.append(indent_str + al + "\n")

    before_line_count = len(before_lines)
    lines[idx : idx + before_line_count] = new_lines

    try:
        with open(filepath, "w", encoding="utf-8") as fh:
            fh.writelines(lines)
    except OSError as e:
        return False, f"Cannot write file: {e}"

    return True, f"Fix applied at line {lineno} in {filepath}"
