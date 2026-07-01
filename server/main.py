from __future__ import annotations

import os
import subprocess
from pathlib import Path

from mcp.server.fastmcp import FastMCP

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
    result = subprocess.run(
        ["git", "-C", str(repo), "status", "--short"],
        capture_output=True,
        text=True,
        timeout=20,
    )
    return result.stdout.strip() or result.stderr.strip() or "Clean working tree"


@mcp.tool()
def list_files(root_path: str, max_files: int = 80) -> str:
    """List files under a directory, skipping common generated folders."""
    root = _safe_path(root_path)
    ignored = {".git", ".venv", "node_modules", "__pycache__"}
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
    result = subprocess.run(
        ["python", "-m", "pytest", "-q"],
        cwd=str(repo),
        capture_output=True,
        text=True,
        timeout=120,
    )
    output = (result.stdout + "\n" + result.stderr).strip()
    return output[-6000:] or "No test output"


if __name__ == "__main__":
    mcp.run()
