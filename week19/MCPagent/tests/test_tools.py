"""
test_tools.py
-------------
Direct tests for lint_fix_server.py (triage_diff and triage_and_fix_file).
Does NOT start any MCP subprocess — patches FastMCP so the real Python
functions are loaded and called directly.

Run with:
    python test_tools.py
    # or, if pytest is installed:
    pytest test_tools.py -v
"""

import os
import sys
import tempfile
import textwrap

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mcp_servers"))

# Patch FastMCP before importing so @mcp.tool() is a no-op pass-through.
import mcp.server.fastmcp as _fmcp

class _NoOpMCP:
    def __init__(self, *a, **kw): pass
    def tool(self): return lambda fn: fn
    def run(self, **kw): pass

_fmcp.FastMCP = _NoOpMCP

import lint_fix_server as lf


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _tmp_py(source: str) -> str:
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".py",
                                    delete=False, encoding="utf-8")
    f.write(textwrap.dedent(source))
    f.close()
    return f.name


SMELLY_DIFF = """\
diff --git a/sample.py b/sample.py
index 0000000..1111111 100644
--- a/sample.py
+++ b/sample.py
@@ -1,3 +1,10 @@
 def greet(name):
+    print("debug:", name)
+    # TODO: validate input
+    api_key = "sk-hardcoded-secret"
+    try:
+        return name.upper()
+    except:
+        pass
+    x = "this_is_intentionally_very_long_to_exceed_one_hundred_characters_in_total_length_padding = True"
     return name
"""

CLEAN_DIFF = """\
diff --git a/clean.py b/clean.py
index 0000000..1111111 100644
--- a/clean.py
+++ b/clean.py
@@ -1,2 +1,3 @@
 def add(a, b):
+    result = a + b
     return result
"""


# ---------------------------------------------------------------------------
# triage_diff — smell detection
# ---------------------------------------------------------------------------

def test_triage_diff_detects_debug_print():
    out = lf.triage_diff(SMELLY_DIFF)
    assert "debug_print" in out


def test_triage_diff_detects_todo():
    out = lf.triage_diff(SMELLY_DIFF)
    assert "leftover_todo" in out


def test_triage_diff_detects_hardcoded_secret():
    out = lf.triage_diff(SMELLY_DIFF)
    assert "hardcoded_secret" in out


def test_triage_diff_detects_bare_except():
    out = lf.triage_diff(SMELLY_DIFF)
    assert "bare_except" in out


def test_triage_diff_detects_long_line():
    out = lf.triage_diff(SMELLY_DIFF)
    assert "long_line" in out


def test_triage_diff_clean_produces_no_issues():
    out = lf.triage_diff(CLEAN_DIFF)
    assert "No issues" in out


def test_triage_diff_empty_input():
    out = lf.triage_diff("")
    assert "No diff provided" in out


def test_triage_diff_shows_fix_for_bare_except():
    out = lf.triage_diff(SMELLY_DIFF)
    assert "except Exception as e:" in out


def test_triage_diff_shows_fix_for_secret():
    out = lf.triage_diff(SMELLY_DIFF)
    assert "os.environ" in out


def test_triage_diff_shows_added_line_count():
    out = lf.triage_diff(SMELLY_DIFF)
    assert "added lines" in out


# ---------------------------------------------------------------------------
# triage_and_fix_file — FIXABLE issues
# ---------------------------------------------------------------------------

def test_fix_mutable_default_list():
    path = _tmp_py("def fn(items=[]):\n    return items\n")
    try:
        out = lf.triage_and_fix_file(path)
        assert "mutable_default" in out
        assert "FIXABLE" in out
        assert "items=None" in out
        assert "if items is None" in out
    finally:
        os.unlink(path)


def test_fix_mutable_default_dict():
    path = _tmp_py("def fn(cfg={}):\n    return cfg\n")
    try:
        out = lf.triage_and_fix_file(path)
        assert "mutable_default" in out
        assert "cfg=None" in out
    finally:
        os.unlink(path)


def test_fix_bare_except():
    path = _tmp_py("""
        def fn():
            try:
                pass
            except:
                pass
    """)
    try:
        out = lf.triage_and_fix_file(path)
        assert "bare_except" in out
        assert "FIXABLE" in out
        assert "except Exception as e:" in out
    finally:
        os.unlink(path)


def test_fix_empty_except():
    path = _tmp_py("""
        def fn():
            try:
                pass
            except Exception:
                pass
    """)
    try:
        out = lf.triage_and_fix_file(path)
        assert "empty_except" in out
        assert "FIXABLE" in out
        assert "raise" in out
    finally:
        os.unlink(path)


def test_fix_builtin_shadow_param():
    path = _tmp_py("def fn(list, type):\n    return list\n")
    try:
        out = lf.triage_and_fix_file(path)
        assert "builtin_shadow_param" in out
        assert "FIXABLE" in out
        assert "lst" in out or "kind" in out
    finally:
        os.unlink(path)


def test_fix_builtin_shadow_variable():
    path = _tmp_py("def fn(x):\n    list = [x]\n    return list\n")
    try:
        out = lf.triage_and_fix_file(path)
        assert "builtin_shadow_var" in out
        assert "FIXABLE" in out
    finally:
        os.unlink(path)


def test_no_false_positive_on_real_one_liner():
    path = _tmp_py(
        'def add(a: int, b: int) -> int:\n'
        '    """Add two numbers."""\n'
        '    return a + b\n'
    )
    try:
        out = lf.triage_and_fix_file(path)
        assert "[FIXABLE]" not in out
        assert "[REFACTOR]" not in out
        assert "[WARNING]" not in out
    finally:
        os.unlink(path)


