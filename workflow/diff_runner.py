from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path


class DiffRunner:
    def verify(self, repo_path: str, diff_text: str) -> str:
        return self._run(repo_path, diff_text, dry=True)

    def write(self, repo_path: str, diff_text: str) -> str:
        return self._run(repo_path, diff_text, dry=False)

    def _run(self, repo_path: str, diff_text: str, dry: bool) -> str:
        repo = Path(repo_path).resolve()
        if not repo.exists():
            raise ValueError("Repository path not found")
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".diff", delete=False) as handle:
            handle.write(diff_text)
            diff_path = handle.name
        cmd = ["git", "-C", str(repo), "apply"]
        if dry:
            cmd.append("--check")
        cmd.append(diff_path)
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            output = (result.stdout + "\n" + result.stderr).strip()
            if result.returncode != 0:
                raise ValueError(output or "diff command failed")
            return output or ("diff verified" if dry else "diff written")
        finally:
            Path(diff_path).unlink(missing_ok=True)
