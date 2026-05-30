"""
report_renderer.py
------------------
Parses the raw text report produced by lint_fix_server and renders it
as interactive Streamlit components.

render_report(text, filters) is the public entry point.
filters dict keys:
  severities  : list of "FIXABLE" | "REFACTOR" | "WARNING" to show
  hide_clean  : bool — collapse/hide files with no issues
  sort        : "name" | "issues_desc"
"""

import re
import streamlit as st

from utils.fix_applier import apply_fix

_ICON = {"FIXABLE": "🔧", "REFACTOR": "🔀", "WARNING": "⚠️"}


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

def _parse_issues(body: str) -> list[dict]:
    issues = []
    parts = re.split(r'\n(?=\[(?:FIXABLE|REFACTOR|WARNING)\])', body)
    for part in parts:
        m = re.match(
            r'\[(FIXABLE|REFACTOR|WARNING)\]\s+(\S+)\s+[—–]\s+(\S+)\s+line\s+(\d+)\s*\n(.*)',
            part.strip(), re.DOTALL,
        )
        if not m:
            continue
        severity, category, fn_name, lineno, rest = m.groups()

        desc_lines = rest.strip().splitlines()
        desc = desc_lines[0].strip() if desc_lines else ""

        before_m = re.search(r'BEFORE:\n((?:    .+\n?)*)', rest)
        before = "\n".join(l[4:] for l in before_m.group(1).splitlines()) if before_m else ""

        after_m = re.search(r'AFTER:\n((?:    .+\n?)*)', rest)
        after = "\n".join(l[4:] for l in after_m.group(1).splitlines()) if after_m else ""

        hint_m = re.search(r'HINT:\s+(.+)', rest)
        hint = hint_m.group(1).strip() if hint_m else ""

        issues.append({
            "severity": severity,
            "category": category,
            "fn": fn_name,
            "line": int(lineno),
            "desc": desc,
            "before": before.strip(),
            "after": after.strip(),
            "hint": hint,
        })
    return issues


def _parse_report(text: str) -> dict:
    preamble_end = text.find("=== TRIAGE")
    header = text[:preamble_end].strip() if preamble_end > 0 else ""

    skipped = [
        line for line in text.splitlines()
        if line.startswith("No functions found in") or line.startswith("Syntax error in")
    ]

    files = []
    for m in re.finditer(
        r'=== TRIAGE \+ FIX: (.+?) ===\n(.*?)(?=\n=== TRIAGE|\Z)',
        text, re.DOTALL,
    ):
        name = m.group(1).strip()
        body = m.group(2)

        filepath_m = re.search(r'^FILEPATH: (.+)$', body, re.MULTILINE)
        filepath = filepath_m.group(1).strip() if filepath_m else ""

        count_m = re.search(
            r'Issues: (\d+)\s+\(FIXABLE: (\d+), REFACTOR: (\d+), WARNING: (\d+)\)', body
        )
        counts = {"total": 0, "fixable": 0, "refactor": 0, "warning": 0}
        if count_m:
            counts = {
                "total":    int(count_m.group(1)),
                "fixable":  int(count_m.group(2)),
                "refactor": int(count_m.group(3)),
                "warning":  int(count_m.group(4)),
            }

        files.append({
            "name":     name,
            "filepath": filepath,
            "counts":   counts,
            "issues":   _parse_issues(body),
        })

    return {"header": header, "files": files, "skipped": skipped}


# ---------------------------------------------------------------------------
# Renderer
# ---------------------------------------------------------------------------

