"""
orchestrator.py
---------------
The brain of the Dev Assistant, built on the smolagents framework.

Supports two LLM backends — set MODEL in .env to switch:
  Groq (cloud):  groq/llama-3.3-70b-versatile   (needs GROQ_API_KEY)
  Ollama (local): ollama/llama3.2                (needs Ollama running locally,
                                                  no API key required)

A typical run: read the git diff -> triage it for smells + patches ->
triage changed files for logic issues + patches -> write combined report.
"""

import os
import logging
import subprocess

from typing import Any

from dotenv import load_dotenv
from mcp import StdioServerParameters
from smolagents import MCPClient, CodeAgent, ToolCallingAgent, LiteLLMModel

# ---------------------------------------------------------------------------
# Config (env-based) — never hard-code secrets.
# ---------------------------------------------------------------------------
load_dotenv()
MODEL = os.environ.get("MODEL", os.environ.get("GROQ_MODEL", "groq/llama-3.3-70b-versatile"))
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")

# GROQ_API_KEY is only required for Groq-hosted models.
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
if not MODEL.startswith("ollama/") and not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is required when not using an Ollama model. "
                     "Set it in .env or switch to MODEL=ollama/<model-name>.")


def _resolve_repo_dir(configured: str) -> str:
    """Return the git root for a given path.

    mcp-server-git requires the path to be the root of a git repo (where .git
    lives). If the user points REPO_DIR at a subdirectory, walk up to find the
    actual root automatically.
    """
    start = os.path.abspath(configured) if configured.strip() else os.path.abspath(".")
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=start, capture_output=True, text=True,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return start


# The git repo the assistant will analyze.
REPO_DIR = _resolve_repo_dir(os.environ.get("REPO_DIR", "."))
# Folder the Filesystem server is allowed to write reports into.
WORK_DIR = os.environ.get("SCOUT_WORK_DIR", os.path.abspath("./reports"))

# ---------------------------------------------------------------------------
# Observability — basic logging so each run is traceable.
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
log = logging.getLogger("scout")


# ---------------------------------------------------------------------------
# Define the three servers. Each entry says how to LAUNCH that server locally.
# smolagents' MCPClient takes a list of these and connects to all of them.
# ---------------------------------------------------------------------------
def server_specs(repo_dir: str) -> list[StdioServerParameters | dict[str, Any]]:
    os.makedirs(WORK_DIR, exist_ok=True)
    return [
        # Third-party server #1: Git — reads the repo's log, status, and diffs.
        StdioServerParameters(
            command="uvx",
            args=["--quiet", "mcp-server-git", "--repository", repo_dir],
            env={**os.environ},
        ),
        # Third-party server #2: Filesystem — writes the report into WORK_DIR.
        StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem", WORK_DIR],
            env={**os.environ},
        ),
        # Custom server: triage + fix proposals for diffs and full files.
        StdioServerParameters(
            command="python",
            args=[os.path.join(os.path.dirname(__file__), "..", "mcp_servers", "lint_fix_server.py")],
            env={**os.environ},
        ),
    ]


def run_goal(goal, mode: str = "diff", repo_dir: str | None = None):
    """Connect to all servers, build the agent, and run the goal.

    mode:     "diff" — analyze only unstaged changed .py files (default)
              "full" — analyze every .py file in the repo tree
    repo_dir: override the REPO_DIR from .env at runtime (UI repo selector).

    Returns the agent's final answer (a string).
    """
    if MODEL.startswith("ollama/"):
        model = LiteLLMModel(model_id=MODEL, api_base=OLLAMA_BASE_URL)
        log.info("Using local Ollama model: %s  (%s)", MODEL, OLLAMA_BASE_URL)
    else:
        model = LiteLLMModel(model_id=MODEL)
        log.info("Using cloud model: %s", MODEL)

    resolved   = _resolve_repo_dir(repo_dir if repo_dir else REPO_DIR)
    report_file = os.path.join(WORK_DIR, "code_review.txt").replace("\\", "/")
    repo_dir    = resolved.replace("\\", "/")

    sandbox_vars = {
        "REPO_PATH":   repo_dir,
        "REPORT_FILE": report_file,
    }

    common_header = (
        f"These Python variables are already defined in your environment:\n"
        f"  REPO_PATH   = '{repo_dir}'\n"
        f"  REPORT_FILE = '{report_file}'\n\n"
        f"IMPORTANT: Every tool returns a plain string — never index results with ['key'].\n"
        f"You MUST end every response with a <code> block. "
        f"Never write 'Final Answer:' as plain text — always call final_answer() inside code.\n\n"
    )

    if mode == "full":
        script = (
            f"Use this exact script — copy it verbatim into ONE code block:\n"
            f"  import glob\n"
            f"  py_files = glob.glob(REPO_PATH + '/**/*.py', recursive=True)\n"
            f"  report = f'Full repo scan: {{len(py_files)}} Python files\\n\\n'\n"
            f"  for filepath in py_files:\n"
            f"      fix = triage_and_fix_file(filepath=filepath)\n"
            f"      report += fix + '\\n\\n'\n"
            f"  write_file(path=REPORT_FILE, content=report)\n"
            f"  final_answer('Report saved to ' + REPORT_FILE)\n\n"
        )
    else:
        script = (
            f"Use this exact script — copy it verbatim into ONE code block:\n"
            f"  diff = git_diff_unstaged(repo_path=REPO_PATH)\n"
            f"  triage_result = triage_diff(diff=diff)\n"
            f"  report = triage_result\n"
            f"  for line in diff.split('\\n'):\n"
            f"      if line.startswith('+++ b/') and '.py' in line:\n"
            f"          rel = line[6:].strip()\n"
            f"          fix = triage_and_fix_file(filepath=REPO_PATH + '/' + rel)\n"
            f"          report += '\\n\\n' + fix\n"
            f"  write_file(path=REPORT_FILE, content=report)\n"
            f"  final_answer('Report saved to ' + REPORT_FILE)\n\n"
        )

    preamble = common_header + script + "TASK:\n"

    with MCPClient(server_specs(resolved), structured_output=False) as tools:
        log.info("Connected to MCP servers — %d tools discovered.", len(tools))
        for t in tools:
            log.info("  tool available: %s", t.name)

        if MODEL.startswith("ollama/"):
            agent = CodeAgent(tools=tools, model=model, max_steps=6,
                              additional_authorized_imports=[
                                  "os", "os.path", "ntpath", "posixpath",
                                  "glob", "pathlib", "fnmatch",
                              ])
        else:
            agent = ToolCallingAgent(tools=tools, model=model, max_steps=6)
        result = agent.run(preamble + goal, additional_args=sandbox_vars)
        log.info("Agent finished.")
        return result
