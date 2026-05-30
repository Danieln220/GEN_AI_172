# Agentic Dev Assistant

A Streamlit app that uses **smolagents + MCP** to automatically review a Python codebase, propose concrete fixes, and save a report.

## How it works

Three MCP servers run in one agent loop:

| Server | What it does |
|---|---|
| `mcp-server-git` | reads git diffs and repo status |
| `@modelcontextprotocol/server-filesystem` | writes the report to disk |
| `mcp_servers/lint_fix_server.py` | AST analysis — finds smells, proposes patches |

The agent (smolagents `CodeAgent` or `ToolCallingAgent`) plans the tool call sequence itself.

## What the linter catches

| Severity | Checks |
|---|---|
| **FIXABLE** | mutable defaults, bare/empty except, builtin shadowing (param + var) |
| **REFACTOR** | long functions, too many params, high complexity, deep nesting |
| **WARNING** | dead imports, hardcoded paths, missing type hints, no docstring, stub functions |

Diff mode also checks: debug prints, TODOs, hardcoded secrets, long lines, leftover breakpoints, commented-out code.

## Setup

1. Install Node.js, Python 3.10+, and `uv`:
   ```
   pip install uv
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Configure `.env`:
   ```
   # Cloud (Groq)
   MODEL=groq/llama-3.3-70b-versatile
   GROQ_API_KEY=your_key_here

   # or Local (Ollama)
   MODEL=ollama/qwen2.5-coder:14b
   OLLAMA_BASE_URL=http://localhost:11434

   REPO_DIR=C:\path\to\repo\to\analyze
   ```
4. Run:
   ```
   streamlit run app.py
   ```

## Features

- **Two scan modes** — diff only (uncommitted changes) or full repo scan
- **Apply Fix** — click a button to patch FIXABLE issues directly in the source file
- **Filters** — show/hide by severity, hide clean files, sort by issue count
- **History** — every scan is saved; browse and compare past reports

## Project structure

```
MCPagent/
├── app.py                  ← Streamlit UI entry point
├── agent/orchestrator.py   ← Agent setup, model config, preamble
├── mcp_servers/
│   └── lint_fix_server.py  ← Custom MCP server (triage_diff + triage_and_fix_file)
├── ui/report_renderer.py   ← Parses and renders the report in Streamlit
├── utils/fix_applier.py    ← Applies FIXABLE patches to source files on disk
└── tests/test_tools.py     ← 33 unit tests (run: python tests/test_tools.py)
```

## Running tests

```
python tests/test_tools.py
```
