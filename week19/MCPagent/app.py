"""
app.py
------
Streamlit front end for the smolagents-powered Dev Assistant.

Run with:
    streamlit run app.py
"""

import glob
import json
import os
import subprocess
from datetime import datetime

import streamlit as st

from week19.MCPagent.agent.orchestrator import run_goal, WORK_DIR, REPO_DIR
from week19.MCPagent.ui.report_renderer import render_report

REPORT_FILE  = os.path.join(WORK_DIR, "code_review.txt")
HISTORY_DIR  = os.path.join(WORK_DIR, "history")

GOAL_DIFF = (
    "Get the unstaged git diff. "
    "Run triage_diff on it to find smells and get fix proposals. "
    "For each changed .py file in the diff, run triage_and_fix_file "
    "to get AST-level issues and patches. "
    "Combine all findings into one report and save it to the report file."
)
GOAL_FULL = (
    "Scan every Python file in the repo. "
    "For each .py file, run triage_and_fix_file to get AST-level issues and patches. "
    "Combine all findings into one report and save it to the report file."
)

st.set_page_config(page_title="Dev Assistant", page_icon="🛠️", layout="wide")
st.title("🛠️ Agentic Dev Assistant")
st.caption("Built on smolagents · MCP tools: Git, Filesystem, lint/fix.")


def _save_history(report_text: str, mode: str, used_repo: str) -> None:
    os.makedirs(HISTORY_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%dT%H%M%S")
    record = {
        "timestamp": datetime.now().isoformat(),
        "mode":      mode,
        "repo_dir":  used_repo,
        "report_text": report_text,
    }
    path = os.path.join(HISTORY_DIR, f"{ts}.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(record, fh, indent=2)


def _load_history() -> list[dict]:
    if not os.path.isdir(HISTORY_DIR):
        return []
    files = sorted(glob.glob(os.path.join(HISTORY_DIR, "*.json")), reverse=True)
    records = []
    for f in files[:30]:
        try:
            with open(f, encoding="utf-8") as fh:
                records.append(json.load(fh))
        except Exception:
            pass
    return records


def _recent_repos() -> list[str]:
    """Unique repo paths from scan history, most recent first."""
    seen, result = set(), []
    for r in _load_history():
        p = r.get("repo_dir", "")
        if p and p not in seen and os.path.isdir(p):
            seen.add(p)
            result.append(p)
    return result


with st.sidebar:
    st.header("Repository")

    recent = _recent_repos()
    if recent:
        chosen = st.selectbox(
            "Recent repos",
            options=["(type a path below)"] + recent,
            help="Repos from previous scans. Selecting one fills the path box.",
        )
        default_path = chosen if chosen != "(type a path below)" else REPO_DIR
    else:
        default_path = REPO_DIR

    repo_path = st.text_input(
        "Repo path",
        value=default_path,
        help="Absolute path to any local git repository.",
    )

    if repo_path and not os.path.isdir(repo_path):
        st.error("Path does not exist.")
    elif repo_path and not os.path.isdir(os.path.join(repo_path, ".git")):
        git_check = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            cwd=repo_path, capture_output=True,
        )
        if git_check.returncode != 0:
            st.warning("Not a git repository — diff mode will have no changes.")
        else:
            st.caption(f"OK: {os.path.basename(repo_path)}")
    elif repo_path:
        st.caption(f"OK: {os.path.basename(repo_path)}")

    st.divider()

    st.header("Filters")

    severities = st.multiselect(
        "Show severity",
        options=["FIXABLE", "REFACTOR", "WARNING"],
        default=["FIXABLE", "REFACTOR", "WARNING"],
    )
    hide_clean = st.checkbox("Hide clean files", value=False)
    sort_by = st.selectbox(
        "Sort files by",
        options=["name", "issues_desc"],
        format_func=lambda s: "Name (A-Z)" if s == "name" else "Most issues first",
    )

filters = {
    "severities": severities,
    "hide_clean": hide_clean,
    "sort": sort_by,
}


tab_analysis, tab_history = st.tabs(["Analysis", "History"])


with tab_analysis:
    mode = st.radio(
        "Analysis mode",
        options=["diff", "full"],
        format_func=lambda m: (
            "Diff mode — only files with uncommitted changes"
            if m == "diff" else
            "Full scan — every .py file in the repo"
        ),
        horizontal=True,
    )

    goal = st.text_area(
        "Goal (editable)",
        value=GOAL_DIFF if mode == "diff" else GOAL_FULL,
        height=110,
    )

    if st.button("Run agent", type="primary"):
        with st.spinner("Agent is planning and calling tools…"):
            try:
                result = run_goal(goal, mode=mode, repo_dir=repo_path)
                st.success("Done!")
            except Exception as exc:
                st.error(f"Something went wrong: {exc}")
                st.caption("Common causes: Ollama not running, or 'uv' not installed.")
                result = None

        if result is not None and os.path.isfile(REPORT_FILE):
            report_text = open(REPORT_FILE, encoding="utf-8").read()
            _save_history(report_text, mode, used_repo=repo_path)
            st.session_state["latest_report"] = report_text
            st.session_state["latest_answer"] = str(result)

    st.divider()

    report_text = st.session_state.get("latest_report") or (
        open(REPORT_FILE, encoding="utf-8").read() if os.path.isfile(REPORT_FILE) else None
    )

    if report_text:
        col_title, col_dl = st.columns([8, 2])
        with col_title:
            st.subheader("Code Review Report")
        with col_dl:
            st.download_button(
                "Download report",
                data=report_text,
                file_name="code_review.txt",
                mime="text/plain",
            )
        render_report(report_text, filters=filters, key_prefix="analysis")

        with st.expander("Agent's final answer (raw)"):
            st.write(st.session_state.get("latest_answer", ""))
    else:
        st.info("Run the agent to see the report here.")


with tab_history:
    records = _load_history()

    if not records:
        st.info("No history yet — run the agent at least once to start tracking scans.")
    else:
        table = [
            {
                "Time":     r["timestamp"][:19].replace("T", " "),
                "Mode":     r.get("mode", "—"),
                "Repo":     os.path.basename(r.get("repo_dir", "—")),
            }
            for r in records
        ]
        st.dataframe(table, use_container_width=True, hide_index=True)

        options = [r["timestamp"][:19].replace("T", " ") for r in records]
        selected = st.selectbox("View a past report:", options)

        if selected:
            idx = options.index(selected)
            st.divider()
            render_report(records[idx]["report_text"], filters=filters, key_prefix=f"hist_{idx}")
