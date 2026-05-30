"""
lint_fix_server.py
------------------
Single MCP server that TRIAGES code issues and PROPOSES concrete patches.
Replaces both review_server.py (diff linting) and logic_server.py (AST analysis).

Tools:
  1. triage_diff(diff)          — lint added lines in a git diff and suggest
                                  a fix for each smell found.
  2. triage_and_fix_file(path)  — full AST analysis of a Python file with
                                  a BEFORE/AFTER patch for every auto-fixable
                                  smell and a refactor hint for structural issues.

Severity levels used in triage_and_fix_file:
  FIXABLE  — a concrete code replacement is provided
  REFACTOR — requires manual restructuring; a plain-language hint is given
  WARNING  — flag for human review; no safe auto-fix exists

Run standalone to test:
    python lint_fix_server.py
"""

import ast
import os
import re

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("lint_fix")

# --- Thresholds ---
MAX_FUNCTION_LINES = 40
MAX_PARAMS = 5
MAX_NESTING_DEPTH = 4
MAX_COMPLEXITY = 10

BUILTIN_NAMES = {
    "len", "list", "dict", "set", "tuple", "type", "id", "str", "int",
    "float", "bool", "print", "input", "open", "range", "enumerate",
    "zip", "map", "filter", "sum", "min", "max", "abs", "round",
    "sorted", "reversed", "hasattr", "getattr", "setattr", "isinstance",
    "issubclass", "iter", "next", "hash", "repr", "format",
}