# ---------------------------------------------------------------------------
# triage_and_fix_file — REFACTOR issues
# ---------------------------------------------------------------------------

def test_refactor_long_function():
    body = "\n".join(f"    x{i} = {i}" for i in range(50))
    path = _tmp_py(f"def long_fn():\n{body}\n    return x0\n")
    try:
        out = lf.triage_and_fix_file(path)
        assert "long_function" in out
        assert "REFACTOR" in out
        assert "HINT" in out
    finally:
        os.unlink(path)


def test_refactor_too_many_params():
    path = _tmp_py("def crowded(a, b, c, d, e, f):\n    return a\n")
    try:
        out = lf.triage_and_fix_file(path)
        assert "too_many_params" in out
        assert "REFACTOR" in out
    finally:
        os.unlink(path)


def test_refactor_deep_nesting():
    path = _tmp_py("""
        def nested(x):
            if x:
                for i in x:
                    if i:
                        while i > 0:
                            if i % 2:
                                pass
                            i -= 1
    """)
    try:
        out = lf.triage_and_fix_file(path)
        assert "deep_nesting" in out
        assert "REFACTOR" in out
    finally:
        os.unlink(path)


# ---------------------------------------------------------------------------
# triage_and_fix_file — new checks (missing_type_hints, no_docstring,
#                                    dead_import, hardcoded_path)
# ---------------------------------------------------------------------------

def test_missing_type_hints():
    path = _tmp_py("def greet(name):\n    return name\n")
    try:
        out = lf.triage_and_fix_file(path)
        assert "missing_type_hints" in out
        assert "WARNING" in out
        assert "name" in out
    finally:
        os.unlink(path)


def test_no_type_hint_warning_on_annotated():
    path = _tmp_py(
        'def greet(name: str) -> str:\n'
        '    """Say hello."""\n'
        '    return name\n'
    )
    try:
        out = lf.triage_and_fix_file(path)
        assert "missing_type_hints" not in out
    finally:
        os.unlink(path)


def test_no_docstring():
    path = _tmp_py("def greet(name: str) -> str:\n    return name\n")
    try:
        out = lf.triage_and_fix_file(path)
        assert "no_docstring" in out
        assert "WARNING" in out
    finally:
        os.unlink(path)


def test_no_docstring_skips_private():
    path = _tmp_py("def _helper(x: int) -> int:\n    return x\n")
    try:
        out = lf.triage_and_fix_file(path)
        assert "no_docstring" not in out
    finally:
        os.unlink(path)


def test_dead_import():
    path = _tmp_py("import os\nimport sys\n\ndef fn() -> None:\n    pass\n")
    try:
        out = lf.triage_and_fix_file(path)
        assert "dead_import" in out
        assert "WARNING" in out
    finally:
        os.unlink(path)


def test_no_false_positive_used_import():
    path = _tmp_py(
        'import os\n\n'
        'def fn() -> str:\n'
        '    """Get cwd."""\n'
        '    return os.getcwd()\n'
    )
    try:
        out = lf.triage_and_fix_file(path)
        assert "dead_import" not in out
    finally:
        os.unlink(path)


def test_hardcoded_path_windows():
    path = _tmp_py(
        'def fn() -> str:\n'
        '    """Return path."""\n'
        '    return "C:/Users/admin/data"\n'
    )
    try:
        out = lf.triage_and_fix_file(path)
        assert "hardcoded_path" in out
        assert "WARNING" in out
    finally:
        os.unlink(path)


# ---------------------------------------------------------------------------
# triage_and_fix_file — WARNING issues
# ---------------------------------------------------------------------------

def test_warning_stub_function():
    path = _tmp_py("def not_yet():\n    pass\n")
    try:
        out = lf.triage_and_fix_file(path)
        assert "stub_function" in out
        assert "WARNING" in out
    finally:
        os.unlink(path)


def test_no_stub_false_positive_on_callable_body():
    path = _tmp_py("def real(x):\n    return x + 1\n")
    try:
        out = lf.triage_and_fix_file(path)
        assert "stub_function" not in out
    finally:
        os.unlink(path)


# ---------------------------------------------------------------------------
# triage_and_fix_file — edge cases
# ---------------------------------------------------------------------------

def test_missing_file():
    out = lf.triage_and_fix_file("does_not_exist.py")
    assert "not found" in out.lower()


def test_syntax_error_file():
    path = _tmp_py("def broken(:\n    pass\n")
    try:
        out = lf.triage_and_fix_file(path)
        assert "Syntax error" in out or "syntax" in out.lower()
    finally:
        os.unlink(path)


def test_file_with_no_functions():
    path = _tmp_py("X = 42\nY = 'hello'\n")
    try:
        out = lf.triage_and_fix_file(path)
        assert "No functions" in out
    finally:
        os.unlink(path)


def test_clean_file_shows_no_issues():
    path = _tmp_py(
        'def add(a: int, b: int) -> int:\n'
        '    """Add two numbers."""\n'
        '    return a + b\n\n'
        'def multiply(a: int, b: int) -> int:\n'
        '    """Multiply two numbers."""\n'
        '    return a * b\n'
    )
    try:
        out = lf.triage_and_fix_file(path)
        assert "[FIXABLE]" not in out
        assert "[REFACTOR]" not in out
        assert "[WARNING]" not in out
    finally:
        os.unlink(path)


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import traceback

    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = failed = 0

    for fn in tests:
        try:
            fn()
            print(f"  PASS  {fn.__name__}")
            passed += 1
        except Exception:
            print(f"  FAIL  {fn.__name__}")
            traceback.print_exc()
            failed += 1

    print(f"\n{passed + failed} tests — {passed} passed, {failed} failed")
    sys.exit(1 if failed else 0)
