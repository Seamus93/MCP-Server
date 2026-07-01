from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from jarvis.supervisor import JarvisSupervisor
from orchestrator.executor import DelegationExecutor
from workflow.diff_runner import DiffRunner
from workflow.response_parser import ChatGPTResponseParser
from workflow.state_store import StateStore

mcp = FastMCP("MCP-Server")

MAX_READ_CHARS = 12_000


def _safe_path(path: str) -> Path:
    resolved = Path(path).expanduser().resolve()
    if not resolved.exists():
        raise ValueError(f"Path does not exist: {resolved}")
    return resolved


@mcp.tool()
def health_check() -> str:
    """Return a basic health status for the MCP server."""
    return "MCP-Server online"


@mcp.tool()
def git_status(repo_path: str) -> str:
    """Return short git status for a local repository."""
    repo = _safe_path(repo_path)
    result = subprocess.run(["git", "-C", str(repo), "status", "--short"], capture_output=True, text=True, timeout=20)
    return result.stdout.strip() or result.stderr.strip() or "Clean working tree"


@mcp.tool()
def list_files(root_path: str, max_files: int = 80) -> str:
    """List files under a directory, skipping common generated folders."""
    root = _safe_path(root_path)
    ignored = {".git", ".venv", "node_modules", "__pycache__", ".mcp_outbox"}
    files: list[str] = []
    for current_root, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d not in ignored]
        for name in names:
            full_path = Path(current_root) / name
            files.append(str(full_path.relative_to(root)))
            if len(files) >= max_files:
                return "\n".join(files)
    return "\n".join(files) or "No files found"


@mcp.tool()
def read_text_file(path: str, max_chars: int = MAX_READ_CHARS) -> str:
    """Read a UTF-8 text file with a character limit."""
    file_path = _safe_path(path)
    if not file_path.is_file():
        raise ValueError("Path is not a file")
    content = file_path.read_text(encoding="utf-8", errors="replace")
    return content[:max_chars]


@mcp.tool()
def run_python_tests(repo_path: str) -> str:
    """Run pytest in a local repository and return compact output."""
    repo = _safe_path(repo_path)
    result = subprocess.run(["python", "-m", "pytest", "-q"], cwd=str(repo), capture_output=True, text=True, timeout=120)
    output = (result.stdout + "\n" + result.stderr).strip()
    return output[-6000:] or "No test output"


@mcp.tool()
def plan_supervised_task(task: str) -> str:
    """Return Jarvis supervisor plan for a task."""
    return json.dumps(JarvisSupervisor().build_plan(task).to_dict(), ensure_ascii=False, indent=2)


@mcp.tool()
def gemini_task(task: str, repository: str | None = "Seamus93/MCP-Server", repo_path: str | None = None, risk_level: str = "normal", outbox_dir: str = ".mcp_outbox") -> str:
    """Primary Gemini-facing command: create the next Jarvis supervisor prompt pack."""
    return create_chatgpt_prompt_pack(task=task, repository=repository, repo_path=repo_path, risk_level=risk_level, outbox_dir=outbox_dir)


@mcp.tool()
def create_chatgpt_prompt_pack(task: str, repository: str | None = None, repo_path: str | None = None, risk_level: str = "normal", outbox_dir: str = ".mcp_outbox") -> str:
    """Create a zero-cost Jarvis supervisor prompt pack to paste manually into ChatGPT Pro."""
    executor = DelegationExecutor()
    return executor.create_manual_prompt_pack(task=task, repository=repository, repo_path=repo_path, risk_level=risk_level, outbox_dir=outbox_dir)


@mcp.tool()
def ingest_chatgpt_response(response: str, response_id: str | None = None, outbox_dir: str = ".mcp_outbox/responses") -> str:
    """Ingest a manually pasted ChatGPT response and save a structured workflow artifact."""
    parser = ChatGPTResponseParser()
    parsed = parser.parse(response)
    path = parser.save(parsed, outbox_dir=outbox_dir, response_id=response_id)
    return f"Stato: {parsed.status}\nFile salvato: {path}\nWarning: {', '.join(parsed.warnings) or 'none'}\n\n{parsed.to_json()}"


@mcp.tool()
def list_workflow_plans(outbox_dir: str = ".mcp_outbox/responses") -> str:
    """List stored workflow plan artifacts."""
    return json.dumps(StateStore(outbox_dir).list_items(), ensure_ascii=False, indent=2)


@mcp.tool()
def approve_plan(plan_path: str) -> str:
    """Mark a stored workflow plan as approved."""
    path = StateStore().update_status(plan_path, "approved")
    return f"Piano approvato: {path}"


@mcp.tool()
def verify_plan_diff(repo_path: str, plan_path: str) -> str:
    """Verify the diff embedded in a workflow artifact."""
    payload = StateStore().read(plan_path)
    diff_text = str(payload.get("patch", "")).strip()
    if not diff_text:
        raise ValueError("Il piano non contiene una patch/diff")
    return DiffRunner().verify(repo_path=repo_path, diff_text=diff_text)


@mcp.tool()
def delegate_to_chatgpt(task: str, repository: str | None = None, repo_path: str | None = None, risk_level: str = "normal") -> str:
    """Delegate a technical task through the configured API provider. Prefer gemini_task for zero-cost MVP."""
    executor = DelegationExecutor()
    return executor.delegate_task(task=task, repository=repository, repo_path=repo_path, risk_level=risk_level)


if __name__ == "__main__":
    mcp.run()