_RENAME_MAP = {
    "list": "lst", "dict": "dct", "set": "items", "tuple": "tpl",
    "type": "kind", "str": "text", "int": "number", "float": "value",
    "bool": "flag", "id": "identifier", "input": "user_input",
    "open": "file_obj", "map": "mapping", "filter": "predicate",
    "sum": "total", "min": "minimum", "max": "maximum",
    "abs": "magnitude", "round": "rounded", "sorted": "sorted_list",
    "reversed": "reversed_list", "len": "length", "print": "output",
    "range": "indices", "enumerate": "enumerated", "zip": "zipped",
    "hash": "hash_val", "repr": "representation", "format": "formatted",
    "hasattr": "has_attr", "getattr": "get_attr", "setattr": "set_attr",
    "isinstance": "is_instance", "issubclass": "is_subclass",
    "iter": "iterator", "next": "next_item",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _read_source(filepath: str):
    if not os.path.isfile(filepath):
        return "", f"File not found: {filepath}"
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            return f.read(), None
    except OSError as e:
        return "", str(e)


def _src_line(lines: list, lineno: int) -> str:
    if 1 <= lineno <= len(lines):
        return lines[lineno - 1].rstrip()
    return ""


def _indent_of(line: str) -> int:
    return len(line) - len(line.lstrip())


def _suggest_rename(name: str) -> str:
    return _RENAME_MAP.get(name, f"{name}_")


def _cyclomatic_complexity(node) -> int:
    branch_types = (ast.If, ast.For, ast.While, ast.ExceptHandler,
                    ast.With, ast.Assert, ast.comprehension)
    count = 1
    for child in ast.walk(node):
        if isinstance(child, branch_types):
            count += 1
        elif isinstance(child, ast.BoolOp):
            count += len(child.values) - 1
    return count


def _max_nesting_depth(node) -> int:
    nesting_types = (ast.If, ast.For, ast.While, ast.With, ast.Try, ast.ExceptHandler)

    def _depth(n, current=0):
        if isinstance(n, nesting_types):
            current += 1
        best = current
        for child in ast.iter_child_nodes(n):
            best = max(best, _depth(child, current))
        return best

    return _depth(node)


def _param_count(fn) -> int:
    return len(fn.args.args) + len(fn.args.posonlyargs) + len(fn.args.kwonlyargs)


def _all_arg_nodes(fn) -> list:
    result = fn.args.args + fn.args.posonlyargs + fn.args.kwonlyargs
    if fn.args.vararg:
        result.append(fn.args.vararg)
    if fn.args.kwarg:
        result.append(fn.args.kwarg)
    return result


def _collect_functions(tree) -> list:
    return [n for n in ast.walk(tree)
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]


def _is_stub(fn) -> bool:
    real = [n for n in fn.body
            if not isinstance(n, ast.Pass) and
            not (isinstance(n, ast.Expr) and
                 isinstance(n.value, ast.Constant) and
                 isinstance(n.value.value, str))]
    return len(real) == 0


def _has_docstring(fn) -> bool:
    return (fn.body and
            isinstance(fn.body[0], ast.Expr) and
            isinstance(fn.body[0].value, ast.Constant) and
            isinstance(fn.body[0].value.value, str))


def _unannotated_params(fn) -> list[str]:
    missing = []
    for arg in fn.args.args + fn.args.posonlyargs + fn.args.kwonlyargs:
        if arg.annotation is None and arg.arg not in ("self", "cls"):
            missing.append(arg.arg)
    return missing


def _unused_imports(tree) -> list[tuple[int, str]]:
    imported: dict[str, int] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.asname if alias.asname else alias.name.split(".")[0]
                imported[name] = node.lineno
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name == "*":
                    continue
                name = alias.asname if alias.asname else alias.name
                imported[name] = node.lineno
    used: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            used.add(node.id)
    return [(lineno, name) for name, lineno in imported.items() if name not in used]


_PATH_RE = re.compile(
    r'[A-Za-z]:[/\\][^\s"\']{3,}'           # Windows: C:\path or C:/path
    r'|/(?:home|usr|var|etc|tmp|opt|app'
    r'|data|Users|root)/[^\s"\']{2,}'        # common Unix roots
)


def _hardcoded_paths(tree) -> list[tuple[int, str]]:
    results = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if _PATH_RE.search(node.value):
                results.append((node.lineno, node.value))
    return results


# ---------------------------------------------------------------------------
# Diff triage helpers
# ---------------------------------------------------------------------------

def _added_lines(diff_text: str):
    filename = "unknown"
    new_line_no = 0
    for raw in diff_text.splitlines():
        if raw.startswith("+++ b/"):
            filename = raw[6:].strip()
        elif raw.startswith("@@"):
            m = re.search(r"\+(\d+)", raw)
            new_line_no = int(m.group(1)) if m else 0
        elif raw.startswith("+") and not raw.startswith("+++"):
            yield filename, new_line_no, raw[1:]
            new_line_no += 1
        elif not raw.startswith("-"):
            new_line_no += 1


def _secret_fix(line: str) -> str:
    m = re.search(r"(\w+)\s*=\s*[\"'][^\"']+[\"']", line)
    if m:
        var = m.group(1)
        return line[:m.start()] + f'{var} = os.environ.get("{var.upper()}")'
    return line.strip() + "  # move to env var"


DIFF_CHECKS = [
    ("debug_print",
     lambda l: bool(re.search(r"\bprint\s*\(", l)),
     lambda l: "Remove or replace with: logging.debug(...)"),
    ("leftover_todo",
     lambda l: bool(re.search(r"#\s*(todo|fixme|hack|xxx)\b", l, re.I)),
     lambda _: "Resolve or delete this comment before merging."),
    ("hardcoded_secret",
     lambda l: bool(re.search(r"(api_key|secret|password|token)\s*=\s*[\"'][^\"']+[\"']", l, re.I)),
     _secret_fix),
    ("bare_except",
     lambda l: bool(re.search(r"except\s*:", l)),
     lambda l: l.replace("except:", "except Exception as e:").strip()),
    ("long_line",
     lambda l: len(l) > 100,
     lambda _: "Break into multiple lines (max 100 chars)."),
    ("breakpoint_left",
     lambda l: "breakpoint()" in l,
     lambda _: "Remove breakpoint() before committing."),
    ("commented_code",
     lambda l: bool(re.match(r"\s*#\s*(import |def |class |return |for |if )", l)),
     lambda _: "Delete commented-out code; use git to recover it if needed."),
]


# ---------------------------------------------------------------------------
# MCP tools
# ---------------------------------------------------------------------------

@mcp.tool()
def triage_diff(diff: str) -> str:
    """Lint added lines in a git diff and return a fix for each smell found.

    Args:
        diff: Raw output of `git diff` (unified diff format).
    """
    if not diff.strip():
        return "No diff provided — nothing to triage."

    findings = []
    added_count = 0
    for filename, line_no, code in _added_lines(diff):
        added_count += 1
        for category, test, fix_fn in DIFF_CHECKS:
            try:
                if test(code):
                    findings.append((filename, line_no, category, code.strip(), fix_fn(code)))
            except Exception:
                continue

    out = [f"=== DIFF TRIAGE: {added_count} added lines — {len(findings)} issues ===", ""]

    if not findings:
        out.append("No issues found in added lines.")
    else:
        for filename, line_no, category, code, fix in findings[:30]:
            snippet = code[:80] + ("…" if len(code) > 80 else "")
            out.append(f"[{category}]  {filename}:~{line_no}")
            out.append(f"  CODE:  {snippet}")
            out.append(f"  FIX:   {fix}")
            out.append("")
        if len(findings) > 30:
            out.append(f"  …and {len(findings) - 30} more issues not shown.")

    return "\n".join(out)


@mcp.tool()
def triage_and_fix_file(filepath: str) -> str:
    """AST analysis of a Python file. Returns BEFORE/AFTER patches for
    auto-fixable smells (mutable defaults, bare/empty excepts, builtin shadowing)
    and refactor hints for structural issues (long functions, deep nesting,
    high complexity). filepath must be an absolute path.

    Args:
        filepath: Absolute path to a Python (.py) source file.
    """
    source, err = _read_source(filepath)
    if err:
        return err

    try:
        tree = ast.parse(source, filename=filepath)
    except SyntaxError as e:
        return f"Syntax error in {filepath}: {e}"

    funcs  = _collect_functions(tree)
    lines  = source.splitlines()
    findings = []

    def add(severity, lineno, fn_name, category, desc, before=None, after=None, hint=None):
        findings.append(dict(severity=severity, lineno=lineno, fn=fn_name,
                             category=category, desc=desc,
                             before=before, after=after, hint=hint))

    # ── Module-level: unused imports ──────────────────────────────────────────
    for lineno, name in _unused_imports(tree):
        orig = _src_line(lines, lineno)
        add("WARNING", lineno, "(module)", "dead_import",
            f"'{name}' is imported but never referenced in this file.",
            hint=f"Remove this line or add '# noqa' if used indirectly (e.g. re-export).")

    # ── Module-level: hardcoded filesystem paths ──────────────────────────────
    for lineno, value in _hardcoded_paths(tree):
        snippet = value[:60] + ("…" if len(value) > 60 else "")
        add("WARNING", lineno, "(module)", "hardcoded_path",
            f"Hardcoded path: '{snippet}'",
            hint="Move this to .env or a config constant so it works across machines.")

    if not funcs:
        if not findings:
            return f"No functions found in {filepath}."

    for fn in funcs:
        end = getattr(fn, "end_lineno", fn.lineno)
        fn_lines = end - fn.lineno + 1

        # ── FIXABLE: mutable default arguments ───────────────────────────
        for i, default in enumerate(fn.args.defaults):
            if not isinstance(default, (ast.List, ast.Dict, ast.Set)):
                continue
            param_idx = len(fn.args.args) - len(fn.args.defaults) + i
            if param_idx >= len(fn.args.args):
                continue
            param_name = fn.args.args[param_idx].arg
            default_repr = ast.unparse(default)
            sig = _src_line(lines, fn.lineno)
            indent = " " * (_indent_of(sig) + 4)
            add("FIXABLE", fn.lineno, fn.name, "mutable_default",
                f"Parameter '{param_name}' has a mutable default {default_repr}. "
                "Python evaluates defaults once — shared across all calls.",
                before=sig.strip(),
                after=(f"{sig.strip().replace(f'{param_name}={default_repr}', f'{param_name}=None')}\n"
                       f"{indent}if {param_name} is None:\n"
                       f"{indent}    {param_name} = {default_repr}"))

        for node in ast.walk(fn):
            # ── FIXABLE: bare except ──────────────────────────────────────
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                orig = _src_line(lines, node.lineno)
                ind = " " * _indent_of(orig)
                add("FIXABLE", node.lineno, fn.name, "bare_except",
                    "Bare 'except:' catches KeyboardInterrupt and SystemExit.",
                    before=orig.strip(),
                    after=f"{ind}except Exception as e:")

            # ── FIXABLE: empty except block ───────────────────────────────
            elif (isinstance(node, ast.ExceptHandler) and node.body and
                  all(isinstance(s, ast.Pass) for s in node.body)):
                orig = _src_line(lines, node.lineno)
                ind = " " * _indent_of(orig)
                add("FIXABLE", node.lineno, fn.name, "empty_except",
                    "Empty except block silently discards the exception.",
                    before=orig.strip() + "\n    " + "pass",
                    after=orig.strip() + "\n    " + "raise")

        # ── FIXABLE: parameter shadows a builtin ──────────────────────────
        for arg in _all_arg_nodes(fn):
            if arg.arg in BUILTIN_NAMES:
                sig = _src_line(lines, fn.lineno)
                new_name = _suggest_rename(arg.arg)
                add("FIXABLE", fn.lineno, fn.name, "builtin_shadow_param",
                    f"Parameter '{arg.arg}' shadows the Python builtin '{arg.arg}'.",
                    before=sig.strip(),
                    after=sig.replace(f" {arg.arg}", f" {new_name}")
                              .replace(f",{arg.arg}", f",{new_name}")
                              .replace(f"({arg.arg}", f"({new_name}").strip())

        # ── FIXABLE: local variable shadows a builtin ─────────────────────
        for node in ast.walk(fn):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id in BUILTIN_NAMES:
                        orig = _src_line(lines, node.lineno)
                        new_name = _suggest_rename(target.id)
                        add("FIXABLE", node.lineno, fn.name, "builtin_shadow_var",
                            f"Variable '{target.id}' shadows the builtin.",
                            before=orig.strip(),
                            after=re.sub(rf"\b{target.id}\b", new_name, orig).strip())

        # ── REFACTOR: structural issues ───────────────────────────────────
        if fn_lines > MAX_FUNCTION_LINES:
            add("REFACTOR", fn.lineno, fn.name, "long_function",
                f"{fn_lines} lines (limit {MAX_FUNCTION_LINES}).",
                hint=("Split into 2–3 smaller functions, each doing one thing. "
                      "Look for natural seams: validation, transformation, I/O."))

        if _param_count(fn) > MAX_PARAMS:
            p = _param_count(fn)
            add("REFACTOR", fn.lineno, fn.name, "too_many_params",
                f"{p} parameters (limit {MAX_PARAMS}).",
                hint=("Group related parameters into a dataclass or TypedDict. "
                      "E.g. replace (name, age, email, role) with a User dataclass."))

        if _cyclomatic_complexity(fn) > MAX_COMPLEXITY:
            c = _cyclomatic_complexity(fn)
            add("REFACTOR", fn.lineno, fn.name, "high_complexity",
                f"Cyclomatic complexity {c} (limit {MAX_COMPLEXITY}).",
                hint=("Extract each major branch into a named helper. "
                      "Consider a dispatch dict or match statement for long if/elif chains."))

        if _max_nesting_depth(fn) > MAX_NESTING_DEPTH:
            d = _max_nesting_depth(fn)
            add("REFACTOR", fn.lineno, fn.name, "deep_nesting",
                f"Nesting depth {d} (limit {MAX_NESTING_DEPTH}).",
                hint=("Use guard clauses (early return/raise) for error cases at the "
                      "top of the function to flatten the happy path."))

        # ── WARNING: missing type hints (public non-stub functions only) ─────
        is_public = not fn.name.startswith("_")
        if is_public and not _is_stub(fn):
            missing_params = _unannotated_params(fn)
            missing_return = fn.returns is None
            if missing_params or missing_return:
                parts = []
                if missing_params:
                    parts.append(f"params: {', '.join(missing_params)}")
                if missing_return:
                    parts.append("return type")
                add("WARNING", fn.lineno, fn.name, "missing_type_hints",
                    f"Missing annotations — {'; '.join(parts)}.",
                    hint="Add type hints: def fn(x: int, y: str) -> bool:")

        # ── WARNING: no docstring (public non-stub functions only) ───────────
        if is_public and not _is_stub(fn) and not _has_docstring(fn):
            add("WARNING", fn.lineno, fn.name, "no_docstring",
                "Public function has no docstring.",
                hint='Add a one-line summary: """Brief description."""')

        # ── WARNING: unimplemented stubs ──────────────────────────────────
        if _is_stub(fn):
            add("WARNING", fn.lineno, fn.name, "stub_function",
                "Function body is empty or stub-only (pass/docstring).",
                hint="Implement or remove this function.")

    # ── Format output ─────────────────────────────────────────────────────
    fixable  = [f for f in findings if f["severity"] == "FIXABLE"]
    refactor = [f for f in findings if f["severity"] == "REFACTOR"]
    warnings = [f for f in findings if f["severity"] == "WARNING"]

    out = [
        f"=== TRIAGE + FIX: {os.path.basename(filepath)} ===",
        f"FILEPATH: {filepath}",
        f"Issues: {len(findings)}  (FIXABLE: {len(fixable)}, "
        f"REFACTOR: {len(refactor)}, WARNING: {len(warnings)})",
        "",
    ]

    for f in findings:
        out.append(f"[{f['severity']}]  {f['category']} — {f['fn']}()  line {f['lineno']}")
        out.append(f"  {f['desc']}")
        if f.get("before"):
            out.append(f"  BEFORE:")
            for bl in f["before"].splitlines():
                out.append(f"    {bl}")
        if f.get("after"):
            out.append(f"  AFTER:")
            for al in f["after"].splitlines():
                out.append(f"    {al}")
        if f.get("hint"):
            out.append(f"  HINT:  {f['hint']}")
        out.append("")

    out.append("FIXABLE patches are safe mechanical changes. "
               "REFACTOR hints require judgment — review context before applying.")
    return "\n".join(out)


if __name__ == "__main__":
    mcp.run(transport="stdio")