def render_report(text: str, filters: dict | None = None, key_prefix: str = "a"):
    if not text.strip():
        st.warning("Report is empty.")
        return

    filters = filters or {}
    data = _parse_report(text)
    files = data["files"]

    # ── Apply filters ────────────────────────────────────────────────────────
    active_sevs = set(filters.get("severities", ["FIXABLE", "REFACTOR", "WARNING"]))

    display_files = []
    for f in files:
        filtered_issues = [i for i in f["issues"] if i["severity"] in active_sevs]
        counts = {
            "total":    len(filtered_issues),
            "fixable":  sum(1 for i in filtered_issues if i["severity"] == "FIXABLE"),
            "refactor": sum(1 for i in filtered_issues if i["severity"] == "REFACTOR"),
            "warning":  sum(1 for i in filtered_issues if i["severity"] == "WARNING"),
        }
        display_files.append({**f, "issues": filtered_issues, "counts": counts})

    if filters.get("hide_clean"):
        display_files = [f for f in display_files if f["counts"]["total"] > 0]

    sort = filters.get("sort", "name")
    if sort == "issues_desc":
        display_files.sort(key=lambda f: f["counts"]["total"], reverse=True)
    else:
        display_files.sort(key=lambda f: f["name"].lower())

    # ── Scan info ────────────────────────────────────────────────────────────
    if data["header"]:
        st.info(data["header"])

    # ── Summary metrics ──────────────────────────────────────────────────────
    total_fixable  = sum(f["counts"]["fixable"]  for f in display_files)
    total_refactor = sum(f["counts"]["refactor"] for f in display_files)
    total_warning  = sum(f["counts"]["warning"]  for f in display_files)
    files_with_issues = sum(1 for f in display_files if f["counts"]["total"] > 0)

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Files shown",   len(display_files))
    c2.metric("With issues",   files_with_issues)
    c3.metric("🔧 Fixable",    total_fixable)
    c4.metric("🔀 Refactor",   total_refactor)
    c5.metric("⚠️ Warning",    total_warning)

    st.divider()

    # ── Per-file sections ────────────────────────────────────────────────────
    for fi, f in enumerate(display_files):
        counts   = f["counts"]
        name     = f["name"]
        filepath = f["filepath"]

        if counts["total"] == 0:
            with st.expander(f"✅  {name}"):
                st.caption("No issues found.")
            continue

        badges = []
        if counts["fixable"]:  badges.append(f"🔧 {counts['fixable']} fixable")
        if counts["refactor"]: badges.append(f"🔀 {counts['refactor']} refactor")
        if counts["warning"]:  badges.append(f"⚠️ {counts['warning']} warning")

        with st.expander(f"❗  {name}   —   {'  ·  '.join(badges)}", expanded=True):
            for ii, issue in enumerate(f["issues"]):
                sev  = issue["severity"]
                icon = _ICON.get(sev, "")

                st.markdown(
                    f"**{icon} {sev}** &nbsp;·&nbsp; "
                    f"`{issue['category']}` &nbsp;·&nbsp; "
                    f"`{issue['fn']}` &nbsp;·&nbsp; line {issue['line']}"
                )
                st.caption(issue["desc"])

                if issue["before"] and issue["after"]:
                    col_before, col_after, col_btn = st.columns([5, 5, 2])
                    with col_before:
                        st.markdown("**Before**")
                        st.code(issue["before"], language="python")
                    with col_after:
                        st.markdown("**After**")
                        st.code(issue["after"], language="python")
                    with col_btn:
                        st.markdown("&nbsp;")
                        btn_key = f"{key_prefix}_fix_{fi}_{ii}"
                        if filepath and st.button("Apply fix", key=btn_key, type="primary"):
                            ok, msg = apply_fix(
                                filepath,
                                issue["line"],
                                issue["before"],
                                issue["after"],
                            )
                            if ok:
                                st.success(msg)
                                st.caption("Re-run the agent to refresh the report.")
                            else:
                                st.error(msg)
                        elif not filepath:
                            st.caption("(path unknown)")

                if issue["hint"]:
                    st.info(f"**Hint:** {issue['hint']}")

                st.divider()

    # ── Skipped files ────────────────────────────────────────────────────────
    if data["skipped"]:
        with st.expander(f"⏭️  {len(data['skipped'])} files skipped"):
            for line in data["skipped"]:
                st.caption(line)
