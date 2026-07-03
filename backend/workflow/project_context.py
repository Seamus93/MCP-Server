from __future__ import annotations

from pathlib import Path


DEFAULT_CONTEXT_FILES = [
    "README.md",
    "AGENTS.md",
    ".skills/README.md",
    "docs/PROJECT_OVERVIEW.md",
    "docs/ARCHITECTURE.md",
    "docs/ROADMAP.md",
    "docs/API.md",
    "docs/SECURITY.md",
    "docs/PM_STATUS.md",
]


class ProjectContextLoader:
    def __init__(self, max_chars_per_file: int = 6000) -> None:
        self.max_chars_per_file = max_chars_per_file

    def load(self, repo_path: str, files: list[str] | None = None) -> str:
        root = Path(repo_path).resolve()
        if not root.exists():
            return f"Repository path not found: {root}"
        selected_files = files or DEFAULT_CONTEXT_FILES
        chunks: list[str] = []
        for relative_path in selected_files:
            path = root / relative_path
            if not path.exists() or not path.is_file():
                continue
            content = path.read_text(encoding="utf-8", errors="replace")[: self.max_chars_per_file]
            chunks.append(f"## {relative_path}\n\n{content}")
        if not chunks:
            return "No standard context files found."
        return "\n\n---\n\n".join(chunks)
